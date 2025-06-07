"""from crewai.tools import BaseTool
import yaml
from yaml import safe_load
import os

class DelegateWorkTool(BaseTool):
    def _load_configs(self):
        config_dir = os.path.join(os.path.dirname(__file__), "../config")
        agents_config_path = os.path.join(config_dir, "agents.yaml")
        tasks_config_path = os.path.join(config_dir, "tasks.yaml")

        try:
            with open(agents_config_path, "r") as f:
                self.agents_config = yaml.safe_load(f)
            with open(tasks_config_path, "r") as f:
                self.tasks_config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Unable to find configuration files at {config_dir}")
            raise
        except yaml.YAMLError as e:
            print(f"Error: Unable to parse configuration files - {e}")
            raise
    def __init__(self, agents, tasks):
        self._load_configs()
        super().__init__(
            name="Delegate Work Tool",
            description="Delegate a specific task to one of the following coworkers: Senior Researcher, LinkedIN Content Creator",
            arguments={
                "task": {"description": "The task to delegate", "type": "str"},
                "context": {"description": "The context for the task", "type": "str"},
                "coworker": {"description": "The coworker to delegate the task to", "type": "str"}
            }
        )

    

    def _run(self, task, context, coworker):
        try:
            # Get the agent configuration from the agents.yaml file
            agent_config = self.agents_config.get(coworker)
            
            # Check if the coworker is a valid agent
            if agent_config is None:
                print(f"invalid coworker: {coworker}")
                return
            #Get the task configuration from the tasks.yaml file
            task_config = self.tasks_config.get(task)
            
            # Check if the task is valid
            if task_config is None:
                print(f"invalid task: {task}")
                return
            
            # Delegate the task to the coworker
            print(f"Delegating task '{task}' to {coworker} with context '{context}'")

            # Simulate the coworker working on the task
            # In a real-world scenario, you would replace this with actual logic
            # to handle the task, such as sending an email or creating a ticket
            print(f"{coworker} is working on task '{task}'")

            # Simulate the coworker completing the task
            # In a real-world scenario, you would replace this with actual logic
            # to handle the completed task, such as sending an email or updating a database
            print(f"{coworker} has completed task '{task}'")
                
            # Return the result of the task
            # In a real-world scenario, you would replace this with actual logic
            # to return the result of the task, such as a completed document or a report
            return f"Task '{task}' completed by {coworker}"
        except Exception as e:
            print(f"Error: Unable to delegate task - {e}")
            raise
            """