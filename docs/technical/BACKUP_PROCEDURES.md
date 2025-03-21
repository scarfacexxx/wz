# Wizards of X: Backup Procedures Guide 💾

## Overview

This document outlines the backup procedures for maintaining data integrity and system recovery capabilities for the Wizards of X game system.

## Database Backups 📊

### Automated Daily Backups

```bash
# Location: /etc/cron.daily/wox-backup.sh
#!/bin/bash

# Variables
BACKUP_DIR="/var/backups/wizards-of-x/mysql"
DATE=$(date +%Y%m%d)
MYSQL_USER="wox_backup"
MYSQL_PASSWORD="[secured]"
DB_NAME="wizards_of_x"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

# Full database backup
mysqldump --user=$MYSQL_USER --password=$MYSQL_PASSWORD \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  $DB_NAME > $BACKUP_DIR/full_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/full_backup_$DATE.sql

# Keep last 7 days of backups
find $BACKUP_DIR -name "full_backup_*.sql.gz" -mtime +7 -delete
```

### Critical Tables Hourly Snapshots

```bash
# Location: /etc/cron.hourly/wox-critical-backup.sh
#!/bin/bash

BACKUP_DIR="/var/backups/wizards-of-x/critical"
DATE=$(date +%Y%m%d_%H)
MYSQL_USER="wox_backup"
MYSQL_PASSWORD="[secured]"
DB_NAME="wizards_of_x"

# Critical tables to backup hourly
TABLES=(
  "players"
  "active_duels"
  "withdrawal_requests"
  "burn_queue"
  "processed_transactions"
)

# Backup each critical table
for table in "${TABLES[@]}"
do
  mysqldump --user=$MYSQL_USER --password=$MYSQL_PASSWORD \
    --single-transaction \
    $DB_NAME $table > $BACKUP_DIR/${table}_${DATE}.sql
  gzip $BACKUP_DIR/${table}_${DATE}.sql
done

# Keep last 24 hours of critical backups
find $BACKUP_DIR -name "*_*.sql.gz" -mtime +1 -delete
```

### Backup Verification

```bash
# Location: /usr/local/bin/verify-backups.sh
#!/bin/bash

# Test restore latest backup to verification database
VERIFY_DB="wox_verify"
LATEST_BACKUP=$(ls -t /var/backups/wizards-of-x/mysql/full_backup_*.sql.gz | head -1)

# Create verification database
mysql -e "DROP DATABASE IF EXISTS $VERIFY_DB; CREATE DATABASE $VERIFY_DB;"

# Restore and verify
gunzip < $LATEST_BACKUP | mysql $VERIFY_DB

# Run verification queries
mysql $VERIFY_DB -e "
  SELECT COUNT(*) as player_count FROM players;
  SELECT COUNT(*) as active_duels FROM active_duels;
  SELECT SUM(withdrawable_galleons) as total_galleons FROM players;
"
```

## State Backups 🗃️

### ELIZAOS Memory State

```bash
# Location: /etc/cron.hourly/wox-state-backup.sh
#!/bin/bash

STATE_DIR="/var/backups/wizards-of-x/state"
DATE=$(date +%Y%m%d_%H)

# Backup ELIZAOS memory state
cp -r /opt/wizards-of-x/elizaos/memory $STATE_DIR/memory_$DATE
tar -czf $STATE_DIR/memory_$DATE.tar.gz $STATE_DIR/memory_$DATE
rm -rf $STATE_DIR/memory_$DATE

# Keep last 24 hours
find $STATE_DIR -name "memory_*.tar.gz" -mtime +1 -delete
```

### Active Game State

```python
# Location: /opt/wizards-of-x/utils/state_backup.py

import json
import os
from datetime import datetime
from game_logic.state_manager import GameStateManager

def backup_active_games():
    """Backup all active game states"""
    state_dir = "/var/backups/wizards-of-x/active_games"
    date_str = datetime.now().strftime("%Y%m%d_%H")
    
    # Get active states
    active_duels = GameStateManager.get_all_active_duels()
    active_tournaments = GameStateManager.get_all_active_tournaments()
    
    # Save states
    state = {
        "duels": active_duels,
        "tournaments": active_tournaments,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(f"{state_dir}/game_state_{date_str}.json", "w") as f:
        json.dump(state, f, indent=2)
    
    # Cleanup old backups (keep 24 hours)
    cleanup_old_states(state_dir)
```

## Configuration Backups ⚙️

### System Configuration

```bash
# Location: /etc/cron.daily/wox-config-backup.sh
#!/bin/bash

CONFIG_DIR="/var/backups/wizards-of-x/config"
DATE=$(date +%Y%m%d)

# Backup configuration files
tar -czf $CONFIG_DIR/config_$DATE.tar.gz \
  /opt/wizards-of-x/config \
  /etc/mysql/conf.d/wizards-of-x.cnf \
  /etc/nginx/sites-available/wizards-of-x \
  /etc/systemd/system/wizards-of-x.service

# Keep last 30 days
find $CONFIG_DIR -name "config_*.tar.gz" -mtime +30 -delete
```

