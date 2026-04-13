from utils.database import save_log, get_logs, add_task, get_tasks
from agents.crypto_agent import get_crypto_data
from agents.email_agent import get_email_summary
from anthropic import Anthropic
import config

client = Anthropic(api_key=config.ANTHROPIC_API_KEY)


def route_message(user_message: str):
    original_message = user_message.strip()
    user_message = user_message.lower().strip()

    try:
        # 🔹 Add Task
        if user_message.startswith("/add_task"):
            task = original_message.replace("/add_task", "").strip()
            add_task(task)
            return f"✅ Task added: {task}"

        # 🔹 View Tasks
        elif user_message.startswith("/view_tasks"):
            tasks = get_tasks()

            if not tasks:
                return "No tasks available."

            formatted = "\n".join(
                [f"{tid}. {t} ({s})" for tid, t, s in tasks]
            )

            return f"📋 Tasks:\n\n{formatted}"

        # 🔹 Crypto
        elif user_message.startswith("/crypto"):
            data = get_crypto_data()

            prompt = f"""
            You are a crypto analyst.

            Here is the latest crypto data:
            {data}

            Give sharp insights, trends, and risks.
            """

            response = call_claude(prompt)
            save_log("crypto", response)
            return response

        # 🔹 History
        elif user_message.startswith("/history"):
            logs = get_logs()

            if not logs:
                return "No history found."

            formatted = "\n\n".join(
                [f"{t} → {c[:100]}..." for t, c, _ in logs]
            )

            return f"🧠 Memory:\n\n{formatted}"

        # 🔹 Default (memory aware)
        else:
            response = call_claude(original_message)
            save_log("chat", response)
            return response

    except Exception as e:
        return f"Error: {str(e)}"


def call_claude(user_input):
    logs = get_logs(3)

    memory_context = "\n".join(
        [f"{t}: {c}" for t, c, _ in logs]
    )

    full_prompt = f"""
    You are an AI operator.

    Memory:
    {memory_context}

    Task:
    {user_input}

    Give clear, actionable response.
    """

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.content[0].text
