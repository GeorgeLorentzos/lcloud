LCloud – Secure Cloud Storage Platform

LCloud is a robust and secure cloud storage platform built with Flask. It enables users to upload, manage, and store files with enterprise-grade security features. The platform supports user authentication, email verification, subscription management via Stripe, and role-based access to scalable file storage.

Designed for reliability, extensibility, and production-grade security.

---

Key Features

- User Authentication & Authorization
  - Secure login and registration
  - Email verification and password reset
  - Session management with Flask-Login

- File Management
  - Upload, rename, and delete files
  - Organized storage with usage tracking
  - Duplicate file handling and quota enforcement

- Subscription System
  - Stripe integration for premium plans
  - Webhook-secured billing and upgrade flow
  - Customer portal for billing management

- Email Notifications
  - SMTP integration via Gmail
  - HTML email templates for verification and password reset
  - TLS encryption enabled

- Responsive Interface
  - Web UI optimized for desktop and mobile devices
  - Built with semantic HTML, responsive CSS, and Jinja2 templating

- Security Best Practices
  - Password hashing with Bcrypt
  - Input sanitization and CSRF protection
  - Secure file handling and ORM-level SQL injection defense

---

Storage Limits

- Free Plan: 2 GB
- Premium Plan: 10 GB

---

File Handling

- Filenames sanitized using secure_filename()
- Duplicate prevention via directory scanning
- Storage quota enforcement with user alerts

---

Email Settings

- Configured for Gmail SMTP with TLS encryption
- HTML email templates with tokenized verification links

---

Security Highlights

- Passwords stored as salted hashes via Flask-Bcrypt
- CSRF protection enforced with Flask-WTF
- Secure form validation using WTForms
- File uploads handled with MIME-type checks and filename sanitization
- SQL injection protection through SQLAlchemy ORM

---

Technology Stack

- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- Security: Bcrypt, WTForms validators, Flask-Mail
- Payments: Stripe API (Checkout, Billing Portal, Webhooks)
- Background Jobs: APScheduler
- Email: Gmail SMTP with Flask-Mail
- Frontend: Jinja2 templates, HTML5, CSS3
- Deployment: Environment variables via .env file

---

Prerequisites

- Python 3.7 or higher
- Gmail account (for SMTP email service)
- Stripe account (for subscription management)

---

Installation

1. Clone the Repository

git clone https://github.com/GeorgeLorentzos/lcloud.git
cd lcloud

2. Install Dependencies

Using requirements.txt:

pip install -r requirements.txt

Or manually:

pip install flask flask-sqlalchemy flask-login flask-wtf wtforms flask-bcrypt python-dotenv werkzeug stripe pytz flask-mail python-dateutil apscheduler

3. Configure Environment Variables

Create a .env file in the project root with the following contents:

# Flask Configuration
SECRET_KEY=your-secret-key

# Email Configuration (Gmail SMTP)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

Replace the placeholder values with your actual credentials.

---

Running the Application

python app.py

Access the app at: http://127.0.0.1:5000

---

Project Structure

lcloud/
├── app.py
├── .env
├── requirements.txt
├── lcloud.db
├── storage/
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── account.html
│   ├── verify.html
│   ├── alert.html
│   ├── reset-password.html
│   ├── request-password-reset.html
│   └── 404.html
└── static/
    ├── css/
    ├── js/
    └── images/

---

License

© 2025 George Lorentzos. All rights reserved.

This software is provided for personal and educational use only. Commercial use, distribution, or reproduction without explicit written permission is strictly prohibited.

---
