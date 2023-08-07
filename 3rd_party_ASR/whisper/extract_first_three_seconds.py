#!/home/xiaorui/anaconda3/bin/python3
import numpy as np
import librosa

def extract_first_three_seconds(wav_file, output_npy_file):
    y, sr = librosa.load(wav_file, sr=None)  # sr=None to preserve the native sampling rate
    num_samples_for_3s = 10 * sr
    y_first_3s = y[:num_samples_for_3s]
    np.save(output_npy_file, y_first_3s)

#wav_file_path = '/home/xiaorui/W/deepgram/10secs_english_speech.wav'
wav_file_path = '/data/xiaorui/101_audios/wav_ces/hi_anita_battery_left.wav'
output_npy_path = '10s_16khz.npy'
extract_first_three_seconds(wav_file_path, output_npy_path)

