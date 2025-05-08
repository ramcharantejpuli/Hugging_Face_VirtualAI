from tkinter import*
from PIL import Image, ImageTk
import action 
import spech_to_text
import speak
import os
import threading
import math
import time

# We'll use the LISTENING_ENABLED flag from spech_to_text.py

# Professional color scheme
COLORS = {
    'primary': '#2C3E50',    # Dark blue-gray
    'secondary': '#34495E',  # Lighter blue-gray
    'accent': '#3498DB',     # Bright blue
    'background': '#ECF0F1', # Light gray
    'text': '#2C3E50'        # Dark blue-gray
}

# Voice Animation class with enhanced design
class VoiceAnimation:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.circles = []
        self.animation_running = False
        self.listening = False
        self.timeout_timer = None
        self.create_circles()
        
    def create_circles(self):
        colors = [COLORS['accent'], COLORS['secondary'], COLORS['primary']]
        for i in range(3):
            circle = self.canvas.create_oval(
                self.x - 25 - i*20, self.y - 25 - i*20,
                self.x + 25 + i*20, self.y + 25 + i*20,
                outline=colors[i], width=3
            )
            self.circles.append(circle)
        
        # Add central dot
        self.center_dot = self.canvas.create_oval(
            self.x - 8, self.y - 8,
            self.x + 8, self.y + 8,
            fill=COLORS['accent'], outline=COLORS['accent']
        )
    
    def animate(self):
        if not self.animation_running:
            return
            
        t = time.time() * 3
        for i, circle in enumerate(self.circles):
            scale = 1 + 0.3 * math.sin(t + i * 0.5)
            self.canvas.coords(
                circle,
                self.x - 25*scale - i*20, self.y - 25*scale - i*20,
                self.x + 25*scale + i*20, self.y + 25*scale + i*20
            )
            
            # Pulse the center dot
            dot_scale = 1 + 0.2 * math.sin(t * 2)
            self.canvas.coords(
                self.center_dot,
                self.x - 8*dot_scale, self.y - 8*dot_scale,
                self.x + 8*dot_scale, self.y + 8*dot_scale
            )
        self.canvas.after(50, self.animate)
    
    def start_animation(self):
        self.animation_running = True
        self.listening = True
        self.animate()
    
    def stop_animation(self):
        self.animation_running = False
        self.listening = False
        # Reset circles to original size
        for i, circle in enumerate(self.circles):
            self.canvas.coords(
                circle,
                self.x - 25 - i*20, self.y - 25 - i*20,
                self.x + 25 + i*20, self.y + 25 + i*20
            )
        # Reset center dot
        self.canvas.coords(
            self.center_dot,
            self.x - 8, self.y - 8,
            self.x + 8, self.y + 8
        )

def continuous_listen():
    global voice_animation
    r = spech_to_text.sr.Recognizer()
    r.energy_threshold = 2800  # Improved sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5  # Slightly shorter pause for better responsiveness
    r.phrase_threshold = 0.3  # Better at catching short commands
    
    def listen_for_wake_word():
        # Only listen if enabled
        if not spech_to_text.LISTENING_ENABLED:
            time.sleep(0.5)  # Sleep briefly to avoid CPU hogging
            return False
            
        try:
            with spech_to_text.sr.Microphone() as source:
                print("Waiting for wake word...")
                # Increase duration for better ambient noise adjustment
                r.adjust_for_ambient_noise(source, duration=1.0)
                # Lower energy threshold for better sensitivity to wake words
                r.energy_threshold = 2500
                # Increase phrase time limit to catch full wake phrase
                audio = r.listen(source, phrase_time_limit=5)
                try:
                    voice_data = r.recognize_google(audio, language='en-IN')
                    print(f"Heard: {voice_data}")
                    # More flexible wake word detection with partial matching
                    voice_lower = voice_data.lower()
                    if ("hey" in voice_lower and "bittu" in voice_lower) or \
                       ("ok" in voice_lower and "bittu" in voice_lower) or \
                       "hey bittu" in voice_lower or "ok bittu" in voice_lower or \
                       "a bittu" in voice_lower or "o bittu" in voice_lower:
                        spech_to_text.speak.speak("Yes, I'm listening!")
                        return True
                except Exception as e:
                    print(f"Recognition error: {str(e)}")
                    pass
        except Exception as e:
            print(f"Microphone error: {str(e)}")
            pass
        return False

    def conversation_loop():
        while voice_animation.listening and spech_to_text.LISTENING_ENABLED:
            try:
                print("Listening for command...")
                voice_data = spech_to_text.spech_to_text(timeout=8)  # Increased timeout
                if voice_data:
                    print(f"Command detected: {voice_data}")
                    # Process the command and get response
                    bot_val = action.Action(voice_data)
                    
                    # Update UI
                    text.insert(END, "Me --> "+voice_data+"\n")
                    if bot_val is not None:
                        text.insert(END, "Bot <-- "+ str(bot_val)+"\n")
                        text.see(END)
                    
                    if bot_val == "ok sir":
                        root.destroy()
                        return
                else:
                    print("No speech detected, stopping animation")
                    voice_animation.stop_animation()
                    return
            except Exception as e:
                print(f"Error in conversation: {str(e)}")
                continue

    # Main listening loop
    while True:
        if spech_to_text.LISTENING_ENABLED and not voice_animation.listening and listen_for_wake_word():
            print("Wake word detected! Starting conversation...")
            voice_animation.start_animation()
            conversation_loop()
        else:
            time.sleep(0.5)  # Sleep briefly when not listening to avoid CPU hogging

