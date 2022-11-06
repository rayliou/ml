# Reboot into recovery mode
If the Jetson is fully booted, then this command should reboot into recovery mode: 
https://forums.developer.nvidia.com/t/jetson-agx-xavier-soft-reset-to-enter-recovery-mode/186603
```
sudo reboot --force forced-recovery
```

## Debug Tools

```
sudo apt install  -y iftop ranger fd-find ncdu htop smem v4l-utils tmux ripgrep libjson-glib-dev
```

