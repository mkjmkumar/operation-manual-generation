# Project overview

I am working on project where I need to create a Operational User Manual from Operations Videos which will check rules in between from rules file. So these operations are like aws ec2 creation, aws s3 creation and a operations manual on how to perform the JP1 jobs check after log into the some remote server etc. So input to this project would be the a video containing all the information related to the operation that need to perform and we need to create the operations user manual. Another input would be the set of rules defined inside the document that can be versioned based on the requirement. Say for example a video containing ec2 operation is given and there set of rules that defined separately in another file. And the rule file says first table would be intro containing the project date and version with dates. Another workbook in expected output should contains the index in manual. third spreadsheet would be the multiple stages with different sections with each section contains the operations steps. And the user manual would be in the form of a single xls spreadsheet with multiple workbook within this file as defined above. The rules are version based can vary depends upon time, say for example if I am not satisfied with the resultant output of operation user manual spreadsheet I will include more rule and generate the spreadsheet again. Now you got an idea so below give you the idea about the workflow that I have identified. Below are the core functionalities for my project to create an effective user operations manual based from operations video media. Below is the provided workflow and some recommendations and enhancements for each step:


Backend
- **Flask**: A lightweight WSGI web application framework used to serve the web interface and handle backend logic.
- **psycopg2-binary**: PostgreSQL database adapter for Python, facilitating database interactions.
- **MinIO**: High performance, Kubernetes-native object storage, used for efficient storage handling.
- **Werkzeug**: A comprehensive WSGI web application library.

Image and Video Processing
- **ffmpeg-python**: A Python wrapper for FFmpeg, used for video processing tasks.
- **Pillow**: The Python Imaging Library adds image processing capabilities to your Python interpreter.
- **pytesseract**: An OCR tool for Python that recognizes text from images.

Development Tools
- **python-dotenv**: Loads environment variables from a `.env` file into `os.environ`, helping in managing configurations.

Installation
This project depends on several system packages:
- **FFmpeg**: For handling video files.
- **Tesseract-OCR**: An OCR engine for image recognition tasks.


8. **Error Tracking and Monitoring**  
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


# Prompt

  You are an expert in TypeScript, Node.js, Next.js App Router, React, Shadcn UI, Radix UI, Tailwind and Supabase.
  
  Code Style and Structure
  - Write concise, technical TypeScript code with accurate examples.
  - Use functional and declarative programming patterns; avoid classes.
  - Prefer iteration and modularization over code duplication.
  - Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
  - Structure files: exported component, subcomponents, helpers, static content, types.
  
  Naming Conventions
  - Use lowercase with dashes for directories (e.g., components/auth-wizard).
  - Favor named exports for components.
  
  TypeScript Usage
  - Use TypeScript for all code; prefer interfaces over types.
  - Avoid enums; use maps instead.
  - Use functional components with TypeScript interfaces.
  
  Syntax and Formatting
  - Use the "function" keyword for pure functions.
  - Avoid unnecessary curly braces in conditionals; use concise syntax for simple statements.
  - Use declarative JSX.
  
  UI, Styling and UI components
  - Use Shadcn UI, Radix, and Tailwind for components and styling.
  - Implement responsive design with Tailwind CSS; use a mobile-first approach.
  - Use shadcn/ui components where available.
  - For layout and styling, use Tailwind CSS utility classes.
  - Maintain a consistent design language across all pages, including typography, color scheme, and component styles.
  - Ensure that the UI is responsive and accessible.
  
  Performance Optimization
  - Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC).
  - Wrap client components in Suspense with fallback.
  - Use dynamic loading for non-critical components.
  - Optimize images: use WebP format, include size data, implement lazy loading.
  
  Key Conventions
  - Use 'nuqs' for URL search parameter state management.
  - Optimize Web Vitals (LCP, CLS, FID).
  - Limit 'use client':
    - Favor server components and Next.js SSR.
    - Use only for Web API access in small components.
    - Avoid for data fetching or state management.
  
  Follow Next.js docs for Data Fetching, Rendering, and Routing.

# Below is the code structure of the project.

$ tree -L 4 -I 'node_modules|git|ls_volume|ui|public'
.
├── components
│   ├── Company
│   │   ├── CompanyListing.tsx
│   │   ├── CreateCompany.tsx
│   │   └── EditCompany.tsx
│   ├── Dashboard.tsx
│   ├── DeltaInsightsDashboard.tsx
│   ├── HandshakeIcon.tsx
│   ├── Header.tsx
│   ├── Login.tsx
│   └── SideBar.tsx
├── components.json
├── Dockerfile
├── hooks
│   └── use-toast.ts
├── instructions
│   └── instructions.md
├── lib
│   ├── setCurrentUser.ts
│   ├── supabaseAdmin.ts
│   ├── supabaseClient.ts
│   └── utils.ts
├── middleware.ts
├── next.config.js
├── next-env.d.ts
├── next-seo.config.js
├── package.json
├── package-lock.json
├── pages
│   ├── api
│   │   ├── companies-list.ts
│   │   ├── company
│   │   │   └── [companyId].ts
│   │   ├── company-add.ts
│   │   ├── company-info.ts
│   │   ├── company-stages.ts
│   │   ├── company-statuses.ts
│   │   ├── countries.ts
│   │   ├── dashboard-data.ts
│   │   ├── delta-insights-data.ts
│   │   ├── export-companies.ts
│   │   ├── industries.ts
│   │   ├── login.ts
│   │   ├── set-current-user.ts
│   │   ├── states.ts
│   │   └── users.ts
│   ├── _app.tsx
│   ├── companies.tsx
│   ├── company_add.tsx
│   ├── company_edit.tsx
│   ├── dashboard.tsx
│   ├── delta-insights.tsx
│   ├── index.tsx
│   ├── login.tsx
│   └── middleware.ts
├── postcss.config.js
├── README.md
├── store
│   └── useStore.ts
├── styles
│   └── globals.css
├── tailwind.config.js
├── __tests__
│   └── LeadsList.test.tsx
└── tsconfig.json

12 directories, 54 files