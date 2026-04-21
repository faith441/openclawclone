---
name: patient-intake-agent
description: Automate patient onboarding with AI-powered form processing, insurance verification, and EMR integration. Use for new patient registration, annual health assessments, and pre-visit questionnaires.
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
              "package": "openai requests pydantic",
              "label": "Install Python dependencies (uv)",
            },
          ],
      },
  }
---

# Patient Intake Agent

Automates patient onboarding with AI-powered form processing, insurance verification, and EMR integration.

## Features

- Digital intake form processing with validation
- AI medical history extraction (GPT-4)
- Insurance eligibility verification
- HIPAA-compliant audit logging
- EMR/EHR integration ready
- Automated patient confirmations

## Quick Start

```bash
# Set API keys
export OPENAI_API_KEY="sk-..."
export ELIGIBLE_API_KEY="..."  # Optional, for insurance verification

# Interactive intake
python scripts/intake_agent.py intake --interactive

# Process from JSON file
python scripts/intake_agent.py intake --file patient_data.json

# View patient record
python scripts/intake_agent.py view P-20240328-abc123
```

## Example Input

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "dob": "1990-01-15",
  "email": "john.doe@example.com",
  "phone": "555-0100",
  "insurance_provider": "Blue Cross Blue Shield",
  "insurance_id": "ABC123456789",
  "medical_history_text": "Diabetes, takes metformin daily. Allergic to penicillin."
}
```

## HIPAA Compliance

This agent logs all PHI access. Ensure:
- Database encryption at rest
- TLS/SSL for all connections
- Proper access controls
- BAA agreements with vendors
