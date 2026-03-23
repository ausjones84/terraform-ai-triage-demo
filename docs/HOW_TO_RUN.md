# How to Run Locally

## Prerequisites

- Python 3.9 or higher
- pip

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/ausjones84/terraform-ai-triage-demo.git
cd terraform-ai-triage-demo
```

---

## Step 2 — Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You will see `(venv)` in your terminal prompt when it is active.

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — the web UI framework
- `pytest` — for running unit tests

---

## Step 4 — Run the Application

```bash
streamlit run app/main.py
```

Streamlit will print a local URL. Open it in your browser:

```
Local URL:  http://localhost:8501
Network URL: http://192.168.x.x:8501
```

---

## Step 5 — Run the Tests (Optional)

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_analyzer.py::TestEmptyInput::test_empty_string_returns_no_input PASSED
tests/test_analyzer.py::TestUnsupportedArgument::test_basic_match PASSED
...
13 passed in 0.42s
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `streamlit: command not found` | Make sure your virtual environment is active |
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| Port 8501 already in use | Run `streamlit run app/main.py --server.port 8502` |
| Tests fail with ImportError | Ensure you run pytest from the repo root: `pytest tests/ -v` |
