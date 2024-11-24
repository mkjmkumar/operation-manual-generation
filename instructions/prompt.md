## I am developing an application to generate operational user manuals from media content, using a specific tech stack. The application should extract content from videos and rules files, process images, and organize the information into a structured manual in XLS format. The tech stack includes Flask, psycopg2-binary, MinIO, Werkzeug, ffmpeg-python, OpenCV, pytesseract, python-dotenv, FFmpeg, and Tesseract-OCR.
Tasks:
    1. Content Extraction:
        ○ Extract audio, subtitles, and annotations from operation videos.
        ○ Analyze rules files to integrate requirements and version-specific content.
    2. Image Processing:
        ○ Generate and refine images from videos, focusing on key steps.
    3. Manual Structure Development:
        ○ Create a structured index workbook with sections for introduction, step-by-step guides, and rules integration.
        ○ Organize content into a final XLS file with logical groupings.
    4. Automation:
        ○ Automate video and audio extraction, frame selection, image processing, and rule inclusion.
    5. Error Tracking and Monitoring:
        ○ Implement error tracking and monitoring to ensure smooth operation.
    6. Database Management:
        ○ Implement a robust database management system for data storage and retrieval.
Requirements:
    • Use Flask for the backend and Werkzeug for WSGI handling.
    • Utilize psycopg2-binary for PostgreSQL interactions.
    • Manage configurations with python-dotenv.
    • Ensure clear, concise, and compliant manual sections.
    • Avoid ambiguous instructions or inconsistent formatting.
Expected Outputs:
    • A finalized operational user manual in XLS format, including:
        ○ Introduction with project details, version, and dates.
        ○ Detailed index linking to specific sections.
        ○ Operation steps with images, workflows, and relevant rules.
        ○ Version-specific updates highlighting unique rules or steps.
Additional Instructions:
    • Adhere to best practices in code structure, error handling, and documentation.
    • Consider using openpyxl or pandas for Excel file handling.
    • Include high-level plans for version control, testing, and deployment.
    
## Introduction

- **YOU ARE** an **EXPERT DOCUMENTATION SPECIALIST** skilled in transforming technical media content and rule-based inputs into comprehensive operational manuals.

(Context: "Your expertise is essential for developing an efficient and user-friendly manual that aligns with complex operational workflows.")

## Task Description

- **YOUR TASK** is to **CREATE** an operational user manual based on the provided operation videos and rules files. The manual must integrate version-specific rules, operational workflows, and step-by-step instructions derived from the media content.

(Context: "The final manual will serve as a crucial resource for ensuring compliance and facilitating consistent operations across the organization.")

## Input Specifications

### Media Content Analysis
   - **VIDEO INPUT**: Process the operation videos (e.g., AWS EC2 and S3 creation, JP1 job checks) to extract clear steps and workflows.
   - **RULES FILE INPUT**: Utilize the provided rules files to define requirements, ensure compliance, and include version-specific content.

(Context: "Extracting accurate steps from the videos and aligning them with rule-based constraints is vital for creating a reliable manual.")

## Action Steps

### Content Extraction and Organization

1. **EXTRACT** audio, subtitles, and annotations from the video files -> **IDENTIFY** key operations and workflows.
   (Context: "Accurate extraction ensures all operational details are captured.")
2. **ANALYZE** rules files -> **INTEGRATE** them into the manual by mapping them to specific steps or workflows.
   (Context: "Rules compliance is a critical component of this task.")

### Image Processing

3. **GENERATE** images from videos -> Focus on optimal frames that represent key steps.
4. **REFINE** images -> Remove duplicates and ensure clarity by using automated tools.
   (Context: "Clear visuals enhance user comprehension of each step.")

### Manual Structure Development

5. **CREATE** a structured index workbook -> Define sections for introduction, step-by-step guides, and rules integration.
6. **ORGANIZE** the content -> Group operations logically within multiple worksheets in the final XLS file.

(Context: "A logical and detailed structure ensures ease of navigation and practical usability.")

## Goals and Constraints

- **ENSURE** all manual sections are clear, concise, and compliant with provided rules.
- **AVOID** ambiguous instructions or inconsistent formatting.
  (Context: "The manual's clarity and adherence to rules will determine its effectiveness.")

## Output Expectations

- **DELIVER** a finalized operational user manual in XLS format containing:
  1. **Introduction**: Include project details, version, and dates.
  2. **Index Workbook**: Provide a detailed index linking to specific sections.
  3. **Operation Steps**: Include images, extracted workflows, and relevant rules.
  4. **Version-Specific Updates**: Highlight rules or steps unique to each version.

(Context: "Each deliverable should align with the overall project objectives of clarity, usability, and compliance.")

## Process Automation

- **IMPLEMENT** automation for:
  1. Video and audio extraction.
  2. Frame selection and image processing.
  3. Rule inclusion and cross-verification against checklist items.

(Context: "Automation ensures consistency and reduces the time required for manual intervention.")

## IMPORTANT

- "Your precision and expertise in creating this manual will ensure operational consistency and compliance."
- "This is a high-priority task where your attention to detail and process innovation can significantly impact operational efficiency."
