"""
API Entry Point for PM Pal

This module serves as the entry point for the RESTful API of the PM Pal application.
It initializes and runs the Flask API server with the ChatbotAPIController.

The API interface provides programmatic access to the PM Pal chatbot's functionality,
allowing other applications to integrate with it through HTTP endpoints.

Usage:
    python api.py
"""

from chatbot.controller import ChatbotAPIController

if __name__ == "__main__":
    # Initialize the API controller with Flask application
    controller = ChatbotAPIController()
    
    # Run the Flask API server
    # This is the production-ready entry point for the API
    controller.run()