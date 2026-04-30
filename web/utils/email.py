"""
Email utility functions
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template_string


def send_email(to_email, subject, html_content, text_content=None):
    """
    Send email using SMTP

    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML content
        text_content (str): Plain text content (optional)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = current_app.config['FROM_EMAIL']
        msg['To'] = to_email

        # Add plain text version
        if text_content:
            part1 = MIMEText(text_content, 'plain')
            msg.attach(part1)

        # Add HTML version
        part2 = MIMEText(html_content, 'html')
        msg.attach(part2)

        # Send via SMTP
        smtp_host = current_app.config['SMTP_HOST']
        smtp_port = current_app.config['SMTP_PORT']
        smtp_user = current_app.config['SMTP_USER']
        smtp_pass = current_app.config['SMTP_PASS']

        if not smtp_host or not smtp_user or not smtp_pass:
            print(f"⚠️ Email not configured. Would send to {to_email}: {subject}")
            return True  # Return True in development without SMTP config

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f"✓ Email sent to {to_email}: {subject}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False


def send_verification_email(user_email, user_name, verification_token):
    """
    Send email verification email

    Args:
        user_email (str): User email
        user_name (str): User full name
        verification_token (str): Verification token

    Returns:
        bool: True if sent successfully
    """
    app_url = current_app.config['APP_URL']
    verification_url = f"{app_url}/auth/verify-email?token={verification_token}"

    subject = "Verify your Zenthral account"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #007bff;">Welcome to Zenthral AI Platform!</h1>

            <p>Hi {user_name},</p>

            <p>Thank you for signing up for Zenthral. Please verify your email address by clicking the button below:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}"
                   style="background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verify Email Address
                </a>
            </div>

            <p>Or copy and paste this link into your browser:</p>
            <p style="background: #f5f5f5; padding: 10px; word-break: break-all;">{verification_url}</p>

            <p>This link will expire in 24 hours.</p>

            <p>If you didn't create an account, you can safely ignore this email.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

            <p style="font-size: 12px; color: #666;">
                Zenthral AI Platform<br>
                AI-Powered Automation for Your Business
            </p>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Welcome to Zenthral AI Platform!

    Hi {user_name},

    Thank you for signing up. Please verify your email address by visiting:
    {verification_url}

    This link will expire in 24 hours.

    If you didn't create an account, you can safely ignore this email.

    ---
    Zenthral AI Platform
    """

    return send_email(user_email, subject, html_content, text_content)


def send_password_reset_email(user_email, user_name, reset_token):
    """
    Send password reset email

    Args:
        user_email (str): User email
        user_name (str): User full name
        reset_token (str): Password reset token

    Returns:
        bool: True if sent successfully
    """
    app_url = current_app.config['APP_URL']
    reset_url = f"{app_url}/auth/reset-password?token={reset_token}"

    subject = "Reset your Zenthral password"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #007bff;">Password Reset Request</h1>

            <p>Hi {user_name},</p>

            <p>We received a request to reset your password. Click the button below to choose a new password:</p>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}"
                   style="background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Reset Password
                </a>
            </div>

            <p>Or copy and paste this link into your browser:</p>
            <p style="background: #f5f5f5; padding: 10px; word-break: break-all;">{reset_url}</p>

            <p><strong>This link will expire in 1 hour.</strong></p>

            <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

            <p style="font-size: 12px; color: #666;">
                Zenthral AI Platform<br>
                AI-Powered Automation for Your Business
            </p>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Password Reset Request

    Hi {user_name},

    We received a request to reset your password. Visit this link to choose a new password:
    {reset_url}

    This link will expire in 1 hour.

    If you didn't request a password reset, you can safely ignore this email.

    ---
    Zenthral AI Platform
    """

    return send_email(user_email, subject, html_content, text_content)


def send_welcome_email(user_email, user_name):
    """
    Send welcome email after email verification

    Args:
        user_email (str): User email
        user_name (str): User full name

    Returns:
        bool: True if sent successfully
    """
    app_url = current_app.config['APP_URL']
    dashboard_url = f"{app_url}/dashboard"

    subject = "Welcome to Zenthral - Get Started!"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #007bff;">🎉 Welcome to Zenthral!</h1>

            <p>Hi {user_name},</p>

            <p>Your email has been verified! You're all set to start automating with AI-powered agents.</p>

            <h2 style="color: #333;">Getting Started:</h2>
            <ol>
                <li><strong>Browse the Agent Marketplace</strong> - Discover 16+ pre-built automation agents</li>
                <li><strong>Install Your First Agent</strong> - One-click installation</li>
                <li><strong>Configure & Run</strong> - Add your API keys and start automating</li>
            </ol>

            <div style="text-align: center; margin: 30px 0;">
                <a href="{dashboard_url}"
                   style="background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Go to Dashboard
                </a>
            </div>

            <p>Need help? Check out our <a href="{app_url}/docs">documentation</a> or contact support.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

            <p style="font-size: 12px; color: #666;">
                Zenthral AI Platform<br>
                AI-Powered Automation for Your Business
            </p>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)
