import unittest
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from game_logic.character import Character
from game_logic.combat import Combat
from game_logic.banking import BankingSystem
from game_logic.command_handler import CommandHandler

class TestLoadPerformance(unittest.TestCase):
    def setUp(self):
        self.banking = BankingSystem()
        self.command_handler = CommandHandler(self.banking)
        self.num_concurrent_users = 100
        self.test_duration = 60  # seconds
        self.metrics = {
            'commands_processed': 0,
            'errors': 0,
            'avg_response_time': 0,
            'response_times': []
        }
        
    def test_high_volume_tweets(self):
        """Test system performance with high volume of incoming tweets."""
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.num_concurrent_users) as executor:
            futures = []
            
            # Submit tweet processing tasks
            while time.time() - start_time < self.test_duration:
                futures.append(
                    executor.submit(
                        self._process_random_command
                    )
                )
                
                # Simulate tweet arrival rate (10ms between tweets)
                time.sleep(0.01)
                
            # Wait for all tasks to complete
            for future in as_completed(futures):
                result = future.result()
                self._update_metrics(result)
                
        # Calculate final metrics
        self.metrics['avg_response_time'] = (
            sum(self.metrics['response_times']) / 
            len(self.metrics['response_times'])
        )
        
        # Assert performance requirements
        self.assertLess(
            self.metrics['avg_response_time'],
            0.5,  # Maximum 500ms average response time
            "Average response time too high"
        )
        
        error_rate = self.metrics['errors'] / self.metrics['commands_processed']
        self.assertLess(
            error_rate,
            0.01,  # Maximum 1% error rate
            "Error rate too high"
        )
        
    def test_concurrent_duels(self):
        """Test system performance with many concurrent duels."""
        # Create test players
        players = self._create_test_players(100)
        active_duels = []
        
        # Start concurrent duels
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit duel creation tasks
            duel_futures = []
            for i in range(0, len(players), 2):
                duel_futures.append(
                    executor.submit(
                        self._start_duel,
                        players[i],
                        players[i+1]
                    )
                )
                
            # Wait for duels to be created
            for future in as_completed(duel_futures):
                duel_id = future.result()
                if duel_id:
                    active_duels.append(duel_id)
                    
            # Submit spell casting tasks
            cast_futures = []
            start_time = time.time()
            
            while time.time() - start_time < self.test_duration:
                for duel_id in active_duels:
                    cast_futures.append(
                        executor.submit(
                            self._cast_spell,
                            duel_id,
                            random.choice(['Incendio', 'Protego'])
                        )
                    )
                    
            # Wait for all casts to complete
            for future in as_completed(cast_futures):
                result = future.result()
                self._update_metrics(result)
                
        # Assert duel performance
        self.assertGreater(
            len(active_duels),
            45,  # At least 45 concurrent duels should succeed
            "Too many failed duel creations"
        )
        
    def test_tournament_scaling(self):
        """Test tournament system with large number of participants."""
        num_players = 128  # Test with 128 players (7 rounds)
        players = self._create_test_players(num_players)
        
        # Start tournament
        tournament_id = self._create_tournament()
        
        # Register players concurrently
        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = []
            for player in players:
                futures.append(
                    executor.submit(
                        self._register_tournament,
                        tournament_id,
                        player
                    )
                )
                
            # Wait for registrations
            for future in as_completed(futures):
                result = future.result()
                self._update_metrics(result)
                
        # Run tournament rounds
        round_times = []
        for round_num in range(7):  # log2(128) = 7 rounds
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=64) as executor:
                futures = []
                matches = self._get_round_matches(tournament_id, round_num)
                
                for match in matches:
                    futures.append(
                        executor.submit(
                            self._process_match,
                            tournament_id,
                            match
                        )
                    )
                    
                # Wait for round completion
                for future in as_completed(futures):
                    result = future.result()
                    self._update_metrics(result)
                    
            round_times.append(time.time() - start_time)
            
        # Assert tournament performance
        avg_round_time = sum(round_times) / len(round_times)
        self.assertLess(
            avg_round_time,
            30,  # Maximum 30 seconds per round
            "Tournament rounds taking too long"
        )
        
    def test_database_performance(self):
        """Test database performance under load."""
        start_time = time.time()
        operation_times = {
            'read': [],
            'write': [],
            'update': []
        }
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            
            while time.time() - start_time < self.test_duration:
                # Mix of read/write operations
                operation = random.choice(['read', 'write', 'update'])
                futures.append(
                    executor.submit(
                        self._database_operation,
                        operation
                    )
                )
                
            # Collect timing results
            for future in as_completed(futures):
                op_type, duration = future.result()
                operation_times[op_type].append(duration)
                
        # Calculate averages
        for op_type in operation_times:
            if operation_times[op_type]:
                avg_time = sum(operation_times[op_type]) / len(operation_times[op_type])
                self.assertLess(
                    avg_time,
                    0.1,  # Maximum 100ms per database operation
                    f"Database {op_type} operations too slow"
                )
                
    def _process_random_command(self) -> Dict:
        """Process a random game command and measure performance."""
        start_time = time.time()
        try:
            command = random.choice([
                ('create', ['TestWizard']),
                ('duel', ['@opponent', '50']),
                ('cast', ['Incendio']),
                ('withdraw', ['100'])
            ])
            
            result = self.command_handler.handle_command(
                command[0],
                command[1],
                f'player_{random.randint(1, 1000)}'
            )
            
            return {
                'success': True,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'error': str(e)
            }
            
    def _update_metrics(self, result: Dict):
        """Update test metrics with command result."""
        self.metrics['commands_processed'] += 1
        self.metrics['response_times'].append(result['response_time'])
        if not result['success']:
            self.metrics['errors'] += 1
            
    def _create_test_players(self, count: int) -> List[Character]:
        """Create test player characters."""
        return [
            Character(f'player_{i}', f'Wizard_{i}')
            for i in range(count)
        ]
        
    def _start_duel(self, player1: Character, player2: Character) -> int:
        """Start a test duel between two players."""
        try:
            result = self.command_handler.handle_command(
                'duel',
                [f'@{player2.twitter_handle}', '50'],
                player1.twitter_handle
            )
            return result.get('duel_id')
        except Exception:
            return None
            
    def _cast_spell(self, duel_id: int, spell: str) -> Dict:
        """Cast a spell in a test duel."""
        start_time = time.time()
        try:
            result = self.command_handler.handle_command(
                'cast',
                [spell],
                f'player_{random.randint(1, 1000)}'
            )
            return {
                'success': True,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'error': str(e)
            }
            
    def _create_tournament(self) -> int:
        """Create a test tournament."""
        result = self.command_handler.handle_command(
            't',
            ['create'],
            'admin'
        )
        return result['tournament_id']
        
    def _register_tournament(self, tournament_id: int, player: Character) -> Dict:
        """Register a player for a tournament."""
        start_time = time.time()
        try:
            result = self.command_handler.handle_command(
                't',
                ['join'],
                player.twitter_handle
            )
            return {
                'success': True,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'error': str(e)
            }
            
    def _get_round_matches(self, tournament_id: int, round_num: int) -> List[Dict]:
        """Get matches for a tournament round."""
        return self.command_handler.handle_command(
            't',
            ['matches', str(round_num)],
            'admin'
        )['matches']
        
    def _process_match(self, tournament_id: int, match: Dict) -> Dict:
        """Process a tournament match."""
        start_time = time.time()
        try:
            result = self.command_handler.handle_command(
                't',
                ['process_match', str(match['id'])],
                'admin'
            )
            return {
                'success': True,
                'response_time': time.time() - start_time
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'error': str(e)
            }
            
    def _database_operation(self, operation: str) -> tuple:
        """Perform a test database operation."""
        start_time = time.time()
        try:
            if operation == 'read':
                self.command_handler.handle_command(
                    'profile',
                    [],
                    f'player_{random.randint(1, 1000)}'
                )
            elif operation == 'write':
                self.command_handler.handle_command(
                    'create',
                    [f'Wizard_{random.randint(1, 1000)}'],
                    f'player_{random.randint(1, 1000)}'
                )
            else:  # update
                self.command_handler.handle_command(
                    'update_profile',
                    ['title', 'Duelist'],
                    f'player_{random.randint(1, 1000)}'
                )
        except Exception:
            pass
            
        return operation, time.time() - start_time
        
if __name__ == '__main__':
    unittest.main() 