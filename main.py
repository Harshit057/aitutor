import spacy
import json
import random

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the content (knowledge base)
try:
    with open("data/content.json") as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    print("Error: content.json file not found. Please ensure the file is in the 'data' directory.")
    knowledge_base = {}
    exit()

# Quiz questions dictionary
quiz_questions = {
    "What is 2 + 2?": "4",
    "What is the capital of France?": "Paris",
    "Who wrote 'Hamlet'?": "Shakespeare",
    "What is the largest planet in our solar system?": "Jupiter"
}

def start_quiz():
    """Conducts a quiz with the user."""
    score = 0
    questions = list(quiz_questions.items())
    random.shuffle(questions)

    print("\nLet's start the quiz! Answer the following questions:\n")
    for question, answer in questions:
        user_answer = input(f"{question} ")
        if user_answer.strip().lower() == answer.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is {answer}.")
    print(f"\nQuiz finished! Your score: {score}/{len(questions)}\n")

# Welcome message
print("Welcome to AI Virtual Tutor!")

while True:
    user_input = input("You: ").strip()
    
    # Exit condition
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Process the user's input with spaCy NLP model
    doc = nlp(user_input)
    print(f"Bot: {doc.text}")

    # Ask the user for the subject they want to learn
    subject = input("\nWhich subject do you want to learn? ").strip()
    if not subject:
        print("Bot: Please enter a valid subject.")
        continue

    # Normalize the subject case and fetch information
    subject_info = knowledge_base.get(subject.capitalize(), "Sorry, I don't know about that topic.")
    print(f"Bot: {subject_info}")

    # Ask if the user wants to take a quiz
    while True:
        quiz_option = input("\nWould you like to take a quiz? (yes/no) ").strip().lower()
        if quiz_option == "yes":
            start_quiz()
            break
        elif quiz_option == "no":
            print("Bot: Alright, let's continue learning.")
            break
        else:
            print("Bot: Please answer with 'yes' or 'no'.")
