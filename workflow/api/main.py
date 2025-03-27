from flask import Flask
from routes import api
import os

app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    '''
    # Initialize the reader with your config directory
    reader = YAMLReader('config')

    # Read tasks
    tasks = reader.get_tasks()
    if tasks:
        for task_name, task_config in tasks.items():
            print(f"Task: {task_name}")
            print(f"Description: {task_config['description']}")

    # Read agents
    agents = reader.get_agents()
    if agents:
        for agent_name, agent_config in agents.items():
            print(f"Agent: {agent_name}")
    '''
    
    app.run(debug=True)
