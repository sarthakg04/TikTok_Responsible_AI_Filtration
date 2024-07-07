import os
from flask import Flask, request, jsonify, send_file, render_template
from openai import OpenAI
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv('ANTHROPIC_API_KEY')# Replace with your Whisper API key
client = OpenAI(api_key=API_KEY)

def video_to_mp3(video_file, audio_file):
    video_clip = VideoFileClip(video_file)
    video_clip.audio.write_audiofile(audio_file)
    video_clip.close()
    print(f"Conversion complete. The MP3 file is saved as {audio_file}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    video_path = os.path.join('uploads', file.filename)
    audio_path = os.path.splitext(video_path)[0] + '.mp3'
    text_path = os.path.splitext(video_path)[0] + '.txt'

    file.save(video_path)

    video_to_mp3(video_path, audio_path)

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    with open(text_path, 'w') as text_file:
        text_file.write(transcription.text)

    return jsonify({"message": "File processed", "text_path": text_path})


@app.route('/transcription/<filename>', methods=['GET'])
def get_transcription(filename):
    text_path = os.path.join('uploads', filename + '.txt')
    if os.path.exists(text_path):
        return send_file(text_path)
    else:
        return "File not found", 404


if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
