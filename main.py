from utils.database import init_db, save_log
from utils.scheduler import start_scheduler
from agents.task_router import route_message
from agents.email_agent import get_email_summary
from agents.crypto_agent import get_crypto_data
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from anthropic import Anthropic
import config

# Initialize Claude
client = Anthropic(api_key=config.ANTHROPIC_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    print("Received message:", user_message)

    reply = route_message(user_message)

    await update.message.reply_text(reply)

# Start bot
app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot is running...")
init_db()
start_scheduler()
app.run_polling()
