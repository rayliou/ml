#!/home/xiaorui/anaconda3/bin/python3
"""
https://github.com/guillaumekln/faster-whisper
https://github.com/guillaumekln/faster-whisper/blob/master/faster_whisper/transcribe.py
"""
from faster_whisper import WhisperModel
import logging
import numpy as np
import librosa


logger = logging.getLogger('main')
log_level = getattr(logging, "DEBUG")
logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


model_size = "base"
# Run on GPU with FP16
model = WhisperModel(model_size, device="auto", compute_type="float32")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

file_path = "/home/xiaorui/W/deepgram/10secs_english_speech.wav"
audio_data, sr = librosa.load(file_path, sr=None, mono=True)
print(audio_data)
#audio_data = np.clip(audio_data, -1, 1)
samples_per_second = sr  # sample rate is the number of samples in one second
samples_per_two_seconds = samples_per_second * 2  # two seconds

logger.info(f"Start processing the file {file_path}")
start = 0
end = samples_per_second
# Iterate over the audio data with a stride of one second
while end <= len(audio_data):
    segment = audio_data[start:end]
    segments, info = model.transcribe(segment, beam_size=5,condition_on_previous_text=False,word_timestamps=True)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    # Move the start and end points by one second
    start = end
    end = end + samples_per_second

logger.info("After detecting")
