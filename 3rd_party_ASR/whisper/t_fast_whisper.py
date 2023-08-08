#!/home/xiaorui/anaconda3/bin/python3
"""
https://github.com/guillaumekln/faster-whisper
https://github.com/guillaumekln/faster-whisper/blob/master/faster_whisper/transcribe.py

Issues
- https://github.com/guillaumekln/faster-whisper/issues/147
"""
import sys

from faster_whisper import WhisperModel
import logging
import numpy as np
import librosa
import re

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
            self.last_word_in_prev_seg_ = None
            self.text_ = ""
            self.prepad_secs_ = 0.2
            self.padding_segment_ = np.zeros(int(self.rate_* self.prepad_secs_), dtype=np.float32)

        def preheat_model(self):
            return
            # Preheat model with 3 second of zeros (numpy float32 data)
            audio_3s = np.load("./10s_16khz.npy")
            self.handle_audio_segment(audio_3s, 0)
            dummy_audio_segment = np.zeros(self.rate_*3, dtype=np.float32)  # 1 second of zeros
            self.handle_audio_segment(dummy_audio_segment , 0)
            self.logger.info("Model preheated successfully!")

        def update_output(self,w, abs_start=-1):
            prefix = "Last word in previous segment" if abs_start == -1 else f"Abs_start:{self.abs_start_ * 1.0 / self.rate_}s"
            w_start = w.start - self.prepad_secs_
            w_end = w.end - self.prepad_secs_
            self.logger.info(
                f"{prefix}:[{w_start:.2f}:{w_end:.2f}]:{w.probability:.3f}\t[{w.word}]")
            #self.text_ += " "
            self.text_ += w.word

        def handle_audio_segment(self, audio_segment, abs_start):
            audio_segment = np.concatenate((self.padding_segment_, audio_segment))
            #Save to wave file
            super().handle_audio_segment(audio_segment, abs_start)

            self.logger.info("Start transcribe")
            segments, info = model.transcribe(audio_segment, beam_size=4,
                                              language = "en", #zh",
                                              vad_filter=False, #True,
                                              suppress_blank=False,
                                              condition_on_previous_text=False, word_timestamps=True,temperature=0.0)
            #self.logger.info(info)
            if self.first_:
                self.text_ = ""
            if self.last_word_in_prev_seg_ is not None:
                w = self.last_word_in_prev_seg_
                self.update_output(w)
            cnt_s = 0
            # The whole time range consists of 3 part
            # t0 t1: overlap the previous window with self.overlap_ if not first else 0
            # t1 t2: the actual effective content
            # t2 t3:
            start_sec = 0 if self.first_ else self.overlap_sec_
            segment_sec = 1.0* self.segment_size_ /self.rate_
            end_sec   = segment_sec - self.overlap_sec_
            with_last_word = False
            for segment in segments:
                for w in segment.words:
                    w_start = w.start - self.prepad_secs_
                    w_end = w.end - self.prepad_secs_
                    if w.probability < 0.15:
                        continue
                    if w_start < 0:
                        self.logger.debug( f"Start is negative:abs_start:{self.abs_start_ * 1.0 / self.rate_}s;[{w_start}:{w_end}]:{w.probability:.3f}\t{w.word}")
                        continue
                    if w_start > end_sec:
                        continue
                    # remove the 1st word
                    elif w_start < start_sec:
                        if self.last_word_in_prev_seg_ is None:
                            self.update_output(w,abs_start)
                        else: #else there is remained last word in previous seg.
                            if w_start == 0.0:
                                self.last_word_in_prev_seg_ = None
                                continue
                            else:
                                clean_word = re.sub(r'[!.,;?]+$', '', w.word)
                                if self.last_word_in_prev_seg_.word == clean_word:
                                    continue
                                self.update_output(w,abs_start)
                    else: #w_start == 0:
                        if w_end > end_sec:  # cross t2
                            w1 = { "start" : w.start, "end": w.end, "word":w.word, "probability":w.probability }
                            w = type('MyWord',(),w1)()
                            w.word = re.sub(r'[!.,;?]+$', '', w.word)
                            self.last_word_in_prev_seg_ = w
                            with_last_word = True
                            self.logger.debug( f"CROSS t2: abs_start:{self.abs_start_ * 1.0 / self.rate_}s;[{w.start}:{w.end}]:{w.probability:.3f}\t{w.word}")
                            break
                        else: #Normal
                            self.update_output(w,abs_start)
                cnt_s +=1
            if not with_last_word:
                self.last_word_in_prev_seg_ = None
            return self.text_

    hrAudio = ASR_AudioStreamHandler()
    hrAudio.logger.setLevel(logging.INFO)
    hrAudio.preheat_model()

    read_size_bytes = read_time_ms * 2 * hrAudio.rate_ // 1000  # convert ms to bytes
    cnt = 0
    file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_answer_call.wav"
    file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav"
    file_path = "./output_16k_mono.wav"
    file_path = "/home/xiaorui/W/deepgram/10secs_english_speech.wav"
    logger.info(f"Start recognize the file {file_path}")
    with open(file_path, 'rb') as f:  # open the file in binary mode
        while True:
            stream_data = f.read(read_size_bytes)  # read from the file
            if not stream_data:
                text = hrAudio.finish()
                logger.warning(f"Final text:{text}")
                break
            start = cnt * read_time_ms
            cnt += 1
            end = cnt * read_time_ms
            #logger.debug(f"process_stream_data({len(stream_data)}, {start},{end})")
            hrAudio.process_stream_data(stream_data)

main(); sys.exit(0)

