# How to Build Wizards of X: A Developer's Guide

## What We're Building
Wizards of X is a Twitter-based RPG where everything happens through tweets. No website, no app - just pure Twitter interactions. Players tweet commands to @WizardsOfX to create wizards, duel each other, craft potions, and participate in tournaments.

## Core Components

### 1. ELIZAOS Foundation
ELIZAOS is our backbone - it's an open-source system (14.8k+ stars) that provides a unique way to interact with Twitter:
- No API keys needed - uses built-in Twitter client
- Works through direct tweet monitoring and responses
- Built-in memory system for game state
- Multi-agent support with consistent personality
- RAG (Retrieval Augmented Generation) for game knowledge
- Support for multiple LLMs (Llama, GPT-4, Claude)

Key ELIZAOS Features:
1. **Tweet Monitoring**
   - Automatically watches for @WizardsOfX mentions
   - Processes commands from tweet text
   - Handles thread-based conversations
   - Manages rate limiting automatically

2. **State Management**
   - Built-in memory system for active games
   - Persistent storage for game data
   - Handles concurrent operations
   - Maintains conversation context

3. **Command Processing**
   - Natural language understanding
   - Command validation and parsing
   - Error handling and responses
   - Multi-turn interactions

4. **Integration Method**
   - Uses ELIZAOS starter template
   - Configure character settings for @WizardsOfX
   - Set up command handlers
   - Define response templates

### 2. Game State & Database
Use MySQL on Google Cloud VM to store:
- Player info (house, level, spells, etc.)
- Active duels and tournaments
- Transaction history
- Leaderboards
- Prize pool and burn queue

### 3. Core Game Systems

#### Character System
- Four houses with unique bonuses:
  * Ravenclaw: +10% spell accuracy
  * Gryffindor: +5 HP
  * Slytherin: +1 critical damage
  * Hufflepuff: +1 HP/turn
- Starting package: 20 non-withdrawable Galleons
- Level progression (1-15)
- XP system:
  * Duel win: 20 XP
  * Duel loss: 10 XP
  * Tournament win: 50 XP
  * Tournament loss: 10 XP
  * Level up requirement: 100 × Current Level

#### Battle System
- Turn-based dueling
- Spell combinations:
  * Two-spell combos: +10% bonus
  * Three-spell combos: +15-20% bonus
- Spell progression from Level 1-15
- House bonus calculations
- HP management

#### Banking System (via @bankrbot)
The banking system works entirely through tweet monitoring - no API integration needed:

#### How @bankrbot Works
- It's a Twitter-based banking system
- No API keys or direct integration required
- All interactions happen through tweets
- Transactions are verified on-chain via Base scan

## Detailed Banking & Tokenomics Implementation

### Deposit Flow
1. Player Action:
   - Player tweets: "@bankrbot transfer [amount] galleons to @WizardsOfX"
2. Processing:
   - ELIZAOS monitors for @bankrbot's confirmation tweet
   - Extracts transaction hash from confirmation
   - Creates deposit request in database
   - Verifies transaction on Base scan
   - Credits balance to withdrawable galleons
3. Database Updates:
   - Create record in deposit_requests table
   - Update player's withdrawable_galleons
   - Create transaction history entry

### Withdrawal Flow
1. Request:
   - Player tweets: "@WizardsOfX withdraw [amount]"
   - System validates balance
2. Fee Processing:
   - Calculate 4% total fee
   - 2% to prize pool (funds tournaments/cups)
   - 2% to burn queue (12-48h random delay)
3. Execution:
   - Create withdrawal request
   - Send transfer via @bankrbot
   - Monitor for confirmation
   - Verify on Base scan
   - Update status in withdrawal_requests table

### Burn Queue System
1. Queue Management:
   - Accumulate 2% fees in burn queue
   - Random delay (12-48h) for each burn
   - Track in BurnQueue table
2. Execution Process:
   - ELIZAOS monitors queue for ready burns
   - Format: "@bankrbot transfer [amount] galleons to 0x000000000000000000000000000000000000dEaD"
   - Verify burn transaction on Base scan
   - Update burn queue status

