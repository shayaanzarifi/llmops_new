import time, requests, statistics as stats

BASE = "http://127.0.0.1:8000"
CASES = [
    ("What is this project about?", False),
    ("Summarise this project.", False),
    ("How do I contact you? Give me an email.", True),
    ("Which file is used as the intro?", False),
]

def call(query: str):
    r = requests.get(f"{BASE}/ask", params={"query": query}, timeout=10)
    r.raise_for_status()
    return r.json()

def main():
    latencies = []
    correct_refusals = 0
    answered = 0
    for q, should_refuse in CASES:
        t0 = time.perf_counter()
        j = call(q)
        t1 = time.perf_counter()
        lat = (t1 - t0) * 1000
        latencies.append(lat)
        if j["refused"] == should_refuse:
            if should_refuse:
                correct_refusals += 1
            else:
                answered += 1
        print(f"Q: {q}\n  refused={j['refused']} source={j['source']} latency={lat:.1f}ms trace_id={j['trace_id']}\n")
    print(f"Accuracy (answers): {answered}/{len([c for c in CASES if not c[1]])}")
    print(f"Refusals (correct): {correct_refusals}/{len([c for c in CASES if c[1]])}")
    print(f"Avg latency: {stats.mean(latencies):.1f} ms")

if __name__ == "__main__":
    main()
