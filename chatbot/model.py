import os # Import the os module to access environment variables.
from openai import OpenAI

class ChatbotAIModel:
    """Handles AI interactions using OpenAI API.

    This class serves as the **Model** in the MVC architecture.
    It processes user input and generates AI-based responses using predefined learning modes.
    
    It does NOT handle user interactions directly (CLI or API).
    """

    def __init__(self):
        """Initialize chatbot with API key and predefined modes."""
        self.api_key = os.getenv("OPENAI_API_KEY")

        # Ensure API key is set, otherwise raise an error.
        if not self.api_key:
            raise ValueError("⚠️ OPENAI_API_KEY is missing! Set it as an environment variable.")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        # Define system prompts for different chatbot modes
        self.modes = {
            "mentor": "You are a seasoned Product Manager mentor. Provide career guidance.",
            "coach": "You are an AI coach for aspiring PMs. Answer questions with real-world examples.",
            "interviewer": "You are a PM interviewer. Ask interview questions, then assess performance."
        }

    def chat(self, user_input, mode):
        """Generates AI response based on the selected learning mode.

        - Validates the mode input to ensure it's a supported category.
        - Sends the request to OpenAI API with an appropriate system prompt.
        - Returns an AI-generated response.
        - Catches and returns errors if API fails.
        """

        # Validate mode
        if mode not in self.modes:
            return "Error: Invalid mode selected. Please choose 'mentor', 'coach', or 'interviewer'."

        system_prompt = self.modes[mode]

        try:
            # Call OpenAI API to generate a response
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content  # Return AI response
        except Exception as e:
            return f"⚠️ API Error: {e}"  # Handle errors properly