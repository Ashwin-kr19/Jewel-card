import json
from groq import Groq

with open("data/api_keys.json", "r") as key_file:
    api_keys = json.load(key_file)
    groq_api_key = api_keys.get("groq")

client = Groq(api_key=groq_api_key)

with open("battlecards.json", "r") as file:
    battlecards_data = json.load(file)

def ask_question_to_groq(question, battlecards_data):
    battlecards_info = json.dumps(battlecards_data, indent=2)
    
    prompt = f"""
    Here is the battlecard information for various jewelry competitors:
    {battlecards_info}
    
    Based on the above data, please answer the following question:
    {question}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        print(chat_completion)

        if chat_completion.choices and len(chat_completion.choices) > 0:
            response = chat_completion.choices[0].message.content
            return response
        else:
            return "Sorry, I couldn't fetch a valid response."

    except Exception as e:
        return f"An error occurred: {e}"

def chatbot():
    print("Welcome to the Jewelry Competitors Battlecards Bot! Ask any questions about the data.")
    while True:
        user_question = input("\nYou: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        answer = ask_question_to_groq(user_question, battlecards_data)
        print(f"Bot: {answer}")

if __name__ == "__main__":
    chatbot()
