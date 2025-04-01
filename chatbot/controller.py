from flask import Flask, request, jsonify # Import Flask and request modules for API handling
from chatbot.model import ChatbotAIModel

class ChatbotAPIController:
    """Handles API interactions for the chatbot.

    This class serves as the **Controller** in the MVC architecture.
    It acts as an intermediary between:
      - The **Model (`ChatbotAIModel`)**: Handles AI processing.
      - The **View (CLI/Web App/External API Clients)**: Provides an interface for user interaction.

    This Controller exposes an API interface via Flask, allowing external clients 
    (web apps, mobile apps, CLI, etc.) to interact with the chatbot.
    """

    def __init__(self):
        """Initialize Flask API and ChatbotAIModel instance."""
        self.chatbot_model = ChatbotAIModel()  # Create Model instance
        self.app = Flask(__name__)  # Initialize Flask app
        self.setup_routes()  # Define API routes

    def setup_routes(self):
        """Define API routes for handling chatbot requests.

        This method sets up an HTTP endpoint (`/chat`) for external clients to interact with the chatbot.

        Steps:
        - Accepts JSON `POST` requests with `message` (user input) and `mode` (chatbot mode).
        - Validates input parameters.
        - Calls the AI Model (`ChatbotAIModel.chat()`) to generate a response.
        - Returns the AI-generated response as a JSON object.
        """
        @self.app.route("/chat", methods=["POST"])
        def api_chat():
            """API endpoint: Handles chatbot conversations via HTTP POST requests.

            **Expected Request Format (JSON)**:
            {
                "message": "Your question here",
                "mode": "mentor"  # Can be 'mentor', 'coach', or 'interviewer'
            }

            **Response Format (JSON)**:
            {
                "response": "AI-generated response based on mode"
            }
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
        """Start the Flask API server."""
        # Run on port 5000 (default Flask port)
        self.app.run(debug=True, port=5000)

# Expose the Flask app for WSGI servers like Gunicorn
app = ChatbotAPIController().app