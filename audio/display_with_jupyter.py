from IPython.lib.display import Audio
import matplotlib.pyplot as plt
import librosa.display
import sys
import numpy as np
from scipy.io import wavfile
import glob



import matplotlib.pyplot as plt

def show_audio_and_features(audio, features, title):
    sample_rate = 16000
    # Display audio using Audio function
    display(Audio(audio, rate=sample_rate, autoplay=False))
     # Plot audio waveform and features spectrogram in the same figure
    #fig, axs = plt.subplots(2, 1, figsize=(16, 6), sharex=True)
    fig, axs = plt.subplots(2, 1, figsize=(20, 6), sharex=True, gridspec_kw={'height_ratios': [1, 2]})


    # Create a time vector
    #print(f"len of audio:{len(audio)} ")
    t = np.arange(len(audio)) *1.0 / sample_rate
    #print(t)

    axs[0].set_title("Audio Signal")
    axs[0].plot(t, audio)
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Amplitude")

    axs[1].set_title("Features Spectrogram")
    librosa.display.specshow(features.T, sr=sample_rate, x_axis='time', y_axis='linear', hop_length=160)
    axs[1].set_xlabel("Time (s)")
    axs[1].set_xlim(axs[0].get_xlim())

    axs[1].set_ylabel("Frequency")
    fig.colorbar(axs[1].collections[0], ax=axs[1], format='%+2.0f dB',orientation='horizontal', pad=0.2)

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()
    #print(f"features.T:{features.shape} audio: {len(audio)/160.}")
    
def process_audio_files(directory):
    wav_files = glob.glob(directory + "/*.wav")

    for audio_file in wav_files:
        feature_file = audio_file + ".npy"
        sample_rate, audio = wavfile.read(audio_file)
        features = np.load(feature_file)
        show_audio_and_features(audio, features, f"Signal for {audio_file}")

# 示例调用
directory = "./result_audio"
process_audio_files(directory)

