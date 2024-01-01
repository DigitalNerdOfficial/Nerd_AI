#Modules:
import os
import datetime
import time
import pyttsx3
import webbrowser
import googletrans
import wikipedia
import speech_recognition as sr

# Voice Configuration
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

# Command history list
command_history = []

# Translator
translator = googletrans.Translator()

# Function to type the input command
def text_input():
    return input("Enter Your Command Here: ").lower()

# Function to get voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        alternatives = recognizer.recognize_google(audio, show_all=True).get('alternative', [])
        if alternatives:
            command = alternatives[0]['transcript'].lower()
            print(f"User said: {command}")
            return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return ""

# Function to set the input type
def set_input_type(input_type):
    global get_input
    if input_type == "text input":
        get_input = text_input
        print("Input type set to 'text_input'")
    elif input_type == "voice input":
        get_input = voice_input
        print("Input type set to 'voice_input'")
    else:
        print("Invalid input type. Keeping the default 'text_input'")

# Default input type is text_input
get_input = text_input

# Function To Make The AI Speak:
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function To Make The AI Speak And Print:
def speak_and_print(text):
    print(text)
    speak(text)

# Function To Wish The User:
def wish_the_user():
    hour = int(datetime.datetime.now().hour)
    if 3 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 15:
        greeting = "Good Afternoon"
    elif 15 <= hour < 20:
        greeting = "Good Evening"
    else:
        greeting = "Hello"
    
    speak_and_print(greeting + ". How can I assist you today?")

# Command To Perform Wikipedia Search:
def perform_wikipedia_search(command):
    try:
        speak_and_print('Searching In Wikipedia...')
        results = wikipedia.summary(command, sentences=4)
        speak_and_print(f"According to Wikipedia:")
        speak_and_print(results)
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e}")
        speak(f"Sorry, I found multiple results. Please specify your query.")
    except wikipedia.exceptions.PageError as e:
        print(f"PageError: {e}")
        speak(f"Sorry, I couldn't find any information on that topic.")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak("Sorry, an unexpected error occurred.")

# Command To Perform Web Search:
def perform_web_search(command):
    try:
        speak_and_print('Searching...')
        command = command.replace("search", "").strip()
        # Provide options for different search engines
        print("1. Google")
        print("2. Bing")
        print("3. Yahoo")
        print("4. Wikipedia")
        speak("Choose a search engine")
        choice = input("Choose a search engine (1/2/3/4): ")
        if choice == "1":
            speak_and_print("Searching In Google")
            search_url = f"https://www.google.com/search?q={command}"
        elif choice == "2":
            speak_and_print("Searching In Bing")
            search_url = f"https://www.bing.com/search?q={command}"
        elif choice == "3":
            speak_and_print("Searching In Yahoo")
            search_url = f"https://search.yahoo.com/search?p={command}"
        elif choice == "4":
            # Use the perform_wikipedia_search function directly
            perform_wikipedia_search(command)
            return  # No need to open the web browser for Wikipedia
        else:
            speak_and_print("Invalid choice. Using Google as the default search engine.")
            search_url = f"https://www.google.com/search?q={command}"
        # Open the default web browser and display search results
        webbrowser.open(search_url)
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak("Sorry, an unexpected error occurred.")

# Function To Perform Language Translation:
def perform_translation(command):
    try:
        speak_and_print('Translating...')
        command = command.replace("translate", "").strip()
        # Detect the source language
        source_lang = translator.detect(command).lang
        # Prompt the user to choose the target language
        target_lang = input("Enter the target language (e.g., 'es' for Spanish): ")
        # Translate the command
        translated_text = translator.translate(command, src=source_lang, dest=target_lang).text
        print(f"Translated text: {translated_text}")
        speak_and_print("If the text appears unclear, please consider copying and pasting it into another location to ensure clarity.")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak("Sorry, an unexpected error occurred.")

