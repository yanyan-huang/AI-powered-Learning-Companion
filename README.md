# AI-Powered Learning Companion (for Product Management) 🎓 🚀

## 📌 Overview  
This **AI-powered learning companion** provides **mentorship, tutoring, and mock interview coaching** for **aspiring and transitioning Product Managers**. It leverages AI to offer **structured learning paths, real-time feedback, and interactive interview practice** via **Telegram**.

## 🎯 MVP Status:
👉 **Mentor Mode** – AI recommends personalized gap analysis and structured learning paths tailored to individual goals.  
👉 **Coach Mode** – AI provides interactive Q&A and guided case study to enhance critical thinking and experiential learning.  
👉 **Mock Interview Mode** – AI simulates different types of PM interviews and gives structured feedback for improvements.  
👉 **Telegram Bot** – Users interact with the AI directly via Telegram, with text and voice support.  
👉 **Flexible LLM routing**: Switchable LLM providers — OpenAI (primary), Claude, Gemini (via config)  
👉 **Multimodal input**: Text and voice (speech-to-text via Whisper)  
👉 **Session Logging** – Automatically saves user input + AI responses by mode and source in JSON.  

## 🚀 Future Exploration  
🔜 **Web UI** – Extend interaction beyond Telegram via a simple chat interface (React + Flask).     
🔜 **Databased integration** – Replace local JSON files with a scalable solution (e.g., PostgreSQL or Firebase) for structured user data and analytics.    

---

## 🔧 Tech Stack

| Layer                | Tools & Libraries                                              | Description                                                                 |
|----------------------|---------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Bot Platform**     | [Telegram Bot API](https://core.telegram.org/bots/api)        | Enables user interaction via chat and voice messages                        |
| **Backend**          | Python                                                        | Core language for bot logic and orchestration                               |
| **AI/LLM Integration** | LangChain, OpenAI (GPT-4), Anthropic (Claude), Google Gemini | Supports flexible routing to different LLM providers                        |
| **Prompt Design**    | Custom system prompts (`prompts.py`)                          | Tailored instructions for mentor, coach, and interviewer modes              |
| **Voice Support**    | MoviePy, OpenAI Whisper API                                   | Converts `.ogg` → `.mp3`, transcribes to text using Whisper                 |
| **Data Storage**     | JSON (via `storage.py`)                                       | Logs mode, user input, AI responses, and message source                     |
| **Environment Config**| python-dotenv                                                 | Loads environment variables securely from `.env`                            |
| **Deployment**       | Render.com (to be upgraded)                                   | Deploy as a background worker for continuous availability                   |


---

## 📂 **Folder Structure**
```
/Project_directory
│─ telegram_bot.py     # Main bot entry point (loads handlers) for Telegram bot interactions
│─ handlers.py         # Handles text messages, mode switching, and voice processing
│─ ai.py               # Core AI logic for processing messages & LLM routing (OpenAI, Claude, Gemini) 
│─ storage.py         # User history tracking + mode/session saving 
│─ config.py           # Stores API keys & environment variables
│─ prompts.py          # Stores AI prompts tailored for different modes
│─ data/
│  └── user_history.json  # Local user history
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
| `/mode mentor` | Switch to **Mentor Mode** (Personalized career guidance & learning paths). |
| `/mode coach` | Switch to **Coach Mode** (Interactive PM concepts Q&A and guided case study). |
| `/mode interviewer` | Switch to **Mock Interview Mode** (Real-time PM interview simulations). 

---

📚 **Want to Contribute?** Fork, clone, and submit a pull request! 🚀  
For any questions, feel free to open a discussion or contact me.  
Happy learning! 😊

