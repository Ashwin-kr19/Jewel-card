# Jewellers Competitor Battlecards

This project focuses on generating detailed and organized battlecards for competitors in the jewelry industry. It leverages competitor data, market trends, and insights to create professional, actionable battlecards. Additionally, the project includes a question-answering chatbot that can provide users with information from the battlecards via a conversational interface. The solution is implemented as a **Streamlit app**.

## Key Features

1. **Competitor Battlecards**:
   - Extracts data from **NewsAPI** to analyze competitor news articles.
   - Clusters data to categorize competitors based on various factors.
   - Generates a comprehensive **battlecard** for each competitor, including:
     - Competitor overview
     - Products
     - Market trends
     - Strengths and weaknesses
   - Customizable templates for battlecards (Modern, Classic, Professional) with distinct color schemes and text formatting.

2. **Conversational Bot**:
   - Integrated **question-answering bot** using Groq LLM.
   - Reads from `battlecards.json` to answer user questions related to competitor data.
   - Supports multi-turn conversations, allowing users to ask multiple questions in the same text box.

3. **Streamlit Application**:
   - Provides a user-friendly interface for generating and viewing battlecards.
   - Includes a chatbot page where users can query competitor information interactively.
   - Premium design for chatbot page with enhanced user experience.

## Workflow

### 1. Data Extraction:
   - Fetch competitor data using **NewsAPI** to gather relevant articles and updates.
   - Preprocess and clean the fetched data for clustering and analysis.

### 2. Data Clustering:
   - Use clustering algorithms to group competitors based on market activity, product categories, or other factors.
   - Store the clustered data in `battlecards.json`.

### 3. Battlecards Generation:
   - Based on the clustered data, generate comprehensive battlecards for each competitor.
   - Battlecards include:
     - Company overview and major products.
     - Analysis of market trends.
     - Strengths, weaknesses, opportunities, and threats (SWOT).
   - Choose from **Modern**, **Classic**, or **Professional** templates for presentation.

### 4. Conversational Bot Integration:
   - Load the generated `battlecards.json` file.
   - Users can interact with the bot through a conversational interface to query details about any competitor.
   - The bot leverages **Groq LLM** for natural language understanding and multi-turn interactions.

### 5. Streamlit App:
   - The Streamlit app serves as the front-end interface for users to:
     - View and generate competitor battlecards.
     - Use the chatbot to retrieve competitor insights.
   - Includes a premium, user-friendly design for the chatbot page with conversational flow.

### 6. PDF Generation:
   - Use **ReportLab** to export the battlecards to a PDF format.
   - Customize the layout, colors, and formatting based on the chosen template.



## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Groq LLM, ReportLab
- **Data**: NewsAPI, Competitor data in JSON format
- **Deployment**: Streamlit cloud or local server

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/battlecards-generator.git
    cd battlecards-generator
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

## Usage

- Open the Streamlit app in your browser.
- Input relevant competitor details or let the app fetch data using NewsAPI.
- Generate and view battlecards with customizable templates.
- Navigate to the chatbot page to ask questions about competitors using the question-answering bot.

## Customization

- You can customize battlecard templates (Modern, Classic, Professional) by editing the `templates/` folder.
- To add more features or adjust the bot's responses, modify the `chat.py` script.
