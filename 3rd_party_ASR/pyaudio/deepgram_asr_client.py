#!/home/xiaorui/anaconda3/bin/python3
import asyncio
import sys,time
from deepgram import Deepgram

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
                'interim_results': True,
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
        speech_final = transcript.get('speech_final', False)
        is_final = transcript.get('is_final', False)
        confidence = transcript.get('channel', {}).get('alternatives', [{}])[0].get('confidence', 0)
        t_transcript = transcript.get('channel', {}).get('alternatives', [{}])[0].get('transcript', 'NA')
        if not is_final:
            self.logger.debug(f"INTERIM Result:C:{confidence:.2f}, {t_transcript}, \t Speech_final: {speech_final}, Is_final: {is_final}")
            return ""
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

if __name__ == "__main__":
    asyncio.run(main())
