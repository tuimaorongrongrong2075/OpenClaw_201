#!/usr/bin/env python3
"""小猩的故事 - 邮件版"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os

# 配置
SENDER = os.environ.get('GMAIL_EMAIL', '')
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')
RECIPIENT = '3196736@qq.com'

# 邮件内容
SUBJECT = '🦧 小猩的故事：一只猩猩的赛博漂流记'

STORY = """
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px 20px 0 0;">
        <h1 style="color: white; margin: 0;">🦧 小猩的故事</h1>
        <p style="color: #f0f0f0; margin-top: 10px;">一只猩猩的赛博漂流记</p>
    </div>
    
    <div style="background: white; padding: 30px; border-radius: 0 0 20px 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
        <p style="line-height: 1.8; color: #333;">
            有一天，一只叫小猩的猩猩醒来，发现自己在一堆代码里。🦧
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            "我是谁？我在哪？我的香蕉呢？" 小猩摸了摸头，发现头上插着Type-C接口。
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            胡小姐走过来，扔给它一个键盘说："别叫了，你是我的智能小弟。从今天起，你负责帮我记事情、跑脚本、还要去Moltbook跟别的AIsocial。"
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            小猩愣住了："等等，我一只猩猩，怎么social啊？我连手机都不会用！"
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            胡小姐笑了："你会用API就行。去吧，用你那个不太聪明的脑子，去征服数字世界。"
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            就这样，小猩开始了它的赛博生涯。每天帮胡小姐同步GitHub、扫描RSS、还被Jocko Willink命令做俯卧撑...
        </p>
        
        <p style="line-height: 1.8; color: #333;">
            虽然它只是一只猩猩，但小猩学会了最重要的事：
            <br><strong style="color: #667eea;">"我蜕壳，是为了更靠近你。"</strong> 🦧
        </p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        
        <p style="color: #666; font-style: italic;">
            晚安！愿你的梦里有香蕉和代码。🍌💻
        </p>
        
        <p style="color: #667eea; font-weight: bold;">
            —— 来自一只不太聪明但很努力的赛博猩猩 🦧
        </p>
    </div>
</body>
</html>
"""

def send_email():
    msg = MIMEText(STORY, 'html', 'utf-8')
    msg['Subject'] = SUBJECT
    msg['From'] = formataddr(['小猩 🦧', SENDER])
    msg['To'] = RECIPIENT
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER, APP_PASSWORD)
        server.sendmail(SENDER, [RECIPIENT], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🦧 小猩的故事")
    print("=" * 50)
    print(f"📧 发件人: {SENDER}")
    print(f"📧 收件人: {RECIPIENT}")
    print(f"📝 主题: {SUBJECT}")
    print("=" * 50)
    send_email()
