# 🦕 Dino Email Bot

一个自动发送每日四语祝福邮件的小机器人，来自中国赣北地区。

## 功能

- 从 1000 条祝福语中随机抽取，每封邮件内容不同
- 每封邮件包含中、英、法、德四语祝福
- 学院派蓝色渐变风格，信封式 HTML 邮件模板
- 支持 GitHub Actions 每日定时自动发送

## 配置

### 1. 添加 API Key

在 GitHub 仓库 Settings → Secrets and variables → Actions 中添加：

```
MATON_API_KEY = 你的 Maton OAuth API Key
```

### 2. 修改收件人

编辑 `recipients.txt`，每行一个邮箱地址。

### 3. 定时发送

GitHub Actions 会在每天日本时间 7:30 自动触发（见 `.github/workflows/daily-email.yml`）。

如需修改时间，编辑 workflow 中的 `cron` 表达式（UTC 时间）：
- 日本时间 7:30 → `30 22 * * *`
- 北京时间 7:30 → `30 23 * * *`

## 手动发送

```bash
export MATON_API_KEY="你的key"
python dino_broadcast.py --send
```

## 文件说明

| 文件 | 说明 |
|---|---|
| `dino_broadcast.py` | 主脚本，生成 HTML 并发送邮件 |
| `recipients.txt` | 收件人列表，每行一个邮箱 |
| `gen_blessings.py` | 祝福语生成器（1000条四语祝福） |
| `.github/workflows/daily-email.yml` | GitHub Actions 定时任务 |
