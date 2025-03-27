import asyncio
import logging
import re
import requests
import nest_asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from utils.yaml_reader import YAMLReader

# Apply fix for event loop issue
nest_asyncio.apply()

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace with your actual API endpoints
CUSTOMER_API_URL = "http://localhost:5000/api/customer"  # Customer API
ORDER_API_URL = "http://localhost:5000/api/order"  # Order API
CREW_API_URL = "http://localhost:5000/api/handle_query"  # CREW API

CUSTOMER_EMAIL = 'customer1@example.com'
ORDER_ID = 'ORD12345'

# ✅ Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user  # Get user details
    # user_id = user.id
    # first_name = user.first_name
    # last_name = user.last_name if user.last_name else ""
    # username = user.username if user.username else "N/A"

    customer_data = await get_customer_details(CUSTOMER_EMAIL)

    context.user_data["customer_email"] = customer_data['email']

    response_text = f"Hello {customer_data['name']} from {customer_data['company']}! How could I be of help today?"
    await update.message.reply_text(response_text)

# ✅ Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip()
    chat_id = update.message.chat.id

    order_id = ORDER_ID
    if "order" in user_message:
        response = await query_crew(context.user_data["customer_email"], "order_status", order_id)
    elif "warranty" in user_message:
        response = await query_crew(context.user_data["customer_email"], "warranty", None)
    else:
        response = "I'm sorry, I didn't understand that. Please ask about your order or warranty."

    await update.message.reply_text(response)

async def query_crew(email: str, query_type: str, query_value: str) -> str:
    try:
        payload = {"email": email, "query_type": query_type, "query_value": query_value}
        response = requests.post(CREW_API_URL, json=payload)

        if response.status_code == 200:
            return response.json().get("response", "No response from API")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
# ✅ Fetch Customer Details from API
async def get_customer_details(identifier: str) -> dict:
    try:
        response = requests.get(f"{CUSTOMER_API_URL}?email={identifier}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Error fetching customer details: {e}")
        return None

# ✅ Fetch Order Details from API
async def get_order_details(order_id: str, customer_id: str) -> dict:
    try:
        response = requests.get(f"{ORDER_API_URL}?order_id={order_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Error fetching order details: {e}")
        return None

# ✅ Call API for Order Status
async def call_order_api(order_id: str) -> str:
    try:
        response = requests.get(f"{ORDER_API_URL}/status?order_id={order_id}")
        if response.status_code == 200:
            return response.json().get("status", "No status available")
        return "Error retrieving order status."
    except Exception as e:
        logging.error(f"Error fetching order status: {e}")
        return "An error occurred while retrieving order status."

# ✅ Main Function to Start Bot
async def main() -> None:
    config_path = '/app/agents/workflow/crew/config'
    print(f'-------config path-------- {config_path}')  # Debug print

    keys_config = YAMLReader(config_path).get_keys()
    application = ApplicationBuilder().token(keys_config['telegram_api_key']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

# ✅ Run the Bot
if __name__ == "__main__":
    asyncio.run(main())  # Now runs without errors
