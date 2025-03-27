from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool
import requests
from utils.yaml_reader import YAMLReader
import os

class CustomerSupportCrew:
    def __init__(self):
        self.config_path = '/app/agents/workflow/crew/config'
        print(f'-------config path-------- {self.config_path}')  # Debug print

        self.agents_config = YAMLReader(self.config_path).get_agents()
        self.tasks_config = YAMLReader(self.config_path).get_tasks()
        self.keys_config = YAMLReader(self.config_path).get_keys()
        self.properties_config = YAMLReader(self.config_path).get_properties()

        openai_api_key = self.keys_config['open_api_key']
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
        os.environ["OPENAI_API_KEY"] = openai_api_key

        serper_api_key = self.keys_config['serper_api_key']
        os.environ["SERPER_API_KEY"] = serper_api_key

        print(f'------------------open api key----------------:{openai_api_key}')

        # Tool: Scrapes warranty terms dynamically from the webpage
        self.docs_scrape_tool = ScrapeWebsiteTool(
            website_url=self.properties_config['product_tnc_url']
        )

        # Create agents
        self.support_agent = Agent(
            role=self.agents_config['ssr']['role'],
            goal=self.agents_config['ssr']['goal'],
            backstory=self.agents_config['ssr']['backstory'],  # Fixed (no parentheses)
            allow_delegation=True,  # Allows delegation to QA agent
            verbose=True
        )

        self.support_quality_assurance_agent = Agent(
            role=self.agents_config['sqar']['role'],
            goal=self.agents_config['sqar']['goal'],
            backstory=self.agents_config['sqar']['backstory'],  # Fixed (no parentheses)
            verbose=True
        )

        # Create tasks
        self.inquiry_resolution = Task(
            description=self.tasks_config['ssr']['description'],  # ✅ Now it's a string
            expected_output=self.tasks_config['ssr']['expected_output'],  # ✅ Now it's a string
            tools=[self.docs_scrape_tool],
            agent=self.support_agent,
        )

        self.quality_assurance_review = Task(
            description=self.tasks_config['sqar']['description'],  # ✅ Fixed
            expected_output=self.tasks_config['sqar']['expected_output'],  # ✅ Fixed
            agent=self.support_quality_assurance_agent,
        )

        # Create crew
        self.support_crew = Crew(
            agents=[self.support_agent, self.support_quality_assurance_agent],
            tasks=[self.inquiry_resolution, self.quality_assurance_review]
        )

    # Handling Customer Queries
    def handle_customer_query(self, email, query_type, query_value=None):
        customer = self.get_customer_details(email)
        if not customer:
            return "Customer not found."

        greeting = f"Hello {customer['name']} from {customer['company']}!"

        if query_type == "order_status":
            order_status = self.get_order_status(query_value)
            if order_status:
                return f"{greeting} Your order ({query_value}) status is: {order_status}."
            else:
                return f"{greeting} Unfortunately, we couldn't find your order. Please check the order ID and try again."

        elif query_type == "warranty":
            response = self.support_crew.kickoff(inputs={"customer": customer["name"], "person": customer["name"], "inquiry": "Warranty details"})
            return f"{greeting} {response}".replace('[Your Name]', self.agents_config['global_agent_name']).replace('[Your Position]', 'Customer Support 24x7')

        else:
            response = self.support_crew.kickoff(inputs={"customer": customer["name"], "inquiry": query_value})
            return f"{greeting} {response}"

    # Fetch Customer Details
    def get_customer_details(self, email):
        response = requests.get(f"{self.properties_config['customer_api']}?email={email}")
        return response.json() if response.status_code == 200 else None

    # Fetch Order Status
    def get_order_status(self, order_id):
        response = requests.get(f"{self.properties_config['order_api']}?order_id={order_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get('status', 'Status not available')
        return None  # Order not found
