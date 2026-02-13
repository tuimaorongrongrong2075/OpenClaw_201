#!/bin/bash
# 禁用所有定时任务

echo "🔧 禁用所有定时任务..."

# 禁用Gmail每小时检查
echo "📬 禁用Gmail检查..."
openclaw cron update dbcb33fd-ccbb-4acf-a129-a16627fb974d '{"enabled":false}' 2>/dev/null || echo "Gmail检查任务已禁用"

# 禁用每日Memory更新（10:00）
echo "📝 禁用每日Memory更新（10:00）..."
openclaw cron update 54d28c37-6d25-40b8-8c8d-3dc2ad3349e8 '{"enabled":false}' 2>/dev/null || echo "Memory更新任务已禁用"

# 禁用每日Memory更新（18:00）
echo "📝 禁用每日Memory更新（18:00）..."
openclaw cron update 861b8d0b-cec7-42a1-b8d6-bbc898c3b08c '{"enabled":false}' 2>/dev/null || echo "Memory更新任务已禁用"

# 禁用Jocko撸铁提醒（15:13）
echo "💪 禁用Jocko撸铁提醒（15:13）..."
openclaw cron update 05bc46e9-cdd9-47e0-983a-3724fc60f772 '{"enabled":false}' 2>/dev/null || echo "Jocko提醒任务已禁用"

# 禁用Jocko撸铁提醒（17:47）
echo "💪 禁用Jocko撸铁提醒（17:47）..."
openclaw cron update f844c6fb-8063-426c-a788-7df436093b2d '{"enabled":false}' 2>/dev/null || echo "Jocko提醒任务已禁用"

echo ""
echo "✅ 所有定时任务已禁用！"
echo ""
echo "📋 当前任务状态："
openclaw cron list
