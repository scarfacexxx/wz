# Wizards of X: Error Codes Reference 🚨

## Error Code Structure

All error codes follow this format:
```
WOX-[Category]-[Subcategory]-[Specific Code]
Example: WOX-DB-CONN-001
```

## System Errors (WOX-SYS) 🖥️

### Connection Errors (CONN)
```
WOX-SYS-CONN-001: VM network connectivity failure
WOX-SYS-CONN-002: Database connection timeout
WOX-SYS-CONN-003: Discord webhook connection failure
WOX-SYS-CONN-004: Twitter API rate limit exceeded
WOX-SYS-CONN-005: Base scan API connection error
```

### Resource Errors (RES)
```
WOX-SYS-RES-001: High CPU usage (>80%)
WOX-SYS-RES-002: Memory limit exceeded
WOX-SYS-RES-003: Disk space critical (<10%)
WOX-SYS-RES-004: Database connection pool exhausted
WOX-SYS-RES-005: Network bandwidth throttled
```

### Process Errors (PROC)
```
WOX-SYS-PROC-001: ELIZAOS service crash
WOX-SYS-PROC-002: MySQL service failure
WOX-SYS-PROC-003: Monitoring service down
WOX-SYS-PROC-004: Backup process failure
WOX-SYS-PROC-005: Cron job execution error
```

## Database Errors (WOX-DB) 📊

### Query Errors (QUERY)
```
WOX-DB-QUERY-001: Syntax error in SQL
WOX-DB-QUERY-002: Deadlock detected
WOX-DB-QUERY-003: Query timeout
WOX-DB-QUERY-004: Invalid parameter
WOX-DB-QUERY-005: Table not found
```

### Transaction Errors (TRANS)
```
WOX-DB-TRANS-001: Transaction rollback
WOX-DB-TRANS-002: Concurrent modification
WOX-DB-TRANS-003: Foreign key violation
WOX-DB-TRANS-004: Unique constraint violation
WOX-DB-TRANS-005: Data integrity error
```

### Performance Errors (PERF)
```
WOX-DB-PERF-001: Slow query detected
WOX-DB-PERF-002: High connection count
WOX-DB-PERF-003: Table lock timeout
WOX-DB-PERF-004: Index scan inefficiency
WOX-DB-PERF-005: Buffer pool exhaustion
```

## Game Logic Errors (WOX-GAME) 🎮

### Duel Errors (DUEL)
```
WOX-GAME-DUEL-001: Invalid spell cast
WOX-GAME-DUEL-002: Out of turn action
WOX-GAME-DUEL-003: Duel timeout
WOX-GAME-DUEL-004: Invalid target
WOX-GAME-DUEL-005: State corruption
```

### Tournament Errors (TOURN)
```
WOX-GAME-TOURN-001: Invalid bracket state
WOX-GAME-TOURN-002: Player not found
WOX-GAME-TOURN-003: Tournament full
WOX-GAME-TOURN-004: Prize distribution error
WOX-GAME-TOURN-005: Schedule conflict
```

### Player Errors (PLAYER)
```
WOX-GAME-PLAYER-001: Invalid level up
WOX-GAME-PLAYER-002: Spell unlock error
WOX-GAME-PLAYER-003: Inventory corruption
WOX-GAME-PLAYER-004: Stats calculation error
WOX-GAME-PLAYER-005: House assignment failure
```

## Banking Errors (WOX-BANK) 💰

### Transaction Errors (TX)
```
WOX-BANK-TX-001: Insufficient balance
WOX-BANK-TX-002: Invalid amount
WOX-BANK-TX-003: Transaction timeout
WOX-BANK-TX-004: Double spend attempt
WOX-BANK-TX-005: Fee calculation error
```

### Verification Errors (VERIFY)
```
WOX-BANK-VERIFY-001: Invalid transaction hash
WOX-BANK-VERIFY-002: Base scan verification failed
WOX-BANK-VERIFY-003: Confirmation timeout
WOX-BANK-VERIFY-004: Invalid sender
WOX-BANK-VERIFY-005: Invalid recipient
```

### Prize Pool Errors (PRIZE)
```
WOX-BANK-PRIZE-001: Pool balance error
WOX-BANK-PRIZE-002: Distribution failure
WOX-BANK-PRIZE-003: Fee allocation error
WOX-BANK-PRIZE-004: Burn queue error
WOX-BANK-PRIZE-005: Tournament prize error
```

## Twitter Integration Errors (WOX-TWIT) 🐦

### Command Errors (CMD)
```
WOX-TWIT-CMD-001: Invalid command format
WOX-TWIT-CMD-002: Command rate limit
WOX-TWIT-CMD-003: Permission denied
WOX-TWIT-CMD-004: Invalid parameters
WOX-TWIT-CMD-005: Command timeout
```