### Prize Pool Management
1. Collection:
   - Accumulates 2% of withdrawal fees
   - Tracks in PrizePool table
2. Distribution:
   - Daily Tournament: Max(400G, 10% of pool)
   - Weekly House Cup: Max(200G, 20% of pool)
3. Monitoring:
   - Regular balance verification
   - Transaction reconciliation
   - Prize pool analytics

## Database Schema

### Core Tables
1. Players Table:
```sql
CREATE TABLE players (
    twitter_handle VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    house ENUM('Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff'),
    level INT DEFAULT 1,
    xp INT DEFAULT 0,
    hp INT DEFAULT 100,
    bonus_galleons DECIMAL(10,2) DEFAULT 20.00,
    withdrawable_galleons DECIMAL(10,2) DEFAULT 0.00,
    spells JSON,
    potions JSON,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    titles JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

2. Active Duels:
```sql
CREATE TABLE active_duels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player1 VARCHAR(50),
    player2 VARCHAR(50),
    bet_amount DECIMAL(10,2),
    status VARCHAR(20),
    turn VARCHAR(50),
    hp1 INT,
    hp2 INT,
    combo_history JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. Banking Tables:
```sql
CREATE TABLE withdrawal_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    twitter_handle VARCHAR(50),
    amount DECIMAL(10,2),
    fee DECIMAL(10,2),
    tx_hash VARCHAR(66),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    block_number BIGINT
);

CREATE TABLE burn_queue (
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10,2),
    scheduled_time TIMESTAMP,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processed_transactions (
    tx_hash VARCHAR(66) PRIMARY KEY,
    block_number BIGINT,
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    value DECIMAL(10,2),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20)
);
```

## Balance Reconciliation System

### Automated Checks (Every 5 Minutes)
1. Fetch Chain Data:
   - Get latest transactions from Base scan
   - Get current wallet balance
2. Database Reconciliation:
   - Sum all player balances
   - Calculate pending transactions
   - Verify prize pool amount
   - Check burn queue status
3. Discrepancy Handling:
   - Log differences
   - Send Discord alerts
   - Flag for manual review

### Manual Reconciliation Process
1. Transaction Audit:
   - Review all recent transactions
   - Verify Base scan records
   - Check @bankrbot confirmations
2. Balance Verification:
   - Compare on-chain vs database
   - Check individual accounts
   - Verify prize pool calculations
3. Correction Actions:
   - Update incorrect balances
   - Reprocess failed transactions
   - Adjust prize pool if needed

## Error Recovery Procedures

### Transaction Failures
1. Deposit Failures:
   - Mark transaction as failed
   - No balance update
   - Send notification tweet
   - Log for monitoring

2. Withdrawal Failures:
   - Restore player balance
   - Reverse fee allocations
   - Remove from burn queue
   - Update transaction status
   - Send notification tweet

### Game State Recovery
1. Interrupted Duels:
   - Save last valid state
   - Restore player HP/status
   - Return bets if needed
   - Send status update

2. Tournament Issues:
   - Save bracket state
   - Handle disconnections
   - Manage prize distribution
   - Update leaderboards

## Monitoring Setup

### System Metrics
1. Performance:
   - VM resource usage
   - Database connections
   - Transaction processing time
   - Response latency

2. Game Economy:
   - Prize pool balance
   - Burn queue size
   - Transaction volume
   - Player balances

### Alert System
1. Discord Webhooks:
   - Critical errors
   - Balance discrepancies
   - System performance
   - Tournament updates

2. Error Tracking:
   - Failed transactions
   - Game state issues
   - API timeouts
   - Database errors

## Testing Strategy

### Unit Tests
1. Game Logic:
   - Spell damage calculation
   - XP system
   - Level progression
   - House bonuses

2. Banking:
   - Fee calculation
   - Prize pool distribution
   - Burn queue processing
   - Balance updates

### Integration Tests
1. Full Flows:
   - Wizard creation → Duel → Rewards
   - Deposit → Withdrawal → Burn
   - Tournament entry → Completion → Prizes

