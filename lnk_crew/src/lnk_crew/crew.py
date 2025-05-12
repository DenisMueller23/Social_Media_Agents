"""Orchestrates the entire Crew as a kind of container and manages how agents work together
to complete tasks"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from lnk_crew.tools.custom_tool import LinkedInContentAnalyzer
from typing import List
import logging
import yaml
import pathlib
import os
from lnk_crew.tools.delegate_work_tool import DelegateWorkTool
#from crewai import ToolRegistry

#ToolRegistry.register(DelegateWorkTool) 

logger = logging.getLogger(__name__)

@CrewBase
class LnkCrew:
    """LnkCrew for LinkedIn content analysis and creation"""
    
    MAX_REVISION_ATTEMPS = 3
    
    def __init__(self):
        logger.debug("Initializing LnkCrew")
        self._load_configs()
        agents = [self.research_agent(), self.content_creation_agent(), self.manager_agent()]
        tasks = [self.content_creation_task(), self.research_task(), self.manager_task()]
        self.delegate_work_tool = DelegateWorkTool(agents, tasks)
        
    def delegate_work(self, task, context, coworker):
        self.delegate_work_tool.delegate_work(task, context, coworker)
        
    def _load_configs(self):
        """Load configuration files"""
        try:
            base_path = pathlib.Path(os.path.abspath(__file__)).parent
            
            agents_path = base_path / "config" / "agents.yaml"
            with open(agents_path, "r") as f:
                self.agents_config = yaml.safe_load(f)
            logger.debug(f"Loaded agents config from {agents_path}")
            
            tasks_path = base_path / "config" / "tasks.yaml"
            with open(tasks_path, "r") as f:
                self.tasks_config = yaml.safe_load(f)
            logger.debug(f"Loaded tasks config from {tasks_path}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration files: {e}")
            raise

    @agent
    def research_agent(self) -> Agent:
        config = self.agents_config['research_agent']
        return Agent(
            name=config.get('name', 'Research Agent'),
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True,
            tools=[LinkedInContentAnalyzer()]
        )
    
    @agent
    def content_creation_agent(self) -> Agent:
        config = self.agents_config['content_creation_agent']
        return Agent(
            name=config.get('name', 'Content Creation Agent'),
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True
        )
    
    
    @agent
    def manager_agent(self) -> Agent:
        config = self.agents_config['manager_agent']
        
        # Create the agents and use the correct configurations
        available_agents = [self.research_agent(), self.content_creation_agent()]
        agent_configs = [self.agents_config['research_agent'], self.agents_config['content_creation_agent']]
        
        # Create delegation tools with the agents parameter 
        delegation_tools = [
            DelegateWorkTool(
                agents=available_agents,
                tasks=self.tasks_config
            )
        ]

        
        return Agent(
            name=config.get('name', 'Manager Agent'),
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True,
            allow_delegation=True,
            tools=delegation_tools
        )

    @task
    def research_task(self) -> Task:
        config = self.tasks_config['research_task']
        return Task(
            description=config['description'],
            agent=self.research_agent(),
            expected_output=config.get('expected_output', 'A research report on {topic}')
        )
            
    @task
    def content_creation_task(self) -> Task:
        config = self.tasks_config['content_creation_task']
        return Task(
            description=config['description'],
            agent=self.content_creation_agent(),
            dependencies=[self.research_task()],
            expected_output=config.get('expected_output', 'A draft LinkedIn post')
        )

    @task
    def manager_task(self) -> Task:
        config = self.tasks_config['manager_task']
        
        # Include the revision information in the description
        enhanced_description = (
            f"{config['description']}\n\n"
            f"Current revision count: 0\n"
            f"Maximum allowed revisions: {self.MAX_REVISION_ATTEMPS}"
        )
        
        return Task(
            description=enhanced_description,
            agent=self.manager_agent(),
            dependencies=[self.content_creation_task()],
            expected_output=config.get('expected_output', 'Final approval or revision of the LinkedIn document')
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LnkCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
