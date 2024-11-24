import cv2
import numpy as np

def test_arrow_drawing():
    # Read the processed image
    image_path = "processed/20241123_225209_SampleEC2.jpg"
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Could not read image")
        return
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Define arrow parameters
    start_point = (50, height//2)  # Starting from left middle
    end_point = (200, height//2)   # Ending 200 pixels to the right
    color = (0, 0, 255)           # Red color in BGR
    thickness = 2
    tip_length = 0.3              # Arrow tip length
    
    # Draw the arrow
    cv2.arrowedLine(
        image,
        start_point,
        end_point,
        color,
        thickness,
        tipLength=tip_length,
        line_type=cv2.LINE_AA
    )
    
    # Save the result
    output_path = "processed/arrow_test_output.jpg"
    cv2.imwrite(output_path, image)
    print(f"Image saved to: {output_path}")

if __name__ == "__main__":
    test_arrow_drawing()
