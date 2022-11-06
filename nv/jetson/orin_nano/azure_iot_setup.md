

## Setup conda and  Azure IoT Edge Dev Tool
- https://github.com/Azure/iotedgedev
```
wget  "https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh"
chmod a+x ./Anaconda3-2024.06-1-Linux-x86_64.sh
./Anaconda3-2024.06-1-Linux-x86_64.sh
conda init zsh
exit # Reenter the terminal
conda create -n py3.8.10-iotedge python=3.8.10
pip install azure-iot-device~=2.12.0 colorlog~=6.7.0 aio-pika~=9.3.0 azure-storage-blob~=12.18.3 janus lib-platform~=1.2.10 requests~=2.31.0 opencv-python~=4.9.0.80 piexif~=1.1.3
pip install iotedgedev
```

## Build Azure IoT Solution

```
 iotedgedev solution build -P arm64v8   -f ./deployment.default.template.json
```

