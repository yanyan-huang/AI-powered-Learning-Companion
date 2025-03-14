from chatbot.controller import app

# ========================= #
#  WSGI Entry Point        #
# ========================= #
"""
This file serves as the Web Server Gateway Interface (WSGI) entry point for the Flask application.

Purpose:
- Used in production environments to launch the Flask API via a WSGI server such as Gunicorn or uWSGI.
- Ensures separation of concerns by keeping the Flask app declaration (`app`) separate from the execution logic.
- Allows Flask to be started using a command like:
  gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

Why WSGI?
- Flask’s built-in server (`app.run()`) is not suitable for production because it is single-threaded and lacks performance optimizations.
- WSGI servers (e.g., Gunicorn) can handle multiple concurrent requests efficiently.
- This approach simplifies deployment in environments such as Docker, AWS, DigitalOcean, or other cloud platforms.

Usage:
- For development, we can continue using `python3 app.py` (or a similar entry point).
- For production, start the application with a command like:
  gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

if __name__ == "__main__":
    # Run the Flask application using the built-in server.
    # Note: This is NOT recommended for production; use a WSGI server like Gunicorn instead.
    app.run()