import schedule
import time
import threading
from agents.email_agent import get_email_summary
from agents.crypto_agent import get_crypto_data
from agents.task_router import call_claude
import requests
import config


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text
    }

    requests.post(url, data=payload)


def auto_email_report():
    print("Running email report...")

    try:
        summary = get_email_summary()
        send_telegram_message(f"📬 EMAIL REPORT\n\n{summary}")
    except Exception as e:
        print("Email error:", e)


def auto_crypto_report():
    print("Running crypto report...")

    try:
        data = get_crypto_data()

        prompt = f"""
        You are a crypto analyst.

        Here is the latest crypto data:
        {data}

        Give key insights, risks, and opportunities.
        """

        analysis = call_claude(prompt)
        send_telegram_message(f"📊 CRYPTO REPORT\n\n{analysis}")

    except Exception as e:
        print("Crypto error:", e)


def run_scheduler():
    schedule.every(12).hours.do(auto_email_report)
    schedule.every(4).hours.do(auto_crypto_report)

    print("Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler():
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
