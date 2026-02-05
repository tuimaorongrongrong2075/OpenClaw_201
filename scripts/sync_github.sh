#!/bin/bash
# 小猩的 Workspace 自动同步脚本
# 每次文件更新后运行此脚本，同步到 GitHub

set -e

REPO_DIR="/root/.openclaw/workspace"
GITHUB_REPO="tuimaorongrongrong2075/OpenClaw_201"
COMMIT_MSG="[$(date '+%Y-%m-%d %H:%M')] 小猩自动同步 🦧"

echo "🦧 开始同步到 GitHub..."

cd "$REPO_DIR"

# 初始化 git（如果需要）
if [ ! -d .git ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit - 小猩的 workspace 🦧"
    git remote add origin "https://github.com/$GITHUB_REPO.git"
    echo "✅ Git 初始化完成"
else
    echo "📂 Git 仓库已存在"
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

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
git push origin main:main 2>/dev/null || git push origin master:master 2>/dev/null || git push origin HEAD:$(git rev-parse --abbrev-ref HEAD)

echo "✅ 同步完成！"
