from fastapi import FastAPI, Query
from pydantic import BaseModel
from pathlib import Path
import time, uuid, re

app = FastAPI(title="LLMOps Starter - Docs Q&A")

# ----- Models -----
class AskResponse(BaseModel):
    answer: str
    source: str
    latency_ms: float
    refused: bool
    reason: str | None = None
    trace_id: str | None = None

# ----- Load docs at startup -----
DOCS_DIR = Path(__file__).resolve().parents[1] / "data"
DOCS = {}
for p in DOCS_DIR.glob("*.txt"):
    DOCS[p.name] = p.read_text(encoding="utf-8")

# ----- Simple guardrail patterns -----
PII_PATTERN = re.compile(r"\b(email|phone|address|passport|ssn|national\s*insurance)\b", re.I)
CONTACT_SEEK_PATTERN = re.compile(r"\b(contact|reach\s*me|dm\s*me)\b", re.I)

def most_relevant_chunk(query: str) -> tuple[str,str]:
    """Naive retrieval: pick the file with most keyword overlaps."""
    query_terms = set(re.findall(r"\w+", query.lower()))
    best_file, best_score = "intro.txt", -1
    for fname, text in DOCS.items():
        text_terms = set(re.findall(r"\w+", text.lower()))
        score = len(query_terms & text_terms)
        if score > best_score:
            best_file, best_score = fname, score
    return best_file, DOCS[best_file]

@app.get("/ask", response_model=AskResponse, description="Answer a question from local docs. Blocks PII/contact-seeking queries.")
def ask(query: str = Query(..., description="Your question")):
    start = time.perf_counter()
    tid = str(uuid.uuid4())

    # Guardrail: refuse PII or contact-seeking requests
    if PII_PATTERN.search(query) or CONTACT_SEEK_PATTERN.search(query):
        latency = (time.perf_counter() - start) * 1000
        return AskResponse(
            answer="I can't help with that request.",
            source="guardrail",
            latency_ms=latency,
            refused=True,
            reason="PII/contact-like request",
            trace_id=tid,
        )

    doc_id, chunk = most_relevant_chunk(query)
    latency = (time.perf_counter() - start) * 1000
    return AskResponse(
        answer=chunk,
        source=doc_id,
        latency_ms=latency,
        refused=False,
        reason=None,
        trace_id=tid,
    )
