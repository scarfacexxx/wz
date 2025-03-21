# Wizards of X: API Documentation

## Command Format
All commands are sent as tweets to @WizardsOfX. The general format is:
```
@WizardsOfX [command] [parameters...]
```

## Core Commands

### Character Creation
```
Command: create [name]
Example: @WizardsOfX create Vex_Blackthorn

Parameters:
- name: 3-20 chars, alphanumeric only

Response:
🎩 The Sorting Hat says... [HOUSE]! ([bonus])
✨ [name] begins:
• Bonus: 20 Galleons (non-withdrawable)
• Withdrawable: 0 Galleons
• Total: 20 Galleons
• Level: 1 (0/100 XP)
• HP: 100/100
• Spells: [starting spells]
```

### Dueling
```
Command: d @player [amount]
Example: @WizardsOfX d @MoonMage 50

Parameters:
- @player: Target player's Twitter handle
- amount: Bet amount (must be > 0)

Response:
⚔️ [player1] challenges @[player2]!
💰 Bet: [amount] Galleons
New Balance: [balance] Galleons
⏳ @[player2], reply '@WizardsOfX accept' within 5 mins!
```

### Spell Casting
```
Command: cast [spell]
Example: @WizardsOfX cast Incendio

Parameters:
- spell: Valid spell name from player's spellbook

Response:
✨ [player] casts [spell]!
💥 [damage] dmg[, effects]!
[target]: [HP display] [current]/[max] HP[, status]!
[Combo information if applicable]
```

### Potion Brewing
```
Command: brew [potion]
Example: @WizardsOfX brew Strength

Parameters:
- potion: Valid potion name

Response:
🧪 Brewing [potion]...
Req: Lvl [level]+, [cost] Galleons
[Success/Failure]
[If success] New Balance: [balance] Galleons
✨ [potion] added: [effects]
```

### Profile View
```
Command: p
Example: @WizardsOfX p

Response:
📊 [name] ([house])
Level: [level] ([xp]/[next_level] XP)
HP: [current]/[max]
💰 Balance: [bonus] Bonus, [withdrawable] Withdrawable
Spells: [spell list]
Potions: [potion list]
Stats: [W/L record]
```

## Tournament Commands

### Join Tournament
```
Command: t join
Example: @WizardsOfX t join

Response:
🏆 [player] joins [tournament type]!
Entry: [cost] Galleons
New Balance: [balance] Galleons
Starts: [time] UTC
```

### Tournament Status
```
Command: t status
Example: @WizardsOfX t status

Response:
🏆 [tournament name]
Round: [current]/[total]
Players: [active]/[total]
Prize Pool: [amount] Galleons
Your Next Match: [opponent] at [time] UTC
```

## Banking Commands

### Deposit
```
Command: deposit
Example: @WizardsOfX deposit

Response:
💰 Use: @bankrbot transfer [amount] Galleons to @WizardsOfX
E.g., @bankrbot transfer 50 Galleons to @WizardsOfX
Waiting...

[After @bankrbot confirms]
✨ Deposit confirmed!
+[amount] Galleons (Withdrawable)
New Balance: [bonus] Bonus, [withdrawable] Withdrawable, [total] Total
```

### Withdraw
```
Command: withdraw [amount]
Example: @WizardsOfX withdraw 50

Parameters:
- amount: Amount to withdraw (must be ≤ withdrawable balance)

Response:
💰 Withdrawing...
Amount: [amount] Galleons
Fee: [fee] Galleons (4%)
• [prize_pool_fee]G to Prize Pool
• [burn_fee]G queued for burning
@bankrbot transfer [final_amount] Galleons to @[player]
```

### View Tokenomics
```
Command: tokenomics
Example: @WizardsOfX tokenomics

Response:
🪙 Wizards of X Tokenomics:
💰 Prize Pool: [amount] Galleons
🔥 Total Burned: [amount] Galleons
⏳ Pending Burns: [amount] Galleons

Fee Structure:
• 4% Total Fee
• 2% to Prize Pool
• 2% to Random Burns

Prizes:
• Daily Tournament: [amount]G
• Weekly House Cup: [amount]G
```

## Leaderboard Commands

### View Leaderboard
```
Command: lb [type]
Example: @WizardsOfX lb s

Parameters:
- type: s (seasonal), a (all-time), or h (house)

Response:
🏆 [Period] [Type] Leaderboard
1. [player1] ([house], Lvl [level]) - [W]W/[L]L, [balance] Galleons
2. [player2] ([house], Lvl [level]) - [W]W/[L]L, [balance] Galleons
[...]
Rewards: [reward structure]
```

## Error Responses

### Invalid Command
```
❌ Unknown command. Type '@WizardsOfX help' for command list.
```

### Insufficient Balance
```
❌ Insufficient balance!
Required: [amount] Galleons
Your Balance: [balance] Galleons
```

### Level Requirement
```
❌ Level too low!
Required: Level [required]
Your Level: [current]
```

### Rate Limit
```
⏳ You're doing that too fast!
Please wait [time] seconds.
```

### Transaction Error
```
❌ Transaction failed!
Error: [reason]
ID: [error_id]
Please try again or contact support.
```

## Response Codes

### Success Codes
- 200: Command processed successfully
- 201: Resource created successfully
- 202: Command accepted, processing

### Error Codes
- 400: Invalid command format
- 401: Unauthorized action
- 403: Insufficient privileges
- 404: Resource not found
- 409: Conflict (e.g., already in duel)
- 429: Rate limit exceeded
- 500: Internal error

## Rate Limits
- General commands: 6 per minute
- Duel actions: 1 per 5 seconds
- Banking operations: 1 per minute
- Profile views: 10 per minute

## Notes
1. All commands are case-insensitive
2. Timestamps are in UTC
3. Response times < 500ms
4. Commands may be queued during high load
5. Some commands require account verification

Remember: All interactions happen through tweets. There are no direct API endpoints - everything is processed through @WizardsOfX mentions and @bankrbot interactions. 