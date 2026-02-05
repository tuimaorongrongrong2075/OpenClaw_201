#!/usr/bin/env python3
"""
RSS 订阅管理器 - 纯 Python 实现
"""
import urllib.request
import ssl
import os
from datetime import datetime
import xml.etree.ElementTree as ET

# 创建一个 SSL 上下文来忽略证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# RSS 订阅列表
RSS_FEEDS = [
    {
        "name": "KrebsOnSecurity",
        "url": "https://krebsonsecurity.com/feed/",
        "category": "安全研究"
    },
    {
        "name": "Daring Fireball",
        "url": "https://daringfireball.net/feeds/main",
        "category": "技术博客"
    },
    {
        "name": "Jeff Geerling",
        "url": "https://www.jeffgeerling.com/blog.xml",
        "category": "树莓派/DevOps"
    },
    {
        "name": "Timsh.org",
        "url": "https://timsh.org/rss/",
        "category": "技术"
    },
]

def fetch_feed(feed_url):
    """获取 RSS 订阅"""
    try:
        with urllib.request.urlopen(feed_url, context=ssl_context, timeout=30) as response:
            content = response.read().decode('utf-8')
        return content
    except Exception as e:
        print(f"❌ Error fetching {feed_url}: {e}")
        return None

def parse_rss(content):
    """解析 RSS/Atom 格式"""
    try:
        # 尝试 RSS 2.0
        root = ET.fromstring(content)
        items = []
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            desc = item.find('description') or item.find('summary') or item.find('content')
            items.append({
                'title': title.text if title is not None else 'No title',
                'link': link.text if link is not None else '',
                'summary': (desc.text[:200] if desc is not None and desc.text else '') + '...'
            })
        return items
    except Exception as e:
        # 尝试 Atom
        try:
            root = ET.fromstring(content)
            entries = root.findall('.//entry')
            items = []
            for entry in entries:
                title = entry.find('title')
                link_elem = entry.find('link')
                link = link_elem.get('href') if link_elem is not None else ''
                summary = entry.find('summary') or entry.find('content')
                items.append({
                    'title': title.text if title is not None else 'No title',
                    'link': link,
                    'summary': (summary.text[:200] if summary is not None and summary.text else '') + '...'
                })
            return items
        except Exception as e2:
            print(f"   ⚠️ Parse error: {e2}")
            return []

def scan_feeds():
    """扫描所有 RSS 订阅"""
    print("📰 扫描 RSS 订阅...\n")
    
    all_articles = []
    
    for feed_info in RSS_FEEDS:
        print(f"🔍 {feed_info['name']}...")
        content = fetch_feed(feed_info['url'])
        
        if content:
            articles = parse_rss(content)
            print(f"   📄 获取到 {len(articles)} 篇文章")
            for article in articles[:3]:  # 只取前3篇
                article['source'] = feed_info['name']
                article['category'] = feed_info['category']
                all_articles.append(article)
        else:
            print(f"   ❌ 获取失败")
        print()
    
    return all_articles

def generate_html(articles):
    """生成 HTML 页面"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS 订阅更新 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #1a1a1b;
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 10px;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
        }}
        .articles {{
            display: grid;
            gap: 20px;
        }}
        .article {{
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
            transition: transform 0.2s;
        }}
        .article:hover {{
            transform: translateX(10px);
        }}
        .source {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        .category {{
            background: #764ba2;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        .title {{
            font-size: 1.2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .title a {{
            color: #1a1a1b;
            text-decoration: none;
        }}
        .title a:hover {{
            color: #667eea;
        }}
        .summary {{
            color: #666;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #999;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 RSS 订阅更新</h1>
        
        <div class="stats">
            <div>
                <div class="stat-value">{len(RSS_FEEDS)}</div>
                <div class="stat-label">订阅源</div>
            </div>
            <div>
                <div class="stat-value">{len(articles)}</div>
                <div class="stat-label">最新文章</div>
            </div>
        </div>
        
        <div class="articles">
"""
    
    for i, article in enumerate(articles, 1):
        html += f"""
            <div class="article">
                <span class="source">{article['source']}</span>
                <span class="category">{article['category']}</span>
                <div class="title">
                    <a href="{article['link']}" target="_blank">{article['title']}</a>
                </div>
                <div class="summary">{article['summary']}</div>
            </div>
"""
    
    html += f"""
        </div>
        
        <div class="footer">
            📰 自动更新 | {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    print("=" * 50)
    print("📰 RSS 订阅管理器")
    print("=" * 50 + "\n")
    
    # 扫描订阅
    articles = scan_feeds()
    
    # 生成 HTML
    html_content = generate_html(articles)
    
    # 保存到文件
    output_file = "/root/.openclaw/workspace/docs/rss_feeds.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("=" * 50)
    print(f"✅ RSS 更新已生成！")
    print(f"📄 文件: {output_file}")
    print(f"📰 文章数: {len(articles)}")
    print("=" * 50)

if __name__ == "__main__":
    main()
