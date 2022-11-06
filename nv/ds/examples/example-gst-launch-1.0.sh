#!/bin/bash
set -ex
# https://developer.ridgerun.com/wiki/index.php/Raspberry_Pi_HQ_camera_IMX477_Linux_driver_for_Jetson#Downloading_the_debian_packages
export SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
export FRAMERATE=60 # Framerate can go from 2 to 60 for 1920x1080 mode
gst-launch-1.0 nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvvidconv ! nvoverlaysink


# Example Pipelines
# Find some example pipelines to use the IMX477 on Jetson Xavier NX below:

display() {
    SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
    FRAMERATE=60 # Framerate can go from 2 to 60 for 1920x1080 mode
#1920x1080
    gst-launch-1.0 nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvvidconv ! nvoverlaysink
#4032x3040
    gst-launch-1.0 nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=4032,height=3040,framerate=$FRAMERATE/1" ! nvvidconv ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvoverlaysink

}
mp4_recording () {
    SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
    FRAMERATE=60 # Framerate can go from 2 to 60 for 1920x1080 mode
#1920x1080
    gst-launch-1.0 -e nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=rpi_v3_imx477_cam$SENSOR_ID.mp4
#4032x3040
    gst-launch-1.0 -e nvarguscamerasrc sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=4032,height=3040,framerate=$FRAMERATE/1" ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=rpi_v3_imx477_cam$SENSOR_ID.mp4
}
jpg_snapshots () {
    SENSOR_ID=0 # 0 for CAM0 and 1 for CAM1 ports
    FRAMERATE=60 # Framerate can go from 2 to 60 for 1920x1080 mode
    NUMBER_OF_SNAPSHOTS=20
#1920x1080
    gst-launch-1.0 -e nvarguscamerasrc num-buffers=$NUMBER_OF_SNAPSHOTS sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$FRAMERATE/1" ! nvjpegenc ! multifilesink location=%03d_rpi_v3_imx477_cam$SENSOR_ID.jpeg
#4032x3040
    gst-launch-1.0 -e nvarguscamerasrc num-buffers=$NUMBER_OF_SNAPSHOTS sensor-id=$SENSOR_ID ! "video/x-raw(memory:NVMM),width=4032,height=3040,framerate=$FRAMERATE/1" ! nvjpegenc ! multifilesink location=%03d_rpi_v3_imx477_cam$SENSOR_ID.jpeg
}

