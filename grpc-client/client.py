import grpc
import gate_pb2
import gate_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:3002')
    stub = gate_pb2_grpc.GateServiceStub(channel)
    response = stub.masuk(gate_pb2.MasukRequest(idkartu=1212121212, idgate=5))
    return response.status

print(run())