def User_send(event=None):
    
    # Get user input
    send = entry1.get()
    if not send.strip():
        return
    
    # Clear the entry field
    entry1.delete(0, END)
    
    # Update UI with user message
    text.insert(END, "Me --> "+send+"\n")
    text.see(END)
    
    # Get response from Bittu
    bot = action.Action(send)
    
    # Update UI with bot response
    if bot != None:
        text.insert(END, "Bot <-- "+ str(bot)+"\n")
        text.see(END)
    
    # Check for exit command
    if bot == "ok sir":
        root.destroy()

def delete_text():
    text.delete("1.0", "end")

# Create main window with professional styling
root = Tk()
root.geometry("600x750")
root.title("AI Assistant")
root.resizable(False, False)
root.config(bg=COLORS['background'])

# Main Frame with modern styling
Main_frame = LabelFrame(root, padx=100, pady=15, borderwidth=2, relief="flat")
Main_frame.config(bg=COLORS['background'])
Main_frame.grid(row=0, column=0, padx=70, pady=20, sticky="nsew")

# Title with professional font
title_frame = Frame(Main_frame, bg=COLORS['background'])
title_frame.grid(row=0, column=0, pady=(0, 20))
# Center elements in the Main_frame
Main_frame.grid_columnconfigure(0, weight=1)

Text_label = Label(title_frame, text="AI Assistant", font=("Helvetica", 24, "bold"), 
                  bg=COLORS['background'], fg=COLORS['primary'])
Text_label.pack(anchor=CENTER)

subtitle = Label(title_frame, text="Say 'Hey Bittu' or 'OK Bittu' to activate", 
                font=("Helvetica", 12), bg=COLORS['background'], fg=COLORS['secondary'])
subtitle.pack(pady=(5, 0), anchor=CENTER)

# Canvas for voice animation with professional styling
canvas = Canvas(Main_frame, width=250, height=250, bg=COLORS['background'], highlightthickness=0)
canvas.grid(row=1, column=0, pady=20)
# Create animation with circles perfectly centered in the canvas
voice_animation = VoiceAnimation(canvas, 125, 125)

# Text widget with modern styling
text_frame = Frame(root, bg=COLORS['background'])
text_frame.grid(row=1, column=0, padx=70, pady=(0, 20), sticky="nsew")

text = Text(text_frame, font=('Helvetica', 11), bg=COLORS['secondary'], fg='white',
           padx=10, pady=10, wrap=WORD, relief="flat")
text.pack(fill=BOTH, expand=True)

# Add default welcome message
text.insert(END, "Bot <-- I'm Bittu, your AI Assistant! I'm waiting for your commands.\n")
text.see(END)

# Entry widget with modern styling
entry_frame = Frame(root, bg=COLORS['background'])
entry_frame.grid(row=2, column=0, padx=70, pady=(0, 20), sticky="nsew")

entry1 = Entry(entry_frame, font=('Helvetica', 11), justify=CENTER, relief="flat",
               bg='white', fg=COLORS['text'])
entry1.pack(fill=X, ipady=8, side=LEFT, expand=True)

# Add an Enter button next to the input field
enter_button = Button(entry_frame, text="↵", command=User_send, font=('Helvetica', 11),
                     bg=COLORS['primary'], fg='white', relief="flat", cursor="hand2", padx=10)
enter_button.pack(side=RIGHT, padx=5, ipady=5)

# Bind Enter key to send message
entry1.bind("<Return>", User_send)

# Buttons frame with modern styling
button_frame = Frame(root, bg=COLORS['background'])
button_frame.grid(row=3, column=0, padx=70, pady=(0, 30), sticky="nsew")

button_style = {
    'font': ('Helvetica', 11),
    'bg': COLORS['primary'],
    'fg': 'white',
    'padx': 30,
    'pady': 10,
    'relief': 'flat',
    'cursor': 'hand2'
}

# Stop button that stops speech and listening
def stop_bittu():
    # Stop the speech
    speak.stop_speaking()
    
    # Toggle listening state using the function from spech_to_text
    current_state = spech_to_text.set_listening_enabled(not spech_to_text.LISTENING_ENABLED)
    
    # Update button text based on state
    if current_state:
        stop_button.config(text="Stop")
        text.insert(END, "Bot <-- Listening enabled.\n")
    else:
        stop_button.config(text="Start")
        text.insert(END, "Bot <-- Listening disabled.\n")
    
    # Stop animation if needed
    if not current_state and voice_animation.listening:
        voice_animation.stop_animation()
    
    text.see(END)

stop_button = Button(button_frame, text="Stop", command=stop_bittu, **button_style)
stop_button.pack(side=RIGHT, padx=5)

button3 = Button(button_frame, text="Clear", command=delete_text, **button_style)
button3.pack(side=RIGHT, padx=5)

# Configure grid weights
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start continuous listening in a separate thread
listen_thread = threading.Thread(target=continuous_listen, daemon=True)
listen_thread.start()

root.mainloop()