# LangGraph Learning Project

## Setup

### Step 1: Create `.env` file

Create a `.env` file in the project root and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key

Step 2: Create a virtual environment

Create a Python 3.12 virtual environment:

python3.12 -m venv venv

Activate the virtual environment:

source venv/bin/activate

Step 3: Install dependencies

Install the required packages:

pip install langgraph
pip install langchain
pip install streamlit
pip install python-dotenv

Step 4: Run the chatbot

The latest frontend file is:

langgraph_database_frontend.py

Run the chatbot with:

streamlit run langgraph_database_frontend.py