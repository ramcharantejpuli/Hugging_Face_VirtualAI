# CSM-355: Machine Learning Project
## CA-1 (30% Progress Report)

## 1. Problem Understanding & Definition

### 1.1 Clarity of Problem Statement (4 Marks)
The project aims to develop an intelligent voice-controlled AI assistant named "Bittu" that can understand and respond to natural language commands. The assistant integrates speech recognition, natural language processing, and system automation to provide users with a hands-free way to control their computer and access information. By combining ChatGPT's intelligence with system control capabilities, the assistant addresses the need for a more natural and efficient way to interact with computers.

### 1.2 Justification for Solving the Problem (3 Marks)
Traditional computer interaction through keyboard and mouse can be inefficient and time-consuming for many tasks. Voice assistants offer several advantages:
- **Accessibility**: Helps users with physical limitations or those who find traditional input methods challenging
- **Efficiency**: Enables multitasking and faster command execution through natural speech
- **Learning Curve**: Reduces the learning curve as users can interact using natural language
- **Productivity**: Studies show that voice commands can be 3x faster than typing for certain tasks
- **Future Relevance**: Voice AI market is expected to grow to $32 billion by 2025, showing increasing demand

### 1.3 Defined Objectives & Hypotheses (3 Marks)

**Objectives:**
1. Develop a voice-activated assistant that responds to wake words "Hey Bittu" or "OK Bittu"
2. Implement reliable speech recognition with natural language understanding
3. Create a visually appealing and responsive GUI with animation feedback
4. Integrate ChatGPT for intelligent conversation handling
5. Enable system control through voice commands (apps, media, system settings)
6. Provide real-time information (time, weather, news)

**Hypothesis:**
"A voice assistant combining local system control with AI-powered conversations will significantly improve user interaction with computers compared to traditional input methods."

## 2. Dataset Selection & Preprocessing

### 2.1 Dataset Relevance and Quality (3 Marks)

#### 2.1.1 Dataset Selection
For this project, we utilize multiple types of data:

1. **Speech Recognition Data**
   - Source: Real-time audio input through microphone
   - Processing: Google Speech Recognition API
   - Quality: Supports multiple languages and accents
   - Format: Audio stream converted to text

2. **Command Dataset**
   - Custom-built command recognition patterns
   - Categories: System commands, web commands, media controls
   - Size: 50+ command patterns
   - Types: String patterns, regular expressions

3. **ChatGPT Training Data**
   - Source: OpenAI GPT-3.5 model
   - Coverage: General knowledge and conversation
   - Quality: State-of-the-art language model
   - Purpose: Natural language understanding and response generation

### 2.2 Handling Missing Values, Outliers, and Data Normalization (3 Marks)

#### 2.2.1 Handling Missing Values
- **Speech Recognition**
  - Implemented timeout handling for no audio input
  - Added error handling for failed recognition attempts
  - Fallback to text input when audio fails

#### 2.2.2 Handling Audio Quality
- **Noise Reduction**
  - Implemented energy threshold adjustment
  - Added pause detection
  - Filtered out background noise

#### 2.2.3 Data Normalization
- **Text Processing**
  - Convert all commands to lowercase
  - Remove extra whitespace
  - Standardize command patterns
  ```python
  data_btn = str(data_btn).lower().strip()
  ```

### 2.3 Feature Selection & Engineering (4 Marks)

#### A. Feature Selection
1. **Command Recognition Features**
   - Wake word detection
   - Command pattern matching
   - Context awareness
   - Time-based responses

2. **System Integration Features**
   - Application control
   - Media management
   - System monitoring
   - Web access

#### B. Feature Engineering
1. **Time-Based Features**
   ```python
   def get_greeting():
       hour = datetime.datetime.now().hour
       if 5 <= hour < 12:
           return "Good morning"
       elif 12 <= hour < 17:
           return "Good afternoon"
       elif 17 <= hour < 21:
           return "Good evening"
       else:
           return "Good night"
   ```

2. **System Monitoring Features**
   ```python
   def get_system_info():
       cpu_usage = psutil.cpu_percent()
       memory = psutil.virtual_memory()
       disk = psutil.disk_usage('/')
       return {
           'cpu': cpu_usage,
           'memory': memory,
           'disk': disk
       }
   ```

3. **Command Categories**
   - Basic commands (greetings, time, date)
   - System operations (open apps, control media)
   - Web commands (open websites, search)
   - Information queries (weather, news, jokes)

[Note: Screenshots of the working application, GUI interface, and command execution will be added in the final PDF version]
