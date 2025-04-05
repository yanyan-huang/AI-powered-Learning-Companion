
# ai.py - Modular LLM router using LangChain with per-user conversation memory

from config import AI_PROVIDER, OPENAI_API_KEY, CLAUDE_API_KEY
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from prompts import MODE_PROMPTS

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

# ================================= #
#  Chat Function for AI Interaction #
# ================================= #
def chat_with_ai(user_id, user_input, mode):
    """
    Process user input and generate a response using the selected AI provider and mode.
    Maintains separate conversation history per user and mode.
    """
    global messages

    if mode is None:
        return "⚠️ Please select a mode first! Use `/mode mentor`, `/mode coach`, or `/mode interviewer`."

    if mode not in MODE_PROMPTS:
        return "⚠️ Invalid mode. Please choose a valid mode."

    llm = llms.get(AI_PROVIDER.lower())
    if not llm:
        return f"⚠️ Unsupported AI provider: {AI_PROVIDER}"

    # Initialize conversation memory for user if not exists
    if user_id not in messages:
        messages[user_id] = {}
    if mode not in messages[user_id]:
        messages[user_id][mode] = [SystemMessage(content=MODE_PROMPTS[mode])]

    # Add new user input to conversation history
    messages[user_id][mode].append(HumanMessage(content=user_input))

    try:
        # Generate AI response using selected provider
        response = llm(messages[user_id][mode])
        ai_reply = response.content

        # Add AI response to conversation history
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