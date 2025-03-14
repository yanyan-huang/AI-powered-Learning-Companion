from chatbot.controller import ChatbotAPIController

if __name__ == "__main__":
    """Flask API Entry Point"""
    controller = ChatbotAPIController()
    controller.run()