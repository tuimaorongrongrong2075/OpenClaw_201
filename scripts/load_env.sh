#!/bin/bash
# 环境变量加载脚本
# 每次 OpenClaw 重启后运行此脚本以加载敏感信息

echo "🔐 加载环境变量..."

# 从 ~/.bashrc 加载环境变量（实际值存储在 ~/.bashrc 中）
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# 验证环境变量
if [ -z "$GMAIL_USER" ]; then
    echo "⚠️  GMAIL_USER 未设置"
    exit 1
fi

if [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "⚠️  GMAIL_APP_PASSWORD 未设置"
    exit 1
fi

echo "✅ 环境变量加载完成！"
