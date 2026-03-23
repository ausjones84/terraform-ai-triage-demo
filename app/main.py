"""
main.py — Streamlit front-end for the Terraform AI Triage Demo.

Run with:
    streamlit run app/main.py

The UI provides:
  - A sample error dropdown for demos
  - A free-text input area for pasting real errors
  - A structured output panel with six clearly labelled sections
"""

import streamlit as st

from analyzer import analyze
from sample_inputs import SAMPLES

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Terraform AI Triage",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Styling — minimal, professional
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .section-box {
            background: #f8f9fa;
            border-left: 4px solid #0078d4;
            padding: 0.8rem 1rem;
            border-radius: 4px;
            margin-bottom: 0.8rem;
        }
        .section-box.green  { border-left-color: #107c10; }
        .section-box.orange { border-left-color: #ca5010; }
        .section-box.purple { border-left-color: #5c2d91; }
        .section-box.grey   { border-left-color: #605e5c; }
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .badge-high   { background:#dff6dd; color:#107c10; }
        .badge-medium { background:#fff4ce; color:#7a3e00; }
        .badge-low    { background:#fde7e9; color:#a80000; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🔧 Terraform AI Triage Assistant")
st.markdown(
    "Paste a Terraform or Azure error below — or pick a sample — and get an "
    "instant structured analysis with enterprise context."
)
st.divider()

# ---------------------------------------------------------------------------
# Layout: two columns
# ---------------------------------------------------------------------------
left_col, right_col = st.columns([1, 1], gap="large")

# Left column: input
with left_col:
    st.subheader("📥 Error Input")

    sample_labels = [s["label"] for s in SAMPLES]
    selected_label = st.selectbox("Load a sample error (for demo):", sample_labels)
    selected_sample = next(s for s in SAMPLES if s["label"] == selected_label)

    default_text = selected_sample["text"]

    error_text = st.text_area(
        "Paste your Terraform / Azure error here:",
        value=default_text,
        height=320,
        placeholder=(
            "Example:\n\nError: Unsupported argument\n\n"
            "  on main.tf line 5:\n  5:   location = var.location\n\n"
            "An argument named \"location\" is not expected here."
        ),
    )

    analyse_btn = st.button("🔍 Analyse Error", type="primary", use_container_width=True)
    clear_btn   = st.button("🗑 Clear", use_container_width=True)

    if clear_btn:
        st.rerun()

# Right column: results
with right_col:
    st.subheader("📊 Analysis Results")

    if analyse_btn and error_text.strip():
        result = analyze(error_text)

        conf = result["confidence"]
        badge_class = {
            "High":   "badge-high",
            "Medium": "badge-medium",
            "Low":    "badge-low",
        }.get(conf, "badge-medium")

        st.markdown(
            f"**Category:** `{result['category']}` &nbsp;&nbsp;"
            f"<span class='badge {badge_class}'>Confidence: {conf}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"### {result['title']}")
        st.divider()

        # What happened
        st.markdown(
            f"<div class='section-box'>"
            f"<strong>🔍 What happened</strong><br>{result['what']}"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Why it happened
        st.markdown(
            f"<div class='section-box orange'>"
            f"<strong>💡 Why it happened</strong><br>{result['why']}"
            f"</div>",
            unsafe_allow_html=True,
        )

        # What to do next
        steps_html = "".join(
            f"<li style='margin-bottom:4px'>{step}</li>"
            for step in result["next_steps"]
        )
        st.markdown(
            f"<div class='section-box green'>"
            f"<strong>✅ What to do next</strong>"
            f"<ol style='margin:0.5rem 0 0 1rem;padding:0'>{steps_html}</ol>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Enterprise context
        if result["enterprise"]:
            st.markdown(
                f"<div class='section-box purple'>"
                f"<strong>🏢 Enterprise context</strong><br>{result['enterprise']}"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Recommended action
        first_step = result["next_steps"][0] if result["next_steps"] else "See steps above."
        st.markdown(
            f"<div class='section-box grey'>"
            f"<strong>⚡ Recommended action</strong><br>{first_step}"
            f"</div>",
            unsafe_allow_html=True,
        )

    elif analyse_btn and not error_text.strip():
        st.warning("Please paste an error message or select a sample before clicking Analyse.")
    else:
        st.info(
            "Select a sample from the dropdown or paste an error on the left, "
            "then click **Analyse Error** to see results here."
        )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.markdown(
    "<small>terraform-ai-triage-demo · Internal DevOps Tooling · "
    "Pattern-matched analysis · Not a replacement for engineer review</small>",
    unsafe_allow_html=True,
)
