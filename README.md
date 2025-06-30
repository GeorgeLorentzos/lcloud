# LCloud – Secure Cloud Storage Platform

**LCloud** is a robust, secure cloud storage platform built with Flask. It enables users to upload, manage, and store files with enterprise-grade security features. The platform supports user authentication, email verification, subscription management via Stripe, and role-based access to scalable file storage.

Designed for reliability, extensibility, and production-grade security, LCloud is ideal for developers, startups, or businesses seeking a customizable file storage solution.

---

## Key Features

- **User Authentication & Authorization**
  - Secure login and registration
  - Email verification and password reset
  - Session management with Flask-Login

- **File Management**
  - Upload, rename, and delete files
  - Organized storage with usage tracking
  - Duplicate file handling and quota enforcement

- **Subscription System**
  - Stripe integration for premium plans
  - Webhook-secured billing and upgrade flow
  - Customer portal for billing management

- **Email Notifications**
  - SMTP integration via Gmail
  - HTML email templates for verification and password reset
  - TLS encryption enabled

- **Responsive Interface**
  - Web UI optimized for desktop and mobile devices
  - Built with semantic HTML, responsive CSS, and templating

- **Security Best Practices**
  - Password hashing with Bcrypt
  - Input sanitization and CSRF protection
  - Secure file handling and ORM-level SQL injection defense

---

## Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Security**: Bcrypt, WTForms validators, Flask-Mail
- **Payments**: Stripe API (checkout, billing portal, webhooks)
- **Background Jobs**: APScheduler
- **Email**: Gmail SMTP with Flask-Mail
- **Frontend**: Jinja2 templates, HTML5/CSS3
- **Deployment Ready**: Environment variables via `.env` and secure production configurations

---

## Prerequisites

- Python 3.7 or higher
- Gmail account (for SMTP email service)
- Stripe account (for handling subscriptions)

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/GeorgeLorentzos/lcloud.git
cd lcloud
```

### Step 2: Install Dependencies

Install via `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms flask-bcrypt python-dotenv werkzeug stripe pytz flask-mail python-dateutil apscheduler
```

### Step 3: Environment Configuration

Create a `.env` file in the root directory with the following:

```env
# Flask Configuration
SECRET_KEY=your-secret-key

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

Update the keys with your actual credentials.

---

## Running the Application

```bash
python app.py
```

The application will run at: `http://127.0.0.1:5000`

---

## Project Structure

```
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
```

---

## Usage Overview

### Registration & Verification
1. Visit `/signup` to create a new account
2. Check your email inbox for a verification link
3. Activate your account before logging in

### File Management Dashboard
- Upload files directly from the dashboard
- Rename and delete files via UI controls
- Monitor storage usage and plan limits

### Subscription Workflow
- Access subscription settings via account dashboard
- Upgrade to a premium plan using Stripe
- Manage billing securely via the Stripe customer portal

---

## Configuration Options

### Storage Limits
- **Free Plan**: 2 GB
- **Premium Plan**: 10 GB

### File Handling
- Filenames are sanitized using `secure_filename()`
- Duplicate prevention via directory scanning
- Storage quota enforcement with alerts

### Email Settings
- Configured for Gmail SMTP
- TLS encryption enabled
- Email templates written in HTML with tokenized verification links

---

## Security Architecture

- Passwords stored as salted hashes via `Flask-Bcrypt`
- CSRF protection enforced via `Flask-WTF`
- Secure form validation using WTForms
- File uploads handled with MIME-type checks and filename sanitization
- SQL injection protection through SQLAlchemy ORM

---

## License

© 2025 George Lorentzos. All rights reserved.

This software is provided for personal and educational use only. Commercial use, distribution, or reproduction without explicit written permission is strictly prohibited.

---

## Contact

For business inquiries or enterprise licensing, please contact:  
📧 **georgelorentzos@gmail.com**

