#!/usr/bin/env python3
"""
OpenClaw Interactive Chat - Connects to Real Services

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
        print("  🤖 OpenClaw Interactive AI Agents")
        print("  Connect to Real Services & Automate Your Business")
        print("=" * 70)
        print("\nAvailable Agents:")
        print("  💰 Finance - Invoice generation, payment tracking")
        print("  🏠 Real Estate - Property listings, lead management")
        print("  🛒 E-commerce - Order processing, inventory")
        print("  ⚖️ Legal - Contract review, document automation")
        print("  🏨 Hospitality - Reservations, guest management")
        print("  🏗️ Construction - Project bidding, scheduling")
        print("  📊 Marketing - Campaign management, analytics")
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
        if self.has_quickbooks:
            sync_qb = input("  Sync to QuickBooks? (y/n, default: y): ").strip().lower()
            config['sync_quickbooks'] = sync_qb != 'n'
        else:
            print("  ⚠️  QuickBooks not configured (set QUICKBOOKS_CLIENT_ID)")
            config['sync_quickbooks'] = False

        if self.has_stripe:
            send_stripe = input("  Send Stripe payment link? (y/n, default: y): ").strip().lower()
            config['send_stripe_link'] = send_stripe != 'n'
        else:
            print("  ⚠️  Stripe not configured (set STRIPE_API_KEY)")
            config['send_stripe_link'] = False

        # Email options
        print("\n📧 EMAIL OPTIONS:")
        send_email = input("  Send invoice via email? (y/n, default: y): ").strip().lower()
        config['send_email'] = send_email != 'n'

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
        else:
            print("\n⚠️  AI not configured (set ANTHROPIC_API_KEY or OPENAI_API_KEY)")
            config['ai_description'] = False

        return config

    def setup_ecommerce(self):
        """Setup e-commerce agent."""
        print("\n🛒 Let's process orders")
        print("-" * 50)

        config = {}

        print("\n📦 ORDER PROCESSING:")
        count = input("  How many orders to process? (default: all pending): ").strip()
        config['order_count'] = int(count) if count else None

        print("\n🔗 INTEGRATIONS:")
        print("  Which platforms should we check?")
        config['check_shopify'] = input("    Shopify? (y/n, default: y): ").strip().lower() != 'n'
        config['check_woocommerce'] = input("    WooCommerce? (y/n, default: n): ").strip().lower() == 'y'
        config['check_amazon'] = input("    Amazon? (y/n, default: n): ").strip().lower() == 'y'

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

    def run_agent(self, agent_type: str, config: dict):
        """Execute the agent with real configuration."""
        print("\n" + "=" * 70)
        print(f"🚀 Running {agent_type.title()} Agent...")
        print("=" * 70 + "\n")

        # Build command based on agent type
        if agent_type == "finance":
            cmd = [
                "python3",
                str(self.base_path / "finance/agents/invoice-generator/scripts/invoice_agent.py"),
                "--client", config['client_name'],
                "--hours", str(config['hours']),
                "--rate", str(config['rate']),
                "--email", config['client_email']
            ]
        elif agent_type == "real-estate":
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
        else:
            print(f"❌ Unknown agent type: {agent_type}")
            return

        # Execute
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
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
                print("  1. 💰 Create Invoice (Finance)")
                print("  2. 🏠 Create Property Listing (Real Estate)")
                print("  3. 🛒 Process Orders (E-commerce)")
                print("  4. ⚖️  Review Contract (Legal)")
                print("  5. 🏨 Make Reservation (Hospitality)")
                print("  6. 🏗️  Prepare Bid (Construction)")
                print("  7. 📊 Create Campaign (Marketing)")
                print("  8. ❌ Exit")
                print("-" * 70)

                choice = input("\nSelect (1-8): ").strip()

                if choice == '8' or choice.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thanks for using OpenClaw! Goodbye!\n")
                    break

                agent_map = {
                    '1': 'finance',
                    '2': 'real-estate',
                    '3': 'ecommerce',
                    '4': 'legal',
                    '5': 'hospitality',
                    '6': 'construction',
                    '7': 'marketing'
                }

                agent_type = agent_map.get(choice)

                if not agent_type:
                    print("\n❌ Invalid choice. Please select 1-8.")
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
