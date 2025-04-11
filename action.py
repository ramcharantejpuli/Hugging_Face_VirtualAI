import datetime
import pyttsx3
import os
import webbrowser
import json
import speak
import requests
import weather
import subprocess
import psutil
import platform
import pyautogui
from config import HUGGINGFACE_API_KEY, HF_MODEL_NAME

def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWS_API_KEY"
        response = requests.get(url)
        news = json.loads(response.text)
        return news['articles'][0]['title']
    except:
        return "Sorry, couldn't fetch news at the moment."

def get_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url)
        joke = json.loads(response.text)
        return f"{joke['setup']} ... {joke['punchline']}"
    except:
        return "Sorry, couldn't fetch a joke at the moment."

def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_used = round(memory.used / (1024.0 ** 3), 2)  # Convert to GB
        memory_total = round(memory.total / (1024.0 ** 3), 2)  # Convert to GB
        disk = psutil.disk_usage('/')
        disk_used = round(disk.used / (1024.0 ** 3), 2)  # Convert to GB
        disk_total = round(disk.total / (1024.0 ** 3), 2)  # Convert to GB
        
        info = f"CPU Usage: {cpu_usage}%\n"
        info += f"Memory: {memory_used}GB used out of {memory_total}GB\n"
        info += f"Disk: {disk_used}GB used out of {disk_total}GB\n"
        info += f"Operating System: {platform.system()} {platform.release()}"
        return info
    except:
        return "Sorry, couldn't fetch system information."

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            power_plugged = battery.power_plugged
            status = "plugged in" if power_plugged else "not plugged in"
            return f"Battery at {percent}% and {status}"
        return "No battery detected"
    except:
        return "Couldn't get battery information"

def get_ip_info():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json()['ip']
        return f"Your public IP address is: {public_ip}"
    except:
        return "Couldn't fetch IP information"

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

def chat_with_hf(prompt):
    try:
        API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_NAME}"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        # Format the prompt for better responses
        formatted_prompt = f"Assistant: I am Bittu, a helpful AI assistant. Please help with: {prompt}\nResponse:"
        
        # Make API call
        response = requests.post(API_URL, headers=headers, json={"inputs": formatted_prompt})
        
        if response.status_code == 200:
            # Extract the response text
            result = response.json()[0]['generated_text']
            # Clean up the response if needed
            result = result.replace('Assistant:', '').replace('Response:', '').strip()
            return result if result else "I'm not sure how to help with that."
        else:
            print(f"HuggingFace API Error: {response.status_code}")
            return "I'm having trouble connecting to my brain right now."
            
    except Exception as e:
        print(f"HuggingFace Error: {str(e)}")
        return "I'm having trouble connecting to my brain right now."

