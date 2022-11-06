#!/bin/bash

# https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nvidiaai
# Computer Vision models

# PeopleNet: Three class object detection network to detect people in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
# ActionRecognitionNet: 5 class network to recognize what people are doing in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/actionrecognitionnet
# TafficCamNet: Four class object detection network to detect cars in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/trafficcamnet




peopleNet() {
	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
	#set -ex
	#mkdir -p $HOME/peoplenet && \
	#wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplenet/versions/pruned_v2.1/files/resnet34_peoplenet_pruned.etlt -O $HOME/peoplenet/resnet34_peoplenet_pruned.etlt

	## Run Application

	xhost +
	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v $HOME:/opt/nvidia/deepstream/deepstream-5.1/samples/models/tlt_pretrained_models \
	-w /opt/nvidia/deepstream/deepstream-5.1/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:5.1-21.02-samples \
	 deepstream-app -c deepstream_app_source1_peoplenet.txt --gst-debug=4
}
VehicleMakeNet () {
	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/vehiclemakenet
	## Download Model:
	set -ex
	rm -fr  $HOME/vehiclemakenet  && mkdir -p $HOME/vehiclemakenet
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/vehiclemakenet/versions/pruned_v1.0/files/resnet18_vehiclemakenet_pruned.etlt \
		-O $HOME/vehiclemakenet/resnet18_vehiclemakenet_pruned.etlt && \
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/vehiclemakenet/versions/pruned_v1.0/files/vehiclemakenet_int8.txt \
		-O $HOME/vehiclemakenet/vehiclemakenet_int8.txt
	## Run Application
	xhost +
	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v $HOME:/opt/nvidia/deepstream/deepstream-5.1/samples/models/tlt_pretrained_models \
	-w /opt/nvidia/deepstream/deepstream-5.1/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:5.1-21.02-samples \
	deepstream-app -c deepstream_app_source1_dashcamnet_vehiclemakenet_vehicletypenet.txt --gst-debug=3


}

TrafficCamNet () {
	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/trafficcamnet
	## Download Model:
	set -ex
	mkdir -p $HOME/trafficcamnet && \
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/resnet18_trafficcamnet_pruned.etlt \
	-O $HOME/trafficcamnet/resnet18_trafficcamnet_pruned.etlt && \
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/trafficnet_int8.txt \
	-O $HOME/trafficcamnet/trafficnet_int8.txt

	## Run Application

	xhost +
	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v $HOME:/opt/nvidia/deepstream/deepstream-5.1/samples/models/tlt_pretrained_models \
	-w /opt/nvidia/deepstream/deepstream-5.1/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:5.1-21.02-samples \
	 deepstream-app -c deepstream_app_source1_trafficcamnet.txt  --gst-debug=3


}
ActionRecognitionNet () {
	# ActionRecognitionNet: 5 class network to recognize what people are doing in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/actionrecognitionnet
	set -ex
}

#peopleNet;
#VehicleMakeNet ;
TrafficCamNet 


