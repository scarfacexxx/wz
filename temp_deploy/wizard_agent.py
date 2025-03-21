import logging
from typing import Dict, Any
from elizaos import Agent

logger = logging.getLogger(__name__)

class WizardAgent(Agent):
    def __init__(self):
        super().__init__()
        self.config = {
            "name": "WizardsOfX",
            "personality": "Helpful magical game master",
            "commands": [
                "create", "duel", "cast", "brew", "use",
                "withdraw", "leaderboard", "tournament"
            ],
            "memory": {
                "type": "persistent",
                "storage": "hybrid"
            },
            "monitoring": {
                "accounts": ["@bankrbot"],
                "patterns": ["transfer", "confirmed", "failed"]
            }
        }

    def load_config(self):
        """Load agent configuration"""
        try:
            self.initialize(self.config)
            logger.info("Wizard agent configuration loaded")
        except Exception as e:
            logger.error(f"Failed to load agent config: {e}")
            raise

    def process_tweets(self):
        """Process incoming tweets and execute commands"""
        try:
            # ELIZAOS handles tweet monitoring automatically
            # We just need to keep the process running
            self.process_mentions()
        except Exception as e:
            logger.error(f"Error processing tweets: {e}")
            raise

    def handle_command(self, command: str, args: Dict[str, Any]) -> str:
        """Handle game commands from tweets"""
        try:
            if command == "create":
                return self._handle_create(args)
            elif command == "duel":
                return self._handle_duel(args)
            elif command == "cast":
                return self._handle_cast(args)
            # Add other command handlers
            
        except Exception as e:
            logger.error(f"Error handling command {command}: {e}")
            return "⚠️ Error processing command. Please try again."

    def _handle_create(self, args: Dict[str, Any]) -> str:
        """Handle wizard creation"""
        name = args.get("name", "")
        if not name or not (3 <= len(name) <= 20):
            return "⚠️ Invalid name! Use 3-20 alphanumeric characters."
            
        # ELIZAOS handles the actual creation
        # We just return the response
        house = self.assign_house()
        return f"""
        🎩 The Sorting Hat says... {house}!
        ✨ {name} begins:
        • Bonus: 20 Galleons (non-withdrawable)
        • Level: 1 (0/100 XP)
        • HP: 100/100
        • Spells: Incendio, Protego
        """

    def _handle_duel(self, args: Dict[str, Any]) -> str:
        """Handle duel requests"""
        opponent = args.get("opponent")
        amount = args.get("amount", 0)
        
        if not opponent or amount <= 0:
            return "⚠️ Invalid duel request! Use: d @player amount"
            
        # ELIZAOS handles the actual duel setup
        return f"⚔️ Duel request sent to {opponent} for {amount} Galleons!"

    def _handle_cast(self, args: Dict[str, Any]) -> str:
        """Handle spell casting"""
        spell = args.get("spell", "").lower()
        if not spell:
            return "⚠️ No spell specified! Use: cast [spell]"
            
        # ELIZAOS handles the actual spell casting
        return f"✨ Casting {spell}..." 