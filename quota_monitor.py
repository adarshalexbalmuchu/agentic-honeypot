#!/usr/bin/env python3
"""
Quota monitoring tool for the agentic honeypot API
"""

import sys
sys.path.append('/workspaces/agentic-honeypot')

from app.agent import llm_client

def display_quota_status():
    """Display current quota usage in a readable format"""
    status = llm_client.get_quota_status()
    
    print("🚦 API QUOTA MONITORING")
    print("=" * 50)
    
    for model, info in status.items():
        usage = info['requests_last_minute']
        limit = info['rpm_limit']
        utilization = info['utilization_percent']
        
        # Color coding based on utilization
        if utilization >= 80:
            status_icon = "🔴"  # Red - high usage
        elif utilization >= 50:
            status_icon = "🟡"  # Yellow - moderate usage
        else:
            status_icon = "🟢"  # Green - low usage
            
        print(f"{status_icon} {model}")
        print(f"   RPM Usage: {usage}/{limit} ({utilization}%)")
        
        # Show bar graph
        bar_length = 20
        filled = int((usage / limit) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}]")
        print()

if __name__ == "__main__":
    display_quota_status()