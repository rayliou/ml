DS_VER=6.0

######### Troubleshooting
# https://stackoverflow.com/questions/58851228/gstreamer-camera-usage-within-docker-containers

################ Models
# https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nvidiaai
# Computer Vision models

# PeopleNet: Three class object detection network to detect people in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
# ActionRecognitionNet: 5 class network to recognize what people are doing in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/actionrecognitionnet
# TafficCamNet: Four class object detection network to detect cars in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/trafficcamnet

DISPLAY=:1

DIR_WORK=/opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/configs/tlt_pretrained_models
DOCKER_CMD=sudo docker run --gpus all -it --rm -v $(PWD):/opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/models/tlt_pretrained_models \
	-w $(DIR_WORK)
CAMERA= --privileged --device /dev/video0
DOCKER_CMD+= --ipc=host -v /tmp/argus_socket:/tmp/argus_socket --cap-add SYS_PTRACE 

#CAMERA= -v /dev/video0:/dev/video0
BINDS=  -v ${PWD}/data_src:/data_src
BINDS+= -v ${PWD}/tlt_pretrained_models/:${DIR_WORK}
BINDS+= -v ${PWD}/data_src/deepstream_app_source1_peoplenet.txt:${DIR_WORK}/deepstream_app_source1_peoplenet.txt
BINDS+= -v ${PWD}/data_src/6.0.1-deepstream_app_source1_trafficcamnet.txt:${DIR_WORK}/deepstream_app_source1_trafficcamnet.txt
BINDS+= -p 8554:8554 -p 8400:8400/udp

GUI= --net=host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$(DISPLAY)
GUI=
# Jetson
#IMG=nvcr.io/nvidia/deepstream-l4t:5.1-21.02-samples 
IMG=nvcr.io/nvidia/deepstream-l4t:6.0.1-samples 
# dGPU
#IMG=nvcr.io/nvidia/deepstream:$(DS_VER)-21.02-samples

CMD=deepstream-app --gst-debug=2
#CMD=$(IMG) cat deepstream_app_source1_trafficcamnet.txt


trafficcamnet:${PWD}/trafficcamnet xhost
	#$(DOCKER_CMD) $(BINDS) $(GUI) $(CAMERA) $(IMG) deepstream-app -c deepstream_app_source1_trafficcamnet.txt  #--gst-debug=3
	$(DOCKER_CMD) $(BINDS) $(GUI)  $(CAMERA) $(IMG) deepstream-app -c deepstream_app_source1_trafficcamnet.txt  --gst-debug=3
bash:xhost
	$(DOCKER_CMD) $(BINDS) $(GUI)  $(CAMERA) $(IMG) bash

${PWD}/trafficcamnet  :
	mkdir -p $@ && \
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/resnet18_trafficcamnet_pruned.etlt \
	-O $@/resnet18_trafficcamnet_pruned.etlt && \
	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/trafficnet_int8.txt \
	-O $@/trafficnet_int8.txt

clean:
	rm -fr ${PWD}/trafficcamnet

xhost:
	echo xhost +

#GUI=

show:xhost
	$(DOCKER_CMD) $(BINDS) $(GUI) $(CMD)


# peopleNet() {
# 	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/peoplenet
# 	#set -ex
# 	#mkdir -p ${PWD}/peoplenet && \
# 	#wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/peoplenet/versions/pruned_v2.1/files/resnet34_peoplenet_pruned.etlt -O ${PWD}/peoplenet/resnet34_peoplenet_pruned.etlt
# 
# 	## Run Application
# 
# 	xhost +
# 	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v ${PWD}:/opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/models/tlt_pretrained_models \
# 	-w /opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:$(DS_VER)-21.02-samples \
# 	 deepstream-app -c deepstream_app_source1_peoplenet.txt --gst-debug=4
# }
# VehicleMakeNet () {
# 	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/vehiclemakenet
# 	## Download Model:
# 	set -ex
# 	rm -fr  ${PWD}/vehiclemakenet  && mkdir -p ${PWD}/vehiclemakenet
# 	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/vehiclemakenet/versions/pruned_v1.0/files/resnet18_vehiclemakenet_pruned.etlt \
# 		-O ${PWD}/vehiclemakenet/resnet18_vehiclemakenet_pruned.etlt && \
# 	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/vehiclemakenet/versions/pruned_v1.0/files/vehiclemakenet_int8.txt \
# 		-O ${PWD}/vehiclemakenet/vehiclemakenet_int8.txt
# 	## Run Application
# 	xhost +
# 	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v ${PWD}:/opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/models/tlt_pretrained_models \
# 	-w /opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:$(DS_VER)-21.02-samples \
# 	deepstream-app -c deepstream_app_source1_dashcamnet_vehiclemakenet_vehicletypenet.txt --gst-debug=3
# 
# 
# }
# 
# TrafficCamNet () {
# 	# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/trafficcamnet
# 	## Download Model:
# 	set -ex
# 	mkdir -p ${PWD}/trafficcamnet && \
# 	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/resnet18_trafficcamnet_pruned.etlt \
# 	-O ${PWD}/trafficcamnet/resnet18_trafficcamnet_pruned.etlt && \
# 	wget https://api.ngc.nvidia.com/v2/models/nvidia/tao/trafficcamnet/versions/pruned_v1.0/files/trafficnet_int8.txt \
# 	-O ${PWD}/trafficcamnet/trafficnet_int8.txt
# 
# 	## Run Application
# 
# 	xhost +
# 	sudo docker run --gpus all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v ${PWD}:/opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/models/tlt_pretrained_models \
# 	-w /opt/nvidia/deepstream/deepstream-$(DS_VER)/samples/configs/tlt_pretrained_models nvcr.io/nvidia/deepstream:$(DS_VER)-21.02-samples \
# 	 deepstream-app -c deepstream_app_source1_trafficcamnet.txt  --gst-debug=3
# 
# 
# }
# ActionRecognitionNet () {
# 	# ActionRecognitionNet: 5 class network to recognize what people are doing in an image. https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/actionrecognitionnet
# 	set -ex
# }
all: 
	echo Please run:
	echo make TrafficCamNet 
# #peopleNet;
# #VehicleMakeNet ;
# TrafficCamNet 
# 
# 
#
play:
	DISPLAY=$(DISPLAY) gst-launch-1.0 uridecodebin uri=rtsp://192.168.0.140:8554/ds-test ! nvoverlaysink
sync:
	cd  ~ && rsync  -Pazvru --delete v2-nv data_src     'henry@192.168.0.126:~'
