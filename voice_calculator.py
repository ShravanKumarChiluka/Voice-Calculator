import speech_recognition as sr
import pyttsx3
import re
import math

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(f"You said: {said}")
            return said.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("Sorry, I could not understand. Could you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")
            speak("Sorry, there was an error with the speech recognition service.")

    return ""

def parse_expression(text):
    # Replace spoken words with mathematical symbols and functions
    text = text.replace('plus', '+')
    text = text.replace('minus', '-')
    text = text.replace('multiply by', '*')
    text = text.replace('multiplied by', '*')
    text = text.replace('times', '*')
    text = text.replace('divided by', '/')
    text = text.replace('divide by', '/')
    text = text.replace('over', '/')
    text = text.replace('into', '*')
    text = text.replace('open brace', '(')
    text = text.replace('close brace', ')')

    # Handle square root separately
    text = re.sub(r'square root of (\d+)', r'math.sqrt(\1)', text)
    
    # Add trigonometric and logarithmic functions
    text = text.replace('sin', 'math.sin')
    text = text.replace('cos', 'math.cos')
    text = text.replace('tan', 'math.tan')
    text = text.replace('log', 'math.log')
    text = text.replace('log base 10', 'math.log10')

    # Remove any non math characters
    expression = re.findall(r'[\d\.]+|[\+\-\*\/\(\)]|math\.\w+\(\d+\)', text)
    return ''.join(expression)

def calculate():
    print("Welcome to the Voice Calculator. Please speak your mathematical expression.")
    speak("Welcome to the Voice Calculator. Please speak your mathematical expression.")
    

    while True:
        text = get_audio()
        if text == "":
            continue
        if "exit" in text or "quit" in text or "stop" in text:
            speak("Goodbye!")
            print("Goodbye!")
            break

        expression = parse_expression(text)
        print(f"Evaluating: {expression}")

        try:
            result = eval(expression)
            print(f"Result: {result}")
            speak(f"The result is {result}")
        except Exception as e:
            print("Sorry, there was an error in calculating the result.")
            speak("Sorry, there was an error in calculating the result.")

if __name__ == "__main__":
    calculate()
