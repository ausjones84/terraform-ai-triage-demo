"""
analyzer.py — Core analysis engine for the Terraform AI Triage tool.

Accepts raw error text and returns a structured analysis result by
matching against the rule set defined in rules.py.

Design:
  - Pattern matching is case-insensitive substring search.
  - Rules are evaluated in order; the first high-confidence match wins.
  - If multiple rules partially match, a scoring system selects the best.
  - A fallback generic rule is always returned if nothing else matches.
"""

from __future__ import annotations

from typing import Any

from rules import RULES


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze(error_text: str) -> dict[str, Any]:
    """
    Analyse error_text and return a structured result dict.

    Returns
    -------
    dict with keys:
        rule_id, category, title, confidence,
        what, why, next_steps, enterprise, raw_input
    """
    if not error_text or not error_text.strip():
        return _empty_result()

    normalised = error_text.lower()
    best_rule, best_score = _find_best_rule(normalised)

    return {
        "rule_id":    best_rule["id"],
        "category":   best_rule["category"],
        "title":      best_rule["title"],
        "confidence": _compute_confidence(best_rule, best_score),
        "what":       best_rule["what"],
        "why":        best_rule["why"],
        "next_steps": best_rule["next_steps"],
        "enterprise": best_rule["enterprise"],
        "raw_input":  error_text.strip(),
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _find_best_rule(normalised_text: str) -> tuple[dict, int]:
    """
    Score every rule against normalised_text and return the best match.
    Score = number of patterns from the rule that appear in the text.
    The generic fallback rule is used only when score == 0 for all others.
    """
    best_rule  = RULES[-1]   # fallback
    best_score = 0

    for rule in RULES[:-1]:   # exclude generic fallback from scoring loop
        score = sum(
            1 for pattern in rule["patterns"]
            if pattern.lower() in normalised_text
        )
        if score > best_score:
            best_score = score
            best_rule  = rule

    return best_rule, best_score


def _compute_confidence(rule: dict, score: int) -> str:
    """
    Override the rule's default confidence based on pattern match density.
    """
    if rule["id"] == "generic_terraform_error":
        return "Low"
    if score >= len(rule["patterns"]):
        return "High"
    if score >= max(1, len(rule["patterns"]) // 2):
        return rule.get("confidence", "Medium")
    return "Medium"


def _empty_result() -> dict[str, Any]:
    return {
        "rule_id":    "no_input",
        "category":   "No Input",
        "title":      "No Error Text Provided",
        "confidence": "N/A",
        "what":       "No error text was submitted for analysis.",
        "why":        "Please paste a Terraform or Azure error message into the input box.",
        "next_steps": ["Paste your error output into the input area and click Analyse."],
        "enterprise": "",
        "raw_input":  "",
    }
