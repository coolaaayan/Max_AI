import os
import time
import random
import threading
import pygame as audio
import speech_recognition as sr
import pyttsx3
import datetime
from groq import Groq
from adafruit_servokit import ServoKit

# === setup ===
kit = ServoKit(channels=16)
Max = pyttsx3.init()
Max.setProperty('rate', 130)
recognizer = sr.Recognizer()

client = Groq(api_key="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")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chime_path = os.path.join(BASE_DIR, "sounds", "chime.mp3")
alarm_path = os.path.join(BASE_DIR, "sounds", "alarm.mp3")

audio.mixer.init()

# === states ===
last_interaction = time.time()

# === hand functions ===
def open_hand():
    kit.servo[0].angle = 180
    for i in range(1, 5):
        kit.servo[i].angle = 0

def close_hand():
    kit.servo[0].angle = 0
    for i in range(1, 5):
        kit.servo[i].angle = 180

def wave_hand():
    for _ in range(2):
        open_hand()
        time.sleep(0.3)
        close_hand()
        time.sleep(0.3)

def thumbs_up():
    kit.servo[0].angle = 180
    for i in range(1, 5):
        kit.servo[i].angle = 180

def peace():
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    kit.servo[2].angle = 0
    kit.servo[3].angle = 180
    kit.servo[4].angle = 180

def shrug():
    open_hand()
    time.sleep(0.1)
    close_hand()
    time.sleep(0.1)

def random_fidget():
    i = random.randint(0, 4)
    kit.servo[i].angle = random.choice([0, 180])

# === sounds ===
def play_sound(path):
    audio.mixer.music.load(path)
    audio.mixer.music.play()
    while audio.mixer.music.get_busy():
        time.sleep(1)

def play_chime():
    play_sound(chime_path)

def play_alarm():
    play_sound(alarm_path)

# === clock ===
def get_current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def day():
    return datetime.datetime.now().strftime("%A")

# === alarm logic ===
def set_alarm(alarm_time):
    while True:
        if datetime.datetime.now().strftime("%I:%M %p") == alarm_time:
            play_alarm()
            open_hand()
            wave_hand()
            Max.say("wake up buddy. rise and shine.")
            Max.runAndWait()
            close_hand()
            break
        time.sleep(1)

# === idle fidget loop ===
def idle_brain():
    global last_interaction
    while True:
        idle = time.time() - last_interaction
        if idle > 90:
            if random.random() < 0.3:
                random_fidget()
        if idle > 300:
            Max.say("yo... you still alive?")
            shrug()
            Max.runAndWait()
        time.sleep(30)

threading.Thread(target=idle_brain, daemon=True).start()

# === main loop ===
while True:
    with sr.Microphone() as source:
        print("⏳ listening...")
        try:
            audio_data = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            continue

    try:
        text = recognizer.recognize_google(audio_data).lower()
        last_interaction = time.time()

        if "hey max" in text:
            play_chime()
            with sr.Microphone() as source:
                audio_data = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio_data).lower()
            last_interaction = time.time()

            if "time" in user_input:
                Max.say(f"it’s {get_current_time()}")
                Max.runAndWait()
                wave_hand()

            elif "day" in user_input:
                Max.say(f"today is {day()}")
                Max.runAndWait()
                shrug()

            elif "set alarm" in user_input or "wake me up" in user_input:
                Max.say("what time you want me to wake you?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                alarm_time = recognizer.recognize_google(audio_data)

                Max.say("a.m. or p.m.?")
                Max.runAndWait()
                with sr.Microphone() as source:
                    audio_data = recognizer.listen(source)
                am_pm = recognizer.recognize_google(audio_data).lower()
                am_pm = "AM" if "am" in am_pm else "PM" if "pm" in am_pm else None

                if not am_pm:
                    Max.say("yo... that ain’t valid. say a.m. or p.m.")
                    Max.runAndWait()
                    continue

                if ":" not in alarm_time:
                    alarm_time = f"{alarm_time[:-2]}:{alarm_time[-2:]}"
                h, m = alarm_time.split(":")
                alarm_time = f"{h.zfill(2)}:{m} {am_pm}"

                Max.say(f"alarm locked for {alarm_time}")
                Max.runAndWait()
                threading.Thread(target=set_alarm, args=(alarm_time,)).start()

            else:
                # ask groq
                response_stream = client.chat.completions.create(
                    model="gemma2-9b-it",
                    messages=[{"role": "user", "content": user_input}],
                    max_completion_tokens=1024,
                    top_p=1,
                    stream=True
                )
                reply = ""
                for r in response_stream:
                    if r.choices[0].delta.content:
                        reply += r.choices[0].delta.content

                Max.say(reply)
                Max.runAndWait()

                # react to content
                if "thank" in user_input:
                    thumbs_up()
                elif "funny" in reply or "haha" in reply:
                    wave_hand()
                elif "don't know" in reply or "sorry" in reply:
                    shrug()

    except sr.UnknownValueError:
        print("Max didn’t catch that.")
    except Exception as e:
        print(f"Error: {e}")
