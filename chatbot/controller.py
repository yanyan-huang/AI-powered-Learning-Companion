from flask import Flask, request, jsonify
from chatbot.model import ChatbotAIModel

class ChatbotController:
    """Handles interactions for the chatbot.

    This class serves as the **Controller** in the MVC architecture.
    It acts as an intermediary between:
      - The **Model (`ChatbotAIModel`)**: Handles AI processing.
      - The **View (CLI/Web App/External API Clients)**: Provides an interface for user interaction.

    This Controller can be used by different interfaces (API, Web, CLI) to process
    user input and generate responses using the AI model.
    """

    def __init__(self, model: ChatbotAIModel):
        """Initialize controller with a model instance."""
        self.model = model
        self.app = Flask(__name__)  # Initialize Flask app for API/web interfaces
        self.setup_routes()

    def setup_routes(self):
        """Define routes for handling chatbot requests."""
        @self.app.route("/chat", methods=["POST"])
        def api_chat():
            """API endpoint: Handles chatbot conversations via HTTP POST requests."""
            data = request.get_json()
            message = data.get("message", "")
            mode = data.get("mode", "mentor")

            if not message:
                return jsonify({"error": "Message is required."}), 400

            response = self.process_message(message, mode)
            return jsonify({"response": response})

    def process_message(self, message: str, mode: str = "mentor") -> str:
        """Process a message and return the AI-generated response.
        
        Args:
            message: The user's input message
            mode: The chatbot mode ('mentor', 'coach', or 'interviewer')
            
        Returns:
            str: The AI-generated response
        """
        return self.model.chat(message, mode)

    def run(self, port: int = 5000):
        """Start the Flask server."""
        self.app.run(debug=True, port=port)

# Expose the Flask app for WSGI servers like Gunicorn
app = ChatbotController(ChatbotAIModel()).app