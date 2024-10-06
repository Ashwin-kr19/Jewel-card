import streamlit as st
import os
import json
from data_collection import collect_data
from data_analysis import analyze_data
from battlecard_generation import generate_battlecards
from battlecard_design import design_battlecards, TEMPLATES
from chat import ask_question_to_groq

def add_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700&family=Roboto:wght@300;400;500&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f7f9fc;
            color: #333;
        }
        .stButton button {
            background-color: #009973;
            color: white;
            font-weight: 500;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 16px;
            transition: all 0.3s ease-in-out;
        }
        .stButton button:hover {
            background-color: #1B6CA8;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            font-size: 15px;
            border-radius: 5px;
            border: 2px solid #00e6ac;
        }
        h1, h2, h3 {
            font-family: 'Montserrat', sans-serif;
            color: #00cc99;
        }
        .sidebar .sidebar-content {
            background-color: #1B6CA8;
        }
        .sidebar .sidebar-content h2 {
            font-size: 24px;
            color: white;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content label {
            color: white;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to clear old battlecards
def clear_old_battlecards():
    battlecards_dir = 'battlecards'
    if os.path.exists(battlecards_dir):
        for file in os.listdir(battlecards_dir):
            os.remove(os.path.join(battlecards_dir, file))

# Function to handle the 'Collect, Analyze, and Generate Battlecards' page
def show_collect_analyze_generate_page():
    st.title("Jewellers Gen-Battlecard")

    st.write(
        """
        Welcome to the Jewellers Battlecard Generator! This application helps you to:
        
        1. **Collect Data**: Input jeweller names and industry keywords to gather relevant data.
        2. **Analyze Data**: Process and analyze the collected data to derive insights.
        3. **Generate Battlecards**: Create detailed battlecards based on the analysis.
        """
    )

    st.markdown("### Instructions:")
    st.write(
        """
        - **Enter Jewellers Names**: Provide a comma-separated list of Jewellers names. E.g., `Tanishq, Malabar Gold and Diamonds`.
        - **Enter Industry Keywords**: Provide a comma-separated list of industry keywords relevant to your analysis.
        """
    )

    # Collect user inputs
    jewellers_names = st.text_input("Enter Jewellers names (comma-separated):")
    industry_keywords = st.text_input("Enter industry keywords (comma-separated):")

    if st.button("Process Data"):
        if jewellers_names and industry_keywords:
            jewellers_names_list = [name.strip() for name in jewellers_names.split(",")]
            industry_keywords_list = [keyword.strip() for keyword in industry_keywords.split(",")]

            clear_old_battlecards()
            collect_data(jewellers_names_list, industry_keywords_list)
            analyze_data()
            generate_battlecards()

            st.success("Data collected, analyzed, and battlecards generated successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to handle the 'Design Battlecards' page
def show_design_battlecards_page():
    st.title("Design Battlecards")

    st.write(
        """
        After generating the battlecards, customize their appearance.
        """
    )

    selected_template = st.selectbox("Select Template", options=list(TEMPLATES.keys()))

    if st.button("Design Battlecards"):
        design_battlecards(template_name=selected_template)
        st.success("Battlecards designed successfully!")

        st.write("Download the generated battlecards:")
        for file in os.listdir('battlecards'):
            if file.endswith('.pdf'):
                st.download_button(
                    label=f"Download {file}",
                    data=open(os.path.join('battlecards', file), 'rb').read(),
                    file_name=file
                )

# Function to handle the 'Chat with Battlecard Bot' page
def show_chatbot_page():
    st.title("Chat with the Battlecard Bot")

    st.write(
        """
        Ask questions about the battlecards, and the bot will provide answers.
        """
    )

    # Initialize session state for chat history and input
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'input_question' not in st.session_state:
        st.session_state.input_question = ""

    # Display previous chat history
    st.write("---")  # Line separator before chat starts
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")
        st.write("<hr>", unsafe_allow_html=True)  

    # Function to clear input after submission
    def submit_question():
        if st.session_state.input_question:
            with open("battlecards.json", "r") as file:
                battlecards_data = json.load(file)

            answer = ask_question_to_groq(st.session_state.input_question, battlecards_data)
            st.session_state.chat_history.append({"user": st.session_state.input_question, "bot": answer})

            # Clear the input question field after asking
            st.session_state.input_question = ""

    st.text_input("Ask a question about the battlecards:", key="input_question", on_change=submit_question)

def main():
    add_custom_css()  
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ["Collect, Analyze, and Generate Battlecards", "Design Battlecards", "Chat with Battlecard Bot"])

    if page == "Collect, Analyze, and Generate Battlecards":
        show_collect_analyze_generate_page()
    elif page == "Design Battlecards":
        show_design_battlecards_page()
    elif page == "Chat with Battlecard Bot":
        show_chatbot_page()

if __name__ == "__main__":
    main()
