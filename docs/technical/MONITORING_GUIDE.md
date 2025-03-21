# Wizards of X: Monitoring Guide 📊

## System Monitoring Overview

This guide outlines the monitoring setup for Wizards of X, covering system health, game economy, and alert configurations.

## Infrastructure Monitoring 🖥️

### VM Resources

```python
# Location: /opt/wizards-of-x/monitoring/vm_monitor.py

import psutil
from utils.discord_webhook import send_alert

def check_vm_resources():
    """Monitor VM resource usage"""
    
    # CPU Usage
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        send_alert(
            "HIGH CPU USAGE",
            f"CPU at {cpu_percent}%",
            severity="warning"
        )
    
    # Memory Usage
    memory = psutil.virtual_memory()
    if memory.percent > 85:
        send_alert(
            "HIGH MEMORY USAGE",
            f"Memory at {memory.percent}%",
            severity="warning"
        )
    
    # Disk Usage
    disk = psutil.disk_usage('/')
    if disk.percent > 85:
        send_alert(
            "LOW DISK SPACE",
            f"Disk usage at {disk.percent}%",
            severity="warning"
        )
```

### Database Performance

```python
# Location: /opt/wizards-of-x/monitoring/db_monitor.py

import mysql.connector
from utils.config import get_db_config

def monitor_database():
    """Monitor database performance metrics"""
    
    conn = mysql.connector.connect(**get_db_config())
    cursor = conn.cursor()
    
    # Check connection count
    cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
    connections = int(cursor.fetchone()[1])
    if connections > 100:
        send_alert("High DB Connections", f"Current: {connections}")
    
    # Check slow queries
    cursor.execute("SHOW GLOBAL STATUS LIKE 'Slow_queries'")
    slow_queries = int(cursor.fetchone()[1])
    if slow_queries > 0:
        send_alert("Slow Queries Detected", f"Count: {slow_queries}")
    
    # Check table sizes
    cursor.execute("""
        SELECT table_name, table_rows, data_length/1024/1024 'Data MB'
        FROM information_schema.tables
        WHERE table_schema = 'wizards_of_x'
    """)
    
    for table in cursor.fetchall():
        if table[2] > 1000:  # 1GB
            send_alert(f"Large Table Warning: {table[0]}")
```

## Game Monitoring 🎮

### Active Games Monitor

```python
# Location: /opt/wizards-of-x/monitoring/game_monitor.py

from game_logic.state_manager import GameStateManager

def monitor_active_games():
    """Monitor active duels and tournaments"""
    
    # Check active duels
    active_duels = GameStateManager.get_all_active_duels()
    if len(active_duels) > 100:
        send_alert("High number of active duels", f"Count: {len(active_duels)}")
    
    # Check for stuck duels
    stuck_duels = [d for d in active_duels if d.is_stuck()]
    if stuck_duels:
        send_alert("Stuck duels detected", f"Count: {len(stuck_duels)}")
    
    # Monitor tournament progress
    active_tournaments = GameStateManager.get_all_active_tournaments()
    for tournament in active_tournaments:
        if tournament.is_delayed():
            send_alert(
                "Tournament Delay",
                f"ID: {tournament.id}, Delay: {tournament.delay_minutes}m"
            )
```

### Tweet Processing Monitor

```python
# Location: /opt/wizards-of-x/monitoring/tweet_monitor.py

from elizaos.metrics import get_processing_stats

def monitor_tweet_processing():
    """Monitor tweet processing performance"""
    
    stats = get_processing_stats()
    
    # Check processing rate
    if stats.tweets_per_minute < 10:
        send_alert("Low tweet processing rate")
    
    # Check error rate
    if stats.error_rate > 0.05:  # 5%
        send_alert("High tweet processing error rate")
    
    # Check response time
    if stats.avg_response_time > 2.0:  # 2 seconds
        send_alert("High tweet response time")
    
    # Monitor rate limits
    if stats.rate_limit_remaining < 100:
        send_alert("Rate limit warning")
```

## Economy Monitoring 💰

### Transaction Monitor

```python
# Location: /opt/wizards-of-x/monitoring/transaction_monitor.py

from banking.transaction_manager import TransactionManager

def monitor_transactions():
    """Monitor transaction processing and verification"""
    
    # Check pending transactions
    pending = TransactionManager.get_pending_transactions()
    if len(pending) > 50:
        send_alert("High number of pending transactions")
    
    # Check failed transactions
    failed = TransactionManager.get_failed_transactions(last_hours=1)
    if len(failed) > 10:
        send_alert("High transaction failure rate")
    
    # Monitor confirmation times
    avg_time = TransactionManager.get_avg_confirmation_time()
    if avg_time > 300:  # 5 minutes
        send_alert("Slow transaction confirmations")
```

### Prize Pool Monitor

```python
# Location: /opt/wizards-of-x/monitoring/economy_monitor.py

from banking.prize_pool import PrizePoolManager
from banking.burn_queue import BurnQueueManager

def monitor_economy():
    """Monitor game economy metrics"""
    
    # Check prize pool
    pool = PrizePoolManager.get_current_pool()
    if pool.balance < 1000:
        send_alert("Low prize pool balance")
    
    # Monitor burn queue
    burn_queue = BurnQueueManager.get_queue_status()
    if burn_queue.pending_amount > 10000:
        send_alert("Large burn queue pending")
    
    # Check economy ratios
    ratios = calculate_economy_ratios()
    if ratios.inflation_rate > 0.1:  # 10%
        send_alert("High inflation rate detected")
```

