import rpyc
import uuid
from rpyc.utils.server import ThreadedServer
from rpyc.utils.helpers import classpartial

class ParticipantService(rpyc.Service):
    def __init__(self, ident, input_dict) -> None:
        self.indent = ident
        self.results_dict = input_dict

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_inference(self, uuid): # this is an exposed method
        matches = [k for k, v in self.results_dict if uuid in k]
        result = None
        for match in matches:
            result.append(self.results_dict.pop(match))
        return result
    

# rpc_service = classpartial(ParticipantService) # decoupled early just in case
# node1 = ThreadedServer(rpc_service, port=18861) # rpyc 4.0+ only, single server for all incoming requests to Node to reduce overhead