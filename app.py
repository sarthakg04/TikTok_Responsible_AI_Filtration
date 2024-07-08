import os
from flask import Flask, request, jsonify, send_file, render_template
from openai import OpenAI
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
import compute_engine
import requests
from urllib.parse import urlparse
import shutil

load_dotenv()
app = Flask(__name__)
API_KEY_OPENAI=os.getenv('API_KEY')
client = OpenAI(api_key=API_KEY_OPENAI)
app.config['WTF_CSRF_ENABLED'] = False


def download_video(url, save_as):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_as, 'wb') as f:
            f.write(response.content)
        print(f"Video downloaded successfully as {save_as}")
    else:
        print(f"Failed to download video: {response.status_code} - {response.reason}")

def video_to_mp3(video_file, audio_file):
    video_clip = VideoFileClip(video_file)
    video_clip.audio.write_audiofile(audio_file)
    video_clip.close()
    print(f"Conversion complete. The MP3 file is saved as {audio_file}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file_new():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('token=')[-1]
        video_path = os.path.join('uploads', filename)
        with open(video_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        audio_path = os.path.splitext(video_path)[0] + '.mp3'
        text_path = os.path.splitext(video_path)[0] + '.txt'
        video_to_mp3(video_path, audio_path)
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        with open(text_path, 'w') as text_file:
            text_file.write(transcription.text)
        response=get_json(video_path)
        return response

    else:
        return jsonify({"error": "Failed to download file"}), 400

@app.route('/transcription/<filename>', methods=['GET'])
def get_transcription(filename):
    text_path = os.path.join('uploads', filename + '.txt')
    if os.path.exists(text_path):
        return send_file(text_path)
    else:
        return "File not found", 404


@app.route('/getjson/<filename>', methods=['GET'])
def get_json(filename):
    text_path = os.path.join('', filename + '.txt')
    with open(text_path, 'r') as file:
        text_content = file.read()
        response=compute_engine.generate_json(text_content)
    return response

    
if __name__ == '__main__':
    # os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)