### Response Errors (RESP)
```
WOX-TWIT-RESP-001: Response too long
WOX-TWIT-RESP-002: Rate limit exceeded
WOX-TWIT-RESP-003: API error
WOX-TWIT-RESP-004: Thread creation failed
WOX-TWIT-RESP-005: Media upload failed
```

### Monitoring Errors (MON)
```
WOX-TWIT-MON-001: Stream disconnection
WOX-TWIT-MON-002: Missed mentions
WOX-TWIT-MON-003: Processing delay
WOX-TWIT-MON-004: Queue overflow
WOX-TWIT-MON-005: Pattern match failure
```

## ELIZAOS Errors (WOX-ELIZA) 🤖

### Agent Errors (AGENT)
```
WOX-ELIZA-AGENT-001: Agent initialization failed
WOX-ELIZA-AGENT-002: Memory corruption
WOX-ELIZA-AGENT-003: Context loss
WOX-ELIZA-AGENT-004: Response generation error
WOX-ELIZA-AGENT-005: Pattern matching failure
```

### Memory Errors (MEM)
```
WOX-ELIZA-MEM-001: State save failure
WOX-ELIZA-MEM-002: State load error
WOX-ELIZA-MEM-003: Memory limit exceeded
WOX-ELIZA-MEM-004: Persistence error
WOX-ELIZA-MEM-005: Cache corruption
```

### Processing Errors (PROC)
```
WOX-ELIZA-PROC-001: Command parsing error
WOX-ELIZA-PROC-002: Response timeout
WOX-ELIZA-PROC-003: Action execution failed
WOX-ELIZA-PROC-004: Context switch error
WOX-ELIZA-PROC-005: Queue processing error
```

## Error Handling Guidelines 📝

### Error Severity Levels
```
CRITICAL: Immediate action required
HIGH: Response needed within 15 minutes
MEDIUM: Response needed within 1 hour
LOW: Response needed within 24 hours
INFO: No immediate action required
```

### Error Response Actions
1. **Critical Errors**
```
- Immediate system alert
- Auto-scaling if applicable
- Service restart if needed
- Admin notification
- Incident report creation
```

2. **High Severity**
```
- System alert
- Error logging
- Recovery attempt
- Admin notification
- Monitor resolution
```

3. **Medium Severity**
```
- Error logging
- Recovery planning
- Monitor impact
- Schedule resolution
```

4. **Low Severity**
```
- Error logging
- Track patterns
- Plan maintenance
- Update documentation
```

## Error Logging Format 📋

### Standard Log Entry
```json
{
  "error_code": "WOX-XXX-YYY-NNN",
  "timestamp": "ISO-8601",
  "severity": "LEVEL",
  "source": "component_name",
  "message": "Error description",
  "context": {
    "user": "affected_user",
    "action": "attempted_action",
    "state": "current_state"
  },
  "stack_trace": "if_applicable"
}
```

### Error Tracking
```python
def log_error(error_code, severity, message, context=None):
    """Log error with standard format"""
    log_entry = {
        "error_code": error_code,
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "message": message,
        "context": context or {}
    }
    
    # Log to file
    logger.error(json.dumps(log_entry))
    
    # Send alert if critical
    if severity == "CRITICAL":
        send_alert(error_code, message)
```

## Recovery Procedures 🔄

### Standard Recovery Flow
1. **Identify Error**
```
- Check error code
- Review context
- Assess severity
```

2. **Initial Response**
```
- Log incident
- Notify stakeholders
- Begin recovery
```

3. **Recovery Actions**
```
- Follow error-specific procedure
- Verify resolution
- Update status
```

4. **Post-Recovery**
```
- Document actions
- Update procedures
- Implement prevention
```

## Error Prevention 🛡️

### Monitoring Thresholds
```python
ERROR_THRESHOLDS = {
    "consecutive_failures": 3,
    "error_rate": 0.05,  # 5%
    "response_time": 2.0,  # seconds
    "memory_usage": 0.85  # 85%
}
```

### Automatic Recovery
```python
def auto_recovery(error_code):
    """Attempt automatic recovery based on error code"""
    if error_code.startswith("WOX-SYS"):
        return attempt_system_recovery()
    elif error_code.startswith("WOX-DB"):
        return attempt_db_recovery()
    elif error_code.startswith("WOX-GAME"):
        return attempt_game_recovery()
```

### Prevention Measures
1. **System Level**
```
- Regular health checks
- Resource monitoring
- Automatic scaling
- Load balancing
```

2. **Application Level**
```
- Input validation
- Rate limiting
- State verification
- Data consistency checks
```

3. **Database Level**
```
- Connection pooling
- Query optimization
- Index maintenance
- Regular backups
```

Remember: Proper error handling and logging are crucial for system stability and maintenance! 🔍 