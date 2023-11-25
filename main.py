# Import the os library to check if the model path is valid:
import os

# Import libraries for the GUI:
import tkinter as tk
import customtkinter

# Import the Llama model from the Llama library:
from llama_cpp import Llama

# Import the random library to generate a random seed for the model:
import random

# Import the datetime library to get the current date:
import datetime

# Import the text to speech library/engine:
import pyttsx3

# Import the speech recognition library/engine:
import speech_recognition

# Global variable - Path to model, change this to the path of your model:
model_path = "llama-2-7b-chat.Q5_K_M.gguf"

# Version of the application:
version = "2.0"

# Get the current date:
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

# This will list the microphone names on your system - You can use this to set the device_index in the speech recognition function below:
print(speech_recognition.Microphone.list_microphone_names())

"""TEXT TO SPEECH ENGINE:"""

# Speech to text object creation:
engine = pyttsx3.init()

"""RATE"""

# Getting details of current speaking rate:
rate = engine.getProperty('rate')

# Setting up new voice rate:
engine.setProperty('rate', 150)

"""VOLUME"""

# Getting to know current volume level (min=0 and max=1):
volume = engine.getProperty('volume')

# setting up volume level  between 0 and 1:
engine.setProperty('volume', 1.0)

"""VOICE"""

# getting details of current voice:
voices = engine.getProperty('voices')

# Changing index, changes voices - 1 for female, 0 for male:
engine.setProperty('voice', voices[1].id)

"""END TEXT TO SPEECH ENGINE."""

"""CUSTOM TKINTER INITIAL SETTINGS:"""

# Modes: system (default), light, dark:
customtkinter.set_appearance_mode("System")

# Themes: blue (default), dark-blue, green:
customtkinter.set_default_color_theme("blue")

"""END CUSTOM TKINTER INITIAL SETTINGS."""

# Create a function to load the model:


def load_model():

    # Check if the model path is valid:
    if not os.path.isfile(model_path):
        print("Error: The model path is invalid. Check the path in the main.py file.")
        print("And, make sure the model is in the same folder as the main.py file.")

        # If the model path is invalid, exit the program:
        exit()

    # If the model path is valid, load the model:
    global model
    model = Llama(model_path=model_path, seed=random.randint(1, 2**31))

# Create a function to generate a response to the user's input:


def generate_response(model, input_tokens, prompt_input_text):

    text_area_display = app.textbox_frame.textbox

    # Display the input text in the text area on top:

    text_area_display.insert(
        tk.INSERT, "\n\nUser: " + prompt_input_text + "\n")

    output_response_text = b""
    count = 0
    output_response_text = b"\n\nLadybot: "
    text_area_display.insert(tk.INSERT, output_response_text)

    """GENERATE RESPONSE:"""

    # Create a variable for the response text:
    response = ""

    for token in model.generate(input_tokens, top_k=40, top_p=0.95, temp=0.72, repeat_penalty=1.1):

        # Extract the response text from the output of the model which is in token format and convert it to a string:
        response_text = model.detokenize([token])
        output_response_text = response_text.decode('utf-8', 'ignore')

        # Display the response text in the text area on top:
        text_area_display.insert(tk.INSERT, output_response_text)
        app.update_idletasks()
        count += 1
        if count > 200 or (token == model.token_eos()):
            break

        # Add the response text to the response variable:
        response += output_response_text

        # Clear the input to let the user know the response from the model is complete:
        app.user_textbox_frame.textbox.delete('1.0', 'end')

    """END GENERATE RESPONSE."""

    # Run the text to speech engine to speak the response:
    engine.say(response)
    engine.runAndWait()
    engine.stop()

# Create a function to send a message to the model and display a response:


def send_message():

    # Get the user input from the User Textbox Frame class and store it in a variable:
    user_prompt_input_text = app.user_textbox_frame.textbox.get(
        "1.0", "end-1c")

    # Delete any leading or trailing spaces from the user input:
    user_prompt_input_text = user_prompt_input_text.strip()

    # Encode the message with uft-8:
    byte_message = user_prompt_input_text.encode('utf-8')

    # Can change the prompt format for the LLM:
    # Experiment with to see what works best for the application.
    input_tokens = model.tokenize(
        b"### User: " + byte_message + b"\n### Ladybot: ")

    # Print out the input tokens to the console for debugging purposes and for information on how it works:
    print("Input tokens: ", input_tokens)

    # Call the generate_response function to generate a response:
    generate_response(model, input_tokens, user_prompt_input_text)

