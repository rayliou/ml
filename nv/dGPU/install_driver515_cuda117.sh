#!/bin/bash
set -ex

# Installing Multiple CUDA & cuDNN Versions in Ubuntu
# https://towardsdatascience.com/installing-multiple-cuda-cudnn-versions-in-ubuntu-fcb6aa5194e2




driver_515 () {
    wget "https://us.download.nvidia.com/XFree86/Linux-x86_64/515.76/NVIDIA-Linux-x86_64-515.76.run"
    chmod a+x ./NVIDIA-Linux-x86_64-515.76.run
    sudo ./NVIDIA-Linux-x86_64-515.76.run
}
cuda_117 () {
    # https://developer.nvidia.com/cuda-11-7-1-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=18.04&target_type=runfile_local

    wget https://developer.download.nvidia.com/compute/cuda/11.7.1/local_installers/cuda_11.7.1_515.65.01_linux.run
    sudo sh cuda_11.7.1_515.65.01_linux.run

# sudo sh cuda_11.7.1_515.65.01_linux.run
# ===========
# = Summary =
# ===========
#
# Driver:   Not Selected
# Toolkit:  Installed in /usr/local/cuda-11.7/
#
# Please make sure that
#  -   PATH includes /usr/local/cuda-11.7/bin
#  -   LD_LIBRARY_PATH includes /usr/local/cuda-11.7/lib64, or, add /usr/local/cuda-11.7/lib64 to /etc/ld.so.conf and run ldconfig as root
#
# To uninstall the CUDA Toolkit, run cuda-uninstaller in /usr/local/cuda-11.7/bin
# ***WARNING: Incomplete installation! This installation did not install the CUDA Driver. A driver of version at least 515.00 is required for CUDA 11.7 functionality to work.
# To install the driver using this installer, run the following command, replacing <CudaInstaller> with the name of this run file:
#     sudo <CudaInstaller>.run --silent --driver
#
# Logfile is /var/log/cuda-installer.log




}
pytorch_for_cuda117 () {
    #
    # https://pytorch.org/get-started/locally/
    pip3 install torch torchvision torchaudio

}
#driver_515
cuda_117

