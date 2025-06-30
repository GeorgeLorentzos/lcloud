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

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Database**: SQLite
- **Payment Processing**: Stripe
- **Email Service**: Flask-Mail (Gmail SMTP)
- **Authentication**: Flask-Bcrypt
- **File Handling**: Werkzeug
- **Task Scheduling**: APScheduler

## Prerequisites

- Python 3.7+
- Gmail account (for email functionality)
- Stripe account (for subscription features)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lcloud.git
cd lcloud
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms flask-bcrypt python-dotenv werkzeug stripe pytz flask-mail python-dateutil apscheduler
```

Or create a `requirements.txt` file:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
WTForms==3.0.1
Flask-Bcrypt==1.0.1
python-dotenv==1.0.0
Werkzeug==2.3.7
stripe==6.6.0
pytz==2023.3
Flask-Mail==0.9.1
python-dateutil==2.8.2
APScheduler==3.10.4
```

Then install:
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

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

## Configuration Guide

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in `MAIL_PASSWORD`

### Stripe Setup

1. **Create Stripe Account**: [https://stripe.com](https://stripe.com)
2. **Get API Keys**:
   - Dashboard → Developers → API keys
   - Copy Publishable key and Secret key
3. **Setup Webhook**:
   - Dashboard → Developers → Webhooks
   - Add endpoint: `http://your-domain.com/webhook`
   - Select events: `checkout.session.completed`, `customer.subscription.deleted`
   - Copy webhook secret

### Database Setup

The application will automatically create the SQLite database on first run. No additional setup required.

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

### Production Deployment

For production deployment, consider using:

- **Gunicorn**: `pip install gunicorn`
- **Nginx**: As reverse proxy
- **PostgreSQL**: Instead of SQLite

Example Gunicorn command:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Project Structure

```
lcloud/
├── app.py                 # Main application file
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── lcloud.db             # SQLite database (auto-generated)
├── storage/              # User file storage directory
├── templates/            # HTML templates
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

## API Endpoints

### Authentication
- `GET/POST /signup` - User registration
- `GET/POST /signin` - User login
- `GET /logout` - User logout
- `GET /verify/<token>` - Email verification

### File Management
- `GET/POST /` - Dashboard (file listing and upload)
- `POST /delete/<filename>` - Delete file
- `POST /rename` - Rename file

### Account Management
- `GET/POST /account` - Account settings
- `POST /delete_account` - Delete user account

### Subscription
- `POST /create-checkout-session` - Create Stripe checkout
- `POST /create-billing-portal-session` - Access billing portal
- `POST /webhook` - Stripe webhook handler

### Password Reset
- `GET/POST /request-password-reset` - Request password reset
- `GET/POST /verify/<token>` - Reset password with token

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

## Troubleshooting

### Common Issues

1. **Email not sending**:
   - Check Gmail app password
   - Verify 2FA is enabled
   - Check firewall settings

2. **Stripe webhook not working**:
   - Verify webhook URL is accessible
   - Check webhook secret matches
   - Ensure HTTPS in production

3. **File upload fails**:
   - Check storage directory permissions
   - Verify storage quota not exceeded
   - Check file size limits

### Debug Mode

Set `debug=True` in `app.run()` for detailed error messages during development.

## Security Considerations

- Passwords are hashed using bcrypt
- File names are sanitized using `secure_filename()`
- SQL injection protection via SQLAlchemy ORM
- CSRF protection with Flask-WTF
- Input validation on all forms

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email your-email@example.com or create an issue on GitHub.

## Changelog

### v1.0.0
- Initial release
- User authentication system
- File upload and management
- Stripe subscription integration
- Email verification and password reset
