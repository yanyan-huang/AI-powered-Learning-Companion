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

from chatbot.web_view import ChatbotWebView

if __name__ == "__main__":
    # Initialize the web view with Flask application
    web_view = ChatbotWebView()
    
    # Run the Flask development server
    # debug=True enables auto-reload on code changes and detailed error messages
    # This should be disabled in production
    web_view.run(debug=True) 