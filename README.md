# 🔧 terraform-ai-triage-demo

> **An AI-powered Terraform + Azure error triage assistant built for enterprise DevOps workflows.**

---

## Why This Was Built

Enterprise Terraform deployments fail in predictable ways. Engineers lose time context-switching to documentation, Slack threads, and GitHub issues to diagnose errors that follow well-known patterns.

This tool demonstrates how a lightweight AI assistant — with embedded enterprise context — can be used to:

- Instantly classify Terraform and Azure errors
- Explain errors in plain English with **why** they happened
- Provide **actionable next steps** without ambiguity
- Surface **enterprise-specific context** (e.g. "this 403 is expected — your pipeline handles state, not you")

Built to show engineering teams what AI-assisted DevOps tooling can look like before committing to a full LLM integration.

---

## Features

| Feature | Details |
|---|---|
| Error classification | 9 specific categories + generic fallback |
| Enterprise context | Explains RBAC, backend restrictions, pipeline patterns |
| Sample error library | 9 pre-loaded real-world errors for demos |
| Structured output | What / Why / Next Steps / Category / Enterprise / Action |
| Confidence scoring | High / Medium / Low based on match depth |
| Clean Streamlit UI | Two-column layout, colour-coded sections |
| Fully local | No API keys, no cloud dependency to run |

---

## Supported Error Categories

- ✅ Terraform code issues (unsupported arguments, missing required args)
- ✅ Variable / input format issues (type mismatches)
- ✅ Module wiring issues (action_group_id not passed)
- ✅ Provider schema issues (location on metric alert)
- ✅ Backend / state issues (locked blobs, access denied)
- ✅ Azure CLI / auth issues (az not installed)
- ✅ Azure RBAC / permission issues (403 AuthorizationFailed)

---

## Folder Structure

```
terraform-ai-triage-demo/
├── app/
│   ├── main.py           # Streamlit UI
│   ├── analyzer.py       # Core analysis engine
│   ├── rules.py          # Error pattern rules + enterprise context
│   └── sample_inputs.py  # Pre-loaded demo errors
├── docs/
│   ├── README_DEMO.md         # Step-by-step demo guide
│   ├── HOW_IT_WORKS.md        # Architecture explanation
│   ├── HOW_TO_RUN.md          # Install + run commands
│   ├── HOW_TO_DEPLOY_TO_AZURE.md  # Azure deployment path
│   ├── DEMO_TALK_TRACK.md     # Exact script for demos
│   └── SAMPLE_OUTPUTS.md      # Example outputs for common errors
├── tests/
│   └── test_analyzer.py  # Pytest unit tests
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/ausjones84/terraform-ai-triage-demo.git
cd terraform-ai-triage-demo

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate.bat    # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run Locally

```bash
streamlit run app/main.py
```

The app opens at **http://localhost:8501** in your default browser.

---

## How to Run Tests

```bash
pytest tests/ -v
```

---

## Example Input / Output

**Input:**
```
Error: Unsupported argument

  on modules/vm-alerts/main.tf line 8, in resource "azurerm_monitor_metric_alert" "cpu":
  8:   location = var.location

An argument named "location" is not expected here.
```

**Output summary:** Category: Provider Schema Issue | Confidence: High | Root cause: metric alerts are global resources, location is not accepted | Enterprise context: update shared module and notify all environment consumers.

See `docs/SAMPLE_OUTPUTS.md` for full examples.

---

## Enterprise Terraform Relevance

This tool is built around real enterprise patterns:

| Pattern | How the tool handles it |
|---|---|
| `modules/` = reusable infrastructure | Module wiring errors are a distinct category |
| `terraform-scripts/dev,prd,dmz` = environments | Error messages reference env-specific paths |
| Remote state in Azure Storage | Backend access errors include storage-specific guidance |
| Engineers ≠ pipeline service principals | RBAC errors flag whether the error is expected |
| Module outputs feed other modules | action_group → vm-alerts wiring is a named pattern |

---

## Future Azure Deployment Path

This application can be containerised and deployed to:

- **Azure Container Apps** (recommended — serverless, scales to zero)
- **Azure App Service** (simpler, familiar to teams already using App Service)

See `docs/HOW_TO_DEPLOY_TO_AZURE.md` for full deployment architecture.

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Analysis engine | Python (pattern matching) |
| Tests | Pytest |
| Future LLM integration | Azure OpenAI / OpenAI API (drop-in replacement for analyzer.py) |

---

## Extending This Tool

To add a new error pattern, add a rule to `app/rules.py`:

```python
{
    "id":         "your_new_rule",
    "category":   "Terraform Code Issue",
    "patterns":   ["phrase to match", "another phrase"],
    "title":      "Short display title",
    "what":       "Plain English description of what happened.",
    "why":        "Plain English root cause explanation.",
    "next_steps": ["Step one.", "Step two."],
    "enterprise": "Enterprise-specific context note.",
    "confidence": "High",
}
```

---

*terraform-ai-triage-demo · Internal DevOps Tooling Demo · ausjones84*
