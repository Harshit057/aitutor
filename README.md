# 🤖 AI Tutor - Personal Learning Assistant

> **A modern, interactive AI tutor that combines conversational AI with specialized educational features - completely local and privacy-focused!**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Harshit057/aitutor/graphs/commit-activity)

## 🌟 Key Highlights

- **🔒 100% Private**: All processing happens locally - your data never leaves your computer
- **💰 Zero Cost**: No API fees or subscriptions required
- **🎓 Educational Focus**: Specialized for learning with 8+ subjects and 30+ quiz questions
## 🚀 Quick Start

### **Option 1: Instant Start (Recommended)**
1. **Double-click `start_ai_tutor.bat`** in the project folder
2. **Open your browser** and navigate to `http://localhost:5000`
3. **Start learning!** 🎉

### **Option 2: Manual Start**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open in browser: http://localhost:5000
```

### **Option 3: With Local LLM (ChatGPT-like)**
For enhanced conversational AI capabilities:

1. **Install Ollama** (recommended):
   ```bash
   # Download from https://ollama.ai
   ollama pull llama3.2  # or llama2, mistral, etc.
   ollama serve
   ```

2. **Start AI Tutor**:
   ```bash
   python app.py
   ```

3. **Enjoy enhanced conversations** with full ChatGPT-like functionality!

> 📖 **Need help with LLM setup?** Check out `LLM_SETUP_GUIDE.md` for detailed instructions.

## ✨ Features

### 🤖 **Hybrid AI Intelligence**
- **Local LLM Integration**: Connect with Ollama, llama.cpp, or any OpenAI-compatible API
- **Built-in Expertise**: Specialized educational knowledge for precise academic responses
- **Smart Routing**: Automatically selects the best AI system for each type of question
- **Fallback System**: Works perfectly even without external LLM connections

### 🎓 **Educational Excellence**
- **📚 Comprehensive Subjects**: 8 major areas including Math, Science, History, and more
- **🎯 Intelligent Quizzes**: 30+ carefully crafted questions with multiple difficulty levels
- **🧮 Math Calculator**: Step-by-step solutions for arithmetic and word problems
- **🤔 Common Sense Q&A**: Practical knowledge about everyday topics
- **📝 Study Assistance**: Homework help and concept explanations

### 🎨 **Modern User Experience**
- **💬 Real-time Chat**: Instant responses with typing indicators
- **🔊 Voice Support**: Toggle text-to-speech for audio learning
- **📱 Responsive Design**: Perfect experience on desktop, tablet, and mobile
- **🎨 Beautiful Interface**: Modern gradient design with smooth animations
- **⚡ Fast Performance**: Optimized for quick responses and smooth interactions

### 🔧 **Technical Features**
- **🐍 Python Backend**: Built with Flask for reliability and scalability
- **🧠 NLP Processing**: Optional spaCy integration for advanced text analysis
- **🌐 HTTP API Ready**: Easy integration with any LLM service
- **� Session Management**: Maintains context during conversations
- **🔒 Privacy First**: All data stays on your machine

# Open in browser: http://localhost:5000
```

### **Option 3: With Local LLM (ChatGPT-like)**
For enhanced conversational AI capabilities:

1. **Install Ollama** (recommended):
   ```bash
   # Download from https://ollama.ai
   ollama pull llama3.2  # or llama2, mistral, etc.
   ollama serve
   ```

2. **Start AI Tutor**:
   ```bash
   python app.py
   ```

3. **Enjoy enhanced conversations** with full ChatGPT-like functionality!
## �️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.7+ | Core application logic |
| **Web Framework** | Flask 2.3+ | HTTP server and routing |
| **NLP** | spaCy (optional) | Natural language processing |
| **TTS** | pyttsx3 | Text-to-speech functionality |
| **HTTP Client** | requests | LLM API communication |
| **Frontend** | HTML5, CSS3, JavaScript | Modern responsive UI |
| **Data** | JSON | Knowledge base storage |

## 💬 Usage Examples

### **Educational Queries**
```
🧑 "Explain photosynthesis"
🤖 Detailed explanation with examples and key concepts

🧑 "Quiz me on mathematics easy"
🤖 Interactive quiz with step-by-step solutions

🧑 "What is 25 × 4 + 10?"
🤖 110. Here's how I calculated it: (25 × 4 = 100) + 10 = 110
```

### **Conversational AI** (with LLM)
```
🧑 "Write a poem about coding"
🤖 Creative poem about programming and technology

🧑 "Explain quantum computing like I'm 10"
🤖 Simple, engaging explanation with analogies

🧑 "Help me brainstorm app ideas"
🤖 Creative suggestions with detailed descriptions
```

