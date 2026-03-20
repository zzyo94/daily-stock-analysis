#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily stock position analysis
"""

import urllib.request
import json
import datetime

PORTFOLIO = {
    "01810.HK": {
        "name": "XiaoMi",
        "cost": 37.65,
        "reason": "long-term"
    },
    "300474.SZ": {
        "name": "JingJiaWei",
        "cost": 68.5,
        "reason": "GPU leader"
    }
}

def get_stock_price(code):
    """Get stock price from Sina"""
    try:
        if code.endswith('.HK'):
            url = f"https://hq.sinajs.cn/list=hk{code.split('.')[0]}"
        else:
            url = f"https://hq.sinajs.cn/list={code}"
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn/"
        })
        r = urllib.request.urlopen(req, timeout=10)
        data = r.read().decode("gbk")
        
        parts = data.split('="')[1].split('"')[0].split(',')
        current = float(parts[1])
        prev = float(parts[2])
        change_pct = ((current - prev) / prev) * 100
        
        return {"current": current, "prev": prev, "change_pct": change_pct}
    except Exception as e:
        return {"error": str(e)}

def generate_report():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"Daily Position Report {now}\n"
    report += "=" * 30 + "\n\n"
    
    for code, info in PORTFOLIO.items():
        data = get_stock_price(code)
        if "error" in data:
            report += f"{info['name']}: Error - {data['error']}\n\n"
        else:
            profit = data["current"] - info["cost"]
            profit_pct = (profit / info["cost"]) * 100
            icon = "📈" if profit_pct > 0 else "📉"
            report += f"{info['name']} ({code})\n"
            report += f"  Price: {data['current']:.2f} ({data['change_pct']:+.2f}%)\n"
            report += f"  Cost: {info['cost']:.2f}\n"
            report += f"  P/L: {icon} {profit_pct:+.2f}%\n\n"
    
    return report

if __name__ == "__main__":
    print(generate_report())
