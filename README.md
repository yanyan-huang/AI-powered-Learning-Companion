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
👉 **Session Logging** Logs user history (text & voice) by mode  

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
│
├── telegram_bot.py               # 🔹 Main entry point — sets up and runs the Telegram bot
├── handlers.py                   # 🔹 Handles /start, /help, /mode, text, and voice messages
│
├── bot_user.py                   # 🧠 Manages user session data, mode, memory, and interaction logging
├── conversation_manager.py       # 🧠 Coordinates user input, mode switching, and LLM response
├── llm_router.py                 # 🧠 Routes requests to OpenAI, Claude, or Gemini (via LangChain or Gemini API)
│
├── prompts.py                    # 📋 Prompt templates for mentor, coach, interviewer modes
├── greetings.py                  # 📋 Greeting messages for each mode
│
├── config.py                     # ⚙️ Loads environment variables and API key validations
│─ data/
│  └── user_history.json          # Local user history
├── README.md                     # 📖 Project overview and usage instructions
│─ requirements.txt               # 📦 (Optional) Dependencies
│─ .env                           # 🔐 (Optional) Environment variables file
```

---
## 🧠 Architecture Highlights

- **ConversationManager** ties together `BotUser` (user state) and `LLMRouter` (LLM output).
- **Handlers** manage command input and delegate to `ConversationManager`.
- **LLMRouter** dynamically switches between OpenAI, Claude, and Gemini.
- **BotUser** tracks mode, memory, and history per user.

### 📊 Architecture Diagram
Below diagram illustrates how the PM Pal Telegram bot orchestrates input handling, AI routing, memory management, and LLM response generation through a clean object-oriented architecture.

```
                 +--------------------+
                 |   Telegram User    |
                 +---------+----------+
                           |
                           v
            +------------------------------+
            |       telegram_bot.py        |
            |  (Bot App & Command Routing) |
            +------+-----------------------+
                   |
       +-----------+------------+
       |                        |
       v                        v
+---------------+     +------------------+
| CommandHandler|     | MessageHandler   |
| (/start, /help)|    | (text / voice)   |
+-------+-------+     +---------+--------+
        |                         |
        v                         v
+-----------------+     +---------------------+
|   handlers.py   | <--> | ConversationManager |
+-----------------+     +----------+----------+
                                   |
       +---------------------------+--------------------------+
       |                                                      |
       v                                                      v
+--------------+                                     +-----------------+
|   BotUser    |                                     |   LLMRouter     |
| (Tracks mode,|                                     | (LLM responses  |
|  memory,     |                                     |  via OpenAI,    |
|  history)    |                                     |  Claude, Gemini)|
+--------------+                                     +-----------------+
       |                                                      |
       |                                              +------------------+
       |                                              |    prompts.py    |
       v                                              +------------------+
+--------------------+                               | Mode-specific    |
| user_data/*.json   | <-----------------------------+ system prompts   |
| (memory + history) |
+--------------------+
```

---
## 🧠 How Memory vs. History Work

To support high-quality, context-aware conversations and long-term user insights, the bot stores two types of conversational data: `memory` and `history`. Here's how they differ:


```
                          ┌────────────────────────────┐
                          │     Telegram Input         │
                          └────────────┬───────────────┘
                                       ▼
                                ┌─────────────┐
                                │ handlers.py │
                                └─────┬───────┘
                                      ▼
                            ┌──────────────────────┐
                            │ ConversationManager  │
                            └─────┬──────────┬──────┘
                                  ▼          ▼
                          ┌────────────┐  ┌────────────┐
                          │   memory   │  │  history   │
                          │ (per mode) │  │ (all msgs) │
                          └────┬───────┘  └────┬───────┘
                               │               │
         ┌─────────────────────┘               └────────────────────┐
         ▼                                                        ▼
┌────────────────┐                                  ┌────────────────────────────┐
│  LLMRouter.py  │◀──────── Uses memory only ──────▶│  Not involved in response  │
└────────────────┘                                  └────────────────────────────┘
```

### 🧠 `memory` vs `history`

| Feature             | `memory`                             | `history`                            |
|--------------------|---------------------------------------|--------------------------------------|
| **What it stores** | A few recent messages (context stack) | All user-assistant messages          |
| **Used by LLM?**   | ✅ Yes – LLM reads from it            | ❌ No – for logs only                 |
| **Format**         | LangChain-style `Message` objects     | JSON with role, timestamp, source    |
| **Scope**          | Per-mode (`mentor`, `coach`, etc.)    | Cumulative, all sessions             |
| **Token-limited?** | ✅ Yes (trimmed for LLMs)             | ❌ No                                |
| **Purpose**        | Maintain coherent conversation context| Track usage, behavior, feedback, etc.|
| **Updated by**     | `ConversationManager`                 | `BotUser`                            |

Including both gives the bot:
- A **short-term memory** for smart replies
- A **long-term history** for insights, logging, and potential analytics

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

