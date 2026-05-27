# main.py
import pyttsx3
import datetime
engine = pyttsx3.init()

bot = "Welcome to Smart AI Assistant"
print(bot)
engine.say(bot)
engine.runAndWait()

print("SMART AI ASSISTANT STARTED")
name="moni"

while True:
    
    user=input("you:").lower()

    if "hi" in user:
       print("bot:hello da")
    elif "how are you" in user:
       print("bot:i am fine")   
    elif "saptiya" in user:
       print("bot:sapthan")
    elif "what is my name" in user:
       print("bot:your name is monisha")
    elif "what is ai" in user:
       print("bot:ai means artificial intelligence") 
    elif "what is python" in user:
       print("bot:python is a high-level programming language")
    elif "motivation" in user:
       print("bot:hard work never fails")
    elif "who i am?" in user:
       print("bot:you are monisha") 
    elif "what is your name" in user:
       print("bot:my name is smartai")
    elif "what is ml" in user:
       print("bot:algorithm based problems")
    elif "what is your favorite  colour" in user:
       print("bot:my favorite colour is sky blue")
    elif "what is operator" in user:
       print("bot:operator means used to perform operation on values or variables in programming")   
    elif "types of operators" in user:
       print("bot:arithmetic operators,comparison operators,logical operators,assignment operators")
    elif "time" in user:
       current = datetime.datetime.now().strftime("%H:%M")
       print("bot: current time is", current) 
    elif "date" in user:
       today = datetime.datetime.now().strftime("%d-%m-%Y")
       print("bot: today's date is", today)  
    elif "bye" in user:
       print("bot:bye,take care") 

    else:
       print("bot:not understand") 

     