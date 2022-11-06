#!/home/xiaorui/anaconda3/bin/python3
import numpy as np
import sys
import logging

class AudioStreamHandler:
    def __init__(self, rate=16000, bits=16):
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        self.overlap_sec_ = 0.5

        self.rate_ = rate
        self.bits_ = bits
        self.queue_size_ = rate * 10  # 10 seconds of audio
        self.queue_ = np.array([], dtype=np.int16)
        self.overlap_ = int(rate * self.overlap_sec_)
        self.first_ = True
        self.start_ = 0  # starting point for processinG
        self.abs_start_ = 0  # from the absolute zero ms of the stream
        self.set_segment_buffer()
    def set_segment_buffer(self):
        self.segment_sec_ = self.overlap_sec_ * (4 if self.first_ else 5)
        self.segment_size_ = int(self.segment_sec_ * self.rate_)

    def process_stream_data(self, stream_data):
        self.set_segment_buffer()
        data = np.frombuffer(stream_data, dtype=np.int16)
        data = data.astype(np.float32) / 32768.0
        self.queue_ = np.concatenate((self.queue_, data))
        if len(self.queue_) - self.start_ >= self.segment_size_:
            end  = int(self.start_ + self.segment_size_)
            start_ms = int(self.start_ * 1000 / self.rate_)
            end_ms = int(end * 1000 / self.rate_)
            self.logger.debug(f"handle_audio_segment([{self.start_}:{end}]), time range: [{start_ms}ms:{end_ms}ms];abs_start_ms:{self.abs_start_ * 1000 / self.rate_}")
            self.handle_audio_segment(self.queue_[self.start_: end],self.abs_start_)
            self.start_ = int(self.start_ + self.segment_size_ - self.overlap_)
            self.abs_start_ += (self.segment_size_ - self.overlap_)
            self.first_ = False

        # Drop oldest data from queue if size exceeds 10 seconds
        if len(self.queue_) > self.queue_size_:
            drop_size = len(self.queue_) - self.queue_size_
            self.queue_ = self.queue_[drop_size:]
            self.start_ -= drop_size  # adjust starting point accordingly
            self.logger.debug(f"Drop:{drop_size*1000/self.rate_}ms,start:{self.start_*1000/self.rate_}ms")

    def finish(self):
        end = len(self.queue_)
        if end <= self.start_ +1:
            return
        start_ms = int(self.start_ * 1000 / self.rate_)
        end_ms = int(end * 1000 / self.rate_)
        self.logger.debug(
            f"handle_audio_segment([{self.start_}:{end}]), time range: [{start_ms}ms:{end_ms}ms];abs_start_ms:{self.abs_start_ * 1000 / self.rate_}")
        text = self.handle_audio_segment(self.queue_[self.start_: end], self.abs_start_)
        return text

    def handle_audio_segment(self, audio_segment,abs_start):
        from scipy.io import wavfile
        audio_segment_int16 = np.int16(audio_segment * 32767)
        sample_rate = 16000
        wavfile.write(f'{1.0 * self.abs_start_/self.rate_}s.wav', sample_rate, audio_segment_int16)
        return ""

def main(read_time_ms):
    logger = logging.getLogger('main')
    log_level = getattr(logging, "DEBUG")
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    hrAudio = AudioStreamHandler()
    read_size_bytes = read_time_ms * 2 * hrAudio.rate_ // 1000  # convert ms to bytes
    cnt = 0
    while True:
        stream_data = sys.stdin.buffer.read(read_size_bytes)  # read data from stdin
        if not stream_data:
            hrAudio.finish()
            break
        start = cnt *read_time_ms
        cnt+=1
        end = cnt *read_time_ms
        logger.debug(f"process_stream_data({start},{end})")
        hrAudio.process_stream_data(stream_data)

if __name__ == "__main__":
    # read_time_ms can be any value between 10 and 500
    read_time_ms = 200
    main(read_time_ms)
