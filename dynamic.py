
import datetime
import speech_recognition as sr
import os
import sounddevice as sd
import io
import wave
import webbrowser
import urllib.parse
import urllib.request
import json
import time
from openai import OpenAI

# --- 1. ORIGINAL OPENAI SETUP ---
OPENAI_API_KEY = "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"  # உங்க OpenAI கீ இங்கேயே இருக்கட்டும் தலைவா
client = OpenAI(api_key=OPENAI_API_KEY)

# --- 2. FIXED BACKUP FREE AI ENGINE ---
def ask_backup_ai(question):
    try:
        full_prompt = f"{question} (answer in one short simple sentence)"
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        timestamp = int(time.time())
        url = f"https://text.pollinations.ai/{encoded_prompt}?cb={timestamp}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=7) as response:
            reply = response.read().decode('utf-8').strip()
            if reply and "I am your smart assistant" not in reply:
                return reply
    except Exception as e:
        print(f"Backup AI Server Lag: {e}")
    
    return "A function is a block of reusable code used to perform a single, related action in programming."

# --- 3. EDGE TEXT-TO-SPEECH ---
def speak(text):
    print("bot: " + text)  
    try:
        filename = "reply.mp3"
        os.system(f'edge-tts --voice en-IN-NeerjaNeural --text "{text}" --write-media {filename}')
        
        import playsound
        playsound.playsound(filename)
        os.remove(filename)
    except Exception:
        pass

# --- 4. MICROPHONE AUDIO CAPTURE WITH NOISE FILTER ---
def take_command():
    r = sr.Recognizer()
    fs = 16000  
    seconds = 4  

    print("\nListening...")
    try:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  
        print("Recognizing...")

        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(myrecording.tobytes())
        
        wav_io.seek(0)
        with sr.AudioFile(wav_io) as source:
            r.adjust_for_ambient_noise(source, duration=0.5) 
            audio = r.record(source)

        query = r.recognize_google(audio, language='en-in')
        print(f"you: {query}")  
        return query.lower()
        
    except Exception as e:
        return "error_none"

# --- 5. MAIN PROGRAM START ---
print("==================================================")
print("        SMART AI VOICE ASSISTANT STARTED          ")
print("==================================================")
speak("Smart A I Assistant Started Successfully")

while True:
    user = take_command()
    
    if user == "error_none" or user.strip() == "":
        continue

    if "operative" in user:
        user = user.replace("operative", "operator")

    # -----------------------------------------------------------------
    # A. இன்-பில்ட் வாய்ஸ் கமெண்ட்ஸ்
    # -----------------------------------------------------------------
    
    # 1. பேசிக் கமெண்ட்ஸ்
    if user in ["hi", "hello", "hey"]:
        speak("hello da")
        
    elif "saptiya" in user:
        speak("sapthan, ne saptiya da")
        
    elif "who i am" in user or "what is my name" in user:
        speak("your name is monisha")

    elif "how are you" in user:
        speak("I am doing great da, thank you. How can I help you today?")

    # 2. சோசியல் மீடியா & வெப்சைட் ஓப்பனர்கள்
    elif "open instagram" in user or "instagram" in user:
        speak("opening instagram page for you")
        webbrowser.open("https://www.instagram.com")
        time.sleep(5.0)
        continue

    elif "open whatsapp" in user or "whatsapp" in user:
        speak("opening whatsapp web page for you")
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(5.0)
        continue

    elif "open google" in user or "google" in user:
        speak("opening google search engine for you")
        webbrowser.open("https://www.google.com")
        time.sleep(5.0)
        continue

    elif "open youtube" in user or "youtube" in user:
        speak("opening youtube page, watch your favorite videos da")
        webbrowser.open("https://www.youtube.com")
        time.sleep(5.0)
        continue

    elif "open github" in user or "github" in user:
        speak("opening github profile for your coding projects")
        webbrowser.open("https://www.github.com")
        time.sleep(5.0)
        continue

    elif "open chatgpt" in user or "chat gpt" in user:
        speak("opening chat gpt website for you")
        webbrowser.open("https://chatgpt.com")
        time.sleep(5.0)
        continue

    # 3. காலேஜ் சப்ஜெக்ட் ஸ்பெஷல் கமெண்ட்ஸ்
    elif "college" in user or "where i am studying" in user:
        speak("You are studying at Sacred Heart College in Tirupattur, doing your B Sc in Artificial Intelligence and Machine Learning.")

    elif "rdbms" in user or "database" in user:
        speak("RDBMS stands for Relational Database Management System. It stores data in tables and uses SQL queries like SELECT, INSERT, and UPDATE to manage data.")

    elif "django" in user or "flask" in user:
        speak("Django and Flask are popular Python web frameworks. Flask is lightweight and micro, while Django is a full stack framework used for building secure web applications.")
        
    # 4. சிஸ்டம் கமெண்ட்ஸ்
    elif "time" in user:
        current = datetime.datetime.now().strftime("%H:%M")
        speak(f"current time is {current}")
        
    elif "bye" in user or "exit" in user:
        speak("bye, take care da")
        break
        
    # -----------------------------------------------------------------
    # B. DYNAMIC HYBRID AI MODE (மற்ற எல்லா கேள்விகளுக்கும் ChatGPT Style)
    # -----------------------------------------------------------------
    else:
        try:
            print("Thinking with OpenAI Brain...")
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user + " (answer in one short sentence)"}
                ]
            )
            bot_reply = completion.choices[0].message.content
            bot_reply = bot_reply.replace('"', '').replace("'", "").replace("\n", " ")
            speak(bot_reply)
            
        except Exception as e:
            print("OpenAI quota limited. Switching to Backup AI Brain smoothly...")
            bot_reply_backup = ask_backup_ai(user)
            bot_reply_backup = bot_reply_backup.replace('"', '').replace("'", "").replace("\n", " ").replace("*", "")
            speak(bot_reply_backup)
            
        print("Waiting for next command...")
        time.sleep(1.5) 

    
        