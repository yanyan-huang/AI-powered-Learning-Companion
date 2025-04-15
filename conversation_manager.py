from langchain.schema import SystemMessage
from prompts import MODE_PROMPTS
from config import WHITELISTED_USER_IDS
# ======================== #
#  Conversation Manager    #
# ======================== #
# This class manages the conversation between the user and the AI.
# It handles switching modes, processing user input, and interacting with the LLM router.
# It manages the user's memory and logs interactions.
# It uses the BotUser class to manage user data and the LLMRouter class to route requests to the appropriate AI provider.
# It raises errors if required API keys are missing or invalid.
# It is designed to be used in a Telegram bot context, where user input is received and responses are sent back.
# It provides methods for switching modes and processing user input.
# It is initialized with a BotUser instance and an LLMRouter instance.
# It handles the conversation flow and manages the user's memory.
# It raises errors if the user ID is invalid or if there are issues with file operations.
# It provides methods for getting and updating memory, logging interactions, and managing the user's mode.  

class ConversationManager:
    def __init__(self, bot_user, llm_router):
        self.user = bot_user
        self.router = llm_router

    def switch_mode(self, new_mode):
        if new_mode in MODE_PROMPTS:
            self.user.mode = new_mode
            memory = self.user.get_memory()
            memory[new_mode] = [SystemMessage(content=MODE_PROMPTS[new_mode])]
            self.user.update_memory(new_mode, memory)
            return f"🔄 Mode switched to *{new_mode.capitalize()}*. Previous conversation cleared."
        else:
            return "⚠️ Invalid mode. Choose `/mode mentor`, `/mode coach`, or `/mode interviewer`."

    def process_input(self, user_input, source="text"):
        if str(self.user.user_id) not in WHITELISTED_USER_IDS:
            if self.user.get_llm_usage_count() >= 8:
                return (
                    "🧪 You’ve used your 8 free AI responses.\n\n"
                    "Want more access or to help shape PM Pal? "
                    "Contact us at huang.yva@gmail.com or DM @yvayvaine on Telegram.\n\n"
                    "Thanks for trying the beta! 🚀"
                )
            
        mode = self.user.mode
        memory = self.user.get_memory()
        ai_reply, updated_memory = self.router.get_response(self.user.user_id, user_input, mode, memory)
        self.user.update_memory(mode, updated_memory)
        self.user.log_interaction(user_input, ai_reply, source=source)

        # ✅ Add this line to log a metric event
        self.user.log_metric_event()      
        
        self.user.increment_llm_usage_count() # Increment usage count for LLM - ai response

        return ai_reply
