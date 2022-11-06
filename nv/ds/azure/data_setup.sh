#!/bin/bash
set -ex

sudo mkdir -p /var/deepstream/custom_configs
cd   /var/deepstream
sudo git clone https://github.com/Azure-Samples/NVIDIA-Deepstream-Azure-IoT-Edge-on-a-NVIDIA-Jetson-Nano
sudo chmod -R 777 /var/deepstream
cd /var/deepstream/custom_configs