## Alert System 🔔

### Discord Webhook Configuration

```python
# Location: /opt/wizards-of-x/config/alerts.py

DISCORD_WEBHOOKS = {
    "critical": "https://discord.com/api/webhooks/...",
    "high": "https://discord.com/api/webhooks/...",
    "medium": "https://discord.com/api/webhooks/...",
    "low": "https://discord.com/api/webhooks/..."
}

ALERT_CHANNELS = {
    "system": {
        "webhook": DISCORD_WEBHOOKS["critical"],
        "mention_role": "system-admin"
    },
    "game": {
        "webhook": DISCORD_WEBHOOKS["high"],
        "mention_role": "game-master"
    },
    "economy": {
        "webhook": DISCORD_WEBHOOKS["high"],
        "mention_role": "economy-admin"
    }
}
```

### Alert Thresholds

```python
# System thresholds
SYSTEM_THRESHOLDS = {
    "cpu_usage": 80,
    "memory_usage": 85,
    "disk_usage": 85,
    "db_connections": 100,
    "response_time": 2.0
}

# Game thresholds
GAME_THRESHOLDS = {
    "max_active_duels": 100,
    "duel_timeout": 300,  # 5 minutes
    "tournament_delay": 300,  # 5 minutes
    "stuck_duel_count": 10
}

# Economy thresholds
ECONOMY_THRESHOLDS = {
    "min_prize_pool": 1000,
    "max_burn_queue": 10000,
    "max_pending_tx": 50,
    "tx_confirmation_time": 300  # 5 minutes
}
```

## Monitoring Dashboard 📈

### Grafana Setup

```ini
# Location: /etc/grafana/provisioning/dashboards/wizards.yaml

apiVersion: 1

providers:
  - name: 'Wizards of X'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /var/lib/grafana/dashboards
```

### Dashboard Panels

1. **System Health**
```
- CPU Usage (Line graph)
- Memory Usage (Line graph)
- Disk Usage (Gauge)
- Database Connections (Line graph)
```

2. **Game Metrics**
```
- Active Duels (Counter)
- Tournament Status (Table)
- Tweet Processing Rate (Line graph)
- Error Rate (Line graph)
```

3. **Economy Metrics**
```
- Prize Pool Balance (Line graph)
- Burn Queue Size (Counter)
- Transaction Volume (Bar graph)
- Confirmation Times (Histogram)
```

## Automated Reports 📧

### Daily System Report

```python
# Location: /opt/wizards-of-x/reporting/daily_report.py

def generate_daily_report():
    """Generate daily system health report"""
    
    report = {
        "system": get_system_metrics(),
        "game": get_game_metrics(),
        "economy": get_economy_metrics(),
        "alerts": get_daily_alerts()
    }
    
    # Format report
    markdown = format_report_markdown(report)
    
    # Send to Discord
    send_report_to_discord(markdown, channel="daily-reports")
```

### Weekly Economy Report

```python
def generate_weekly_economy():
    """Generate weekly economy report"""
    
    report = {
        "transactions": analyze_weekly_transactions(),
        "prize_pool": analyze_prize_distribution(),
        "burn_queue": analyze_burn_metrics(),
        "player_economy": analyze_player_metrics()
    }
    
    # Generate visualizations
    charts = generate_economy_charts(report)
    
    # Send report
    send_economy_report(report, charts)
```

## Best Practices 📝

### 1. Alert Management
- Set appropriate thresholds
- Avoid alert fatigue
- Use severity levels
- Implement alert aggregation

### 2. Performance Monitoring
- Monitor trends over time
- Set baseline metrics
- Track seasonal patterns
- Monitor rate limits

### 3. Data Collection
- Use appropriate intervals
- Implement data retention
- Monitor collector health
- Validate data accuracy

### 4. Response Procedures
1. **Critical Alerts**
   - Immediate response required
   - Follow incident playbook
   - Update status page
   - Post-incident review

2. **Warning Alerts**
   - Investigate within 1 hour
   - Document findings
   - Plan preventive actions
   - Monitor resolution

3. **Info Alerts**
   - Review daily
   - Track patterns
   - Update thresholds
   - Document changes

## Troubleshooting Guide 🔧

### Common Issues

1. **High CPU Usage**
```bash
# Check top processes
top -b -n 1 | head -n 20

# Check system load
uptime

# Monitor specific process
ps aux | grep wizards-of-x
```

2. **Database Issues**
```sql
-- Check slow queries
SHOW FULL PROCESSLIST;

-- Analyze table sizes
SELECT 
    table_name,
    table_rows,
    data_length/1024/1024 as 'Data MB'
FROM information_schema.tables
WHERE table_schema = 'wizards_of_x'
ORDER BY data_length DESC;
```

3. **Network Issues**
```bash
# Check network stats
netstat -an | grep ESTABLISHED | wc -l

# Monitor network traffic
iftop -i eth0
```

Remember: Regular monitoring and proactive maintenance are key to system stability! 🔍 