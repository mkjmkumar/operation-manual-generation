# Main image processing module for text highlighting and annotation
import cv2
import pytesseract  # OCR engine for text detection
import numpy as np
import os
import logging
import sys

# Logger configuration for debugging and monitoring
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def highlight_text_with_arrow(image_path, search_text, output_path=None):
    """
    Main function to process images:
    1. Uses Pytesseract OCR to find text locations
    2. OpenCV for drawing:
        - Green border around text
        - Semi-transparent yellow highlight
        - Blue arrow pointing to text
    3. Saves processed image
    """
    try:
        logger.critical("===================HIGHLIGHT TEXT PROCESSING START ===================")
        logger.critical(f"Current working directory: {os.getcwd()}")
        logger.critical(f"Input image path: {image_path}")
        logger.critical(f"Output path: {output_path}")
        logger.critical(f"Search text: {search_text}")
        
        # Step 1: Image Loading and Validation
        # - Reads image file from provided path using OpenCV
        # - Returns None if image loading fails (corrupted or non-existent file)
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Could not read image: {image_path}")
            return None

        # Step 2: Image Preprocessing for OCR
        # - Converts BGR image to grayscale format
        # - Improves OCR accuracy by removing color information
        # - Reduces noise and normalizes image contrast
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Step 3: OCR Text Detection and Recognition
        # - Performs OCR using Pytesseract engine
        # - Returns dictionary containing:
        #   * text: detected text strings
        #   * conf: confidence levels (0-100)
        #   * left, top: coordinates of text
        #   * width, height: dimensions of text boxes
        ocr_data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
        
        # Step 4: OCR Results Initialization
        # - Gets total number of detected text boxes
        # - Initializes flag to track if search text was found
        # - Prepares for text matching and coordinate extraction
        n_boxes = len(ocr_data['text'])
        found_text = False
        
        for i in range(n_boxes):
            text = ocr_data['text'][i].lower()
            conf = float(ocr_data['conf'][i])
            
            # Only process text with confidence > 0
            if conf > 0 and search_text.lower() in text:
                found_text = True
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]
                
                # Add padding around the text
                padding = 2  # pixels of padding
                x = max(0, ocr_data['left'][i] - padding)
                y = max(0, ocr_data['top'][i] - padding)
                w = ocr_data['width'][i] + (2 * padding)
                h = ocr_data['height'][i] + (2 * padding)
                
                # Draw rectangle around text with thinner, visible border
                border_color = (0, 0, 255)  # Red border in BGR
                border_thickness = 1  # Reduced thickness from 2 to 1
                cv2.rectangle(image, (x, y), (x + w, y + h), border_color, border_thickness)
                
                # Highlight the text by filling rectangle with semi-transparent light yellow
                overlay = image.copy()
                cv2.rectangle(overlay, (x, y), (x + w, y + h), (51, 255, 255), -1)  # Light yellow in BGR
                alpha = 0.3  # Transparency factor
                image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
                
                # Calculate arrow points with increased margin
                margin = 70  # Increased from 50 to 70 pixels
                start_x = max(0, x - margin)
                center_y = y + h//2
                end_x = max(0, x - 10)  # Stop arrow 10 pixels before the text
                
                # Draw arrow
                color = (255, 0, 0)  # Blue color
                thickness = 2
                tip_length = 0.5     # Increased tip length
                cv2.arrowedLine(
                    image,
                    (start_x, center_y),
                    (end_x, center_y),
                    color,
                    thickness,
                    tipLength=tip_length,
                    line_type=cv2.LINE_AA
                )
                logger.info(f"Found text at coordinates: x={x}, y={y}, w={w}, h={h}")

        if not found_text:
            logger.warning(f"Text '{search_text}' not found in image")

        # Save the processed image
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            success = cv2.imwrite(output_path, image)
            if success:
                logger.info(f"Successfully saved image to {output_path}")
            else:
                logger.error("Failed to save image")

        return image

    except Exception as e:
        logger.error(f"Error in highlight_text_with_arrow: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

# Export the function
__all__ = ['highlight_text_with_arrow'] 