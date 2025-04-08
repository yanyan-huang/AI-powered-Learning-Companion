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
                model="gpt-4",
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
        llm = self.llms.get(self.provider)
        if not llm:
            return f"⚠️ Unsupported AI provider: {self.provider}", memory

        if mode not in memory:
            memory[mode] = [SystemMessage(content=MODE_PROMPTS[mode])]

        memory[mode].append(HumanMessage(content=user_input))
        try:
            response = llm(memory[mode])
            memory[mode].append(response)
            return response.content, memory
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
                prefix = "User" if msg.type == "human" else "Assistant"
                conversation_history += f"{prefix}: {msg.content}\n"

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
