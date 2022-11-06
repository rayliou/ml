sudo apt-get install v4l-utils
v4l2-ctl --list-devices
sudo v4l2-ctl --list-devices



IMX477 – How to install the Driver
https://www.arducam.com/docs/camera-for-jetson-nano/native-jetson-cameras-imx219-imx477/imx477-how-to-install-the-driver/

    wget https://github.com/ArduCAM/MIPI_Camera/releases/download/v0.0.3/install_full.sh
    chmod +x install_full.sh
    ./install_full.sh -m imx477

    sudo dpkg -r arducam-nvidia-l4t-kernel


