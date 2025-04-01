"""
Web View Implementation for PM Pal

This module implements the web interface for the PM Pal application using Flask.
It provides a user-friendly way to interact with the chatbot through a browser.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from chatbot.controller import ChatbotController

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotWebView:
    def __init__(self, controller: ChatbotController):
        self.app = Flask(__name__)
        self.controller = controller
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                message = data.get('message')
                mode = data.get('mode', 'mentor')
                
                if not message:
                    return jsonify({'error': 'No message provided'}), 400
                
                logger.info(f"Processing message in {mode} mode: {message}")
                response = self.controller.process_message(message, mode)
                logger.info(f"Generated response: {response[:100]}...")
                
                return jsonify({'response': response})
            except Exception as e:
                logger.error(f"Error in chat endpoint: {str(e)}")
                return jsonify({'error': str(e)}), 500

    def run(self, host='0.0.0.0', port=5001, debug=True):
        logger.info(f"Starting server on port {port}")
        self.app.run(host=host, port=port, debug=debug) 