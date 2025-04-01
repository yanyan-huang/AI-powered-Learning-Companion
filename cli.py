"""
CLI Entry Point for PM Pal

This module serves as the entry point for the command-line interface of the PM Pal application.
It initializes and runs the CLI interface with the ChatbotCLIView.

The CLI interface provides a text-based way to interact with the PM Pal chatbot
through the terminal, offering direct access to all chatbot features without
the overhead of a web server or API.

Usage:
    python cli.py
"""

from chatbot.cli_view import ChatbotCLIView

if __name__ == "__main__":
    # Initialize the CLI view with the chatbot model
    cli_view = ChatbotCLIView()
    
    # Run the CLI interface
    # This will start an interactive session in the terminal
    cli_view.run()