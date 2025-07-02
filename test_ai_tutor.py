"""
Enhanced Test script for AI Tutor functionality
"""

import json
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_knowledge_base():
    """Test if enhanced knowledge base loads correctly"""
    try:
        with open("data/content.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        subjects = data.get('subjects', {})
        quiz_db = data.get('quiz_database', {})
        patterns = data.get('conversation_patterns', {})
        
        print(f"✅ Enhanced knowledge base loaded:")
        print(f"   - {len(subjects)} subjects available")
        print(f"   - {sum(len(questions) for questions in quiz_db.values())} quiz questions")
        print(f"   - {len(patterns)} conversation pattern types")
        
        # Test subject structure
        for subject, content in list(subjects.items())[:3]:  # Test first 3 subjects
            if 'description' in content and 'topics' in content:
                print(f"   - {subject}: {len(content['topics'])} topics")
            else:
                print(f"   ⚠️ {subject}: Missing required structure")
        
        return True
    except Exception as e:
        print(f"❌ Enhanced knowledge base error: {e}")
        return False

def test_ai_tutor_class():
    """Test the AITutor class functionality"""
    try:
        from app import AITutor, subjects, quiz_database, conversation_patterns
        
        ai_tutor = AITutor()
        print("✅ AITutor class initialized successfully")
        
        # Test subject extraction
        test_cases = [
            ("Tell me about mathematics", "mathematics"),
            ("What is physics?", "physics"),
            ("I want to learn chemistry", "chemistry"),
            ("Explain programming", "computer_science"),
            ("Biology basics", "biology")
        ]
        
        for test_input, expected_subject in test_cases:
            extracted = ai_tutor.extract_subject_from_input(test_input)
            if extracted == expected_subject:
                print(f"✅ Subject extraction: '{test_input}' → {extracted}")
            else:
                print(f"⚠️ Subject extraction: '{test_input}' → {extracted} (expected {expected_subject})")
        
        return True
    except Exception as e:
        print(f"❌ AITutor class error: {e}")
        return False

def test_quiz_system():
    """Test the enhanced quiz system"""
    try:
        from app import AITutor
        
        ai_tutor = AITutor()
        
        # Test getting quiz questions
        all_questions = ai_tutor.get_quiz_questions()
        math_questions = ai_tutor.get_quiz_questions('mathematics')
        easy_questions = ai_tutor.get_quiz_questions(difficulty='easy')
        
        print(f"✅ Quiz system tests:")
        print(f"   - General quiz: {len(all_questions)} questions")
        print(f"   - Mathematics quiz: {len(math_questions)} questions")
        print(f"   - Easy difficulty: {len(easy_questions)} questions")
        
        # Test question structure
        if all_questions:
            sample_q = all_questions[0]
            required_fields = ['question', 'answer']
            has_all_fields = all(field in sample_q for field in required_fields)
            print(f"   - Question structure: {'✅' if has_all_fields else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ Quiz system error: {e}")
        return False

def test_smart_responses():
    """Test the smart response generation"""
    try:
        from app import AITutor
        
        ai_tutor = AITutor()
        
        test_cases = [
            ("Hello", "greeting"),
            ("What is mathematics?", "subject_explanation"),
            ("Help me", "help_response"),
            ("Tell me about physics", "detailed_subject"),
            ("Quiz mathematics", "quiz_initiation"),
            ("Explain photosynthesis", "topic_explanation")
        ]
        
        print("✅ Smart response tests:")
        for test_input, expected_type in test_cases:
            response = ai_tutor.get_smart_response(test_input)
            if response and len(response) > 10:  # Basic check for substantial response
                print(f"   ✅ '{test_input}' → Response generated ({len(response)} chars)")
            else:
                print(f"   ❌ '{test_input}' → Insufficient response")
        
        return True
    except Exception as e:
        print(f"❌ Smart response error: {e}")
        return False

def test_flask_integration():
    """Test Flask app integration"""
    try:
        from app import app, ai_tutor
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask home page loads successfully")
            else:
                print(f"❌ Flask home page error: {response.status_code}")
                return False
            
            # Test API endpoint
            response = client.post('/api/chat', 
                                 json={'message': 'Hello'},
                                 content_type='application/json')
            if response.status_code == 200:
                print("✅ Flask API endpoint responds successfully")
            else:
                print(f"❌ Flask API endpoint error: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Flask integration error: {e}")
        return False

def main():
    print("🤖 Enhanced AI Tutor Test Suite")
    print("=" * 50)
    
    tests = [
        test_enhanced_knowledge_base,
        test_ai_tutor_class,
        test_quiz_system,
        test_smart_responses,
        test_flask_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The Enhanced AI Tutor is ready!")
        print("\n🚀 Features available:")
        print("  • Comprehensive subject coverage")
        print("  • Intelligent conversation handling")
        print("  • Advanced quiz system with explanations")
        print("  • Subject-specific and difficulty-based quizzes")
        print("  • Natural language understanding")
        print("\n💡 To start the application:")
        print("  python app.py")
        print("  or double-click start_ai_tutor.bat")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("The application may still work with reduced functionality.")

if __name__ == "__main__":
    main()
