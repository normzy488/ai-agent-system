from utils.database import save_log, get_logs
from agents.crypto_agent import get_crypto_data
from agents.email_agent import get_email_summary
from anthropic import Anthropic
import config

client = Anthropic(api_key=config.ANTHROPIC_API_KEY)


def route_message(user_message: str):
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

        # 🔹 Ask
        elif user_message.startswith("/ask"):
            user_query = user_message.replace("/ask", "").strip()

            prompt = f"""
            You are a high-level business advisor.

            User question:
            {user_query}

            Give sharp, practical advice.
            """

            response = call_claude(prompt)
            save_log("chat", response)
            return response

        # 🔹 Default
        else:
            prompt = f"Respond clearly: {user_message}"

            response = call_claude(prompt)
            save_log("chat", response)
            return response

    except Exception as e:
        return f"Error: {str(e)}"


def call_claude(prompt):
    logs = get_logs(5)

    memory_context = "\n".join(
        [f"{t}: {c}" for t, c, _ in logs]
    )

    full_prompt = f"""
    You are an intelligent AI agent with memory.

    Past context:
    {memory_context}

    Current task:
    {prompt}
    """

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.content[0].text
