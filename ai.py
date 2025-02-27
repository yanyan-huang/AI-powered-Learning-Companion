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

# Store conversation history to maintain context
messages = [{"role": "system", "content": MODE_PROMPTS[DEFAULT_MODE]}]  # Default system prompt
current_mode = DEFAULT_MODE  # Default AI mode

def chat_with_ai(user_input):
    """
    Process user input and generate an AI response based on the selected mode.
    Maintains conversation history for context.
    """
    messages.append({"role": "user", "content": user_input})  # Append user input

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )  # Generate AI response

    ai_reply = response.choices[0].message.content  # Extract AI response
    messages.append({"role": "assistant", "content": ai_reply})  # Store AI response

    return ai_reply  # Return AI-generated response

# =============================== #
#  AI Mode Switching Function     #
# =============================== #

def switch_mode(mode):
    """
    Switch AI mode and reset conversation history.
    """
    global current_mode
    if mode in MODE_PROMPTS:
        current_mode = mode  # Update current mode
        messages.clear()  # Clear conversation history
        messages.append({"role": "system", "content": MODE_PROMPTS[current_mode]})  # Set new system prompt
        return f"🔄 Mode switched to *{mode.capitalize()}*"
    else:
        return "⚠️ Invalid mode. Choose from: mentor, tutor, interviewer."