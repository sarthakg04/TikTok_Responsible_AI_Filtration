import os
from dotenv import load_dotenv
import anthropic
import json
# Load environment variables from .env file

def extract_json_from_text(text):
    # Function to find and extract JSON-like structures from text
    start_index = text.find('{')
    end_index = text.rfind('}') + 1

    if start_index != -1 and end_index != -1:
        json_str = text[start_index:end_index]
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON-like structure found in the text.")
        return None


def read_text(text_file):
    f = open(text_file,'r')
    return f.read()

def generate_json(obj):

    prompt = read_text('data/prompt.txt')
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": obj
                    }
                ]
            }
        ]
    ).content[0].text
    json_data = extract_json_from_text(message)
    return json_data
