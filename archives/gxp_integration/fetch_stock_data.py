#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协鑫集成(002506.SZ) 股价数据获取脚本
使用 akshare 库获取股票数据

使用方法:
    python fetch_stock_data.py
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data():
    """获取协鑫集成股价数据"""
    print("📈 正在获取协鑫集成(002506.SZ) 股价数据...")
    
    try:
        # 获取日线数据 (近3个月)
        stock_df = ak.stock_zh_a_hist(
            symbol="002506", 
            period="daily", 
            start_date=(datetime.now() - timedelta(days=90)).strftime('%Y%m%d'),
            end_date=datetime.now().strftime('%Y%m%d'),
            adjust="qfq"  # 前复权
        )
        
        # 重命名列
        stock_df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'change_pct', 'change', 'turnover_rate']
        
        # 转换日期格式
        stock_df['date'] = pd.to_datetime(stock_df['date']).dt.strftime('%Y-%m-%d')
        
        # 保存CSV
        output_file = 'data/stock_price.csv'
        stock_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ 数据已保存到: {output_file}")
        print(f"📊 共获取 {len(stock_df)} 条记录")
        print(f"📅 数据范围: {stock_df['date'].min()} 至 {stock_df['date'].max()}")
        
        # 显示最近5条数据
        print("\n📉 最新5条数据:")
        print(stock_df.tail().to_string(index=False))
        
        return stock_df
        
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        print("💡 请确保已安装 akshare 库: pip install akshare")
        return None

if __name__ == "__main__":
    fetch_stock_data()
