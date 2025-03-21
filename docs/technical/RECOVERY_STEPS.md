# Wizards of X: Recovery Steps Guide 🔄

## Overview

This document provides step-by-step procedures for recovering from various system failures and issues in the Wizards of X game system.

## System Recovery 🖥️

### 1. Complete System Failure

#### Initial Assessment
```bash
# Check system status
systemctl status wizards-of-x
systemctl status mysql
systemctl status nginx

# Check logs
tail -f /var/log/wizards-of-x/error.log
journalctl -xe
```

#### Recovery Steps
1. **Service Restart**
```bash
# Restart core services
systemctl restart wizards-of-x
systemctl restart mysql
systemctl restart nginx

# Verify services
systemctl status wizards-of-x
```

2. **Data Verification**
```python
# Location: /opt/wizards-of-x/utils/verify_system.py

def verify_system_state():
    """Verify system integrity"""
    checks = [
        verify_database_connection(),
        verify_elizaos_state(),
        verify_active_games(),
        verify_banking_state()
    ]
    return all(checks)
```

3. **State Recovery**
```bash
# Restore from latest backup if needed
/usr/local/bin/wox-restore-backup.sh

# Verify state
/usr/local/bin/wox-verify-state.sh
```

### 2. Database Recovery

#### Connection Issues
```bash
# Check MySQL status
systemctl status mysql

# Check connection count
mysql -e "SHOW STATUS LIKE 'Threads_connected';"

# Reset connections if needed
mysql -e "FLUSH HOSTS;"
```

#### Data Corruption
1. **Table Check**
```sql
-- Check tables
CHECK TABLE players, active_duels, withdrawal_requests;

-- Repair if needed
REPAIR TABLE affected_table;
```

2. **Data Restore**
```bash
# Stop game services
systemctl stop wizards-of-x

# Restore specific table
mysql wizards_of_x < /var/backups/wizards-of-x/critical/table_backup.sql

# Verify data
mysql wizards_of_x -e "SELECT COUNT(*) FROM restored_table;"
```

## Game State Recovery 🎮

### 1. Active Duel Recovery

#### Interrupted Duels
```python
# Location: /opt/wizards-of-x/recovery/duel_recovery.py

def recover_interrupted_duel(duel_id):
    """Recover interrupted duel state"""
    # Get last valid state
    last_state = get_last_valid_state(duel_id)
    
    # Verify player states
    verify_player_states(last_state)
    
    # Restore duel
    restore_duel_state(last_state)
    
    # Notify players
    notify_players_of_recovery(duel_id)
```

#### Stuck Duels
```python
def handle_stuck_duel(duel_id):
    """Handle stuck duel recovery"""
    # Check if truly stuck
    if is_duel_stuck(duel_id):
        # Save current state
        backup_duel_state(duel_id)
        
        # Force end if needed
        force_end_duel(duel_id)
        
        # Compensate players
        compensate_players(duel_id)
```

### 2. Tournament Recovery

#### Bracket Recovery
```python
def recover_tournament_bracket(tournament_id):
    """Recover tournament bracket state"""
    # Get last valid bracket
    bracket = get_last_valid_bracket(tournament_id)
    
    # Verify matches
    verify_match_states(bracket)
    
    # Restore bracket
    restore_tournament_bracket(bracket)
    
    # Update participants
    notify_tournament_update(tournament_id)
```

#### Prize Distribution Recovery
```python
def recover_prize_distribution(tournament_id):
    """Recover failed prize distribution"""
    # Check distribution status
    status = get_prize_distribution_status(tournament_id)
    
    # Verify transactions
    verify_prize_transactions(tournament_id)
    
    # Complete distribution
    complete_prize_distribution(tournament_id)
```

## Banking Recovery 💰

### 1. Transaction Recovery

#### Failed Deposits
```python
# Location: /opt/wizards-of-x/recovery/banking_recovery.py

def recover_failed_deposit(tx_hash):
    """Recover failed deposit"""
    # Verify transaction on Base scan
    tx_status = verify_transaction(tx_hash)
    
    if tx_status.confirmed:
        # Update local state
        update_player_balance(tx_status)
        
        # Log recovery
        log_deposit_recovery(tx_hash)
        
        # Notify player
        notify_deposit_recovery(tx_status)
```

#### Failed Withdrawals
```python
def recover_failed_withdrawal(withdrawal_id):
    """Recover failed withdrawal"""
    # Get withdrawal details
    withdrawal = get_withdrawal_details(withdrawal_id)
    
    # Verify status on Base scan
    chain_status = verify_withdrawal_chain(withdrawal)
    
    if not chain_status.executed:
        # Reverse withdrawal
        reverse_withdrawal(withdrawal)
        
        # Restore player balance
        restore_player_balance(withdrawal)
        
        # Notify player
        notify_withdrawal_reversal(withdrawal)
```

### 2. Balance Recovery

#### Balance Reconciliation
```python
def reconcile_balances():
    """Reconcile player balances"""
    # Get all balances
    balances = get_all_player_balances()
    
    # Verify transactions
    verify_transaction_history()
    
    # Adjust if needed
    for balance in balances:
        if needs_adjustment(balance):
            adjust_balance(balance)
            log_adjustment(balance)
```

#### Prize Pool Recovery
```python
def recover_prize_pool():
    """Recover prize pool state"""
    # Calculate expected balance
    expected = calculate_expected_pool()
    
    # Verify actual balance
    actual = get_actual_pool_balance()
    
    # Reconcile difference
    if expected != actual:
        reconcile_pool_difference(expected, actual)
        log_pool_reconciliation()
```

