# LCloud
- A robust Python Flask web application for secure cloud storage and file management.

## Features
- Multi-user cloud storage platform with secure authentication
- File upload and storage with intelligent size management
- Premium subscription tiers with expanded storage capacity
- Secure user data isolation and folder management
- Email verification and password recovery system
- Stripe payment integration for subscription management
- Real-time storage usage tracking and quotas
- Cross-timezone file management support
- Modern responsive web interface

## Supported File Types
- **Images:** `.jpg`, `.png`, `.gif`, `.svg`, etc.
- **Documents:** `.pdf`, `.docx`, `.txt`, `.xlsx`, etc.
- **Videos:** `.mp4`, `.mkv`, `.avi`, etc.
- **Audio:** `.mp3`, `.wav`, `.flac`, etc.
- **Archives:** `.zip`, `.rar`, `.7z`, etc.
- **Scripts:** `.py`, `.js`, `.sh`, `.java`, etc.
- **Others:** `.exe`, `.apk`, `.log`, `.tmp`, etc.

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
3. Set up environment variables in `.env` file:
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
