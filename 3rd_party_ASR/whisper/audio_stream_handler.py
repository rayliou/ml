#!/home/xiaorui/anaconda3/bin/python3
import numpy as np
import sys
import logging

class AudioStreamHandler:
    def __init__(self, rate=16000, bits=16):
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        self.rate_ = rate
        self.bits_ = bits
        self.queue_size_ = rate * 10  # 10 seconds of audio
        self.queue_ = np.array([], dtype=np.int16)
        self.overlap_ = rate // 4  # 250ms overlap
        self.process_size_ = rate * 2  # process every 2 seconds
        self.first_ = True
        self.start_ = 0  # starting point for processing
        self.abs_start_ = 0  # from the absolute zero ms of the stream

    def process_stream_data(self, stream_data):
        data = np.frombuffer(stream_data, dtype=np.int16)
        self.queue_ = np.concatenate((self.queue_, data))
        segment_size = self.rate_ * 1.75 if self.first_ else self.process_size_
        if len(self.queue_) - self.start_ >= segment_size:
            end  = int(self.start_ + segment_size)
            start_ms = int(self.start_ * 1000 / self.rate_)
            end_ms = int(end * 1000 / self.rate_)
            self.logger.debug(f"handle_audio_segment([{self.start_}:{end}]), time range: [{start_ms}ms:{end_ms}ms];abs_start_ms:{self.abs_start_ * 1000 / self.rate_}")
            self.handle_audio_segment(self.queue_[self.start_: end])
            self.start_ = int(self.start_ + segment_size - self.overlap_)
            self.abs_start_ += (segment_size - self.overlap_)
            self.first_ = False

        # Drop oldest data from queue if size exceeds 10 seconds
        if len(self.queue_) > self.queue_size_:
            drop_size = len(self.queue_) - self.queue_size_
            self.queue_ = self.queue_[drop_size:]
            self.start_ -= drop_size  # adjust starting point accordingly
            self.logger.debug(f"Drop:{drop_size*1000/self.rate_}ms,start:{self.start_*1000/self.rate_}ms")

    def handle_audio_segment(self, audio_segment):
        # Handle audio processing here
        pass

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
