
from google import genai

# 1. Connect to the AI (Replace with your actual API key)
API_KEY = "AIzaSyC35NLmD9zXzFrVsgZegmGw9pvcWiMyJMc"
client = genai.Client(api_key=API_KEY)

# 2. Initialize a continuous chat session using a fast model
chat = client.chats.create(model="gemini-3.6-flash")

print("=== AI Assistant Online (Type 'quit' to exit) ===")

# 3. Create a loop so you can keep chatting
while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == 'quit':
        print("Shutting down...")
        break
        
    # 4. Send your message to the AI and wait for the response
    try:
        response = chat.send_message(user_input)
        print(f"\nAI: {response.text}")
    except Exception as e:
        print(f"\nError connecting to the API: {e}")