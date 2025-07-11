#!/usr/bin/env python3
"""
AI Tutor Test Script - Demonstrates ChatGPT-like functionality
Tests both local LLM integration and built-in capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_ai_tutor(message, description=""):
    """Send a message to the AI Tutor and display the response"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": message},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n🤖 {description}")
            print(f"👤 User: {message}")
            print(f"🎓 AI Tutor: {data.get('message', 'No response')}")
            print("-" * 60)
        else:
            print(f"❌ Error: HTTP {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to AI Tutor. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    print("🚀 AI Tutor ChatGPT-like Functionality Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print("✅ AI Tutor server is running!")
    except:
        print("❌ AI Tutor server is not running. Please start it first:")
        print("   python app.py")
        return
    
    # Test various capabilities
    test_cases = [
        # Built-in capabilities (will work even without local LLM)
        ("Hello! How are you doing today?", "Casual Greeting"),
        ("What is 25 + 17?", "Math Calculator"),
        ("Why do things fall down?", "Common Sense Question"),
        ("Tell me about photosynthesis", "Educational Topic"),
        ("quiz mathematics easy", "Quiz System"),
        
        # General questions (will use local LLM if available, otherwise show fallback)
        ("What is the meaning of life?", "Open-ended Question (LLM Test)"),
        ("Explain quantum computing in simple terms", "Complex Topic (LLM Test)"),
        ("Write a short poem about artificial intelligence", "Creative Request (LLM Test)"),
    ]
    
    for message, description in test_cases:
        if not test_ai_tutor(message, description):
            break
        time.sleep(1)  # Brief pause between requests
    
    print("\n🎯 Test Complete!")
    print("\n📋 Results Analysis:")
    print("✅ If you see responses to all questions: Everything is working perfectly!")
    print("⚠️  If you see 'LLM connection error': Built-in features work, but no local LLM is running")
    print("📖 To enable full ChatGPT-like features, follow the LLM_SETUP_GUIDE.md")
    
    print("\n🔗 Next Steps:")
    print("1. Install Ollama: https://ollama.ai")
    print("2. Pull a model: ollama pull llama2")
    print("3. Start server: ollama serve")
    print("4. Re-run this test to see the difference!")

if __name__ == "__main__":
    main()
