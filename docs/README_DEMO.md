# Demo Guide — terraform-ai-triage-demo

## What This Demo Shows

A working AI-assisted Terraform error triage tool that:
- Classifies Terraform and Azure errors into specific categories
- Returns plain-English explanations with enterprise-specific context
- Runs entirely locally with no API keys or cloud connectivity

**Target audience:** Engineering team
**Demo duration:** 3-5 minutes
**Pre-requisite:** App running at http://localhost:8501

---

## Before the Demo — Setup Checklist

```bash
cd terraform-ai-triage-demo
source venv/bin/activate
streamlit run app/main.py
```

- [ ] Browser is open at http://localhost:8501
- [ ] App shows two-column layout
- [ ] Sample dropdown is visible
- [ ] Repo open in editor (optional, for code questions)

---

## Demo Flow — 5 Steps

### Step 1 — Introduce the tool (30 sec)

Point to the UI and explain the problem it solves.
See `DEMO_TALK_TRACK.md` for the exact script.

---

### Step 2 — Show Sample 2: Provider Schema Error

**Dropdown:** "2 · Invalid location on azurerm_monitor_metric_alert"
**Click:** Analyse Error

**Point out:**
- Category: Provider Schema Issue
- Confidence: High
- Enterprise context section — module update required, notify all envs

---

### Step 3 — Show Sample 6: 403 AuthorizationFailed

**Dropdown:** "6 · 403 AuthorizationFailed"
**Click:** Analyse Error

**Point out:**
- Enterprise context: This error is EXPECTED in prd — pipeline handles this
- Next steps guide the engineer away from chasing permissions

---

### Step 4 — Show Sample 8: State Blob Locked

**Dropdown:** "8 · State blob already locked"
**Click:** Analyse Error

**Point out:**
- Lock ID referenced in next steps
- Warning: co-ordinate before force-unlocking
- Prevents a real incident in shared environments

---

### Step 5 — Paste a Custom Error

Clear the input and paste any real Terraform error from your environment.

**Shows:** The tool works on errors not in the sample list.

---

## Code Tour (Optional — 2 min)

```
app/rules.py     — show one rule dict, explain fields
app/analyzer.py  — show the _find_best_rule() function
app/main.py      — show it is ~80 lines, mention Streamlit
```

---

## Key Talking Points

1. **Deterministic** — same input = same output, every time, auditable
2. **Enterprise context embedded** — not just docs, but how WE work
3. **Extensible** — new rules are 10 lines of Python
4. **LLM-ready** — analyzer.py is a clean interface to swap later
5. **Pipeline-ready** — could auto-triage on failed runs

---

## Full Talk Track

See `docs/DEMO_TALK_TRACK.md` for word-for-word script.
