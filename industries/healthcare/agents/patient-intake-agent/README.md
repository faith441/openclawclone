# Patient Intake Agent

Automates patient onboarding with AI-powered form processing, insurance verification, and EMR integration.

## Features

- ✅ Digital intake form processing
- ✅ AI medical history extraction (GPT-4)
- ✅ Insurance eligibility verification
- ✅ HIPAA-compliant audit logging
- ✅ EMR/EHR integration ready
- ✅ Automated confirmations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

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

## Example

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "dob": "1990-01-15",
  "email": "john.doe@example.com",
  "phone": "555-0100",
  "address": "123 Main St, City, ST 12345",
  "insurance_provider": "Blue Cross Blue Shield",
  "insurance_id": "ABC123456789",
  "insurance_group": "GRP001",
  "medical_history_text": "Diabetes, takes metformin daily. Allergic to penicillin."
}
```

## Output

```json
{
  "success": true,
  "patient_id": "P-20240328-abc123",
  "insurance_verified": true,
  "emr_created": true,
  "confirmation_sent": true
}
```

## HIPAA Compliance

⚠️ **Important**: This agent logs all PHI access. Ensure:
- Database is encrypted at rest
- TLS/SSL for all connections
- Proper access controls
- Regular security audits
- BAA agreements with vendors

## Documentation

See [Healthcare README](../../README.md) for full setup and integration details.
