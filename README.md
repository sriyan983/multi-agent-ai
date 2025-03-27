📌 Multi Agent AI Crew

A chatbot integrated with Telegram that fetches customer and order details using APIs. It utilizes OpenAI for responses and Serper for search functionalities.

🚀 Setup Instructions

1️⃣ Prerequisites

Python 3.10+

pip (Python package manager)

A Telegram Bot Token

API keys for OpenAI and Serper

2️⃣ Clone the Repository

git clone https://github.com/your-repo.git
cd your-repo

3️⃣ Install Dependencies

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install required dependencies:

pip install -r requirements.txt

4️⃣ Configure API Keys

Fill in the key.yaml file with your API keys:

openai_key: "your-openai-api-key"
serper_key: "your-serper-api-key"
telegram_bot_token: "your-telegram-bot-token"

5️⃣ Run the API Server

FLASK_APP=api/main.py flask run --host=0.0.0.0 --port=5000

This will start the API server on http://localhost:5000.

6️⃣ Run the Telegram Bot

python telegram_bot.py

This will start the Telegram bot, which will respond to messages.

🛠 Features

Retrieves customer details using email from Telegram messages.

Fetches order details and confirms with the customer.

Integrates OpenAI for response generation.

Uses Serper for additional search functionalities.

📄 API Endpoints

POST /handle_query

Handles customer queries by retrieving order details.

Request Body:

{
  "email": "customer@example.com",
  "query_type": "order_status",
  "query_value": "ORDER123"
}

Response:

{
  "response": "Your order ORDER123 is shipped."
}

📝 License

This project is licensed under MIT License.
