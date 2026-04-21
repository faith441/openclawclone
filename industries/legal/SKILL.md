---
name: legal-agents
description: AI-powered automation for law firms and legal departments. Agents for contract review, legal research, document automation, case management, and e-discovery.
homepage: https://github.com/openclaw/industries/legal
metadata:
  {
    "openclaw":
      {
        "emoji": "⚖️",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "openai requests pypdf2 docx2txt",
              "label": "Install Legal dependencies (uv)",
            },
          ],
      },
  }
---

# Legal Services AI Agents

AI-powered automation for law firms, legal departments, and legal service providers.

## Available Agents

### 1. Contract Review Agent
Automated contract analysis, clause extraction, risk identification, and redlining suggestions.

### 2. Legal Research Agent
Natural language legal queries, case law search, citation verification, and research memo generation.

### 3. Document Automation Agent
Template-based document generation with AI-powered clause selection and e-signature integration.

### 4. Case Management Agent
Case intake, deadline tracking, court filing automation, and time tracking.

### 5. Discovery Assistant Agent
E-discovery processing, AI-powered document classification, privilege review, and redaction automation.

## Quick Start

```bash
cd industries/legal
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."
export CLIO_API_KEY="..."          # Practice management
export DOCUSIGN_KEY="..."          # E-signatures

cd agents/contract-review-agent
python scripts/contract_agent.py review --file contract.pdf
```

## Sample Workflow

```python
from legal.agents import ContractReviewAgent

agent = ContractReviewAgent()
analysis = agent.review_contract("vendor_agreement.pdf")

# Returns: document_type, parties, term, risks with severity,
# missing clauses, key dates, and redline suggestions
```

## Integrations

- **Practice Management**: Clio, MyCase, PracticePanther
- **Legal Research**: Westlaw, LexisNexis, Casetext
- **Document Management**: NetDocuments, iManage
- **E-Signatures**: DocuSign, Adobe Sign
- **E-Discovery**: Relativity, Everlaw, Logikcull

## Ethics & Compliance

- Attorney-client privilege protection
- ABA Model Rule 1.1 technology competence
- Human review of all AI outputs required
- Audit logging of all access
- Bias detection and mitigation