## ELIZAOS Recovery 🤖

### 1. Memory State Recovery

#### Agent State
```python
# Location: /opt/wizards-of-x/recovery/elizaos_recovery.py

def recover_agent_state():
    """Recover ELIZAOS agent state"""
    # Backup current state
    backup_agent_state()
    
    # Load last known good state
    load_backup_state()
    
    # Verify agent functionality
    verify_agent_responses()
    
    # Resume operations
    resume_agent_processing()
```

#### Conversation Context
```python
def recover_conversation_context():
    """Recover lost conversation context"""
    # Get recent interactions
    recent = get_recent_interactions()
    
    # Rebuild context
    rebuild_conversation_context(recent)
    
    # Verify context
    verify_context_consistency()
```

### 2. Command Recovery

#### Failed Commands
```python
def recover_failed_commands():
    """Recover failed command processing"""
    # Get failed commands
    failed = get_failed_commands()
    
    for cmd in failed:
        # Verify command validity
        if is_command_still_valid(cmd):
            # Reprocess command
            reprocess_command(cmd)
            
            # Verify outcome
            verify_command_outcome(cmd)
```

#### Rate Limit Recovery
```python
def handle_rate_limit_recovery():
    """Handle rate limit recovery"""
    # Check current limits
    limits = get_current_rate_limits()
    
    # Queue important commands
    queue_priority_commands()
    
    # Implement backoff
    apply_rate_limit_backoff()
```

## Network Recovery 🌐

### 1. Connection Recovery

#### API Connection
```python
# Location: /opt/wizards-of-x/recovery/network_recovery.py

def recover_api_connection():
    """Recover API connectivity"""
    # Test connections
    test_twitter_api()
    test_base_scan_api()
    
    # Reset if needed
    reset_api_connections()
    
    # Verify connectivity
    verify_api_functionality()
```

#### Database Connection
```python
def recover_db_connection():
    """Recover database connectivity"""
    # Check connection pool
    check_connection_pool()
    
    # Reset connections
    reset_db_connections()
    
    # Verify connectivity
    verify_db_connectivity()
```

### 2. Service Recovery

#### Discord Integration
```python
def recover_discord_integration():
    """Recover Discord webhook functionality"""
    # Test webhooks
    test_discord_webhooks()
    
    # Reset if needed
    reset_webhook_connections()
    
    # Verify notifications
    verify_discord_notifications()
```

#### Twitter Monitoring
```python
def recover_twitter_monitoring():
    """Recover Twitter monitoring"""
    # Check stream status
    check_twitter_stream()
    
    # Reconnect if needed
    reconnect_twitter_stream()
    
    # Verify monitoring
    verify_tweet_processing()
```

## Emergency Procedures 🚨

### 1. Critical Failure Recovery

#### System Lockdown
```python
# Location: /opt/wizards-of-x/recovery/emergency.py

def emergency_lockdown():
    """Implement emergency system lockdown"""
    # Stop new actions
    pause_new_commands()
    
    # Save all states
    save_all_game_states()
    
    # Notify players
    broadcast_maintenance_mode()
```

#### Safe Mode Recovery
```python
def enter_safe_mode():
    """Enter system safe mode"""
    # Minimal services
    start_core_services()
    
    # Verify critical components
    verify_critical_systems()
    
    # Begin recovery
    start_recovery_process()
```

### 2. Data Recovery

#### Emergency Backup
```python
def emergency_backup():
    """Create emergency backup"""
    # Stop services
    stop_all_services()
    
    # Backup everything
    backup_all_data()
    
    # Verify backup
    verify_backup_integrity()
```

#### State Restoration
```python
def restore_system_state():
    """Restore from emergency backup"""
    # Verify backup
    verify_backup_state()
    
    # Restore data
    restore_from_backup()
    
    # Verify restoration
    verify_system_integrity()
```

## Recovery Verification 📋

### 1. System Checks

#### Component Verification
```python
# Location: /opt/wizards-of-x/recovery/verification.py

def verify_all_components():
    """Verify all system components"""
    checks = [
        verify_database(),
        verify_elizaos(),
        verify_game_state(),
        verify_banking(),
        verify_networking()
    ]
    return all(checks)
```

#### Integration Tests
```python
def run_recovery_tests():
    """Run post-recovery integration tests"""
    tests = [
        test_game_flow(),
        test_banking_flow(),
        test_tournament_flow(),
        test_social_integration()
    ]
    return all(tests)
```

### 2. Monitoring Recovery

#### Alert Verification
```python
def verify_monitoring():
    """Verify monitoring systems"""
    # Check alert system
    verify_alert_system()
    
    # Test notifications
    test_notifications()
    
    # Verify metrics
    verify_metrics_collection()
```

#### Performance Verification
```python
def verify_performance():
    """Verify system performance"""
    # Check response times
    verify_response_times()
    
    # Check resource usage
    verify_resource_usage()
    
    # Monitor error rates
    verify_error_rates()
```

## Best Practices 📝

### 1. Recovery Documentation
- Keep detailed recovery logs
- Document all actions taken
- Update procedures based on outcomes
- Maintain incident history

### 2. Prevention Measures
- Regular system checks
- Proactive monitoring
- Automated recovery where possible
- Regular backup verification

### 3. Communication
- Keep stakeholders informed
- Document downtime causes
- Share recovery timelines
- Provide status updates

Remember: Always follow these procedures in order and document all recovery actions! 🔄 