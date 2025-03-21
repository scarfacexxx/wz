# 🧙‍♂️ Wizards of X

A Twitter-native wizarding game where players duel, brew potions, and compete in tournaments through tweets.

## 🎮 Game Overview

Wizards of X is a magical RPG that lives entirely on Twitter. Players interact with @WizardsOfX through tweets to:
- Create their wizard and get sorted into houses
- Learn and cast spells in duels
- Brew and use potions
- Participate in tournaments
- Earn and manage Galleons (in-game currency)

### Houses & Bonuses
- 🦅 Ravenclaw: +10% accuracy
- 🦁 Gryffindor: +5 HP
- 🐍 Slytherin: +1 crit dmg
- 🦡 Hufflepuff: +1 HP/turn

## 🛠 Tech Stack

- Python 3.8+
- ELIZAOS Framework for Twitter interactions
- MySQL 8.0 for game state
- Base blockchain for transactions
- Discord webhooks for monitoring

## 📋 Requirements

- Python 3.8 or higher
- MySQL 8.0
- Twitter Developer Account
- Base blockchain access (for transaction verification)

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/scarfacexxx/wz.git
cd wz
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. Start the service:
```bash
python -m wizards_of_x.main
```

## 🎮 Game Commands

- `@WizardsOfX i want to play` - Start playing
- `@WizardsOfX create [name]` - Create your wizard
- `@WizardsOfX d @player [amount]` - Challenge to duel
- `@WizardsOfX cast [spell]` - Cast spell in duel
- `@WizardsOfX brew [potion]` - Craft potion
- `@WizardsOfX t join` - Join tournament
- `@WizardsOfX withdraw [amount]` - Withdraw Galleons

## 💰 Banking System

The game uses @bankrbot for handling Galleon transactions:
- Deposits: Tweet `@bankrbot transfer [amount] Galleons to @WizardsOfX`
- Withdrawals: Tweet `@WizardsOfX withdraw [amount]`
- 4% fee on withdrawals:
  * 2% to prize pool
  * 2% to burn queue (12-48h delay)

## 🏆 Tournaments

- Daily Tournament: Max(400G, 10% of pool)
- Weekly House Cup: Max(200G, 20% of pool)
- Entry fees contribute to prize pool

## 🔍 Monitoring

The system includes comprehensive monitoring:
- System metrics (CPU, memory, response times)
- Game metrics (active players, transactions)
- Discord alerts for critical events
- Transaction verification logs

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=wizards_of_x tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- ELIZAOS Framework for Twitter interaction
- @bankrbot for handling transactions
- Base blockchain for verification
- All our magical players! 