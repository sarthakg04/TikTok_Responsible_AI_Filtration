import os
from dotenv import load_dotenv
import anthropic
# Load environment variables from .env file
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    temperature=0,
    system="Define System Prompt Here, Like JSON on how to extract etc.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Text from Video"
                }
            ]
        }
    ]
)
print(message.content)
