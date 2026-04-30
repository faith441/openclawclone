#!/usr/bin/env python3
"""
Zenthral AI Platform - Web Dashboard
Full-featured SaaS with authentication, database, and AI automation
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# Load environment variables
load_dotenv()

# Import new modules
try:
    from config import get_config
    from models import db
    from api import api as api_blueprint
    HAS_NEW_MODULES = True
except ImportError as e:
    print(f"⚠️  Warning: Could not import new modules: {e}")
    print("    Running in legacy mode without authentication")
    HAS_NEW_MODULES = False
    # Create minimal Flask app for legacy mode
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    db = None

# Initialize Flask app
if HAS_NEW_MODULES:
    app = Flask(__name__)
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    # Initialize database
    db.init_app(app)
else:
    # Already initialized in legacy mode above
    pass

# Gmail OAuth Configuration
GMAIL_CLIENT_ID = os.environ.get('GMAIL_CLIENT_ID', '175580175862-3au3aea8mr8nll6psp9g705bt3270dr4.apps.googleusercontent.com')
GMAIL_CLIENT_SECRET = os.environ.get('GMAIL_CLIENT_SECRET', '')  # Add your client secret
GMAIL_REDIRECT_URI = 'http://localhost:5001/auth/gmail/callback'
GMAIL_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow HTTP for localhost development

# Try to import AI libraries
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# AI Providers and Models
AI_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "models": [
            {"id": "gpt-4o", "name": "GPT-4o", "new": True, "input_price": 2.50, "output_price": 10.00},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "input_price": 10.00, "output_price": 30.00},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "input_price": 0.50, "output_price": 1.50},
        ]
    },
    "anthropic": {
        "name": "Anthropic",
        "recommended": True,
        "models": [
            {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4", "new": True, "input_price": 3.00, "output_price": 15.00},
            {"id": "claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "input_price": 3.00, "output_price": 15.00},
            {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "input_price": 0.25, "output_price": 1.25},
        ]
    },
    "google": {
        "name": "Google",
        "models": [
            {"id": "gemini-pro", "name": "Gemini Pro", "input_price": 0.50, "output_price": 1.50},
            {"id": "gemini-ultra", "name": "Gemini Ultra", "new": True, "input_price": 5.00, "output_price": 15.00},
        ]
    }
}

# Available Skills/Agents
SKILLS = [
    {"id": "finance", "name": "Finance Agent", "icon": "💰", "description": "Invoice generation, Stripe payments", "category": "industry"},
    {"id": "real-estate", "name": "Real Estate Agent", "icon": "🏠", "description": "AI property listings", "category": "industry"},
    {"id": "ecommerce", "name": "E-commerce Agent", "icon": "🛒", "description": "Shopify order processing", "category": "industry"},
    {"id": "legal", "name": "Legal Agent", "icon": "⚖️", "description": "Contract review", "category": "industry"},
    {"id": "hospitality", "name": "Hospitality Agent", "icon": "🏨", "description": "Reservations management", "category": "industry"},
    {"id": "construction", "name": "Construction Agent", "icon": "🏗️", "description": "Project bidding", "category": "industry"},
    {"id": "marketing", "name": "Marketing Agent", "icon": "📊", "description": "Campaign management", "category": "industry"},
    {"id": "email", "name": "Email Automation", "icon": "📧", "description": "SMTP email sending", "category": "automation"},
    {"id": "sms", "name": "SMS Sender", "icon": "📱", "description": "Twilio text messages", "category": "automation"},
    {"id": "pdf", "name": "PDF Generator", "icon": "📄", "description": "Create PDFs", "category": "automation"},
    {"id": "web-scraper", "name": "Web Scraper", "icon": "🌐", "description": "Extract web content", "category": "automation"},
    {"id": "data-converter", "name": "Data Converter", "icon": "🔄", "description": "Convert CSV/JSON/XML", "category": "automation"},
    {"id": "image-optimizer", "name": "Image Optimizer", "icon": "🖼️", "description": "Resize & compress", "category": "automation"},
    {"id": "slack", "name": "Slack Notifier", "icon": "💬", "description": "Send Slack messages", "category": "automation"},
]

# Register API blueprint (only if new modules loaded)
if HAS_NEW_MODULES:
    app.register_blueprint(api_blueprint)

# ============================================
# AUTHENTICATION ROUTES (UI Pages)
# ============================================

if HAS_NEW_MODULES:
    @app.route('/auth/login')
    def auth_login():
        """Login page"""
        return render_template('auth/login.html')

    @app.route('/auth/register')
    def auth_register():
        """Registration page"""
        return render_template('auth/register.html')

    @app.route('/auth/verify-email')
    def auth_verify_email():
        """Email verification page"""
        return render_template('auth/verify_email.html')

    # Marketplace routes
    @app.route('/marketplace/browse')
    def marketplace_browse():
        """Agent marketplace browse page"""
        return render_template('marketplace/browse.html')

    @app.route('/marketplace/my-agents')
    def marketplace_my_agents():
        """User's installed agents page"""
        return render_template('marketplace/my_agents.html')

