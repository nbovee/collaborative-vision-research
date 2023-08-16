import os
import sys
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models
import time
import pandas as pd
import atexit
from collections import OrderedDict
import uuid
import copy
from torchinfo import summary
from torchinfo.layer_info import LayerInfo


class HookExitException(Exception):
    """Exception to early exit from inference in naive running."""

    def __init__(self, out, *args: object) -> None:
        super().__init__(*args)
        self.result = out


class WrappedModel(nn.Module):
    """Wraps a pretrained model with the features necesarry to perform edge computing tests. Uses pytorch
    hooks to perform benchmarkings, grab intermediate layers, and slice the Sequential to provide input to intermediate layers or exit early.
    """

    layer_template_dict = {
        "layer_id": None, # this one may prove unneeded
        "class": None,
        "inference_time": None,
        "parameters": None,
        "parameter_bytes": None,
        # "precision": None, precision is not technically per layer, disabled for now
        "cpu_cycles_used": None,
        "watts_used": None,
    }

    def __init__(self, *args, **kwargs):
        print(*args)
        super().__init__(*args)
        self.timer = time.perf_counter_ns
        self.master_dict = kwargs.get("dict", {}) # this should be the externally accessible dict
        self.inference_dict = {} # collation dict for the current partition of a given inference
        self.forward_dict = {} # dict for the results from the current forward pass
        self.device = kwargs.get("device", "cpu")
        self.mode = kwargs.get("mode","eval")
        self.hook_depth = kwargs.get("depth", np.inf)
        self.base_input_size = kwargs.get("image_size", (3, 224, 224))
        atexit.register(self.safeClose)
        self.pretrained = kwargs.pop("pretrained", models.alexnet(pretrained=True))
        self.splittable_layer_count = 0
        self.selected_out = OrderedDict()  # could be useful for skips
        self.f_hooks = []
        self.f_pre_hooks = []
       
        # run torchinfo here to get parameters/flops/mac for entry into dict      
        self.torchinfo = summary(self.pretrained, (1, *self.base_input_size), verbose=0)
        self.walk_modules(self.pretrained.children(), 1) # depth starts at 1 to match torchinfo depths
        del self.torchinfo
        self.empty_buffer_dict = copy.deepcopy(self.forward_dict)
       
        # ---- class scope values that the hooks and forward pass use ----
        self.current_module_stop_index = None
        self.current_module_index = None
        
        # inference will never be started below this layer, watch if pruned.
        self.start_layer_index = 0
        
        # will not perform inference at this layer or above, watch if pruned.
        self.max_ignore_layer_index = self.splittable_layer_count - 1
        

        if self.mode == "eval":
            self.pretrained.eval()
        if self.device == "cuda":
            if torch.cuda.is_available():
                print("Loading Model to CUDA.")
            else:
                print("Loading Model to CPU. CUDA not available.")
                self.device = "cpu"
        self.pretrained.to(self.device)
        self.warmup(iterations=2)

    def walk_modules(self, module_generator, depth):
        """Recursively walks and marks Modules for hooks in a DFS. Most NN have an intended or intuitive depth to split at, but it is not obvious to the naive program."""
        for child in module_generator:
            if len(list(child.children())) > 0 and depth < self.hook_depth:
                # either has children we want to look at, or is max depth
                print(
                    f"{'-'*depth}Module {str(child).split('(')[0]} with children found, hooking children instead of module."
                )
                self.walk_modules(child.children(), depth + 1)
                print(
                    f"{'-'*depth}End of Module {str(child).split('(')[0]}'s children."
                )
            elif isinstance(child, nn.Module):
                # if not iterable/too deep, we have found a layer to hook
                
                for layer in self.torchinfo.summary_list:
                    if layer.layer_id == id(child):
                        break
                if layer.layer_id != id(child):
                    raise Exception("module id not find while adding hooks.")
                self.forward_dict[self.splittable_layer_count] = copy.deepcopy(WrappedModel.layer_template_dict)
                self.forward_dict[self.splittable_layer_count]["depth"] = depth
                # block of data from torchinfo
                self.forward_dict[self.splittable_layer_count]["layer_id"] = self.splittable_layer_count
                self.forward_dict[self.splittable_layer_count]["class"] = layer.class_name
                self.forward_dict[self.splittable_layer_count]["precision"] = None
                self.forward_dict[self.splittable_layer_count]["parameters"] = layer.num_params
                self.forward_dict[self.splittable_layer_count]["parameter_bytes"] = layer.param_bytes
                self.forward_dict[self.splittable_layer_count]["input_size"] = layer.input_size
                self.forward_dict[self.splittable_layer_count]["output_size"] = layer.output_size
                self.forward_dict[self.splittable_layer_count]["output_bytes"] = layer.output_bytes

                self.f_hooks.append(
                    child.register_forward_pre_hook(
                        self.forward_prehook(
                            self.splittable_layer_count,
                            str(child).split("(")[0],
                            (0, 0),
                        ),
                        with_kwargs=False,
                    )
                )
                self.f_pre_hooks.append(
                    child.register_forward_hook(
                        self.forward_posthook(
                            self.splittable_layer_count,
                            str(child).split("(")[0],
                            (0, 0),
                        ),
                        with_kwargs=False,
                    )
                )
                print(
                    f"{'-'*depth}Layer {self.splittable_layer_count}: {str(child).split('(')[0]} hooks applied."
                )
                # back hooks left out for now
                self.splittable_layer_count += 1

    def forward_prehook(self, layer_index, layer_name, input_shape):
        """Prehook a layer for benchmarking."""

        def pre_hook(module, args):
            if self.log:
                self.forward_dict[layer_index]['inference_time'] = -self.timer()
            self.current_module_index += 1
            # print(f"L{layer_index}-{layer_name} called.")
            # print(f"val. {self.current_module_index}")

        return pre_hook

    def forward_posthook(self, layer_index, layer_name, input_shape, **kwargs):
        """Posthook a layer for output capture and benchmarking."""

        def hook(module, args, output):
            if self.log:
                self.forward_dict[layer_index]['inference_time'] += self.timer()
            if (
                layer_index >= self.current_module_stop_index - 1
                and layer_index < self.max_ignore_layer_index - 1
            ):
                raise HookExitException(output)
            # print(f"stop at layer: {self.current_module_stop_index -1}")
            # print(f"L{layer_index}-{layer_name} returned.")

        return hook

    def enforce_bounds(self, start, end):
        start = self.start_layer_index if start < self.start_layer_index else start
        end = self.max_ignore_layer_index if end > self.max_ignore_layer_index else end
        if start >= end:
            raise Exception("Start and End indexes overlap.")
        return start, end

    def forward(self, x, inference_id = None, start=0, end=np.inf, log=True):
        """Wraps the pretrained forward pass to utilize our slicing."""
        start, end = self.enforce_bounds(start, end)
        self.log = log
        self.current_module_stop_index = end
        self.current_module_index = 0
        inference_id = uuid.uuid4() if inference_id is None else inference_id
        self.inference_dict['inference_id'] = str(inference_id)+'.0'
        # forward values generated by hooks go to an buffer dict, which is cleard after each complete pass
        try:
            if self.mode != "train":
                with torch.no_grad():
                    out = self.pretrained(x)
            else:
                out = self.pretrained(x)
        except HookExitException as e:
            print("Exit early from hook.")
            out = e.result

        self.inference_dict['layer_information'] = self.forward_dict
        if log:
            self.master_dict[inference_id] = copy.deepcopy(self.inference_dict) # only one deepcopy needed
        self.inference_dict = {}
        self.forward_dict = copy.deepcopy(self.empty_buffer_dict)

        # reset hook variables
        self.current_module_stop_index = None
        self.current_module_index = None
        return out

    def parse_input(self, input):
        """Checks if the input is appropriate at the given stage of the network. Does not yet check Tensor shapes for intermediate layers."""
        if isinstance(input, Image.Image):
            if input.size != self.base_input_size:
                input = input.resize(self.base_input_size)
            input_tensor = self.preprocess(input)
            input_tensor = input_tensor.unsqueeze(0)
        elif isinstance(input, torch.Tensor):
            input_tensor = input
        if (
            torch.cuda.is_available()
            and self.mode == "cuda"
            and input_tensor.device != self.mode
        ):
            input_tensor = input_tensor.to(self.mode)
        return input_tensor

    def warmup(self, iterations=50, force=False):
        if self.device != "cuda" and force is not False:
            print("Warmup not required.")
        else:
            print("Starting warmup.")
            with torch.no_grad():
                for i in range(iterations):
                    self(torch.randn(1, *self.base_input_size), log = False)
            print("Warmup complete.")

    def prune_layers(newlow, newhigh):
        """NYE: Trim network layers. inputs specify the lower and upper layers to REMAIN. Used to attempt usage on low compute power devices, such as early Raspberry Pi models."""
        raise NotImplementedError

    def safeClose(self):
        torch.cuda.empty_cache()


if __name__ == "__main__":
    # running as main will test baselines on the running platform
    m = WrappedModel()
    for k, v in m.master_dict.items():
        print(f"{k}:\n")
        for i, j in v.items():
            if i == "layer_information":
                for x, y in j.items():
                    print(f"{x} : {y}")
            else:   
                print(f"{i} : {j}")
