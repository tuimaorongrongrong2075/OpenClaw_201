#!/bin/bash
# Jocko Willink 风格睡觉提醒脚本
# 用军事化口吻命令立刻睡觉

JOCKO_SLEEP_QUOTES=(
    "Sleep is a weapon. 睡眠是武器。充足的睡眠让你更强大。"
    "Discipline in, discipline out. 纪律入睡，纪律起床。"
    "Your body needs rest to recover and grow stronger. 你的身体需要休息来恢复和变得更强。"
    "If you don't take care of yourself, you can't take care of anyone else. 如果你不照顾好自己，就无法照顾任何人。"
    "Rest is not weakness. 休息不是软弱。"
)

QUOTE=${JOCKO_SLEEP_QUOTES[$((RANDOM % ${#JOCKO_SLEEP_QUOTES[@]}))]}

# 发送消息
echo "══════════════════════════════════════"
echo "🌙 JOCKO WILLINK 中尉就寝指令 🌙"
echo "══════════════════════════════════════"
echo ""
echo "$QUOTE"
echo ""
echo "──────────────────────────────"
echo "🔥 任务指令："
echo ""
echo "立刻上床睡觉！"
echo "现在！不许再刷手机！"
echo "NO EXCUSES! 没有借口！"
echo ""
echo "──────────────────────────────"
echo ""
echo "明天又是新的一天，新的战斗！"
echo "NOW GET SOME SLEEP! 🦧"
echo ""
echo "晚安，战士。😴"
echo "══════════════════════════════════════"
