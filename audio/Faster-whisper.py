#! /usr/bin/env python3

from faster_whisper import WhisperModel,BatchedInferencePipeline

# model_size = "base"
model_size = "large-v3-turbo"

# Run on GPU with FP16
#model = WhisperModel(model_size, device="cuda", compute_type="float16")
model = WhisperModel(model_size, device="cpu", compute_type="int8")
batch_model = BatchedInferencePipeline(model)

def transcribe_audio(audio_file):
    segments, info = model.transcribe(audio_file, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

def translate_to_english(audio_file):
    segments, info = model.transcribe(audio_file, task="translate"
                ,beam_size=5,best_of=5
                ,language="fr")
    # segments, info = batch_model.transcribe(audio_file, batch_size=4, task="translate",beam_size=5,language="fr")
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

# Example usage:
transcribe_audio("./output.wav")
# translate_to_english("./output.wav")
