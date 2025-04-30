#Version 1 MAX
import time
import pygame as audio
import speech_recognition as sr
import pyttsx3
import datetime
from groq import Groq
import threading

Max = pyttsx3.init()
Max.setProperty('rate', 130)

recognizer = sr.Recognizer()

chime_path = "/Users/aayanbhatia/Downloads/chime.mp3"
audio.mixer.init()
audio.mixer.music.load(chime_path)

def play_chime():
    audio.mixer.music.play()
    while audio.mixer.music.get_busy():
        time.sleep(1)

# AI API KEY 
client = Groq(api_key="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")

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def play_alarm():
    alarm_path = "/Users/aayanbhatia/Downloads/alarm.mp3"
    audio.mixer.music.load(alarm_path)
    audio.mixer.music.play()
    while audio.mixer.music.get_busy():
        time.sleep(1)

def set_alarm(alarm_time):
    print(f"set_alarm called with: {alarm_time}")  # Debugging statement
    while True:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"Current time: {current_time}")  # Debugging statement
        if current_time == alarm_time:
            play_alarm()
            Max.say("wake up dude you told me to wake you up")
            Max.runAndWait()
            break
        time.sleep(1)  # Check every second
def day():
    now = datetime.datetime.now()
    return now.strftime("%A")

while True:
    with sr.Microphone() as source:
        print("Waiting for User Input...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        if text.lower() == "hey max":
            play_chime()
            with sr.Microphone() as source:
                audio_data = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio_data)
            if user_input.lower() == "what time is it":
                current_time = get_current_time()
                Max.say(f"The current time is {current_time}")
                Max.runAndWait()
            if user_input.lower() == "time":
                current_time = get_current_time()
                Max.say(f"The current time is {current_time}")
                Max.runAndWait()
            if user_input.lower() == "tell me the time":
                current_time = get_current_time()
                Max.say(f"The current time is {current_time}")
                Max.runAndWait()
            if user_input.lower() == "what day is it":
                Max.say(f"Today is {day()}")
                Max.runAndWait()
            elif user_input.lower() == "wake me up":
                Max.say("What time would you like to set the alarm for?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                alarm_time = recognizer.recognize_google(audio_data)
                
                Max.say("Is that AM or PM?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                am_pm = recognizer.recognize_google(audio_data).lower()

                if am_pm in ["morning", "am"]:
                    am_pm = "AM"
                elif am_pm in ["night", "pm"]:
                    am_pm = "PM"

                if am_pm not in ["AM", "PM"]:
                    Max.say("Sorry, I didn't catch that. Please say AM or PM.")
                    Max.runAndWait()
            elif user_input.lower() == "set an alarm":
                Max.say("What time would you like to set the alarm for?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                alarm_time = recognizer.recognize_google(audio_data)
                
                Max.say("Is that AM or PM?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                am_pm = recognizer.recognize_google(audio_data).lower()

                if am_pm in ["morning", "am"]:
                    am_pm = "AM"
                elif am_pm in ["night", "pm"]:
                    am_pm = "PM"

                if am_pm not in ["AM", "PM"]:
                    Max.say("Sorry, I didn't catch that. Please say AM or PM.")
                    Max.runAndWait()
                else:
                    # makes it so that it has a colon, so max can recognize time.
                    if ":" not in alarm_time:
                        alarm_time = f"{alarm_time[:len(alarm_time)-2]}:{alarm_time[len(alarm_time)-2:]}"
                    # alaem time here makes it in hh:mm format
                    alarm_time_parts = alarm_time.split(":")
                    if len(alarm_time_parts[0]) == 1:
                        alarm_time_parts[0] = f"0{alarm_time_parts[0]}"
                    alarm_time = f"{alarm_time_parts[0]}:{alarm_time_parts[1]} {am_pm}"
                    Max.say(f"Setting alarm for {alarm_time}")
                    Max.runAndWait()
                    print(f"Alarm set for: {alarm_time}")  # Debugging statement
                    alarm_thread = threading.Thread(target=set_alarm, args=(alarm_time,))
                    alarm_thread.start()
            elif user_input.lower() == "hi":
                Max.say("yo")
                Max.runAndWait()
            elif user_input.lower() == "bye":
                Max.say("adios")
                Max.runAndWait()
            if user_input.lower() == "stop":
                print("user said to stop...")
            if user_input.lower() == "shut down":
                Max.say("Shutting Down.")
                Max.runAndWait()
                break
            else:
                Max.say("sorry, can you say that again?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                question = recognizer.recognize_google(audio_data)
                response_stream = client.chat.completions.create(
                    model="gemma2-9b-it",
                    messages=[{"role": "user", "content": question}],
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=True,
                    stop=None
                )
                response_text = ""
                for response in response_stream:
                    if response.choices[0].delta.content:
                        response_text += response.choices[0].delta.content
                Max.say(response_text)
                Max.runAndWait()

    except sr.UnknownValueError:
        print("Max: I didn't catch that.")
    except sr.RequestError as e:
        Max.say("I'm having trouble with my speech recognition service. Please try again later.")
        Max.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")
