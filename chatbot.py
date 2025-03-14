# ========================= #
#  Model - AI Logic         #
# ========================= #
import os
from openai import OpenAI

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is missing! Set it as an environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_ai(user_input, mode):
    """AI responds based on the selected learning mode."""
    mode_prompts = {
        "mentor": "You are a seasoned Product Manager mentor. Provide career guidance, learning resources, and job insights.",
        "tutor": "You are an AI tutor for aspiring Product Managers. Answer questions clearly with real-world examples.",
        "interviewer": "You are a PM interview coach. Ask case-study questions, then assess performance after completion."
    }
    
    system_prompt = mode_prompts.get(mode, "You are an AI assistant specialized in Product Management.")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ========================= #
#  Controller - API Layer   #
# ========================= #
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def api_chat():
    data = request.json
    user_input = data.get("message")
    mode = data.get("mode", "tutor")
    response = chat_with_ai(user_input, mode)
    return jsonify({"response": response})

# ========================= #
#  View - CLI Interaction  #
# ========================= #
if __name__ == "__main__":
    print("🎓 AI Learning Companion for Product Management")
    print("Modes: [1] Mentor 🧑‍🏫| [2] Tutor 📖 | [3] Mock Interview 🎤")
    
    mode_selection = input("Choose a mode (1/2/3): ").strip()
    mode_map = {"1": "mentor", "2": "tutor", "3": "interviewer"}
    mode = mode_map.get(mode_selection, "tutor")
    
    print(f"🔹 Mode selected: {mode.capitalize()} mode")
    print("Type 'quit' to exit the conversation.\n")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Exiting chat. Keep learning and growing! 🚀")
            break
        response = chat_with_ai(user_input, mode)
        print(f"🤖 AI Mentor: {response}")
    
    # Run the API if executing the script
    app.run(debug=True)