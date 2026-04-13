import schedule
import time
import threading
from agents.task_router import call_claude
from utils.database import get_tasks, save_log
import requests
import config


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text
    }

    requests.post(url, data=payload)


# 🔥 EXECUTE TASKS
def run_task_executor():
    print("Running task executor...")

    tasks = get_tasks()

    for task_id, task, status in tasks:
        if status == "pending":

            prompt = f"""
            You are an AI operations assistant.

            Task:
            {task}

            Execute this task intelligently and give a result or recommendation.
            """

            result = call_claude(prompt)

            send_telegram_message(f"✅ TASK EXECUTED:\n\n{task}\n\n{result}")

            save_log("task", f"{task} → {result}")


# 🔹 Existing Reports
def auto_crypto_report():
    print("Running crypto report...")

    try:
        prompt = "Give latest important crypto insights and risks."
        analysis = call_claude(prompt)

        send_telegram_message(f"📊 CRYPTO REPORT\n\n{analysis}")

    except Exception as e:
        print("Crypto error:", e)


def run_scheduler():
    schedule.every(2).minutes.do(run_task_executor)
    schedule.every(4).hours.do(auto_crypto_report)

    print("Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler():
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
