#!/bin/bash



if [ $# -ne 1 ]; then
    echo "Please run $0 test_azure_iotedge_sync|test_azure_iotedge_async"
    exit 1;
fi

set -ex
cd /opt/nvidia/deepstream/deepstream-6.0/sources/libs/azure_protocol_adaptor/module_client
make -f Makefile.test
/opt/nvidia/deepstream/deepstream-6.0/sources/libs/azure_protocol_adaptor/module_client/$1 /opt/nvidia/deepstream/deepstream/lib/libnvds_azure_edge_proto.so
#/opt/nvidia/deepstream/deepstream-6.0/sources/libs/azure_protocol_adaptor/module_client/test_azure_iotedge_sync /opt/nvidia/deepstream/deepstream/lib/libnvds_azure_edge_proto.so


