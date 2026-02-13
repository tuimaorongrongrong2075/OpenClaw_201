#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送邮件脚本
"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email():
    # 邮件配置
    import os
    sender_email = os.environ.get("GMAIL_USER", "tuimaorongrong@gmail.com")
    sender_password = os.environ.get("GMAIL_APP_PASSWORD", "")
    sender_name = "小猩"
    recipient_email = "7391117@qq.com"
    recipient_name = ""
    
    # 邮件内容
    subject = "分享几个链接"
    
    html_body = """
<html>
<body>
<p>Hi，</p>
<p>以下是三个链接：</p>
<p>1. 腾讯云开发者文章<br>
   <a href="https://cloud.tencent.com/developer/article/2626151">https://cloud.tencent.com/developer/article/2626151</a></p>
<p>2. 腾讯云轻量应用服务器控制台<br>
   <a href="https://console.cloud.tencent.com/lighthouse/instance/index?rid=15">https://console.cloud.tencent.com/lighthouse/instance/index?rid=15</a></p>
<p>3. OpenClaw 文档<br>
   <a href="https://docs.openclaw.ai/zh-CN">https://docs.openclaw.ai/zh-CN</a></p>
<hr>
<p><small>来自小猩 🦧</small></p>
</body>
</html>
"""
    
    # 创建邮件
    msg = MIMEText(html_body, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = formataddr([sender_name, sender_email])
    msg['To'] = formataddr([recipient_name, recipient_email])
    
    try:
        # 连接Gmail SMTP服务器
        print("📧 正在连接 Gmail SMTP 服务器...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print("🔐 正在登录...")
        server.login(sender_email, sender_password)
        print("📨 正在发送邮件...")
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    send_email()
