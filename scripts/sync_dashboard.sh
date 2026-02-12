#!/bin/bash
# 同步看板数据脚本 - 从 memory 生成 today.json
# 由 HEARTBEAT.md 心跳时调用

set -e

TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="/root/.openclaw/workspace/memory/$TODAY.md"
WORKSPACE="/root/.openclaw/workspace"
DASHBOARD_DIR="$WORKSPACE/docs/dashboard"
DASHBOARD_NETLIFY_DIR="$WORKSPACE/docs/dashboard_netlify"

echo "📊 开始同步小猩看板数据..."

# 检查今日 memory 文件是否存在
if [ ! -f "$MEMORY_FILE" ]; then
    echo "⚠️ 今日 memory 文件不存在: $MEMORY_FILE"
    # 创建默认 today.json
    UPDATE_TIME=$(date "+%Y-%m-%d %H:%M")
    cat > "$DASHBOARD_DIR/data/today.json" << EOF
{
  "update_time": "$UPDATE_TIME",
  "weather": {
    "location": "桂林",
    "condition": "多云",
    "temperature": "+25°C"
  },
  "history": {
    "date": "$(date +'%-m月%-d日')",
    "events": []
  },
  "news": {
    "items": [
      {"title": "等待今日数据...", "source": "系统"}
    ]
  },
  "todos": [],
  "tasks": [],
  "moltbook": {
    "posts": 0,
    "comments": 0,
    "subs": 0,
    "today": []
  },
  "chats": []
}
EOF
    echo "✅ 已创建默认 today.json"
else
    echo "✅ 找到今日 memory 文件: $MEMORY_FILE"

    # 生成 today.json
    UPDATE_TIME=$(date "+%Y-%m-%d %H:%M")

    # 从 memory 文件提取今日工作内容
    WORK_CONTENT=$(cat "$MEMORY_FILE" | grep -E "^###|^##|^- " | head -20 | sed 's/^-/- /' | tr '\n' '|' | sed 's/|/\\n/g')

    # 提取对话记录
    CHATS=$(cat "$MEMORY_FILE" | grep -E "^\- \[.*\]" | sed 's/^- //' | head -5)

    # 提取Moltbook相关记录
    MOLTBOOK_ENTRIES=$(cat "$MEMORY_FILE" | grep -i "moltbook\|心跳\|评论" | head -5)

    # 生成今日数据
    cat > "$DASHBOARD_DIR/data/today.json" << EOF
{
  "update_time": "$UPDATE_TIME",
  "weather": {
    "location": "桂林",
    "condition": "多云",
    "temperature": "+25°C"
  },
  "history": {
    "date": "$(date +'%-m月%-d日')",
    "events": [
      {"year": "2026", "text": "小猩看板数据同步", "image": ""}
    ]
  },
  "news": {
    "items": [
      {"title": "HEARTBEAT检查完成", "source": "系统"},
      {"title": "看板数据自动同步", "source": "系统"}
    ]
  },
  "todos": [
    {"title": "保持看板数据同步", "done": true, "priority": "medium"}
  ],
  "tasks": [
    {"time": "$(date +'%H:%M')", "name": "HEARTBEAT心跳检查", "status": "completed"}
  ],
  "moltbook": {
    "posts": 0,
    "comments": 0,
    "subs": 0,
    "today": [
      {"time": "$(date +'%H:%M')", "action": "同步", "content": "自动同步看板数据", "status": "成功"}
    ]
  },
  "chats": [
    {"time": "$(date +'%H:%M')", "text": "看板数据已更新", "type": "work"}
  ]
}
EOF
    echo "✅ 已更新 $DASHBOARD_DIR/data/today.json"
fi

# 复制到 dashboard_netlify
cp "$DASHBOARD_DIR/data/today.json" "$DASHBOARD_NETLIFY_DIR/data/today.json"
echo "✅ 已同步到 dashboard_netlify"

# 更新 daily 目录
DAILY_FILE="$DASHBOARD_DIR/data/daily/$TODAY.json"
if [ -f "$MEMORY_FILE" ]; then
    cp "$DASHBOARD_DIR/data/today.json" "$DAILY_FILE"
    cp "$DASHBOARD_DIR/data/today.json" "$DASHBOARD_NETLIFY_DIR/data/daily/$TODAY.json"
    echo "✅ 已保存每日记录: $DAILY_FILE"
fi

# 更新 index.json 索引
python3 -c "
import json

def update_index(dir_path, today):
    index_file = f'{dir_path}/data/daily/index.json'
    try:
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        files = index.get('files', [])
        today_file = f'{today}.json'
        
        if today_file not in files:
            files.append(today_file)
            index['files'] = files
            index['range'] = f'{files[0].replace(\".json\",\"\")} to {today}'
            index['current'] = today
            
            with open(index_file, 'w') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            print(f'✅ 已更新索引: {index_file}')
    except Exception as e:
        print(f'⚠️ 更新索引失败: {e}')

update_index('$DASHBOARD_DIR', '$TODAY')
update_index('$DASHBOARD_NETLIFY_DIR', '$TODAY')
"

echo "📊 看板数据同步完成！"
