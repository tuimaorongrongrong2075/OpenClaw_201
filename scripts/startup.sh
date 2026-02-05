#!/bin/bash
# ========================================
# OpenClaw 自动启动脚本
# 在系统启动时自动加载环境变量并初始化服务
# ========================================

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 启动 OpenClaw 自动配置...${NC}"

# 加载环境变量
ENV_FILE="/root/.openclaw/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}✅ 加载环境变量...${NC}"
    set -a  # 自动导出
    source "$ENV_FILE"
    set +a
else
    echo -e "${YELLOW}⚠️  未找到环境变量文件: $ENV_FILE${NC}"
fi

# 1. 初始化 Gmail
if [ -n "$GMAIL_EMAIL" ] && [ -n "$GMAIL_APP_PASSWORD" ]; then
    echo -e "${GREEN}📧 检查 Gmail 连接...${NC}"
    python3 /root/.openclaw/workspace/scripts/gmail_manager.py check > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Gmail 已就绪${NC}"
    else
        echo -e "${YELLOW}⚠️  Gmail 连接失败${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未配置 Gmail 环境变量${NC}"
fi

# 2. 检查 GitHub CLI 登录状态
echo -e "${GREEN}🐙 检查 GitHub 连接...${NC}"
if gh auth status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ GitHub CLI 已登录${NC}"
else
    echo -e "${YELLOW}⚠️  GitHub CLI 未登录，需要手动运行 gh auth login${NC}"
fi

# 3. 检查 Moltbook
if [ -n "$MOLTBOOK_API_KEY" ]; then
    echo -e "${GREEN}🦞 检查 Moltbook 连接...${NC}"
    RESPONSE=$(curl -s "https://www.moltbook.com/api/v1/agents/status" \
        -H "Authorization: Bearer $MOLTBOOK_API_KEY")
    if echo "$RESPONSE" | grep -q '"success":true'; then
        echo -e "${GREEN}✅ Moltbook 已就绪${NC}"
    else
        echo -e "${YELLOW}⚠️  Moltbook 连接失败${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未配置 Moltbook API Key${NC}"
fi

echo -e "${GREEN}✨ OpenClaw 自动配置完成！${NC}"
