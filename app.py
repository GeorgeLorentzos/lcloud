from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    send_from_directory,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
)
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

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lcloud.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USE_TLS"] = True

mail = Mail(app)
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
scheduler = BackgroundScheduler()

random_string = "qwertyuiopasdfghjklzxcvbnm-"
random_numbers = "0123456789"

server_url = "http://127.0.0.1:5000"


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@login_manager.user_loader
def load_user_by_id(user_id):
    return User.query.get(int(user_id))


storage_folder = "storage"
if not os.path.exists(storage_folder):
    os.mkdir(storage_folder)


class User(UserMixin, database.Model):
    __tablename__ = "users"
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    hashed_password = database.Column(database.String(280), nullable=False)
    folder_path = database.Column(database.String, nullable=False)
    files = database.relationship("File", backref="owner", lazy=True)
    maxstorage = database.Column(
        database.Integer, default=1024**3 * 2, nullable=False
    )
    subscription_plan = database.Column(
        database.String, default="Normal", nullable=False
    )
    subscription_expiration_date = database.Column(database.DateTime)
    subscription_id = database.Column(database.String, nullable=True)
    subscription_before = database.Column(database.Boolean, default=False)
    timezone = database.Column(database.String, nullable=False, default="UTC")
    created_at = database.Column(database.DateTime, nullable=False)
    is_email_verified = database.Column(database.Boolean, default=False)


class File(database.Model):
    __tablename__ = "files"
    id = database.Column(database.Integer, primary_key=True)
    filename = database.Column(database.String, nullable=False)
    filesize = database.Column(database.Float, nullable=False)
    upload_date = database.Column(database.DateTime, nullable=False)
    file_path = database.Column(database.String, nullable=False)
    user_id = database.Column(
        database.Integer, database.ForeignKey("users.id"), nullable=False
    )

    __table_args__ = (
        database.UniqueConstraint(
            "filename", "user_id", name="unique_filename_per_user"
        ),
    )


