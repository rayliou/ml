*****************************************************************************
* Copyright (c) 2018-2020 NVIDIA Corporation.  All rights reserved.
*
* NVIDIA Corporation and its licensors retain all intellectual property
* and proprietary rights in and to this software, related documentation
* and any modifications thereto.  Any use, reproduction, disclosure or
* distribution of this software and related documentation without an express
* license agreement from NVIDIA Corporation is strictly prohibited.
*****************************************************************************

================================================================================
DeepStream SDK
================================================================================
Setup pre-requisites:
- Ubuntu 18.04
- Gstreamer 1.14.1
- NVIDIA driver 440+
- CUDA 11.1
- TensorRT 7.2+

--------------------------------------------------------------------------------
Package Contents
--------------------------------------------------------------------------------
The DeepStream packages include:
1. sources - Sources for sample application and plugin
2. samples - Config files, Models, streams and tools to run the sample app

Note for running with docker
-----------------------------
While running DeepStream with docker, necessary packages are already pre-installed.
Hence please skip the installation steps and proceed to "Running the samples" section of this document.

--------------------------------------------------------------------------------
Installing Pre-requisites:
--------------------------------------------------------------------------------
Packages to be installed:
$ sudo apt-get install \
    libssl1.0.0 \
    libgstreamer1.0-0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libgstrtspserver-1.0-0 \
    libjansson4 \
    libjson-glib-1.0-0

CUDA 11.1
--------
Download and install Cuda-11.1 from nvidia website
https://developer.nvidia.com/cuda-toolkit-archive

TensorRT 7.2+
-------------
Download and install TensorRT 7.2.1 from nvidia website
https://developer.nvidia.com/nvidia-tensorrt-download

Create symlink for libnvcuvid.so:
---------------------------------
sudo ln -s /usr/lib/nvidia-<driver-version>/libnvcuvid.so \
    /usr/lib/x86_64-linux-gnu/libnvcuvid.so

-------------------------------------------------------------------------------
Using Kafka protocol adaptor with message broker
-------------------------------------------------------------------------------
Refer README file availabe under sources/libs/kafka_protocol_adaptor for
detailed documentation on prerequisites and usages of kafka protocol
adaptor with message broker plugin for sending messages to cloud.

Refer source code and README of deepstream-test4 available under
sources/apps/sample_apps/deepstream-test4/ to send messages to the cloud.

-----------------------------------------------------------------------
Using azure MQTT protocol adaptor with message broker
-----------------------------------------------------------------------
Refer README files availabe under sources/libs/azure_protocol_adaptor for
detailed documentation on prerequisites and usages of azure MQTT protocol
adaptor with message broker plugin for sending messages to cloud.

Refer source code and README of deepstream-test4 available under
sources/apps/sample_apps/deepstream-test4/ to send messages to the cloud.

--------------------------------------------------------------------------
[Optional] Uninstall DeepStream 3.0
---------------------------------------------------------------------------
To uninstall any previously installed DeepStream 3.0 libraries, run the following command.

sudo rm -rf /usr/local/deepstream /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libnvdsgst_* \
            /usr/lib/x86_64-linux-gnu/gstreamer-1.0/libgstnv* \
            /usr/bin/deepstream*

--------------------------------------------------------------------------
[Optional] Uninstall DeepStream 4.0
---------------------------------------------------------------------------
To uninstall any previously installed DeepStream 4.0 libraries, use uninstall.sh script.

1. Open the uninstall.sh file which will be present in /opt/nvidia/deepstream/deepstream/
2. Set PREV_DS_VER as 4.0
3. Run the script as sudo ./uninstall.sh

Note that this will run only for DeepStreamSDK versions equal to or above 4.0.

--------------------------------------------------------------------------------
Extract and Install DeepStream SDK
--------------------------------------------------------------------------------
1. Untar deepstream_sdk_v5.1.0_x86_64.tbz2
   sudo tar -xvf deepstream_sdk_v5.1.0_x86_64.tbz2 -C /
2. The samples, sources and install script will be found in:
   /opt/nvidia/deepstream/deepstream-5.1/
3. Run the install.sh script as follows:
   sudo ./install.sh

--------------------------------------------------------------------------------
Running the samples
--------------------------------------------------------------------------------
1. Go to samples directory and run
   deepstream-app -c <path to config.txt>
2. Application config files included in `configs/deepstream-app/`
   a. source30_1080p_dec_infer-resnet_tiled_display_int8.txt (30 Decode + Infer)
   b. source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt
      (4 Decode + Infer + SGIE + Tracker)
   c. source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8_gpu1.txt
      (4 Decode + Infer + SGIE + Tracker executed on gpu1)
3. Configuration files for "nvinfer" element in `configs/deepstream-app/`
   a. config_infer_primary.txt (Primary Object Detector)
   b. config_infer_secondary_carcolor.txt (Secondary Car Color Classifier)
   c. config_infer_secondary_carmake.txt (Secondary Car Make Classifier)
   d. config_infer_secondary_vehicletypes.txt (Secondary Vehicle Type Classifier)

--------------------------------------------------------------------------------
Running the Triton Inference Server samples
--------------------------------------------------------------------------------

Instructions to prepare and run Triton inference server samples
are provided in samples/configs/deepstream-app-trtis/README.

--------------------------------------------------------------------------------
Downloading and Running the Pre-trained Transfer Learning Toolkit Models
--------------------------------------------------------------------------------
Instructions to download and run the pre-trained Transfer Learning Toolkit models
are provided in samples/configs/tlt_pretrained_models/README.

--------------------------------------------------------------------------------
Notes:
--------------------------------------------------------------------------------
1. If the application runs into errors, cannot create gst elements, try again
after removing gstreamer cache
   rm ${HOME}/.cache/gstreamer-1.0/registry.x86_64.bin
2. When running deepstream for first time, the following warning might show up:
   "GStreamer-WARNING: Failed to load plugin '...libnvdsgst_inferserver.so':
    libtrtserver.so: cannot open shared object file: No such file or directory"
This is a harmless warning indicating that the DeepStream's nvinferserver plugin
cannot be used since "Triton Inference Server" is not installed.
If required, try DeepStream's TRT-IS docker image or install the Triton Inference
Server manually. For more details, refer to https://github.com/NVIDIA/triton-inference-server.
