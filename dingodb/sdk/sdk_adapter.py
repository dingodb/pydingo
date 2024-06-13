#!/usr/bin/python3

from dingosdk import dingo_store

from dingodb.common.rep import (
    ScalarType,
    ScarlarValue,
    ScalarData,
    Vector,
    VectorWithId,
    VectorValueType,
    SearchResult,
    VectorWithDistance,
    MetricType,
    IndexMetric,
)

from typing import List, Dict

sdk_value_type_to_vector_value_type = {
    dingo_store.ValueType.kFloat: VectorValueType.FLOAT,
    dingo_store.ValueType.kUint8: VectorValueType.BINARY,
}

sdk_type_to_scalar_type = {
    dingo_store.Type.kBOOL: ScalarType.BOOL,
    dingo_store.Type.kINT64: ScalarType.INT64,
    dingo_store.Type.kDOUBLE: ScalarType.DOUBLE,
    dingo_store.Type.kSTRING: ScalarType.STRING,
}

sdk_metric_type_to_metric_type = {
    dingo_store.MetricType.kL2: MetricType.L2,
    dingo_store.MetricType.kInnerProduct: MetricType.INNER_PRODUCT,
    dingo_store.MetricType.kCosine: MetricType.COSINE,
}


def sdk_scalar_fields_to_fields_list(
    scalar_type: ScalarType, sdk_scalar_fileds: List
) -> list:
    if scalar_type == ScalarType.BOOL:
        return [x.bool_data for x in sdk_scalar_fileds]
    elif scalar_type == ScalarType.INT64:
        return [x.long_data for x in sdk_scalar_fileds]
    elif scalar_type == ScalarType.DOUBLE:
        return [x.double_data for x in sdk_scalar_fileds]
    elif scalar_type == ScalarType.STRING:
        return [x.string_data for x in sdk_scalar_fileds]
    else:
        raise RuntimeError(f"Unknown scalar type {scalar_type}")


def sdk_scalar_value_to_scalar_value(
    sdk_scalar_value: dingo_store.ScalarValue,
) -> ScarlarValue:
    return ScarlarValue(
        scalar_type=sdk_type_to_scalar_type[sdk_scalar_value.type],
        fields=sdk_scalar_fields_to_fields_list(
            sdk_type_to_scalar_type[sdk_scalar_value.type], sdk_scalar_value.fields
        ),
    )


def sdk_scalar_data_to_scalar_data(
    sdk_scalar_data: Dict,
) -> ScalarData:
    scalar_data = ScalarData()
    for key, value in sdk_scalar_data.items():
        scalar_data.add_scalar_value(key, sdk_scalar_value_to_scalar_value(value))

    return scalar_data


def sdk_vector_with_id_to_vector_with_id(
    sdk_vector_with_id: dingo_store.VectorWithId,
) -> VectorWithId:
    return VectorWithId(
        id=sdk_vector_with_id.id,
        vector=Vector(
            dimension=sdk_vector_with_id.vector.dimension,
            value_type=sdk_value_type_to_vector_value_type[
                sdk_vector_with_id.vector.value_type
            ],
            float_values=sdk_vector_with_id.vector.float_values,
            binary_values=sdk_vector_with_id.vector.binary_values,
        ),
        scalar_data=sdk_scalar_data_to_scalar_data(sdk_vector_with_id.scalar_data),
    )


def sdk_vector_with_distance_to_vector_with_distance(
    sdk_vector_with_distance: dingo_store.VectorWithDistance,
) -> VectorWithDistance:
    return VectorWithDistance(
        vector_with_id=sdk_vector_with_id_to_vector_with_id(
            sdk_vector_with_distance.vector_data
        ),
        distance=sdk_vector_with_distance.distance,
        metric_type=sdk_metric_type_to_metric_type[
            sdk_vector_with_distance.metric_type
        ],
    )


def sdk_search_result_to_search_result(
    sdk_search_result: dingo_store.SearchResult,
) -> SearchResult:
    return SearchResult(
        vector_with_distance_list=[
            sdk_vector_with_distance_to_vector_with_distance(x)
            for x in sdk_search_result.vector_datas
        ]
    )


def sdk_index_metrics_result_to_index_metric(
    sdk_index_metrics_result: dingo_store.IndexMetricsResult,
) -> IndexMetric:
    return IndexMetric(
        index_type=dingo_store.VectorIndexTypeToString(
            sdk_index_metrics_result.index_type
        ),
        count=sdk_index_metrics_result.count,
        deleted_count=sdk_index_metrics_result.deleted_count,
        max_vector_id=sdk_index_metrics_result.max_vector_id,
        min_vector_id=sdk_index_metrics_result.min_vector_id,
        memory_bytes=sdk_index_metrics_result.memory_bytes,
    )
