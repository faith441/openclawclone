# Healthcare AI Agents

AI-powered automation for healthcare practices, clinics, and hospitals. HIPAA-compliant agents for patient management, scheduling, billing, and medical records.

## 🏥 Available Agents

### 1. Patient Intake Agent
Automates patient onboarding with AI-powered form processing, insurance verification, and medical history collection.

**Features:**
- Digital intake forms with validation
- Insurance eligibility verification
- Medical history extraction from documents
- Auto-populate EMR/EHR systems
- Consent form management

**Use Cases:**
- New patient registration
- Annual health assessments
- Pre-visit questionnaires

### 2. Appointment Scheduler
Intelligent appointment scheduling with conflict detection, automated reminders, and patient preferences.

**Features:**
- Natural language appointment booking
- Provider availability management
- Automated SMS/email reminders
- Telehealth appointment setup
- Waitlist management

**Use Cases:**
- Phone/web appointment booking
- Follow-up scheduling
- Emergency slot management

### 3. Medical Billing Agent
Automated medical billing, insurance claims, and payment processing.

**Features:**
- CPT/ICD-10 code automation
- Insurance claim submission (EDI 837)
- Claim status tracking
- Payment posting
- Denial management

**Use Cases:**
- Medical billing automation
- Insurance claims processing
- Revenue cycle management

## Prerequisites

### Required APIs & Services

```bash
# Healthcare APIs
export ELIGIBLE_API_KEY="..."        # Insurance verification
export ATHENAHEALTH_KEY="..."        # EMR integration (if using)
export TWILIO_ACCOUNT_SID="..."      # SMS reminders
export TWILIO_AUTH_TOKEN="..."

# AI Services
export OPENAI_API_KEY="sk-..."       # GPT-4 for NLP
export ANTHROPIC_API_KEY="..."       # Claude (optional)

# Database
export DATABASE_URL="postgresql://user:pass@localhost/healthcare"
```

### Compliance

⚠️ **HIPAA Compliance Required**
- Encrypt data at rest and in transit
- Implement audit logging
- Use secure authentication (OAuth2)
- Sign Business Associate Agreements (BAAs)
- Regular security assessments

## Quick Start

```bash
# 1. Navigate to healthcare
cd industries/healthcare

# 2. Install dependencies (uses shared requirements)
pip install -r requirements.txt

# 3. Configure agents
cp config/agents.example.yaml config/agents.yaml
# Edit with your API keys and settings

# 4. Run a specific agent
cd agents/patient-intake-agent
python scripts/intake_agent.py start

# 5. Or run all agents
docker-compose up
```

## Architecture

```
┌─────────────┐
│   Patient   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Patient Intake Agent            │
│  - Form processing                  │
│  - Insurance verification           │
│  - Document extraction              │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│     EMR/EHR System                  │
│  (Athenahealth, Epic, Cerner)       │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Appointment Scheduler           │
│  - Availability matching            │
│  - Automated reminders              │
│  - Telehealth setup                 │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Medical Billing Agent           │
│  - Coding automation                │
│  - Claims submission                │
│  - Payment processing               │
└─────────────────────────────────────┘
```

## Integrations

### EMR/EHR Systems
- **Athenahealth**: Full API integration
- **Epic**: FHIR API support
- **Cerner**: HL7/FHIR integration
- **DrChrono**: REST API
- **Practice Fusion**: API integration

### Insurance Verification
- **Eligible API**: Real-time eligibility
- **Change Healthcare**: Clearinghouse integration
- **Availity**: Multi-payer portal

### Communication
- **Twilio**: SMS reminders and notifications
- **SendGrid**: Email communications
- **RingCentral**: Phone integration

## Sample Workflows

### New Patient Onboarding