### **Study Assistance**
```
🧑 "Help me understand Newton's laws"
🤖 Comprehensive explanation with real-world examples

🧑 "Common sense: Why do things fall down?"
🤖 Simple explanation of gravity suitable for all ages
```

## 📁 Project Structure

```
aitutor/
├── 📄 app.py                  # Main Flask application
├── 📄 main.py                 # Command-line interface
├── 📄 config.py               # Configuration settings
├── 📄 requirements.txt        # Python dependencies
├── 📄 start_ai_tutor.bat      # Windows quick-start script
├── 📄 question_answering.py   # Advanced Q&A processing
├── 📁 data/
│   └── 📄 content.json        # Educational knowledge base
├── 📁 templates/
│   └── 📄 index.html          # Modern web interface
└── 📁 __pycache__/            # Python cache files
```

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### **Detailed Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Harshit057/aitutor.git
   cd aitutor
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **[Optional] Install spaCy for enhanced NLP**:
   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

4. **[Optional] Set up local LLM**:
   - **Ollama** (recommended): Follow instructions at https://ollama.ai
   - **llama.cpp**: Set up local server
   - **Other**: Any OpenAI-compatible API endpoint

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the interface**:
   Open your browser and navigate to `http://localhost:5000`

## 🎯 AI Tutor vs. Alternatives

| Feature | AI Tutor | ChatGPT Plus | Khan Academy | Wolfram Alpha |
|---------|----------|--------------|--------------|---------------|
| **Privacy** | ✅ 100% Local | ❌ Cloud-based | ❌ Cloud-based | ❌ Cloud-based |
| **Cost** | ✅ Free Forever | ❌ $20/month | ✅ Free/Premium | ❌ Subscription |
| **Offline Use** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Educational Focus** | ✅ Specialized | ⚠️ General | ✅ Specialized | ✅ Math Focus |
| **Voice Support** | ✅ Built-in | ❌ Separate App | ❌ Limited | ❌ No |
| **Quizzes** | ✅ Interactive | ❌ No | ✅ Yes | ❌ No |
| **Math Solver** | ✅ Step-by-step | ⚠️ Text-based | ✅ Yes | ✅ Advanced |
| **Customization** | ✅ Full Control | ❌ Limited | ❌ No | ❌ No |

## 🎓 Perfect For

- **Students** (middle school to university)
- **Self-learners** exploring science and technology
- **Parents** helping with children's homework
- **Teachers** using interactive classroom tools
- **Privacy-conscious users** keeping data local
- **Budget-conscious learners** avoiding subscription fees
- **Offline learners** in areas with limited internet

## 🔮 Roadmap & Future Features

### **Upcoming Enhancements**
- [ ] User authentication and progress tracking
- [ ] More interactive learning modules
- [ ] Advanced quiz analytics
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Integration with more LLM providers
- [ ] Collaborative learning features
- [ ] Advanced visualization tools

### **Long-term Vision**
- [ ] Personalized learning paths
- [ ] AI-generated practice problems
- [ ] Integration with educational platforms
- [ ] Voice-first learning experience
- [ ] Advanced assessment tools

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Add features, fix bugs, improve documentation
4. **Test thoroughly**: Ensure everything works as expected
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Submit pull request**: Describe your changes clearly

### **Development Guidelines**
- Follow PEP 8 coding standards
- Add comments for complex logic
- Update documentation for new features
- Test with and without LLM integration
- Ensure mobile responsiveness

## 🐛 Troubleshooting

### **Common Issues**

**App won't start:**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check for port conflicts
netstat -ano | findstr :5000
```

**TTS not working:**
- Ensure pyttsx3 is installed correctly
- Check system audio settings
- Try toggling voice on/off in the interface

**LLM connection issues:**
- Verify LLM server is running
- Check firewall settings
- Review LLM_SETUP_GUIDE.md

**spaCy model missing:**
```bash
python -m spacy download en_core_web_sm
```

### **Getting Help**
- 📖 Check `LLM_SETUP_GUIDE.md` for detailed setup instructions
- 💬 Open an issue on GitHub for bugs or questions
- 📧 Contact the maintainers for urgent issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy**: Advanced natural language processing
- **Flask**: Lightweight and powerful web framework
- **pyttsx3**: Cross-platform text-to-speech library
- **Ollama**: Making local LLMs accessible
- **The open-source community**: For continuous inspiration and support

---

<div align="center">

**⭐ Star this project if you find it helpful!**

[Report Bug](https://github.com/Harshit057/aitutor/issues) • [Request Feature](https://github.com/Harshit057/aitutor/issues) • [Contribute](https://github.com/Harshit057/aitutor/pulls)

Made with ❤️ for learners everywhere

</div>
