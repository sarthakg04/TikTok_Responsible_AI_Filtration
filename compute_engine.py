import os
from dotenv import load_dotenv
import anthropic
import json
# Load environment variables from .env file

def extract_content_from_video(url):
    return

def read_json_configuration(f_config):
    with open(f_config) as json_data:
        d = json.load(json_data)
        print(d)

def read_text(prompt):
    f = open(prompt,'r')
    return f.read()


def main():

    # url = 
    # obj = extract_content_from_video(url)
    obj = ''' On the outskirts of Yogyakarta, an Indonesian city that’s home to many universities, is a small boarding school with a mission that seems out of place in a nation with more Muslim citizens than any other. Its students are transgender women.

    It is a rare oasis of LGBTQ acceptance – not only in Indonesia, but across the far-flung Muslim world. Many Muslim nations criminalize gay sex — including World Cup host Qatar. LGBTQ people routinely are rejected by their families, denounced by Islamic authorities, hounded by security forces, and limited to clandestine social lives. Appeals for change from LGBTQ-friendly nations are routinely dismissed as unwarranted outside interference.

    Yogyakarta’s Al-Fatah Islamic school was founded 14 years ago by Shinta Ratri, a trans woman who struggled with self-doubts in her youth, wondering if her gender transition was sinful.

    '''
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
    print(message)

main()
