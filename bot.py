import os
import telebot
from flask import Flask, request

# ─────────────── 配置部分 ───────────────
#
# 1. 在 Replit（或其他主机）中创建环境变量 TELEGRAM_API_TOKEN，值为你的 Bot Token。
# 2. 将下面的 WEBHOOK_BASE_URL 替换为你应用的公网 URL（不要末尾带斜杠）。
#
#    例如，在 Replit 上可能是：
#      https://<你的-repl-名称>.<你的-用户名>.replit.app
#
# 3. 部署后，打开：https://<你的-webhook-base-url>/  即可自动移除旧的 webhook 并设置新的 webhook。
# 4. 安装依赖：pip install -r requirements.txt
#
# ────────────────────────────────────────────────────────

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
if not API_TOKEN:
    raise RuntimeError("错误：未检测到环境变量 TELEGRAM_API_TOKEN，请先设置。")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 将此变量替换为你真实的公网 URL（末尾不要带斜杠）
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL')
if not WEBHOOK_BASE_URL:
    raise RuntimeError("错误：未检测到环境变量 WEBHOOK_BASE_URL，请先设置。")

# ─────────── Bot 命令处理 ───────────

@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    当用户发送 /start 时，机器人将发送欢迎图片和消息。
    '''
    welcome_photo_url = 'https://i.postimg.cc/nV0KwdBC/DALL-E-2024-05-04-20-46.jpg'
    bot.send_photo(message.chat.id, photo=welcome_photo_url)
    bot.send_message(
        message.chat.id,
        "🎉 Welcome to KWGGAME 🎉\n\n"
        "💸 Claim your rewards now!\n"
        "🌐 Visit: https://www.kwggame.com\n"
        "👉 Tap /menu to see options"
    )

@bot.message_handler(commands=['menu'])
def show_menu(message):
    '''
    当用户发送 /menu 时，显示一个包含三种选项的自定义键盘。
    '''
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎁 Claim Bonus', '🎮 Play Games')
    markup.row('📞 Contact Support')
    bot.send_message(
        message.chat.id,
        "请选择一个选项：",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    '''
    处理其他所有文本消息，根据自定义键盘选项回复对应内容。
    '''
    text = message.text.strip()

    if text == '🎁 Claim Bonus':
        bot.send_message(
            message.chat.id,
            "点击此处领取奖金： https://kwg04.com"
        )
    elif text == '🎮 Play Games':
        bot.send_message(
            message.chat.id,
            "立即游戏： https://kwggame.com/play"
        )
    elif text == '📞 Contact Support':
        bot.send_message(
            message.chat.id,
            "客服联系方式： @kwggameVIP_bot"
        )
    else:
        bot.send_message(
            message.chat.id,
            "请从菜单中选择一个选项，谢谢！"
        )

# ─────────── Webhook 路由 ───────────

@app.route(f"/{API_TOKEN}", methods=['POST'])
def receive_update():
    '''
    该接口用于接收 Telegram 通过 webhook 推送的更新（POST 请求）。
    '''
    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def set_webhook():
    '''
    当访问根路径时，机器人会自动移除旧的 webhook 并设置新的 webhook。
    新的 webhook 地址形式为：<WEBHOOK_BASE_URL>/<API_TOKEN>
    '''
    bot.remove_webhook()
    new_hook = f"{WEBHOOK_BASE_URL}/{API_TOKEN}"
    bot.set_webhook(url=new_hook)
    return f"Webhook 已设置为： {new_hook}", 200

# ─────────── 程序入口 ───────────

if __name__ == "__main__":
    # 在 0.0.0.0:8080 上启动 Flask 应用，用于接收 Telegram 的 webhook 请求
    app.run(host="0.0.0.0", port=8080)
