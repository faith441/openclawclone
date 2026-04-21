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

## Available Agents

### 1. Patient Intake Agent
Automates patient onboarding with AI-powered form processing, insurance verification, and medical history collection.

### 2. Appointment Scheduler
Intelligent appointment scheduling with conflict detection, automated reminders, and telehealth setup.

### 3. Medical Billing Agent
Automated medical billing, CPT/ICD-10 coding, insurance claims submission, and denial management.

### 4. Prescription Manager
E-prescription and refill automation with pharmacy integration.

### 5. Medical Records Agent
HIPAA-compliant records management with audit logging.

## Quick Start

```bash
cd industries/healthcare
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export ELIGIBLE_API_KEY="..."        # Insurance verification
export TWILIO_ACCOUNT_SID="..."      # SMS reminders

cd agents/patient-intake-agent
python scripts/intake_agent.py start
```

## Integrations

- **EMR/EHR**: Athenahealth, Epic, Cerner, DrChrono
- **Insurance**: Eligible API, Change Healthcare, Availity
- **Communication**: Twilio, SendGrid, RingCentral

## HIPAA Compliance Required

- AES-256 encryption at rest
- TLS 1.3 for data in transit
- Multi-factor authentication
- 7-year audit log retention
- Business Associate Agreements (BAAs)
