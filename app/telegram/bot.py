import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

API_URL = "http://127.0.0.1:8000/message/"

async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    full_name = update.effective_user.full_name
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        payload = {
            "user_id": user_id,
            "name": full_name,
            "message": user_text
        }
        
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            reply_text = data["reply"]
            
            if data.get("needs_human_support"):
                reply_text += "\n\n⚠️ *پیام شما برای تیم پشتیبانی نیز ارسال شد.*"

            await update.message.reply_text(reply_text, parse_mode="Markdown")
        else:
            await update.message.reply_text("متأسفانه مشکلی در ارتباط با سرور پیش آمده است.")

    except Exception as e:
        logging.error(f"Error connecting to backend: {e}")
        await update.message.reply_text("در حال حاضر قادر به پاسخگویی نیستم. لطفاً کمی بعد تلاش کنید.")

if __name__ == '__main__':
  
    TOKEN = "TELEGRAM_BOT_TOKEN"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
  
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_telegram_message)
    application.add_handler(text_handler)
    
    print("Bot is running...")
    application.run_polling()
