#!/usr/bin/env python3
"""
OpenClaw-Style Chat Interface for Industry Agents

Natural language interface to all industry AI agents.
"""

import subprocess
import sys
from pathlib import Path

class OpenClawChat:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.agents = {
            "invoice": {
                "path": "finance/agents/invoice-generator/scripts/invoice_agent.py",
                "keywords": ["invoice", "bill", "payment", "finance", "accounting"]
            },
            "listing": {
                "path": "real-estate/agents/listing-agent/scripts/listing_agent.py",
                "keywords": ["property", "listing", "real estate", "house", "home"]
            },
            "order": {
                "path": "ecommerce/agents/order-processor/scripts/order_agent.py",
                "keywords": ["order", "ecommerce", "shop", "purchase", "product"]
            },
            "contract": {
                "path": "legal/agents/contract-review/scripts/contract_agent.py",
                "keywords": ["contract", "legal", "review", "agreement", "terms"]
            },
            "reservation": {
                "path": "hospitality/agents/reservation-agent/scripts/reservation_agent.py",
                "keywords": ["hotel", "reservation", "booking", "room", "guest"]
            },
            "bid": {
                "path": "construction/agents/bidding-agent/scripts/bidding_agent.py",
                "keywords": ["construction", "bid", "estimate", "project", "building"]
            },
            "campaign": {
                "path": "marketing/agents/campaign-manager/scripts/campaign_agent.py",
                "keywords": ["marketing", "campaign", "ads", "promotion", "advertising"]
            }
        }

    def detect_intent(self, message: str) -> str:
        """Detect which agent to use based on message."""
        message_lower = message.lower()

        for agent_name, agent_info in self.agents.items():
            for keyword in agent_info["keywords"]:
                if keyword in message_lower:
                    return agent_name

        return None

    def parse_command(self, message: str, agent: str) -> list:
        """Parse natural language into CLI arguments."""
        message_lower = message.lower()

        if agent == "invoice":
            # Extract client, hours, rate
            client = "Client"
            hours = 40
            rate = 150

            if "acme" in message_lower:
                client = "Acme Corp"
            if "hours" in message_lower:
                words = message_lower.split()
                for i, word in enumerate(words):
                    if "hours" in word and i > 0:
                        try:
                            hours = int(words[i-1])
                        except:
                            pass

            return ["--client", client, "--hours", str(hours), "--rate", str(rate)]

        elif agent == "listing":
            address = "123 Main St, City, ST"
            price = 500000

            if "address" in message_lower or "property" in message_lower:
                # Try to extract address from quotes
                if '"' in message:
                    parts = message.split('"')
                    if len(parts) >= 2:
                        address = parts[1]

            return ["--address", address, "--price", str(price)]

        elif agent == "order":
            count = 15
            if "orders" in message_lower:
                words = message_lower.split()
                for i, word in enumerate(words):
                    if word.isdigit():
                        count = int(word)
                        break

            return ["--count", str(count)]

        elif agent == "contract":
            filename = "contract.pdf"
            if ".pdf" in message_lower:
                words = message.split()
                for word in words:
                    if ".pdf" in word:
                        filename = word
                        break

            return ["--file", filename]

        elif agent == "reservation":
            guest = "Guest Name"
            if '"' in message:
                parts = message.split('"')
                if len(parts) >= 2:
                    guest = parts[1]
            elif "for " in message_lower:
                parts = message_lower.split("for ")
                if len(parts) >= 2:
                    guest = parts[1].split()[0].title()

            return ["--guest", guest]

        elif agent == "bid":
            project = "Project Name"
            if '"' in message:
                parts = message.split('"')
                if len(parts) >= 2:
                    project = parts[1]

            return ["--project", project]

        elif agent == "campaign":
            product = "Product"
            budget = 50000

            if '"' in message:
                parts = message.split('"')
                if len(parts) >= 2:
                    product = parts[1]

            if "budget" in message_lower or "$" in message:
                words = message.replace("$", "").replace(",", "").split()
                for word in words:
                    if word.isdigit():
                        budget = int(word)
                        break

            return ["--product", product, "--budget", str(budget)]

        return []

    def run_agent(self, agent: str, args: list):
        """Execute the agent script."""
        agent_path = self.base_path / self.agents[agent]["path"]

        cmd = ["python3", str(agent_path)] + args

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running agent: {e}"

    def chat(self):
        """Start interactive chat session."""
        print("=" * 60)
        print("  OpenClaw Industry AI Agents - Chat Interface")
        print("=" * 60)
        print("\nAvailable agents:")
        print("  💰 Finance: Create invoices")
        print("  🏠 Real Estate: Create property listings")
        print("  🛒 E-commerce: Process orders")
        print("  ⚖️ Legal: Review contracts")
        print("  🏨 Hospitality: Make reservations")
        print("  🏗️ Construction: Prepare bids")
        print("  📊 Marketing: Create campaigns")
        print("\nType your request in natural language, or 'quit' to exit.")
        print("=" * 60)

        while True:
            try:
                message = input("\n> ").strip()

                if message.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                if not message:
                    continue

                # Detect which agent to use
                agent = self.detect_intent(message)

                if not agent:
                    print("❌ I'm not sure which agent to use. Try mentioning:")
                    print("   invoice, property, order, contract, reservation, bid, or campaign")
                    continue

                # Parse the command
                args = self.parse_command(message, agent)

                # Run the agent
                print(f"\n🤖 Running {agent} agent...")
                output = self.run_agent(agent, args)
                print(output)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    chat = OpenClawChat()
    chat.chat()

if __name__ == "__main__":
    main()
