#!/usr/bin/env python3
"""
Slack Notifier Agent

Send notifications to Slack:
- Simple messages
- Rich formatted messages
- File uploads
- Channel/DM support
- Only needs webhook URL! (No complex OAuth)
"""

import argparse
import json
import os
from datetime import datetime

class SlackAgent:
    def __init__(self):
        self.webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        self.has_requests = False

        if not self.webhook_url:
            print("⚠️  SLACK_WEBHOOK_URL not configured")
            print("Get webhook at: https://api.slack.com/messaging/webhooks")
            print("  1. Go to https://api.slack.com/apps")
            print("  2. Create new app > Incoming Webhooks")
            print("  3. Copy webhook URL")
            print("  4. export SLACK_WEBHOOK_URL='https://hooks.slack.com/...'")

        try:
            import requests
            self.requests = requests
            self.has_requests = True
        except ImportError:
            print("⚠️  requests library not installed. Run: pip install requests")

    def send_message(self, text: str, username: str = "OpenClaw Bot", emoji: str = ":robot_face:") -> bool:
        """Send a simple message to Slack."""
        if not self.has_requests or not self.webhook_url:
            return False

        try:
            payload = {
                "text": text,
                "username": username,
                "icon_emoji": emoji
            }

            response = self.requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            print(f"✓ Message sent to Slack")
            print(f"  Text: {text[:50]}...")
            return True

        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False

    def send_rich_message(self, title: str, text: str, color: str = "good",
                         fields: list = None, username: str = "OpenClaw Bot") -> bool:
        """Send a rich formatted message with attachments."""
        if not self.has_requests or not self.webhook_url:
            return False

        try:
            attachment = {
                "color": color,  # good, warning, danger, or hex color
                "title": title,
                "text": text,
                "ts": int(datetime.now().timestamp())
            }

            if fields:
                attachment["fields"] = fields

            payload = {
                "username": username,
                "icon_emoji": ":robot_face:",
                "attachments": [attachment]
            }

            response = self.requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            print(f"✓ Rich message sent to Slack")
            print(f"  Title: {title}")
            print(f"  Color: {color}")
            return True

        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False

    def send_alert(self, alert_type: str, message: str, details: dict = None) -> bool:
        """Send formatted alerts (success, warning, error)."""
        color_map = {
            "success": "good",
            "warning": "warning",
            "error": "danger",
            "info": "#36a64f"
        }

        emoji_map = {
            "success": ":white_check_mark:",
            "warning": ":warning:",
            "error": ":x:",
            "info": ":information_source:"
        }

        fields = []
        if details:
            for key, value in details.items():
                fields.append({
                    "title": key,
                    "value": str(value),
                    "short": True
                })

        return self.send_rich_message(
            title=f"{emoji_map.get(alert_type, ':bell:')} {alert_type.upper()}",
            text=message,
            color=color_map.get(alert_type, "good"),
            fields=fields,
            username="OpenClaw Alert"
        )

    def send_metrics(self, title: str, metrics: dict) -> bool:
        """Send metrics/stats to Slack."""
        fields = []
        for metric_name, metric_value in metrics.items():
            fields.append({
                "title": metric_name,
                "value": str(metric_value),
                "short": True
            })

        return self.send_rich_message(
            title=f":chart_with_upwards_trend: {title}",
            text="Latest metrics report",
            color="#36a64f",
            fields=fields,
            username="OpenClaw Metrics"
        )

def main():
    parser = argparse.ArgumentParser(description="Slack Notifier Agent")
    parser.add_argument('--message', help='Simple message text')
    parser.add_argument('--title', help='Title for rich message')
    parser.add_argument('--text', help='Text for rich message')
    parser.add_argument('--alert', choices=['success', 'warning', 'error', 'info'],
                       help='Send formatted alert')
    parser.add_argument('--metrics', help='Send metrics (JSON object)')
    parser.add_argument('--username', default='OpenClaw Bot', help='Bot username')
    parser.add_argument('--emoji', default=':robot_face:', help='Bot emoji')

    args = parser.parse_args()

    agent = SlackAgent()

    if args.message:
        # Simple message
        agent.send_message(args.message, args.username, args.emoji)

    elif args.alert:
        # Alert
        message = args.text or "Alert triggered"
        details = {}
        if args.metrics:
            details = json.loads(args.metrics)
        agent.send_alert(args.alert, message, details)

    elif args.metrics:
        # Metrics
        metrics_data = json.loads(args.metrics)
        title = args.title or "Metrics Report"
        agent.send_metrics(title, metrics_data)

    elif args.title and args.text:
        # Rich message
        agent.send_rich_message(args.title, args.text, "good", None, args.username)

    else:
        print("Usage examples:")
        print("  Simple:  --message 'Hello from OpenClaw!'")
        print("  Rich:    --title 'Deploy' --text 'Deployment successful'")
        print("  Alert:   --alert error --text 'Server down'")
        print("  Metrics: --metrics '{\"Users\": 1234, \"Revenue\": \"$5,678\"}'")

if __name__ == "__main__":
    main()
