"""
Web Interface Entry Point for PM Pal

This module serves as the entry point for the web interface of the PM Pal application.
It initializes and runs the Flask web server with the ChatbotWebView.

The web interface provides a user-friendly way to interact with the PM Pal chatbot
through a browser, offering the same functionality as the CLI interface but with
a graphical user interface.

Usage:
    python web.py
"""

from chatbot.controller import ChatbotController
from chatbot.model import ChatbotAIModel
from views.web.web_view import ChatbotWebView

def main():
    # Initialize MVC components
    model = ChatbotAIModel()
    controller = ChatbotController(model)
    view = ChatbotWebView(controller)
    
    # Run the web interface
    view.run()

if __name__ == "__main__":
    main() 