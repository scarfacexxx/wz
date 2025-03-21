# Wizards of X: Recovery Procedures

## Overview
This document outlines the procedures for handling various system failures and recovery scenarios in the Wizards of X game.

## 1. Transaction Recovery

### Failed Deposits
```
1. Check transaction status:
   - Query Base scan for transaction hash
   - Verify @bankrbot confirmation tweet
   - Check processed_transactions table

2. If transaction confirmed but not credited:
   SELECT * FROM processed_transactions 
   WHERE tx_hash = '[hash]' AND status = 'confirmed';
   
   UPDATE players 
   SET withdrawable_galleons = withdrawable_galleons + [amount]
   WHERE twitter_handle = '[handle]';
   
   INSERT INTO transaction_log (type, amount, status, notes)
   VALUES ('recovery', [amount], 'completed', 'Manual deposit recovery');

3. If transaction pending:
   - Wait for confirmation (up to 1 hour)
   - Set up monitoring alert
   - Notify player of delay

4. If transaction failed:
   - Notify player
   - Log incident
   - Request new transaction
```

### Failed Withdrawals
```
1. Check withdrawal status:
   SELECT * FROM withdrawal_requests 
   WHERE id = [request_id];

2. If funds deducted but not sent:
   BEGIN TRANSACTION;
   
   UPDATE players 
   SET withdrawable_galleons = withdrawable_galleons + [amount]
   WHERE twitter_handle = '[handle]';
   
   UPDATE withdrawal_requests 
   SET status = 'failed'
   WHERE id = [request_id];
   
   INSERT INTO transaction_log (type, amount, status, notes)
   VALUES ('withdrawal_reversal', [amount], 'completed', 'Failed withdrawal recovery');
   
   COMMIT;

3. If @bankrbot error:
   - Check @bankrbot status
   - Retry transaction
   - Monitor for confirmation
```

## 2. Game State Recovery

### Interrupted Duels
```
1. Check duel state:
   SELECT * FROM active_duels 
   WHERE id = [duel_id];

2. If bet amount held:
   BEGIN TRANSACTION;
   
   UPDATE players 
   SET withdrawable_galleons = withdrawable_galleons + [bet_amount]
   WHERE twitter_handle IN (player1, player2);
   
   UPDATE active_duels 
   SET status = 'cancelled'
   WHERE id = [duel_id];
   
   INSERT INTO duel_log (duel_id, action, notes)
   VALUES ([duel_id], 'cancelled', 'Interrupted duel recovery');
   
   COMMIT;

3. Notify players:
   - Send status update
   - Explain refund
   - Provide new duel option
```

### Tournament Recovery
```
1. Check tournament state:
   SELECT * FROM tournaments 
   WHERE id = [tournament_id];

2. For each interrupted match:
   - Identify affected players
   - Check round status
   - Verify prize pool integrity

3. Recovery options:
   a) Resume from last valid state:
      UPDATE tournament_matches 
      SET status = 'pending'
      WHERE tournament_id = [id] AND round = [current_round];

   b) Restart round:
      CALL sp_restart_tournament_round([tournament_id], [round_number]);

   c) Emergency tournament end:
      CALL sp_emergency_tournament_end([tournament_id], [compensation_amount]);
```

## 3. System Recovery

### Database Recovery
```
1. Check backup status:
   ls -l /backup/mysql/[date]/*

2. Stop game services:
   systemctl stop wizards-service

3. Restore from backup:
   mysql -u [user] -p wizards < /backup/mysql/[date]/full_backup.sql

4. Verify integrity:
   CALL sp_verify_database_integrity();

5. Reconcile transactions:
   CALL sp_reconcile_transactions('[start_date]', '[end_date]');

6. Restart services:
   systemctl start wizards-service
```

### VM Recovery
```
1. Access recovery console:
   ssh -i recovery.pem admin@[backup_ip]

2. Mount backup volume:
   mount /dev/sdb1 /mnt/backup

3. Restore configuration:
   cp -r /mnt/backup/config/* /etc/wizards/

4. Restore database:
   mysql -u [user] -p wizards < /mnt/backup/db/latest.sql

5. Verify services:
   systemctl status wizards-service
   systemctl status mysql
```

## 4. State Verification

### Balance Reconciliation
```sql
-- 1. Calculate expected totals
SELECT SUM(withdrawable_galleons) as total_withdrawable,
       SUM(bonus_galleons) as total_bonus
FROM players;

-- 2. Verify against transactions
SELECT SUM(amount) as total_processed
FROM processed_transactions
WHERE status = 'confirmed';

-- 3. Check prize pool
SELECT current_amount FROM prize_pool;

-- 4. Verify burn queue
SELECT SUM(amount) as pending_burns
FROM burn_queue
WHERE status = 'pending';
```

### Game State Verification
```sql
-- 1. Check for stuck duels
SELECT * FROM active_duels
WHERE status = 'active'
AND last_action < NOW() - INTERVAL 30 MINUTE;

-- 2. Verify tournament integrity
SELECT t.id, t.status, COUNT(tm.id) as matches
FROM tournaments t
LEFT JOIN tournament_matches tm ON t.id = tm.tournament_id
WHERE t.status = 'active'
GROUP BY t.id, t.status;

-- 3. Check player states
SELECT twitter_handle, level, xp
FROM players
WHERE xp >= level * 100
AND level < 15;
```

## 5. Emergency Procedures

### Critical System Failure
1. Activate maintenance mode:
   ```bash
   ./wizards.sh maintenance on
   ```

2. Notify players:
   ```bash
   ./wizards.sh notify all "System maintenance in progress. Please stand by."
   ```

3. Secure current state:
   ```bash
   ./wizards.sh backup now
   ```

4. Verify critical data:
   ```bash
   ./wizards.sh verify all
   ```

5. Begin recovery:
   ```bash
   ./wizards.sh recover [failure_type]
   ```

### Network Partition
1. Check connectivity:
   ```bash
   ./wizards.sh check-network
   ```

2. Enable offline mode:
   ```bash
   ./wizards.sh offline-mode on
   ```

3. Queue commands:
   ```bash
   ./wizards.sh enable-command-queue
   ```

4. Process backlog:
   ```bash
   ./wizards.sh process-queue
   ```

## 6. Recovery Verification

### Post-Recovery Checks
```bash
# 1. Verify player data
./wizards.sh verify players

# 2. Check transaction consistency
./wizards.sh verify transactions

# 3. Validate game state
./wizards.sh verify game-state

# 4. Test critical functions
./wizards.sh test-suite recovery
```

### Monitoring Recovery
```bash
# 1. Watch error rates
./wizards.sh monitor errors --window 5m

# 2. Check performance
./wizards.sh monitor performance --detailed

# 3. Verify throughput
./wizards.sh monitor transactions --live
```

## 7. Prevention Measures

### Automated Checks
1. Regular state verification (every 5 minutes)
2. Balance reconciliation (every hour)
3. Transaction verification (real-time)
4. Game state validation (every minute)

### Backup Schedule
1. Database: Every 6 hours
2. Configuration: Daily
3. Game state: Every 15 minutes
4. Transaction log: Real-time

### Monitoring Alerts
1. Error rate exceeds 1%
2. Response time > 500ms
3. Database lag > 100ms
4. Memory usage > 80%

Remember: All recovery procedures must be tested regularly in a staging environment. Document any deviations from these procedures and update as needed. 