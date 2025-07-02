# LCloud
- A robust Python Flask web application for secure cloud storage and file management.

## Key Features  
### Security & Authentication  
- Multi-layer user authentication with Flask-Login and bcrypt hashing  
- Complete email verification system for new account activation  
- Secure password recovery with time-limited tokens  
- CSRF protection on all forms  

### File Management  
- User-isolated storage with dedicated folders  
- Intelligent quota system (2GB free / 10GB premium)  
- Secure file handling with Werkzeug's secure_filename()  
- Timezone-aware timestamps (pytz integration)  

### Subscription & Payments  
- Stripe integration for premium subscriptions  
- Automated billing portal for customers  
- Webhook handling for payment events  
- Tiered storage plans with automatic upgrades/downgrades  

### Email System  
- SMTP integration with TLS encryption  
- Custom HTML templates for verification/reset emails  
- Async email delivery (using Flask-Mail)  

## Usage
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/lcloud.git
    cd lcloud
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a .env file and set up the environment variables with the following content:
    ```
    SECRET_KEY=your_secret_key
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_app_password
    STRIPE_SECRET_KEY=your_stripe_secret_key
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
    STRIPE_WEBHOOK_SECRET=your_webhook_secret
    ```
4. Run the application:
    ```bash
    python app.py
    ```
    
> This is a development template - not production-ready. Use as a starting point for building your own cloud storage application.
