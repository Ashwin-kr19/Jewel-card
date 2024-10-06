import json
from groq import Groq

# Load API key from the data/api_keys.json file
with open("data/api_keys.json", "r") as key_file:
    api_keys = json.load(key_file)
    groq_api_key = api_keys.get("groq")

# Initialize the Groq client with the extracted API key
client = Groq(api_key=groq_api_key)

# Load the battlecards.json file
with open("battlecards.json", "r") as file:
    battlecards_data = json.load(file)

# Define a function to handle user questions
def ask_question_to_groq(question, battlecards_data):
    # Format the battlecards data to provide context for Groq
    battlecards_info = json.dumps(battlecards_data, indent=2)
    
    # Create a prompt that combines the battlecard info and user question
    prompt = f"""
    Here is the battlecard information for various jewelry competitors:
    {battlecards_info}
    
    Based on the above data, please answer the following question:
    {question}
    """

    try:
        # Call the Groq API to get a response
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        # Print the full response for debugging purposes
        print(chat_completion)

        # Extract and return the response content safely using attributes
        if chat_completion.choices and len(chat_completion.choices) > 0:
            # Access the content as an attribute
            response = chat_completion.choices[0].message.content
            return response
        else:
            return "Sorry, I couldn't fetch a valid response."

    except Exception as e:
        return f"An error occurred: {e}"

# Main interaction loop for the bot
def chatbot():
    print("Welcome to the Jewelry Competitors Battlecards Bot! Ask any questions about the data.")
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        # Pass the user question and battlecards data to the function
        answer = ask_question_to_groq(user_question, battlecards_data)
        print(f"Bot: {answer}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()