#!/home/xiaorui/anaconda3/bin/python3
"""
https://github.com/guillaumekln/faster-whisper
https://github.com/guillaumekln/faster-whisper/blob/master/faster_whisper/transcribe.py
"""
import sys

from faster_whisper import WhisperModel
import logging
import numpy as np
import librosa
from audio_stream_handler import AudioStreamHandler

"""
logger = logging.getLogger('main')
log_level = getattr(logging, "DEBUG")
logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
"""


model_size = "base"
model = WhisperModel(model_size, device="auto", compute_type="float32")

def main(read_time_ms=200):
    logger = logging.getLogger('main')
    log_level = getattr(logging, "DEBUG")
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    class ASR_AudioStreamHandler(AudioStreamHandler):
        def handle_audio_segment(self, audio_segment,abs_start):
            segments, info = model.transcribe(audio_segment, beam_size=5, language = "en", condition_on_previous_text=True, word_timestamps=True)
            cnt_s = 0
            for segment in segments:
                cnt_w = 0
                for w in segment.words:
                    if w.probability < 0.15:
                        continue
                    self.logger.info(f"seg:word[{cnt_s}:{cnt_w}];abs_start:{self.abs_start_*1000/self.rate_}ms;[{w.start}:{w.end}]:{w.probability:.3f}\t{w.word}")
                    cnt_w +=1
                cnt_s +=1
                #self.logger.info(f"[abs_start_ms:{self.abs_start_*1000/self.rate_}]ms[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            #print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
            pass
    hrAudio = ASR_AudioStreamHandler()
    hrAudio.logger.setLevel(logging.INFO)

    read_size_bytes = read_time_ms * 2 * hrAudio.rate_ // 1000  # convert ms to bytes
    cnt = 0
    filt_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav"
    filt_path = "/home/xiaorui/W/deepgram/10secs_english_speech.wav"
    logger.info(f"Start recognize the file {filt_path}")
    with open(filt_path, 'rb') as f:  # open the file in binary mode
        while True:
            stream_data = f.read(read_size_bytes)  # read from the file
            if not stream_data:
                hrAudio.finish()
                break
            start = cnt * read_time_ms
            cnt += 1
            end = cnt * read_time_ms
            #logger.debug(f"process_stream_data({len(stream_data)}, {start},{end})")
            hrAudio.process_stream_data(stream_data)

main(); sys.exit(0)

"""
    read_size_bytes = read_time_ms * 2 * hrAudio.rate_ // 1000  # convert ms to bytes
    cnt = 0
    while True:
        stream_data = sys.stdin.buffer.read(read_size_bytes)  # read data from stdin
        if not stream_data:
            break
        start = cnt *read_time_ms
        cnt+=1
        end = cnt *read_time_ms
        #logger.debug(f"process_stream_data({start},{end})")
        hrAudio.process_stream_data(stream_data)
"""

"""
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
"""
