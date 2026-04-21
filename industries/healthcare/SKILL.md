---
name: healthcare-agents
description: AI-powered automation for healthcare practices, clinics, and hospitals. HIPAA-compliant agents for patient intake, appointment scheduling, medical billing, and records management.
homepage: https://github.com/openclaw/industries/healthcare
metadata:
  {
    "openclaw":
      {
        "emoji": "🏥",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests pydantic twilio",
              "label": "Install Healthcare dependencies (uv)",
            },
          ],
      },
  }
---

# Healthcare AI Agents

AI-powered automation for healthcare practices with HIPAA-compliant patient management.

## Quick Deploy

```bash
$ openclaw deploy --agent healthcare-bot
✓ Agent "healthcare-bot" is live and running
Connected: EMR/EHR, Insurance API, Twilio, Calendar
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure HIPAA compliance manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install healthcare-agents
✓ Installed healthcare-agents v1.0.0

# Deploy patient intake agent
$ openclaw deploy --agent patient-intake
✓ Agent "patient-intake" is live and running
Connected: OpenAI, Eligible API, EMR System

# Process a new patient
$ openclaw run patient-intake --file patient_data.json
✓ Patient John Doe registered
✓ Insurance verified: Blue Cross (Active)
✓ EMR record created: P-20240422-abc123
✓ Confirmation email sent
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `patient-intake` | Automates patient onboarding, insurance verification, medical history |
| `appointment-scheduler` | Smart scheduling with reminders and telehealth setup |
| `medical-billing` | CPT/ICD-10 coding, claims submission, denial management |
| `prescription-manager` | E-prescription and refill automation |
| `medical-records` | HIPAA-compliant records management with audit logging |

## Integrations

- **EMR/EHR**: Athenahealth, Epic, Cerner, DrChrono
- **Insurance**: Eligible API, Change Healthcare, Availity
- **Communication**: Twilio, SendGrid, RingCentral

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export ELIGIBLE_API_KEY="..."            # Insurance verification
export TWILIO_ACCOUNT_SID="..."          # SMS reminders
export TWILIO_AUTH_TOKEN="..."
```
