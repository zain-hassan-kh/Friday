import os
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import pyjokes
import random
import requests
import json

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    if "Zira" in voice.name: 
        engine.setProperty('voice', voice.id)
        break

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Wishing the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 6 and hour < 12:
        speak("Good Morning!")
        print("Good Morning!")
    elif hour >= 12 and hour < 15:
        speak("Good Afternoon!")
        print("Good Afternoon!")
    else:
        speak("Good Evening!")
        print("Good Evening!")

    speak("Hi, I am Friday. I am your virtual assistant. Please tell me, how may I help you?")
    print("Hi, I am Friday. I am your virtual assistant. Please tell me, how may I help you?")

# Taking user commands
def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.75
        audio = r.listen(source, timeout = None, phrase_time_limit = 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='eng-GB, eng-US, eng-IN')
        print(f"You said: {query}\n")

    except Exception as e:
        print(e)
        print("Say that again, please...")
        return "None"
    
    return query

# Calculator function where operator is taken first, followed by numbers
def Calculator():
    try:
        # Manual input for the operator
        speak("Please enter the operator. You can type add, subtract, multiply, or divide.")
        operator = input("Enter the operator: ").lower()

        if "add" in operator:
            operator = '+'
        elif "subtract" in operator:
            operator = '-'
        elif "multiply" in operator:
            operator = '*'
        elif "divide" in operator:
            operator = '/'
        else:
            speak("Invalid operator. Please try again.")
            return

        # Manual input for the first number
        speak("Please enter the first number.")
        num1 = int(input("Enter the first number: "))  # Take integer input from user

        # Manual input for the second number
        speak("Please enter the second number.")
        num2 = int(input("Enter the second number: "))  # Take integer input from user

        # Perform the calculation based on the operator
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                speak("Division by zero is not allowed.")
                return

        # Display and speak the result
        speak(f"The result is {result}")
        print(f"Result: {result}")

    except ValueError:
        speak("Please enter valid numbers.")
        print("Invalid input, please enter numeric values.")
    except Exception as e:
        speak("There was an error. Please try again.")
        print(e)

# Function to fetch the latest news
def get_latest_news():
    api_key = "your-api-key-here"
    url = "your-url-here"
    
    try:
        response = requests.get(url)
        news_data = response.json() # json is a method to convert the response into a dictionary format

        if news_data['status'] == 'ok':
            print("Here are the latest news headlines:\n")
            for article in news_data['articles'][:5]:
                print(f"- {article['title']}")
                speak(article['title'])
        else:
            print("Could not fetch the news. Please try again later.")
    except Exception as e:
        print("An error occurred:", e)

# Function to fetch weather updates
def get_weather(city_name):
    api_key = "your-api-key-here"
    base_url = "base-url-here"

    params = {
        "access_key": api_key,
        "query": city_name
    }

    try:
        response = requests.get(base_url, params = params)
        data = response.json()

        if "current" in data:
            temperature = data["current"]["temperature"]
            weather_description = data["current"]["weather_descriptions"][0] 
            humidity = data["current"]["humidity"]
            wind_speed = data["current"]["wind_speed"]

            weather_report = (
                f"The current weather in {city_name} is {weather_description}. "
                f"The temperature is {temperature}°C, with a humidity level of {humidity}% "
                f"and wind speed of {wind_speed} km/h."
            )

            print(weather_report)
            speak(weather_report)
        else:
            error_message = data.get("error", {}).get("info", "Unable to fetch weather data.")
            print(error_message)
            speak(f"Sorry, I couldn't fetch the weather for {city_name}. {error_message}")

    except Exception as e:
        speak("There was an error fetching the weather data.")
        print(f"An error occurred: {e}")

# Main function to execute the assistant's features
def main():
    wishMe()
    while True:
        query = TakeCommand().lower() 
          
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Opening YouTube. Please wait...")
            webbrowser.open("youtube.com")
        
        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("google.com")

        elif 'play music' in query:
            speak("Playing music. Please wait...")
            music_dir = 'assets\\audio'
            songs = os.listdir(music_dir)
            random_song = random.choice(songs)
            print(f"Playing: {random_song}")
            os.startfile(os.path.join(music_dir, random_song))

        elif 'open spotify' in query:
            speak("Opening Spotify. Please wait...")
            os.system("start spotify:")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H hour %M minute %S seconds")
            speak(f"The time is {strTime}")
            print(f"The time is {strTime}")

        elif 'calculator' in query:
            speak("Opening Calculator. Please wait...")
            Calculator()

        elif 'the news' in query:
            speak("Getting the latest news...")
            get_latest_news()
        
        elif 'the weather' in query:
            speak("Please tell me the city name.")
            city_name = TakeCommand().lower()
            get_weather(city_name)

        elif 'about you' in query:
            speak("I am Friday! I am your friend.")
        
        elif 'how are you' in query:
            speak("I am good. Thank you for asking.")
            speak("Tell me about you.")
        
        elif 'joke' in query:
           joke = pyjokes.get_joke('en','neutral')
           print(joke)
           speak(joke)

        elif 'open image' in query:
            path = r'assets\\images'
            random_image = random.choice(os.listdir(path))
            print(f"Opening image: {random_image}")
            os.startfile(os.path.join(path, random_image))

        elif 'thank you' in query:
            speak("My pleasure!")
        
        elif 'quit' in query:
            speak("Okay! See you soon.")
            print("Okay! See you soon.")
            print("Exiting the program...")
            exit()

main()