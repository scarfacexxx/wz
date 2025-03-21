import os
import logging
from typing import Dict, Any
from elizaos import ElizaOS, Agent
from .agents.wizard_agent import WizardAgent
from .monitoring.metrics import MonitoringSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/var/log/wizards-of-x/game.log'
)
logger = logging.getLogger(__name__)

class GameService:
    def __init__(self):
        self.agent = WizardAgent()
        self.monitoring = MonitoringSystem()
        self.running = False

    def start(self):
        try:
            logger.info("Starting Wizards of X game service...")
            os.makedirs('/var/log/wizards-of-x', exist_ok=True)
            
            # Initialize ELIZAOS agent
            self._init_elizaos()
            
            # Start main loop
            self.running = True
            self._run()
            
        except Exception as e:
            logger.error(f"Failed to start game service: {e}")
            raise

    def _init_elizaos(self):
        """Initialize ELIZAOS with wizard agent configuration"""
        try:
            self.agent.load_config()
            logger.info("ELIZAOS agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ELIZAOS: {e}")
            raise

    def _run(self):
        """Main game loop"""
        while self.running:
            try:
                # Process tweets and game state
                self.agent.process_tweets()
                
                # Update monitoring metrics
                self.monitoring.update_metrics()
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                # Continue running despite errors
                continue

def main():
    service = GameService()
    try:
        service.start()
    except Exception as e:
        logger.error(f"Service failed to start: {e}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main()) 