# Create a function for the speech recognition:


def start_speech_recognition():

    # Create a variable for the recognizer:
    recognizer = speech_recognition.Recognizer()

    # Create a variable for the microphone:
    mic = speech_recognition.Microphone(device_index=1)

    # Create a loop to keep the speech recognition running:
    while True:
        with mic as source:
            engine.say("I am listening...")
            engine.runAndWait()
            engine.stop()
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)

        engine.say("Processing...")
        engine.runAndWait()
        engine.stop()

        try:
            user_input = recognizer.recognize_google(audio)

            if user_input.lower() == "goodbye":
                engine.say("It was nice chatting with you. Goodbye.")
                engine.runAndWait()
                engine.stop()
                exit()

        except Exception as e:
            print("ERROR: {}".format(e))

        prompt = user_input

        # Delete any leading or trailing spaces from the user input:
        prompt.strip()

        # Encode the message with uft-8:
        byte_message = prompt.encode('utf-8')

        # Can change the prompt format for the LLM:
        # Experiment with to see what works best for the application.
        input_tokens = model.tokenize(
            b"### User: " + byte_message + b"\n### Ladybot: ")

        # Print out the input tokens to the console for debugging purposes and for information on how it works:
        print("Input tokens: ", input_tokens)

        # Call the generate_response function to generate a response:
        generate_response(model, input_tokens, prompt)

# Create classes that inherit from customtkinter.CTkFrame:


class TextboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Add widgets onto the frame:

        # Create scrollable textbox:
        self.textbox = customtkinter.CTkTextbox(
            self, border_width=1, border_color="blue", width=960, height=400, corner_radius=10, activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew", columnspan=1)

        # Create CTk scrollbar:
        self.scrollbar = customtkinter.CTkScrollbar(
            self, command=self.textbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Connect textbox scroll event to CTk scrollbar:
        self.textbox.configure(yscrollcommand=self.scrollbar.set)


class UserTextboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Add widgets onto the frame:

        # Create scrollable textbox:
        self.textbox = customtkinter.CTkTextbox(
            self, border_width=1, border_color="blue", width=960, height=200, corner_radius=10, activate_scrollbars=False)
        self.textbox.grid(row=0, column=0, sticky="nsew", columnspan=1)

        # Create CTk scrollbar:
        self.scrollbar = customtkinter.CTkScrollbar(
            self, command=self.textbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Connect textbox scroll event to CTk scrollbar:
        self.textbox.configure(yscrollcommand=self.scrollbar.set)

# Create a class that inherits from customtkinter.CTk:


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ladybot" + " - " + version + " - " + todays_date)

        self.geometry("1000x700")

        # Configure the grid system:
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Add frames with a textbox to the window:
        self.textbox_frame = TextboxFrame(self)
        self.textbox_frame.grid(row=0, column=0, padx=10,
                                pady=(10, 0), sticky="nsew", columnspan=3)

        self.user_textbox_frame = UserTextboxFrame(self)
        self.user_textbox_frame.grid(row=1, column=0, padx=10,
                                     pady=(10, 0), sticky="nsew", columnspan=3)

        # Add buttons to the bottom of the window:
        self.button_1 = customtkinter.CTkButton(
            self, text="Start Speech Recognition", command=start_speech_recognition)
        self.button_1.grid(row=2, column=0, padx=20,
                           pady=20, sticky="ew", columnspan=1)

        self.button_2 = customtkinter.CTkButton(
            self, text="Send Message", command=send_message)
        self.button_2.grid(row=2, column=1, padx=20,
                           pady=20, sticky="ew", columnspan=1)

        self.button_3 = customtkinter.CTkButton(
            self, text="Exit", command=self.destroy)
        self.button_3.grid(row=2, column=2, padx=20,
                           pady=20, sticky="ew", columnspan=1)

# Main function to start the application:


def main():

    # Load model when the application starts:
    load_model()

    engine.say("Hello, I am Ladybot. Let's chat.")
    engine.runAndWait()
    engine.stop()

    # Starts the application:
    global app
    app = App()
    app.mainloop()

# Application starts here:


if __name__ == "__main__":
    # Call our main function to start the application:
    main()

"""Links:"""

# https://pyttsx3.readthedocs.io/en/latest/
# https://github.com/nateshmbhat/pyttsx3
# https://pypi.org/project/SpeechRecognition/
# https://github.com/TomSchimansky/CustomTkinter
# https://customtkinter.tomschimansky.com/documentation/
