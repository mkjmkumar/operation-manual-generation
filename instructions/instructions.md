# Project overview

I am working on project where I need to create a Operational User Manual from Operations Videos which will check rules in between from rules file. So these operations are like aws ec2 creation, aws s3 creation and a operations manual on how to perform the JP1 jobs check after log into the some remote server etc. So input to this project would be the a video containing all the information related to the operation that need to perform and we need to create the operations user manual. Another input would be the set of rules defined inside the document that can be versioned based on the requirement. Say for example a video containing ec2 operation is given and there set of rules that defined separately in another file. And the rule file says first table would be intro containing the project date and version with dates. Another workbook in expected output should contains the index in manual. third spreadsheet would be the multiple stages with different sections with each section contains the operations steps. And the user manual would be in the form of a single xls spreadsheet with multiple workbook within this file as defined above. The rules are version based can vary depends upon time, say for example if I am not satisfied with the resultant output of operation user manual spreadsheet I will include more rule and generate the spreadsheet again. Now you got an idea so below give you the idea about the workflow that I have identified. Below are the core functionalities for my project to create an effective user operations manual based from operations video media. Below is the provided workflow and some recommendations and enhancements for each step:


Backend
- **Flask**: A lightweight WSGI web application framework used to serve the web interface and handle backend logic.
- **psycopg2-binary**: PostgreSQL database adapter for Python, facilitating database interactions.
- **MinIO**: High performance, Kubernetes-native object storage, used for efficient storage handling.
- **Werkzeug**: A comprehensive WSGI web application library.

Image and Video Processing
- **OpenCV**: A Python wrapper, used for video processing tasks.
- **ffmpeg-python**: A Python wrapper, used for video processing tasks.
- **pytesseract**: An OCR tool for Python that recognizes text from images.

Development Tools
- **python-dotenv**: Loads environment variables from a `.env` file into `os.environ`, helping in managing configurations.

Installation and packaged being used so far

For Text Detection: 
1. Pytesseract (OCR engine) is being used for:
-   Converting image to text
-   Getting text coordinates
-   Detecting text locations

2. For Web Application:
-   Flask (Python web framework) is handling:
-   File uploads
-   API endpoints
-   Web routing
3. For Frontend:
-   TailwindCSS for styling
-   Vanilla JavaScript for interactions
All the image processing (highlighting, boxing, and arrowing) is being done with OpenCV. The main image processing pipeline is:
4. Pytesseract finds text and coordinates
5. OpenCV draws rectangles, highlights, and arrows
6. OpenCV saves the processed image

7. **Error Tracking and Monitoring**  
We want to ensure our app is running smoothly in production:
TBD

### 9. **Database management system**  
TBD


# Core functionalities or Product requirements document - PRD

Below are the core functionalities for my project to create an effective user operations manual based from operations video media. Below is the provided workflow and some recommendations and enhancements for each step:

1. **Video Collection and Limit Identification**: Clearly document the requirements, such as supported video size, encoding, and file types, before starting the process. This will help ensure that only compatible files are selected.

2. **Audio, Subtitle, and Annotation Extraction**: Consider using tools that can automate the extraction of audio, subtitles, and annotations in various formats. This data can help in creating accurate context and prompts for each user step.

3. **Context and Prompt Creation**: Define a structured template for creating context and prompts to ensure consistency. This could include information like purpose, action, and expected outcome for each step.

4. **Image Generation**: Use video analysis tools to automatically select optimal frames, focusing on key moments or transitions in the video. This step could benefit from automation to streamline the process.

5. **Duplicate Image Removal**: Set a similarity threshold to remove near-duplicate frames. Machine learning algorithms or image matching techniques can help with this step.

6. **Image Refinement**: Implement automated tools to reduce noise and filter out images with PII. Consider privacy-preserving tools if working with sensitive data.

7. **LLM Identification**: Clearly define the criteria for selecting an appropriate LLM (local, cloud-based, or locally trained). This may depend on factors like data sensitivity, cost, and processing requirements.

8. **Image Processing with LLM**: Automate the process of passing images with context to the LLM, if possible. This could help in generating consistent descriptions of user steps or activities.

9. **Chain of Thought Creation**: Create a logical flow for user actions, using clear language that highlights each step's purpose and outcome. This should help users follow each action smoothly.

10. **Repeat Process**: Automate steps 8 and 9 for all images to save time, ensuring that each image and its context are processed consistently.

11. **Storage System Identification**: Choose a scalable and secure storage system, possibly with tagging and categorization features, to store and retrieve generated content easily.

12. **Checklist Comparison**: Regularly compare the generated content with a predefined checklist to ensure quality and completeness. This can be automated for quick validation.

13. **Rule Inclusion**: Include any necessary rules within the output, such as safety guidelines or best practices for each action, to make the manual more comprehensive.

14. **Tool/Utility Selection for Final Document Creation**: Consider using a tool that allows easy formatting, editing, and version control. Tools like Microsoft Word, Google Docs, or specialized documentation software can be beneficial.

**Additional Recommendations and tools that I am looking for**:
- **Automation**: Look for automation opportunities, especially in image extraction, duplicate detection, and LLM processing.
- **User Testing**: Test the user manual with a sample group to ensure it meets users' needs and is easy to follow.
- **Iterative Feedback**: Incorporate feedback loops to refine the manual based on user feedback.
- **Visuals and Annotations**: Add annotated screenshots or visuals to make each step more understandable.




These packages, along with Next.js’s built-in features like **API routes** and **server-side rendering**, will help us to build an efficient and scalable **SalesConnect** application. Let me know if you'd like more details on any of these!


# Below is the code structure of the project.

$ tree -L 4 -I 'node_modules|git|ls_volume|ui|public'
.
├── app.py
├── instructions
│   ├── instructions.md
│   └── prompt.md
├── lib
│   ├── image_processor.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── image_processor.cpython-311.pyc
│   │   ├── __init__.cpython-311.pyc
│   │   ├── text_highlighter.cpython-311.pyc
│   │   └── video_processor.cpython-311.pyc
│   ├── text_highlighter.py
│   └── video_processor.py
├── ocr_output.txt
├── processed
│   └── 20241123_122746_SampleEC2.jpg
├── __pycache__
│   └── translations.cpython-311.pyc
├── Readme.md
├── requirements.txt
├── templates
│   ├── base.html
│   ├── index.html
│   └── login.html
├── translations.py
└── uploads
    ├── rules
    ├── SampleEC2.jpg
    └── videos


12 directories, 54 files