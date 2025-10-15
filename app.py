from flask import Flask, request, jsonify, render_template
from video_summarizer import videoSummarizer
from flask_cors import CORS
import tempfile
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])  
def summarize_video():
    if 'video' not in request.files:
        return jsonify({'error': 'Video not found'}), 400  
    
    file = request.files['video'] 
    if file.filename == '':
        return jsonify({'error': 'File is empty'}), 400
    
    temp_path = None
    try:
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path) 
        result = videoSummarizer(temp_path)
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        if not result or 'summary' not in result:
            return jsonify({'error': 'File was corrupted or could not be processed'}), 500
        
        return jsonify({
            'summary': result['summary'],
            'transcript': result.get('transcript', 'Transcript not available')
        })
    
    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)