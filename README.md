# LLMOps Starter — Docs Q&A (FastAPI) with Guardrails + Mini-Eval

A tiny FastAPI API that answers questions from local `.txt` files, with a simple guardrail for PII/contact-seeking queries and a per-request `trace_id` for observability. Includes a 4-case mini evaluation (accuracy, latency, refusal rate).

## Run locally

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install --upgrade pip
# If your Python is 3.14, enable the ABI3 compatibility flag before install:
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
pip install -r requirements.txt

# start the API (leave this tab running)
uvicorn app.main:app --reload
Open Swagger UI: http://127.0.0.1:8000/docs
Try GET /ask → Try it out → query: What is this project about? → Execute.
To stop the server: press Ctrl + C in the terminal running Uvicorn.

Mini-evaluation
# Open a second terminal tab in the same folder and activate the venv again:
source .venv/bin/activate
pip install requests
python eval/run_eval.py
This prints something like:

Accuracy (answers): 3/3

Refusals (correct): 1/1

Avg latency: ~8 ms

What’s inside
app/main.py — FastAPI app with /ask, naive retrieval over local text, guardrail regex for PII/contact, latency timing, and trace_id.

data/intro.txt — Sample local text used by the API.

eval/run_eval.py — 4-case evaluation (3 normal, 1 guardrail).

requirements.txt — Locked deps: FastAPI, Uvicorn, Pydantic, Regex.

Troubleshooting
pydantic-core build error on Python 3.14: create a Python 3.12 venv instead:

brew install python@3.12  # macOS
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Quick pitch (for recruiters)

Built a minimal **LLMOps** API that:
- Reads local docs and answers questions (no paid AI needed).
- Enforces a simple **PII/contact guardrail** so risky queries are refused.
- Adds a per-request **trace_id** for observability.
- Ships with a tiny **evaluation harness** (accuracy, latency, refusal rate) so changes can be tested.
