import os
import psutil
import logging
from typing import Dict, Any
from discord_webhook import DiscordWebhook

logger = logging.getLogger(__name__)

class MonitoringSystem:
    def __init__(self):
        # Discord webhooks
        self.error_webhook = os.getenv('DISCORD_ERROR_WEBHOOK')
        self.info_webhook = os.getenv('DISCORD_INFO_WEBHOOK')
        self.alert_webhook = os.getenv('DISCORD_ALERT_WEBHOOK')
        
        # Alert thresholds
        self.thresholds = {
            'cpu_usage': 80.0,  # 80%
            'memory_usage': 85.0,  # 85%
            'disk_usage': 90.0,  # 90%
            'response_time': 1000,  # 1000ms
            'min_prize_pool': 1000,  # 1000 Galleons
            'max_pending_tx': 100  # 100 transactions
        }
        
        # Metrics history (144 points = 12 hours at 5-min intervals)
        self.metrics_history = {
            'cpu_usage': [],
            'memory_usage': [],
            'disk_usage': [],
            'response_time': [],
            'active_players': [],
            'prize_pool': []
        }
        self.history_limit = 144

    def update_metrics(self):
        """Collect and store current metrics"""
        try:
            # System metrics
            metrics = self._collect_system_metrics()
            
            # Store metrics
            for key, value in metrics.items():
                if key in self.metrics_history:
                    self.metrics_history[key].append(value)
                    # Keep only last N points
                    if len(self.metrics_history[key]) > self.history_limit:
                        self.metrics_history[key].pop(0)
            
            # Check thresholds
            self._check_alerts(metrics)
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
            self._send_alert("Error collecting metrics", str(e), "error")

    def _collect_system_metrics(self) -> Dict[str, float]:
        """Collect system performance metrics"""
        try:
            return {
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'response_time': self._get_response_time()
            }
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}

    def _get_response_time(self) -> float:
        """Measure tweet response time"""
        # ELIZAOS handles this internally
        # We just need to monitor it
        return 0.0

    def _check_alerts(self, metrics: Dict[str, float]):
        """Check metrics against thresholds"""
        for metric, value in metrics.items():
            threshold = self.thresholds.get(metric)
            if threshold and value > threshold:
                self._send_alert(
                    f"High {metric}",
                    f"{metric} is at {value}% (threshold: {threshold}%)",
                    "alert"
                )

    def _send_alert(self, title: str, message: str, level: str = "info"):
        """Send alert to Discord"""
        try:
            webhook_url = getattr(self, f"{level}_webhook", None)
            if webhook_url:
                webhook = DiscordWebhook(
                    url=webhook_url,
                    content=f"**{title}**\n{message}"
                )
                webhook.execute()
        except Exception as e:
            logger.error(f"Error sending alert: {e}") 