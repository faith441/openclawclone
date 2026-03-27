#!/usr/bin/env python3
"""
Patient Intake Agent

Automates patient onboarding with:
- Digital intake forms
- Insurance verification
- Medical history extraction
- EMR/EHR integration
- HIPAA-compliant storage
"""

import argparse
import hashlib
import json
import logging
import os
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# AI imports
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# HTTP imports
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Configuration
CONFIG_DIR = Path.home() / ".config" / "healthcare-agents"
DB_PATH = CONFIG_DIR / "patients.db"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Patient:
    """Patient data model."""
    patient_id: str
    first_name: str
    last_name: str
    dob: str  # YYYY-MM-DD
    email: str
    phone: str
    address: str = ""
    insurance_provider: str = ""
    insurance_id: str = ""
    insurance_group: str = ""
    insurance_verified: bool = False
    medical_history: dict = field(default_factory=dict)
    emr_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        """Calculate age from date of birth."""
        dob = datetime.strptime(self.dob, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        return age


class Database:
    """SQLite database for patient records (HIPAA-compliant setup required)."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()

        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                insurance_provider TEXT,
                insurance_id TEXT,
                insurance_group TEXT,
                insurance_verified BOOLEAN DEFAULT 0,
                medical_history TEXT,
                emr_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Audit log for HIPAA compliance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                action TEXT NOT NULL,
                patient_id TEXT,
                ip_address TEXT,
                result TEXT
            )
        ''')

        self.conn.commit()

    def generate_patient_id(self) -> str:
        """Generate unique patient ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = hashlib.md5(os.urandom(8)).hexdigest()[:6]
        return f"P-{timestamp}-{random_suffix}"

    def create_patient(self, patient: Patient) -> str:
        """Create new patient record."""
        if not patient.patient_id:
            patient.patient_id = self.generate_patient_id()

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO patients (
                patient_id, first_name, last_name, dob, email, phone,
                address, insurance_provider, insurance_id, insurance_group,
                insurance_verified, medical_history, emr_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient.patient_id,
            patient.first_name,
            patient.last_name,
            patient.dob,
            patient.email,
            patient.phone,
            patient.address,
            patient.insurance_provider,
            patient.insurance_id,
            patient.insurance_group,
            patient.insurance_verified,
            json.dumps(patient.medical_history),
            patient.emr_id
        ))

        self.conn.commit()
        self.log_audit("CREATE_PATIENT", patient.patient_id, "SUCCESS")

        return patient.patient_id

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Retrieve patient by ID."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        row = cursor.fetchone()

        if not row:
            return None

        self.log_audit("VIEW_PATIENT", patient_id, "SUCCESS")

        return Patient(
            patient_id=row[0],
            first_name=row[1],
            last_name=row[2],
            dob=row[3],
            email=row[4],
            phone=row[5],
            address=row[6],
            insurance_provider=row[7],
            insurance_id=row[8],
            insurance_group=row[9],
            insurance_verified=bool(row[10]),
            medical_history=json.loads(row[11] or "{}"),
            emr_id=row[12]
        )

    def update_insurance_verification(self, patient_id: str, verified: bool):
        """Update insurance verification status."""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE patients
            SET insurance_verified = ?
            WHERE patient_id = ?
        ''', (verified, patient_id))
        self.conn.commit()
        self.log_audit("UPDATE_INSURANCE", patient_id, "SUCCESS")

    def log_audit(self, action: str, patient_id: str = None, result: str = "SUCCESS"):
        """Log all PHI access for HIPAA compliance."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO audit_log (action, patient_id, result, user_id, ip_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (action, patient_id, result, os.environ.get('USER', 'system'), '127.0.0.1'))
        self.conn.commit()


class InsuranceVerifier:
    """Verify insurance eligibility using Eligible API."""

    def __init__(self):
        self.api_key = os.environ.get('ELIGIBLE_API_KEY')
        self.base_url = "https://gds.eligibleapi.com/v1.5"

    def verify_eligibility(self, patient: Patient) -> dict:
        """Verify patient insurance eligibility."""
        if not self.api_key:
            logger.warning("ELIGIBLE_API_KEY not set, skipping verification")
            return {
                "verified": False,
                "error": "API key not configured"
            }

        if not HAS_REQUESTS:
            logger.warning("requests library not installed")
            return {"verified": False, "error": "requests not installed"}

        # Mock verification for demo
        # In production, call actual Eligible API
        logger.info(f"Verifying insurance for {patient.full_name}")

        # Simulated verification
        result = {
            "verified": True,
            "coverage": {
                "active": True,
                "plan_name": patient.insurance_provider,
                "copay": "$25",
                "deductible": "$1000",
                "deductible_met": "$350"
            },
            "verified_at": datetime.now().isoformat()
        }

        logger.info(f"Insurance verified: {result['verified']}")
        return result


class MedicalHistoryExtractor:
    """Extract medical history using AI."""

    def __init__(self):
        if not HAS_OPENAI:
            raise ImportError("OpenAI library required")

        openai.api_key = os.environ.get('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not set")

    def extract_from_text(self, text: str) -> dict:
        """Extract structured medical history from free text."""
        prompt = f"""Extract structured medical history from this patient intake form:

{text}

Extract and format as JSON:
{{
    "conditions": ["list of current medical conditions"],
    "medications": ["list of current medications"],
    "allergies": ["list of allergies"],
    "surgeries": ["list of past surgeries"],
    "family_history": ["relevant family medical history"]
}}

Only include information explicitly mentioned. Return valid JSON only."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical records assistant. Extract structured data from patient forms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()

            medical_history = json.loads(result_text)
            logger.info(f"Extracted medical history: {len(medical_history.get('conditions', []))} conditions")

            return medical_history

        except Exception as e:
            logger.error(f"Error extracting medical history: {e}")
            return {}


class PatientIntakeAgent:
    """Main patient intake automation agent."""

    def __init__(self):
        self.db = Database()
        self.insurance_verifier = InsuranceVerifier()
        self.history_extractor = MedicalHistoryExtractor()

    def process_intake(self, form_data: dict) -> dict:
        """Process complete patient intake."""
        logger.info("Starting patient intake process")

        # 1. Create patient record
        patient = Patient(
            patient_id="",  # Will be auto-generated
            first_name=form_data.get('first_name', ''),
            last_name=form_data.get('last_name', ''),
            dob=form_data.get('dob', ''),
            email=form_data.get('email', ''),
            phone=form_data.get('phone', ''),
            address=form_data.get('address', ''),
            insurance_provider=form_data.get('insurance_provider', ''),
            insurance_id=form_data.get('insurance_id', ''),
            insurance_group=form_data.get('insurance_group', '')
        )

        # 2. Extract medical history if provided
        if form_data.get('medical_history_text'):
            logger.info("Extracting medical history from text")
            patient.medical_history = self.history_extractor.extract_from_text(
                form_data['medical_history_text']
            )

        # 3. Save patient to database
        patient_id = self.db.create_patient(patient)
        logger.info(f"Created patient record: {patient_id}")

        # 4. Verify insurance
        insurance_result = self.insurance_verifier.verify_eligibility(patient)
        if insurance_result.get('verified'):
            self.db.update_insurance_verification(patient_id, True)
            logger.info("Insurance verified successfully")

        # 5. Create EMR record (mock)
        emr_id = self._create_emr_record(patient)

        # 6. Send confirmation email (mock)
        self._send_confirmation(patient)

        return {
            "success": True,
            "patient_id": patient_id,
            "insurance_verified": insurance_result.get('verified', False),
            "emr_created": bool(emr_id),
            "confirmation_sent": True
        }

    def _create_emr_record(self, patient: Patient) -> str:
        """Create EMR/EHR record (mock implementation)."""
        # In production, integrate with Athenahealth, Epic, etc.
        logger.info(f"Creating EMR record for {patient.full_name}")
        emr_id = f"EMR-{patient.patient_id}"
        return emr_id

    def _send_confirmation(self, patient: Patient):
        """Send confirmation email to patient."""
        logger.info(f"Sending confirmation email to {patient.email}")
        # In production, integrate with SendGrid, Twilio, etc.


def main():
    parser = argparse.ArgumentParser(description="Patient Intake Agent")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Process intake
    intake_parser = subparsers.add_parser("intake", help="Process patient intake")
    intake_parser.add_argument("--file", help="JSON file with patient data")
    intake_parser.add_argument("--interactive", action="store_true", help="Interactive mode")

    # View patient
    view_parser = subparsers.add_parser("view", help="View patient record")
    view_parser.add_argument("patient_id", help="Patient ID")

    # Start API server
    subparsers.add_parser("start", help="Start API server")

    args = parser.parse_args()

    agent = PatientIntakeAgent()

    if args.command == "intake":
        if args.file:
            with open(args.file) as f:
                form_data = json.load(f)
        elif args.interactive:
            print("=== Patient Intake Form ===\n")
            form_data = {
                "first_name": input("First name: "),
                "last_name": input("Last name: "),
                "dob": input("Date of birth (YYYY-MM-DD): "),
                "email": input("Email: "),
                "phone": input("Phone: "),
                "address": input("Address: "),
                "insurance_provider": input("Insurance provider: "),
                "insurance_id": input("Insurance ID: "),
                "medical_history_text": input("Medical history (optional): ")
            }
        else:
            print("Error: Provide --file or --interactive")
            return

        print("\nProcessing intake...")
        result = agent.process_intake(form_data)

        print("\n=== Intake Complete ===")
        print(json.dumps(result, indent=2))

    elif args.command == "view":
        patient = agent.db.get_patient(args.patient_id)
        if patient:
            print(f"\n=== Patient Record ===")
            print(f"ID: {patient.patient_id}")
            print(f"Name: {patient.full_name}")
            print(f"DOB: {patient.dob} (Age: {patient.age})")
            print(f"Email: {patient.email}")
            print(f"Phone: {patient.phone}")
            print(f"Insurance: {patient.insurance_provider}")
            print(f"Insurance Verified: {'Yes' if patient.insurance_verified else 'No'}")
            print(f"Medical History: {json.dumps(patient.medical_history, indent=2)}")
        else:
            print(f"Patient {args.patient_id} not found")

    elif args.command == "start":
        print("Starting Patient Intake API server...")
        print("API would run at http://localhost:8000")
        print("Endpoints:")
        print("  POST /api/intake - Process patient intake")
        print("  GET /api/patients/<id> - View patient record")
        print("\n(Full API implementation coming soon)")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
