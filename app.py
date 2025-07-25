# 📁 File: app.py

from flask import Flask, render_template, request
import os
from gtts import gTTS
import uuid

app = Flask(__name__)
app.config['SIGN_FOLDER'] = os.path.join('static', 'sign_images')
app.config['AUDIO_FOLDER'] = os.path.join('static', 'audio')

# Create audio folder if not exists
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# Function to map text to sign image paths
def get_sign_images(text):
    images = []
    for char in text.lower():
        if char.isalpha():
            img_path = os.path.join(app.config['SIGN_FOLDER'], f"{char}.jpg")
            if os.path.exists(img_path):
                images.append(img_path)
    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-text', methods=['POST'])
def process_text():
    input_text = request.form['input_text']

    # Get gesture/sign images for text
    output_images = get_sign_images(input_text)

    # Generate TTS audio file
    filename = f"{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
    tts = gTTS(input_text)
    tts.save(audio_path)

    return render_template(
        'index.html',
        input_text=input_text,
        output_images=output_images,
        tts_audio=audio_path
    )

if __name__ == '__main__':
    app.run(debug=True)