# ============================================
# MAIN ROUTES
# ============================================

@app.route('/')
def index():
    if HAS_NEW_MODULES:
        return redirect(url_for('auth_login'))  # Redirect to login for new auth system
    else:
        return redirect(url_for('dashboard'))  # Redirect to dashboard for legacy mode

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                         providers=AI_PROVIDERS,
                         skills=SKILLS)

@app.route('/chat')
def chat():
    return render_template('chat.html',
                         providers=AI_PROVIDERS)

@app.route('/skills')
def skills():
    return render_template('skills.html',
                         skills=SKILLS)

@app.route('/integration')
def integration():
    return render_template('integration.html')

@app.route('/usage')
def usage():
    return render_template('usage.html')

@app.route('/ai-models')
def ai_models():
    return render_template('ai_models.html',
                         providers=AI_PROVIDERS)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/create-automation')
def create_automation():
    return render_template('create_automation.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/channels')
def channels():
    return render_template('channels.html')

@app.route('/instances')
def instances():
    return render_template('instances.html')

@app.route('/sessions')
def sessions():
    return render_template('sessions.html')

@app.route('/cron')
def cron():
    return render_template('cron.html')

@app.route('/agents')
def agents():
    return render_template('agents.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

# API Endpoints
@app.route('/api/set-provider', methods=['POST'])
def set_provider():
    data = request.json
    session['provider'] = data.get('provider')
    session['model'] = data.get('model')
    return jsonify({"status": "success", "provider": session['provider'], "model": session['model']})

@app.route('/api/set-api-key', methods=['POST'])
def set_api_key():
    data = request.json
    provider = data.get('provider')
    api_key = data.get('api_key')

    # Store in session (in production, use secure storage)
    if 'api_keys' not in session:
        session['api_keys'] = {}
    session['api_keys'][provider] = api_key

    return jsonify({"status": "success", "provider": provider})

@app.route('/api/run-skill', methods=['POST'])
def run_skill():
    data = request.json
    skill_id = data.get('skill')
    params = data.get('params', {})

    # This would execute the actual agent
    return jsonify({
        "status": "success",
        "skill": skill_id,
        "result": f"Executed {skill_id} with params: {params}"
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    message = data.get('message')
    provider = session.get('provider', 'anthropic')
    model = session.get('model', 'claude-sonnet-4-20250514')

    # Get API key from session or environment
    api_keys = session.get('api_keys', {})

    try:
        if provider == 'anthropic':
            api_key = api_keys.get('anthropic') or os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                return jsonify({
                    "status": "error",
                    "response": "Please set your Anthropic API key in Integration settings or ANTHROPIC_API_KEY environment variable."
                })

            if ANTHROPIC_AVAILABLE:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model=model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": message}]
                )
                response_text = response.content[0].text
                tokens = {"input": response.usage.input_tokens, "output": response.usage.output_tokens}
            else:
                return jsonify({"status": "error", "response": "Anthropic library not installed. Run: pip install anthropic"})

        elif provider == 'openai':
            api_key = api_keys.get('openai') or os.environ.get('OPENAI_API_KEY')
            if not api_key:
                return jsonify({
                    "status": "error",
                    "response": "Please set your OpenAI API key in Integration settings or OPENAI_API_KEY environment variable."
                })

            if OPENAI_AVAILABLE:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    max_tokens=1024
                )
                response_text = response.choices[0].message.content
                tokens = {"input": response.usage.prompt_tokens, "output": response.usage.completion_tokens}
            else:
                return jsonify({"status": "error", "response": "OpenAI library not installed. Run: pip install openai"})

        elif provider == 'google':
            # Google Gemini would require google-generativeai library
            return jsonify({
                "status": "error",
                "response": "Google Gemini integration coming soon. Please use Anthropic or OpenAI for now."
            })
        else:
            return jsonify({"status": "error", "response": f"Unknown provider: {provider}"})

        # Track usage
        if 'usage' not in session:
            session['usage'] = {"total_input": 0, "total_output": 0, "requests": 0}
        session['usage']['total_input'] += tokens.get('input', 0)
        session['usage']['total_output'] += tokens.get('output', 0)
        session['usage']['requests'] += 1
        session.modified = True

        return jsonify({
            "status": "success",
            "response": response_text,
            "tokens": tokens,
            "model": model
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "response": f"Error calling {provider} API: {str(e)}"
        })

@app.route('/api/usage')
def api_usage():
    """Get usage statistics"""
    usage = session.get('usage', {"total_input": 0, "total_output": 0, "requests": 0})
    return jsonify({
        "status": "success",
        "usage": usage
    })

@app.route('/api/current-model')
def api_current_model():
    """Get current selected provider and model"""
    return jsonify({
        "status": "success",
        "provider": session.get('provider', 'anthropic'),
        "model": session.get('model', 'claude-sonnet-4-20250514')
    })

@app.route('/api/check-keys')
def api_check_keys():
    """Check which API keys are configured"""
    api_keys = session.get('api_keys', {})
    configured = {}
    for provider in ['anthropic', 'openai', 'google']:
        has_session_key = bool(api_keys.get(provider))
        has_env_key = bool(os.environ.get(f'{provider.upper()}_API_KEY'))
        configured[provider] = has_session_key or has_env_key
    return jsonify({
        "status": "success",
        "configured": configured
    })

# Gmail OAuth Routes
@app.route('/gmail')
def gmail():
    """Gmail management page"""
    gmail_connected = 'gmail_credentials' in session
    gmail_email = session.get('gmail_email', None)
    return render_template('gmail.html',
                         gmail_connected=gmail_connected,
                         gmail_email=gmail_email)

@app.route('/auth/gmail')
def auth_gmail():
    """Start Gmail OAuth flow"""
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GMAIL_CLIENT_ID,
                    "client_secret": GMAIL_CLIENT_SECRET,
                    "redirect_uris": [GMAIL_REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=GMAIL_SCOPES,
            redirect_uri=GMAIL_REDIRECT_URI
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true'
        )

        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        return jsonify({"status": "error", "message": f"OAuth setup failed: {str(e)}"}), 500

@app.route('/auth/gmail/callback')
def auth_gmail_callback():
    """Handle Gmail OAuth callback"""
    try:
        state = session.get('oauth_state')

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GMAIL_CLIENT_ID,
                    "client_secret": GMAIL_CLIENT_SECRET,
                    "redirect_uris": [GMAIL_REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=GMAIL_SCOPES,
            state=state,
            redirect_uri=GMAIL_REDIRECT_URI
        )

        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        # Get user's email address
        gmail_service = build('gmail', 'v1', credentials=credentials)
        profile = gmail_service.users().getProfile(userId='me').execute()
        email_address = profile.get('emailAddress')

        # Store credentials in session (in production, use database)
        session['gmail_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        session['gmail_email'] = email_address
        session.modified = True

        return redirect(url_for('gmail'))
    except Exception as e:
        return jsonify({"status": "error", "message": f"OAuth callback failed: {str(e)}"}), 500

@app.route('/api/send-email', methods=['POST'])
def api_send_email():
    """Send email using authenticated Gmail account"""
    try:
        if 'gmail_credentials' not in session:
            return jsonify({"status": "error", "message": "Gmail not connected. Please authenticate first."}), 401

        data = request.json
        to_email = data.get('to')
        subject = data.get('subject')
        body = data.get('body')

        if not all([to_email, subject, body]):
            return jsonify({"status": "error", "message": "Missing required fields: to, subject, body"}), 400

        # Reconstruct credentials from session
        creds_data = session['gmail_credentials']
        credentials = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )

        # Build Gmail service
        gmail_service = build('gmail', 'v1', credentials=credentials)

        # Create message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        message['from'] = session.get('gmail_email', 'me')

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Send email
        send_result = gmail_service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return jsonify({
            "status": "success",
            "message": "Email sent successfully",
            "message_id": send_result.get('id')
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }), 500

@app.route('/api/gmail-disconnect', methods=['POST'])
def api_gmail_disconnect():
    """Disconnect Gmail account"""
    if 'gmail_credentials' in session:
        del session['gmail_credentials']
    if 'gmail_email' in session:
        del session['gmail_email']
    session.modified = True
    return jsonify({"status": "success", "message": "Gmail disconnected"})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  ⚡ Zenthral AI Platform - SaaS Edition")
    print("="*60)
    print("\n  🚀 Starting web dashboard...")
    print("  📍 URL: http://localhost:5001")
    print("\n  🔐 Authentication:")
    print("     - Register: http://localhost:5001/auth/register")
    print("     - Login:    http://localhost:5001/auth/login")
    print("\n  📚 API Documentation:")
    print("     - Auth API: http://localhost:5001/api/v1/auth/*")
    print("\n  💡 Tips:")
    print("     - First time? Create an account at /auth/register")
    print("     - API keys: Configure in Integration settings")
    print("     - Database: Using", app.config['SQLALCHEMY_DATABASE_URI'])
    print("\n" + "="*60 + "\n")

    # Create database tables if they don't exist
    if HAS_NEW_MODULES:
        with app.app_context():
            db.create_all()
            print("  ✓ Database initialized")
            print("\n" + "="*60 + "\n")
    else:
        print("  ⚠️  Running in legacy mode (no database)")
        print("\n" + "="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
