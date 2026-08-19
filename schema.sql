CREATE DATABASE IF NOT EXISTS job_portal;
USE job_portal;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    extracted_text LONGTEXT,
    skills TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    resume_id INT NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    matched_skills TEXT,
    missing_skills TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

INSERT INTO jobs (title, company, location, description, required_skills)
SELECT 'Custom Software Engineer - Python', 'Accenture', 'Hyderabad',
'Build, test and maintain software solutions using Python and modern engineering practices.',
'python,sql,git,rest api,oop,linux'
WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title='Custom Software Engineer - Python' AND company='Accenture');

INSERT INTO jobs (title, company, location, description, required_skills)
SELECT 'Python Backend Developer', 'TechNova', 'Hyderabad',
'Develop REST APIs and backend services with Python and Flask.',
'python,flask,sql,mysql,rest api,git,oop'
WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title='Python Backend Developer' AND company='TechNova');

INSERT INTO jobs (title, company, location, description, required_skills)
SELECT 'Junior Data Engineer', 'DataWorks', 'Bengaluru',
'Work with Python data processing pipelines and SQL databases.',
'python,pandas,numpy,sql,mysql,git'
WHERE NOT EXISTS (SELECT 1 FROM jobs WHERE title='Junior Data Engineer' AND company='DataWorks');
