# SmartHire — Smart Job Portal & Resume Analyzer

A beginner-friendly full-stack Python project built with Flask and MySQL. Users can register, browse jobs, upload PDF/TXT resumes, extract skills, calculate job-match scores, and review applications.

## Features
- User registration and secure password hashing
- Login/logout with Flask sessions
- Job listing and job details
- Resume upload (PDF/TXT)
- Python-based skill extraction
- Skill matching and match percentage
- MySQL persistence
- Application dashboard
- JSON endpoint: `/api/jobs`

## Tech Stack
Python, Flask, MySQL, HTML, CSS, Bootstrap, JavaScript, pypdf

## Project Structure
```text
smart_job_portal_resume_analyzer/
├── app.py
├── requirements.txt
├── schema.sql
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── job_detail.html
│   ├── apply.html
│   ├── result.html
│   └── dashboard.html
└── static/
    ├── style.css
    └── uploads/
```

## Requirements
- Python 3.10+
- MySQL 8+
- pip
- Git

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-job-portal-resume-analyzer.git
cd smart-job-portal-resume-analyzer
```

### 2. Create a virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MySQL
Start MySQL and run:
```bash
mysql -u root -p < schema.sql
```

Or open MySQL Workbench and execute `schema.sql`.

If your MySQL password is not empty, set environment variables.

Windows PowerShell:
```powershell
$env:DB_PASSWORD="your_mysql_password"
```

macOS/Linux:
```bash
export DB_PASSWORD="your_mysql_password"
```

Optional:
```text
DB_HOST=localhost
DB_USER=root
DB_NAME=job_portal
SECRET_KEY=replace-with-a-random-secret
```

### 5. Run the application
```bash
python app.py
```

Open:
```text
http://127.0.0.1:5000
```

## How the Resume Analyzer Works
1. User selects a job.
2. User uploads a PDF/TXT resume.
3. Python extracts text.
4. The application searches the text for supported technical skills.
5. The extracted skills are compared with the job's required skills.
6. Match percentage, matched skills, and missing skills are displayed.
7. The application and analysis are stored in MySQL.

## Resume Project Entry
**Smart Job Portal & Resume Analyzer**  
*Python, Flask, MySQL, HTML, CSS, JavaScript*

- Developed a Python-based job portal with user authentication, job search, resume upload, and application tracking.
- Built a resume analyzer using Python to extract technical skills from uploaded PDF/TXT resumes.
- Implemented a skill-matching algorithm to calculate candidate-job compatibility and identify missing skills.
- Integrated Flask REST endpoints with MySQL for persistent storage of users, jobs, resumes, and applications.

## Future Enhancements
- NLP-based skill extraction
- Admin dashboard
- JWT authentication
- Email notifications
- Job recommendation model
- Docker deployment
- Cloud deployment

## Important
This is a portfolio/learning project. Before using it in production, add CSRF protection, stricter file validation, rate limiting, secure secret management, and safer file storage.
