import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


API_URL = "http://127.0.0.1:8000/message/"
BOT_TOKEN = "8944961039:AAFa25tK6k2f0DMZ8Ad-Gy2ZeuyXhBNTTS8"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text
    user = update.message.from_user

    payload = {
        "user_id": str(user.id),
        "name": user.first_name or "User",
        "message": user_message
    }

    try:

        response = requests.post(API_URL, json=payload)

        data = response.json()

        reply = data["reply"]

    except Exception:
        reply = "خطا در ارتباط با سرور."

    await update.message.reply_text(reply)


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Telegram bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
