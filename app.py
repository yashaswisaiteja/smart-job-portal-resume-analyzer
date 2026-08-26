from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector
import os
import re


app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)


# =========================================================
# UPLOAD SETTINGS
# =========================================================

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "txt",
    "pdf"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

#DB_CONFIG = {
    #"host": os.getenv(
    #    "DB_HOST",
     #   "localhost"
    #),

#    "user": os.getenv(
 #       "DB_USER",
  #      "root"
   # ),

    #"password": os.getenv(
     #   "DB_PASSWORD",
      #  ""
    #),
    #"port": int(os.getenv("DB_PORT", "3306")),

    #"database": os.getenv(
     #   "DB_NAME",
      #  "job_portal"
    #)
#}
DB_CONFIG = {
    "host": os.getenv("DB_HOST") or "localhost",
    "port": int(os.getenv("DB_PORT") or "3306"),
    "user": os.getenv("DB_USER") or "root",
    "password": os.getenv("DB_PASSWORD") or "",
    "database": os.getenv("DB_NAME") or "job_portal"
}

def get_db():
    return mysql.connector.connect(
        **DB_CONFIG
    )


# =========================================================
# FILE VALIDATION
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# RESUME TEXT EXTRACTION
# =========================================================

def extract_text(filepath):

    ext = filepath.rsplit(
        ".",
        1
    )[1].lower()

    if ext == "txt":

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            return f.read()

    try:

        from pypdf import PdfReader

        reader = PdfReader(filepath)

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    except Exception:

        return ""


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize(text):

    return re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text.lower()
    )


# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(text):

    catalog = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "flask",
        "django",
        "spring boot",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "git",
        "github",
        "docker",
        "aws",
        "rest api",
        "html",
        "css",
        "pandas",
        "numpy",
        "tensorflow",
        "keras",
        "opencv",
        "machine learning",
        "data structures",
        "algorithms",
        "oop",
        "linux"
    ]

    normalized = normalize(text)

    return [
        skill
        for skill in catalog
        if skill in normalized
    ]


# =========================================================
# MATCH CALCULATION
# =========================================================

def calculate_match(
    resume_skills,
    job_skills
):

    job_skills = [
        s.strip().lower()
        for s in job_skills.split(",")
        if s.strip()
    ]

    matched = sorted(
        set(resume_skills)
        &
        set(job_skills)
    )

    missing = sorted(
        set(job_skills)
        -
        set(resume_skills)
    )

    score = (
        round(
            len(matched)
            /
            len(set(job_skills))
            *
            100
        )
        if job_skills
        else 0
    )

    return (
        score,
        matched,
        missing
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    db = get_db()

    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    cur.execute(
        """
        SELECT *
        FROM jobs
        ORDER BY created_at DESC
        """
    )

    jobs = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        "index.html",
        jobs=jobs
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form[
            "name"
        ].strip()

        email = request.form[
            "email"
        ].strip().lower()

        password = request.form[
            "password"
        ]

        db = get_db()

        cur = db.cursor(
            buffered=True
        )

        try:

            cur.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password_hash
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    name,
                    email,
                    generate_password_hash(
                        password
                    )
                )
            )

            db.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except mysql.connector.IntegrityError:

            flash(
                "Email already registered.",
                "danger"
            )

        finally:

            cur.close()
            db.close()

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form[
            "email"
        ].strip().lower()

        password = request.form[
            "password"
        ]

        db = get_db()

        cur = db.cursor(
            dictionary=True,
            buffered=True
        )

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        db.close()

        if user and check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    db = get_db()

    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    cur.execute(
        """
        SELECT
            a.*,
            j.title,
            j.company,
            r.filename AS resume_filename

        FROM applications a

        JOIN jobs j
            ON a.job_id = j.id

        JOIN resumes r
            ON a.resume_id = r.id

        WHERE a.user_id = %s

        ORDER BY a.applied_at DESC
        """,
        (session["user_id"],)
    )

    applications = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        "dashboard.html",
        applications=applications
    )


# =========================================================
# JOB DETAILS
# =========================================================