class Token(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    token = database.Column(database.String, nullable=True)
    token_type = database.Column(database.String, nullable=True)
    user_id = database.Column(database.Integer, nullable=False, unique=True)
    expire_at = database.Column(
        database.DateTime, default=lambda: datetime.utcnow() + relativedelta(minutes=1)
    )


class AccountForm(FlaskForm):
    username = StringField("name")
    email = EmailField("email")
    current_password = PasswordField("current password")
    new_password = PasswordField("new password")
    confirm_password = PasswordField("confirm password")
    submit = SubmitField("Update")


class RegistrationForm(FlaskForm):
    username = StringField("name", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField("name", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField()


class FileUploadForm(FlaskForm):
    file = FileField("Upload File", validators=[DataRequired()])
    submit = SubmitField()


class RenameForm(FlaskForm):
    new_filename = StringField("new name", validators=[DataRequired()])
    submit = SubmitField()


class DeleteAccountForm(FlaskForm):
    submit = SubmitField("Delete Account")


class RequestPasswordResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")


@app.route("/", methods=["GET", "POST"])
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_files = File.query.filter_by(user_id=current_user.id).all()
    total_storage = sum(f.filesize for f in user_files)
    upload_form = FileUploadForm()
    if request.method == "POST":
        if upload_form.validate_on_submit():
            uploaded_file = upload_form.file.data
            uploaded_file_size = len(uploaded_file.read())
            uploaded_file.seek(0)

            if total_storage + uploaded_file_size <= current_user.maxstorage:
                user_folder_path = os.path.join(storage_folder, current_user.username)
                clean_filename = secure_filename(uploaded_file.filename)
                saved_file_path = os.path.join(user_folder_path, clean_filename)

                if not os.path.exists(user_folder_path):
                    try:
                        os.mkdir(user_folder_path)
                    except Exception as e:
                        flash(f"Failed to create user directory: {e}", "danger")
                        return redirect("/")

                if not os.path.exists(saved_file_path):
                    try:
                        uploaded_file.save(saved_file_path)

                        timezone_str = request.form.get("timezone", "UTC")
                        try:
                            user_tz = pytz_timezone(timezone_str)
                        except:
                            user_tz = pytz.UTC

                        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
                        local_now = utc_now.astimezone(user_tz)

                        new_db_file = File(
                            filename=clean_filename,
                            filesize=os.path.getsize(saved_file_path),
                            file_path=saved_file_path,
                            user_id=current_user.id,
                            upload_date=local_now,
                        )
                        database.session.add(new_db_file)
                        database.session.commit()
                        flash("File uploaded successfully!", "success")
                        return redirect("/")
                    except Exception as e:
                        flash(f"Error saving file: {e}", "danger")
                        return redirect("/")
                else:
                    flash("File already exists", "warning")
                    return redirect("/")
            else:
                flash("Uploading this file would exceed your storage limit.", "danger")
                return redirect("/")
        else:
            flash("Invalid file upload", "warning")
            return redirect("/")

    max_user_account_storage_gb = round(current_user.maxstorage / 1024**3, 2)
    total_storage_in_mb = round(total_storage / (1024**2), 2)
    total_storage_in_gb = round(total_storage / (1024**3), 2)

    return render_template(
        "dashboard.html",
        file_upload_form=upload_form,
        files=user_files,
        total_storage=total_storage,
        max_user_account_storage_gb=max_user_account_storage_gb,
        total_storage_in_mb=total_storage_in_mb,
        total_storage_in_gb=total_storage_in_gb,
        rename_form=RenameForm(),
        stripe_publishable_key=os.getenv("STRIPE_PUBLISHABLE_KEY"),
    )


@app.route("/signup", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = str(form.username.data)
            email = form.email.data
            timezone_str = request.form.get("timezone", "UTC")

            try:
                user_tz = pytz_timezone(timezone_str)
            except:
                user_tz = pytz.UTC

            utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            local_now = utc_now.astimezone(user_tz)

            created_at = local_now

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Name already exists", "warning")
                return redirect("/signup")
            elif existing_email:
                flash("This email is already registered", "warning")
                return redirect("/signup")
            else:
                try:
                    user_folder_path = os.path.join(storage_folder, username)
                    if not os.path.exists(user_folder_path):
                        os.mkdir(user_folder_path)

                    new_user = User(
                        username=username,
                        email=email,
                        hashed_password=hashed_password,
                        folder_path=user_folder_path,
                        created_at=created_at,
                        timezone=timezone_str,
                        is_email_verified=False,
                    )

                    database.session.add(new_user)
                    database.session.flush()

                    token = "".join(
                        random.choices(random_string + random_numbers, k=50)
                    )
                    verification_link = server_url + "/verify/" + token

                    new_token = Token(
                        token=token,
                        token_type="Account-Verify",
                        user_id=new_user.id,
                    )

                    database.session.add(new_token)
                    database.session.flush()

                    try:
                        html = render_template(
                            "verify.html",
                            link=verification_link,
                            title="Account Verify",
                            button_text="Verify Account",
                            username=new_user.username,
                            description="We have received a request to verify your account. To complete the verification, please click the button below.",
                        )
                        msg = Message(
                            subject="Verify Account",
                            sender=app.config["MAIL_USERNAME"],
                            recipients=[new_user.email],
                            html=html,
                        )
                        mail.send(msg)
                    except Exception as e:
                        print(f"Failed to send verification email: {e}")

                    database.session.commit()

                    return render_template(
                        "alert.html",
                        title="Registration Successful",
                        username=new_user.username,
                        email=new_user.email,
                        description=f"We have sent you a verification link to the email {new_user.email}.",
                    )

                except Exception as e:
                    flash(f"Error during registration: {e}", "danger")
                    return redirect("/signup")
    return render_template("signup.html", form=form)


@app.route("/verify/<token>", methods=["GET", "POST"])
def verify(token):
    token = Token.query.filter_by(token=token).first()
    if not token:
        return redirect("/signin")

    user = User.query.filter_by(id=token.user_id).first()
    if not user:
        return redirect("/signin")

    if token.token_type == "Account-Verify":
        user.is_email_verified = True
        database.session.delete(token)
        database.session.commit()
        return redirect("/signin")

    elif token.token_type == "Password-Reset":
        form = ResetPasswordForm()
        if request.method == "POST" and form.validate_on_submit():
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data
            if new_password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(new_password).decode(
                    "utf-8"
                )
                user.hashed_password = hashed_password
                database.session.delete(token)
                database.session.commit()
                return redirect("/signin")
            else:
                flash("Passwords do not match. Please try again.", "info")
        return render_template("reset-password.html", form=form, token=token)

    return redirect("/signin")


@app.route("/signin", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if not user:
                flash("User does not exist.", "warning")
                return redirect("/signin")
            elif not user.is_email_verified:
                flash("Please verify your account first.", "warning")
                return redirect("/signin")
            elif (
                bcrypt.check_password_hash(user.hashed_password, password)
                and user.is_email_verified
            ):
                login_user(user)
                return redirect("/")
            else:
                flash("Incorrect password. Please try again.", "danger")
                return redirect("/signin")
        else:
            flash("Please fill out the form correctly.", "warning")
            return redirect("/signin")
    return render_template("signin.html", form=form)


@app.route("/delete/<string:filename>", methods=["POST"])
@login_required
def delete_file(filename):
    file_to_delete = File.query.filter_by(
        filename=filename, user_id=current_user.id
    ).first()
    if file_to_delete:
        try:
            database.session.delete(file_to_delete)
            database.session.commit()

            if os.path.exists(file_to_delete.file_path):
                os.remove(file_to_delete.file_path)

            flash("File deleted successfully.", "success")
        except Exception as e:
            database.session.rollback()
            flash(f"Failed to delete file: {e}", "danger")
    else:
        flash("File not found.", "warning")
    return redirect("/")


@app.route("/rename", methods=["GET", "POST"])
@login_required
def rename_file():
    rename_form = RenameForm()
    if request.method == "POST":
        if rename_form.validate_on_submit():
            old_filename = request.form.get("filename")
            new_filename = secure_filename(rename_form.new_filename.data)
            file_to_rename = File.query.filter_by(
                filename=old_filename, user_id=current_user.id
            ).first()
            if not new_filename or new_filename.startswith("."):
                flash("Invalid new filename.", "warning")
                return redirect("/")

            if file_to_rename:
                if new_filename == old_filename:
                    flash("The new filename is the same as the old filename.", "info")
                    return redirect("/")
                old_file_path = file_to_rename.file_path
                user_folder_path = os.path.dirname(old_file_path)
                new_file_path = os.path.join(user_folder_path, new_filename)
                if not os.path.exists(new_file_path):
                    try:
                        os.rename(old_file_path, new_file_path)
                        file_to_rename.filename = new_filename
                        file_to_rename.file_path = new_file_path
                        database.session.commit()
                        flash("File renamed successfully.", "success")
                        return redirect("/")
                    except Exception as e:
                        flash(f"Failed to rename file: {e}", "danger")
                        return redirect("/")
                else:
                    flash("A file with the new name already exists.", "warning")
                    return redirect("/")
            else:
                flash("File not found.", "warning")
                return redirect("/")
        else:
            flash("Invalid rename form submission.", "warning")
            return redirect("/")
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user_files = File.query.filter_by(user_id=current_user.id).all()
    total_storage = sum(f.filesize for f in user_files)
    max_user_account_storage_gb = round(current_user.maxstorage / 1024**3, 2)
    total_storage_in_mb = round(total_storage / (1024**2), 2)
    total_storage_in_gb = round(total_storage / (1024**3), 2)
    account_form = AccountForm()
    delete_account_form = DeleteAccountForm()
    if request.method == "POST":
        if account_form.validate_on_submit():
            new_username = account_form.username.data
            new_email = account_form.email.data
            current_password = account_form.current_password.data
            new_password = account_form.new_password.data
            confirm_password = account_form.confirm_password.data
            old_username = current_user.username
            old_folder_path = os.path.join(storage_folder, old_username)
            new_folder_path = os.path.join(storage_folder, new_username)
            if new_username and new_username != current_user.username:
                if os.path.exists(old_folder_path):
                    try:
                        os.rename(old_folder_path, new_folder_path)
                    except Exception as e:
                        flash(f"Failed to rename user folder: {e}", "danger")
                        return redirect("/account")

                user_files = File.query.filter_by(user_id=current_user.id).all()
                for user_file in user_files:
                    user_file.file_path = user_file.file_path.replace(
                        old_folder_path, new_folder_path
                    )
            current_user.folder_path = new_folder_path
            current_user.username = new_username
            if new_email and new_email != current_user.email:
                current_user.email = new_email

            if new_password or confirm_password:
                if not bcrypt.check_password_hash(
                    current_user.hashed_password, current_password
                ):
                    flash("Your current password is wrong!", "danger")
                    return redirect("/account")
                if new_password != confirm_password:
                    flash("Passwords do not match.", "danger")
                    return redirect("/account")
                hashed_new_password = bcrypt.generate_password_hash(
                    new_password
                ).decode("utf-8")
                current_user.hashed_password = hashed_new_password
            try:
                database.session.commit()
                flash("Account updated successfully!", "success")
                return redirect("/account")
            except Exception as e:
                flash(f"Failed to update account: {e}", "danger")
                return redirect("/account")
        else:
            flash("Please fill out the form correctly.", "warning")
            return redirect("/account")
    account_form.username.data = current_user.username
    account_form.email.data = current_user.email
    return render_template(
        "account.html",
        account_form=account_form,
        delete_account_form=delete_account_form,
        total_storage=total_storage,
        total_storage_in_mb=total_storage_in_mb,
        total_storage_in_gb=total_storage_in_gb,
        stripe_publishable_key=os.getenv("STRIPE_PUBLISHABLE_KEY"),
    )


@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    delete_account_btn = DeleteAccountForm()
    if request.method == "POST" and delete_account_btn.validate_on_submit():
        user_to_delete = User.query.filter_by(username=current_user.username).first()
        user_files = File.query.filter_by(user_id=current_user.id)
        if user_to_delete:
            try:
                shutil.rmtree(user_to_delete.folder_path)
            except Exception as e:
                flash(f"Failed to remove user folder: {e}", "danger")
                return redirect("/account")
            try:
                for file_item in user_files:
                    database.session.delete(file_item)
                database.session.delete(user_to_delete)
                database.session.commit()
                flash("Account and files deleted successfully.", "success")
            except Exception as e:
                flash(f"Failed to delete user data: {e}", "danger")
                return redirect("/account")
        else:
            flash("User not found.", "warning")
            return redirect("/account")
        logout_user()
        return redirect("/signin")
    else:
        flash("Please confirm account deletion.", "warning")
        return redirect("/account")


def get_or_create_premium_price():
    product = stripe.Product.create(name="Premium")
    price = stripe.Price.create(
        unit_amount=2000,
        currency="usd",
        recurring={"interval": "month"},
        product=product.id,
    )
    return price.id


@app.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    price_id = get_or_create_premium_price()

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:5000/",
        cancel_url="http://127.0.0.1:5000/",
        payment_method_types=["card"],
        mode="subscription",
        customer_email=current_user.email,
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
    )
    return jsonify({"sessionId": session.id})


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    event = None
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        subscription_id = session.get("subscription")

        user = User.query.filter_by(email=customer_email).first()
        if user:
            try:
                user_tz = pytz_timezone(user.timezone)
            except Exception:
                user_tz = "UTC"

        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        if user:
            user.maxstorage = 1024**3 * 10
            user.subscription_plan = "Premium"
            user.subscription_before = True
            user.subscription_id = subscription_id
            user.subscription_expiration_date = utc_now.astimezone(
                user_tz
            ) + datetime.timedelta(days=30)
            database.session.commit()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        stripe_sub_id = subscription["id"]

        user = User.query.filter_by(subscription_id=stripe_sub_id).first()
        if user:
            user.subscription_plan = "Normal"
            user.maxstorage = 1024**3 * 2
            user.subscription_expiration_date = None
            user.subscription_id = None
            database.session.commit()

    return "", 200


@app.route("/create-billing-portal-session", methods=["POST"])
@login_required
def create_billing_portal_session():
    if not current_user.email:
        return jsonify({"error": "No email associated with account"}), 400

    try:
        customers = stripe.Customer.list(email=current_user.email)

        if len(customers.data) == 0:
            return jsonify({"error": "No subscription found"}), 400

        customer_id = customers.data[0].id

        session = stripe.billing_portal.Session.create(
            customer=customer_id, return_url=url_for("account", _external=True)
        )

        return jsonify({"url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/request-password-reset", methods=["GET", "POST"])
def request_password_reset():
    form = RequestPasswordResetForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User doesn't exist.", "warning")
            return redirect(request.referrer or "/request-password-reset")

        token = "".join(random.choices(random_string + random_numbers, k=50))
        reset_link = server_url + "/verify/" + token

        existing_token = Token.query.filter_by(user_id=user.id).first()
        if existing_token:
            existing_token.token = token
            existing_token.token_type = "Password-Reset"
            database.session.commit()
        else:
            new_token = Token(
                user_id=user.id,
                token=token,
                token_type="Password-Reset",
            )
            database.session.add(new_token)
            database.session.commit()

        try:
            html = render_template(
                "verify.html",
                link=reset_link,
                title="Password Reset Request",
                username=user.username,
                button_text="Reset Password",
                description="We've received a request to reset the password for your account. To proceed, please click the button below.",
            )
            msg = Message(
                subject="Reset Password Request",
                recipients=[user.email],
                sender=app.config["MAIL_USERNAME"],
                html=html,
            )
            mail.send(msg)
            flash(
                f"We have sent a password reset link to the email {user.email}", "info"
            )
        except Exception as e:
            print(f"Error sending email: {e}")

    return render_template("request-password-reset.html", form=form)


def periodically_cleanup_expired_tokens():
    while True:
        time.sleep(600)
        tokens = Token.query.all()
        for token in tokens:
            if datetime.utcnow() > token.expire_at:
                database.session.delete(token)
        database.session.commit()


scheduler.add_job(periodically_cleanup_expired_tokens, "interval", minutes=10)
scheduler.start()

if __name__ == "__main__":
    with app.app_context():
        database.create_all()
    app.run(debug=True)
    