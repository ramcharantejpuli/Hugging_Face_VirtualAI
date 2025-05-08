import speech_recognition as sr 
from requests_html import HTMLSession
import speak
import time

# Global flag to control speech recognition
LISTENING_ENABLED = True

def spech_to_text(timeout=None):
    global LISTENING_ENABLED
    
    # If listening is disabled, return immediately
    if not LISTENING_ENABLED:
        print("Speech recognition is disabled")
        return None
    
    r = sr.Recognizer()
    r.energy_threshold = 2500  # Lower threshold for better sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5  # Shorter pause for more responsive detection
    r.phrase_threshold = 0.3  # Better at catching short commands
    r.non_speaking_duration = 0.3  # Shorter non-speaking duration for quicker response
    
    with sr.Microphone() as source:
        try:
            # Check again if listening is still enabled
            if not LISTENING_ENABLED:
                return None
                
            print("Listening...")
            # Longer ambient noise adjustment for better calibration
            r.adjust_for_ambient_noise(source, duration=1.0)
            
            # Add a slight delay to ensure microphone is fully ready
            time.sleep(0.2)
            
            # Check again if listening is still enabled
            if not LISTENING_ENABLED:
                return None
                
            if timeout:
                # Increased phrase_time_limit for longer commands
                audio = r.listen(source, timeout=timeout, phrase_time_limit=10)
            else:
                audio = r.listen(source)
                
            # Check again if listening is still enabled
            if not LISTENING_ENABLED:
                return None
                
            print("Processing speech...")
            
            # Try multiple language options for better recognition
            try:
                voice_data = r.recognize_google(audio, language='en-IN')  # Try Indian English first
            except:
                try:
                    voice_data = r.recognize_google(audio, language='en-US')  # Fall back to US English
                except:
                    voice_data = r.recognize_google(audio)  # Last resort: default language
                    
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
            print(f"Error in speech recognition: {e}")
            return None
            
# Function to enable/disable speech recognition
def set_listening_enabled(enabled):
    global LISTENING_ENABLED
    LISTENING_ENABLED = enabled
    return LISTENING_ENABLED
