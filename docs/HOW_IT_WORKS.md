# How It Works

## Architecture Overview

```
User Input (Streamlit UI)
        │
        ▼
  analyzer.py — analyze(error_text)
        │
        ▼
  rules.py — RULES list
  (pattern matching loop)
        │
        ▼
  Best-match rule selected
        │
        ▼
  Structured result dict returned to UI
        │
        ▼
  Streamlit renders 6 labelled sections
```

---

## Component Breakdown

### `app/main.py` — Streamlit UI

The front-end. It:
1. Renders a two-column layout (input left, results right)
2. Loads sample errors from `sample_inputs.py` into a dropdown
3. Passes pasted or selected error text to `analyzer.py`
4. Renders the result as six colour-coded HTML sections

No business logic lives here — it is purely presentation.

---

### `app/analyzer.py` — Analysis Engine

The core logic. The `analyze()` function:

1. **Normalises** the input (strips whitespace, lowercases)
2. **Scores** each rule in `RULES` by counting how many of the rule's patterns appear in the text
3. **Selects** the highest-scoring rule
4. **Computes confidence** based on score vs. total patterns in the rule
5. **Returns** a structured dict with all display fields populated

The generic fallback rule is only used if no other rule scores above zero.

---

### `app/rules.py` — Rule Definitions

A flat list of rule dictionaries. Each rule contains:

| Field | Purpose |
|---|---|
| `id` | Unique identifier |
| `category` | High-level error category |
| `patterns` | Substrings to match (case-insensitive) |
| `title` | Short display heading |
| `what` | Plain-English description of what happened |
| `why` | Root cause explanation |
| `next_steps` | Ordered list of recommended actions |
| `enterprise` | Enterprise-specific context (pipeline, RBAC, etc.) |
| `confidence` | Default confidence level |

Rules are evaluated in order. The first rule with the highest pattern match score wins.

---

### `app/sample_inputs.py` — Demo Samples

A list of 9 pre-loaded real-world error strings. These are displayed in a dropdown so a demo presenter can instantly show any scenario without typing.

---

### `tests/test_analyzer.py` — Unit Tests

Pytest tests that verify:
- Empty input returns the correct no-input result
- Each major error category is correctly identified
- All result dicts contain the required keys
- Next steps is always a non-empty list

---

## Why Pattern Matching (Not an LLM)?

This version uses deterministic pattern matching because:

1. **No API key required** — runs fully offline, instantly
2. **Predictable output** — every input produces the same result every time
3. **Fast** — sub-millisecond analysis
4. **Auditable** — every decision can be traced to a specific rule

The `analyze()` function signature is intentionally simple — it can be replaced with an LLM call (Azure OpenAI, OpenAI API) by swapping the internals of `analyzer.py` without changing the UI or tests.

---

## Adding New Rules

Add a new dict to the `RULES` list in `rules.py`. The analyzer picks it up automatically — no other changes required.

Keep rules ordered from most specific to least specific. The generic fallback rule must always be last.
