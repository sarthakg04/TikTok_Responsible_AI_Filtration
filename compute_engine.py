import os
from dotenv import load_dotenv
import anthropic
import json
# Load environment variables from .env file

def remove_first_and_last_line_from_text(text):
    lines = text.splitlines()
    if len(lines) > 2:
        lines = lines[1:-1]  # Remove the first and last line
    return '\n'.join(lines)
def parse_message_to_json(message):
    
    text = remove_first_and_last_line_from_text(message) 
    try:
        json_data = json.loads(text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def read_json_configuration(f_config):
    with open(f_config) as json_data:
        d = json.load(json_data)
        print(d)

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
    json_data = parse_message_to_json(message)
    return json_data
