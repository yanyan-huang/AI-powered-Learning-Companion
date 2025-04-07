# ai.py - Modular LLM router using LangChain with per-user model and conversation memory

from config import AI_PROVIDER, OPENAI_API_KEY, CLAUDE_API_KEY, GOOGLE_API_KEY
from config import AVAILABLE_MODELS  # Optional: for validation/debug
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import google.generativeai as genai
from prompts import MODE_PROMPTS
from storage import get_user_model  # Fetches model per provider per user

# ================================= #
#  Memory for User Conversations    #
# ================================= #
messages = {}  # messages[user_id][mode] → LangChain message history

# ================================ #
#   Core Chat Function             #
# ================================ #
def chat_with_ai(user_id, user_input, mode):
    """
    Route user input to their selected LLM model and return the AI response.
    Handles memory per user and per learning mode.
    """
    global messages

    if mode is None:
        return "⚠️ Please select a mode first! Use `/mode mentor`, `/mode coach`, or `/mode interviewer`."

    if mode not in MODE_PROMPTS:
        return "⚠️ Invalid mode. Please choose a valid mode."

    provider = AI_PROVIDER.lower()
    model_name = get_user_model(user_id, provider)

    # Special routing for Gemini
    if provider == "gemini":
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(model_name)
        system_prompt = MODE_PROMPTS[mode]

        # Build conversation history into plain string prompt
        conversation_history = ""
        if user_id in messages and mode in messages[user_id]:
            for msg in messages[user_id][mode]:
                prefix = "User" if isinstance(msg, HumanMessage) else "Assistant"
                conversation_history += f"{prefix}: {msg.content}\n"

        prompt = f"{system_prompt}\n\n{conversation_history}User: {user_input}"

        try:
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
        except Exception as e:
            ai_reply = f"❌ Gemini error: {str(e)}"

        # Track memory
        if user_id not in messages:
            messages[user_id] = {}
        if mode not in messages[user_id]:
            messages[user_id][mode] = [SystemMessage(content=system_prompt)]

        messages[user_id][mode].append(HumanMessage(content=user_input))
        messages[user_id][mode].append(SystemMessage(content=ai_reply))

        return ai_reply

    # Handle OpenAI or Claude via LangChain
    try:
        if provider == "openai":
            llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=model_name)
        elif provider == "claude":
            llm = ChatAnthropic(anthropic_api_key=CLAUDE_API_KEY, model=model_name)
        else:
            return f"⚠️ Unsupported provider: {provider}"
    except Exception as e:
        return f"❌ Error initializing model: {e}"

    # Initialize user memory if not already
    if user_id not in messages:
        messages[user_id] = {}
    if mode not in messages[user_id]:
        messages[user_id][mode] = [SystemMessage(content=MODE_PROMPTS[mode])]

    messages[user_id][mode].append(HumanMessage(content=user_input))

    try:
        response = llm(messages[user_id][mode])
        ai_reply = response.content
        messages[user_id][mode].append(response)
        return ai_reply
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# ================================= #
#  Mode Switching Utility Function  #
# ================================= #
def switch_mode(user_id, mode):
    """
    Reset conversation for a selected mode.
    """
    global messages
    if mode in MODE_PROMPTS:
        if user_id not in messages:
            messages[user_id] = {}
        messages[user_id][mode] = [SystemMessage(content=MODE_PROMPTS[mode])]
        return f"🔄 Mode switched to *{mode.capitalize()}*. Previous conversation cleared."
    else:
        return "⚠️ Invalid mode. Choose `/mode mentor`, `/mode coach`, or `/mode interviewer`."