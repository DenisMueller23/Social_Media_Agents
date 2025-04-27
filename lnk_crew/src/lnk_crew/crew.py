"""Orchestrates the entire Crew as a kind of container and manages how agents work together
to complete tasks"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from lnk_crew.tools.custom_tool import LinkedInContentAnalyzer

@CrewBase
class LnkCrew:
    """LnkCrew for LinkedIn content analysis and creation"""
    
    MAX_REVISION_ATTEMPS = 3
    
    # Define config file paths as class attributes
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            verbose=True,
            tools=[LinkedInContentAnalyzer()]
        )
    
    @agent
    def content_creation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creation_agent'],
            verbose=True
        )
    
    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_agent'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )
            
    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
            dependencies=[self.research_task()]
        )

    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['manager_task'],
            dependencies=[self.content_creation_task()]
        )
              
    @crew
    def crew(self) -> Crew:
        """Creates the LnkCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically populated by @agent decorators
            tasks=self.tasks,    # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True
        )