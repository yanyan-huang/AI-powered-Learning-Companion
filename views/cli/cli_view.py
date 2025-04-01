from chatbot.controller import ChatbotController
from chatbot.model import ChatbotAIModel

class ChatbotCLIView:
    """Handles user interaction via the command line.

    This class serves as the **View** in the MVC architecture.
    It provides a CLI interface for users to interact with the chatbot.

    The **CLI View** uses the **Controller** to process user input and generate responses.
    """

    def __init__(self):
        """Initialize CLI chatbot with controller and model."""
        model = ChatbotAIModel()
        self.controller = ChatbotController(model)

    def run(self):
        """Run CLI chatbot interaction."""
        print("🎓 AI Learning Companion for Product Management")

        # Ask user to choose a mode
        mode = None
        while mode not in ["mentor", "coach", "interviewer"]:
            mode = input("Choose mode (mentor/coach/interviewer): ").strip().lower()

        print(f"🔹 Mode selected: {mode.capitalize()} mode")
        print("Type 'quit' to exit the conversation.\n")

        while True:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Exiting chat. Keep learning and growing! 🚀")
                break

            response = self.controller.process_message(user_input, mode)
            print(f"🤖 AI {mode.capitalize()}: {response}")