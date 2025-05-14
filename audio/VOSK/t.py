#! /usr/bin/env python3


"""
Large model : vosk-model-en-us-0.22
"""

import os
import logging
import argparse
import wave
from pathlib import Path
import json
from vosk import Model, KaldiRecognizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
home_path = Path.home()

def load_vocabulary(file_path):
    """
    Load vocabulary from a file, removing punctuation and converting to lowercase.
    Keeps separators within words (like apostrophes in contractions).
    """
    vocabulary = []
    seen_words = set()
    MAX_WORDS = 500
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                for word in line.strip().split():
                    word = word.lower()
                    word = word.strip('.,;:!?()[]{}"\'-')
                    if not word:
                        continue
                    if word not in seen_words:
                        vocabulary.append(word)
                        seen_words.add(word)
                    if len(vocabulary) >= MAX_WORDS:
                        raise ValueError(f"Vocabulary file contains more than {MAX_WORDS} words")
    except FileNotFoundError:
        raise FileNotFoundError(f"Vocabulary file not found at {file_path}")
    grammar = json.dumps(vocabulary)
    return grammar

def init_recognizer(vocabulary_path="vocabulary.txt", model_name="vosk-model-small-en-us-0.15"):
    # 1. Load the model
    model_path = os.path.join(home_path, ".cache/vosk/", model_name)
    model = Model(model_path)
    grammar = load_vocabulary(vocabulary_path)
    recognizer = KaldiRecognizer(model, 16000, grammar)
    return recognizer


def transcribe_audio(recognizer, wf):
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            results.append(result.get("text", ""))
    
    # Append the final partial result   
    final_result = json.loads(recognizer.FinalResult())
    results.append(final_result.get("text", ""))

    # Print the full transcription
    full_transcript = " ".join(filter(None, results))
    print("Transcription:", full_transcript)
    
    return full_transcript

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio using Vosk")
    parser.add_argument("-w", "--wave_file", type=str, default="input.wav", help="Path to the wave file")
    parser.add_argument("-m", "--model_name", type=str, default="vosk-model-small-en-us-0.15", help="Name of the Vosk model")
    parser.add_argument("-v", "--vocabulary_path", type=str, default="vocabulary.txt", help="Path to vocabulary file")
    args = parser.parse_args()
    logger.info(args)
    
    wf = wave.open(args.wave_file, "rb")
    recognizer = init_recognizer(vocabulary_path=args.vocabulary_path, model_name=args.model_name)
    transcribe_audio(recognizer, wf)
    
    wf.close()