def Action(data_btn):
    data_btn = str(data_btn).lower().strip()
    
    # Basic commands
    if "hello" in data_btn or "hi" in data_btn:
        greeting = get_greeting()
        speak.speak(f"{greeting}! How can I help you today?")
        return f"{greeting}! How can I help you today?"
        
    elif "good morning" in data_btn or "morning" in data_btn:
        greeting = get_greeting()
        response = f"{greeting}! I hope you have a wonderful day ahead."
        speak.speak(response)
        return response
        
    elif "good afternoon" in data_btn or "afternoon" in data_btn:
        greeting = get_greeting()
        response = f"{greeting}! I hope you're having a great day."
        speak.speak(response)
        return response
        
    elif "good evening" in data_btn or "evening" in data_btn:
        greeting = get_greeting()
        response = f"{greeting}! I hope you had a productive day."
        speak.speak(response)
        return response
        
    elif "good night" in data_btn or "night" in data_btn:
        greeting = get_greeting()
        response = f"{greeting}! Have a peaceful rest."
        speak.speak(response)
        return response
        
    elif "what is your name" in data_btn or "who are you" in data_btn:
        speak.speak("My name is Bittu, your AI Assistant! I'm here to help you with anything you need.")
        return "My name is Bittu, your AI Assistant!"
        
    elif "what's my name" in data_btn or "do you know me" in data_btn:
        speak.speak("Your name is Lavanya, and it's a pleasure to assist you!")
        return "Your name is Lavanya!"
        
    # Time and Date
    elif "time now" in data_btn or "what's the time" in data_btn or "time" in data_btn:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak.speak(f"The current time is {current_time}")
        return f"The current time is {current_time}"
        
    elif "date" in data_btn or "what's the date" in data_btn:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak.speak(f"Today's date is {current_date}")
        return f"Today's date is {current_date}"
        
    elif "day" in data_btn or "what day is it" in data_btn:
        day = datetime.datetime.now().strftime("%A")
        speak.speak(f"Today is {day}")
        return f"Today is {day}"
        
    # System Information
    elif "system info" in data_btn or "computer status" in data_btn:
        info = get_system_info()
        speak.speak("Here's your system information")
        return info
        
    elif "battery" in data_btn or "power status" in data_btn:
        info = get_battery_info()
        speak.speak(info)
        return info
        
    elif "cpu usage" in data_btn:
        usage = psutil.cpu_percent()
        speak.speak(f"CPU usage is {usage}%")
        return f"CPU usage is {usage}%"
        
    elif "memory usage" in data_btn or "ram usage" in data_btn:
        memory = psutil.virtual_memory()
        used = round(memory.used / (1024.0 ** 3), 2)
        total = round(memory.total / (1024.0 ** 3), 2)
        speak.speak(f"Memory usage is {used}GB out of {total}GB")
        return f"Memory usage: {used}GB / {total}GB"
        
    elif "ip address" in data_btn or "what's my ip" in data_btn:
        info = get_ip_info()
        speak.speak(info)
        return info
        
    # Entertainment
    elif "tell me a joke" in data_btn or "joke" in data_btn:
        joke = get_joke()
        speak.speak(joke)
        return joke
        
    elif "news" in data_btn or "latest news" in data_btn:
        news = get_news()
        speak.speak(f"Here's the latest headline: {news}")
        return f"Latest News: {news}"
        
    elif "weather" in data_btn:
        weather_info = weather.get_weather()
        speak.speak(weather_info)
        return weather_info
        
    # System commands
    elif "open" in data_btn:
        # Browsers
        if "chrome" in data_btn:
            os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
            speak.speak("Opening Chrome")
            return "Opening Chrome"
        elif "edge" in data_btn:
            os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            speak.speak("Opening Microsoft Edge")
            return "Opening Microsoft Edge"
            
        # System apps
        elif "notepad" in data_btn:
            os.system("start notepad")
            speak.speak("Opening Notepad")
            return "Opening Notepad"
        elif "calculator" in data_btn:
            os.system("start calc")
            speak.speak("Opening Calculator")
            return "Opening Calculator"
        elif "paint" in data_btn:
            os.system("start mspaint")
            speak.speak("Opening Paint")
            return "Opening Paint"
        elif "camera" in data_btn:
            os.system("start microsoft.windows.camera:")
            speak.speak("Opening Camera")
            return "Opening Camera"
        elif "settings" in data_btn:
            os.system("start ms-settings:")
            speak.speak("Opening Settings")
            return "Opening Settings"
        elif "control panel" in data_btn:
            os.system("start control panel")
            speak.speak("Opening Control Panel")
            return "Opening Control Panel"
        elif "task manager" in data_btn:
            os.system("start taskmgr")
            speak.speak("Opening Task Manager")
            return "Opening Task Manager"
        elif "file explorer" in data_btn or "this pc" in data_btn:
            os.system("start explorer")
            speak.speak("Opening File Explorer")
            return "Opening File Explorer"
        elif "cmd" in data_btn or "command prompt" in data_btn:
            os.system("start cmd")
            speak.speak("Opening Command Prompt")
            return "Opening Command Prompt"
        elif "powershell" in data_btn:
            os.system("start powershell")
            speak.speak("Opening PowerShell")
            return "Opening PowerShell"
            
        # Websites
        elif "google" in data_btn:
            webbrowser.open("https://www.google.com")
            speak.speak("Opening Google")
            return "Opening Google"
        elif "youtube" in data_btn:
            webbrowser.open("https://www.youtube.com")
            speak.speak("Opening YouTube")
            return "Opening YouTube"
        elif "instagram" in data_btn:
            webbrowser.open("https://www.instagram.com")
            speak.speak("Opening Instagram")
            return "Opening Instagram"
        elif "facebook" in data_btn:
            webbrowser.open("https://www.facebook.com")
            speak.speak("Opening Facebook")
            return "Opening Facebook"
        elif "linkedin" in data_btn:
            webbrowser.open("https://www.linkedin.com")
            speak.speak("Opening LinkedIn")
            return "Opening LinkedIn"
        elif "whatsapp" in data_btn:
            webbrowser.open("https://web.whatsapp.com")
            speak.speak("Opening WhatsApp Web")
            return "Opening WhatsApp Web"
        elif "spotify" in data_btn or "music" in data_btn:
            webbrowser.open("https://open.spotify.com")
            speak.speak("Opening Spotify")
            return "Opening Spotify"
        elif "github" in data_btn:
            webbrowser.open("https://github.com")
            speak.speak("Opening GitHub")
            return "Opening GitHub"
        elif "gmail" in data_btn:
            webbrowser.open("https://mail.google.com")
            speak.speak("Opening Gmail")
            return "Opening Gmail"
            
    # System Control
    elif "lock" in data_btn and "computer" in data_btn:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak.speak("Locking your computer")
        return "Locking computer"
        
    elif "restart" in data_btn and "computer" in data_btn:
        speak.speak("Restarting your computer in 1 minute")
        os.system("shutdown /r /t 60")
        return "Restarting computer in 1 minute"
        
    elif "cancel restart" in data_btn or "cancel shutdown" in data_btn:
        os.system("shutdown /a")
        speak.speak("Cancelled restart/shutdown")
        return "Cancelled restart/shutdown"
        
    elif ("shutdown" in data_btn and "computer" in data_btn) or "turn off computer" in data_btn:
        speak.speak("Shutting down your computer in 1 minute")
        os.system("shutdown /s /t 60")
        return "Shutting down computer in 1 minute"
        
    # Volume and Media Control
    elif "mute" in data_btn:
        os.system("nircmd.exe mutesysvolume 1")
        speak.speak("Audio muted")
        return "Audio muted"
        
    elif "unmute" in data_btn:
        os.system("nircmd.exe mutesysvolume 0")
        speak.speak("Audio unmuted")
        return "Audio unmuted"
        
    elif "volume up" in data_btn:
        pyautogui.press("volumeup")
        speak.speak("Volume increased")
        return "Volume increased"
        
    elif "volume down" in data_btn:
        pyautogui.press("volumedown")
        speak.speak("Volume decreased")
        return "Volume decreased"
        
    elif "play" in data_btn or "pause" in data_btn:
        pyautogui.press("playpause")
        return "Toggled play/pause"
        
    elif "next track" in data_btn or "next song" in data_btn:
        pyautogui.press("nexttrack")
        return "Next track"
        
    elif "previous track" in data_btn or "previous song" in data_btn:
        pyautogui.press("prevtrack")
        return "Previous track"
        
    # Exit Commands
    elif "bye" in data_btn or "goodbye" in data_btn or "exit" in data_btn or "quit" in data_btn or "shutdown" in data_btn:
        speak.speak("Goodbye! Have a great day!")
        return "ok sir"
        
    # Use HuggingFace for all other queries
    else:
        response = chat_with_hf(data_btn)
        speak.speak(response)
        return response
