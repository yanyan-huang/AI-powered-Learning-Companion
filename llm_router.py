from config import AI_PROVIDER, OPENAI_API_KEY, CLAUDE_API_KEY, GOOGLE_API_KEY
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
import google.generativeai as genai
from prompts import MODE_PROMPTS

# ======================== #
#  LLM Router Class       #
# ======================== #
# This class routes user queries to the appropriate LLM provider
# based on the configuration and user input.
# It manages conversation history for each mode and handles errors.
# It supports OpenAI, Claude, and Gemini.
# The class is initialized with the API keys and provider information.
# It uses the LangChain library for OpenAI and Claude, and Google Generative AI for Gemini.
# The class also includes methods for routing requests to the respective providers and managing memory.
# It raises errors if required API keys are missing or invalid.
# The class is designed to be used in a Telegram bot context, where user input is received and responses are sent back.

class LLMRouter:
    def __init__(self):
        """Initialize the LLMRouter with API keys and provider information."""
        self.provider = AI_PROVIDER.lower()
        self.llms = {
            "openai": ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                model="gpt-3.5-turbo", # 
                temperature=0
            ),
            "claude": ChatAnthropic(
                anthropic_api_key=CLAUDE_API_KEY,
                model="claude-3-7-sonnet-20250219"
            )
        }

    def get_response(self, user_id, user_input, mode, memory):
        """Route the user input to the appropriate LLM provider and return the response."""
        if not mode or mode not in MODE_PROMPTS:
            return "⚠️ Invalid or missing mode.", memory

        if self.provider == "gemini":
            return self._route_to_gemini(user_id, user_input, mode, memory)
        else:
            return self._route_to_langchain(user_id, user_input, mode, memory)

    def _route_to_langchain(self, user_id, user_input, mode, memory):
        """Route the user input to OpenAI or Claude using LangChain."""
        print("DEBUGGING in _route_to_langchain:", 
              "\nuser_id: ", user_id, "\nuser_input: ", user_input, 
              "\nmode: ", mode, "\nmemory: ", memory)
        llm = self.llms.get(self.provider)
        if not llm:
            return f"⚠️ Unsupported AI provider: {self.provider}", memory

        if mode not in memory:
            memory[mode] = [SystemMessage(content=MODE_PROMPTS[mode])]

        memory[mode].append(HumanMessage(content=user_input))
        try:
            response = llm(memory[mode])
            memory[mode].append(response)
            print("DEBUGGING: 🧠 LLM Response Type:", type(response), "Content:", extract_content(response), "Memory:", len(memory))
            return extract_content(response), memory
        except Exception as e:
            return f"❌ Error generating response: {str(e)}", memory

    def _route_to_gemini(self, user_id, user_input, mode, memory):
        """Route the user input to Gemini using Google Generative AI."""
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        system_prompt = MODE_PROMPTS[mode]

        conversation_history = ""
        if mode in memory:
            for msg in memory[mode]:
                prefix = msg["role"].capitalize()  # 'System', 'User', 'Ai'
                conversation_history += f"{prefix}: {msg['content']}\n"

        prompt = f"{system_prompt}\n\n{conversation_history}User: {user_input}"

        try:
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
        except Exception as e:
            ai_reply = f"❌ Gemini error: {str(e)}"

        if mode not in memory:
            memory[mode] = [SystemMessage(content=system_prompt)]

        memory[mode].append(HumanMessage(content=user_input))
        memory[mode].append(SystemMessage(content=ai_reply))

        return ai_reply, memory


# ==================================================================
# Safe content extractor helper: Extract LLM response content safely
# ==================================================================
def extract_content(response):
    """ 
    Ensures the bot can handle different LLM response formats gracefully.
    Why this matters:
    During inference, responses might come as:
    - dicts (e.g., from Firestore or custom wrappers)
    - LangChain Message objects with a `.content` attribute
    - raw strings (fallbacks or mocked values)

    This helper avoids runtime crashes like:
        'dict' object has no attribute 'content'
    It checks the format and returns usable content consistently.
    """
    if isinstance(response, dict):
        return response.get("content", "")
    elif hasattr(response, "content"):
        return response.content
    elif isinstance(response, str):
        return response
    return ""