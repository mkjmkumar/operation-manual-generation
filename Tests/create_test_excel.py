from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os
from datetime import datetime

def create_test_excel():
    try:
        # Create a new workbook and select the active sheet
        wb = Workbook()
        
        # First worksheet - Text content
        text_sheet = wb.active
        text_sheet.title = "Sample Text"
        
        # Add some sample text
        text_sheet['A1'] = "Operation Manual Test"
        text_sheet['A2'] = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        text_sheet['A4'] = "Section 1: Introduction"
        text_sheet['A5'] = "This is a sample text worksheet demonstrating Excel generation capabilities."
        
        # Create second worksheet - Image content
        image_sheet = wb.create_sheet(title="Sample Image")
        
        # Get the image path
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'processed', 
            'frame_219_2024-11-24T06-30-21-859Z.jpg'
        )
        
        # Add image to the second worksheet
        if os.path.exists(image_path):
            img = Image(image_path)
            
            # You can adjust image size if needed
            img.width = 600
            img.height = 400
            
            # Add image to cell B2
            image_sheet.add_image(img, 'B2')
        else:
            image_sheet['B2'] = "Image not found at specified path"
            print(f"Warning: Image not found at {image_path}")
        
        # Create tests directory if it doesn't exist
        output_dir = os.path.dirname(__file__)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the workbook
        output_path = os.path.join(output_dir, 'test_manual.xlsx')
        wb.save(output_path)
        print(f"Excel file created successfully at: {output_path}")
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")

if __name__ == "__main__":
    create_test_excel() 