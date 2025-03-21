import random
import re
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from .character import Character
from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    amount: float
    sender: str
    tx_hash: Optional[str]
    status: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    retries: int = 0

class BankingSystem:
    FEE_RATE = 0.04  # 4% total fee
    PRIZE_POOL_RATE = 0.02  # 2% to prize pool
    BURN_RATE = 0.02  # 2% to burn queue
    
    def __init__(self):
        self.prize_pool = 0.0
        self.burn_queue = []  # List of (amount, scheduled_time) tuples
        self.processed_transactions = {}  # tx_hash -> transaction_details
        
    def process_deposit(self, tx_hash: str, player: Character, amount: float) -> Dict:
        """Process a deposit from @bankrbot."""
        if tx_hash in self.processed_transactions:
            return {'error': 'Transaction already processed'}
            
        # Verify transaction on Base scan (placeholder - implement actual verification)
        if not self._verify_transaction(tx_hash):
            return {'error': 'Transaction verification failed'}
            
        # Update player balance
        player.withdrawable_galleons += amount
        
        # Record transaction
        self.processed_transactions[tx_hash] = {
            'type': 'deposit',
            'player': player.twitter_handle,
            'amount': amount,
            'timestamp': datetime.now()
        }
        
        return {
            'success': True,
            'amount': amount,
            'new_balance': player.withdrawable_galleons
        }
        
    def process_withdrawal(self, player: Character, amount: float) -> Dict:
        """Process a withdrawal request."""
        if amount > player.withdrawable_galleons:
            return {'error': 'Insufficient balance'}
            
        # Calculate fees
        total_fee = amount * self.FEE_RATE
        prize_pool_fee = amount * self.PRIZE_POOL_RATE
        burn_fee = amount * self.BURN_RATE
        net_amount = amount - total_fee
        
        # Update balances
        player.withdrawable_galleons -= amount
        self.prize_pool += prize_pool_fee
        
        # Schedule burn
        burn_time = datetime.now() + timedelta(hours=random.randint(12, 48))
        self.burn_queue.append((burn_fee, burn_time))
        
        return {
            'success': True,
            'amount': net_amount,
            'fee': total_fee,
            'prize_pool_contribution': prize_pool_fee,
            'burn_amount': burn_fee,
            'new_balance': player.withdrawable_galleons
        }
        
    def process_burn_queue(self) -> Dict:
        """Process any pending burns that are due."""
        current_time = datetime.now()
        burns_processed = []
        remaining_burns = []
        total_burned = 0
        
        for amount, scheduled_time in self.burn_queue:
            if current_time >= scheduled_time:
                # Execute burn (placeholder - implement actual burn transaction)
                self._execute_burn(amount)
                burns_processed.append((amount, scheduled_time))
                total_burned += amount
            else:
                remaining_burns.append((amount, scheduled_time))
                
        self.burn_queue = remaining_burns
        
        return {
            'burns_processed': burns_processed,
            'total_burned': total_burned,
            'remaining_burns': len(remaining_burns)
        }
        
    def distribute_tournament_prize(self, winner: Character, tournament_type: str) -> Dict:
        """Distribute prize pool for tournament winners."""
        if tournament_type == 'daily':
            prize = max(400, self.prize_pool * 0.10)
        elif tournament_type == 'weekly':
            prize = max(200, self.prize_pool * 0.20)
        else:
            return {'error': 'Invalid tournament type'}
            
        if prize > self.prize_pool:
            return {'error': 'Insufficient prize pool'}
            
        self.prize_pool -= prize
        winner.withdrawable_galleons += prize
        
        return {
            'success': True,
            'prize': prize,
            'remaining_pool': self.prize_pool,
            'winner_new_balance': winner.withdrawable_galleons
        }
        
    def get_tokenomics(self) -> Dict:
        """Get current tokenomics status."""
        return {
            'prize_pool': self.prize_pool,
            'pending_burns': sum(amount for amount, _ in self.burn_queue),
            'total_processed_volume': sum(
                tx['amount'] for tx in self.processed_transactions.values()
            )
        }
        
    def _verify_transaction(self, tx_hash: str) -> bool:
        """Verify transaction on Base scan."""
        # TODO: Implement actual Base scan verification
        return True
        
    def _execute_burn(self, amount: float) -> bool:
        """Execute burn transaction."""
        # TODO: Implement actual burn transaction
        return True

