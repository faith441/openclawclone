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

## Quick Deploy

```bash
$ openclaw deploy --agent legal-bot
✓ Agent "legal-bot" is live and running
Connected: Clio, Westlaw, DocuSign, NetDocuments
```

OpenClaw skips all the complexity.

- You don't need to manage servers.
- You don't need to configure legal research APIs manually.
- You don't need to debug agent behavior.
- It just works. 24/7.

## Usage

```bash
# Install the skill
$ openclaw skills install legal-agents
✓ Installed legal-agents v1.0.0

# Review a contract for risks
$ openclaw run contract-agent review --file vendor_agreement.pdf
✓ Document type: Vendor Services Agreement
✓ Parties: Acme Corp, XYZ Services LLC
✓ Term: 3 years
✓ Risks found: 2 HIGH, 3 MEDIUM
✓ Missing clauses: Force Majeure, GDPR Compliance
✓ Redline suggestions generated
✓ Report saved: contract_review_report.pdf

# Legal research query
$ openclaw run research-agent query "standard of care for attorneys in California"
✓ Query analyzed
✓ 12 relevant cases found
✓ 3 statutes identified
✓ Research memo generated
✓ Citations verified

# Generate legal document
$ openclaw run document-agent create --type NDA --parties "Company A, Company B"
✓ Template selected: Mutual NDA
✓ Parties populated
✓ Clauses customized (AI)
✓ Document generated: NDA_CompanyA_CompanyB.docx
✓ Sent for e-signature via DocuSign
```

## Available Agents

| Agent | What it does |
|-------|--------------|
| `contract-agent` | Contract analysis, risk identification, redlining |
| `research-agent` | Case law search, citation verification, memo generation |
| `document-agent` | Template-based document generation, e-signatures |
| `case-agent` | Case intake, deadline tracking, court filings |
| `discovery-agent` | E-discovery processing, document classification, privilege review |

## Integrations

- **Practice Management**: Clio, MyCase, PracticePanther
- **Legal Research**: Westlaw, LexisNexis, Casetext
- **Document Management**: NetDocuments, iManage
- **E-Signatures**: DocuSign, Adobe Sign
- **E-Discovery**: Relativity, Everlaw, Logikcull

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."           # Required
export CLIO_API_KEY="..."                # Practice management
export DOCUSIGN_KEY="..."                # E-signatures
export WESTLAW_API_KEY="..."             # Legal research (optional)
```
