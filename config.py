"""
Configuration settings for AI Tutor application
"""

import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ai-tutor-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Application settings
    KNOWLEDGE_BASE_FILE = 'data/content.json'
    MAX_MESSAGE_LENGTH = 1000
    QUIZ_TIME_LIMIT = 300  # seconds
    
    # Text-to-speech settings
    TTS_ENABLED = True
    TTS_RATE = 150  # words per minute
    TTS_VOLUME = 0.8
    
    # NLP settings
    SPACY_MODEL = 'en_core_web_sm'
    SPACY_REQUIRED = False  # Make spaCy optional
    
    # UI settings
    APP_NAME = 'AI Tutor'
    APP_DESCRIPTION = 'Your Personal Learning Assistant'
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
