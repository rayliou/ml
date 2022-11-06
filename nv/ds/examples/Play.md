#  RTSP Play
```
gst-launch-1.0 uridecodebin uri=rtsp://192.168.0.140:8554/ds-test ! nvoverlaysink

mplayer rtsp://192.168.0.140:8554/ds-test

```

