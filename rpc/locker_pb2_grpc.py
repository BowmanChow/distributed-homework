# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import locker_pb2 as locker__pb2


class LockerStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Lock = channel.unary_unary(
                '/locker.Locker/Lock',
                request_serializer=locker__pb2.LockRequest.SerializeToString,
                response_deserializer=locker__pb2.LockReply.FromString,
                )


class LockerServicer(object):
    """The greeting service definition.
    """

    def Lock(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LockerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Lock': grpc.unary_unary_rpc_method_handler(
                    servicer.Lock,
                    request_deserializer=locker__pb2.LockRequest.FromString,
                    response_serializer=locker__pb2.LockReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'locker.Locker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Locker(object):
    """The greeting service definition.
    """

    @staticmethod
    def Lock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/locker.Locker/Lock',
            locker__pb2.LockRequest.SerializeToString,
            locker__pb2.LockReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
