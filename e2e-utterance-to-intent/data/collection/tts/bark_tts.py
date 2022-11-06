#!/bin/env python3
"""
  # Create a virtual environment
  uv venv --python=python3.9  ~/py3.9
  source ~/py3.9/bin/activate
  # Install Bark
    git clone https://github.com/suno-ai/bark#
    cd bark
    uv pip install .
    uv pip install git+https://github.com/huggingface/transformers.git
    uv pip install accelerate

    conda env list
 vim  ~/.zshrc
  pwd
  cd ..
"""
import scipy
import numpy as np
import torch
from transformers import AutoProcessor, BarkModel
device = "cuda:1" if torch.cuda.is_available() else "cpu"
device = "cpu"

text = "Unbelievable! You're a genius! -uh- sure, sure, sure"

processor = AutoProcessor.from_pretrained("suno/bark")
#model = BarkModel.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float16).to(device)
print("Loaded model")

voice_preset = "v2/en_speaker_6"

inputs = processor(text, voice_preset=voice_preset)
# Move inputs to the same device as the model
for key, value in inputs.items():
    inputs[key] = value.to(device)


audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()

# Convert to float32 or int16 to avoid the "Unsupported data type 'float16'" error
# Option 1: Convert to float32 (range -1.0 to 1.0)
audio_array = audio_array.astype(np.float32)

# Option 2: Convert to int16 (better for wav files)
# Scale to int16 range and convert
audio_array = (audio_array * 32767).astype(np.int16)

sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sample_rate, data=audio_array)

