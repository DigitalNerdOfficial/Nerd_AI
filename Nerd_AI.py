#Modules:
import os
import datetime

#Functions:
# Function To Wish The User:
def wishtheuser():
    hour = int(datetime.datetime.now().hour)
    if hour>=3 and hour<12:
        print("Good Morning")
    elif hour>=12 and hour<15:
        print("Good Afternoon")
    elif hour>=15 and hour<20:
        print("Good Evening")
    print("How Can I Assist You Today?")

if __name__ == "__main__":
    wishtheuser()
    while True:
        command=input("Enter Your Command Here: ")
        command=command.lower()
        #Commands:

        #Command To Open Browsers:
        if "open chrome" in command:
            os.startfile("chrome.exe")
            print("Opening Chrome...")
        elif "open microsoft edge" in command:
            os.startfile("msedge.exe")
            print("Opening Microsoft Edge...")
        elif "open brave" in command:
            os.startfile("brave.exe")
            print("Opening Brave...")
        elif "open opera" in command:
            os.startfile("opera.exe")
            print("Opening Opera...")
        elif "open mozilla firefox" in command:
            os.startfile("firefox.exe")
            print("Opening Mozilla Firefox...")

        #Command To Open Applications:
        elif "open file explorer" in command:
            os.startfile("explorer.exe")
            print("Opening File Explorer...")

        #Simple Chats:
        elif "hello" in command:
            print("Hello! How can I assist you today?")
        elif "hi" in command:
            print("Hello! How can I assist you today?")
        elif "thank" in command:
            print("You're welcome! If you have any more questions or if there's anything else I can help you with, feel free to ask. Happy computing!")

        #Command To Close The Chat or Application
        elif "exit" or "close" or "quit" in command:
            exit()