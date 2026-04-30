#!/bin/bash

# Zenthral AI Platform - Setup Script
# This script installs dependencies and initializes the database

echo ""
echo "=========================================="
echo "  ⚡ Zenthral AI Platform - Setup"
echo "=========================================="
echo ""

# Check if we're in the web directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the web directory"
    echo "   cd web && ./setup.sh"
    exit 1
fi

# Step 1: Install Python dependencies
echo "📦 Step 1: Installing Python dependencies..."
echo ""
pip3 install --break-system-packages -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to install dependencies"
    echo "   Try: pip3 install -r requirements.txt"
    exit 1
fi

echo ""
echo "✓ Dependencies installed"
echo ""

# Step 2: Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Step 2: Creating .env file..."
    echo ""

    cat > .env << EOF
# Database (SQLite for development)
DATABASE_URL=sqlite:///zenthral.db

# Security Secrets (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
ENCRYPTION_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Email Configuration (Optional - for development, emails print to console)
# SMTP_HOST=smtp.sendgrid.net
# SMTP_PORT=587
# SMTP_USER=apikey
# SMTP_PASS=YOUR_SENDGRID_API_KEY
# FROM_EMAIL=noreply@zenthral.ai

# Gmail OAuth (from previous setup)
GMAIL_CLIENT_ID=175580175862-3au3aea8mr8nll6psp9g705bt3270dr4.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=${GMAIL_CLIENT_SECRET}

# AI Provider API Keys (Optional)
# ANTHROPIC_API_KEY=
# OPENAI_API_KEY=

# Application
APP_URL=http://localhost:5001
FLASK_ENV=development
EOF

    echo "✓ Created .env file with random secrets"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Step 3: Initialize database
echo "🗄️  Step 3: Initializing database..."
echo ""

# Create initial migration
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✓ Database tables created')
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to create database tables"
    exit 1
fi

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 To start the server:"
echo "   python3 app.py"
echo ""
echo "📍 Then visit:"
echo "   http://localhost:5001/auth/register"
echo ""
echo "💡 Next steps:"
echo "   1. Create an account"
echo "   2. Verify your email (check console if no SMTP configured)"
echo "   3. Start using Zenthral!"
echo ""
echo "=========================================="
echo ""