"""
Speaker 0 (EN)	v2/en_speaker_0	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_0.mp3
Speaker 1 (EN)	v2/en_speaker_1	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_1.mp3
Speaker 2 (EN)	v2/en_speaker_2	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_2.mp3
Speaker 3 (EN)	v2/en_speaker_3	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_3.mp3
Speaker 4 (EN)	v2/en_speaker_4	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_4.mp3
Speaker 5 (EN)	v2/en_speaker_5	English	Male	Grainy	https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_5.mp3
Speaker 6 (EN)	v2/en_speaker_6	English	Male	Suno Favorite	https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_6.mp3
Speaker 7 (EN)	v2/en_speaker_7	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_7.mp3
Speaker 8 (EN)	v2/en_speaker_8	English	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_8.mp3
Speaker 9 (EN)	v2/en_speaker_9	English	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/en_speaker_9.mp3
Speaker 0 (ZH)	v2/zh_speaker_0	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_0.mp3
Speaker 1 (ZH)	v2/zh_speaker_1	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_1.mp3
Speaker 2 (ZH)	v2/zh_speaker_2	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_2.mp3
Speaker 3 (ZH)	v2/zh_speaker_3	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_3.mp3
Speaker 4 (ZH)	v2/zh_speaker_4	Chinese (Simplified)	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_4.mp3
Speaker 5 (ZH)	v2/zh_speaker_5	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_5.mp3
Speaker 6 (ZH)	v2/zh_speaker_6	Chinese (Simplified)	Female	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_6.mp3
Speaker 7 (ZH)	v2/zh_speaker_7	Chinese (Simplified)	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_7.mp3
Speaker 8 (ZH)	v2/zh_speaker_8	Chinese (Simplified)	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_8.mp3
Speaker 9 (ZH)	v2/zh_speaker_9	Chinese (Simplified)	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/zh_speaker_9.mp3
Speaker 0 (FR)	v2/fr_speaker_0	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_0.mp3
Speaker 1 (FR)	v2/fr_speaker_1	French	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_1.mp3
Speaker 2 (FR)	v2/fr_speaker_2	French	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_2.mp3
Speaker 3 (FR)	v2/fr_speaker_3	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_3.mp3
Speaker 4 (FR)	v2/fr_speaker_4	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_4.mp3
Speaker 5 (FR)	v2/fr_speaker_5	French	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_5.mp3
Speaker 6 (FR)	v2/fr_speaker_6	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_6.mp3
Speaker 7 (FR)	v2/fr_speaker_7	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_7.mp3
Speaker 8 (FR)	v2/fr_speaker_8	French	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_8.mp3
Speaker 9 (FR)	v2/fr_speaker_9	French	Male	Auditorium	https://dl.suno-models.io/bark/prompts/prompt_audio/fr_speaker_9.mp3
Speaker 0 (DE)	v2/de_speaker_0	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_0.mp3
Speaker 1 (DE)	v2/de_speaker_1	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_1.mp3
Speaker 2 (DE)	v2/de_speaker_2	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_2.mp3
Speaker 3 (DE)	v2/de_speaker_3	German	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_3.mp3
Speaker 4 (DE)	v2/de_speaker_4	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_4.mp3
Speaker 5 (DE)	v2/de_speaker_5	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_5.mp3
Speaker 6 (DE)	v2/de_speaker_6	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_6.mp3
Speaker 7 (DE)	v2/de_speaker_7	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_7.mp3
Speaker 8 (DE)	v2/de_speaker_8	German	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_8.mp3
Speaker 9 (DE)	v2/de_speaker_9	German	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/de_speaker_9.mp3
Speaker 0 (HI)	v2/hi_speaker_0	Hindi	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_0.mp3
Speaker 1 (HI)	v2/hi_speaker_1	Hindi	Female	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_1.mp3
Speaker 2 (HI)	v2/hi_speaker_2	Hindi	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_2.mp3
Speaker 3 (HI)	v2/hi_speaker_3	Hindi	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_3.mp3
Speaker 4 (HI)	v2/hi_speaker_4	Hindi	Female	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_4.mp3
Speaker 5 (HI)	v2/hi_speaker_5	Hindi	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_5.mp3
Speaker 6 (HI)	v2/hi_speaker_6	Hindi	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_6.mp3
Speaker 7 (HI)	v2/hi_speaker_7	Hindi	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_7.mp3
Speaker 8 (HI)	v2/hi_speaker_8	Hindi	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_8.mp3
Speaker 9 (HI)	v2/hi_speaker_9	Hindi	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/hi_speaker_9.mp3
Speaker 0 (IT)	v2/it_speaker_0	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_0.mp3
Speaker 1 (IT)	v2/it_speaker_1	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_1.mp3
Speaker 2 (IT)	v2/it_speaker_2	Italian	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_2.mp3
Speaker 3 (IT)	v2/it_speaker_3	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_3.mp3
Speaker 4 (IT)	v2/it_speaker_4	Italian	Male	Suno Favorite	https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_4.mp3
Speaker 5 (IT)	v2/it_speaker_5	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_5.mp3
Speaker 6 (IT)	v2/it_speaker_6	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_6.mp3
Speaker 7 (IT)	v2/it_speaker_7	Italian	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_7.mp3
Speaker 8 (IT)	v2/it_speaker_8	Italian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_8.mp3
Speaker 9 (IT)	v2/it_speaker_9	Italian	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/it_speaker_9.mp3
Speaker 0 (JA)	v2/ja_speaker_0	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_0.mp3
Speaker 1 (JA)	v2/ja_speaker_1	Japanese	Female	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_1.mp3
Speaker 2 (JA)	v2/ja_speaker_2	Japanese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_2.mp3
Speaker 3 (JA)	v2/ja_speaker_3	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_3.mp3
Speaker 4 (JA)	v2/ja_speaker_4	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_4.mp3
Speaker 5 (JA)	v2/ja_speaker_5	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_5.mp3
Speaker 6 (JA)	v2/ja_speaker_6	Japanese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_6.mp3
Speaker 7 (JA)	v2/ja_speaker_7	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_7.mp3
Speaker 8 (JA)	v2/ja_speaker_8	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_8.mp3
Speaker 9 (JA)	v2/ja_speaker_9	Japanese	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ja_speaker_9.mp3
Speaker 0 (KO)	v2/ko_speaker_0	Korean	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_0.mp3
Speaker 1 (KO)	v2/ko_speaker_1	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_1.mp3
Speaker 2 (KO)	v2/ko_speaker_2	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_2.mp3
Speaker 3 (KO)	v2/ko_speaker_3	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_3.mp3
Speaker 4 (KO)	v2/ko_speaker_4	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_4.mp3
Speaker 5 (KO)	v2/ko_speaker_5	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_5.mp3
Speaker 6 (KO)	v2/ko_speaker_6	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_6.mp3
Speaker 7 (KO)	v2/ko_speaker_7	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_7.mp3
Speaker 8 (KO)	v2/ko_speaker_8	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_8.mp3
Speaker 9 (KO)	v2/ko_speaker_9	Korean	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ko_speaker_9.mp3
Speaker 0 (PL)	v2/pl_speaker_0	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_0.mp3
Speaker 1 (PL)	v2/pl_speaker_1	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_1.mp3
Speaker 2 (PL)	v2/pl_speaker_2	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_2.mp3
Speaker 3 (PL)	v2/pl_speaker_3	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_3.mp3
Speaker 4 (PL)	v2/pl_speaker_4	Polish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_4.mp3
Speaker 5 (PL)	v2/pl_speaker_5	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_5.mp3
Speaker 6 (PL)	v2/pl_speaker_6	Polish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_6.mp3
Speaker 7 (PL)	v2/pl_speaker_7	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_7.mp3
Speaker 8 (PL)	v2/pl_speaker_8	Polish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_8.mp3
Speaker 9 (PL)	v2/pl_speaker_9	Polish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/pl_speaker_9.mp3
Speaker 0 (PT)	v2/pt_speaker_0	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_0.mp3
Speaker 1 (PT)	v2/pt_speaker_1	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_1.mp3
Speaker 2 (PT)	v2/pt_speaker_2	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_2.mp3
Speaker 3 (PT)	v2/pt_speaker_3	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_3.mp3
Speaker 4 (PT)	v2/pt_speaker_4	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_4.mp3
Speaker 5 (PT)	v2/pt_speaker_5	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_5.mp3
Speaker 6 (PT)	v2/pt_speaker_6	Portuguese	Male	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_6.mp3
Speaker 7 (PT)	v2/pt_speaker_7	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_7.mp3
Speaker 8 (PT)	v2/pt_speaker_8	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_8.mp3
Speaker 9 (PT)	v2/pt_speaker_9	Portuguese	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/pt_speaker_9.mp3
Speaker 0 (RU)	v2/ru_speaker_0	Russian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_0.mp3
Speaker 1 (RU)	v2/ru_speaker_1	Russian	Male	Echoes	https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_1.mp3
Speaker 2 (RU)	v2/ru_speaker_2	Russian	Male	Echoes	https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_2.mp3
Speaker 3 (RU)	v2/ru_speaker_3	Russian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_3.mp3
Speaker 4 (RU)	v2/ru_speaker_4	Russian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_4.mp3
Speaker 5 (RU)	v2/ru_speaker_5	Russian	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_5.mp3
Speaker 6 (RU)	v2/ru_speaker_6	Russian	Female	Grainy	https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_6.mp3
Speaker 7 (RU)	v2/ru_speaker_7	Russian	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_7.mp3
Speaker 8 (RU)	v2/ru_speaker_8	Russian	Male	Grainy	https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_8.mp3
Speaker 9 (RU)	v2/ru_speaker_9	Russian	Female	Grainy	https://dl.suno-models.io/bark/prompts/prompt_audio/ru_speaker_9.mp3
Speaker 0 (ES)	v2/es_speaker_0	Spanish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_0.mp3
Speaker 1 (ES)	v2/es_speaker_1	Spanish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_1.mp3
Speaker 2 (ES)	v2/es_speaker_2	Spanish	Male	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_2.mp3
Speaker 3 (ES)	v2/es_speaker_3	Spanish	Male	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_3.mp3
Speaker 4 (ES)	v2/es_speaker_4	Spanish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_4.mp3
Speaker 5 (ES)	v2/es_speaker_5	Spanish	Male	Background Noise	https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_5.mp3
Speaker 6 (ES)	v2/es_speaker_6	Spanish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_6.mp3
Speaker 7 (ES)	v2/es_speaker_7	Spanish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_7.mp3
Speaker 8 (ES)	v2/es_speaker_8	Spanish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_8.mp3
Speaker 9 (ES)	v2/es_speaker_9	Spanish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/es_speaker_9.mp3
Speaker 0 (TR)	v2/tr_speaker_0	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_0.mp3
Speaker 1 (TR)	v2/tr_speaker_1	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_1.mp3
Speaker 2 (TR)	v2/tr_speaker_2	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_2.mp3
Speaker 3 (TR)	v2/tr_speaker_3	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_3.mp3
Speaker 4 (TR)	v2/tr_speaker_4	Turkish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_4.mp3
Speaker 5 (TR)	v2/tr_speaker_5	Turkish	Female		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_5.mp3
Speaker 6 (TR)	v2/tr_speaker_6	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_6.mp3
Speaker 7 (TR)	v2/tr_speaker_7	Turkish	Male	Grainy	https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_7.mp3
Speaker 8 (TR)	v2/tr_speaker_8	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_8.mp3
Speaker 9 (TR)	v2/tr_speaker_9	Turkish	Male		https://dl.suno-models.io/bark/prompts/prompt_audio/tr_speaker_9.mp3
"""
# Speaker presets organized by language
# Each language has its own dictionary of speakers with their details

