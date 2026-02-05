#!/usr/bin/env python3
"""
🦞 小猩的 Gmail 摘要机器人
功能：读取邮件 → 生成摘要 → 发送简报
"""

import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from email.header import decode_header
from datetime import datetime, timedelta
import json
import hashlib
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import gmail_email, gmail_password

# ============== 配置 ==============
EMAIL = gmail_email()
PASSWORD = gmail_password()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 收件人
TO_EMAILS = []

# 邮件过滤关键词（重要邮件）
IMPORTANT_KEYWORDS = [
    "github", "polymarket", "openclaw", "code", "project", "task",
    "deadline", "meeting", "review", "important", "urgent",
    "report", "summary", "analysis", "task", "action"
]

# 忽略的邮件（垃圾/推广）
IGNORE_KEYWORDS = [
    "newsletter", "promo", "sale", "discount", "offer", "deal",
    "marketing", "advertising", "unsubscribe", "click here",
    "buy now", "limited time", "free gift"
]

# ============== 工具函数 ==============

def decode_str(header_value):
    """解码邮件头"""
    if not header_value:
        return ""
    decoded_list = decode_header(header_value)
    decoded_str = ""
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            decoded_str += content.decode(encoding or 'utf-8', errors='ignore')
        else:
            decoded_str += str(content)
    return decoded_str

def clean_text(text):
    """清理邮件正文"""
    if not text:
        return ""
    # 移除多余空白
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)[:2000]  # 限制长度

def classify_email(subject, from_addr, content):
    """分类邮件"""
    text = (subject + " " + from_addr + " " + content).lower()
    
    # 检查是否忽略
    for kw in IGNORE_KEYWORDS:
        if kw in text:
            return "ignore"
    
    # 检查是否重要
    for kw in IMPORTANT_KEYWORDS:
        if kw in text:
            return "important"
    
    return "normal"

def get_email_body(msg):
    """提取邮件正文"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True)
                    body = clean_text(body.decode('utf-8', errors='ignore'))
                except:
                    pass
                break
    else:
        try:
            body = msg.get_payload(decode=True)
            body = clean_text(body.decode('utf-8', errors='ignore'))
        except:
            pass
    return body

# ============== 核心功能 ==============

def fetch_emails(hours=24, limit=50):
    """获取最近邮件"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(EMAIL, PASSWORD)
        mail.select("INBOX")
        
        # 搜索最近 N 小时的邮件
        since = (datetime.now() - timedelta(hours=hours)).strftime("%d-%b-%Y")
        typ, data = mail.search(None, f'SINCE {since}')
        email_ids = data[0].split()
        
        recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
        print(f"📧 获取到 {len(recent_ids)} 封最近邮件")
        
        emails = []
        for eid in reversed(recent_ids):
            typ, msg_data = mail.fetch(eid, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = decode_str(msg['Subject'])
            from_addr = decode_str(msg['From'])
            date_str = msg['Date']
            
            # 提取正文
            body = get_email_body(msg)
            
            # 分类
            category = classify_email(subject, from_addr, body)
            
            emails.append({
                'id': eid.decode() if isinstance(eid, bytes) else str(eid),
                'subject': subject,
                'from': from_addr,
                'date': date_str,
                'body': body[:300],
                'category': category
            })
        
        mail.logout()
        return emails
        
    except Exception as e:
        print(f"❌ 获取邮件失败: {e}")
        return []

def generate_summary(emails):
    """生成摘要（基于规则）"""
    important = [e for e in emails if e['category'] == 'important']
    normal = [e for e in emails if e['category'] == 'normal']
    ignored = [e for e in emails if e['category'] == 'ignore']
    
    summary = {
        'total': len(emails),
        'important_count': len(important),
        'important': important[:5],  # 只显示前5封重要邮件
        'normal_count': len(normal),
        'ignored_count': len(ignored)
    }
    
    return summary

def format_report(emails, summary):
    """格式化报告"""
    report = f"""
{'='*60}
🦞 小猩的 Gmail 邮件摘要
{'='*60}
📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📧 总邮件数: {summary['total']}
  ⭐ 重要邮件: {summary['important_count']}
  📝 普通邮件: {summary['normal_count']}
  🗑️ 已忽略: {summary['ignored_count']}

"""

    # 重要邮件详情
    if summary['important']:
        report += f"{'⭐'*2} 重要邮件 ({len(summary['important'])} 封)\n"
        report += f"{'-'*60}\n"
        for i, e in enumerate(summary['important'], 1):
            report += f"""
{i}. {e['subject']}
   发件人: {e['from'][:40]}
   摘要: {e['body'][:150]}...
"""
        report += "\n"
    
    # 统计信息
    froms = {}
    for e in emails:
        if e['category'] != 'ignore':
            name = e['from'].split('<')[0].strip() or "Unknown"
            froms[name] = froms.get(name, 0) + 1
    
    if froms:
        top_senders = sorted(froms.items(), key=lambda x: x[1], reverse=True)[:5]
        report += f"{'📊'*2} 频繁发件人 TOP 5\n"
        report += f"{'-'*60}\n"
        for name, count in top_senders:
            report += f"  • {name}: {count} 封\n"
    
    report += f"""
{'='*60}
💚 来自小猩的摘要服务
如果您想调整过滤规则，请告诉小猩！
{'='*60}
"""
    return report

def send_report(report, to_email):
    """发送报告到邮箱"""
    try:
        msg = MIMEText(report, 'plain', 'utf-8')
        msg['From'] = f"小猩 <{EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = f"📧 小猩邮件摘要 - {datetime.now().strftime('%Y-%m-%d')}"
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        server.quit()
        
        print(f"✅ 报告已发送到 {to_email}")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

# ============== 主程序 ==============

def main():
    print("\n" + "="*60)
    print("🦞 小猩 Gmail 摘要机器人")
    print("="*60 + "\n")
    
    # 1. 获取邮件
    print("📥 正在获取邮件...")
    emails = fetch_emails(hours=24, limit=100)
    
    if not emails:
        print("😴 没有新邮件")
        return
    
    # 2. 生成摘要
    print("📝 正在生成摘要...")
    summary = generate_summary(emails)
    
    # 3. 格式化报告
    report = format_report(emails, summary)
    
    # 4. 显示报告
    print(report)
    
    # 5. 发送到邮箱
    print("\n📨 发送报告...")
    for email in TO_EMAILS:
        send_report(report, email)
    
    print("\n✅ 完成！")

if __name__ == "__main__":
    main()
