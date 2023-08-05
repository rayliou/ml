#!/home/xiaorui/anaconda3/bin/python3
import asyncio
import sys,time
import subprocess
from deepgram import Deepgram
import numpy as np
import configparser
import argparse
import aiohttp
import struct
import logging

from mic_device import MicDevice


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
class OpenAIGPTLLMClient:
    def __init__(self, config):
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        self.api_key = config.get(self.__class__.__name__, 'api_key', fallback='')
        self.enable = config.get(self.__class__.__name__, 'enable', fallback=True)
        self.enable = False if self.enable.strip().lower() == "false" else True
        self.logger.debug(f"api_key:{self.api_key}")
        self.session = aiohttp.ClientSession()  # 创建一个aiohttp的会话对象，用于管理所有的HTTP请求和响应

    async def send_and_receive(self, question):
        """ https://platform.openai.com/docs/api-reference/making-requests """
        if not self.enable: 
            return "The LLM is disable"
        url = "https://api.openai.com/v1/chat/completions"
        headers =  {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        json_body  = {
            "temperature": 0.7,
            "model": "gpt-3.5-turbo",
             "messages": [
                 {"role": "system", "content": "You are a general AI assistant, please respond to questions according to my needs."},
                 {"role": "user", "content": question}
             ],
        }
        async with self.session.request("POST", url, headers=headers, json=json_body) as response:
            return await response.json()

    async def close(self):
        await self.session.close()  # 关闭aiohttp的会话

class DeepgramASRClient:
    def __init__(self, config):
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        self.api_key_ = config.get('DeepgramASRClient', 'DEEPGRAM_API_KEY', fallback='')
        if self.api_key_ == "" :
            print("Please set the correct DEEPGRAM_API_KEY in the section of DeepgramASRClient on the configuration file")
            sys.exit(0)
        self.deepgram_ = Deepgram(self.api_key_)
        self.deepgramLive_ = None
        self.disconnected_ = False
        self.text_ = ""
        self.start_time_ = time.time()

        self.record_mode_ = config.getboolean('Device', 'record_mode', fallback=False)
        if self.record_mode_:
            self.record_file_ = config.get('Device', 'record_file', fallback='record.wav')
            self.file_ = None

    async def connect(self):
        if self.record_mode_:
            self.file_ = open(self.record_file_, 'wb')
        try:
            self.deepgramLive_ = await self.deepgram_.transcription.live({
                'smart_format': True,
                'interim_results': False,
                'language': 'en-US',
                'model': 'nova',
            })
            self.deepgramLive_.registerHandler(self.deepgramLive_.event.TRANSCRIPT_RECEIVED, self.handle_transcript)
            self.deepgramLive_.registerHandler(self.deepgramLive_.event.CLOSE, self.handle_close)
            self.logger.debug(f"ASR Live was created")

        except Exception as e:
            print(f'Could not open socket: {e}')
            sys.exit(1)

    def handle_transcript(self, transcript):
        text = self.get_asr_transcript_text(transcript)
        if text != "":
            self.text_ += " "
            self.text_ += text

    def get_asr_transcript_text(self, transcript):
        """
        start = transcript.get('start', 'NA')
        duration = transcript.get('duration', 'NA')

        if start != 'NA' and duration != 'NA':
            end_time = start + duration
        else:
            end_time = 'NA'
        """
        confidence = transcript.get('channel', {}).get('alternatives', [{}])[0].get('confidence', 0)
        t_transcript = transcript.get('channel', {}).get('alternatives', [{}])[0].get('transcript', 'NA')
        speech_final = transcript.get('speech_final', 'NA')
        is_final = transcript.get('is_final', 'NA')
        #self.logger.debug(f"[{start}:{end_time}][D:{duration}] C: {confidence:.2f}, {t_transcript}, \t Speech_final: {speech_final}, Is_final: {is_final}")
        self.logger.info(f"C:{confidence:.2f}, {t_transcript}, \t Speech_final: {speech_final}, Is_final: {is_final}")
        return t_transcript.strip()


    def handle_close(self, code):
        self.disconnected_ = True
        self.logger.warning(f'Connection closed with code {code}.')

    async def send_audio(self, audio):
        if self.disconnected_:
            return
        if self.record_mode_:
            self.file_.write(audio)
        if self.deepgramLive_:
            self.deepgramLive_.send(audio)

    async def disconnect(self):
        if self.record_mode_:
            self.file_.close()
            self.logger.info("Close record audio file")
        if self.deepgramLive_:
            self.logger.info("Close deepgramLive_")
            self.disconnected_ = True
            await self.deepgramLive_.finish()

class DeviceManager:
    def __init__(self,config, device, asr_client, llm_client):
        self.asr_session_timeout_ = float(config.get(self.__class__.__name__, 'asr_session_timeout', fallback=20))
        self.non_speech_timeout_  = float(config.get(self.__class__.__name__, 'non_speech_timeout', fallback=5))
        self.logger = logging.getLogger("main." + self.__class__.__name__)
        self.device_ = device
        self.asr_client_ = asr_client
        self.llm_client_ = llm_client


    async def disconnect_asr_after_timeout(self, timeout):
        self.logger.debug(f"ASR timeout {timeout} s")
        secs_passed = 0
        self.non_speech_timeout = 5
        non_speech_secs_passed  = 0
        last_text = ""
        while secs_passed < timeout:
            if int(2 * secs_passed) % 2 == 0:
                self.logger.warning("=" * int(secs_passed))
            await asyncio.sleep(0.5)
            secs_passed += 0.5
            non_speech_secs_passed += 0.5
            if self.asr_client_.text_ != last_text:
                last_text = self.asr_client_.text_
                non_speech_secs_passed = 0.5
            elif last_text != "" and  non_speech_secs_passed > self.non_speech_timeout_:
                self.logger.debug(f"No more transcription after {non_speech_secs_passed}s")
                break

        await self.asr_client_.disconnect()
        self.logger.debug(f"Disconnect the asr due to the timeout {timeout} s")

    async def connect_asr(self):
        await self.asr_client_.connect()

    async def play_audio(self):
        await asyncio.sleep(3)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.run_shell_command)

    def run_shell_command(self):
        subprocess.Popen(["aplay", "./10secs_english_speech.wav"])

    async def start(self):
        await self.connect_asr()
        audio_data = create_wave_header()
        await self.asr_client_.send_audio(audio_data)
        #play_audio_task = asyncio.create_task(self.play_audio())
        timeout = self.asr_session_timeout_
        self.logger.debug(f"create a timeout task for  {timeout} s" )
        disconnect_task = asyncio.create_task(self.disconnect_asr_after_timeout(timeout))
        try:
            cnt = 0
            while not self.asr_client_.disconnected_:
                audio_data = await self.device_.get_data()
                if audio_data is None:
                    break
                await self.asr_client_.send_audio(audio_data)
            question = self.asr_client_.text_.strip()
            self.logger.warning(f"Question from ASR: [{question}]")
            answer = await self.llm_client_.send_and_receive(question)
            self.logger.warning(f"Answer from LLM: [{answer}]")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        self.device_.cleanup()

