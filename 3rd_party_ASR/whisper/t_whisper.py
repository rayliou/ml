#!/home/xiaorui/anaconda3/bin/python3
import whisper
import logging

logger = logging.getLogger('main')
log_level = getattr(logging, "DEBUG")
logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

model = whisper.load_model("base")
#model = whisper.load_model("tiny")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("/data/xiaorui/101_audios/01cmd_hi_anita_pause_the_song.wav")
audio = whisper.load_audio("/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav")
file_path = "/home/xiaorui/W/deepgram/10secs_english_speech.wav"
file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_answer_call.wav"
file_path = "/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav"
audio = whisper.load_audio(file_path)
logger.info(f"Processing file {file_path}")
logger.info("start padding")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
logger.info("log_mel_spectrogram")
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
logger.info("detect ")
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions(fp16 = False)
result = whisper.decode(model, mel, options)

# print the recognized text
#print(result)
print(result.text)
logger.info("After detecting")
