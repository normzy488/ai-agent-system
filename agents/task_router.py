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

            return call_claude(prompt)

        # 🔹 Email
        elif user_message.startswith("/email"):
            return get_email_summary()

        # 🔹 Ask
        elif user_message.startswith("/ask"):
            user_query = user_message.replace("/ask", "").strip()
            prompt = f"Act as a high-level business advisor. Give sharp advice: {user_query}"
            return call_claude(prompt)

        # 🔹 Default
        else:
            prompt = f"Respond clearly: {user_message}"
            return call_claude(prompt)

    except Exception as e:
        return f"Error: {str(e)}"


def call_claude(prompt):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
