# src/my_project/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from utils.yaml_reader import YAMLReader
import os

@CrewBase
class CustomCrew():
    
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config= self.agents_config['researcher'],
			verbose=True,
			tools=[SerperDevTool()]
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		
		print('------test-----')
		
		config_path = '/app/agents/workflow/crew/config'
		print(f'-------config path-------- {config_path}')  # Debug print

		self.agents_config = YAMLReader(config_path).get_agents()
		self.tasks_config = YAMLReader(config_path).get_tasks()
		self.keys_config = YAMLReader(config_path).get_keys()		

		openai_api_key = self.keys_config['open_api_key'];
		os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
		os.environ["OPENAI_API_KEY"] = openai_api_key

		serper_api_key = self.keys_config['serper_api_key'];
		os.environ["SERPER_API_KEY"] = serper_api_key

		print(f'------------------open api key----------------:{openai_api_key}')
		# print(f'serper api key - {self.keys_config['serper_api_key']}')

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)