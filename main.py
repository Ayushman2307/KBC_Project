import time
import json
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Function to read text aloud (Text-to-Speech)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the player's voice and recognize the answer
def listen_for_answer():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your answer...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(audio).lower()
            print(f"Player said: {answer}")
            return answer
        except sr.UnknownValueError:
            print("Sorry, I did not understand your answer.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

# Load questions from the JSON file
def load_questions_from_json(file_path):
    """Load questions and options from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['questions']
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

# Function to update the GUI with the current question and options
def update_question_label(question, options):
    question_label.config(text=question)
    option_a_button.config(text=f"a. {options[0]}")
    option_b_button.config(text=f"b. {options[1]}")
    option_c_button.config(text=f"c. {options[2]}")
    option_d_button.config(text=f"d. {options[3]}")
    speak(question)
    speak("Choose your answer by saying a, b, c, or d")

# Function to handle user input (voice or button click)
def handle_answer(selected_option, question, correct_answer, current_level):
    global last_correct_amount, current_question_index
    # Compare the selected option with the correct answer
    if selected_option == correct_answer:
        result_label.config(text="Correct Answer!", fg="green")
        speak("Correct Answer!")
        last_correct_amount = current_level  # Save the last correct amount
        speak(f"You have won Rs. {last_correct_amount}")  # Announce the amount
        time.sleep(1)
        current_question_index += 1  # Move to the next question
        next_question()
    else:
        result_label.config(text="Wrong Answer!", fg="red")
        speak("Wrong Answer!")
        speak(f"You have won Rs. {last_correct_amount}")  # Announce the last correct amount
        time.sleep(1)
        game_over()

# Function for when a player selects an option using voice
def voice_input():
    answer = listen_for_answer()
    if answer:
        options = ["a", "b", "c", "d"]
        if answer in options:
            correct_answer = questions[current_question_index]['answer']  # The correct answer ('a', 'b', 'c', or 'd')
            current_level = levels[current_question_index]
            handle_answer(answer, questions[current_question_index]['question'], correct_answer, current_level)
        else:
            print("Please choose a valid option: a, b, c, or d")
            speak("Please choose a valid option: a, b, c, or d")
            voice_input()

# Function for when a player clicks on a button
def button_input(selected_option):
    correct_answer = questions[current_question_index]['answer']  # The correct answer ('a', 'b', 'c', or 'd')
    current_level = levels[current_question_index]
    handle_answer(selected_option, questions[current_question_index]['question'], correct_answer, current_level)

# Function for the next question
def next_question():
    global current_question_index, questions
    if current_question_index < len(questions):
        question = questions[current_question_index]
        update_question_label(question['question'], question['options'])
    else:
        messagebox.showinfo("Game Over", f"Congratulations! You've completed the quiz! You won Rs. {last_correct_amount}")
        window.quit()

# Function to handle game over and display final winnings
def game_over():
    messagebox.showinfo("Game Over", f"You have won Rs. {last_correct_amount}")
    window.quit()

# Create the GUI window
window = tk.Tk()
window.title("KBC Quiz")

# Initialize the current question index
current_question_index = 0
last_correct_amount = 0

# Load the questions
questions = load_questions_from_json('questions.json')

# Define levels for money
levels = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1250000, 2500000, 5000000, 10000000, 50000000, 70000000]

# Create and pack GUI elements
question_label = tk.Label(window, text="", font=("Helvetica", 14), wraplength=400)
question_label.pack(pady=20)

option_a_button = tk.Button(window, text="a. Option A", font=("Helvetica", 12), command=lambda: button_input('a'))
option_a_button.pack(fill="both", pady=5)

option_b_button = tk.Button(window, text="b. Option B", font=("Helvetica", 12), command=lambda: button_input('b'))
option_b_button.pack(fill="both", pady=5)

option_c_button = tk.Button(window, text="c. Option C", font=("Helvetica", 12), command=lambda: button_input('c'))
option_c_button.pack(fill="both", pady=5)

option_d_button = tk.Button(window, text="d. Option D", font=("Helvetica", 12), command=lambda: button_input('d'))
option_d_button.pack(fill="both", pady=5)

result_label = tk.Label(window, text="", font=("Helvetica", 14), fg="black")
result_label.pack(pady=20)

# Start the quiz with the first question
next_question()

# Add voice input button
voice_button = tk.Button(window, text="Speak Your Answer", font=("Helvetica", 12), command=voice_input)
voice_button.pack(pady=10)

# Run the GUI main loop
window.mainloop();
