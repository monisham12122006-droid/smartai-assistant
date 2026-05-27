import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import sounddevice as sd
import io
import wave

# playsound-ஐ சேஃபா லோட் பண்றோம்
try:
    import playsound
except ImportError:
    os.system('pip install playsound==1.2.2')
    import playsound

# --- 1. GOOGLE TEXT-TO-SPEECH (gTTS) ---
def speak(text):
    print("bot: " + text)  # ஆன்சரை பிரிண்ட் பண்ணும்
    
    try:
        filename = "reply.mp3"
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        pass

# --- 2. NO PYAUDIO MICROPHONE CAPTURE ---
def take_command():
    r = sr.Recognizer()
    fs = 16000  # Sample rate
    seconds = 6  # நீங்க நிதானமா பேச 5 செகண்ட் டைம் இருக்கும்

    print("\nListening...")
    try:
        # PyAudio-க்கு பதிலா sounddevice வச்சு சேஃபா ஆடியோ ரெக்கார்ட் பண்றோம்
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  
        print("Recognizing...")

        # ரெக்கார்ட் ஆன ஆடியோவை ஸ்பீச் ரெகக்னிஷன் ஃபார்மேட்டுக்கு மாத்துறோம்
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(myrecording.tobytes())
        
        wav_io.seek(0)
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)

        query = r.recognize_google(audio, language='en-in')
        print(f"you: {query}")
        return query.lower()
        
    except Exception as e:
        return "none"

# --- 3. MAIN PROGRAM START ---
print("SMART AI ASSISTANT STARTED")
speak("Smart A I Assistant Started")

while True:
    user = take_command()
    
    if user == "none":
        continue

    # பாட் கண்டிஷன்ஸ் 
    if "hi" in user:
        speak("hello da")
        
    elif "how are you" in user:
        speak("i am fine")
        
    elif "saptiya" in user:
        speak("sapthan")
        
    elif "what is my name" in user or "who i am" in user:
        speak("your name is monisha")
        
    elif "what is ai" in user:
        speak("ai means artificial intelligence")
        
    elif "what is python" in user:
        speak("python is a high-level programming language")
        
    elif "motivation" in user:
        speak("hard work never fails")
        
    elif "what is your name" in user:
        speak("my name is smartai")
        
    elif "what is ml" in user:
        speak("algorithm based problems")
        
    elif "favorite colour" in user:
        speak("my favorite colour is sky blue")
        
    elif "what is operator" in user:
        speak("operator means used to perform operation on values or variables")
        
    elif "types of operators" in user:
        speak("arithmetic operators, comparison operators, logical operators")
        
    elif "time" in user:
        current = datetime.datetime.now().strftime("%H:%M")
        speak(f"current time is {current}")
        
    elif "date" in user:
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        speak(f"today's date is {today}")
        
    elif "bye" in user:
        speak("bye, take care")
        break
        
    else:
        speak("not understand")