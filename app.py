import os
import logging
from flask import Flask, render_template, request, jsonify
from sign_language_processor import process_sign_language
from chat_assistant import get_chat_response

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-sign', methods=['POST'])
def process_sign():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image data received'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        result = process_sign_language(image_file)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error processing sign language: {str(e)}")
        return jsonify({'error': 'Failed to process sign language'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        response = get_chat_response(data['message'])
        return jsonify({'response': response})
    
    except Exception as e:
        logger.error(f"Error in chat processing: {str(e)}")
        return jsonify({'error': 'Failed to get chat response'}), 500

if __name__ == '__main__':
    app.run(debug=True)