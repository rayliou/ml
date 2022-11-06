1. [Intelligent-Video-Analytics-with-NVIDIA-Jetson-and-Microsoft-Azure](https://github.com/toolboc/Intelligent-Video-Analytics-with-NVIDIA-Jetson-and-Microsoft-Azure)
  - https://www.youtube.com/watch?v=yZz-4uOx_Js
1. [Intelligent-Video-Analytics-with-NVIDIA-Jetson-and-Microsoft-Azure](https://github.com/toolboc/Intelligent-Video-Analytics-with-NVIDIA-Jetson-and-Microsoft-Azure)
1. [NVIDIA Deepstream + Azure IoT Edge on a NVIDIA Jetson Nano ](https://github.com/Azure-Samples/NVIDIA-Deepstream-Azure-IoT-Edge-on-a-NVIDIA-Jetson-Nano)
1. [Azure Stream Analytics on IoT Edge](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-edge?WT.mc_id=julyot-iva-pdecarlo)



(https://forums.developer.nvidia.com/t/could-not-receive-message-from-the-deepstreamsdk-module-on-azure-iot-edge-sink-type-6/226421/4)

Actually, I have ever mounted **/etc/aziot/config.toml**  on host to the docker container, but it also didn't work. I'm wondering if I'm experiencing compatibility issues between the latest host azure IoT  edge environments and our azure edge adapter (**msg-broker-proto-lib=/opt/nvidia/deepstream/deepstream-5.1/lib/libnvds_azure_edge_proto.so**).
