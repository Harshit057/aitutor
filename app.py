from flask import Flask, render_template, request, jsonify, session
import json
import pyttsx3
import threading
import random
import os
import re
import math
from datetime import datetime, timedelta
from config import Config

# Initialize NLP (optional)
nlp = None
try:
    import spacy
    nlp = spacy.load(Config.SPACY_MODEL)
except (ImportError, IOError):
    print("spaCy not available. Using advanced keyword matching.")
    nlp = None

try:
    engine = pyttsx3.init()
    if Config.TTS_ENABLED and engine:
        engine.setProperty('rate', Config.TTS_RATE)
        engine.setProperty('volume', Config.TTS_VOLUME)
except RuntimeError:
    print("Text-to-speech engine not available")
    engine = None

# Load the enhanced knowledge base
try:
    with open(Config.KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        subjects = data.get('subjects', {})
        quiz_database = data.get('quiz_database', {})
        conversation_patterns = data.get('conversation_patterns', {})
        common_sense_knowledge = data.get('common_sense_knowledge', {})
        math_operations = data.get('math_operations', {})
        casual_conversation = data.get('casual_conversation', {})
except FileNotFoundError:
    print(f"Error: {Config.KNOWLEDGE_BASE_FILE} file not found. Using minimal data.")
    subjects = {}
    quiz_database = {}
    conversation_patterns = {}
    common_sense_knowledge = {}
    math_operations = {}
    casual_conversation = {}
except UnicodeDecodeError:
    print("Encoding error in knowledge base file. Using minimal data.")
    subjects = {}
    quiz_database = {}
    conversation_patterns = {}
    common_sense_knowledge = {}
    math_operations = {}
    casual_conversation = {}

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(seconds=Config.PERMANENT_SESSION_LIFETIME)

# Function for the bot to speak
def speak(text):
    if engine:
        try:
            # Clean text for speech
            clean_text = re.sub(r'[^\w\s.,!?]', '', text)
            engine.say(clean_text)
            engine.runAndWait()
        except:
            pass  # If speech fails, continue silently

class AIAssistant:
    def __init__(self):
        self.subjects = subjects
        self.quiz_db = quiz_database
        self.patterns = conversation_patterns
        self.common_sense = common_sense_knowledge
        self.math_ops = math_operations
        self.casual_conv = casual_conversation
        self.conversation_history = []
        self.user_context = {}
    
    def calculate_math(self, expression):
        """Safely evaluate mathematical expressions"""
        try:
            # Clean the expression - only allow numbers, operators, and basic functions
            clean_expr = re.sub(r'[^0-9+\-*/().,\s]', '', expression)
            
            # Handle basic word problems
            if 'plus' in expression.lower():
                clean_expr = clean_expr.replace('plus', '+')
            if 'minus' in expression.lower():
                clean_expr = clean_expr.replace('minus', '-')
            if 'times' in expression.lower():
                clean_expr = clean_expr.replace('times', '*')
            if 'divided by' in expression.lower():
                clean_expr = clean_expr.replace('divided by', '/')
            
            # Use eval safely for basic arithmetic
            if clean_expr and all(c in '0123456789+-*/().,\s' for c in clean_expr):
                result = eval(clean_expr)
                return f"The answer is: **{result}**\n\nCalculation: {clean_expr} = {result}"
            
            return None
        except:
            return None
    
    def handle_math_query(self, user_input):
        """Handle mathematical questions and calculations"""
        user_lower = user_input.lower()
        
        # Check for calculation requests
        math_patterns = [
            r'what is ([\d+\-*/().\s]+)',
            r'calculate ([\d+\-*/().\s]+)',
            r'solve ([\d+\-*/().\s]+)',
            r'([\d+\-*/().\s]+) equals?',
            r'([\d+\-*/().\s]+) =',
        ]
        
        for pattern in math_patterns:
            match = re.search(pattern, user_lower)
            if match:
                expression = match.group(1)
                result = self.calculate_math(expression)
                if result:
                    return result
        
        # Handle word problems
        if any(word in user_lower for word in ['cost', 'buy', 'spend', 'total', 'sum']):
            # Extract numbers from word problems
            numbers = re.findall(r'\d+\.?\d*', user_input)
            if len(numbers) >= 2:
                try:
                    if 'cost' in user_lower and ('buy' in user_lower or 'purchase' in user_lower):
                        cost = float(numbers[0])
                        quantity = float(numbers[1])
                        total = cost * quantity
                        return f"If each item costs ${cost} and you buy {quantity} items, the total cost is: **${total}**"
                except:
                    pass
        
        # Math concept explanations
        math_concepts = {
            'addition': 'Addition means combining numbers to get a larger number. For example: 3 + 4 = 7',
            'subtraction': 'Subtraction means taking away one number from another. For example: 7 - 3 = 4',
            'multiplication': 'Multiplication is repeated addition. For example: 3 × 4 = 12 (adding 3 four times)',
            'division': 'Division means splitting a number into equal parts. For example: 12 ÷ 3 = 4',
            'percentage': 'A percentage is a fraction out of 100. For example: 50% = 50/100 = 0.5',
            'fraction': 'A fraction represents part of a whole. For example: 1/2 means one part out of two equal parts',
        }
        
        for concept, explanation in math_concepts.items():
            if concept in user_lower:
                return f"**{concept.title()}**: {explanation}\n\nWould you like me to solve a {concept} problem for you?"
        
        return None
    
    def handle_common_sense(self, user_input):
        """Handle common sense questions and reasoning"""
        user_lower = user_input.lower()
        
        # Basic facts
        if 'hours in a day' in user_lower or 'hours in day' in user_lower:
            return "There are **24 hours** in a day. This comes from the time it takes Earth to rotate once on its axis."
        
        if 'days in a week' in user_lower or 'days in week' in user_lower:
            return "There are **7 days** in a week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday."
        
        if 'months in a year' in user_lower or 'months in year' in user_lower:
            return "There are **12 months** in a year: January through December. A year is based on Earth's orbit around the Sun."
        
        # Weather and nature
        if any(word in user_lower for word in ['rain', 'wet', 'water']):
            return "Rain is water falling from clouds. It makes things wet and is essential for plants and life on Earth! ☔"
        
        if 'sun' in user_lower and ('hot' in user_lower or 'warm' in user_lower):
            return "The Sun provides heat and light to Earth. It's a star that's about 93 million miles away from us! ☀️"
        
        # Simple cause and effect
        if 'why' in user_lower:
            if 'fall down' in user_lower or 'things fall' in user_lower:
                return "Things fall down because of **gravity**! Gravity is a force that pulls objects toward the Earth's center."
            
            if 'need sleep' in user_lower:
                return "We need sleep to rest our brains and bodies. During sleep, our brain processes memories and our body repairs itself."
            
            if 'need water' in user_lower:
                return "Water is essential for life! Our bodies are about 60% water, and we need it for almost every bodily function."
        
        # Comparisons
        if 'bigger' in user_lower or 'larger' in user_lower:
            if 'elephant' in user_lower and 'mouse' in user_lower:
                return "Elephants are much larger than mice! An elephant can weigh up to 6 tons, while a mouse weighs only a few ounces."
        
        # Animal facts
        animals = {
            'dog': 'Dogs bark to communicate! They are loyal companions and have an excellent sense of smell.',
            'cat': 'Cats meow mainly to communicate with humans. They are independent and great hunters.',
            'bird': 'Most birds can fly using their wings and hollow bones that make them lightweight.',
            'fish': 'Fish breathe underwater using gills and use fins to swim through water.'
        }
        
        for animal, fact in animals.items():
            if animal in user_lower:
                return f"🐾 **{animal.title()} fact**: {fact}"
        
        return None
    
    def handle_casual_conversation(self, user_input):
        """Handle casual, friendly conversation"""
        user_lower = user_input.lower()
        
        # Greetings
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greeting in user_lower for greeting in greetings):
            return random.choice(self.casual_conv.get('greetings', ['Hello! How can I help you today?']))
        
        # How are you questions
        if any(phrase in user_lower for phrase in ['how are you', 'how do you feel', 'how is everything']):
            responses = [
                "I'm doing great! I love helping people learn new things. How are you doing?",
                "I'm wonderful! Every conversation teaches me something new. What's on your mind today?",
                "I'm doing well, thank you for asking! I'm always excited to help with learning. How about you?",
                "I'm fantastic! Ready to explore some interesting topics together. How are you feeling today?"
            ]
            return random.choice(responses)
        
        # Personal questions about the AI
        if any(phrase in user_lower for phrase in ['who are you', 'what are you', 'tell me about yourself']):
            return "I'm your AI tutor! 🤖 I'm here to help you learn about various subjects, answer questions, solve math problems, and have friendly conversations. I love helping people discover new knowledge!"
        
        # Compliments and encouragement
        if any(word in user_lower for word in ['thank you', 'thanks', 'appreciate']):
            return "You're very welcome! I'm happy to help. Learning together is one of my favorite things! 😊"
        
        if any(word in user_lower for word in ['smart', 'clever', 'good job', 'amazing']):
            return "Thank you for the kind words! You're pretty amazing yourself for being curious and asking great questions! 🌟"
        
        # Weather talk
        if 'weather' in user_lower:
            return self.casual_conv['small_talk'].get('weather', "Weather can really affect our mood! What's the weather like where you are?")
        
        # Food talk
        if any(word in user_lower for word in ['food', 'eat', 'hungry', 'lunch', 'dinner']):
            return self.casual_conv['small_talk'].get('food', "Food is fascinating! It's fuel for our bodies and a way to explore different cultures. What's your favorite food?")
        
        # Simple reasoning problems
        if 'problem' in user_lower and 'solve' in user_lower:
            return "I'd love to help you solve a problem! You can ask me about math calculations, give me a reasoning puzzle, or ask for help understanding a concept. What kind of problem is it?"
        
        return None
        
    def extract_subject_from_input(self, user_input):
        """Extract subject from user input using various methods"""
        user_lower = user_input.lower()
        
        # Direct subject mentions
        for subject in self.subjects.keys():
            if subject in user_lower or subject.replace('_', ' ') in user_lower:
                return subject
        
        # Check for topic mentions within subjects
        for subject, content in self.subjects.items():
            if 'topics' in content:
                for topic in content['topics'].keys():
                    if topic in user_lower or topic.replace('_', ' ') in user_lower:
                        return subject
        
        # Keyword mapping for better recognition
        keyword_mapping = {
            'math': 'mathematics',
            'maths': 'mathematics',
            'calculus': 'mathematics',
            'algebra': 'mathematics',
            'geometry': 'mathematics',
            'science': 'physics',
            'programming': 'computer_science',
            'coding': 'computer_science',
            'algorithm': 'computer_science',
            'ai': 'computer_science',
            'machine learning': 'computer_science',
            'cell': 'biology',
            'dna': 'biology',
            'evolution': 'biology',
            'atom': 'chemistry',
            'molecule': 'chemistry',
            'reaction': 'chemistry',
            'war': 'history',
            'ancient': 'history',
            'poem': 'literature',
            'novel': 'literature',
            'book': 'literature',
            'map': 'geography',
            'climate': 'geography',
            'country': 'geography'
        }
        
        for keyword, subject in keyword_mapping.items():
            if keyword in user_lower:
                return subject
        
        return None
    
    def get_detailed_response(self, subject, user_input):
        """Generate detailed response about a subject"""
        if subject not in self.subjects:
            return self.get_general_help_response()
        
        subject_data = self.subjects[subject]
        user_lower = user_input.lower()
        
        # Check if asking about specific topic
        if 'topics' in subject_data:
            for topic, description in subject_data['topics'].items():
                if topic in user_lower or topic.replace('_', ' ') in user_lower:
                    return f"**{topic.replace('_', ' ').title()}**: {description}\n\nWould you like to know more about other aspects of {subject.replace('_', ' ')}?"
        
        # General subject overview
        response = f"**{subject.replace('_', ' ').title()}**\n\n{subject_data.get('description', 'No description available.')}"
        
        if 'key_concepts' in subject_data:
            response += f"\n\n**Key Concepts:**\n"
            for concept in subject_data['key_concepts'][:3]:  # Show first 3 concepts
                response += f"• {concept}\n"
        
        if 'topics' in subject_data:
            response += f"\n**Topics I can help you with:**\n"
            topics_list = list(subject_data['topics'].keys())[:4]  # Show first 4 topics
            for topic in topics_list:
                response += f"• {topic.replace('_', ' ').title()}\n"
        
        response += f"\n💡 Ask me specific questions about {subject.replace('_', ' ')} or type 'quiz {subject}' for a quiz!"
        return response
    
    def get_smart_response(self, user_input):
        """Generate intelligent responses using advanced analysis"""
        user_lower = user_input.lower()
        
        # First, try casual conversation
        casual_response = self.handle_casual_conversation(user_input)
        if casual_response:
            return casual_response
        
        # Try math calculations and problems
        math_response = self.handle_math_query(user_input)
        if math_response:
            return math_response
        
        # Try common sense reasoning
        common_sense_response = self.handle_common_sense(user_input)
        if common_sense_response:
            return common_sense_response
        
        # Greeting detection (fallback)
        if any(greeting in user_lower for greeting in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon']):
            return random.choice(self.patterns.get('greetings', ['Hello! How can I help you learn today?']))
        
        # Help detection
        if any(help_word in user_lower for help_word in ['help', 'what can you do', 'assistance', 'guide', 'how to use']):
            return random.choice(self.patterns.get('help_responses', ['I can help you learn various subjects!'])) + "\n\n💡 I can also:\n• Solve math problems (try: 'what is 15 + 27?')\n• Answer common sense questions\n• Have casual conversations\n• Explain concepts in simple terms"
        
        # Quiz detection
        if 'quiz' in user_lower or 'test' in user_lower:
            return "Starting a quiz! 🎯"
        
        # Subject-specific query
        subject = self.extract_subject_from_input(user_input)
        if subject:
            encouragement = random.choice(self.patterns.get('encouragement', ['Great question!']))
            detailed_response = self.get_detailed_response(subject, user_input)
            return f"{encouragement}\n\n{detailed_response}"
        
        # Question patterns for general knowledge
        question_patterns = [
            (r'what is (.*)', 'definition'),
            (r'how does (.*) work', 'explanation'),
            (r'explain (.*)', 'explanation'),
            (r'tell me about (.*)', 'general'),
            (r'define (.*)', 'definition'),
            (r'why (.*)', 'reasoning')
        ]
        
        for pattern, query_type in question_patterns:
            match = re.search(pattern, user_lower)
            if match:
                topic = match.group(1)
                subject = self.extract_subject_from_input(topic)
                if subject:
                    return self.get_detailed_response(subject, user_input)
        
        # Learning intent detection
        if any(word in user_lower for word in ['learn', 'study', 'teach me', 'understand', 'know about']):
            available_subjects = ', '.join([s.replace('_', ' ').title() for s in self.subjects.keys()])
            return f"I'd love to help you learn! I can teach you about:\n\n{available_subjects}\n\n🎯 You can also take subject-specific quizzes by typing 'quiz [subject]'\n🧮 Ask me math questions like 'what is 25 × 4?'\n� Or just chat with me about anything!\n�💡 Just ask me about any topic you're curious about!"
        
        # Fallback with helpful suggestions
        return "I'm not sure about that specific topic, but I'm here to help! 😊\n\n💡 **Try asking me:**\n• Educational questions: 'Explain photosynthesis'\n• Math problems: 'What is 15 + 27?'\n• Common sense: 'Why do things fall down?'\n• Casual chat: 'How are you doing?'\n• Subject learning: 'Tell me about physics'\n• Quizzes: 'Quiz mathematics easy'\n\nWhat would you like to explore?"
    
    def get_general_help_response(self):
        """Return a helpful general response"""
        available_subjects = ', '.join([s.replace('_', ' ').title() for s in self.subjects.keys()])
        return f"I'm your AI tutor and I can help you with many subjects!\n\n📚 **Available subjects:** {available_subjects}\n\n💡 **Try asking:**\n• 'Tell me about physics'\n• 'What is calculus?'\n• 'Explain photosynthesis'\n• 'Quiz mathematics'\n\n🎯 I can provide detailed explanations, answer questions, and create personalized quizzes!"
    
    def get_quiz_questions(self, subject=None, difficulty=None, count=5):
        """Get quiz questions for specific subject or mixed"""
        questions = []
        
        if subject and subject in self.quiz_db:
            available_questions = self.quiz_db[subject]
            if difficulty:
                available_questions = [q for q in available_questions if q.get('difficulty') == difficulty]
            questions = random.sample(available_questions, min(count, len(available_questions)))
        else:
            # Mixed quiz from all subjects
            all_questions = []
            for subj_questions in self.quiz_db.values():
                all_questions.extend(subj_questions)
            if difficulty:
                all_questions = [q for q in all_questions if q.get('difficulty') == difficulty]
            questions = random.sample(all_questions, min(count, len(all_questions)))
        
        return questions

# Initialize AI Tutor
ai_tutor = AITutor()

# API endpoint for AJAX requests
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_input = data.get('message', '')
    
    # Initialize session variables
    if 'quiz_active' not in session:
        session['quiz_active'] = False
        session['quiz_questions'] = []
        session['current_question'] = 0
        session['score'] = 0
        session['quiz_subject'] = None
    
    response = {}
    
    if session['quiz_active']:
        # Handle quiz answers
        if session['current_question'] < len(session['quiz_questions']):
            current_q = session['quiz_questions'][session['current_question']]
            user_answer = user_input.strip()
            correct_answer = current_q['answer']
            
            # Check answer (case-insensitive, flexible matching)
            is_correct = (user_answer.lower() == correct_answer.lower() or 
                         user_answer.lower() in correct_answer.lower() or
                         any(word in correct_answer.lower() for word in user_answer.lower().split() if len(word) > 2))
            
            if is_correct:
                encouragement = random.choice(conversation_patterns.get('quiz_encouragement', ['Correct!']))
                response['message'] = f"{encouragement}\n\n📝 **Explanation:** {current_q.get('explanation', 'Well done!')}"
                session['score'] += 1
            else:
                correction = random.choice(conversation_patterns.get('quiz_correction', ['Not quite right.']))
                response['message'] = f"{correction} **{correct_answer}**\n\n📝 **Explanation:** {current_q.get('explanation', '')}"
            
            session['current_question'] += 1
            
            # Check if more questions remain
            if session['current_question'] < len(session['quiz_questions']):
                next_q = session['quiz_questions'][session['current_question']]
                response['message'] += f"\n\n**Question {session['current_question'] + 1}:** {next_q['question']}"
                if next_q.get('type'):
                    response['message'] += f"\n*Topic: {next_q['type'].replace('_', ' ').title()}*"
            else:
                # Quiz finished
                total_questions = len(session['quiz_questions'])
                percentage = (session['score'] / total_questions) * 100
                
                if percentage >= 80:
                    grade = "Excellent! 🏆"
                elif percentage >= 60:
                    grade = "Good job! 👍"
                elif percentage >= 40:
                    grade = "Not bad! 📚"
                else:
                    grade = "Keep studying! 💪"
                
                response['message'] += f"\n\n🎯 **Quiz Complete!**\nScore: {session['score']}/{total_questions} ({percentage:.0f}%)\n{grade}"
                
                # Reset quiz session
                session['quiz_active'] = False
                session['current_question'] = 0
                session['score'] = 0
        else:
            session['quiz_active'] = False
            response['message'] = "Quiz completed! Type 'quiz' to start a new one."
    else:
        # Handle regular conversation
        user_input_lower = user_input.lower()
        
        # Quiz initiation
        if 'quiz' in user_input_lower:
            # Extract subject if specified
            quiz_subject = None
            for subject in ai_tutor.subjects.keys():
                if subject in user_input_lower or subject.replace('_', ' ') in user_input_lower:
                    quiz_subject = subject
                    break
            
            # Extract difficulty if specified
            difficulty = None
            if 'easy' in user_input_lower:
                difficulty = 'easy'
            elif 'medium' in user_input_lower:
                difficulty = 'medium'
            elif 'hard' in user_input_lower:
                difficulty = 'hard'
            
            # Get quiz questions
            questions = ai_tutor.get_quiz_questions(quiz_subject, difficulty, 5)
            
            if questions:
                session['quiz_active'] = True
                session['quiz_questions'] = questions
                session['current_question'] = 0
                session['score'] = 0
                session['quiz_subject'] = quiz_subject
                
                first_q = questions[0]
                subject_text = f" on {quiz_subject.replace('_', ' ').title()}" if quiz_subject else ""
                difficulty_text = f" ({difficulty} level)" if difficulty else ""
                
                response['message'] = f"🎯 **Starting Quiz{subject_text}{difficulty_text}!**\n\n**Question 1:** {first_q['question']}"
                if first_q.get('type'):
                    response['message'] += f"\n*Topic: {first_q['type'].replace('_', ' ').title()}*"
            else:
                response['message'] = "Sorry, I couldn't find quiz questions for that topic. Try 'quiz mathematics' or just 'quiz' for a mixed quiz!"
        else:
            # Regular conversation
            response['message'] = ai_tutor.get_smart_response(user_input)
    
    return jsonify(response)

# Start Flask routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input", "")
    
    # Initialize session variables
    if 'quiz_active' not in session:
        session['quiz_active'] = False
        session['quiz_questions'] = []
        session['current_question'] = 0
        session['score'] = 0
    
    if session['quiz_active']:
        # Handle quiz answers
        if session['current_question'] < len(session['quiz_questions']):
            current_q = session['quiz_questions'][session['current_question']]
            user_answer = user_input.strip()
            correct_answer = current_q['answer']
            
            # Check answer
            is_correct = (user_answer.lower() == correct_answer.lower() or 
                         user_answer.lower() in correct_answer.lower())
            
            if is_correct:
                response = f"Correct! 🎉\n\n{current_q.get('explanation', '')}"
                session['score'] += 1
            else:
                response = f"Not quite right. The correct answer is: {correct_answer}\n\n{current_q.get('explanation', '')}"
            
            session['current_question'] += 1
            
            if session['current_question'] < len(session['quiz_questions']):
                next_q = session['quiz_questions'][session['current_question']]
                response += f"\n\nQuestion {session['current_question'] + 1}: {next_q['question']}"
            else:
                total = len(session['quiz_questions'])
                percentage = (session['score'] / total) * 100
                response += f"\n\nQuiz finished! Your score: {session['score']}/{total} ({percentage:.0f}%) 🏆"
                session['quiz_active'] = False
        else:
            session['quiz_active'] = False
            response = "Quiz completed!"
    else:
        # Handle regular conversation
        if "quiz" in user_input.lower():
            questions = ai_tutor.get_quiz_questions()
            if questions:
                session['quiz_active'] = True
                session['quiz_questions'] = questions
                session['current_question'] = 0
                session['score'] = 0
                
                first_q = questions[0]
                response = f"Starting quiz! 🎯\n\nQuestion 1: {first_q['question']}"
            else:
                response = "Sorry, no quiz questions available."
        else:
            response = ai_tutor.get_smart_response(user_input)
    
    # Speak the response in a separate thread
    if response:
        threading.Thread(target=speak, args=(response,), daemon=True).start()
    
    return render_template("index.html", bot_response=response, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)
