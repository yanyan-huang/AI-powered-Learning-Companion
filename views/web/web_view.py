"""
Web View Implementation for PM Pal

This module implements the web interface for the PM Pal application using Flask.
It provides a user-friendly way to interact with the chatbot through a browser.
"""

import os
from flask import Flask, render_template, request, jsonify
from chatbot.controller import ChatbotController

class ChatbotWebView:
    def __init__(self, controller: ChatbotController):
        self.controller = controller
        self.app = Flask(__name__, 
                        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                        static_folder=os.path.join(os.path.dirname(__file__), 'static'))
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/chat', methods=['POST'])
        def chat():
            data = request.get_json()
            message = data.get('message', '')
            mode = data.get('mode', 'mentor')
            
            response = self.controller.process_message(message, mode)
            return jsonify({'response': response})

    def run(self, debug=True):
        # Run on port 5001 to avoid conflicts with API (which uses 5000)
        self.app.run(debug=debug, port=5001) 