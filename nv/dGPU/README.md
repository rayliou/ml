
- How to uninstall 3-party driver
  
  ```
  disable_nouveau () {
    sudo bash -c "echo blacklist nouveau > /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
    sudo bash -c "echo options nouveau modeset=0 >> /etc/modprobe.d/blacklist-nvidia-nouveau.conf"
    cat /etc/modprobe.d/blacklist-nvidia-nouveau.conf
    sudo update-initramfs -u
}
```
