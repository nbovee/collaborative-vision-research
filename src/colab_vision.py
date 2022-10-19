from bz2 import compress
from concurrent import futures
from email import message
import enum
from fileinput import filename
from logging.handlers import WatchedFileHandler
from multiprocessing.connection import wait
import sys
import logging
import os
import io
import grpc
# from timeit import default_timer as timer
import time
# from time import perf_counter_ns as timer, process_time_ns as cpu_timer
from time import time as timer
import uuid
import pickle
import blosc
import numpy as np
from PIL import Image

sys.path.append(".")
parent = os.path.abspath('.')
sys.path.insert(1, parent)

from alexnet_pytorch_split import Model
from test_data import test_data_loader as data_loader

import colab_vision_pb2
import colab_vision_pb2_grpc


bitrate = 0.1 * 2 ** 20# byte/s
compression = False
CHUNK_SIZE = 1024 #reduce size for testing * 1024  # 1MB
# this should probably be an independant database that client and server can both interact with async
results_dict = {}

def get_object_chunks(object):
    object = pickle.dumps(object)
    for pos in range(0, len(object), CHUNK_SIZE):
        piece = object[pos:pos + CHUNK_SIZE]
        if len(piece) == 0:
            return
        yield colab_vision_pb2.Chunk(chunk=piece)

def save_chunks_to_object(chunks):
    chunk_byte_list = []
    for c in chunks:
        chunk_byte_list.append(c.chunk)
    obj_bytes = b''.join(chunk_byte_list)
    return obj_bytes

def inference_generator(data_loader):
    while data_loader.has_next():
        [ current_obj, exit_layer, filename ] = data_loader.next()
        message = colab_vision_pb2.Info_Chunk()
        message.action = colab_vision_pb2.Action()
        message.id = uuid.UUID()
        results_dict[message.id] = {}
        results_dict[message.id]["filename"] = filename
        # getting split layer should be broken out and methodized
        # for current_split_layer in range(1, Model.max_layers + 1): # we will be iterating over split layers to generate test results. 0 = server handles full inference (tbi). Max_layers + 1 = client handles full inference (tbi)
        message.layer = exit_layer + 1 # the server begins inference 1 layer above where the edge exited
        #split into chunks, set values, add message to messages list
        if compress:
            message.action.append(5)
            current_obj = blosc.compress(current_obj)
        for i, piece in enumerate(get_object_chunks(current_obj)):
            message.chunk = piece
            if i == 0:
                message.action.append(1)
            if piece is None: #current behavior will send the entirety of the current_obj, then when generator ends, follow up with action flags. small efficiency boost possible if has_next is altered
                message.action.append(3)
            yield message

class FileClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = colab_vision_pb2_grpc.colab_visionStub(channel)

    def initiateConstantInference(self, target):
        #stuff
        for received_msg in self.stub.constantInference(inference_generator(target)):
            print("Received message from server with contents: ")
            for i in received_msg:
                print(i)
            results_dict[received_msg.pop(id)] = received_msg
        return None

class FileServer(colab_vision_pb2_grpc.colab_visionServicer):
    def __init__(self):

        class Servicer(colab_vision_pb2_grpc.colab_visionServicer):
            def __init__(self):
                self.tmp_folder = './temp/'
                # self.model = Model()
            
            def constantInference(self, request_iterator, context):
                #unpack msg contents
                current_chunks = []
                last_id = None
                for msg in request_iterator:
                    print("Received message from client with contents: ")
                    for thingy in msg:
                        print(thingy)
                    if 4 in msg.action:
                        break #exit
                    if 1 in msg.action:
                        #reset operation regardless of current progress
                        current_chunks = []
                        last_id = msg.layer
                    if msg.id == last_id:
                        current_chunks.append(msg.chunk)
                        #continue the same inference
                    else:
                        current_chunks = [].append(msg.chunk)
                    #continue the same inference
                    if 2 in msg.action: 
                        #convert chunks into object and save at appropriate layer
                        current_chunks = save_chunks_to_object(current_chunks)
                        if 5 in msg.action: # decompress
                            current_chunks = blosc.decompress(current_chunks)
                        pickle.loads(current_chunks)
                        pass #not yet implemented
                    if 3 in msg.action:
                        #convert chunks into object and perform inference
                        if 5 in msg.action: # decompress
                            current_chunks = blosc.decompress(current_chunks)
                        pickle.loads(current_chunks)
                        pass
                        
                    
                #deal with chunks

                #do flag actions
                pass

        logging.basicConfig()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        colab_vision_pb2_grpc.add_colab_visionServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()
        self.server.wait_for_termination()
