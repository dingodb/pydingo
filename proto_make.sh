#!/bin/bash

OUTDIR=dingodb/protos/
PROTO_DIR="dingodb/protos/dingo-proto/proto"

python -m pip install "grpcio-tools==$(python3 -c 'import grpc; print(grpc.__version__)')"

python -m grpc_tools.protoc -I ${PROTO_DIR} --python_out=${OUTDIR} --pyi_out=${OUTDIR} ${PROTO_DIR}/*.proto

echo "Success to generate the python proto files."
