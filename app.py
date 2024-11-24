from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from werkzeug.utils import secure_filename
import os
from translations import TRANSLATIONS
import ffmpeg
import sys
import pytesseract
from PIL import Image, ImageDraw
import subprocess
from datetime import datetime
from lib.text_highlighter import highlight_text_with_arrow
import logging
import cv2
import math  # Make sure to import math for arrow calculations

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

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
    app.logger.debug("Starting process_image route")
    try:
        data = request.get_json()
        word = data.get('word')
        timestamp = data.get('timestamp')
        
        # Get the most recently uploaded file from UPLOAD_FOLDER
        uploaded_files = [f for f in os.listdir(UPLOAD_FOLDER) 
                         if f.lower().endswith(tuple(ALLOWED_EXTENSIONS))]
        
        if not uploaded_files:
            return jsonify({"success": False, "message": "No uploaded image found"})
            
        # Get most recent file based on creation time
        latest_file = max(uploaded_files, 
                         key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x)))
        
        # Get original filename without extension
        filename_without_ext = os.path.splitext(latest_file)[0]
        
        input_path = os.path.join(UPLOAD_FOLDER, latest_file)
        output_filename = f"{filename_without_ext}_{timestamp}.jpg"
        output_path = os.path.join(PROCESSED_FOLDER, output_filename)
        
        app.logger.debug(f"Processing file: {input_path}")
        
        # Call the highlight function with correct paths
        result = highlight_text_with_arrow(
            image_path=input_path,
            search_text=word,
            output_path=output_path
        )
        
        if result is None:
            return jsonify({"success": False, "message": "Image processing failed"})
            
        return jsonify({
            "success": True, 
            "message": "Image processed successfully",
            "filename": output_filename
        })
        
    except Exception as e:
        app.logger.error(f"Error in process_image: {str(e)}")
        return jsonify({"success": False, "message": str(e)})

@app.route('/ocr_results')
def get_ocr_results():
    try:
        with open('ocr_output.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'No OCR results available'

def draw_arrow(image, x, y, size=20, color='red'):
    """Draw a small arrow pointing to the text"""
    draw = ImageDraw.Draw(image)
    
    # Arrow points
    arrow_x = x - size  # Position arrow to the left of text
    arrow_y = y
    
    # Draw arrow (triangle)
    draw.polygon([
        (arrow_x, arrow_y),  # Tip
        (arrow_x - size//2, arrow_y - size//2),  # Top left
        (arrow_x - size//2, arrow_y + size//2)   # Bottom left
    ], fill=color)
    
    return image

def process_ocr_output(image):
    # Create a copy of the image for drawing
    annotated_image = image.copy()
    
    custom_config = r'--oem 3 --psm 6'
    results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    # Group words by their y-coordinate (same line) with more tolerance
    lines = {}
    for i in range(len(results['text'])):
        if not results['text'][i].strip():
            continue
            
        text = results['text'][i]
        conf = int(results['conf'][i])
        x = results['left'][i]
        y = results['top'][i]
        width = results['width'][i]  # Get the width of the text
        
        # Use a tolerance of ±10 pixels for y-coordinate
        y_key = y // 10 * 10
        
        if y_key not in lines:
            lines[y_key] = []
        
        lines[y_key].append({
            'text': text,
            'x': x,
            'width': width,
            'conf': conf
        })
    
    # Process each line to combine nearby words
    processed_results = []
    for y_key in sorted(lines.keys()):
        line_words = sorted(lines[y_key], key=lambda w: w['x'])
        
        current_phrase = []
        last_x_end = None
        
        for word in line_words:
            # Calculate the gap between this word and the last word
            if last_x_end is None:
                current_phrase.append(word)
            else:
                gap = word['x'] - last_x_end
                # If gap is less than 50 pixels, consider words as part of same phrase
                if gap < 50:
                    current_phrase.append(word)
                else:
                    # Save current phrase and start new one
                    if current_phrase:
                        combined_text = ' '.join(w['text'] for w in current_phrase)
                        avg_conf = sum(w['conf'] for w in current_phrase) // len(current_phrase)
                        processed_results.append({
                            'text': combined_text,
                            'confidence': avg_conf,
                            'position': f"x={current_phrase[0]['x']}, y={y_key}"
                        })
                    current_phrase = [word]
            
            last_x_end = word['x'] + word['width']
        
        # Don't forget the last phrase
        if current_phrase:
            combined_text = ' '.join(w['text'] for w in current_phrase)
            avg_conf = sum(w['conf'] for w in current_phrase) // len(current_phrase)
            processed_results.append({
                'text': combined_text,
                'confidence': avg_conf,
                'position': f"x={current_phrase[0]['x']}, y={y_key}"
            })
    
    # Format output
    output_text = "OCR Detection Results:\n"
    output_text += "====================\n\n"
    
    for item in processed_results:
        output_text += f"Text: {item['text']}\n"
        output_text += f"Confidence: {item['confidence']}%\n"
        output_text += f"Position: {item['position']}\n"
        output_text += "--------------------\n"
    
    # Add arrows for each detected text
    for item in processed_results:
        x = int(item['position'].split('x=')[1].split(',')[0])
        y = int(item['position'].split('y=')[1])
        annotated_image = draw_arrow(annotated_image, x, y)
    
    # Save the annotated image
    output_path = 'static/annotated_image.png'
    annotated_image.save(output_path)
    
    return output_text, output_path

@app.route('/process-image', methods=['POST'])
def process_image_with_arrows():
    """
    Main route for processing images with text detection and arrow annotation.
    Accepts: POST request with JSON containing 'word' to search for
    Returns: JSON response with processing status and filename
    """
    try:
        # Get the search word from the POST request JSON
        data = request.get_json()
        search_text = data.get('word', '')
        
        # Look for image files in the upload folder
        files = os.listdir(UPLOAD_FOLDER)
        if not files:
            return jsonify({
                'success': False,
                'message': 'No images to process'
            })
        
        # Process each valid image file
        for filename in files:
            if filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
                # Construct input and output paths
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                
                # Generate timestamp-based filename for processed image
                current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"{current_time}_{filename}"
                output_path = os.path.join(PROCESSED_FOLDER, output_filename)
                
                # Call text_highlighter.py function to:
                # 1. Detect text using OCR
                # 2. Draw green rectangle around matched text
                # 3. Draw red arrow pointing to text
                processed_image = highlight_text_with_arrow(
                    image_path=input_path,
                    search_text=search_text,
                    output_path=output_path
                )
                
                if processed_image is not None:
                    # Convert processed image for OCR text extraction
                    img = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(img)
                    
                    # Get detailed OCR data including positions
                    ocr_data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
                    
                    # Write OCR results to text file for validation
                    with open('ocr_output.txt', 'w', encoding='utf-8') as f:
                        f.write("OCR Detection Results:\n")
                        f.write("====================\n\n")
                        for i, text in enumerate(ocr_data['text']):
                            if text.strip():
                                confidence = ocr_data['conf'][i]
                                f.write(f"Text: {text}\n")
                                f.write(f"Confidence: {confidence}%\n")
                                f.write(f"Position: x={ocr_data['left'][i]}, y={ocr_data['top'][i]}\n")
                                f.write("--------------------\n")
                    
                    # Return success response with processed filename
                    return jsonify({
                        'success': True,
                        'message': f'Successfully processed image and found text: {search_text}',
                        'filename': output_filename
                    })
                
        # Return failure if no valid images were processed
        return jsonify({
            'success': False,
            'message': 'No valid images found to process'
        })
        
    except Exception as e:
        # Log any errors and return failure response
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58080, debug=True)
