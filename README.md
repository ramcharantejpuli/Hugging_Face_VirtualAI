# Bittu - Your Intelligent Voice Assistant 🎙️

## Overview
Bittu is a sophisticated voice assistant that combines the power of Groq's AI models with system automation to create a seamless voice-controlled computing experience. Using natural language, you can control your computer, get information, and have intelligent conversations.

## 🌟 Key Features

### 🗣️ Voice Control
- Wake word detection: "Hey Bittu" or "OK Bittu"
- Natural language understanding using Groq AI
- Dynamic circle animation for visual feedback
- Automatic timeout after 7 seconds of silence

### 🤖 AI Integration
- Groq's Llama 3 70B language model for intelligent responses
- Ultra-fast inference for quick response times
- Context-aware conversations
- Natural and informative replies

### ⚡ System Commands
- **Media Control**
  - "Volume up/down" - Adjust system volume
  - "Play/pause" - Control media playback
  - "Next/previous track" - Navigate music

- **Application Launch**
  - "Open Chrome/Edge" - Launch browsers
  - "Open calculator/notepad/paint" - System tools
  - "Open camera" - Access webcam
  - "Open task manager" - System monitoring

- **Web Navigation**
  - "Open YouTube/Instagram/WhatsApp"
  - "Google search"
  - "Check weather"
  - "Latest news"

### Time & Information
- Time-based greetings (morning/afternoon/evening)
- Current time and date
- Weather updates
- Random jokes

## Technical Stack
- **Python 3.10.11** - Core programming
- **SpeechRecognition** - Voice input processing
- **pyttsx3** - Text-to-speech conversion
- **Groq API** - AI language model (Llama 3 70B)
- **PyAudio** - Audio processing
- **pyautogui** - System control
- **psutil** - System monitoring

## Installation

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Groq API:
- Get API key from [Groq](https://console.groq.com/)
- Add key to `action.py` (API key variable is defined at the top of the file)

## 🚀 Usage

1. Start the assistant:
```bash
python gui.py
```

2. Say "Hey Bittu" or "OK Bittu"
3. Wait for the animation
4. Speak your command

## 📝 Common Commands

```plaintext
General:
- "Hello/Hi"
- "How are you?"
- "Thank you"
- "Goodbye/Exit"

System:
- "Open [application]"
- "Volume up/down"
- "Play/pause music"
- "Next/previous track"

Information:
- "What's the time?"
- "Weather"
- "Tell me a joke"
- "Latest news"

Web:
- "Open YouTube"
- "Open Google"
- "Open Instagram"
```

## 🔧 Configuration
- Adjust wake word sensitivity in `gui.py`
- Customize AI responses in `action.py`
- Modify system commands in `action.py`
- Configure Groq API key in `action.py`

## 📂 Project Structure
```
Virtual Assistant/
├── gui.py           # Main interface & wake word
├── action.py        # Command processing & AI with Groq API key
├── speak.py         # Text-to-speech engine
├── spech_to_text.py # Voice recognition
├── weather.py       # Weather service
└── requirements.txt # Dependencies
```

## 🎯 Future Enhancements
1. Custom wake word training
2. Multi-language support
3. Smart home integration
4. Calendar management
5. Email integration

## 👨‍💻 Author
**Puli Ram Charan Tej ❤️**
CSM355CA1 - AI and ML Project

## 📄 License
This project is for educational purposes. Created as part of CSM355 coursework.
