"""
Main entry point for the Wizards of X game service.
"""
import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/wizards-of-x/game.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for the game service."""
    logger.info("Starting Wizards of X game service...")
    
    # Create log directory if it doesn't exist
    log_dir = Path("/var/log/wizards-of-x")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # TODO: Initialize game components
    # - Setup ELIZAOS agent
    # - Initialize Twitter client
    # - Connect to database
    # - Start game loop
    
    logger.info("Game service started successfully!")

if __name__ == "__main__":
    main() 