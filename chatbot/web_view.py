from flask import Flask, render_template, request, jsonify
from chatbot.model import ChatbotAIModel
import os

class ChatbotWebView:
    """Handles user interaction via a web interface.

    This class serves as the **View** in the MVC architecture for web-based interactions.
    It provides a web interface for users to interact with the chatbot using Flask.
    """

    def __init__(self):
        """Initialize web chatbot with Flask and AI model."""
        # Get the absolute path to the templates directory
        template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
        self.app = Flask(__name__, template_folder=template_dir)
        self.chatbot_model = ChatbotAIModel()
        self.setup_routes()

    def setup_routes(self):
        """Set up Flask routes for the web interface."""
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/chat', methods=['POST'])
        def chat():
            data = request.json
            user_message = data.get('message', '')
            mode = data.get('mode', 'mentor')  # Default to mentor mode if not specified
            
            if not user_message:
                return jsonify({'response': 'Please provide a message.'})
            
            try:
                response = self.chatbot_model.chat(user_message, mode)
                return jsonify({'response': response})
            except Exception as e:
                return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

    def run(self, debug=True):
        """Run the Flask web application."""
        # Run on port 5001 to avoid conflicts with API
        self.app.run(debug=debug, port=5001) 