# AI-Powered Learning Companion (for Product Management) 🎓 🚀

## 📌 Overview  
This **AI-powered learning companion** provides **mentorship, tutoring, and mock interview coaching** for **aspiring and transitioning Product Managers**. It leverages AI to offer **structured learning paths, real-time feedback, and interactive interview practice**.

## 🎯 MVP Focus: Backend Development  
✅ **Mentor Mode** – AI recommends structured learning paths, courses, books, and career advice.  
✅ **Tutor Mode** – AI provides Q&A assistance for PM concepts with real-world examples.  
✅ **Mock Interview Mode** – AI conducts simulated PM interviews and gives structured feedback.  
✅ **Flask API** – A backend service to process user queries via API requests.

## 🚀 Future Exploration  
🔜 **Simple Web UI** – Users interact with AI via a web-based text interface.  
🔜 **Voice Input** – Allow users to ask questions using Web Speech API.  

---

## 🛠️ Tech Stack  
- **Backend**: Python (Flask) + OpenAI API  
- **Environment Management**: `.env` for API key security  
- **API Interaction**: JSON-based Flask API (can be connected to future UI)  

---

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

### 4️⃣ Run the Flask API  
```bash
python app.py
```
- The API will be available at **`http://127.0.0.1:5000`**.

---

## 🛠️ Testing the API  

Use **Postman** or **`curl`** to test the API.  

Example request using `curl`:
```bash
curl -X POST http://127.0.0.1:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "How do I improve my product sense?", "mode": "mentor"}'
```

Example JSON response:
```json
{
    "response": "To improve your product sense, analyze successful products, understand user needs, and practice problem-solving through case studies."
}
```

---

## 🔮 Future Enhancements  
🚀 **Web Interface** – Simple UI for chat interaction.  
🚀 **Voice Input** – Explore Web Speech API for spoken queries.  
🚀 **User Data Tracking** – Store user interactions for personalized learning.  
🚀 **Deployment** – Host the API on Render, Heroku, or AWS.  


---

🔗 **Want to Contribute?** Fork, clone, and submit a pull request! 🚀  
For any questions, feel free to open a discussion or contact me.  
Happy learning! 😊
