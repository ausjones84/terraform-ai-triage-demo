# Demo Talk Track

> **Time:** 3-5 minutes
> **Audience:** Engineering team
> **Format:** Screen share with live app running at http://localhost:8501

---

## Before You Start

1. Run `streamlit run app/main.py` and have the browser open
2. Have the repo open in your editor to show code if asked
3. The app should show the two-column layout with the sample dropdown visible

---

## Opening (30 seconds)

> "So — we all know what it feels like when a Terraform plan fails in a pipeline at 4pm.
> You have got an error message, you are not sure if it is your code, a permission issue,
> or something the platform team needs to fix. You spend 20 minutes in docs and Slack.
>
> I built this to show what it would look like if we had a tool that instantly triages
> those errors and gives us the right context — including enterprise-specific context
> that generic documentation does not have."

---

## Demo — Step 1: Provider Schema Error (45 seconds)

1. In the dropdown, select: **"2 · Invalid location on azurerm_monitor_metric_alert"** (Sample 2)
2. Click **Analyse Error**

> "Here — an engineer has hit an 'unsupported argument' error. They added a location
> field to a metric alert resource because they copied it from a VM template.
> The tool immediately classifies this as a Provider Schema Issue, confidence: High.
>
> It explains in plain English what happened, why it happened — metric alerts are global
> resources, they do not have a location — and gives exact next steps.
>
> And critically — the Enterprise Context section explains that if this is in a shared
> vm-alerts module, you need to update the module and notify all environments.
> That is the kind of thing that lives in someone's head, not in the Terraform docs."

---

## Demo — Step 2: 403 AuthorizationFailed (45 seconds)

1. Select: **"6 · 403 AuthorizationFailed"** (Sample 6)
2. Click **Analyse Error**

> "Here is one we have all seen. 403 AuthorizationFailed when running terraform apply.
>
> The standard response is 'fix your permissions.' But the enterprise context here
> says something more nuanced: in our environment, this error is EXPECTED for prd and dmz.
> Engineers do not run applies directly — that is the pipeline's job.
>
> So instead of spending an hour chasing an Azure admin, an engineer now knows within
> seconds: 'I should not be running this locally at all. I need to trigger the pipeline.'
>
> That is the difference between a generic tool and one that understands how we work."

---

## Demo — Step 3: State Lock (45 seconds)

1. Select: **"8 · State blob already locked"** (Sample 8)
2. Click **Analyse Error**

> "State locking errors are stressful because the instinct is to immediately force-unlock.
>
> The tool shows the Lock ID, explains why the lock exists, and — importantly — puts
> a warning in the next steps: only force-unlock if you are certain no pipeline is
> currently writing to state. In shared environments, a premature force-unlock during
> an active apply can corrupt the state file.
>
> The enterprise note tells the engineer to co-ordinate with the DevOps team first.
> That is the kind of guardrail that prevents real incidents."

---

## Architecture Slide (30 seconds)

> "Under the hood — it is intentionally simple. Three Python files.
>
> rules.py holds the pattern library. Each rule has the patterns to match,
> and the full explanation including enterprise context.
>
> analyzer.py scores each rule against the input and picks the best match.
>
> main.py is the Streamlit UI — it is about 80 lines.
>
> No API keys. No cloud dependency. Runs entirely locally.
>
> The key design decision: the analyze() function signature is simple enough that
> we could swap the pattern matching for an Azure OpenAI call without changing the UI
> or the tests. That is the natural next step."

---

## Closing (30 seconds)

> "What I want to show with this is the workflow, not just the code.
> We identify common failure modes, we encode enterprise context alongside them,
> and we surface it at the point of failure — not in a wiki page nobody reads.
>
> A production version integrated into our pipelines could triage errors automatically
> during failed runs, post the analysis to a Teams channel, or surface it in the ADO
> build summary.
>
> The repo is here — happy to walk through any of the code, or talk about
> how we would extend this for production use."

---

## Questions You Might Get

**"What about errors this does not recognise?"**
> The generic fallback still gives basic guidance. Adding new rules takes about
> 10 lines of Python — we can grow the library with the team's most common errors.

**"Could this connect to our actual Terraform state?"**
> Yes — with the right service principal permissions on the state storage account,
> we could pull live state context to make the analysis even more specific.

**"Could this run in Azure?"**
> Yes — see docs/HOW_TO_DEPLOY_TO_AZURE.md. Azure Container Apps is the
> recommended target. It could also be a pipeline step that auto-triages on failure.

**"Why not just use ChatGPT?"**
> This is deterministic — every input produces the same, auditable output.
> It has enterprise context baked in, not generic documentation.
> And it runs without an internet connection or API key.
> LLM integration is the natural evolution, not the starting point.
