# AI-Powered Learning Companion (for Product Management) 🎓 🚀

## 📌 Overview
This AI-powered learning companion provides mentorship, coaching, and mock interview simulations for aspiring and transitioning Product Managers. It leverages OpenAI's GPT-4 to offer structured learning paths, real-time feedback, and interactive practice sessions. The application is built using a modular **Model-View-Controller (MVC)** architecture and supports both a RESTful API and a command-line interface (CLI).

## 🎯 MVP Focus
- **Mentor Mode** – AI recommends structured learning paths, courses, books, and career advice.
- **Coach Mode** – AI provides Q&A assistance for PM concepts with real-world examples.
- **Mock Interview Mode** – AI conducts simulated PM interviews and provides structured feedback.
- **Flask API** – Exposes a RESTful API for integration with future web or mobile interfaces.
- **CLI Interface** – Allows direct interaction with the backend for testing and debugging.

## 🚀 Future Enhancements
- **Web UI:** Extend interaction via a web-based chat interface.
- **Advanced Voice Input:** Enhance transcription accuracy using tools like OpenAI Whisper.
- **User Data Tracking:** Store and analyze user interactions for personalized learning.
- **Deployment:** Host the API on cloud platforms using a production-ready WSGI server.

## 🛠️ Tech Stack
**Backend: Python (Flask API & CLI)**  
- **Flask API:** Serves as the primary interface for external clients by exposing RESTful endpoints.
- **CLI:** A command-line interface built on the same backend logic. Although a CLI is an interface, it is considered part of the backend because it directly interacts with the core business logic and is used for development, testing, and debugging.
- **OpenAI GPT-4:** Provides intelligent responses.
- **Gunicorn:** A production-ready WSGI server to deploy the Flask API.
- **python-dotenv:** Manages environment variables securely.

## 📂 Folder Structure
```
/Project_directory
│-- api.py      # API Entry Point
│-- web.py      # Web Interface Entry Point
│-- cli.py      # CLI Interface Entry Point
│-- chatbot/    # Main Application Code
│   ├── __init__.py
│   ├── model.py      # AI Model (Business logic)
│   ├── controller.py # API Controller (Flask logic)
│   ├── cli_view.py   # CLI Interface (View)
│   └── web_view.py   # Web Interface (View)
│-- tests/      # Test Scripts
│   ├── test_api.py   # API Test Script
│-- requirements.txt   # Python Dependencies
│-- README.md         # Project Documentation
│-- .env             # Environment Variables (not tracked by Git)
│-- wsgi.py          # WSGI Entry Point for Production Deployment
```

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yanyan-huang/AI-powered-Learning-Companion.git
cd AI-powered-Learning-Companion
```

### 2️⃣ Create a Virtual Environment & Install Dependencies  
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Up API Key Securely  

#### **Option 1: Use an Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"  # macOS/Linux
setx OPENAI_API_KEY "your-api-key-here"    # Windows (Command Prompt)
```

#### **Option 2: Use a `.env` File**  
1. Create a `.env` file in the project root:  
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
2. Install `python-dotenv` if not already installed:  
   ```bash
   pip install python-dotenv
   ```

### 4️⃣ Install OpenAI Library 
```bash
pip install openai
```  

### 5️⃣ Run the Application
Choose the appropriate entry point based on your needs:

```bash
# For API mode (Production)
python api.py

# For Web Interface (Development)
python web.py

# For CLI Interface (Development/Testing)
python cli.py
```

For Production Deployment with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
```

## 🔮 Future Enhancements  
🚀 **Web Interface** – Simple UI for chat interaction.  
🚀 **Voice Input** – Integrate voice processing (e.g., using OpenAI Whisper).  
🚀 **User Data Tracking** – Store user interactions for personalized learning.  
🚀 **Deployment** – Consider using Gunicorn with a reverse proxy (e.g., Nginx) or deploy on popular platforms like Render or AWS for automated scaling and reduced operational overhead.

---

🔗 **Want to Contribute?** Fork, clone, and submit a pull request! 🚀  
For any questions, feel free to open a discussion or contact me.  
Happy learning! 😊
