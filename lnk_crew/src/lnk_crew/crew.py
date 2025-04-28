"""Orchestrates the entire Crew as a kind of container and manages how agents work together
to complete tasks"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from lnk_crew.tools.custom_tool import LinkedInContentAnalyzer
from typing import List
from crewai.tools.agent_tools.delegate_work_tool import DelegateWorkTool

logger = logging.getLogger(__name__)

@CrewBase
class LnkCrew:
    """LnkCrew for LinkedIn content analysis and creation"""
    
    MAX_REVISION_ATTEMPS = 3
    
    def __init__(self):
        logger.debug("Initializing LnkCrew")
        self._agents = []
        self._tasks = []
        self._load_configs()
        
    def _load_configs(self):
        """Load configuration files"""
        
        try: 
            # Get absolute path to the config directory
            base_path = Path(__file__).parent.parent.parent
            
            # Load agents config
            agents_path = base_path / "config" / "agents.yaml"
            with open(agents_path, "r") as f:
                self.agents_config = yaml.safe_load(f)
            logger.debug(f"Loaded agents config from {agents_path}")
            
            #Load tasks config
            tasks_path = base_path / "config" / "tasks.yaml"
            with open(tasks_path, "r") as f:
                self.tasks_config = yaml.safe_load(f)
            logger.debug(f"Loaded tasks config from {tasks_path}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration files: {e}")
            raise
            
            
            
            
    
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
        # Get all the agents that the manager can delegate to
        available_agents = [self.research_agent(), self.content_creation_agent()]
        
        # Create delegation tools
        delegation_tools = self._create_delegation_tools(available_agents)

        return Agent(
            config=self.agents_config['manager_agent'],
            verbose=True,
            allow_delegation=True,
            tools=delegation_tools
        )
        
    def _create_delegation_tools(self, agents: List[Agent]) -> List[DelegateWorkTool]:
        # Create a string of available coworkers for the tool description
        coworkers = ", ".join([f"{agent.role}" for agent in agents])
        
        # Create the delegation tool
        delegate_tool = DelegateWorkTool(
            agents=agents,
            description=f"Delegate work to your coworkers: {coworkers}. "
                       f"Use this when you need content revisions or additional research."
        )
        
        return [delegate_tool]

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
            dependencies=[self.content_creation_task()],
            context=[
                f"Current revision count: 0",
                f"Maximum allowed revisions: {self.MAX_REVISION_ATTEMPS}"
            ],

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