```python
from healthcare.agents import PatientIntakeAgent

agent = PatientIntakeAgent()

# Patient fills out digital form
form_data = {
    "first_name": "John",
    "last_name": "Doe",
    "dob": "1990-01-15",
    "insurance_id": "ABC123456",
    "insurance_provider": "Blue Cross",
    "chief_complaint": "Annual checkup"
}

# Agent processes intake
result = agent.process_intake(form_data)

# Automatically:
# 1. Verifies insurance eligibility
# 2. Extracts medical history
# 3. Creates patient record in EMR
# 4. Schedules first appointment
# 5. Sends confirmation email

print(result)
# {
#   "patient_id": "P-12345",
#   "insurance_verified": True,
#   "emr_created": True,
#   "appointment_id": "A-67890",
#   "confirmation_sent": True
# }
```

### Appointment Scheduling

```python
from healthcare.agents import AppointmentScheduler

scheduler = AppointmentScheduler()

# Natural language scheduling
booking = scheduler.book_appointment(
    patient_id="P-12345",
    request="I need to see Dr. Smith next Tuesday afternoon",
    provider_preference="Dr. Smith",
    visit_type="Follow-up"
)

# Automatically:
# 1. Finds available slots
# 2. Checks provider availability
# 3. Books appointment
# 4. Sends confirmation
# 5. Sets up reminders

print(booking)
# {
#   "appointment_id": "A-67890",
#   "datetime": "2024-04-02 14:30:00",
#   "provider": "Dr. Smith",
#   "reminders_scheduled": ["24h", "2h"]
# }
```

## Security & Compliance

### Data Encryption
```yaml
# config/security.yaml
encryption:
  at_rest: AES-256
  in_transit: TLS 1.3
  key_management: AWS KMS

audit_logging:
  enabled: true
  log_all_access: true
  retention_days: 2555  # 7 years (HIPAA requirement)

authentication:
  method: OAuth2
  mfa_required: true
  session_timeout: 15  # minutes
```

### Audit Logging
All PHI access is logged:
```
[2024-03-28 10:15:23] User: dr_smith@clinic.com
Action: VIEW_PATIENT_RECORD
Patient ID: P-12345
IP: 192.168.1.100
Result: SUCCESS
```

## Testing

```bash
# Unit tests
pytest tests/

# Integration tests (requires test database)
pytest tests/integration/

# HIPAA compliance tests
pytest tests/compliance/

# Load testing
locust -f tests/load/locustfile.py
```

## Deployment

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  patient-intake:
    build: ./agents/patient-intake-agent
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    ports:
      - "8001:8000"

  appointment-scheduler:
    build: ./agents/appointment-scheduler
    environment:
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
    ports:
      - "8002:8000"

  medical-billing:
    build: ./agents/medical-billing-agent
    ports:
      - "8003:8000"

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: healthcare
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
# Deploy
docker-compose up -d

# View logs
docker-compose logs -f

# Scale agents
docker-compose up -d --scale patient-intake=3
```

## Monitoring & Analytics

### Metrics Dashboard
- Patient intake completion rate
- Average intake time
- Insurance verification success rate
- Appointment no-show rate
- Billing claim acceptance rate

### Alerts
- Failed insurance verifications
- Appointment reminder failures
- Claim denials
- System errors

## Cost Estimates

### API Costs (per 1000 patients/month)
- **OpenAI GPT-4**: ~$50-100 (NLP processing)
- **Eligible API**: ~$50 (insurance verification)
- **Twilio SMS**: ~$75 (reminders)
- **Total**: ~$175-225/month

### Infrastructure
- **Database**: ~$25-50/month (managed PostgreSQL)
- **Hosting**: ~$50-100/month (cloud VMs)
- **Total**: ~$75-150/month

**Total Monthly Cost**: ~$250-375 for 1000 patients

## Support

For healthcare-specific questions:
- 📧 Email: healthcare-agents@yourdomain.com
- 💬 Slack: #healthcare-agents
- 📚 Docs: https://docs.yourdomain.com/healthcare

## License

See main repository LICENSE. Note: You are responsible for ensuring HIPAA compliance in your deployment.
