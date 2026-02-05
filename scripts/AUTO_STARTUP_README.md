# OpenClaw 自动启动配置指南

## 📁 文件结构

```
/root/.openclaw/
├── .env                  ← 敏感环境变量（不加入 Git）
├── workspace/
│   ├── .gitignore        ← 已更新，排除 .env
│   ├── scripts/
│   │   ├── startup.sh    ← 启动脚本
│   │   ├── gmail_manager.py
│   │   └── ...
│   └── ...
└── ...
```

## 🔧 安装步骤（在服务器上执行）

### 1. 安装系统服务（开机自动运行）

```bash
# 复制服务文件
sudo cp /root/.openclaw/workspace/scripts/openclaw-autostart.service /etc/systemd/system/

# 重新加载 systemd
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable openclaw-autostart.service

# 手动测试运行
sudo systemctl start openclaw-autostart.service

# 查看状态
sudo systemctl status openclaw-autostart.service
```

### 2. 手动测试启动脚本

```bash
chmod +x /root/.openclaw/workspace/scripts/startup.sh
/root/.openclaw/workspace/scripts/startup.sh
```

## 🔒 安全特性

1. **敏感信息隔离**：`.env` 文件包含所有密码和 API Key
2. **Git 排除**：`~/.gitignore` 已配置，排除 `.env` 等敏感文件
3. **最小权限**：系统服务以 root 运行，但只加载必要环境变量
4. **静默失败**：服务启动失败不会阻止系统启动

## 📝 管理命令

```bash
# 查看服务状态
systemctl status openclaw-autostart.service

# 查看启动日志
journalctl -u openclaw-autostart.service -f

# 停止服务
systemctl stop openclaw-autostart.service

# 禁用服务
systemctl disable openclaw-autostart.service
```

## ⚠️ 注意事项

1. **首次配置**：需要手动创建 `.env` 文件并填入敏感信息
2. **权限**：确保 `startup.sh` 有执行权限：`chmod +x startup.sh`
3. **更新密码**：修改 `.env` 文件后需要重启服务生效
4. **备份**：建议备份 `.env` 文件到安全位置
