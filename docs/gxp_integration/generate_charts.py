#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协鑫集成(002506.SZ) 股价走势图生成脚本

使用方法:
    python generate_charts.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def generate_charts():
    """生成股价走势图"""
    print("📊 正在生成股价走势图...")
    
    try:
        # 读取数据
        df = pd.read_csv('data/stock_price.csv')
        df['date'] = pd.to_datetime(df['date'])
        
        # 设置日期为索引
        df.set_index('date', inplace=True)
        
        # 创建图表
        fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # 1. 股价走势图
        ax1 = axes[0]
        ax1.plot(df.index, df['close'], 'b-', linewidth=1.5, label='收盘价')
        ax1.fill_between(df.index, df['low'], df['high'], alpha=0.3, color='blue', label='最高-最低区间')
        ax1.plot(df.index, df['close'], 'ro-', markersize=3, linewidth=1, alpha=0.7, label='收盘价(点)')
        
        # 添加移动平均线 (MA5, MA10, MA20)
        if len(df) >= 5:
            df['MA5'] = df['close'].rolling(window=5).mean()
            ax1.plot(df.index, df['MA5'], 'g--', linewidth=1, alpha=0.8, label='MA5')
        if len(df) >= 10:
            df['MA10'] = df['close'].rolling(window=10).mean()
            ax1.plot(df.index, df['MA10'], 'm--', linewidth=1, alpha=0.8, label='MA10')
        if len(df) >= 20:
            df['MA20'] = df['close'].rolling(window=20).mean()
            ax1.plot(df.index, df['MA20'], 'c--', linewidth=1, alpha=0.8, label='MA20')
        
        ax1.set_title('协鑫集成(002506.SZ) 股价走势', fontsize=16, fontweight='bold')
        ax1.set_ylabel('股价 (CNY)', fontsize=12)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 2. 成交量图
        ax2 = axes[1]
        colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' for i in range(len(df))]
        ax2.bar(df.index, df['volume']/10000, color=colors, alpha=0.7, width=0.8)
        ax2.set_title('成交量', fontsize=12)
        ax2.set_ylabel('成交量 (万手)', fontsize=10)
        ax2.set_xlabel('日期', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.setp(ax2.x_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # 保存图表
        output_file = 'charts/price_trend.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ 图表已保存到: {output_file}")
        
        # 基本统计信息
        print("\n📈 基本统计:")
        print(f"  最高价: {df['high'].max():.2f} CNY")
        print(f"  最低价: {df['low'].min():.2f} CNY")
        print(f"  平均价: {df['close'].mean():.2f} CNY")
        print(f"  成交量: {df['volume'].mean()/10000:.2f} 万手")
        
    except Exception as e:
        print(f"❌ 生成图表失败: {e}")
        print("💡 请先运行 fetch_stock_data.py 获取数据")

if __name__ == "__main__":
    generate_charts()
