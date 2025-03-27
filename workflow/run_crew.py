#!/usr/bin/env python
# src/my_project/main.py
import sys
from crew.research_crew import CustomCrew
from crew.customer_support_crew import CustomerSupportCrew

from utils.yaml_reader import YAMLReader
import os

import json

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI Agents'
    }
    # config = YAMLReader('config').get_keys()
    CustomCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    crew = CustomerSupportCrew()
    email = "customer1@example.com"
    query_type = "warranty"  # "order_status", "warranty", or "general"
    query_value = "ORD12345"  # Order ID for order queries

    response = crew.handle_customer_query(email, query_type, query_value)
    json_output = json.dumps({"response": response}, indent=4)
    print(json_output)

    #run()