class BankrbotHandler:
    def __init__(self):
        self.pending_transactions: Dict[str, Transaction] = {}
        self.last_interaction = datetime.now()
        self.cooldown = 60  # seconds
        
    def validate_tweet_pattern(self, tweet_text: str) -> bool:
        """Validate if tweet matches expected bankrbot patterns"""
        safe_patterns = [
            r'^transfer \d+ Galleons to @WizardsOfX$',
            r'^Transaction confirmed: 0x[a-fA-F0-9]{64}$',
            r'^Transaction failed:.*$'
        ]
        return any(re.match(pattern, tweet_text) for pattern in safe_patterns)

    def extract_transaction_data(self, tweet_text: str) -> Optional[Dict]:
        """Safely extract transaction data from tweet"""
        try:
            if 'transfer' in tweet_text.lower():
                match = re.match(r'transfer (\d+) Galleons to @WizardsOfX', tweet_text)
                if match:
                    return {
                        'type': 'transfer',
                        'amount': int(match.group(1))
                    }
            elif 'confirmed' in tweet_text.lower():
                match = re.match(r'Transaction confirmed: (0x[a-fA-F0-9]{64})', tweet_text)
                if match:
                    return {
                        'type': 'confirmation',
                        'tx_hash': match.group(1)
                    }
            return None
        except Exception as e:
            logger.error(f"Error parsing bankrbot tweet: {e}")
            return None

    async def process_bankrbot_tweet(self, tweet_text: str, sender: str) -> Optional[str]:
        """Process incoming bankrbot tweets with safety checks"""
        # Enforce cooldown
        if (datetime.now() - self.last_interaction).total_seconds() < self.cooldown:
            return None
            
        # Validate tweet pattern
        if not self.validate_tweet_pattern(tweet_text):
            logger.warning(f"Invalid tweet pattern from bankrbot: {tweet_text}")
            return None

        # Extract data
        data = self.extract_transaction_data(tweet_text)
        if not data:
            return None

        # Handle transfer initiation
        if data['type'] == 'transfer':
            tx_id = f"tx_{int(time.time())}"
            self.pending_transactions[tx_id] = Transaction(
                id=tx_id,
                amount=data['amount'],
                sender=sender,
                tx_hash=None,
                status='pending',
                created_at=datetime.now(),
                confirmed_at=None
            )
            return tx_id

        # Handle confirmation
        elif data['type'] == 'confirmation':
            # Find matching pending transaction
            for tx_id, tx in self.pending_transactions.items():
                if tx.status == 'pending' and not tx.tx_hash:
                    tx.tx_hash = data['tx_hash']
                    tx.status = 'confirming'
                    # Verify on Base scan
                    if await self.verify_transaction_on_basescan(tx):
                        tx.status = 'confirmed'
                        tx.confirmed_at = datetime.now()
                        return tx_id
            
        self.last_interaction = datetime.now()
        return None

    async def verify_transaction_on_basescan(self, tx: Transaction) -> bool:
        """Verify transaction on Base scan with retries"""
        for _ in range(3):  # Max retries
            try:
                # Add Base scan verification logic here
                # For now, we'll simulate verification
                time.sleep(2)
                return True
            except Exception as e:
                tx.retries += 1
                if tx.retries >= 3:
                    tx.status = 'failed'
                    return False
                await asyncio.sleep(5)  # Wait before retry
        return False

    def cleanup_old_transactions(self):
        """Clean up old pending transactions"""
        cutoff = datetime.now() - timedelta(hours=1)
        for tx_id, tx in list(self.pending_transactions.items()):
            if tx.created_at < cutoff and tx.status in ['pending', 'confirming']:
                tx.status = 'expired'
                logger.warning(f"Transaction {tx_id} expired")

    def get_transaction_status(self, tx_id: str) -> Optional[str]:
        """Get current status of a transaction"""
        if tx_id in self.pending_transactions:
            return self.pending_transactions[tx_id].status
        return None 