from flask import Blueprint, request, jsonify
from crew.customer_support_crew import CustomerSupportCrew

api = Blueprint("api", __name__)

# Mock customer database
CUSTOMERS = {
    "customer1@example.com": {
        "name": "John Doe",
        "company": "Acme Corp",
        "email": "customer1@example.com"
    },
    "customer2@example.com": {
        "name": "Jane Smith",
        "company": "Globex Ltd",
        "email": "customer2@example.com"
    }
}

# Mock order database
ORDERS = {
    "ORD12345": {
        "order_id": "ORD12345",
        "status": "Shipped",
        "estimated_delivery": "2024-07-30",
        "customer_email": "customer1@example.com"
    },
    "ORD67890": {
        "order_id": "ORD67890",
        "status": "Processing",
        "estimated_delivery": "2024-08-02",
        "customer_email": "customer2@example.com"
    }
}

@api.route("/check_status", methods=["GET"])
def get_status():
    return jsonify({
        "status": "api available",
    })

@api.route("/customer", methods=["GET"])
def get_customer_details():
    """
    Fetches customer details based on email.
    Example: GET /customer?email=customer1@example.com
    """
    email = request.args.get("email")
    
    if not email:
        return jsonify({"error": "Email parameter is required"}), 400

    customer = CUSTOMERS.get(email)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

@api.route("/order", methods=["GET"])
def get_order_status():
    """
    Fetches order status based on order ID.
    Example: GET /order?order_id=ORD12345
    """
    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify({"error": "Order ID is required"}), 400

    order = ORDERS.get(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({"error": "Order not found"}), 404

@api.route("/handle_query", methods=["POST"])
def handle_query():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not all(k in data for k in ["email", "query_type", "query_value"]):
            return jsonify({"error": "Missing required fields"}), 400

        # Initialize the crew
        crew = CustomerSupportCrew()
        
        # Call the function
        response = crew.handle_customer_query(data["email"], data["query_type"], data["query_value"])

        # Return response as JSON
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500