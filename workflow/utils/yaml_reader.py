import os
import yaml
from typing import Dict, Any, Optional

class YAMLReader:
    def __init__(self, config_dir: str):
        """
        Initialize the YAML reader with a configuration directory.
        
        Args:
            config_dir (str): Path to the directory containing YAML files
        """
        self.config_dir = config_dir
        self.cache: Dict[str, Any] = {}

    def read_yaml(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Read and parse a YAML file.
        
        Args:
            filename (str): Name of the YAML file (e.g., 'tasks.yaml')
            
        Returns:
            Dict containing the YAML contents or None if file doesn't exist
        """
        file_path = os.path.join(self.config_dir, filename)
        print(f'Attempting to read: {file_path}')  # Debug print
        # Return cached content if available
        if file_path in self.cache:
            return self.cache[file_path]
        
        try:
            with open(file_path, 'r') as file:
                content = yaml.safe_load(file)
                self.cache[file_path] = content
                return content
        except FileNotFoundError:
            print(f"Warning: File {filename} not found in {self.config_dir}")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing {filename}: {str(e)}")
            return None

    def get_tasks(self) -> Optional[Dict[str, Any]]:
        """
        Get contents of tasks.yaml
        """
        return self.read_yaml('tasks.yaml')

    def get_agents(self) -> Optional[Dict[str, Any]]:
        """
        Get contents of agents.yaml
        """
        return self.read_yaml('agents.yaml')
    
    def get_keys(self) -> Optional[Dict[str, Any]]:
        """
        Get keys of keys.yaml
        """
        return self.read_yaml('keys.yaml')
    
    def get_properties(self) -> Optional[Dict[str, Any]]:
        """
        Get keys of properties.yaml
        """
        return self.read_yaml('properties.yaml')

    def _load_yaml(self, filename: str):
        file_path = os.path.join(self.config_dir, filename)
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Warning: File {filename} not found in {self.config_dir}")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file {filename}: {e}")
