"""
CLI Entry Point for PM Pal

This module serves as the entry point for the command-line interface of the PM Pal application.
It initializes and runs the CLI interface with the ChatbotCLIView.

The CLI interface provides a text-based way to interact with the PM Pal chatbot
through the terminal, offering direct access to all chatbot features without
the overhead of a web server or API.
"""

from chatbot.controller import ChatbotController
from chatbot.model import ChatbotModel
from views.cli.cli_view import ChatbotCLIView

def main():
    # Initialize MVC components
    model = ChatbotModel()
    controller = ChatbotController(model)
    view = ChatbotCLIView(controller)
    
    # Run the CLI interface
    view.run()

if __name__ == "__main__":
    main()