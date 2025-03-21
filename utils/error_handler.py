import logging
from typing import Dict, Optional
from datetime import datetime
import json
import traceback

class GameError(Exception):
    """Base class for game-specific exceptions."""
    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()

class TransactionError(GameError):
    """Raised when a transaction fails."""
    pass

class GameStateError(GameError):
    """Raised when game state becomes invalid."""
    pass

class NetworkError(GameError):
    """Raised when network operations fail."""
    pass

class ErrorHandler:
    def __init__(self, discord_webhook_url: Optional[str] = None):
        self.discord_webhook_url = discord_webhook_url
        self.logger = logging.getLogger('wizards_of_x')
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging settings."""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for all logs
        fh = logging.FileHandler('game.log')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        
        # File handler for errors only
        error_fh = logging.FileHandler('error.log')
        error_fh.setLevel(logging.ERROR)
        error_fh.setFormatter(formatter)
        
        # Stream handler for console
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(error_fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.INFO)
        
    def handle_error(self, error: Exception, context: Dict = None) -> Dict:
        """Handle any error and return appropriate response."""
        context = context or {}
        
        if isinstance(error, GameError):
            return self._handle_game_error(error, context)
        else:
            return self._handle_unknown_error(error, context)
            
    def _handle_game_error(self, error: GameError, context: Dict) -> Dict:
        """Handle game-specific errors."""
        self.logger.error(
            f"Game Error: {error.error_code} - {str(error)}",
            extra={
                'error_code': error.error_code,
                'details': error.details,
                'context': context
            }
        )
        
        if isinstance(error, TransactionError):
            self._notify_discord(
                f"🚨 Transaction Error: {error.error_code}\n"
                f"Message: {str(error)}\n"
                f"Details: {json.dumps(error.details, indent=2)}"
            )
            
        return {
            'error': True,
            'code': error.error_code,
            'message': str(error),
            'details': error.details
        }
        
    def _handle_unknown_error(self, error: Exception, context: Dict) -> Dict:
        """Handle unexpected errors."""
        error_id = datetime.now().strftime('%Y%m%d%H%M%S')
        
        self.logger.error(
            f"Unexpected Error [{error_id}]: {str(error)}",
            extra={
                'error_id': error_id,
                'traceback': traceback.format_exc(),
                'context': context
            }
        )
        
        self._notify_discord(
            f"🚨 Unexpected Error [{error_id}]\n"
            f"Error: {str(error)}\n"
            f"```\n{traceback.format_exc()}\n```"
        )
        
        return {
            'error': True,
            'code': 'UNKNOWN_ERROR',
            'message': 'An unexpected error occurred',
            'error_id': error_id
        }
        
    def _notify_discord(self, message: str):
        """Send error notification to Discord."""
        if not self.discord_webhook_url:
            return
            
        # TODO: Implement Discord webhook notification
        pass
        
class StateRecovery:
    """Handles game state recovery operations."""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.logger = error_handler.logger
        
    def recover_duel(self, duel_id: int) -> Dict:
        """Recover from an interrupted duel."""
        try:
            # TODO: Implement duel recovery logic
            # 1. Load duel state from database
            # 2. Verify player states
            # 3. Either resume or safely end duel
            # 4. Return bets if needed
            pass
        except Exception as e:
            return self.error_handler.handle_error(e, {'duel_id': duel_id})
            
    def recover_transaction(self, tx_hash: str) -> Dict:
        """Recover from a failed transaction."""
        try:
            # TODO: Implement transaction recovery logic
            # 1. Check transaction status on Base scan
            # 2. Verify local state
            # 3. Apply or reverse changes as needed
            pass
        except Exception as e:
            return self.error_handler.handle_error(e, {'tx_hash': tx_hash})
            
    def recover_tournament(self, tournament_id: int) -> Dict:
        """Recover from an interrupted tournament."""
        try:
            # TODO: Implement tournament recovery logic
            # 1. Load tournament state
            # 2. Verify all matches
            # 3. Resume or safely end tournament
            # 4. Handle prize distribution
            pass
        except Exception as e:
            return self.error_handler.handle_error(e, {'tournament_id': tournament_id}) 