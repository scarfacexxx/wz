import unittest
from game_logic.character import Character
from game_logic.combat import Combat
from game_logic.banking import BankingSystem

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character('test_user', 'TestWizard')
        
    def test_character_creation(self):
        """Test basic character creation."""
        self.assertEqual(self.character.twitter_handle, 'test_user')
        self.assertEqual(self.character.name, 'TestWizard')
        self.assertEqual(self.character.level, 1)
        self.assertEqual(self.character.xp, 0)
        self.assertEqual(self.character.hp, 100)
        self.assertEqual(self.character.bonus_galleons, 20.00)
        self.assertEqual(self.character.withdrawable_galleons, 0.00)
        
    def test_starting_spells(self):
        """Test starting spell configuration."""
        spells = self.character._get_starting_spells()
        self.assertIn('Incendio', spells)
        self.assertIn('Protego', spells)
        
        incendio = spells['Incendio']
        self.assertEqual(incendio['accuracy'], 110)
        self.assertEqual(incendio['effect']['burn'], 20)
        
    def test_level_up(self):
        """Test level up mechanics."""
        self.character.xp = 100
        new_abilities = self.character.level_up()
        
        self.assertEqual(self.character.level, 2)
        self.assertEqual(self.character.xp, 0)
        self.assertIn('Flipendo', new_abilities['spells'])
        
class TestCombat(unittest.TestCase):
    def setUp(self):
        self.player1 = Character('player1', 'Wizard1')
        self.player2 = Character('player2', 'Wizard2')
        self.combat = Combat(self.player1, self.player2, 50.0)
        
    def test_combat_initialization(self):
        """Test combat setup."""
        self.assertEqual(self.combat.turn, self.player1.twitter_handle)
        self.assertEqual(self.combat.bet_amount, 50.0)
        self.assertEqual(self.combat.status, 'active')
        
    def test_spell_casting(self):
        """Test basic spell casting."""
        result = self.combat.cast_spell('player1', 'Incendio')
        
        self.assertNotIn('error', result)
        self.assertEqual(result['spell'], 'Incendio')
        self.assertEqual(self.combat.turn, 'player2')
        
    def test_invalid_turn(self):
        """Test casting on wrong turn."""
        result = self.combat.cast_spell('player2', 'Incendio')
        self.assertIn('error', result)
        
    def test_combat_end(self):
        """Test combat ending conditions."""
        # Force player2's HP to 1
        self.combat.hp2 = 1
        
        # Cast Incendio which should end the combat
        result = self.combat.cast_spell('player1', 'Incendio')
        
        self.assertEqual(self.combat.status, 'player1_wins')
        self.assertEqual(self.player1.wins, 1)
        self.assertEqual(self.player2.losses, 1)
        
class TestBanking(unittest.TestCase):
    def setUp(self):
        self.banking = BankingSystem()
        self.player = Character('test_user', 'TestWizard')
        
    def test_deposit(self):
        """Test deposit processing."""
        result = self.banking.process_deposit(
            'test_tx_hash',
            self.player,
            100.0
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['amount'], 100.0)
        self.assertEqual(self.player.withdrawable_galleons, 100.0)
        
    def test_withdrawal(self):
        """Test withdrawal processing."""
        # Setup initial balance
        self.player.withdrawable_galleons = 100.0
        
        result = self.banking.process_withdrawal(self.player, 50.0)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['amount'], 48.0)  # After 4% fee
        self.assertEqual(self.player.withdrawable_galleons, 50.0)
        
    def test_insufficient_balance(self):
        """Test withdrawal with insufficient balance."""
        self.player.withdrawable_galleons = 10.0
        
        result = self.banking.process_withdrawal(self.player, 50.0)
        self.assertIn('error', result)
        self.assertEqual(self.player.withdrawable_galleons, 10.0)
        
    def test_prize_distribution(self):
        """Test tournament prize distribution."""
        self.banking.prize_pool = 1000.0
        result = self.banking.distribute_tournament_prize(
            self.player,
            'daily'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['prize'], 400.0)  # Minimum daily prize
        self.assertEqual(self.player.withdrawable_galleons, 400.0)
        
if __name__ == '__main__':
    unittest.main() 