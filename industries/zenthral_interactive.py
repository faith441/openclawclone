#!/usr/bin/env python3
"""
Zenthral Interactive Chat - Connects to Real Services

This version:
- Asks users for requirements interactively
- Connects to real APIs and services
- Performs actual operations (not mock data)
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class InteractiveChat:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.check_environment()

    def check_environment(self):
        """Check for API keys and services."""
        # For testing, use Claude API (Anthropic)
        self.has_claude = bool(os.environ.get('ANTHROPIC_API_KEY'))
        self.has_openai = bool(os.environ.get('OPENAI_API_KEY'))
        self.has_ai = self.has_claude or self.has_openai
        self.has_stripe = bool(os.environ.get('STRIPE_API_KEY'))
        self.has_quickbooks = bool(os.environ.get('QUICKBOOKS_CLIENT_ID'))
        self.has_zillow = bool(os.environ.get('ZILLOW_API_KEY'))

    def print_header(self):
        """Print welcome header."""
        print("\n" + "=" * 70)
        print("  🤖 Zenthral Interactive AI Agents")
        print("  Connect to Real Services & Automate Your Business")
        print("=" * 70)
        print("\nIndustry Agents:")
        print("  💰 Finance - Invoice generation, Stripe payments")
        print("  🏠 Real Estate - AI property listings, Claude-powered")
        print("  🛒 E-commerce - Shopify order processing")
        print("  ⚖️ Legal - Contract review, document automation")
        print("  🏨 Hospitality - Reservations, guest management")
        print("  🏗️ Construction - Project bidding, scheduling")
        print("  📊 Marketing - Campaign management, analytics")
        print("\nAutomation Agents (Easy Setup!):")
        print("  📧 Email - SMTP email automation")
        print("  📱 SMS - Twilio text messages")
        print("  📄 PDF - Generate PDFs from text/CSV")
        print("  🌐 Web Scraper - Extract text, links, images")
        print("  🔄 Data Converter - CSV/JSON/XML/Excel")
        print("  🖼️  Image Optimizer - Resize, compress, convert")
        print("  💬 Slack Notifier - Send Slack messages")
        print("\n" + "=" * 70)

    def setup_wizard(self, agent_type: str):
        """Interactive setup for each agent."""
        print(f"\n🔧 Setting up {agent_type} Agent")
        print("=" * 50)

        if agent_type == "finance":
            return self.setup_finance()
        elif agent_type == "real-estate":
            return self.setup_real_estate()
        elif agent_type == "ecommerce":
            return self.setup_ecommerce()
        elif agent_type == "legal":
            return self.setup_legal()
        elif agent_type == "hospitality":
            return self.setup_hospitality()
        elif agent_type == "construction":
            return self.setup_construction()
        elif agent_type == "marketing":
            return self.setup_marketing()
        elif agent_type == "email":
            return self.setup_email()
        elif agent_type == "sms":
            return self.setup_sms()
        elif agent_type == "pdf":
            return self.setup_pdf()
        elif agent_type == "web-scraper":
            return self.setup_web_scraper()
        elif agent_type == "data-converter":
            return self.setup_data_converter()
        elif agent_type == "image-optimizer":
            return self.setup_image_optimizer()
        elif agent_type == "slack":
            return self.setup_slack()

    def setup_finance(self):
        """Setup finance agent with real connections."""
        print("\n📋 Let's create an invoice")
        print("-" * 50)

        config = {}

        # Client info
        print("\n👤 CLIENT INFORMATION:")
        config['client_name'] = input("  Client/Company name: ").strip() or "Acme Corp"
        config['client_email'] = input("  Client email: ").strip() or "billing@example.com"

        # Invoice details
        print("\n💼 INVOICE DETAILS:")
        config['description'] = input("  Service description: ").strip() or "Consulting Services"

        hours = input("  Hours worked (default: 40): ").strip()
        config['hours'] = float(hours) if hours else 40.0

        rate = input("  Hourly rate (default: $150): ").strip()
        config['rate'] = float(rate) if rate else 150.0

        # Payment terms
        print("\n💳 PAYMENT TERMS:")
        print("  1. NET30 (due in 30 days)")
        print("  2. NET15 (due in 15 days)")
        print("  3. Due on receipt")
        terms_choice = input("  Choose (1-3, default: 1): ").strip()
        terms_map = {"1": "NET30", "2": "NET15", "3": "DUE_ON_RECEIPT"}
        config['terms'] = terms_map.get(terms_choice, "NET30")

        # Integration options
        print("\n🔗 INTEGRATIONS:")

        # Stripe setup
        if self.has_stripe:
            send_stripe = input("  Send Stripe payment link? (y/n, default: y): ").strip().lower()
            config['send_stripe_link'] = send_stripe != 'n'
            config['stripe_api_key'] = None  # Already set in environment
        else:
            print("  ⚠️  Stripe not configured")
            setup_stripe = input("  Would you like to set up Stripe now? (y/n): ").strip().lower()
            if setup_stripe == 'y':
                print("\n  📝 Get your Stripe API key:")
                print("     1. Go to https://dashboard.stripe.com/apikeys")
                print("     2. Copy your 'Secret key' (starts with sk_test_ or sk_live_)")
                stripe_key = input("\n  Paste your Stripe API key (or press Enter to skip): ").strip()
                if stripe_key:
                    config['stripe_api_key'] = stripe_key
                    config['send_stripe_link'] = True
                    print("  ✅ Stripe configured for this session!")
                else:
                    config['send_stripe_link'] = False
                    config['stripe_api_key'] = None
            else:
                config['send_stripe_link'] = False
                config['stripe_api_key'] = None

        # QuickBooks setup
        if self.has_quickbooks:
            sync_qb = input("  Sync to QuickBooks? (y/n, default: y): ").strip().lower()
            config['sync_quickbooks'] = sync_qb != 'n'
            config['quickbooks_client_id'] = None
        else:
            print("  ⚠️  QuickBooks not configured (coming soon)")
            config['sync_quickbooks'] = False
            config['quickbooks_client_id'] = None

        # Email options
        print("\n📧 EMAIL OPTIONS:")
        if self.has_email:
            send_email = input("  Send invoice via email? (y/n, default: y): ").strip().lower()
            config['send_email'] = send_email != 'n'
            config['smtp_config'] = None  # Already set in environment
        else:
            print("  ⚠️  Email (SMTP) not configured")
            setup_email = input("  Would you like to set up email now? (y/n): ").strip().lower()
            if setup_email == 'y':
                print("\n  📝 Enter your SMTP settings:")
                print("     For Gmail: smtp.gmail.com, port 587")
                print("     Get app password: https://myaccount.google.com/apppasswords")

                smtp_config = {}
                smtp_config['host'] = input("\n  SMTP Host (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
                smtp_config['port'] = input("  SMTP Port (default: 587): ").strip() or "587"
                smtp_config['user'] = input("  Email address: ").strip()
                smtp_config['password'] = input("  Password/App Password: ").strip()

                if smtp_config['user'] and smtp_config['password']:
                    config['smtp_config'] = smtp_config
                    config['send_email'] = True
                    print("  ✅ Email configured for this session!")
                else:
                    config['send_email'] = False
                    config['smtp_config'] = None
            else:
                config['send_email'] = False
                config['smtp_config'] = None

        return config

    def setup_real_estate(self):
        """Setup real estate agent."""
        print("\n🏠 Let's create a property listing")
        print("-" * 50)

        config = {}

        # Property info
        print("\n🏘️  PROPERTY INFORMATION:")
        config['address'] = input("  Property address: ").strip() or "123 Main St, San Francisco, CA 94102"

        price = input("  Listing price: $").strip()
        config['price'] = int(price) if price else 1250000

        beds = input("  Bedrooms (default: 3): ").strip()
        config['bedrooms'] = int(beds) if beds else 3

        baths = input("  Bathrooms (default: 2): ").strip()
        config['bathrooms'] = float(baths) if baths else 2.0

        sqft = input("  Square footage (default: 1800): ").strip()
        config['sqft'] = int(sqft) if sqft else 1800

        # Features
        print("\n✨ PROPERTY FEATURES:")
        features_input = input("  Features (comma-separated): ").strip()
        if features_input:
            config['features'] = [f.strip() for f in features_input.split(',')]
        else:
            config['features'] = ["hardwood floors", "updated kitchen", "backyard"]

        # Distribution
        print("\n📤 DISTRIBUTION:")
        print("  Where should we publish this listing?")
        config['publish_zillow'] = input("    Zillow? (y/n, default: y): ").strip().lower() != 'n'
        config['publish_realtor'] = input("    Realtor.com? (y/n, default: y): ").strip().lower() != 'n'
        config['publish_mls'] = input("    MLS? (y/n, default: y): ").strip().lower() != 'n'

        # AI description
        if self.has_ai:
            ai_provider = "Claude" if self.has_claude else "OpenAI"
            gen_desc = input(f"\n🤖 Generate AI description using {ai_provider}? (y/n, default: y): ").strip().lower()
            config['ai_description'] = gen_desc != 'n'
            config['ai_api_key'] = None  # Already set in environment
        else:
            print("\n⚠️  AI not configured")
            setup_ai = input("  Would you like to set up AI now? (y/n): ").strip().lower()
            if setup_ai == 'y':
                print("\n  Choose AI provider:")
                print("    1. Claude (Anthropic) - Recommended")
                print("    2. OpenAI (ChatGPT)")
                provider_choice = input("  Choose (1-2, default: 1): ").strip()

                if provider_choice == "2":
                    print("\n  📝 Get your OpenAI API key:")
                    print("     1. Go to https://platform.openai.com/api-keys")
                    print("     2. Create new secret key")
                    api_key = input("\n  Paste your OpenAI API key (or press Enter to skip): ").strip()
                    if api_key:
                        config['ai_api_key'] = api_key
                        config['ai_provider'] = 'openai'
                        config['ai_description'] = True
                        print("  ✅ OpenAI configured for this session!")
                    else:
                        config['ai_description'] = False
                        config['ai_api_key'] = None
                else:
                    print("\n  📝 Get your Claude API key:")
                    print("     1. Go to https://console.anthropic.com/")
                    print("     2. Create API key")
                    api_key = input("\n  Paste your Claude API key (or press Enter to skip): ").strip()
                    if api_key:
                        config['ai_api_key'] = api_key
                        config['ai_provider'] = 'claude'
                        config['ai_description'] = True
                        print("  ✅ Claude configured for this session!")
                    else:
                        config['ai_description'] = False
                        config['ai_api_key'] = None
            else:
                config['ai_description'] = False
                config['ai_api_key'] = None

        return config

    def setup_ecommerce(self):
        """Setup e-commerce agent."""
        print("\n🛒 Let's process orders")
        print("-" * 50)

        config = {}

        print("\n📦 ORDER PROCESSING:")
        count = input("  How many orders to process? (default: all pending): ").strip()
        config['order_count'] = int(count) if count else None

        print("\n🔗 SHOPIFY INTEGRATION:")
        if not os.environ.get('SHOPIFY_ACCESS_TOKEN'):
            print("  ⚠️  Shopify not configured")
            setup_shopify = input("  Would you like to set up Shopify now? (y/n): ").strip().lower()
            if setup_shopify == 'y':
                print("\n  📝 Get your Shopify credentials:")
                print("     1. Go to Shopify Admin > Apps > Develop apps")
                print("     2. Create private app")
                print("     3. Get Admin API access token")

                shop_name = input("\n  Shopify store name (e.g., 'mystore' from mystore.myshopify.com): ").strip()
                access_token = input("  Admin API access token: ").strip()

                if shop_name and access_token:
                    config['shopify_shop_name'] = shop_name
                    config['shopify_access_token'] = access_token
                    config['check_shopify'] = True
                    print("  ✅ Shopify configured for this session!")
                else:
                    config['check_shopify'] = False
                    config['shopify_shop_name'] = None
                    config['shopify_access_token'] = None
            else:
                config['check_shopify'] = False
                config['shopify_shop_name'] = None
                config['shopify_access_token'] = None
        else:
            config['check_shopify'] = input("    Process Shopify orders? (y/n, default: y): ").strip().lower() != 'n'
            config['shopify_shop_name'] = None
            config['shopify_access_token'] = None

        print("\n📧 NOTIFICATIONS:")
        config['send_confirmations'] = input("  Send order confirmations? (y/n, default: y): ").strip().lower() != 'n'
        config['send_tracking'] = input("  Send tracking numbers? (y/n, default: y): ").strip().lower() != 'n'

        return config

    def setup_legal(self):
        """Setup legal agent."""
        print("\n⚖️  Let's review a contract")
        print("-" * 50)

        config = {}

        print("\n📄 CONTRACT REVIEW:")
        config['file_path'] = input("  Contract file path (.pdf or .docx): ").strip()

        if not config['file_path']:
            print("  ⚠️  No file provided, using demo mode")
            config['file_path'] = "vendor_agreement.pdf"
            config['demo_mode'] = True
        else:
            config['demo_mode'] = False

        print("\n🔍 REVIEW OPTIONS:")
        config['check_risks'] = input("  Identify risks? (y/n, default: y): ").strip().lower() != 'n'
        config['missing_clauses'] = input("  Check for missing clauses? (y/n, default: y): ").strip().lower() != 'n'
        config['generate_redlines'] = input("  Generate redline suggestions? (y/n, default: y): ").strip().lower() != 'n'

        if self.has_ai:
            ai_provider = "Claude" if self.has_claude else "OpenAI"
            config['ai_analysis'] = input(f"  Use {ai_provider} for deep analysis? (y/n, default: y): ").strip().lower() != 'n'
        else:
            print("  ⚠️  AI not configured (set ANTHROPIC_API_KEY or OPENAI_API_KEY)")
            config['ai_analysis'] = False

        return config

    def setup_hospitality(self):
        """Setup hospitality agent."""
        print("\n🏨 Let's make a reservation")
        print("-" * 50)

        config = {}

        print("\n👤 GUEST INFORMATION:")
        config['guest_name'] = input("  Guest name: ").strip() or "John Smith"
        config['guest_email'] = input("  Guest email: ").strip() or "guest@example.com"
        config['guest_phone'] = input("  Guest phone: ").strip() or "+1-555-0100"

        print("\n📅 RESERVATION DATES:")
        config['checkin'] = input("  Check-in date (YYYY-MM-DD, default: tomorrow): ").strip() or "2024-04-15"
        config['checkout'] = input("  Check-out date (YYYY-MM-DD): ").strip() or "2024-04-18"

        print("\n🛏️  ROOM SELECTION:")
        print("  1. Standard Queen")
        print("  2. Deluxe King")
        print("  3. Suite")
        room_choice = input("  Choose room type (1-3, default: 2): ").strip()
        room_map = {"1": "Standard Queen", "2": "Deluxe King", "3": "Suite"}
        config['room_type'] = room_map.get(room_choice, "Deluxe King")

        print("\n🔔 SPECIAL REQUESTS:")
        config['special_requests'] = input("  Any special requests? ").strip() or "High floor, late check-in"

        return config

    def setup_construction(self):
        """Setup construction agent."""
        print("\n🏗️  Let's prepare a project bid")
        print("-" * 50)

        config = {}

        print("\n🏠 PROJECT INFORMATION:")
        config['project_name'] = input("  Project name: ").strip() or "Smith Residence Remodel"
        config['project_type'] = input("  Project type (residential/commercial): ").strip() or "residential"
        config['location'] = input("  Project location: ").strip() or "San Francisco, CA"

        print("\n📋 PROJECT SCOPE:")
        config['blueprints'] = input("  Blueprint file path (.pdf): ").strip()

        if not config['blueprints']:
            print("  ⚠️  No blueprints provided, using estimate mode")

        print("\n💰 COST ESTIMATION:")
        print("  Should we include:")
        config['include_materials'] = input("    Materials? (y/n, default: y): ").strip().lower() != 'n'
        config['include_labor'] = input("    Labor? (y/n, default: y): ").strip().lower() != 'n'
        config['include_subcontractors'] = input("    Subcontractors? (y/n, default: y): ").strip().lower() != 'n'

        return config

    def setup_marketing(self):
        """Setup marketing agent."""
        print("\n📊 Let's create a marketing campaign")
        print("-" * 50)

        config = {}

        print("\n🎯 CAMPAIGN BASICS:")
        config['product'] = input("  Product/Service name: ").strip() or "AI CRM Software"

        budget = input("  Total budget: $").strip()
        config['budget'] = int(budget) if budget else 50000

        config['duration'] = input("  Campaign duration (e.g., '3 months'): ").strip() or "3 months"

        print("\n📢 TARGET AUDIENCE:")
        config['audience'] = input("  Target audience: ").strip() or "B2B SaaS companies"

        print("\n📱 CHANNELS:")
        print("  Which channels should we use?")
        config['use_google_ads'] = input("    Google Ads? (y/n, default: y): ").strip().lower() != 'n'
        config['use_facebook'] = input("    Facebook/Instagram? (y/n, default: y): ").strip().lower() != 'n'
        config['use_linkedin'] = input("    LinkedIn? (y/n, default: y): ").strip().lower() != 'n'
        config['use_email'] = input("    Email marketing? (y/n, default: y): ").strip().lower() != 'n'

        return config

    def setup_email(self):
        """Setup email automation agent."""
        print("\n📧 Let's send an email")
        print("-" * 50)

        config = {}

        # SMTP Setup
        if not os.environ.get('SMTP_USER'):
            print("\n⚠️  Email (SMTP) not configured")
            setup_smtp = input("  Would you like to set up email now? (y/n): ").strip().lower()
            if setup_smtp == 'y':
                print("\n  📝 Enter your SMTP settings:")
                print("     For Gmail: smtp.gmail.com, port 587")
                print("     Get app password: https://myaccount.google.com/apppasswords")

                smtp_config = {}
                smtp_config['host'] = input("\n  SMTP Host (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
                smtp_config['port'] = input("  SMTP Port (default: 587): ").strip() or "587"
                smtp_config['user'] = input("  Email address: ").strip()
                smtp_config['password'] = input("  Password/App Password: ").strip()

                if smtp_config['user'] and smtp_config['password']:
                    config['smtp_config'] = smtp_config
                    print("  ✅ Email configured for this session!")
                else:
                    print("  ⚠️  Skipping email setup")
                    config['smtp_config'] = None
            else:
                config['smtp_config'] = None
        else:
            config['smtp_config'] = None  # Already set in environment

        print("\n📬 EMAIL DETAILS:")
        config['to'] = input("  To (email address): ").strip() or "recipient@example.com"
        config['subject'] = input("  Subject: ").strip() or "Test Email"
        config['body'] = input("  Message: ").strip() or "This is a test email from Zenthral!"

        print("\n⚙️  OPTIONS:")
        config['html'] = input("  Send as HTML? (y/n, default: n): ").strip().lower() == 'y'

        return config

    def setup_sms(self):
        """Setup SMS notification agent."""
        print("\n📱 Let's send an SMS")
        print("-" * 50)

        config = {}

        # Twilio Setup
        if not os.environ.get('TWILIO_ACCOUNT_SID'):
            print("\n⚠️  Twilio not configured")
            setup_twilio = input("  Would you like to set up Twilio now? (y/n): ").strip().lower()
            if setup_twilio == 'y':
                print("\n  📝 Get your Twilio credentials:")
                print("     1. Sign up at https://www.twilio.com/try-twilio (Free $15 credit!)")
                print("     2. Get Account SID, Auth Token, and Phone Number from console")

                twilio_config = {}
                twilio_config['account_sid'] = input("\n  Twilio Account SID: ").strip()
                twilio_config['auth_token'] = input("  Twilio Auth Token: ").strip()
                twilio_config['phone_number'] = input("  Twilio Phone Number (e.g., +1234567890): ").strip()

                if all([twilio_config['account_sid'], twilio_config['auth_token'], twilio_config['phone_number']]):
                    config['twilio_config'] = twilio_config
                    print("  ✅ Twilio configured for this session!")
                else:
                    print("  ⚠️  Skipping Twilio setup")
                    config['twilio_config'] = None
            else:
                config['twilio_config'] = None
        else:
            config['twilio_config'] = None  # Already set in environment

        print("\n💬 SMS DETAILS:")
        config['to'] = input("  To (phone with country code, e.g., +1234567890): ").strip() or "+11234567890"
        config['message'] = input("  Message: ").strip() or "Test SMS from Zenthral!"

        return config

    def setup_pdf(self):
        """Setup PDF generator agent."""
        print("\n📄 Let's generate a PDF")
        print("-" * 50)

        config = {}

        print("\n📑 PDF TYPE:")
        print("  1. Text to PDF")
        print("  2. CSV to PDF Table")
        pdf_choice = input("  Choose (1-2, default: 1): ").strip()

        if pdf_choice == "2":
            config['mode'] = 'csv'
            config['csv_file'] = input("  CSV file path: ").strip()
            config['title'] = input("  PDF title (default: Table Report): ").strip() or "Table Report"
        else:
            config['mode'] = 'text'
            config['text'] = input("  Text content: ").strip() or "Sample PDF content from Zenthral."
            config['title'] = input("  PDF title (default: Document): ").strip() or "Document"

        config['output'] = input("  Output filename (default: output.pdf): ").strip() or "output.pdf"

        return config

    def setup_web_scraper(self):
        """Setup web scraper agent."""
        print("\n🌐 Let's scrape a website")
        print("-" * 50)

        config = {}

        print("\n🔗 WEBSITE:")
        config['url'] = input("  URL to scrape: ").strip() or "https://example.com"

        print("\n📑 SCRAPE MODE:")
        print("  1. Extract text")
        print("  2. Extract links")
        print("  3. Download images")
        mode_choice = input("  Choose (1-3, default: 1): ").strip()
        mode_map = {"1": "text", "2": "links", "3": "images"}
        config['mode'] = mode_map.get(mode_choice, "text")

        if config['mode'] == 'images':
            config['output'] = input("  Output directory (default: images): ").strip() or "images"
        else:
            config['output'] = input("  Save to file (optional, press Enter to skip): ").strip() or None

        return config

    def setup_data_converter(self):
        """Setup data converter agent."""
        print("\n🔄 Let's convert data formats")
        print("-" * 50)

        config = {}

        print("\n📂 FILES:")
        config['input'] = input("  Input file: ").strip()
        config['output'] = input("  Output file: ").strip()

        print("\n🔄 FORMAT:")
        print("  Auto-detected from file extensions")
        print("  Supported: CSV ↔ JSON, CSV ↔ XML, XML → JSON, CSV ↔ Excel")

        return config

    def setup_image_optimizer(self):
        """Setup image optimizer agent."""
        print("\n🖼️  Let's optimize images")
        print("-" * 50)

        config = {}

        print("\n📂 FILES:")
        config['input'] = input("  Input file/directory: ").strip()
        config['output'] = input("  Output file/directory: ").strip()

        print("\n⚙️  MODE:")
        print("  1. Resize")
        print("  2. Compress")
        print("  3. Convert format")
        print("  4. Create thumbnail")
        print("  5. Batch optimize")
        mode_choice = input("  Choose (1-5, default: 2): ").strip()
        mode_map = {"1": "resize", "2": "compress", "3": "convert", "4": "thumbnail", "5": "batch"}
        config['mode'] = mode_map.get(mode_choice, "compress")

        if config['mode'] in ['resize', 'batch']:
            width = input("  Width (optional): ").strip()
            config['width'] = int(width) if width else None

        quality = input("  Quality 1-100 (default: 85): ").strip()
        config['quality'] = int(quality) if quality else 85

        return config

    def setup_slack(self):
        """Setup Slack notifier agent."""
        print("\n💬 Let's send a Slack message")
        print("-" * 50)

        config = {}

        # Slack Webhook Setup
        if not os.environ.get('SLACK_WEBHOOK_URL'):
            print("\n⚠️  Slack not configured")
            setup_slack = input("  Would you like to set up Slack now? (y/n): ").strip().lower()
            if setup_slack == 'y':
                print("\n  📝 Get your Slack webhook URL:")
                print("     1. Go to https://api.slack.com/apps")
                print("     2. Create app > Incoming Webhooks")
                print("     3. Activate webhooks and add to workspace")
                print("     4. Copy webhook URL")

                webhook_url = input("\n  Paste your Slack webhook URL: ").strip()

                if webhook_url:
                    config['slack_webhook_url'] = webhook_url
                    print("  ✅ Slack configured for this session!")
                else:
                    print("  ⚠️  Skipping Slack setup")
                    config['slack_webhook_url'] = None
            else:
                config['slack_webhook_url'] = None
        else:
            config['slack_webhook_url'] = None  # Already set in environment

        print("\n💬 MESSAGE:")
        config['message'] = input("  Message text: ").strip() or "Hello from Zenthral!"

        print("\n📊 TYPE:")
        print("  1. Simple message")
        print("  2. Alert (success/warning/error)")
        type_choice = input("  Choose (1-2, default: 1): ").strip()

        if type_choice == "2":
            print("\n  Alert type:")
            print("    1. Success")
            print("    2. Warning")
            print("    3. Error")
            alert_choice = input("    Choose (1-3): ").strip()
            alert_map = {"1": "success", "2": "warning", "3": "error"}
            config['alert'] = alert_map.get(alert_choice, "info")

        return config

    def run_agent(self, agent_type: str, config: dict):
        """Execute the agent with real configuration."""
        print("\n" + "=" * 70)
        print(f"🚀 Running {agent_type.title()} Agent...")
        print("=" * 70 + "\n")

        # Prepare environment variables for this execution
        env = os.environ.copy()

        # Build command based on agent type
        if agent_type == "finance":
            # Set credentials from config if provided
            if config.get('stripe_api_key'):
                env['STRIPE_API_KEY'] = config['stripe_api_key']

            if config.get('smtp_config'):
                smtp = config['smtp_config']
                env['SMTP_HOST'] = smtp['host']
                env['SMTP_PORT'] = smtp['port']
                env['SMTP_USER'] = smtp['user']
                env['SMTP_PASS'] = smtp['password']

            cmd = [
                "python3",
                str(self.base_path / "finance/agents/invoice-generator/scripts/invoice_agent.py"),
                "--client", config['client_name'],
                "--hours", str(config['hours']),
                "--rate", str(config['rate']),
                "--email", config['client_email']
            ]
        elif agent_type == "real-estate":
            # Set AI credentials if provided
            if config.get('ai_api_key'):
                if config.get('ai_provider') == 'claude':
                    env['ANTHROPIC_API_KEY'] = config['ai_api_key']
                else:
                    env['OPENAI_API_KEY'] = config['ai_api_key']

            cmd = [
                "python3",
                str(self.base_path / "real-estate/agents/listing-agent/scripts/listing_agent.py"),
                "--address", config['address'],
                "--price", str(config['price']),
                "--beds", str(config['bedrooms']),
                "--baths", str(config['bathrooms']),
                "--sqft", str(config['sqft'])
            ]
        elif agent_type == "ecommerce":
            # Set Shopify credentials if provided
            if config.get('shopify_shop_name') and config.get('shopify_access_token'):
                env['SHOPIFY_SHOP_NAME'] = config['shopify_shop_name']
                env['SHOPIFY_ACCESS_TOKEN'] = config['shopify_access_token']

            count = config.get('order_count', 15)
            cmd = [
                "python3",
                str(self.base_path / "ecommerce/agents/order-processor/scripts/order_agent.py"),
                "--count", str(count)
            ]
        elif agent_type == "legal":
            cmd = [
                "python3",
                str(self.base_path / "legal/agents/contract-review/scripts/contract_agent.py"),
                "--file", config['file_path']
            ]
        elif agent_type == "hospitality":
            cmd = [
                "python3",
                str(self.base_path / "hospitality/agents/reservation-agent/scripts/reservation_agent.py"),
                "--guest", config['guest_name'],
                "--checkin", config['checkin'],
                "--checkout", config['checkout'],
                "--room", config['room_type']
            ]
        elif agent_type == "construction":
            cmd = [
                "python3",
                str(self.base_path / "construction/agents/bidding-agent/scripts/bidding_agent.py"),
                "--project", config['project_name'],
                "--type", config.get('project_type', 'residential')
            ]
        elif agent_type == "marketing":
            cmd = [
                "python3",
                str(self.base_path / "marketing/agents/campaign-manager/scripts/campaign_agent.py"),
                "--product", config['product'],
                "--budget", str(config['budget']),
                "--duration", config['duration']
            ]
        elif agent_type == "email":
            # Set SMTP credentials if provided
            if config.get('smtp_config'):
                smtp = config['smtp_config']
                env['SMTP_HOST'] = smtp['host']
                env['SMTP_PORT'] = smtp['port']
                env['SMTP_USER'] = smtp['user']
                env['SMTP_PASS'] = smtp['password']

            cmd = [
                "python3",
                str(self.base_path / "automation/agents/email-sender/scripts/email_agent.py"),
                "--to", config['to'],
                "--subject", config['subject'],
                "--body", config['body']
            ]
            if config.get('html'):
                cmd.append("--html")
        elif agent_type == "sms":
            # Set Twilio credentials if provided
            if config.get('twilio_config'):
                twilio = config['twilio_config']
                env['TWILIO_ACCOUNT_SID'] = twilio['account_sid']
                env['TWILIO_AUTH_TOKEN'] = twilio['auth_token']
                env['TWILIO_PHONE_NUMBER'] = twilio['phone_number']

            cmd = [
                "python3",
                str(self.base_path / "automation/agents/sms-sender/scripts/sms_agent.py"),
                "--to", config['to'],
                "--message", config['message']
            ]
        elif agent_type == "pdf":
            if config['mode'] == 'csv':
                cmd = [
                    "python3",
                    str(self.base_path / "automation/agents/pdf-generator/scripts/pdf_agent.py"),
                    "--csv", config['csv_file'],
                    "--output", config['output'],
                    "--title", config['title']
                ]
            else:
                cmd = [
                    "python3",
                    str(self.base_path / "automation/agents/pdf-generator/scripts/pdf_agent.py"),
                    "--text", config['text'],
                    "--output", config['output'],
                    "--title", config['title']
                ]
        elif agent_type == "web-scraper":
            cmd = [
                "python3",
                str(self.base_path / "automation/agents/web-scraper/scripts/scraper_agent.py"),
                "--url", config['url'],
                "--mode", config['mode']
            ]
            if config.get('output'):
                cmd.extend(["--output", config['output']])
        elif agent_type == "data-converter":
            cmd = [
                "python3",
                str(self.base_path / "automation/agents/data-converter/scripts/converter_agent.py"),
                "--input", config['input'],
                "--output", config['output']
            ]
        elif agent_type == "image-optimizer":
            cmd = [
                "python3",
                str(self.base_path / "automation/agents/image-optimizer/scripts/image_agent.py"),
                "--input", config['input'],
                "--output", config['output'],
                "--mode", config['mode'],
                "--quality", str(config['quality'])
            ]
            if config.get('width'):
                cmd.extend(["--width", str(config['width'])])
        elif agent_type == "slack":
            # Set Slack webhook if provided
            if config.get('slack_webhook_url'):
                env['SLACK_WEBHOOK_URL'] = config['slack_webhook_url']

            cmd = [
                "python3",
                str(self.base_path / "automation/agents/slack-notifier/scripts/slack_agent.py"),
                "--message", config['message']
            ]
            if config.get('alert'):
                cmd = [
                    "python3",
                    str(self.base_path / "automation/agents/slack-notifier/scripts/slack_agent.py"),
                    "--alert", config['alert'],
                    "--text", config['message']
                ]
        else:
            print(f"❌ Unknown agent type: {agent_type}")
            return

        # Execute
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            print(result.stdout)

            if result.returncode != 0 and result.stderr:
                print(f"\n⚠️  Warning: {result.stderr}")

        except Exception as e:
            print(f"\n❌ Error running agent: {e}")

    def chat(self):
        """Main interactive chat loop."""
        self.print_header()

        while True:
            try:
                print("\n" + "=" * 70)
                print("What would you like to do?")
                print("-" * 70)
                print("  INDUSTRY AGENTS:")
                print("  1. 💰 Create Invoice (Finance)")
                print("  2. 🏠 Create Property Listing (Real Estate)")
                print("  3. 🛒 Process Orders (E-commerce)")
                print("  4. ⚖️  Review Contract (Legal)")
                print("  5. 🏨 Make Reservation (Hospitality)")
                print("  6. 🏗️  Prepare Bid (Construction)")
                print("  7. 📊 Create Campaign (Marketing)")
                print("")
                print("  AUTOMATION AGENTS (Easy Setup!):")
                print("  8. 📧 Send Email")
                print("  9. 📱 Send SMS")
                print("  10. 📄 Generate PDF")
                print("  11. 🌐 Scrape Website")
                print("  12. 🔄 Convert Data Formats")
                print("  13. 🖼️  Optimize Images")
                print("  14. 💬 Send Slack Message")
                print("")
                print("  15. ❌ Exit")
                print("-" * 70)

                choice = input("\nSelect (1-15): ").strip()

                if choice == '15' or choice.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thanks for using Zenthral! Goodbye!\n")
                    break

                agent_map = {
                    '1': 'finance',
                    '2': 'real-estate',
                    '3': 'ecommerce',
                    '4': 'legal',
                    '5': 'hospitality',
                    '6': 'construction',
                    '7': 'marketing',
                    '8': 'email',
                    '9': 'sms',
                    '10': 'pdf',
                    '11': 'web-scraper',
                    '12': 'data-converter',
                    '13': 'image-optimizer',
                    '14': 'slack'
                }

                agent_type = agent_map.get(choice)

                if not agent_type:
                    print("\n❌ Invalid choice. Please select 1-15.")
                    continue

                # Run setup wizard
                config = self.setup_wizard(agent_type)

                # Confirm before running
                print("\n" + "=" * 70)
                print("📋 CONFIGURATION SUMMARY:")
                print("-" * 70)
                for key, value in config.items():
                    print(f"  {key}: {value}")
                print("=" * 70)

                confirm = input("\n✅ Proceed with this configuration? (y/n): ").strip().lower()

                if confirm == 'y':
                    self.run_agent(agent_type, config)
                else:
                    print("\n❌ Cancelled. Returning to main menu...")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Returning to main menu...\n")

def main():
    chat = InteractiveChat()
    chat.chat()

if __name__ == "__main__":
    main()
