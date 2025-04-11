import speech_recognition as sr 
from requests_html import HTMLSession
import speak
import time

def spech_to_text(timeout=None):
    r = sr.Recognizer()
    r.energy_threshold = 3000  # Adjusted for better sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.6  # Shorter pause for more responsive detection
    r.phrase_threshold = 0.3  # Better at catching short commands
    
    with sr.Microphone() as source:
        try:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            if timeout:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=None)
            else:
                audio = r.listen(source)
            print("Processing speech...")
            
            voice_data = r.recognize_google(audio, language='en-IN')  # Using Indian English
            print(f"Recognized: {voice_data}")
            return voice_data.lower()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError:
            speak.speak('Please check your internet connection')
            print("Could not request results")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
