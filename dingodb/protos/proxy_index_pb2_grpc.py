# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proxy_index_pb2 as proxy__index__pb2


class IndexServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VectorAdd = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorAdd',
                request_serializer=proxy__index__pb2.VectorAddRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorAddResponse.FromString,
                )
        self.VectorGet = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorGet',
                request_serializer=proxy__index__pb2.VectorGetRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorGetResponse.FromString,
                )
        self.VectorSearch = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorSearch',
                request_serializer=proxy__index__pb2.VectorSearchRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorSearchResponse.FromString,
                )
        self.VectorDelete = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorDelete',
                request_serializer=proxy__index__pb2.VectorDeleteRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorDeleteResponse.FromString,
                )
        self.VectorGetBorderId = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorGetBorderId',
                request_serializer=proxy__index__pb2.VectorGetBorderIdRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorGetBorderIdResponse.FromString,
                )
        self.VectorScanQuery = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorScanQuery',
                request_serializer=proxy__index__pb2.VectorScanQueryRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorScanQueryResponse.FromString,
                )
        self.VectorGetRegionMetrics = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorGetRegionMetrics',
                request_serializer=proxy__index__pb2.VectorGetRegionMetricsRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorGetRegionMetricsResponse.FromString,
                )
        self.VectorCount = channel.unary_unary(
                '/dingodb.pb.proxy.index.IndexService/VectorCount',
                request_serializer=proxy__index__pb2.VectorCountRequest.SerializeToString,
                response_deserializer=proxy__index__pb2.VectorCountResponse.FromString,
                )


class IndexServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def VectorAdd(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorGet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorSearch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorDelete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorGetBorderId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorScanQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorGetRegionMetrics(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VectorCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IndexServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'VectorAdd': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorAdd,
                    request_deserializer=proxy__index__pb2.VectorAddRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorAddResponse.SerializeToString,
            ),
            'VectorGet': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorGet,
                    request_deserializer=proxy__index__pb2.VectorGetRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorGetResponse.SerializeToString,
            ),
            'VectorSearch': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorSearch,
                    request_deserializer=proxy__index__pb2.VectorSearchRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorSearchResponse.SerializeToString,
            ),
            'VectorDelete': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorDelete,
                    request_deserializer=proxy__index__pb2.VectorDeleteRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorDeleteResponse.SerializeToString,
            ),
            'VectorGetBorderId': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorGetBorderId,
                    request_deserializer=proxy__index__pb2.VectorGetBorderIdRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorGetBorderIdResponse.SerializeToString,
            ),
            'VectorScanQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorScanQuery,
                    request_deserializer=proxy__index__pb2.VectorScanQueryRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorScanQueryResponse.SerializeToString,
            ),
            'VectorGetRegionMetrics': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorGetRegionMetrics,
                    request_deserializer=proxy__index__pb2.VectorGetRegionMetricsRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorGetRegionMetricsResponse.SerializeToString,
            ),
            'VectorCount': grpc.unary_unary_rpc_method_handler(
                    servicer.VectorCount,
                    request_deserializer=proxy__index__pb2.VectorCountRequest.FromString,
                    response_serializer=proxy__index__pb2.VectorCountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dingodb.pb.proxy.index.IndexService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IndexService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def VectorAdd(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorAdd',
            proxy__index__pb2.VectorAddRequest.SerializeToString,
            proxy__index__pb2.VectorAddResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorGet',
            proxy__index__pb2.VectorGetRequest.SerializeToString,
            proxy__index__pb2.VectorGetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorSearch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorSearch',
            proxy__index__pb2.VectorSearchRequest.SerializeToString,
            proxy__index__pb2.VectorSearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorDelete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorDelete',
            proxy__index__pb2.VectorDeleteRequest.SerializeToString,
            proxy__index__pb2.VectorDeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorGetBorderId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorGetBorderId',
            proxy__index__pb2.VectorGetBorderIdRequest.SerializeToString,
            proxy__index__pb2.VectorGetBorderIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorScanQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorScanQuery',
            proxy__index__pb2.VectorScanQueryRequest.SerializeToString,
            proxy__index__pb2.VectorScanQueryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorGetRegionMetrics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorGetRegionMetrics',
            proxy__index__pb2.VectorGetRegionMetricsRequest.SerializeToString,
            proxy__index__pb2.VectorGetRegionMetricsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VectorCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dingodb.pb.proxy.index.IndexService/VectorCount',
            proxy__index__pb2.VectorCountRequest.SerializeToString,
            proxy__index__pb2.VectorCountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
