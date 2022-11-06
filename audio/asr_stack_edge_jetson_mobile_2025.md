# Optimized Speech Recognition Technology Stack for Mobile Devices and Jetson Orin Nano​
- [k2-Sherpa-ONNX-Icefall-Kaldi](./k2-Sherpa-ONNX-Icefall-Kaldi.md)

## Top 10 Open-Source ASR Repositories for Edge Deployment

### **1. [Vosk](https://github.com/alphacep/vosk-api)**  
**Use for**: Lightweight, real-time **offline ASR**  
- Optimized for edge devices (Jetson, Raspberry Pi)  
- JSON output with timestamps, multiple languages  
- Extremely low resource footprint  
- Trained models available and customizable  

---

### **2. [Sherpa-ONNX](https://github.com/k2-fsa/sherpa-onnx)**  
**Use for**: **Streaming or non-streaming ONNX ASR** inference  
- Converts Whisper, Transducer, CTC models into fast ONNX pipelines  
- Supports **C++ and Python**, Jetson-friendly  
- Designed for low-latency edge deployment  

---

### **3. [Icefall](https://github.com/k2-fsa/icefall)**  
**Use for**: Training modern ASR models: **CTC, Transducer, Whisper**  
- Replaces Kaldi training pipeline with PyTorch  
- Works with Sherpa-ONNX for deployment  
- Prepares Kaldi-style data and handles multilingual training  

---

### **4. [k2](https://github.com/k2-fsa/k2)**  
**Use for**: Finite state automata (FSA/FST) for ASR decoding  
- Low-level library used by Icefall and Sherpa  
- GPU-accelerated decoding and lattice composition  
- Core engine for next-gen Kaldi-compatible decoders  

---

### **5. [Kaldi](https://github.com/kaldi-asr/kaldi)**  
**Use for**: Legacy, robust ASR toolkit  
- Highly flexible, supports large-vocabulary ASR, speaker adaptation, lattice-based decoding  
- Not ideal for edge due to complexity and resource use, but excellent for backend and research  
- Rich collection of recipes (e.g., Librispeech, Aishell, AMI)  

---

### **6. [ESPnet](https://github.com/espnet/espnet)**  
**Use for**: **End-to-end ASR + NLU**, speech translation, diarization  
- PyTorch-based, supports transformer and RNN architectures  
- Integrates with Kaldi for feature extraction and alignment  
- Supports speech-to-intent models with slot filling  

---

### **7. [AlphaCephei Kaldi Models](https://github.com/alphacep/kaldi-models)**  
**Use for**: Pretrained models for **Vosk and Kaldi**  
- Multilingual support: English, French, Spanish, Mandarin, etc.  
- Actively maintained for embedded and server-side ASR  
- Essential if using Vosk for quick prototyping  

---

### **8. [Nemo-ASR](https://github.com/NVIDIA/NeMo)**  
**Use for**: Transformer/Conformer-based ASR for NVIDIA Jetson  
- Large model zoo, exportable to ONNX or TorchScript  
- Kaldi-compatible features, high accuracy  
- Less lightweight than Vosk but GPU-accelerated  

---

### **9. [Whisper Models in Sherpa](https://github.com/k2-fsa/sherpa-onnx/blob/master/docs/whisper.md)**  
**Use for**: Deploying **Whisper models** in optimized ONNX runtime  
- Avoids heavy Python-only whisper.cpp runtime  
- Faster inference on Jetson and ARM devices  
- Supports multilingual transcription with timestamps  

---

### **10. [Wenet](https://github.com/wenet-e2e/wenet)**  
**Use for**: Modern CTC/Transducer ASR with Kaldi-style structure  
- Real-time streaming with WebSocket + Python + C++  
- Kaldi-style data prep with PyTorch training  
- ONNX export supported  

---

### Summary Table

| Repo               | Role                                   | Key Strength                                  | Suitable for Edge |
|--------------------|----------------------------------------|-----------------------------------------------|-------------------|
| Vosk               | ASR Inference                          | Lightweight, offline, real-time               | Yes               |
| Sherpa-ONNX        | ASR Inference                          | ONNX streaming ASR                            | Yes               |
| Icefall            | Model Training                         | Whisper, CTC, Transducer training             | Exportable        |
| k2                 | Decoding Core                          | FSA-based decoding backend                    | Yes (GPU)         |
| Kaldi              | Traditional ASR Toolkit                | Stable, modular, well-documented              | No (Too heavy)    |
| ESPnet             | End-to-End ASR & S2I                   | SOTA transformer models, NLU pipelines        | Partial           |
| Kaldi-Models       | Pretrained Vosk-compatible Models      | Immediate use, multilingual                   | Yes               |
| Nemo-ASR           | High-performance Transformer ASR       | NVIDIA hardware optimized                     | Yes (Jetson)      |
| Sherpa-ONNX Whisper| Whisper model optimized inference      | ONNX runtime efficiency                       | Yes               |
| Wenet              | Modern Streaming ASR                   | Fast training + inference                     | Partial           |

## Recommended Technology Stack for Mobile Devices and NVIDIA Jetson Orin Nano
---

### **1. Speech Recognition (ASR)**

- **Sherpa-ONNX**: An efficient, ONNX-based speech recognition toolkit optimized for edge devices. It supports streaming and non-streaming ASR, making it suitable for real-time applications on Jetson Orin Nano.

- **Vosk**: A lightweight, offline speech recognition toolkit that supports multiple languages. It's well-suited for devices with limited resources and has been successfully deployed on Jetson platforms.

---

### **2. Model Training and Customization**

- **Icefall**: A PyTorch-based training framework for modern ASR models like CTC and Transducer. It integrates seamlessly with Sherpa-ONNX for deploying trained models on edge devices.

---

### **3. Deployment and Inference Optimization**

- **ONNX Runtime**: Facilitates the deployment of models trained with frameworks like PyTorch by converting them into a format optimized for inference on devices like the Jetson Orin Nano.

- **TensorRT**: NVIDIA's SDK for high-performance deep learning inference. It can be used to further optimize ONNX models for deployment on Jetson devices, ensuring low latency and efficient resource utilization.

---

### **4. Voice Activity Detection (VAD) and Preprocessing**

- **Silero VAD**: A lightweight and efficient VAD model that can be integrated with ASR systems to improve accuracy by filtering out non-speech segments.

---

### **5. Language Modeling and Intent Recognition**

- **DistilBERT or TinyBERT**: Compact transformer models suitable for intent recognition tasks on resource-constrained devices. They can process the transcribed text from the ASR system to determine user intent.

---

### **6. Text-to-Speech (TTS)**

- **Coqui TTS**: An open-source TTS framework that supports various models, including lightweight ones suitable for edge devices. It can be used to provide voice feedback to users.

---

### **7. Integration and Orchestration**

- **Docker with NVIDIA Container Toolkit**: Facilitates the deployment and management of applications in containers, ensuring consistency and ease of updates across devices.

---

**Note**: While the Jetson Orin Nano offers improved performance over its predecessors, it's essential to consider the resource constraints when selecting models and frameworks. The above stack balances performance with efficiency, ensuring optimal operation on edge devices.

If you require further details on implementing this stack or have specific use cases in mind, feel free to ask! 