### ELIZAOS Configuration

```bash
# Backup ELIZAOS specific configs
cp -r /opt/wizards-of-x/agents $CONFIG_DIR/agents_$DATE
tar -czf $CONFIG_DIR/agents_$DATE.tar.gz $CONFIG_DIR/agents_$DATE
rm -rf $CONFIG_DIR/agents_$DATE
```

## Recovery Procedures 🔄

### Database Recovery

1. **Full Database Restore**
```bash
# Stop game services
systemctl stop wizards-of-x

# Restore from latest backup
latest_backup=$(ls -t /var/backups/wizards-of-x/mysql/full_backup_*.sql.gz | head -1)
gunzip < $latest_backup | mysql wizards_of_x

# Verify restoration
mysql wizards_of_x -e "SELECT COUNT(*) FROM players;"

# Start services
systemctl start wizards-of-x
```

2. **Single Table Recovery**
```bash
# Example: Restore players table
latest_players=$(ls -t /var/backups/wizards-of-x/critical/players_*.sql.gz | head -1)
gunzip < $latest_players | mysql wizards_of_x
```

### State Recovery

1. **ELIZAOS Memory Recovery**
```bash
# Stop services
systemctl stop wizards-of-x

# Restore memory state
latest_memory=$(ls -t /var/backups/wizards-of-x/state/memory_*.tar.gz | head -1)
tar -xzf $latest_memory -C /opt/wizards-of-x/elizaos/

# Start services
systemctl start wizards-of-x
```

2. **Game State Recovery**
```python
from utils.state_recovery import GameStateRecovery

def recover_game_states():
    """Recover from latest game state backup"""
    recovery = GameStateRecovery()
    latest_state = recovery.get_latest_state_backup()
    
    # Restore active duels
    for duel in latest_state["duels"]:
        recovery.restore_duel(duel)
    
    # Restore tournaments
    for tournament in latest_state["tournaments"]:
        recovery.restore_tournament(tournament)
```

## Monitoring & Alerts 🔔

### Backup Monitoring

```python
# Location: /opt/wizards-of-x/monitoring/backup_monitor.py

from utils.discord_webhook import send_alert

def check_backup_status():
    """Monitor backup completion and integrity"""
    
    # Check backup age
    if backup_too_old():
        send_alert("CRITICAL: Database backup is outdated")
    
    # Verify backup integrity
    if not verify_backup_integrity():
        send_alert("WARNING: Latest backup integrity check failed")
    
    # Check backup size
    if backup_size_anomaly():
        send_alert("WARNING: Unusual backup size detected")
```

### Alert Configuration

```python
# Backup failure alerts
ALERT_CONFIGS = {
    "backup_failed": {
        "severity": "critical",
        "channel": "system-alerts",
        "retry_interval": 300  # 5 minutes
    },
    "integrity_check_failed": {
        "severity": "high",
        "channel": "system-alerts",
        "retry_interval": 600  # 10 minutes
    },
    "space_warning": {
        "severity": "medium",
        "channel": "system-alerts",
        "threshold": 85  # Percentage
    }
}
```

## Best Practices 📝

1. **Backup Verification**
   - Test restore procedures monthly
   - Verify backup integrity daily
   - Monitor backup sizes for anomalies
   - Keep backup logs for 90 days

2. **Security**
   - Encrypt sensitive backups
   - Use dedicated backup user
   - Restrict backup access
   - Monitor backup access logs

3. **Storage Management**
   - Monitor backup storage usage
   - Implement retention policies
   - Compress old backups
   - Archive historical data

4. **Documentation**
   - Keep recovery procedures updated
   - Document backup configurations
   - Maintain change logs
   - Record recovery tests

## Emergency Procedures 🚨

### Backup Failure Recovery

1. **Immediate Actions**
```bash
# Check system resources
df -h
free -m
top -n 1

# Check MySQL status
systemctl status mysql
mysqlcheck -A

# Verify backup permissions
ls -la /var/backups/wizards-of-x/
```

2. **Manual Backup Initiation**
```bash
# Force immediate backup
/usr/local/bin/wox-force-backup.sh

# Verify completion
tail -f /var/log/wizards-of-x/backup.log
```

### Corruption Recovery

1. **Database Corruption**
```bash
# Stop game services
systemctl stop wizards-of-x

# Check and repair tables
mysqlcheck -r wizards_of_x

# If repair fails, restore from backup
/usr/local/bin/wox-restore-backup.sh
```

2. **State Corruption**
```bash
# Backup corrupted state
mv /opt/wizards-of-x/elizaos/memory /opt/wizards-of-x/elizaos/memory_corrupted

# Restore from last known good state
/usr/local/bin/wox-restore-state.sh

# Verify game state
/usr/local/bin/wox-verify-state.sh
```

Remember: Regular testing of backup and recovery procedures is crucial. Schedule monthly recovery drills and keep all documentation updated! 🔄 