import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Sir: {query}\nBun To: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Correct method and model
            messages=[
                {"role": "system", "content": "You are an assistant named Bun To."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        say(reply)
        chatStr += f"{reply}\n"
        return reply
    except Exception as e:
        print(f"Error during chat completion: {e}")
        say("Sorry, I couldn't process your request.")
        return "Error in generating response."

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        reply = response["choices"][0]["message"]["content"]
        text += reply

        # Ensure the "Openai" directory exists
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        
        # Create a valid filename
        filename = prompt[:20].replace(" ", "_").replace("/", "_") + ".txt"
        with open(f"Openai/{filename}", "w") as f:
            f.write(text)
        say("Response saved successfully.")
    except Exception as e:
        print(f"Error during AI response: {e}")
        say("Sorry, I couldn't save the AI response.")

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return "Listening timed out."
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return "I didn't catch that."
        except Exception as e:
            print(f"Error: {e}")
            return "Some error occurred. Sorry from Bun To."

if __name__ == '__main__':
    print('Welcome to Bun To A.I')
    say("Namaste Sir, Bantu A.I me aapka swagat hai. How can I assist you, sir?")
    while True:
        query = takeCommand()
        if query.strip() == "":
            continue
        
        # Predefined commands
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
            ["my website", "https://www.harshchaudhary.com.np"]
        ]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break
        
        # Open music
        if "open music" in query.lower():
            musicPath = "/Users/harshchaudhary/Downloads/jhalle.mp3"
            if os.path.exists(musicPath):
                os.system(f"open {musicPath}")
                say("Playing your music.")
            else:
                say("Music file not found.")
        
        # Tell time
        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        # Open specific applications
        elif "open facetime" in query.lower():
            os.system("open /System/Applications/FaceTime.app")
            say("Opening FaceTime.")

        elif "your name" in query.lower():
            say("Sir, mero naam Bantu ho.")

        elif "Who is techy guy" in query.lower():
            say("Sir, he has made me.")

        elif "made" in query.lower():
            say("Sir, Techy Guy has made me. He is a Nepali Programmer, YouTuber, and content creator.")

        elif "what can you do" in query.lower():
            say("Sir, I can do everything Techy Guy has programmed me to do.")
        
        elif "open pass" in query.lower():
            os.system("open /Applications/Passky.app")
            say("Opening Passky.")
        
        # Use AI for a specific prompt
        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        # Quit the assistant
        elif "stop your system" in query.lower():
            say("Goodbye Sir. Have a great day!")
            exit()
        
        # Reset chat history
        elif "reset chat" in query.lower():
            chatStr = ""
            say("Chat history reset.")
        
        # Default: Chat
        else:
            print("Chatting...")
            chat(query)
