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

Automates patient onboarding with AI-powered form processing and insurance verification.

## Quick Deploy

```bash
$ openclaw deploy --agent patient-intake
✓ Agent "patient-intake" is live and running
Connected: OpenAI, Eligible API, EMR System
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure HIPAA compliance manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install patient-intake-agent
✓ Installed patient-intake-agent v1.0.0

# Interactive intake session
$ openclaw run patient-intake --interactive
? Patient first name: John
? Patient last name: Doe
? Date of birth: 1990-01-15
? Insurance provider: Blue Cross Blue Shield
...
✓ Patient registered: P-20240422-abc123
✓ Insurance verified: Active coverage
✓ EMR record created
✓ Confirmation sent to john.doe@example.com

# Process from JSON file
$ openclaw run patient-intake --file patient_data.json
✓ Processing patient: Jane Smith
✓ Insurance verified: Aetna (Active)
✓ Medical history extracted: Diabetes, Hypertension
✓ EMR record created: P-20240422-xyz789

# View patient record
$ openclaw run patient-intake view P-20240422-abc123
Patient: John Doe
Status: Active
Insurance: Blue Cross Blue Shield (Verified)
```

## Features

- Digital intake form processing with validation
- AI medical history extraction (GPT-4)
- Real-time insurance eligibility verification
- HIPAA-compliant audit logging
- EMR/EHR integration ready
- Automated patient confirmations

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export ELIGIBLE_API_KEY="..."            # Insurance verification (optional)
```
