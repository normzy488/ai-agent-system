from email_reader import get_recent_emails
from anthropic import Anthropic
import config

client = Anthropic(api_key=config.ANTHROPIC_API_KEY)


def get_email_summary():
    try:
        emails = get_recent_emails()

        prompt = f"""
        You are a high-level executive assistant.

        Here are recent emails:
        {emails}

        - Summarize key messages
        - Highlight urgent items
        - Extract action points
        """

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except Exception as e:
        return f"Email error: {str(e)}"
