import os
from openai import OpenAI
from flask import Flask, request, jsonify

# ========================= #
#  Model - AI Processing   #
# ========================= #
class ChatbotModel:
    """Handles AI interactions using OpenAI API.
    This class serves as the Model in the MVC architecture.
    It is responsible for processing user input and generating
    AI-based responses using predefined learning modes.
    It does not interact directly with users or handle HTTP requests.
    """
    def __init__(self):
        """Initialize chatbot with API key and predefined modes."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ OPENAI_API_KEY is missing! Set it as an environment variable.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
        
        # Define system prompts for different modes
        self.modes = {
            "mentor": "You are a seasoned Product Manager mentor. Provide career guidance, learning resources, and job insights.",
            "coach": "You are an AI coach for aspiring Product Managers. Answer questions clearly with real-world examples and guide users through learning processes.",
            "interviewer": "You are a Product Manager interviewer. Ask PM interview questions, then assess performance after completion."
        }
    
    def chat(self, user_input, mode):
        """Generates AI response based on the selected learning mode.
        This function communicates with the OpenAI API and returns
        an AI-generated response.
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
            return f"Error: {e}"

# ========================= #
#  Controller - API Layer   #
# ========================= #
class ChatbotController:
    """Handles API interactions for the chatbot.
    This class serves as the Controller in the MVC architecture.
    It acts as an intermediary between the Model and external clients
    (such as the CLI or Web UI), exposing an API interface via Flask.
    """
    def __init__(self):
        """Initialize Flask API and ChatbotModel instance."""
        self.chatbot_model = ChatbotModel()  # Create an instance of ChatbotModel
        self.app = Flask(__name__)  # Initialize Flask app
        self.setup_routes()  # Define API routes
    
    def setup_routes(self):
        """Define API routes for handling chatbot requests.
        This method sets up an HTTP endpoint for external clients to interact with the chatbot.
        It allows requests to be sent to `/chat`, which is processed and forwarded
        to the AI model for generating responses.
        """
        @self.app.route("/chat", methods=["POST"])
        def api_chat():
            """API endpoint to interact with AI.
            This function:
            - Extracts the `message` and `mode` parameters from the incoming JSON request.
            - Validates the input to ensure `mode` is provided.
            - Calls the AI Model (`ChatbotModel.chat()`) to generate a response.
            - Returns the AI-generated response as a JSON object.
            """
            data = request.json  # Get JSON data from the request
            user_input = data.get("message")  # Extract user message
            mode = data.get("mode")  # Extract the AI mode
            
            # Validate mode to prevent errors in AI processing
            if not mode:
                return jsonify({"error": "Mode is required. Please specify 'mentor', 'coach', or 'interviewer'."}), 400
            
            response = self.chatbot_model.chat(user_input, mode)  # Call AI model function
            return jsonify({"response": response})  # Return response as JSON
    
    def run(self):
        """Start the Flask API server.
        Runs the Flask application and listens for incoming API requests.
        This function ensures that the chatbot can be accessed by external clients.
        """
        self.app.run(debug=True)
        # self.app.run(host="0.0.0.0", port=8080, debug=True)  # Change port from 5000 to 8080 for debugging

# ========================= #
#  View - CLI Interaction  #
# ========================= #
class ChatbotView:
    """Handles user interaction via the command line.
    This class serves as the View in the MVC architecture.
    It provides a CLI interface for users to interact with the chatbot
    and receive AI-generated responses. It calls the Controller
    to process input and display output.
    """
    def __init__(self):
        """Initialize CLI with ChatbotModel instance."""
        self.chatbot_model = ChatbotModel()  # Create an instance of ChatbotModel
    
    def run(self):
        """Run CLI chatbot interaction.
        Prompts the user to choose a mode and engages in a text-based conversation
        with the AI chatbot.
        """
        print("🎓 AI Learning Companion for Product Management")
        
        # Ask user to choose a mode
        while True:
            print("Modes: [1] Mentor 🧑‍🏫 | [2] Coach 📖 | [3] Mock Interview 🎤")
            mode_selection = input("Choose a mode (1/2/3): ").strip()
            mode_map = {"1": "mentor", "2": "coach", "3": "interviewer"}
            mode = mode_map.get(mode_selection)
            
            if mode:
                break
            else:
                print("⚠️ Invalid mode selected. Please choose 1, 2, or 3.")
        
        print(f"🔹 Mode selected: {mode.capitalize()} mode")
        print("\n💬 Type your message or 'quit' to exit.\n")
        
        # Main loop for user interaction
        while True:
            user_input = input("User: ")  # Get user input
            if user_input.lower() in ["quit", "exit", "bye"]:  # Exit condition
                print("Exiting chat. Keep learning and growing! 🚀")
                break
            
            response = self.chatbot_model.chat(user_input, mode)  # Get AI response from Model
            print(f"🤖 AI {mode.capitalize()}: {response}")

# ========================= #
#  Entry Point - Run App   #
# ========================= #
if __name__ == "__main__":
    """Main entry point of the application.
    - First, it initializes and starts the CLI chatbot interaction.
    - Once the CLI session ends, it initializes and starts the controller (Flask API server).
    """
    cli = ChatbotView()  # Initialize CLI chatbot view
    cli.run()  # Start CLI interaction
    
    controller = ChatbotController()  # Initialize Controller (Flask API server)
    controller.run()  # Start Flask server