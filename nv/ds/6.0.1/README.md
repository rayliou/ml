
- [Docs » Application Migration to DeepStream 6.0 from DeepStream 5.X](https://docs.nvidia.com/metropolis/deepstream/6.0/dev-guide/text/DS_Application_migration.html)
    ```
     cp -afr /home/henry/Downloads/opt_deepstream_sdk_v5.1.0_jetson/nvidia/deepstream/deepstream-5.1/samples/configs/tlt_pretrained_models .

    mkdir /opt/nvidia/deepstream/deepstream-5.1
    mkdir /opt/nvidia/deepstream/deepstream-5.1/lib
    ln -s /opt/nvidia/deepstream/deepstream-6.0/lib/* /opt/nvidia/deepstream/deepstream-5.1/lib/
    ```
  - Low-level Object Tracker Library Migration from DeepStream 5.1 Apps to DeepStream 6.0
- https://stackoverflow.com/questions/58851228/gstreamer-camera-usage-within-docker-containers
