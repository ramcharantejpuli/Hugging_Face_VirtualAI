# pip install pyttsx3

import pyttsx3
import threading
import time

# Global engine and flag
engine = None
engine_busy = False
stop_requested = False

# Create a lock for thread safety
engine_lock = threading.Lock()

def initialize_engine():
    """Initialize the TTS engine"""
    global engine
    if engine is None:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-70)
    return engine

def speak(text):
    """Speak the given text using text-to-speech"""
    global engine_busy, stop_requested
    
    # Don't try to speak empty text
    if not text or len(text.strip()) == 0:
        return
        
    print(f"Speaking: {text}")
    
    # Reset stop flag
    stop_requested = False
    
    # Initialize engine if needed
    initialize_engine()
    
    # Mark engine as busy
    with engine_lock:
        engine_busy = True
    
    # For short responses, use a blocking approach for reliability
    if len(text) < 100:  # Short text, speak directly
        try:
            if not stop_requested:
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")
        finally:
            # Mark engine as not busy
            with engine_lock:
                engine_busy = False
    else:  # Longer text, use threading
        def speak_thread():
            global engine_busy, stop_requested
            try:
                # Only proceed if stop hasn't been requested
                if not stop_requested:
                    engine.say(text)
                    engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                # Mark engine as not busy
                with engine_lock:
                    engine_busy = False
        
        # Run speech in a separate thread
        threading.Thread(target=speak_thread).start()

def stop_speaking():
    """Request to stop speaking"""
    global stop_requested, engine, engine_busy
    
    # Set the stop flag
    stop_requested = True
    
    # Try to stop the engine if it's busy
    with engine_lock:
        if engine_busy and engine is not None:
            try:
                # Try different methods to stop the engine
                engine.stop()
            except:
                # If stopping fails, try to reset the engine
                try:
                    engine = None
                    initialize_engine()
                except:
                    pass
    
    return True  # Indicate stop was requested
