#!/bin/bash
# 小猩的 Workspace 自动同步脚本
# 每次文件更新后运行此脚本，同步到 GitHub

set -e

REPO_DIR="/root/.openclaw/workspace"
GITHUB_REPO="tuimaorongrongrong2075/OpenClaw_201"
BRANCH="main"
COMMIT_MSG="[$(date '+%Y-%m-%d %H:%M')] 小猩自动同步 🦧"

echo "🦧 开始同步到 GitHub..."

cd "$REPO_DIR"

# 初始化 git（如果需要）
if [ ! -d .git ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git config user.email "xiaoxing@example.com"
    git config user.name "小猩"
    git add -A
    git commit -m "Initial commit - 小猩的 workspace 🦧"
    echo "✅ Git 初始化完成"
fi

# 添加所有更改
git add -A

# 检查是否有更改
if git diff --cached --quiet; then
    echo "✅ 没有新更改，跳过提交"
    exit 0
fi

# 提交
git commit -m "$COMMIT_MSG"

# 使用 gh 推送（自动处理认证）
echo "🚀 推送到 GitHub..."
gh repo set-default "$GITHUB_REPO" 2>/dev/null || true
# 强制推送到 GitHub（覆盖远程，确保同步）
git push https://x-access-token:$(gh auth token)@github.com/$GITHUB_REPO.git HEAD:$BRANCH --force 2>/dev/null || \
git push https://x-access-token:$(gh auth token)@github.com/$GITHUB_REPO.git HEAD:$BRANCH --force

echo "✅ 同步完成！"
