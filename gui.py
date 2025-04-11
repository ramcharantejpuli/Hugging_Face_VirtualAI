from tkinter import*
from PIL import Image, ImageTk
import action 
import spech_to_text
import os
import threading
import math
import time

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
    r.energy_threshold = 3000  # Better sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.6
    
    def listen_for_wake_word():
        while True:
            try:
                with spech_to_text.sr.Microphone() as source:
                    print("Waiting for wake word...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, phrase_time_limit=3)
                    try:
                        voice_data = r.recognize_google(audio, language='en-IN')
                        print(f"Heard: {voice_data}")
                        if "hey bittu" in voice_data.lower() or "ok bittu" in voice_data.lower():
                            spech_to_text.speak.speak("Yes, I'm listening!")
                            return True
                    except:
                        pass
            except:
                pass
        return False

    def conversation_loop():
        while voice_animation.listening:
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
        if not voice_animation.listening and listen_for_wake_word():
            print("Wake word detected! Starting conversation...")
            voice_animation.start_animation()
            conversation_loop()

def User_send():
    send = entry1.get()
    bot = action.Action(send)
    text.insert(END, "Me --> "+send+"\n")
    if bot != None:
        text.insert(END, "Bot <-- "+ str(bot)+"\n")
        text.see(END)
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

Text_label = Label(title_frame, text="AI Assistant", font=("Helvetica", 24, "bold"), 
                  bg=COLORS['background'], fg=COLORS['primary'])
Text_label.pack()

subtitle = Label(title_frame, text="Say 'Hey Bittu' or 'OK Bittu' to activate", 
                font=("Helvetica", 12), bg=COLORS['background'], fg=COLORS['secondary'])
subtitle.pack(pady=(5, 0))

# Canvas for voice animation with professional styling
canvas = Canvas(Main_frame, width=250, height=250, bg=COLORS['background'], highlightthickness=0)
canvas.grid(row=1, column=0, pady=20)
voice_animation = VoiceAnimation(canvas, 125, 125)

# Text widget with modern styling
text_frame = Frame(root, bg=COLORS['background'])
text_frame.grid(row=1, column=0, padx=70, pady=(0, 20), sticky="nsew")

text = Text(text_frame, font=('Helvetica', 11), bg=COLORS['secondary'], fg='white',
           padx=10, pady=10, wrap=WORD, relief="flat")
text.pack(fill=BOTH, expand=True)

# Entry widget with modern styling
entry_frame = Frame(root, bg=COLORS['background'])
entry_frame.grid(row=2, column=0, padx=70, pady=(0, 20), sticky="nsew")

entry1 = Entry(entry_frame, font=('Helvetica', 11), justify=CENTER, relief="flat",
               bg='white', fg=COLORS['text'])
entry1.pack(fill=X, ipady=8)

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

button2 = Button(button_frame, text="Send", command=User_send, **button_style)
button2.pack(side=RIGHT, padx=5)

button3 = Button(button_frame, text="Clear", command=delete_text, **button_style)
button3.pack(side=RIGHT, padx=5)

# Configure grid weights
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start continuous listening in a separate thread
listen_thread = threading.Thread(target=continuous_listen, daemon=True)
listen_thread.start()

root.mainloop()