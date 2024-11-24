# Helper module for image processing operations
import cv2
import numpy as np
import logging

def draw_arrow_on_image(image, start_x, center_y, end_x, end_y, color=(0, 0, 255), thickness=1, tipLength=0.3, line_type=cv2.LINE_AA):
    """
    Utility function for drawing arrows on images using OpenCV
    - Creates directional arrows with customizable:
        - Color
        - Thickness (reduced to 1)
        - Tip length
        - Anti-aliasing
    """
    try:
        # Create points tuples
        start_point = (int(start_x), int(center_y))
        end_point = (int(end_x), int(end_y))
        
        # Draw the arrow
        cv2.arrowedLine(
            image,
            start_point,
            end_point,
            color,
            thickness,
            line_type=line_type,
            tipLength=tipLength
        )
        return image
    except Exception as e:
        print(f"Error drawing arrow: {str(e)}")
        return image 