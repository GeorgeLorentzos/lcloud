# 🌩️ LCloud - Cloud Storage Platform

**LCloud** is a Flask-based cloud storage application that allows users to securely upload, manage, and store files. Key features include user authentication, email verification, Stripe-based subscription plans, and robust file handling.

---

## 🚀 Features

- 🔐 **User Authentication**: Secure login, registration, and email verification  
- 📂 **File Management**: Upload, rename, delete, and organize files  
- 📊 **Storage Tracking**: Configurable storage limits and usage tracking  
- 💳 **Subscription Plans**: Premium plan support via Stripe integration  
- ✉️ **Email Notifications**: Account verification and password reset via Gmail  
- 📱 **Responsive UI**: Fully functional on desktop and mobile  
- 🛡️ **Security First**: Password hashing, input validation, secure file handling  

---

## 🛠️ Tech Stack

```python
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField 
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
import os
import re
import shutil
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import stripe
from pytz import timezone as pytz_timezone
import pytz
from flask_mail import Mail, Message
import random
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
```

---

## ✅ Prerequisites

- Python 3.7+
- Gmail account (for email functionality)
- Stripe account (for subscriptions)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GeorgeLorentzos/lcloud.git
cd lcloud
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms flask-bcrypt python-dotenv werkzeug stripe pytz flask-mail python-dateutil apscheduler
```

---

### 3. Environment Configuration

Create a `.env` file in the root directory and add:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here

# Gmail SMTP Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Stripe API Keys
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

---

## ▶️ Running the Application

```bash
python app.py
```

Then visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🗂️ Project Structure

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

## 👥 Usage

### 🔐 Registering an Account

1. Go to `/signup`
2. Fill out the form
3. Check your email and click the verification link

### 📁 Managing Files

- Upload files via the dashboard
- Rename and delete files with ease
- Monitor storage usage

### 💳 Upgrading Your Plan

1. Go to **Account Settings**
2. Click "Upgrade to Premium"
3. Complete payment via Stripe
4. Manage your billing via the customer portal

---

## ⚙️ Configuration Options

### 🔒 Storage Limits

- **Free Plan**: 2GB
- **Premium Plan**: 10GB

### 📤 Upload Handling

- Filenames sanitized with `secure_filename()`
- Duplicate file checks
- Enforced storage quota

### 📧 Email Setup

- Gmail SMTP
- TLS enabled
- HTML-based email templates

---

## 🔐 Security

- Passwords hashed using **bcrypt**
- Secure filenames using **Werkzeug**
- ORM-based SQL injection protection via **SQLAlchemy**
- CSRF protection via **Flask-WTF**
- Input validation with **WTForms**

---

## 📄 License

**© 2025 George Lorentzos**

For personal or educational use only. Reproduction, redistribution, or commercial use is prohibited without written permission.