#Function To Perform Tasks:
def tasks():
    while True:
        time.sleep(1)
        command = get_input()

        # Add the command to the history
        command_history.append(command)

        # Command to switch between "text input" and "voice input"
        if "text input" in command:
            set_input_type("text input")
            continue
        elif "voice input" in command:
            set_input_type("voice input")
            continue

        #Command To Perform Web Search:
        if "search" in command:
            perform_web_search(command)

        # Command to perform language translation:
        elif "translate" in command:
            perform_translation(command)

        #Command To Open Browsers:
        elif "open chrome" in command:
            speak_and_print("Opening Chrome...")
            os.startfile("chrome.exe")
        elif command in ["open microsoft edge","open edge"]:
            speak_and_print("Opening Microsoft Edge...")
            os.startfile("msedge.exe")
        elif "open brave" in command:
            speak_and_print("Opening Brave...")
            os.startfile("brave.exe")
        elif "open opera" in command:
            speak_and_print("Opening Opera...")
            os.startfile("opera.exe")
        elif command in ["open mozilla firefox","open firefox"]:
            speak_and_print("Opening Mozilla Firefox...")
            os.startfile("firefox.exe")

        #Command To Open Applications:
        elif "open cmd" in command:
            speak_and_print("Opening Command Prompt...")
            os.system("start cmd")
        elif command in ["open file explorer","open explorer"]:
            speak_and_print("Opening File Explorer...")
            os.system("explorer")
        elif "open control panel" in command:
            speak_and_print("Opening Control Panel...")
            os.system("control")
        elif "open notepad" in command:
            speak_and_print("Opening Notepad...")
            os.system("notepad")
        elif "open calculator" in command:
            speak_and_print("Opening Calculator...")
            os.system("calc")
        elif "open calendar" in command:
            speak_and_print("Opening Calendar...")
            os.system("start outlookcal:")
        elif "open mail" in command:
            speak_and_print("Opening Mail...")
            os.system("start outlookmail:")
        elif "open microsoft store" in command:
            speak_and_print("Opening Microsoft Store...")
            os.system("start ms-windows-store:")
        elif "open settings" in command:
            speak_and_print("Opening Settings...")
            os.system("start ms-settings:")
        elif command in ["open music player","open video player","open media player"]:
            speak_and_print("Opening Default Media/Music Application...")
            os.system("mediaplayer")

        # Command To Display The Time;and Date,Day:
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M")
            print(f"The current time is: "+ current_time)
            speak(f"The current time is, "+ current_time)
        elif command in ["date","day"]:
            current_date = datetime.datetime.now().date()
            current_day = datetime.datetime.now().strftime("%A")
            print(f"Current date is : {current_date}"+f" and Day is : {current_day}")
            speak(f"Current date is {current_date}"+f" and day is {current_day}")

        #Simple Chats:
        elif command in ["hi","hello"]:
            speak_and_print("Hello! How can I assist you today?")
        elif command in ["thanks","thank you"]:
            speak_and_print("You're welcome! If you have any more questions or if there's anything else I can help you with, feel free to ask. Happy computing!")

        # Command to review command history
        elif "history" in command:
            print("Command History:")
            for i, cmd in enumerate(command_history, start=1):
                print(f"{i}. {cmd}")
            speak("Command History has been displayed.")

        # Command To Close The Chat or Application
        elif command in ["exit", "close", "quit"]:
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm_exit == "yes":
                speak_and_print("Goodbye! Have a great day!")
                exit()
            else:
                speak_and_print("Okay, I'll continue to assist you.")

        # Command To ShutDown/Restart The Computer:
        elif "shutdown" in command:
            confirm_shutdown = input("Are you sure you want to shutdown your computer? (yes/no): ").lower()
            if confirm_shutdown == "yes":
                speak_and_print("Your computer will Shutdown within few seconds")
                speak_and_print("Goodbye! Have a great day!")
                os.system("shutdown /s /t 5")
            else:
                speak_and_print("User cancelled the shutdown.")
        elif "restart" in command:
            confirm_restart = input("Are you sure you want to restart your computer? (yes/no): ").lower()
            if confirm_restart == "yes":
                speak_and_print("Your computer will restart within few seconds")
                speak_and_print("Goodbye! Have a great day!")
                os.system("shutdown /s /t 5")
            else:
                speak_and_print("User cancelled the restart.")

        #If The Command doesn't correspond to any recognizable words or queries.
        else:
            print(f"It seems like your input '{command}' doesn't correspond to any recognizable words or queries.")
            print("Please read the Documentation to know the full information about this AI, and its features. ")
            print("Documentation will be available sooner")
            speak(f"It seems like your input doesn't correspond to any recognizable words or queries. "
                "For detailed information about this AI and its features, please refer to the Documentation. "
                "Documentation will be available soon.")

if __name__ == "__main__":
    wish_the_user()
    tasks()
