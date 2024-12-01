from flask import Flask, render_template, request
import spacy
import json
import pyttsx3
import threading
import random

# Initialize spaCy and pyttsx3
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

# Load the content (knowledge base) from the JSON file
try:
    with open("data/content.json") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    print("Error: content.json file not found. Please ensure the file is in the 'data' directory.")
    knowledge_base = {}
    exit()

# Quiz questions
quiz_questions = {
    "What is 2 + 2?": "4",
    "What is the capital of France?": "Paris",
    "Who wrote 'Hamlet'?": "Shakespeare",
    "What is the largest planet in our solar system?": "Jupiter"
}

app = Flask(__name__)
quiz_in_progress = False
quiz_iterator = iter([])  # To handle quiz questions dynamically
score = 0

# Function for the bot to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Start Flask routes
@app.route("/", methods=["GET", "POST"])
def home():
    global quiz_in_progress, quiz_iterator, score
    response = ""
    if request.method == "POST":
        try:
            # Get user input from the form
            user_input = request.form["user_input"]
            print(f"User Input: {user_input}")  # Debugging line to check input

            # NLP processing using spaCy
            doc = nlp(user_input)
            print(f"Processed text: {doc.text}")  # Debugging line to check NLP processing

            if quiz_in_progress:
                # Handle quiz answers
                try:
                    question, correct_answer = next(quiz_iterator)
                    if user_input.lower() == correct_answer.lower():
                        response = "Correct!"
                        score += 1
                    else:
                        response = f"Wrong! The correct answer is {correct_answer}."
                except StopIteration:
                    quiz_in_progress = False
                    response = f"Quiz finished! Your score: {score}/{len(quiz_questions)}"
                    score = 0
            else:
                # Handle regular conversation
                user_input_lower = user_input.lower()
                if "quiz" in user_input_lower:
                    quiz_in_progress = True
                    quiz_iterator = iter(quiz_questions.items())
                    response = "Starting the quiz! Here's your first question:"
                    question, _ = next(quiz_iterator)
                    response += f" {question}"
                elif user_input_lower in knowledge_base:
                    response = knowledge_base[user_input_lower]
                else:
                    response = "I'm not sure about that topic."

            # Speak the response
            speak(response)

        except Exception as e:
            print(f"Error processing the request: {e}")
            response = "Sorry, I encountered an error. Please try again."

    return render_template("index.html", bot_response=response)

if __name__ == "__main__":
    app.run(debug=True)
