#!/home/xiaorui/anaconda3/bin/python3
from whisper_live.client import TranscriptionClient
host = "127.0.0.1"
port = 9090
client = TranscriptionClient(host, port, is_multilingual=True,translate=True)
client("/home/xiaorui/W/deepgram/10secs_english_speech.wav")
