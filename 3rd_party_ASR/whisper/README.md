
# Install the latest version of the fast whisper.
```
pip uninstall faster-whisper
rm  -fr   /home/xiaorui/anaconda3/lib/python3.8/site-packages/PyYAML-5.3.1-py3.8.egg-info
rm  -fr   /home/xiaorui/anaconda3/lib/python3.8/site-packages/mpmath*
pip install --force-reinstall "faster-whisper @ https://github.com/guillaumekln/faster-whisper/archive/refs/heads/master.tar.gz"
```

# FYI
```
https://github.com/guillaumekln/faster-whisper
https://github.com/guillaumekln/faster-whisper/blob/master/faster_whisper/transcribe.py

Issues
- https://github.com/guillaumekln/faster-whisper/issues/147
```
