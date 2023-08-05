#!/home/xiaorui/anaconda3/bin/python3
from whisper_live.server import TranscriptionServer
server = TranscriptionServer()
server.run("0.0.0.0", 9090)
