Step 1: Create .env file

Create a .env file in the project root and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key
Step 2: Create a virtual environment

Create a Python 3.12 virtual environment:

python3.12 -m venv venv

Activate it:

source venv/bin/activate
Step 3: Install dependencies

Install the required packages:

pip install langgraph
pip install langchain
pip install streamlit
pip install python-dotenv

python-dotenv is used because the code loads environment variables with from dotenv import load_dotenv.

Step 4: Run the chatbot

The latest frontend file is:

langgraph_database_frontend.py

Run it with:

streamlit run langgraph_database_frontend.py