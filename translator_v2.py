import pyttsx3
import speech_recognition as sr
from googletrans import Translator, LANGUAGES

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

# Function for text-to-speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function for speech-to-text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (speak now)")
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language='en-US')  # English input
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results, check your internet connection.")
            return None
        except sr.WaitTimeoutError:
            print("Timeout occurred. Please try again.")
            return None

# Function to display available languages
def show_languages():
    print("\nAvailable Languages:")
    for code, name in LANGUAGES.items():
        print(f"{name.capitalize()} ({code})")

# Main translator function
def multi_language_translator():
    translator = Translator()
    print("Multi-Language Translator with Speech-to-Text and Text-to-Speech")
    print("Type 'exit' to quit the program.")
    
    while True:
        # Show language options
        show_languages()
        
        # Get the target language from the user
        target_lang = input("\nEnter the language code for the target language (e.g., 'hi' for Hindi): ").strip().lower()
        if target_lang == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break
        if target_lang not in LANGUAGES:
            print("Invalid language code. Please try again.")
            continue
        
        print("\nWould you like to speak or type your input? (say/type): ", end="")
        input_mode = input().strip().lower()
        
        if input_mode == "say":
            english_text = listen()
            if not english_text:
                continue  # Skip if input is invalid
        elif input_mode == "type":
            english_text = input("\nEnter text in English: ")
        else:
            print("Invalid option. Please choose 'say' or 'type'.")
            continue
        
        # Exit condition
        if english_text and english_text.lower() == "exit":
            print("Goodbye!")
            speak("Goodbye!")
            break

        try:
            # Translate the input to the chosen language
            translation = translator.translate(english_text, src='en', dest=target_lang)
            translated_text = translation.text
            print(f"Translation in {LANGUAGES[target_lang].capitalize()}: {translated_text}")
            speak(translated_text)  # Speak the translated text
        except Exception as e:
            print("Error while translating:", e)

# Run the translator
if __name__ == "__main__":
    multi_language_translator()