# English speakers
english_speakers = {
    "en_speaker_0": {"prompt": "v2/en_speaker_0", "language": "English", "sex": "Male"},
    "en_speaker_1": {"prompt": "v2/en_speaker_1", "language": "English", "sex": "Male"},
    "en_speaker_2": {"prompt": "v2/en_speaker_2", "language": "English", "sex": "Male"},
    "en_speaker_3": {"prompt": "v2/en_speaker_3", "language": "English", "sex": "Male"},
    "en_speaker_4": {"prompt": "v2/en_speaker_4", "language": "English", "sex": "Male"},
    "en_speaker_5": {"prompt": "v2/en_speaker_5", "language": "English", "sex": "Male"},
    "en_speaker_6": {"prompt": "v2/en_speaker_6", "language": "English", "sex": "Male"},
    "en_speaker_7": {"prompt": "v2/en_speaker_7", "language": "English", "sex": "Male"},
    "en_speaker_8": {"prompt": "v2/en_speaker_8", "language": "English", "sex": "Male"},
    "en_speaker_9": {"prompt": "v2/en_speaker_9", "language": "English", "sex": "Female"}
}

# Chinese speakers
chinese_speakers = {
    "zh_speaker_0": {"prompt": "v2/zh_speaker_0", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_1": {"prompt": "v2/zh_speaker_1", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_2": {"prompt": "v2/zh_speaker_2", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_3": {"prompt": "v2/zh_speaker_3", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_4": {"prompt": "v2/zh_speaker_4", "language": "Chinese (Simplified)", "sex": "Female"},
    "zh_speaker_5": {"prompt": "v2/zh_speaker_5", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_6": {"prompt": "v2/zh_speaker_6", "language": "Chinese (Simplified)", "sex": "Female"},
    "zh_speaker_7": {"prompt": "v2/zh_speaker_7", "language": "Chinese (Simplified)", "sex": "Female"},
    "zh_speaker_8": {"prompt": "v2/zh_speaker_8", "language": "Chinese (Simplified)", "sex": "Male"},
    "zh_speaker_9": {"prompt": "v2/zh_speaker_9", "language": "Chinese (Simplified)", "sex": "Female"}
}

# French speakers
french_speakers = {
    "fr_speaker_0": {"prompt": "v2/fr_speaker_0", "language": "French", "sex": "Male"},
    "fr_speaker_1": {"prompt": "v2/fr_speaker_1", "language": "French", "sex": "Female"},
    "fr_speaker_2": {"prompt": "v2/fr_speaker_2", "language": "French", "sex": "Female"},
    "fr_speaker_3": {"prompt": "v2/fr_speaker_3", "language": "French", "sex": "Male"},
    "fr_speaker_4": {"prompt": "v2/fr_speaker_4", "language": "French", "sex": "Male"},
    "fr_speaker_5": {"prompt": "v2/fr_speaker_5", "language": "French", "sex": "Female"}
}

# Polish speakers
polish_speakers = {
    "pl_speaker_1": {"prompt": "v2/pl_speaker_1", "language": "Polish", "sex": "Male"},
    "pl_speaker_2": {"prompt": "v2/pl_speaker_2", "language": "Polish", "sex": "Male"},
    "pl_speaker_3": {"prompt": "v2/pl_speaker_3", "language": "Polish", "sex": "Male"},
    "pl_speaker_4": {"prompt": "v2/pl_speaker_4", "language": "Polish", "sex": "Female"},
    "pl_speaker_5": {"prompt": "v2/pl_speaker_5", "language": "Polish", "sex": "Male"},
    "pl_speaker_6": {"prompt": "v2/pl_speaker_6", "language": "Polish", "sex": "Female"},
    "pl_speaker_7": {"prompt": "v2/pl_speaker_7", "language": "Polish", "sex": "Male"},
    "pl_speaker_8": {"prompt": "v2/pl_speaker_8", "language": "Polish", "sex": "Male"},
    "pl_speaker_9": {"prompt": "v2/pl_speaker_9", "language": "Polish", "sex": "Female"}
}

# Portuguese speakers
portuguese_speakers = {
    "pt_speaker_0": {"prompt": "v2/pt_speaker_0", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_1": {"prompt": "v2/pt_speaker_1", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_2": {"prompt": "v2/pt_speaker_2", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_3": {"prompt": "v2/pt_speaker_3", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_4": {"prompt": "v2/pt_speaker_4", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_5": {"prompt": "v2/pt_speaker_5", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_6": {"prompt": "v2/pt_speaker_6", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_7": {"prompt": "v2/pt_speaker_7", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_8": {"prompt": "v2/pt_speaker_8", "language": "Portuguese", "sex": "Male"},
    "pt_speaker_9": {"prompt": "v2/pt_speaker_9", "language": "Portuguese", "sex": "Male"}
}

# Russian speakers
russian_speakers = {
    "ru_speaker_0": {"prompt": "v2/ru_speaker_0", "language": "Russian", "sex": "Male"},
    "ru_speaker_1": {"prompt": "v2/ru_speaker_1", "language": "Russian", "sex": "Male"},
    "ru_speaker_2": {"prompt": "v2/ru_speaker_2", "language": "Russian", "sex": "Male"},
    "ru_speaker_3": {"prompt": "v2/ru_speaker_3", "language": "Russian", "sex": "Male"},
    "ru_speaker_4": {"prompt": "v2/ru_speaker_4", "language": "Russian", "sex": "Male"},
    "ru_speaker_5": {"prompt": "v2/ru_speaker_5", "language": "Russian", "sex": "Female"},
    "ru_speaker_6": {"prompt": "v2/ru_speaker_6", "language": "Russian", "sex": "Female"},
    "ru_speaker_7": {"prompt": "v2/ru_speaker_7", "language": "Russian", "sex": "Male"},
    "ru_speaker_8": {"prompt": "v2/ru_speaker_8", "language": "Russian", "sex": "Male"},
    "ru_speaker_9": {"prompt": "v2/ru_speaker_9", "language": "Russian", "sex": "Female"}
}

# Spanish speakers
spanish_speakers = {
    "es_speaker_0": {"prompt": "v2/es_speaker_0", "language": "Spanish", "sex": "Male"},
    "es_speaker_1": {"prompt": "v2/es_speaker_1", "language": "Spanish", "sex": "Male"},
    "es_speaker_2": {"prompt": "v2/es_speaker_2", "language": "Spanish", "sex": "Male"},
    "es_speaker_3": {"prompt": "v2/es_speaker_3", "language": "Spanish", "sex": "Male"},
    "es_speaker_4": {"prompt": "v2/es_speaker_4", "language": "Spanish", "sex": "Male"},
    "es_speaker_5": {"prompt": "v2/es_speaker_5", "language": "Spanish", "sex": "Male"},
    "es_speaker_6": {"prompt": "v2/es_speaker_6", "language": "Spanish", "sex": "Male"},
    "es_speaker_7": {"prompt": "v2/es_speaker_7", "language": "Spanish", "sex": "Male"},
    "es_speaker_8": {"prompt": "v2/es_speaker_8", "language": "Spanish", "sex": "Female"},
    "es_speaker_9": {"prompt": "v2/es_speaker_9", "language": "Spanish", "sex": "Female"}
}

# Turkish speakers
turkish_speakers = {
    "tr_speaker_0": {"prompt": "v2/tr_speaker_0", "language": "Turkish", "sex": "Male"},
    "tr_speaker_1": {"prompt": "v2/tr_speaker_1", "language": "Turkish", "sex": "Male"},
    "tr_speaker_2": {"prompt": "v2/tr_speaker_2", "language": "Turkish", "sex": "Male"},
    "tr_speaker_3": {"prompt": "v2/tr_speaker_3", "language": "Turkish", "sex": "Male"},
    "tr_speaker_4": {"prompt": "v2/tr_speaker_4", "language": "Turkish", "sex": "Female"},
    "tr_speaker_5": {"prompt": "v2/tr_speaker_5", "language": "Turkish", "sex": "Female"},
    "tr_speaker_6": {"prompt": "v2/tr_speaker_6", "language": "Turkish", "sex": "Male"},
    "tr_speaker_7": {"prompt": "v2/tr_speaker_7", "language": "Turkish", "sex": "Male"},
    "tr_speaker_8": {"prompt": "v2/tr_speaker_8", "language": "Turkish", "sex": "Male"},
    "tr_speaker_9": {"prompt": "v2/tr_speaker_9", "language": "Turkish", "sex": "Male"}
}

# General dictionary that maps language codes to speaker dictionaries
speaker_presets = {
    "en": {"name": "English", "speakers": english_speakers},
    "zh": {"name": "Chinese", "speakers": chinese_speakers},
    "fr": {"name": "French", "speakers": french_speakers},
    "pl": {"name": "Polish", "speakers": polish_speakers},
    "pt": {"name": "Portuguese", "speakers": portuguese_speakers},
    "ru": {"name": "Russian", "speakers": russian_speakers},
    "es": {"name": "Spanish", "speakers": spanish_speakers},
    "tr": {"name": "Turkish", "speakers": turkish_speakers}
}

# Dictionary with all speakers combined for direct access
all_speakers = {}
for lang_speakers in speaker_presets.values():
    all_speakers.update(lang_speakers["speakers"])


