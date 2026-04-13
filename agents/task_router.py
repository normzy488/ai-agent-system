from utils.database import save_log, get_logs
from agents.crypto_agent import get_crypto_data
from agents.email_agent import get_email_summary
from anthropic import Anthropic
import config

client = Anthropic(api_key=config.ANTHROPIC_API_KEY)


def route_message(user_message: str):
    original_message = user_message.strip()
    user_message = user_message.lower().strip()

    try:
        # 🔹 Crypto
        if user_message.startswith("/crypto"):
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

            return f"🧠 Recent Memory:\n\n{formatted}"

        # 🔹 Email
        elif user_message.startswith("/email"):
            response = get_email_summary()
            save_log("email", response)
            return response

        # 🔹 Everything else (memory-aware)
        else:
            response = call_claude(original_message)
            save_log("chat", response)
            return response

    except Exception as e:
        return f"Error: {str(e)}"


def call_claude(user_input):
    logs = get_logs(3)

    if logs:
        last_type, last_content, _ = logs[0]

        memory_section = f"""
        LAST MEMORY ({last_type}):
        {last_content}
        """
    else:
        memory_section = "No past memory."

    full_prompt = f"""
    You are an intelligent AI agent with memory.

    RULES:
    - You DO have access to past memory below
    - If the user refers to "last", "previous", "earlier" → use LAST MEMORY
    - NEVER say you don’t have access to previous context

    ===== MEMORY =====
    {memory_section}
    ==================

    USER MESSAGE:
    {user_input}

    Respond clearly and use memory when relevant.
    """

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.content[0].text
