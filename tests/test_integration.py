import unittest
from game_logic.character import Character
from game_logic.combat import Combat
from game_logic.banking import BankingSystem
from game_logic.command_handler import CommandHandler

class TestGameFlows(unittest.TestCase):
    def setUp(self):
        self.banking = BankingSystem()
        self.command_handler = CommandHandler(self.banking)
        
    def test_full_duel_flow(self):
        """Test complete duel flow from start to finish."""
        # Create characters
        create_result1 = self.command_handler.handle_command(
            'create',
            ['Wizard1'],
            'player1'
        )
        create_result2 = self.command_handler.handle_command(
            'create',
            ['Wizard2'],
            'player2'
        )
        
        self.assertTrue(create_result1['success'])
        self.assertTrue(create_result2['success'])
        
        # Start duel
        duel_result = self.command_handler.handle_command(
            'duel',
            ['@player2', '50'],
            'player1'
        )
        
        self.assertTrue(duel_result['success'])
        self.assertEqual(duel_result['duel']['bet_amount'], 50.0)
        
        # Cast spells
        cast_result1 = self.command_handler.handle_command(
            'cast',
            ['Incendio'],
            'player1'
        )
        
        self.assertNotIn('error', cast_result1)
        self.assertEqual(cast_result1['spell'], 'Incendio')
        
        cast_result2 = self.command_handler.handle_command(
            'cast',
            ['Protego'],
            'player2'
        )
        
        self.assertNotIn('error', cast_result2)
        self.assertEqual(cast_result2['spell'], 'Protego')
        
    def test_banking_flow(self):
        """Test complete banking flow."""
        # Create character
        create_result = self.command_handler.handle_command(
            'create',
            ['Wizard1'],
            'player1'
        )
        
        self.assertTrue(create_result['success'])
        
        # Process deposit
        deposit_result = self.banking.process_deposit(
            'test_tx_hash',
            Character('player1', 'Wizard1'),
            100.0
        )
        
        self.assertTrue(deposit_result['success'])
        self.assertEqual(deposit_result['amount'], 100.0)
        
        # Request withdrawal
        withdraw_result = self.command_handler.handle_command(
            'withdraw',
            ['50'],
            'player1'
        )
        
        self.assertTrue(withdraw_result['success'])
        self.assertEqual(withdraw_result['amount'], 48.0)  # After fees
        
        # Check tokenomics
        tokenomics = self.command_handler.handle_command(
            'tokenomics',
            [],
            'player1'
        )
        
        self.assertIn('prize_pool', tokenomics)
        self.assertIn('pending_burns', tokenomics)
        
    def test_tournament_flow(self):
        """Test tournament flow."""
        # Create multiple characters
        players = ['player1', 'player2', 'player3', 'player4']
        for player in players:
            result = self.command_handler.handle_command(
                'create',
                [f'Wizard_{player}'],
                player
            )
            self.assertTrue(result['success'])
            
        # Join tournament
        for player in players:
            result = self.command_handler.handle_command(
                't',
                ['join'],
                player
            )
            self.assertTrue(result['success'])
            
        # Simulate tournament matches
        # Note: In a real implementation, this would be more complex
        # and would handle brackets, timing, etc.
        
    def test_error_recovery(self):
        """Test error recovery in various scenarios."""
        # Test interrupted duel
        create_result = self.command_handler.handle_command(
            'create',
            ['Wizard1'],
            'player1'
        )
        
        self.assertTrue(create_result['success'])
        
        # Start duel that will be interrupted
        duel_result = self.command_handler.handle_command(
            'duel',
            ['@player2', '50'],
            'player1'
        )
        
        # Simulate interruption by clearing active duels
        self.command_handler.active_duels.clear()
        
        # Attempt to continue duel
        cast_result = self.command_handler.handle_command(
            'cast',
            ['Incendio'],
            'player1'
        )
        
        self.assertIn('error', cast_result)
        
    def test_concurrent_operations(self):
        """Test handling of concurrent operations."""
        # Create character
        create_result = self.command_handler.handle_command(
            'create',
            ['Wizard1'],
            'player1'
        )
        
        self.assertTrue(create_result['success'])
        
        # Simulate concurrent withdrawals
        # In a real implementation, this would use threading/async
        withdraw1 = self.command_handler.handle_command(
            'withdraw',
            ['50'],
            'player1'
        )
        
        withdraw2 = self.command_handler.handle_command(
            'withdraw',
            ['50'],
            'player1'
        )
        
        # One should succeed, one should fail
        self.assertTrue(
            (withdraw1.get('success') and 'error' in withdraw2) or
            (withdraw2.get('success') and 'error' in withdraw1)
        )
        
if __name__ == '__main__':
    unittest.main() 