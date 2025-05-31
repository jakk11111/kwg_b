# KWGGAME Telegram 机器人

本仓库包含一个简单的 Telegram 机器人源码，功能如下：
- 当用户发送 `/start` 时，发送欢迎图片和欢迎消息。
- 当用户发送 `/menu` 时，弹出自定义键盘，包括 “🎁 Claim Bonus”、“🎮 Play Games” 和 “📞 Contact Support” 三个选项。
- 用户点击菜单任一选项后，机器人会回复对应的链接或联系方式。

该项目基于 Python + Flask，通过 webhook 与 Telegram 进行通信。

---

## 环境搭建与部署

### 1. 新建 Telegram Bot 并获取 Token
1. 打开 Telegram，搜索 “@BotFather”。  
2. 发送 `/newbot` 并按照提示设置机器人名称和用户名。  
3. BotFather 会返回一个 **API Token**，示例格式：  
   ```
   123456789:ABCDefGhIJKlmNO_PQrSTuvWXyZ
   ```
   请复制此 Token，后续作为环境变量使用。

### 2. 克隆或 Fork 本仓库
```bash
git clone https://github.com/<你的用户名>/kwggame-telegram-bot.git
cd kwggame-telegram-bot
```

### 3. 在 Replit（或其他主机）中设置环境变量
#### 3.1 在 Replit 中：
- 打开左侧菜单 → Secrets（Environment Variables）
- 添加以下两个环境变量（Key / Value）：

  ```
  KEY: TELEGRAM_API_TOKEN
  VALUE: 你的 BotFather 提供的 Token（示例：7676537698:AAGTWW-Kqxpzh7HgD4wLPoLhHfrUI1_2g2c）

  KEY: WEBHOOK_BASE_URL
  VALUE: https://<你的-repl-名称>.<你的-用户名>.replit.app
  ```
> **注意：**  
> - 请务必不要将以上 Token 等敏感信息直接上传到 GitHub。  
> - `WEBHOOK_BASE_URL` 必须是真实可访问的公网地址，末尾不要添加斜杠。  

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 启动并测试
1. 运行 Flask 应用：  
   ```bash
   python bot.py
   ```
2. 在浏览器中打开：  
   ```
   https://<你的-webhook-base-url>/
   ```  
   该操作会移除旧的 webhook 并注册新的 webhook。  
3. 打开 Telegram，给你的机器人发送 `/start`：  
   - 应该会收到一张欢迎图片和欢迎消息。  
   - 再发送 `/menu`，测试三个菜单按钮是否正常工作。  

---

## 功能原理简介

1. **Webhook 机制**  
   - 当你在浏览器中访问根路径（`/`）时，程序会执行：
     ```python
     bot.remove_webhook()
     bot.set_webhook(url = "<WEBHOOK_BASE_URL>/<API_TOKEN>")
     ```
     这样 Telegram 就将所有更新（消息、命令等）推送到 `https://<WEBHOOK_BASE_URL>/<API_TOKEN>` 这个地址。

2. **接收并处理更新**  
   - 当 Telegram 将用户消息推送到 `/\<API_TOKEN>` 路由时，Flask 会调用 `receive_update()`：  
     ```python
     json_string = request.stream.read().decode("utf-8")
     update = telebot.types.Update.de_json(json_string)
     bot.process_new_updates([update])
     ```
     然后由 `pyTelegramBotAPI` 内部将更新分发给相应的处理函数（如 `/start`、`/menu` 或文字消息处理函数）。

3. **命令与消息处理**  
   - `/start`：发送欢迎图片与文字说明。  
   - `/menu`：弹出自定义键盘，包含“🎁 Claim Bonus”“🎮 Play Games”“📞 Contact Support”三个按钮。  
   - 用户点击对应按钮后，会进入文字消息处理函数，根据文字内容匹配相应分支并回复链接或客服信息。  

---

## 自定义与扩展

- **修改图片或链接**  
  在 `bot.py` 中，可修改：
  ```python
  welcome_photo_url = "https://i.postimg.cc/nV0KwdBC/DALL-E-2024-05-04-20-46.jpg"
  ```
  以及各菜单按钮的链接：
  ```python
  "点击此处领取奖金： https://kwg04.com"
  "立即游戏： https://kwggame.com/play"
  "客服联系方式： @kwggameVIP_bot"
  ```

- **新增命令**  
  你可在 `bot.py` 里添加新命令，如：
  ```python
  @bot.message_handler(commands=['help'])
  def send_help(message):
      bot.send_message(message.chat.id, "这是帮助信息：...")
  ```

- **修改自定义键盘**  
  在 `show_menu()` 中：
  ```python
  markup.row('🎁 Claim Bonus', '🎮 Play Games')
  markup.row('📞 Contact Support')
  ```
  可根据需求增删按钮。

- **暂时移除 Webhook**  
  如果需要临时关闭 webhook，可执行：
  ```python
  bot.remove_webhook()
  ```

---

## 如何推送到 GitHub

1. 如果尚未初始化 Git 仓库：
   ```bash
   git init
   git add .
   git commit -m "初次提交：KWGGAME Telegram 机器人"
   ```
2. 在 GitHub 上新建仓库（例如 `kwggame-telegram-bot`），然后按照提示推送：
   ```bash
   git remote add origin https://github.com/<你的用户名>/kwggame-telegram-bot.git
   git branch -M main
   git push -u origin main
   ```

---

### 最终说明

- 所有文字说明均为中文，代码本身保持英文格式。  
- 部署前，请务必在 Replit 或其他主机上设置环境变量 `TELEGRAM_API_TOKEN` 和 `WEBHOOK_BASE_URL`。  
- 推送到 GitHub 后，你即可分享仓库地址、邀请他人协作。  