@app.route("/jobs/<int:job_id>")
def job_detail(job_id):

    db = get_db()

    # buffered=True fixes:
    # mysql.connector.errors.InternalError:
    # Unread result found
    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    # Get job details
    cur.execute(
        """
        SELECT *
        FROM jobs
        WHERE id=%s
        """,
        (job_id,)
    )

    job = cur.fetchone()

    if not job:

        cur.close()
        db.close()

        return "Job not found", 404

    # Assume the user has not applied
    already_applied = False

    # Check if logged-in user already applied
    if "user_id" in session:

        cur.execute(
            """
            SELECT id
            FROM applications
            WHERE user_id=%s
            AND job_id=%s
            """,
            (
                session["user_id"],
                job_id
            )
        )

        application = cur.fetchone()

        if application:

            already_applied = True

    cur.close()
    db.close()

    return render_template(
        "job_detail.html",
        job=job,
        already_applied=already_applied
    )


# =========================================================
# APPLY FOR JOB + RESUME ANALYSIS
# =========================================================

@app.route(
    "/jobs/<int:job_id>/apply",
    methods=["GET", "POST"]
)
def apply(job_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    db = get_db()

    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    # Get job
    cur.execute(
        """
        SELECT *
        FROM jobs
        WHERE id=%s
        """,
        (job_id,)
    )

    job = cur.fetchone()

    cur.close()
    db.close()

    if not job:

        return "Job not found", 404


    # =====================================================
    # PREVENT DUPLICATE APPLICATION
    # =====================================================

    db = get_db()

    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    cur.execute(
        """
        SELECT id
        FROM applications
        WHERE user_id=%s
        AND job_id=%s
        """,
        (
            session["user_id"],
            job_id
        )
    )

    existing_application = cur.fetchone()

    cur.close()
    db.close()

    if existing_application:

        flash(
            "You have already applied for this job.",
            "warning"
        )

        return redirect(
            url_for(
                "job_detail",
                job_id=job_id
            )
        )


    # =====================================================
    # PROCESS APPLICATION
    # =====================================================

    if request.method == "POST":

        file = request.files.get(
            "resume"
        )

        if (
            not file
            or file.filename == ""
            or not allowed_file(
                file.filename
            )
        ):

            flash(
                "Upload a PDF or TXT resume.",
                "danger"
            )

            return redirect(
                request.url
            )


        # Create safe filename
        filename = secure_filename(
            f"{session['user_id']}_{file.filename}"
        )

        # File path
        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save uploaded resume
        file.save(path)


        # Extract resume text
        text = extract_text(
            path
        )


        # Extract skills
        skills = extract_skills(
            text
        )


        # Calculate match score
        score, matched, missing = calculate_match(
            skills,
            job["required_skills"]
        )


        # =================================================
        # SAVE RESUME
        # =================================================

        db = get_db()

        cur = db.cursor(
            buffered=True
        )

        cur.execute(
            """
            INSERT INTO resumes
            (
                user_id,
                filename,
                extracted_text,
                skills
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                session["user_id"],
                filename,
                text,
                ", ".join(skills)
            )
        )

        resume_id = cur.lastrowid


        # =================================================
        # SAVE APPLICATION
        # =================================================

        cur.execute(
            """
            INSERT INTO applications
            (
                user_id,
                job_id,
                resume_id,
                match_score,
                matched_skills,
                missing_skills
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                session["user_id"],
                job_id,
                resume_id,
                score,
                ", ".join(matched),
                ", ".join(missing)
            )
        )

        db.commit()

        cur.close()
        db.close()


        # =================================================
        # SHOW RESULT
        # =================================================

        return render_template(
            "result.html",
            job=job,
            score=score,
            matched=matched,
            missing=missing,
            resume_filename=filename
        )


    return render_template(
        "apply.html",
        job=job
    )


# =========================================================
# API - JOBS
# =========================================================

@app.route("/api/jobs")
def api_jobs():

    db = get_db()

    cur = db.cursor(
        dictionary=True,
        buffered=True
    )

    cur.execute(
        """
        SELECT
            id,
            title,
            company,
            location,
            description,
            required_skills
        FROM jobs
        """
    )

    jobs = cur.fetchall()

    cur.close()
    db.close()

    return jsonify(
        jobs
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )