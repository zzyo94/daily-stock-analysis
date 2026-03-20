#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily market analysis
"""

import urllib.request
import json
import datetime

def get_index(code, name):
    """Get index data from Sina"""
    try:
        url = f"https://hq.sinajs.cn/list={code}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn/"
        })
        r = urllib.request.urlopen(req, timeout=10)
        data = r.read().decode("gbk")
        
        parts = data.split('="')[1].split('"')[0].split(',')
        current = float(parts[1])
        change = float(parts[2])
        change_pct = float(parts[3])
        
        return {"name": name, "current": current, "change": change, "change_pct": change_pct}
    except Exception as e:
        return {"name": name, "error": str(e)}

def generate_report():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"Market Report {now}\n"
    report += "=" * 35 + "\n\n"
    
    indices = [
        ("sh000001", "Shanghai"),
        ("sz399001", "Shenzhen"),
        ("sz399006", "ChiNext"),
    ]
    
    report += "【A-Share】\n"
    for code, name in indices:
        data = get_index(code, name)
        if "error" in data:
            report += f"  {name}: Error\n"
        else:
            icon = "📈" if data["change_pct"] > 0 else "📉"
            report += f"  {icon} {name}: {data['current']:.2f} ({data['change_pct']:+.2f}%)\n"
    
    report += "\n"
    report += "=" * 35 + "\n"
    
    return report

if __name__ == "__main__":
    print(generate_report())
