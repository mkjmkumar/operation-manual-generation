from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from werkzeug.utils import secure_filename
import os
from translations import TRANSLATIONS
import ffmpeg
import sys
import pytesseract
from PIL import Image
import subprocess
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

# Configure upload folders
UPLOAD_FOLDER = 'uploads'
VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
RULES_FOLDER = os.path.join(UPLOAD_FOLDER, 'rules')
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create upload directories if they don't exist
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(RULES_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Mock user credentials (replace with database in production)
USERS = {
    'admin': 'password123'
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_language = request.form.get('selected_language', 'en')
        
        if username == 'admin' and password == 'password123':
            session['username'] = username
            session['language'] = selected_language  # Store language preference in session
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload_videos', methods=['POST'])
def upload_videos():
    if 'videos' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    files = request.files.getlist('videos')
    uploaded_files = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if file and file.filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_files.append(filename)
    
    if uploaded_files:
        return jsonify({
            'success': True, 
            'message': f'Successfully uploaded {len(uploaded_files)} files'
        })
    
    return jsonify({'success': False, 'message': 'No valid files uploaded'}), 400

@app.route('/upload_rules', methods=['POST'])
@login_required
def upload_rules():
    if 'rules' not in request.files:
        return 'No rules file uploaded', 400
    
    rules_file = request.files['rules']
    if rules_file.filename:
        filename = secure_filename(rules_file.filename)
        rules_file.save(os.path.join(RULES_FOLDER, filename))
    
    return 'Rules uploaded successfully'

@app.context_processor
def utility_processor():
    def translate(key):
        lang = session.get('language', 'en')
        return TRANSLATIONS[lang].get(key, key)
    return dict(t=translate)

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['en', 'ja']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

@app.before_request
def before_request():
    if 'language' not in session:
        session['language'] = 'en'

def add_highlight(input_image, output_image, x=100, y=100, radius=50, color='#FFEB3B@0.3', shape='circle'):
    try:
        # Create the filter complex string with light yellow color and 30% opacity
        filter_complex = (
            f"drawbox=x={x-radius}:y={y-radius}:"
            f"w={2*radius}:h={2*radius}:"
            f"color={color}:t=fill"
        )

        # Build the ffmpeg command
        stream = (
            ffmpeg
            .input(input_image)
            .filter('drawbox', 
                x=x-radius, 
                y=y-radius, 
                w=2*radius, 
                h=2*radius, 
                color='#FFEB3B@0.3',  # Light yellow with 30% opacity
                t='fill'
            )
            .output(output_image)
            .overwrite_output()
        )
        
        # Run the command
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        return True
        
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}", file=sys.stderr)
        return False

def process_image_with_text_highlight(input_image, output_image, target_word):
    try:
        # Generate timestamp for filename
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_filename = os.path.basename(input_image)
        new_filename = f"{current_time}_{input_filename}"
        output_path = os.path.join(os.path.dirname(output_image), new_filename)
        
        # Open image using PIL
        img = Image.open(input_image)
        
        # Perform OCR
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        
        # Log OCR results
        with open('ocr_output.txt', 'w', encoding='utf-8') as f:
            f.write("OCR Detection Results:\n")
            f.write("====================\n\n")
            for i, text in enumerate(data['text']):
                if text.strip():
                    confidence = data['conf'][i]
                    f.write(f"Text: {text}\n")
                    f.write(f"Confidence: {confidence}%\n")
                    f.write(f"Position: x={data['left'][i]}, y={data['top'][i]}\n")
                    f.write("--------------------\n")

        # Find matching words
        found_words = []
        for i, word in enumerate(data['text']):
            if word.lower() == target_word.lower():
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                found_words.append((x, y, w, h))

        if not found_words:
            return False, 0, "No matching words found", None

        try:
            # Create ffmpeg command with highlight box and outline
            command = ['ffmpeg', '-i', input_image]
            filter_parts = []
            
            for x, y, w, h in found_words:
                # Add padding
                padding = 5
                
                # Yellow highlight box (semi-transparent)
                filter_parts.append(
                    f"drawbox=x={x-padding}:y={y-padding}:w={w+2*padding}:h={h+2*padding}:color=yellow@0.3:t=fill"
                )
                
                # Red outline box (solid)
                filter_parts.append(
                    f"drawbox=x={x-padding}:y={y-padding}:w={w+2*padding}:h={h+2*padding}:color=red:t=2"
                )
            
            filter_string = ','.join(filter_parts)
            command.extend(['-vf', filter_string, '-y', output_path])
            
            # Execute command
            subprocess.run(command, check=True, capture_output=True)
            
            return True, len(found_words), f"Successfully highlighted {len(found_words)} instances", new_filename
            
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            return False, 0, f"FFmpeg processing failed: {e.stderr.decode()}", None
            
    except Exception as e:
        print(f"General error: {str(e)}")
        return False, 0, str(e), None

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.json
        target_word = data.get('word', '')
        
        if not target_word:
            return jsonify({
                'success': False,
                'message': 'Please provide a word to highlight'
            })

        files = os.listdir(UPLOAD_FOLDER)
        if not files:
            return jsonify({
                'success': False,
                'message': 'No images to process'
            })
            
        for filename in files:
            if filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                output_path = os.path.join(PROCESSED_FOLDER, filename)  # temporary path
                
                success, count, message, new_filename = process_image_with_text_highlight(
                    input_path, output_path, target_word
                )
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': f'Found {count} instances. {message}',
                        'filename': new_filename
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': message
                    })
        
        return jsonify({
            'success': False,
            'message': 'No valid images found to process'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Processing failed: {str(e)}'
        })

@app.route('/ocr_results')
def get_ocr_results():
    try:
        with open('ocr_output.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'No OCR results available'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58080, debug=True)