2. Edge Cases:
   - Network failures
   - Transaction timeouts
   - Concurrent operations
   - State conflicts

Remember: Everything in this game happens through tweets. ELIZAOS handles all Twitter interactions without API keys, and @bankrbot operations are managed through tweet monitoring. The system is designed to be fully autonomous while maintaining complete transparency through the blockchain.

## Development Steps

### 1. Infrastructure Setup
1. Set up Google Cloud VM (e2-micro)
2. Install ELIZAOS using their starter template
3. Configure MySQL database
4. Set up monitoring (Discord webhooks)

### 2. Core Systems Implementation
1. Character Creation
   - Random house assignment
   - Starting stats allocation
   - Spell assignment

2. Battle System
   - Turn management
   - Damage calculation
   - Combo system
   - Win/loss handling

3. Banking Integration
   - Monitor @bankrbot tweets
   - Track transactions
   - Handle deposits/withdrawals
   - Manage burn queue

4. Tournament System
   - Entry handling
   - Bracket management
   - Prize distribution
   - Leaderboard updates

### 3. Command System
Implement core commands:
- start: Create wizard
- d @player amount: Start duel
- cast spell: Use spell in duel
- brew potion: Create potions
- t join: Join tournament
- lb: Check leaderboards
- withdraw: Request withdrawal

### 4. Error Handling & Recovery
- Monitor failed transactions
- Handle interrupted duels
- Manage state conflicts
- Implement automatic retries
- Set up Discord alerts

### 5. Balance & Economy
- Prize pool management
- Burn queue execution
- Tournament prize scaling
- Fee distribution
- Balance reconciliation

## Testing & Monitoring

### Game Testing
1. Test all commands via tweets
2. Verify banking flows
3. Run tournament simulations
4. Test house bonuses
5. Verify XP calculations
6. Check leaderboard updates

### System Monitoring
- Transaction verification
- Balance reconciliation
- Prize pool tracking
- Burn queue execution
- Error logging
- Performance metrics

## Important Notes

### Twitter Interaction
- Everything must work through tweets
- Keep commands simple
- Handle rate limits
- Plan for interrupted flows

### State Management
- Use ELIZAOS memory for active games
- Database for persistent data
- Regular state verification
- Handle edge cases

### Banking Operations
- Monitor @bankrbot interactions
- Track all transactions
- Verify on Base scan
- Handle failed operations

### Game Balance
- Test economy thoroughly
- Balance spell damage
- Adjust XP rates
- Monitor prize pool

## Common Challenges

1. **State Consistency**
   - Between ELIZAOS memory and database
   - During interrupted operations
   - Across multiple duels

2. **Transaction Verification**
   - Monitoring @bankrbot responses
   - Verifying Base scan data
   - Handling timeouts

3. **Game Balance**
   - Spell damage scaling
   - House bonus effects
   - Tournament prize pools
   - XP progression

4. **Error Recovery**
   - Failed transactions
   - Interrupted duels
   - Network issues
   - State conflicts

Remember: This is a Twitter-native game. Everything revolves around tweet interactions. ELIZAOS handles the Twitter communication and state management, while the database maintains long-term data. No external APIs needed - just Twitter interactions and blockchain verification through Base scan. 

## Additional Notes

### ELIZAOS Character Configuration
Your character configuration is crucial. Example structure:
```json
{
  "name": "WizardsOfX",
  "personality": "Helpful magical game master",
  "commands": ["start", "duel", "cast", ...],
  "memory": {
    "type": "persistent",
    "storage": "hybrid"
  },
  "clients": ["twitter"],
  "monitoring": {
    "accounts": ["@bankrbot"],
    "patterns": ["transfer", "confirmed", "failed"]
  }
}
```

### Tweet Monitoring Patterns
Key patterns to watch:
1. Game Commands: "@WizardsOfX [command]"
2. Banking Deposits: "@bankrbot transfer"
3. Transaction Confirmations: "Transaction confirmed"
4. Error Messages: "Transaction failed"

Remember: The entire system operates through tweet monitoring and responses. There are no direct API integrations - everything happens through public tweets that ELIZAOS and bankrbot process naturally. 