#!/bin/bash

# https://docs.nvidia.com/metropolis/deepstream/5.1/dev-guide/text/DS_Quickstart.html#dgpu-setup-for-ubuntu


# Setup pre-requisites:
# - Ubuntu 18.04
# - Gstreamer 1.14.1
# - NVIDIA driver 440+
# - CUDA 11.1
# - TensorRT 7.2+


t() {
	echo dddd
}
kafka_install() {
	 set -ex
	 git clone https://github.com/edenhill/librdkafka.git && cd librdkafka &&  git reset --hard 7101c2310341ab3f4675fc565f64f0967e135a6a && ./configure && make && sudo make install
	 sudo mkdir -p /opt/nvidia/deepstream/deepstream-5.1/lib &&  sudo cp /usr/local/lib/librdkafka* /opt/nvidia/deepstream/deepstream-5.1/lib
	 rm -fr librdkafka
}
cuda_install() {
	#Download and install Cuda-11.1 from nvidia website
	# https://developer.nvidia.com/cuda-11.1.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal
	set -ex
	wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
	sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
	wget https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda-repo-ubuntu1804-11-1-local_11.1.0-455.23.05-1_amd64.deb
	sudo dpkg -i cuda-repo-ubuntu1804-11-1-local_11.1.0-455.23.05-1_amd64.deb
	sudo apt-key add /var/cuda-repo-ubuntu1804-11-1-local/7fa2af80.pub
	sudo apt-get update
	sudo apt-get -y install cuda

	echo 1;
}

trr_install() {
	#Download and install TensorRT 7.2.1 from nvidia website
	# https://developer.nvidia.com/nvidia-tensorrt-download
	# https://developer.nvidia.com/compute/machine-learning/tensorrt/secure/7.2.1/local_repos/nv-tensorrt-repo-ubuntu1804-cuda11.1-trt7.2.1.6-ga-20201007_1-1_amd64.deb
	#nv-tensorrt-repo-ubuntu1804-cuda11.1-trt7.2.1.6-ga-20201007_1-1_amd64.deb
	set -ex
	os="ubuntu1804"
	tag="cuda11.1-trt7.2.1.6-ga-20201007"
	sudo dpkg -i nv-tensorrt-repo-${os}-${tag}_1-1_amd64.deb
	sudo apt-key add /var/nv-tensorrt-repo-${tag}/7fa2af80.pub
	sudo apt-get update
	sudo apt-get install -y tensorrt
	sudo apt-get install -y python-libnvinfer-dev
	sudo apt-get install -y python3-libnvinfer-dev
	sudo apt-get install -y uff-converter-tf
	sudo apt-get install -y  onnx-graphsurgeon
	dpkg -l | grep TensorRT

}
docker_install() {
	# https://docs.nvidia.com/ai-enterprise/deployment-guide/dg-docker.html#enabling-the-docker-repository-and-installing-the-nvidia-container-toolkit
	set -ex
	sudo apt-get update
	sudo apt-get install -y \
	    apt-transport-https \
	    ca-certificates \
	    curl \
	    gnupg-agent \
	    software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository \
	   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	   $(lsb_release -cs) \
	   stable"
	sudo apt-get update
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io
	sudo docker run hello-world


	distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
	curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
	curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
	sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
	sudo service docker restart
	sudo docker run --gpus all nvidia/cuda:11.0-base nvidia-smi

}
ds_install () {
	set -xe
	#sudo tar -xvf deepstream_sdk_v5.1.0_x86_64.tbz2 -C /
	pushd /opt/nvidia/deepstream/deepstream-5.1/
	sudo ./install.sh
	sudo ldconfig
	popd
}

#cuda_install
#trr_install ;
docker_install;
#kafka_install
#ds_install
