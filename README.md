# 🎙️ VocaFree AI: Zero-Cost, Low-Latency Voice Interface

[![Live Demo on Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Try%20Live%20Demo-blue)](https://huggingface.co/spaces/MalikShehram/VocaFree_AI)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Groq Powered](https://img.shields.io/badge/Powered%20by-Groq%20LPU-f97316)](https://groq.com/)

**VocaFree AI** is a research and development prototype demonstrating a high-efficiency pipeline for real-time, voice-to-voice AI interaction. 

Designed to bypass traditional, expensive paid APIs, this project achieves conversational latency comparable to premium subscription services at **zero operating cost** by intelligently routing open-weight models through free-tier infrastructure.

---

## ✨ Key Features

* **Real-Time Processing:** Achieves near-instantaneous AI responses using Groq's specialized Language Processing Units (LPUs).
* **Zero-Cost Architecture:** Built entirely utilizing open-source models and free-tier API limits.
* **Persistent Memory:** Maintains conversation history dynamically during the active session.
* **Clean UI/UX:** Features a professional, responsive Gradio interface deployed via Docker.

---

## 📊 System Architecture

The data flow is structured to maximize speed while minimizing computational overhead:

1. **Input (Speech-to-Text):** User audio is captured via the browser and processed locally/in-container using **OpenAI's Whisper (Base)** model.
2. **Processing (LLM):** The transcribed text is securely passed to **Meta's LLaMA 3.3 (70B)**. Inference is handled via the **Groq API** to ensure ultra-low latency.
3. **Output (Text-to-Speech):** The AI's text response is synthesized back into natural-sounding audio using **Google Text-to-Speech (gTTS)**.
4. **Interface:** The frontend is built with **Gradio 5.x** and containerized for deployment on Hugging Face Spaces.

---

## 🚀 Local Installation & Setup

Want to run this prototype locally? Follow these steps:

### Prerequisites
* Python 3.10 or higher
* [FFmpeg](https://ffmpeg.org/download.html) installed on your system (required for Whisper audio processing)
* A free [Groq API Key](https://console.groq.com/keys)

### Quick Start

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/VocaFree-AI.git](https://github.com/YOUR_GITHUB_USERNAME/VocaFree-AI.git)
cd VocaFree-AI
