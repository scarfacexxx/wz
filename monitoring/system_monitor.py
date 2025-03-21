import psutil
import mysql.connector
from datetime import datetime
import json
from typing import Dict, List
import logging

class SystemMonitor:
    def __init__(self, discord_webhook_url: str, db_config: Dict):
        self.discord_webhook_url = discord_webhook_url
        self.db_config = db_config
        self.logger = logging.getLogger('wizards_of_x.monitor')
        
    def check_system_health(self) -> Dict:
        """Check overall system health."""
        return {
            'vm': self._check_vm_resources(),
            'database': self._check_database_health(),
            'game': self._check_game_metrics()
        }
        
    def _check_vm_resources(self) -> Dict:
        """Monitor VM resource usage."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = 'healthy'
        alerts = []
        
        if cpu_percent > 80:
            status = 'warning'
            alerts.append('High CPU usage')
            
        if memory.percent > 80:
            status = 'warning'
            alerts.append('High memory usage')
            
        if disk.percent > 80:
            status = 'warning'
            alerts.append('Low disk space')
            
        return {
            'status': status,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'alerts': alerts
        }
        
    def _check_database_health(self) -> Dict:
        """Check database performance and connections."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check connection count
            cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
            connections = int(cursor.fetchone()[1])
            
            # Check slow queries
            cursor.execute("SHOW STATUS LIKE 'Slow_queries'")
            slow_queries = int(cursor.fetchone()[1])
            
            status = 'healthy'
            alerts = []
            
            if connections > 80:  # Assuming 100 max connections
                status = 'warning'
                alerts.append('High connection count')
                
            if slow_queries > 100:  # Threshold for slow queries
                status = 'warning'
                alerts.append('High number of slow queries')
                
            cursor.close()
            conn.close()
            
            return {
                'status': status,
                'connections': connections,
                'slow_queries': slow_queries,
                'alerts': alerts
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'alerts': ['Database connection failed']
            }
            
    def _check_game_metrics(self) -> Dict:
        """Monitor game-specific metrics."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check active duels
            cursor.execute("SELECT COUNT(*) FROM active_duels WHERE status = 'active'")
            active_duels = cursor.fetchone()[0]
            
            # Check pending transactions
            cursor.execute(
                "SELECT COUNT(*) FROM withdrawal_requests WHERE status = 'pending'"
            )
            pending_withdrawals = cursor.fetchone()[0]
            
            # Check prize pool
            cursor.execute("SELECT SUM(amount) FROM prize_pool")
            prize_pool = cursor.fetchone()[0] or 0
            
            # Check burn queue
            cursor.execute(
                "SELECT COUNT(*), SUM(amount) FROM burn_queue WHERE status = 'pending'"
            )
            burn_queue = cursor.fetchone()
            pending_burns = burn_queue[0]
            burn_amount = burn_queue[1] or 0
            
            status = 'healthy'
            alerts = []
            
            if active_duels > 100:  # Arbitrary threshold
                alerts.append('High number of active duels')
                
            if pending_withdrawals > 50:  # Arbitrary threshold
                alerts.append('High number of pending withdrawals')
                
            if pending_burns > 100:  # Arbitrary threshold
                alerts.append('Large burn queue')
                
            cursor.close()
            conn.close()
            
            return {
                'status': status,
                'active_duels': active_duels,
                'pending_withdrawals': pending_withdrawals,
                'prize_pool': prize_pool,
                'pending_burns': pending_burns,
                'burn_amount': burn_amount,
                'alerts': alerts
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'alerts': ['Failed to fetch game metrics']
            }
            
    def send_alert(self, alert_type: str, message: str, details: Dict = None):
        """Send alert to Discord."""
        if not self.discord_webhook_url:
            return
            
        emoji_map = {
            'error': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        emoji = emoji_map.get(alert_type, 'ℹ️')
        
        alert_message = (
            f"{emoji} **{alert_type.upper()}**\n"
            f"{message}\n"
        )
        
        if details:
            alert_message += f"```json\n{json.dumps(details, indent=2)}\n```"
            
        # TODO: Implement Discord webhook notification
        pass
        
    def log_metrics(self, metrics: Dict):
        """Log metrics for historical tracking."""
        timestamp = datetime.now()
        
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Insert system metrics
            cursor.execute(
                """
                INSERT INTO system_metrics (
                    timestamp, cpu_percent, memory_percent, disk_percent,
                    db_connections, slow_queries, active_duels,
                    pending_withdrawals, prize_pool, pending_burns
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    timestamp,
                    metrics['vm']['cpu_percent'],
                    metrics['vm']['memory_percent'],
                    metrics['vm']['disk_percent'],
                    metrics['database']['connections'],
                    metrics['database']['slow_queries'],
                    metrics['game']['active_duels'],
                    metrics['game']['pending_withdrawals'],
                    metrics['game']['prize_pool'],
                    metrics['game']['pending_burns']
                )
            )
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to log metrics: {e}")
            self.send_alert('error', 'Failed to log system metrics', {'error': str(e)}) 