- [Nvidia docker Container Runtimes](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#container-runtimes)
- 
# Reset docker config and switch docker context
```
rm -vf  ~/.docker/config.json &&  docker context use desktop-linux
docker logout socrates.azurecr.io
echo "Plain password" | docker login socrates.azurecr.io --username socrates --password-stdin


```
