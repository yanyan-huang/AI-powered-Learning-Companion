"""
API Entry Point for PM Pal

This module serves as the entry point for the RESTful API of the PM Pal application.
It initializes and runs the Flask API server with the ChatbotController.

The API provides programmatic access to the PM Pal chatbot's functionality,
allowing integration with other applications and services.
"""

from chatbot.controller import ChatbotController
from chatbot.model import ChatbotModel

def create_app():
    # Initialize MVC components
    model = ChatbotModel()
    controller = ChatbotController(model)
    
    # Create and configure the Flask application
    app = controller.app
    
    return app

app = create_app()

if __name__ == "__main__":
    # Run the Flask development server
    # debug=True enables auto-reload on code changes and detailed error messages
    # This should be disabled in production
    app.run(debug=True)