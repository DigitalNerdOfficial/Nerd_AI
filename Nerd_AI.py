#Modules:
import pyttsx3
import speech_recognition as sr
import os
import datetime
import time
import webbrowser
import googletrans
import wikipedia
import requests
from requests.exceptions import RequestException
import bs4

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
def text_input(): return input("Enter Your Command Here: ").lower()

# Function to get voice input
def voice_input():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            alternatives = recognizer.recognize_google(audio, show_all=True)
            if alternatives and 'alternative' in alternatives:
                command = alternatives['alternative'][0]['transcript'].lower()
                print(f"User said: {command}")
                if not command.strip(): print("Sorry, you did not say anything. Please try again.")
                else: return command
        except sr.UnknownValueError: print("Sorry, I couldn't understand what you said. Please try again.")
        except sr.RequestError as e: print(f"Error with the speech recognition service; {e}")

# Function to set the input type
def set_input_type(input_type):
    global get_input
    if input_type == "text input":
        get_input = text_input
        print("Input type set to 'text_input'")
    elif input_type == "voice input":
        get_input = voice_input
        print("Input type set to 'voice_input'")
    else: print("Invalid input type. Keeping the default 'text_input'")

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
    if 3 <= hour < 12: greeting = "Good Morning"
    elif 12 <= hour < 15: greeting = "Good Afternoon"
    elif 15 <= hour < 20: greeting = "Good Evening"
    else: greeting = "Hello"
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
            perform_wikipedia_search(command)
            return
        else:
            speak_and_print("Invalid choice. Using Google as the default search engine.")
            search_url = f"https://www.google.com/search?q={command}"
        webbrowser.open(search_url)
    except RequestException as e:
        print(f"Network Error: {e}")
        speak_and_print("Sorry, there was a network error. Please check your internet connection and try again.")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak("Sorry, an unexpected error occurred.")


# Function to perform language translation:
def perform_translation(command):
    try:
        if "available languages" in command:
            available_languages = ", ".join(googletrans.LANGUAGES.values())
            speak_and_print(f"Available languages are: {available_languages}")
            return
        speak_and_print('Translating...')
        command = command.replace("translate", "").strip()
        print("Please enter the target language. For example, 'es' for Spanish.")
        speak("Please enter the target language.")
        target_lang = input("Enter the target language: ")
        if target_lang in googletrans.LANGUAGES:
            translated_text = translator.translate(command, dest=target_lang).text
            print(f"Translated text: {translated_text}")
            speak_and_print("If the text appears unclear, please consider copying and pasting it into another location to ensure clarity.")
        else:
            speak_and_print("Invalid language code. Please enter a valid language code from available languages.")
            speak_and_print("You can also say 'available languages' to see the list of available languages.")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak_and_print("Sorry, an unexpected error occurred.")

# Function to get weather information using web scraping
def get_weather_without_api(city):
    try:
        base_url = f'https://www.weather-forecast.com/locations/{city}/forecasts/latest'
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            weather_info = soup.find('span', {'class': 'phrase'}).text
            speak_and_print(f"The current weather in {city} is: {weather_info}")
        else:
            speak_and_print(f"Sorry, I couldn't find weather information for {city}. Please check the city name.")
    except RequestException as e:
        print(f"Network Error: {e}")
        speak_and_print("Sorry, there was a network error. Please check your internet connection and try again.")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred while fetching weather information: {e}")
        speak_and_print("Sorry, I couldn't fetch the weather information at the moment.")

# Function to show news updates from BBC News
def show_news_updates(limit=5):
    try:
        speak_and_print("Fetching the latest news updates...")
        speak_and_print(f"The latest news headlines are:")
        bbc_news_url = 'https://www.bbc.com/news'
        response = requests.get(bbc_news_url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')
            for index, headline in enumerate(headlines, start=1):
                if limit is not None and index > limit:
                    break
                news_text = headline.get_text().strip()
                speak_and_print(f"News {index}: {news_text}")
        else:
            speak_and_print("Sorry, unable to fetch the latest news at the moment.")
    except RequestException as e:
        print(f"Network Error: {e}")
        speak_and_print("Sorry, there was a network error. Please check your internet connection and try again.")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak_and_print("Sorry, there was an error fetching the latest news updates.")

# Function To Open Applications:
def open_application(application_name):
    browsers = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "brave": "brave.exe",
        "opera": "opera.exe",
        "firefox": "firefox.exe",
    }
    other_applications = {
        "cmd": "start cmd",
        "explorer": "explorer",
        "control panel": "control",
        "notepad": "notepad",
        "calculator": "calc",
        "calendar": "start outlookcal:",
        "mail": "start outlookmail:",
        "microsoft store": "start ms-windows-store:",
        "settings": "start ms-settings:",
        "player": "mediaplayer",
    }
    application_name_lower = application_name.lower()
    try:
        if application_name_lower in browsers:
            speak_and_print(f"Opening {application_name}...")
            os.startfile(browsers[application_name_lower])
        elif application_name_lower in other_applications:
            speak_and_print(f"Opening {application_name}...")
            os.system(other_applications[application_name_lower])
        else: raise ValueError(f"Application not found: {application_name}")
    except Exception as e:
        print(f"Sorry, an unexpected error occurred: {e}")
        speak("Sorry, an unexpected error occurred.")

