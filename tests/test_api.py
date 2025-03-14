import requests

# Define API URL
API_URL = "http://127.0.0.1:5000/chat"
headers = {"Content-Type": "application/json"}

# Define test cases for all three chatbot modes
test_cases = [
    {"message": "How do I transition into a PM role?", "mode": "mentor"},
    {"message": "Can you coach me to do a PM case study?", "mode": "coach"},
    {"message": "Can you give me a PM interview question?", "mode": "interviewer"},
]

# Loop through test cases and send POST requests
for test in test_cases:
    response = requests.post(API_URL, json=test, headers=headers)
    
    # Print the results
    print(f"\n🔹 Mode: {test['mode'].capitalize()}")
    print(f"💬 User: {test['message']}")
    print(f"🤖 AI: {response.json().get('response', 'Error: No response received')}")