async def main():
    parser = argparse.ArgumentParser(description='My Script')
    parser.add_argument('--log_level', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        default=None, help='Set the log level from command line.')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read('config.ini')
    if args.log_level:
        log_level = getattr(logging, args.log_level.upper())
    else:
        log_level = config.get('Logging', 'log_level', fallback='DEBUG')
        log_level = getattr(logging, log_level.upper())
    logger = logging.getLogger('main')
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    def getch():
        try:
            # Unix-like systems
            import termios, tty
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setcbreak(sys.stdin.fileno())
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except ImportError:
            # Windows systems
            import msvcrt
            char = msvcrt.getch().decode("utf-8")
        return char


    while True:
        print("Press 'q' to quit.")
        print("Press 'g' or ' ' (space) to enter Cloud-based ASR-LLM.")
        user_input = getch().lower()
        if user_input == 'q':
            print("Exiting the event loop. Goodbye!")
            break
        elif user_input in ['g', ' ']:
            print("Entering Cloud-based ASR-LLM.")
            device = MicDevice(config)
            asr_client = DeepgramASRClient(config)
            llm_client = OpenAIGPTLLMClient(config)
            device_manager = DeviceManager(config, device, asr_client, llm_client)
            await device_manager.start()
        else:
            print(f"Invalid input [{user_input}] . Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
