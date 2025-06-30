# LCloud - Cloud Storage

A Flask-based cloud storage application that allows users to upload, manage, and store files securely. Features include user authentication, email verification, subscription management with Stripe, and file management capabilities.

## Features

- **User Authentication**: Secure registration and login system with email verification
- **File Management**: Upload, rename, delete, and organize files
- **Storage Management**: Track storage usage with configurable limits
- **Subscription System**: Premium plans with Stripe integration
- **Email Notifications**: Account verification and password reset emails
- **Responsive Design**: Works on desktop and mobile devices
- **Security**: Password hashing, secure file handling, and input validation

## Tech Stack

```bash
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

## Prerequisites

- Python 3.7+
- Gmail account (for email functionality)
- Stripe account (for subscription features)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GeorgeLorentzos/lcloud.git
cd lcloud
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms flask-bcrypt python-dotenv werkzeug stripe pytz flask-mail python-dateutil apscheduler
```

Or install `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

If you already have a `.env` file, please verify it includes the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

Update the values as needed.

## Running the Application

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

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
└── static/              # CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

## Usage

### User Registration
1. Visit `/signup` to create new account
2. Check email for verification link
3. Click verification link to activate account

### File Management
1. Login to access dashboard
2. Upload files using the upload form
3. Rename files by clicking the rename button
4. Delete files using the delete button

### Subscription Management
1. Go to Account settings
2. Click "Upgrade to Premium" for more storage
3. Complete Stripe checkout process
4. Manage subscription through billing portal

## Configuration Options

### Storage Limits
- **Free Plan**: 2GB storage
- **Premium Plan**: 10GB storage

### File Upload
- Secure filename handling
- Duplicate file prevention
- Storage quota enforcement

### Email Settings
- SMTP server: Gmail
- TLS encryption enabled
- Template-based HTML emails

## Security Considerations

- Passwords are hashed using bcrypt
- File names are sanitized using `secure_filename()`
- SQL injection protection via SQLAlchemy ORM
- CSRF protection with Flask-WTF
- Input validation on all forms

## License

Copyright (c) 2025 George Lorentzos

Permission is granted to view this code for personal or educational purposes only. 
Any reproduction, redistribution, or commercial use is prohibited without written permission.
