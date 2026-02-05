#!/usr/bin/env python3
"""查看今天收到的邮件数量"""
import imaplib
import os
from datetime import datetime, timedelta

def get_today_emails():
    """获取今天收到的邮件"""
    email_addr = os.environ.get('GMAIL_EMAIL', 'tuimaorongrong@gmail.com')
    app_password = os.environ.get('GMAIL_APP_PASSWORD', 'compnxsxaqxszcyc')
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select('INBOX')
        
        # 今天日期
        today = datetime.now().strftime("%d-%b-%Y")
        
        # 搜索今天收到的邮件
        status, messages = mail.search(None, f'SINCE {today}')
        
        if status == 'OK':
            count = len(messages[0].split())
            print(f"📬 今天（{datetime.now().strftime('%Y-%m-%d')}）收到的邮件数量：{count} 封")
            
            # 如果有邮件，显示最新几封的主题
            if count > 0:
                latest_emails = messages[0].split()[-5:]  # 最新5封
                print("\n📧 最新邮件：")
                for i, msg_id in enumerate(reversed(latest_emails), 1):
                    status, msg_data = mail.fetch(msg_id, '(RFC822.HEADER)')
                    if status == 'OK':
                        raw_email = msg_data[0][1]
                        # 提取Subject
                        for line in raw_email.decode().split('\r\n'):
                            if line.startswith('Subject:'):
                                subject = line[8:].strip()
                                print(f"  {i}. {subject[:50]}...")
                                break
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ 获取邮件失败: {e}")

if __name__ == '__main__':
    get_today_emails()