def tell_joke():
    try:
        joke_api_url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data.get('type') == 'twopart':
                joke_setup = joke_data.get('setup', '')
                joke_punchline = joke_data.get('delivery', '')
                if joke_setup and joke_punchline:
                    speak_and_print("Here's a joke for you:")
                    speak_and_print(joke_setup)
                    speak_and_print(joke_punchline)
                    speak_and_print("ha ha ha")
                else: speak_and_print("I'm sorry, but I couldn't fetch a joke at the moment.")
            else:
                joke_text = joke_data.get('joke', '')
                if joke_text:
                    speak_and_print("Here's a joke for you:")
                    speak_and_print(joke_text)
                    speak_and_print("ha ha ha")
                else: speak_and_print("I'm sorry, but I couldn't fetch a joke at the moment.")
        else: speak_and_print("I'm sorry, but I couldn't fetch a joke at the moment.")
    except RequestException as e:
        print(f"Network Error: {e}")
        speak_and_print("Sorry, there was a network error. Please check your internet connection and try again.")
    except Exception as e:
        print(f"An error occurred while fetching a joke: {e}")
        speak_and_print("I'm sorry, but I couldn't fetch a joke at the moment.")

def tell_trivia():
    try:
        from html import unescape
        import random
        trivia_api_url = "https://opentdb.com/api.php?amount=1&type=multiple"
        response = requests.get(trivia_api_url)
        if response.status_code != 200:
            speak_and_print("I'm sorry, but I couldn't fetch trivia at the moment.")
            return
        trivia_data = response.json()
        question, correct_answer, incorrect_answers = [unescape(trivia_data['results'][0].get(key, '')) for key in ['question', 'correct_answer', 'incorrect_answers']]
        if question and correct_answer and len(incorrect_answers) >= 3:
            selected_incorrect_answers = random.sample(incorrect_answers, 3)
            all_answers = [correct_answer] + selected_incorrect_answers
            random.shuffle(all_answers)
            speak_and_print("Here's a trivia question:")
            speak_and_print(question)
            speak_and_print("Options:")
            [speak_and_print(f"{i}. {unescape(answer)}") for i, answer in enumerate(all_answers, start=1)]
            while True:
                user_answer = input("Enter your answer (1/2/3/4): ")
                speak("Enter your answer")
                if user_answer.isdigit() and 1 <= int(user_answer) <= len(all_answers):
                    user_selected_answer = all_answers[int(user_answer) - 1]
                    speak_and_print("Congratulations! You got it right." if user_selected_answer == correct_answer else f"Sorry, the correct answer is: {correct_answer}")
                    break
                else: speak_and_print("Invalid response. Please choose a valid option.")
        else: speak_and_print("I'm sorry, but I couldn't fetch trivia at the moment.")
    except RequestException as e:
        print(f"Network Error: {e}")
        speak_and_print("Sorry, there was a network error. Please check your internet connection and try again.")
    except Exception as e:
        print(f"An error occurred while fetching trivia: {e}")
        speak_and_print("I'm sorry, but I couldn't fetch trivia at the moment.")

# Function to perform math calculations
def perform_math_calculation(command):
    try:
        expression = command.replace("calculate", "").strip()
        result = eval(expression)
        print(f"Result of {expression} is: {result}")
        speak(f"The result of the calculation is: {result}")
    except Exception as e:
        print(f"Sorry, an error occurred during the calculation: {e}")
        speak("Sorry, an error occurred during the calculation.")

# Function to handle system actions (shutdown or restart)
def handle_system_action(action):
    confirmation_message = f"Are you sure you want to shutdown/restart your computer? (yes/no): "
    command = f"shutdown /{action} /t 5"
    confirm_response = input(confirmation_message).lower()
    if confirm_response == "yes":
        speak_and_print(f"Your computer will shutdown/restart within a few seconds.")
        speak_and_print("Goodbye! Have a great day!")
        os.system(command)
    else: speak_and_print(f"User cancelled the shutdown/restart.")

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
        elif "search" in command: perform_web_search(command)

        #Command To Display Weather:
        elif "weather" in command:
            city = input("Enter the city name: ")
            get_weather_without_api(city)

        # Command to show news updates
        elif "news" in command: show_news_updates()

        # Command to perform language translation:
        elif "translate" in command: perform_translation(command)
        elif "available languages" in command: perform_translation(command)

        # Command To Open Applications:
        elif "open" in command:
            application_name = command.replace("open", "").strip()
            open_application(application_name)

        # Command To Perform Math Calculations:
        elif "calculate" in command:
            perform_math_calculation(command)

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
        elif command in ["hi","hello"]: speak_and_print("Hello! How can I assist you today?")
        elif command in ["thanks","thank you"]: speak_and_print("You're welcome! If you have any more questions or if there's anything else I can help you with, feel free to ask. Happy computing!")
        elif "joke" in command: tell_joke()
        elif "trivia" in command: tell_trivia()

        # Command to review command history
        elif "history" in command:
            print("Command History:")
            for i, cmd in enumerate(command_history, start=1):
                print(f"{i}. {cmd}")
            speak("Command History has been displayed.")

        # Command To Shutdown The Computer:
        elif "shutdown" in command:
            handle_system_action("s")
        # Command To Restart The Computer:
        elif "restart" in command:
            handle_system_action("r")

        # Command To Close The Chat or Application
        elif command in ["exit", "close", "quit"]:
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").lower()
            if confirm_exit == "yes":
                speak_and_print("Goodbye! Have a great day!")
                exit()
            else:
                speak_and_print("Okay, I'll continue to assist you.")

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
