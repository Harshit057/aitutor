from transformers import pipeline

# Initialize the question-answering pipeline
question_answerer = pipeline("question-answering")

# Define a context and question
context = """
Hugging Face is a company that provides machine learning tools and models for NLP tasks.
They are well known for their work on transformers and pre-trained models, which allow users
to quickly apply state-of-the-art deep learning models to natural language processing problems.
"""

question = "What does Hugging Face provide?"

# Get the answer from the model
answer = question_answerer(question=question, context=context)

# Print the answer
print(answer)
