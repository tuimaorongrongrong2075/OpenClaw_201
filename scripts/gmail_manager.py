#!/usr/bin/env python3
"""
Gmail 管理工具
"""
import imaplib
import email
import os

def get_credentials():
    """获取邮箱凭据"""
    email_addr = os.environ.get('GMAIL_EMAIL', 'tuimaorongrong@gmail.com')
    app_password = os.environ.get('GMAIL_APP_PASSWORD', '')
    return email_addr, app_password

def connect_gmail():
    """连接 Gmail"""
    email_addr, app_password = get_credentials()
    if not app_password:
        print("❌ 未找到应用密码，请设置 GMAIL_APP_PASSWORD 环境变量")
        return None
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        print("✅ Gmail 连接成功！")
        return mail
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return None

def list_folders():
    """列出所有邮件文件夹"""
    mail = connect_gmail()
    if mail:
        status, folders = mail.list()
        if status == 'OK':
            print("\n📁 邮件文件夹:")
            for folder in folders:
                print(f"  {folder.decode()}")
        mail.logout()

def check_inbox():
    """检查收件箱"""
    mail = connect_gmail()
    if mail:
        mail.select('INBOX')
        status, messages = mail.search(None, 'ALL')
        if status == 'OK':
            count = len(messages[0].split())
            print(f"📬 收件箱共有 {count} 封邮件")
        mail.logout()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'folders':
            list_folders()
        elif command == 'check':
            check_inbox()
        else:
            print("用法: python3 gmail_manager.py [folders|check]")
    else:
        check_inbox()
