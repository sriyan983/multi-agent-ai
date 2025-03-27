import os
from utils.yaml_reader import YAMLReader

config = YAMLReader('config').get_keys()

openai_api_key = config['open_api_key'];
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

serper_api_key = config['serper_api_key'];

print(f'open api key - {openai_api_key}')
print(f'serper api key - {serper_api_key}')