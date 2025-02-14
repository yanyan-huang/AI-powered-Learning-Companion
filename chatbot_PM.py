import os
from openai import OpenAI

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is missing! Set it as an environment variable.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_ai(user_input, mode, all_responses=None, assess=False):
    """AI responds based on the selected learning mode. In interview mode, it assesses responses only when the user quits."""
    
    # Define system prompts for different modes
    mode_prompts = {
        "mentor": "You are an seasoned Product Manager expert and mentor. Help mentor junior, aspring product managers, or people transitionining from other fields to design their learning path, recommend resources(courses, books, tutorials, etc), job opportunities, anything that might help them grow as to be a better product manager. Explain in a encouraging way.",
        "tutor": "You are an AI tutor for aspiring Product Managers. Answer questions in detail, simplify complex topics, and provide real-world examples.",
        "interviewer": (
            "You are a Product Manager interview coach. Your process: "
            "1) Ask the user a behavioral or case-study question. "
            "2) Wait for their response. "
            "3) Once the user finishes the interview session, assess all their responses at once. "
            "4) Provide a structured evaluation of their performance, highlighting strengths, weaknesses, and areas for improvement."
        )
    }
    
    system_prompt = mode_prompts.get(mode, "You are a helpful AI assistant who acts as a learning companion specilized in Product Management.")

    # If in interviewer mode and assessment is requested at the end, provide feedback on all responses
    if mode == "interviewer" and assess and all_responses:
        system_prompt += " Now analyze all the user's responses and provide structured feedback on their overall interview performance."

    try:
        response = client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200  # More tokens for comprehensive feedback
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("🎓 AI Learning Companion for Product Management")
    print("Modes: [1] Mentor 🧑‍🏫| [2] Tutor 📖 | [3] Mock Interview 🎤")
    
    # Select mode
    mode_selection = input("Choose a mode (1/2/3): ").strip()
    mode_map = {"1": "lecturer", "2": "tutor", "3": "interviewer"}
    mode = mode_map.get(mode_selection, "tutor")  # Default to tutor mode

    print(f"🔹 Mode selected: {mode.capitalize()} mode")
    print("Type 'quit' to exit the conversation.\n")

    all_responses = []  # Store all interview responses

    while True:
        if mode == "interviewer":
            # Step 1: Ask an interview question
            interview_question = chat_with_ai("Ask me a Product Manager interview question.", mode)
            print(f"🎤 AI Interviewer: {interview_question}")

            # Step 2: Get user response
            user_response = input("📝 Your Response: ")
            if user_response.lower() in ["quit", "exit", "bye"]:
                if mode == "interviewer" and all_responses:
                    print("\n📊 Analyzing your interview performance... Please wait...\n")
                
                    # Step 3: AI evaluates all interview responses
                    combined_responses = "\n".join(all_responses)
                    evaluation = chat_with_ai(combined_responses, mode, all_responses=True, assess=True)
                    print(f"✅ AI Feedback: {evaluation}")
                
                print("Exiting conversation. Keep learning, practicing, and improving! 🚀")
                break

            # Step 4: Store response and continue the interview
            all_responses.append(f"User Response: {user_response}")
        
        else:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Exiting chat. Keep learning and growing! 🚀")
                break

            response = chat_with_ai(user_input, mode)
            print(f"🤖 AI Mentor: {response}")
