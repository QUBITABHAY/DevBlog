# DEV_BLOG - Flask Blog Application

A full-featured blog application built with Flask and MongoDB. This modern web application enables users to create, manage, and share blog posts with a clean, responsive interface.

## Tech Stack
- Backend: Flask (Python)
- Database: MongoDB
- Frontend: Tailwind CSS
- Authentication: Flask-Login
- Email: Flask-Mail

## Overview
DEV_BLOG provides a robust platform for bloggers with features like user authentication, content management, and email notifications. Perfect for developers who want to share their technical insights and experiences.

## Features
- User Authentication (Register, Login, Logout)
- CRUD Operations for Blog Posts
- User Profile Management
- Password Reset via Email
- Post Categories and Tags
- Responsive Design with Tailwind CSS

## Quick Start

1. **Clone and Setup:**
```bash
git clone https://github.com/yourusername/DEV_BLOG.git
cd DEV_BLOG
python3 -m venv venv
source venv/bin/activate  # For Mac
pip install -r requirements.txt
cp .env.example .env
```

2. **Configure Environment:**
```python
# .env file
SECRET_KEY=your_secret_key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
EMAIL_USER=your_email
EMAIL_PASS=your_email_password
```

3. **Run Development Server:**
```python
python run.py  # Runs with debug mode
```

## Project Structure
```
DEV_BLOG/
├── Dev_BLOG/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   ├── static/
│   └── templates/
├── requirements.txt
└── run.py
```

## Development Tools

1. **Watch Tailwind Changes:**
```bash
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
```

2. **Run Tests:**
```bash
python -m pytest
```

## Contributing
1. Fork repository
2. Create feature branch
3. Submit pull request

## Documentation
Detailed documentation about setup, configuration, and usage can be found in the project's source code comments and docstrings.
