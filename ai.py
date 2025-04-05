
# ai.py - Modular LLM router using LangChain with per-user conversation memory

from config import AI_PROVIDER, OPENAI_API_KEY, CLAUDE_API_KEY, GOOGLE_API_KEY # Load API keys and provider
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import google.generativeai as genai  # Gemini SDK
from prompts import MODE_PROMPTS

# # DEBUGGING: Print gemini models
# genai.configure(api_key=GOOGLE_API_KEY)

# print("Available Gemini models:")
# for model in genai.list_models():
#     print(f"- {model.name} | {model.supported_generation_methods}")

# ================================= #
#  Initialize LangChain LLM Clients #
# ================================= #
llms = {
    "openai": ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-4",
        temperature=0
    ),
    "claude": ChatAnthropic(
        anthropic_api_key=CLAUDE_API_KEY,
        model="claude-3-7-sonnet-20250219"
    )
}

# ================================= #
#  Memory for User Conversations    #
# ================================= #
# Stores conversation history by user_id and mode
# Example: messages[user_id][mode] → List of message objects (System, Human, Assistant)
messages = {} 

# ================================ #
#   Core Chat Function             #
# ================================ #
def chat_with_ai(user_id, user_input, mode):
    """
    Route to appropriate LLM based on AI_PROVIDER and return AI response.
    Handles memory per user and per mode.
    """
    global messages

    if mode is None:
        return "⚠️ Please select a mode first! Use `/mode mentor`, `/mode coach`, or `/mode interviewer`."

    if mode not in MODE_PROMPTS:
        return "⚠️ Invalid mode. Please choose a valid mode."

    # Special Gemini routing logic because Gemini does not fit so well into LangChain currently
    if AI_PROVIDER == "gemini":
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        system_prompt = MODE_PROMPTS[mode]

        # Rebuild conversation history into flat string
        conversation_history = ""
        if user_id in messages and mode in messages[user_id]:
            for msg in messages[user_id][mode]:
                prefix = "User" if msg.type == "human" else "Assistant"
                conversation_history += f"{prefix}: {msg.content}\n"

        prompt = f"{system_prompt}\n\n{conversation_history}User: {user_input}"

        try:
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
        except Exception as e:
            ai_reply = f"❌ Gemini error: {str(e)}"

        # Track memory even for Gemini
        if user_id not in messages:
            messages[user_id] = {}
        if mode not in messages[user_id]:
            messages[user_id][mode] = [SystemMessage(content=system_prompt)]

        messages[user_id][mode].append(HumanMessage(content=user_input))
        messages[user_id][mode].append(SystemMessage(content=ai_reply))

        return ai_reply

    # Default LangChain LLM path (OpenAI, Claude, etc.)
    llm = llms.get(AI_PROVIDER.lower())
    if not llm:
        return f"⚠️ Unsupported AI provider: {AI_PROVIDER}"

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
    Switch the AI mode for the user and clear previous conversation history.
    """
    global messages
    if mode in MODE_PROMPTS:
        if user_id not in messages:
            messages[user_id] = {}
        messages[user_id][mode] = [SystemMessage(content=MODE_PROMPTS[mode])]
        return f"🔄 Mode switched to *{mode.capitalize()}*. Previous conversation cleared."
    else:
        return "⚠️ Invalid mode. Choose `/mode mentor`, `/mode coach`, or `/mode interviewer`."