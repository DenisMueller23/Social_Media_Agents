from datetime import datetime
import logging
from lnk_crew.crew import LnkCrew

logger = logging.getLogger(__name__)

def get_user_input():
    """Get topic input from user"""
    print("\Welcome to LinkedIn content creator!")
    topic = input("Enter the topic you are ambitioned to create content about: ").strip()
    while not topic:
        print("Topic cannot be empty!")
        topic = input("Please enter a topic: ").strip()
    return topic

def run():
    """
    Run the crew with logging.
    """
    crew = LnkCrew().crew()
    
    try:
        # Get topic from user 
        topic = get_user_input()
        result = crew.kickoff(
            inputs={
                'topic': topic,
                'current_year': str(datetime.now().year)
            }
        )
        
        # Access task results
        for task in crew.tasks:
            logger.info(f"Task {task.name} output: {task.output}")
            
        # Access agent history
        for agent in crew.agents:
            logger.info(f"Agent {agent.name} history: {agent.message_history}")
            
        return result
            
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {e}")
        raise

def train():
    """Training function placeholder"""
    pass

def replay():
    """Replay function placeholder"""
    pass

def test():
    """Test function placeholder"""
    pass

if __name__ == "__main__":
    run()