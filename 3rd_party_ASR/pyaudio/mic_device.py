#!/home/xiaorui/anaconda3/bin/python3
"""
| play -t raw -b 16 -c 1 -e signed -r 16000 -
"""

import asyncio
import atexit
import multiprocessing
import struct
import sys

import librosa
import numpy as np
import pyaudio
import logging


def create_wave_header(sample_rate=16000, bits_per_sample=16, num_channels=1, num_frames=16000*120):
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    """ https://docs.fileformat.com/audio/wav/
    1 - 4	“RIFF”	Marks the file as a riff file. Characters are each 1 byte long.
    5 - 8	File size (integer)	Size of the overall file - 8 bytes, in bytes (32-bit integer). Typically, you’d fill this in after creation.
    9 -12	“WAVE”	File Type Header. For our purposes, it always equals “WAVE”.
    13-16	“fmt "	Format chunk marker. Includes trailing null
    17-20	16	Length of format data as listed above
    21-22	1	Type of format (1 is PCM) - 2 byte integer
    23-24	2	Number of Channels - 2 byte integer
    25-28	44100	Sample Rate - 32 byte integer. Common values are 44100 (CD), 48000 (DAT). Sample Rate = Number of Samples per second, or Hertz.
    29-32	176400	(Sample Rate * BitsPerSample * Channels) / 8.
    33-34	4	(BitsPerSample * Channels) / 8.1 - 8 bit mono2 - 8 bit stereo/16 bit mono4 - 16 bit stereo
    35-36	16	Bits per sample
    
    37-40	“data”	“data” chunk header. Marks the beginning of the data section.
    41-44	File size (data)	Size of the data section.
Sample values are given above for a 16-bit stereo source.
    """
    # https://docs.python.org/3/library/struct.html
    wave_header = struct.pack( '<4sI4s4sIHHIIHH4sI',
                              b'RIFF',  # RIFF format
                              36 + num_frames * block_align,  # ChunkSize
                              b'WAVE',  # 'WAVE' format
                              b'fmt ',  # 'fmt ' subchunk
                              16,  # Subchunk1Size
                              1,  # AudioFormat (PCM)
                              num_channels,  # NumChannels
                              sample_rate,  # SampleRate
                              byte_rate,  # ByteRate
                              block_align,  # BlockAlign
                              bits_per_sample,  # BitsPerSample
                              b'data',  # 'data' subchunk
                              num_frames * block_align  # Subchunk2Size
                              )

    return wave_header


class MicDevice:
    CHUNK = 88200 #2 seconds
    CHUNK = 44100 #1 s
    INPUT_SAMPLE_RATE = 44100
    OUTPUT_SAMPLE_RATE = 16000
    def __init__(self, config):
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        # Use 100ms (20 to 250)
        # https://developers.deepgram.com/docs/measuring-streaming-latency#causes-of-latency
        # https://developers.deepgram.com/reference/streaming
        if config is not None:
            read_buffer_ms = int(config.get(self.__class__.__name__, 'read_buffer_ms', fallback=250))
        else:
            read_buffer_ms = 250
        if read_buffer_ms < 20 or read_buffer_ms > 250:
            self.logger.critical("The read buffer should be in [20,250]ms")
            sys.exit(1)
        self.buffer_size_ = int(read_buffer_ms * self.INPUT_SAMPLE_RATE /1000.)
        self.logger.info(f"Read buffer:{read_buffer_ms}ms,{self.buffer_size_}frames")
        dummy_data = np.zeros(10)
        librosa.resample(dummy_data , orig_sr=MicDevice.INPUT_SAMPLE_RATE, target_sr=MicDevice.OUTPUT_SAMPLE_RATE)

        self.queue_ = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()

        self.listen_process = multiprocessing.Process(target=self.listen)
        self.listen_process.start()

        self.process_pool = multiprocessing.Pool(6)
        self.process_process = multiprocessing.Process(target=self.process_data)
        self.process_process.start()
        self.current_index = 0
        atexit.register(self.cleanup)

    def cleanup(self):
        self.logger.info("Cleanuping .....")
        self.listen_process.terminate()
        self.process_pool.terminate()
        self.process_process.terminate()


    async def get_data(self):
        loop = asyncio.get_running_loop()
        while True:
            data = await loop.run_in_executor(None, self.result_queue.get)
            index, result = data
            if index is None:
                return None
            elif index == self.current_index:
                self.current_index += 1
                return result
            else:
                self.result_queue.put(data)

    def listen(self):
        self.p_ = pyaudio.PyAudio()
        self.stream_ = self.p_.open(format=self.p_.get_format_from_width(2),
                                    channels=1, rate=MicDevice.INPUT_SAMPLE_RATE, input=True, output=False,
                                    frames_per_buffer=MicDevice.CHUNK, input_device_index=0
                                    )

        index = 0
        overflow_count = 0  # counter for overflows
        while True:
            try:
                data = self.stream_.read(self.buffer_size_, exception_on_overflow=False)
                self.queue_.put((index, data))
            except Exception as e:
                if isinstance(e, IOError):
                    if e.errno == -9988:
                        print("The PyAudio stream was closed")
                        self.queue_.put((None, None))
                        return
                    elif e.errno == pyaudio.paInputOverflowed:
                        overflow_count += 1
                        self.logger.debug("Pyaudio overflow")
                pass
            index += 1


    def process_data(self):
        while True:
            index, data = self.queue_.get()
            if index is None or data is None:
                self.result_queue.put((None, None))
                break
            data = np.frombuffer(data, dtype=np.int16)
            data = data.astype(np.float32) / np.iinfo(np.int16).max
            processed_data = librosa.resample(data, orig_sr=MicDevice.INPUT_SAMPLE_RATE, target_sr=MicDevice.OUTPUT_SAMPLE_RATE)
            audio_data_int16 = (processed_data * np.iinfo(np.int16).max).astype(np.int16)
            audio_data_bytes = audio_data_int16.tobytes()
            self.result_queue.put((index, audio_data_bytes))


def main(config=None):
    device = MicDevice(config)
    loop = asyncio.get_event_loop()
    n  = 0
    while True:
        try:
            data = loop.run_until_complete(device.get_data())
            sys.stdout.buffer.write(data)
        except KeyboardInterrupt:
            print("Terminating...")
            break


if __name__ == '__main__':
    main(None)
