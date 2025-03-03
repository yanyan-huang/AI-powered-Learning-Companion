# AI-Powered Learning Companion (for Product Management) 🎓 🚀

## 📌 Overview  
This **AI-powered learning companion** provides **mentorship, tutoring, and mock interview coaching** for **aspiring and transitioning Product Managers**. It leverages AI to offer **structured learning paths, real-time feedback, and interactive interview practice** via **Telegram**.

## 🎯 MVP Focus:
👉 **Mentor Mode** – AI recommends structured learning paths, courses, books, and career advice.  
👉 **Tutor Mode** – AI provides Q&A assistance for PM concepts with real-world examples.  
👉 **Mock Interview Mode** – AI conducts simulated PM interviews and gives structured feedback.  
👉 **Telegram Bot** – Users interact with the AI directly via Telegram, with text and voice support.  

## 🚀 Future Exploration  
🔜 **Coach Mode** – Guides users in **case study learning**, prompting user research while following **canonical frameworks**.  
🔜 **Web UI** – Extend interaction beyond Telegram via a simple chat interface.  
🔜 **Advanced Voice Input** – Enhance transcription accuracy for better responses.  
🔜 **User Data Tracking** – Store user interactions for personalized learning experiences.  

---

## 🛠️ Tech Stack  
- **Backend:** Python (Telegram Bot API + OpenAI API)  
- **AI Integration:** OpenAI GPT-4 for intelligent responses  
- **Voice Processing:** Telegram handles voice message retrieval; OpenAI Whisper transcribes speech to text
- **Environment Management:** `.env` for API key security  
- **Deployment:** Hosted on **Render.com** as a **Background Worker** for continuous availability  

---

## 📂 **Folder Structure**
```
/your_project_directory
│─ telegram_bot.py     # Main bot entry point (loads handlers) for Telegram bot interactions
│─ handlers.py         # Handles text messages, mode switching, and voice processing
│─ ai.py               # AI logic for processing messages & switching modes
│─ config.py           # Stores API keys & environment variables
│─ prompts.py          # Stores AI mode prompts
│─ requirements.txt  # (Optional) Dependencies
│─ .env              # (Optional) Environment variables file
```

---

## 🔧 **Installation & Setup**  

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

### 3️⃣ Set Up API Keys Securely  

#### **Option 1: Use Environment Variables (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"  # macOS/Linux
setx OPENAI_API_KEY "your-api-key-here"    # Windows (Command Prompt)
export TELEGRAM_API_TOKEN="your-telegram-bot-token-here"  # macOS/Linux
setx TELEGRAM_API_TOKEN "your-telegram-bot-token-here"    # Windows (Command Prompt)
```

#### **Option 2: Use a `.env` File**  
1. Create a `.env` file in the project root:  
   ```
   OPENAI_API_KEY=your-api-key-here
   TELEGRAM_API_TOKEN=your-telegram-bot-token-here
   ```
2. Install `python-dotenv` if not already installed:  
   ```bash
   pip install python-dotenv
   ```

---

## 🚀 **Running the Telegram Bot Locally**
```bash
python telegram_bot.py
```
- The bot will start and listen for messages on Telegram.  
- Open your **Telegram bot** and send a message to start interacting.  

---

## 🚀 **Using the Telegram Bot**
The bot is live and can be accessed on Telegram:  
👉 [LearningPAL Bot](https://web.telegram.org/k/#@LearningPAL_Bot)

---

## 📍 **Using the Bot**
### **Basic Commands**
| Command | Description |
|---------|------------|
| `/help` | Show instructions on how to use the bot. |
| `/mode mentor` | Switch to **Mentor Mode** (Career guidance & learning paths). |
| `/mode tutor` | Switch to **Tutor Mode** (Q&A for PM concepts). |
| `/mode interviewer` | Switch to **Mock Interview Mode** (PM interview simulations). |
| `/mode coach` | Switch to **Coach Mode** (Guided case study learning). |

---

📚 **Want to Contribute?** Fork, clone, and submit a pull request! 🚀  
For any questions, feel free to open a discussion or contact me.  
Happy learning! 😊

