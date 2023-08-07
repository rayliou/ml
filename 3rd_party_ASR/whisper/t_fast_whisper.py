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


model_size = "small"
model_size = "base"
model = WhisperModel(model_size, device="auto", compute_type="float32")

def configure_logger(name, level=logging.DEBUG):
    """
    Configure a logger with a given name and level.
    Args:
    - name (str): Name of the logger.
    - level (int): Logging level (e.g., logging.DEBUG).
    Returns:
    - logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Check if handlers already exist. If they do, avoid adding more to prevent duplicate logs.
    if not logger.handlers:
        handler = logging.StreamHandler()
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def main(read_time_ms=200):
    configure_logger("faster_whisper",logging.WARNING)
    logger = configure_logger("main")


    class ASR_AudioStreamHandler(AudioStreamHandler):
        def __init__(self, rate=16000, bits=16):
            super().__init__(rate, bits)
        def preheat_model(self):
            return
            # Preheat model with 3 second of zeros (numpy float32 data)
            audio_3s = np.load("./10s_16khz.npy")
            self.handle_audio_segment(audio_3s, 0)
            dummy_audio_segment = np.zeros(self.rate_*3, dtype=np.float32)  # 1 second of zeros
            self.handle_audio_segment(dummy_audio_segment , 0)
            self.logger.info("Model preheated successfully!")

        def handle_audio_segment(self, audio_segment, abs_start):

            self.logger.info("Start transcribe")
            segments, info = model.transcribe(audio_segment, beam_size=5, language = "en",
                                              vad_filter=True,
                                              condition_on_previous_text=False, word_timestamps=True,temperature=0.1)
            #self.logger.info(info)
            cnt_s = 0
            for segment in segments:
                cnt_w = 0
                #self.logger.info(f"[{segment.start}:{segment.end}]:{segment.text}")
                for w in segment.words:
                    if w.probability < 0.15:
                        continue
                    self.logger.info(f"seg:word[{cnt_s}:{cnt_w}];abs_start:{self.abs_start_*1000/self.rate_}ms;[{w.start}:{w.end}]:{w.probability:.3f}\t{w.word}")
                    cnt_w +=1
                cnt_s +=1
            #print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
            pass

    hrAudio = ASR_AudioStreamHandler()
    hrAudio.logger.setLevel(logging.INFO)
    hrAudio.preheat_model()

    read_size_bytes = read_time_ms * 2 * hrAudio.rate_ // 1000  # convert ms to bytes
    cnt = 0
    file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_answer_call.wav"
    file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav"
    file_path = "/home/xiaorui/W/deepgram/10secs_english_speech.wav"
    logger.info(f"Start recognize the file {file_path}")
    with open(file_path, 'rb') as f:  # open the file in binary mode
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

