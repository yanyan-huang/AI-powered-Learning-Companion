from openai import OpenAI  # OpenAI API client for GPT-based interactions
from config import OPENAI_API_KEY  # Load OpenAI API key from config
from prompts import MODE_PROMPTS, DEFAULT_MODE  # Import AI learning mode prompts

# ============================== #
#  Initialize OpenAI API Client  #
# ============================== #

# Initialize OpenAI Client with API key
client = OpenAI(api_key=OPENAI_API_KEY)

# ============================== #
#  AI Chat & Conversation Logic  #
# ============================== #

# Store conversation history per user and mode
# Example: messages[user_id][mode] → List of conversation messages
messages = {}

def chat_with_ai(user_id, user_input, mode):
    """
    Process user input and generate an AI response based on the selected mode.
    """
    global messages

    # Ensure a mode is selected before responding
    if mode is None:
        return "⚠️ Please select a mode first! Type `/mode mentor`, `/mode coach`, or `/mode interviewer` to begin."

    # Reset and start fresh if switching mode
    if user_id not in messages:
        messages[user_id] = {}
    if mode not in messages[user_id]:  # Start fresh when switching modes
        messages[user_id][mode] = [{"role": "system", "content": MODE_PROMPTS[mode]}]

    messages[user_id][mode].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages[user_id][mode]
    )

    ai_reply = response.choices[0].message.content
    messages[user_id][mode].append({"role": "assistant", "content": ai_reply})

    return ai_reply

# =============================== #
#  AI Mode Switching Function     #
# =============================== #

def switch_mode(user_id, mode):
    """
    Switch AI mode for the user and reset conversation history.
    """
    global messages
    if mode in MODE_PROMPTS:
        if user_id not in messages:
            messages[user_id] = {}
        messages[user_id][mode] = [{"role": "system", "content": MODE_PROMPTS[mode]}]  # Reset history
        return f"🔄 Mode switched to *{mode.capitalize()}*. Previous conversation cleared."
    else:
        return "⚠️ Invalid mode. Choose `/mode mentor`, `/mode coach`, or `/mode interviewer`."