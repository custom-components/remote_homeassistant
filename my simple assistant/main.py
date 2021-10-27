import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pyjokes
import smtplib
from email.message import EmailMessage
import pyautogui

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[1].id)

email_id = 'kumarraunak077@gmail.com'
pswd = os.environ.get('password')
email = EmailMessage()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak("Good Morning!")
    elif hour >=12 and hour < 17:
        speak("Good Afternoon!")
    elif hour >=17 and hour < 20:
        speak("Good Evening!")
    else:
        speak("Good Night!")
    speak("I'm your virtual Desktop Assistant. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hi! I'm listening to you.")
        speak("Hi! I'm listening to you.")
        r.pause_threshold = 2
        audio = r.listen(source)
    try:
        print("I'm recognizing your voice.")
        query = r.recognize_google(audio, language='en')
        print(f"You said: {query}\n")
    except Exception as e:
        error = "Sorry the following error occurred:"+str(e)
        print(error)
        speak("Sorry an unexpected error occurred. Say that again please...")
        return "Nothing"
    return query

def takeEmailDescriptions():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 2
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en')
    except Exception as e:
        error = "Sorry the following error occurred:"+str(e)
        #print(error)
        speak("Sorry an unexpected error occurred. Say that again please...")
        return "Nothing"
    return query

def openApp(location, name):
    os.startfile(location)
    speak(f"Opening {name} for you sir")

def openWebsite(url, name):
    webbrowser.open_new(url)
    speak(f"Opening {name} for you sir")

def openChromeHistory():
    pyautogui.moveTo(953,1055, duration=2)
    pyautogui.click()
    pyautogui.moveTo(1891,60, duration=2)
    pyautogui.click()
    pyautogui.moveTo(1885,210, duration=2)
    pyautogui.click()
    pyautogui.moveTo(1500,210, duration=2)
    pyautogui.moveTo(1500,285, duration=2)
    pyautogui.click()
    speak("The last closed tabs of Chrome are restored for you, Raunak")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("As per Wikipedia")
            speak(results)
        elif 'open youtube' in query:
            openWebsite("https://www.youtube.com", "Youtube")
        elif 'open google' in query:
            openWebsite("https://www.google.com", "Google")
        elif 'open stackoverflow' in query:
            openWebsite("https://www.stackoverflow.com", "Stackoverflow")
        elif 'open github' in query:
            openWebsite("https://www.github.com", "Github")
        elif 'open repl' in query:
            openWebsite("https://www.replit.com", "Replit")
        elif 'open repl' in query:
            openWebsite("https://www.drive.google.com", "Drive")
        elif 'open mail' in query:
            openWebsite("https://www.gmail.com", "Gmail")
        elif 'open discord' in query:
            openWebsite("https://www.discord.com", "Replit")
        elif 'open mattrab' in query:
            openWebsite("https://www.askmattrab.com", "Mattrab")
        elif "the time" in query:
            currentTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {currentTime}")
        elif "open code" in query:
            openApp(r"D:\Installed apps\VS Code\Microsoft VS Code\Code.exe", "V.S. Code")
        elif "open python" in query:
            openApp(r"C:\Program Files\Python39\python.exe", "Python IDE")
        elif "open atom" in query:
            openApp(r"C:\ProgramData\Dell\atom\app-1.57.0\atom.exe", "Atom Editor")
        elif "open indesign" in query:
            openApp(r"C:\Program Files\Adobe\Adobe InDesign 2021\InDesign.exe", "Adobe Indesign")
        elif "open chrome history" in query:
            openChromeHistory()
        elif "open file" in query:
            openApp(r"C:\Windows\explorer.exe", "File Explorer")
        elif "tell jokes" in query:
            joke = pyjokes.get_joke()
            speak(joke)
        elif "send email" in query:
            speak("Whom do you want to mail?")
            to = takeEmailDescriptions().lower()
            speak(f"Sending email to {to}")
            print(f"Sending email to {to}")
            speak("What is the Subject of your email ?")
            subject = takeEmailDescriptions().lower()
            print(f"Subject: {subject}")
            speak("What do you want to say ?")
            content = takeEmailDescriptions().lower()
            print(f"Mail Content: {content}")
            email['From'] = email_id
            email['To'] = f'{to}@gmail.com'
            email['Subject'] = subject
            email.set_content(content)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_id ,pswd)
                smtp.send_message(email)
                speak("Your email is sent Sir!!")
