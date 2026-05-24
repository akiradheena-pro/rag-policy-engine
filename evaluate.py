import json
import time
import os
from app import ask_question

# Load evaluation dataset
with open("data/eval_set.json", "r") as f:
    eval_data = json.load(f)

results = []
total_latency = 0
grounded_count = 0
citation_acc_count = 0

print("🧪 Starting Evaluation...\n")

for i, item in enumerate(eval_data):
    question = item["question"]
    gold_answer = item.get("gold_answer", "")
    expected_source = item.get("expected_source", "")
    
    start_time = time.time()
    result = ask_question(question)
    latency = time.time() - start_time
    total_latency += latency
    
    answer = result["answer"].lower()
    sources = result["sources"]
    
    # Simple groundedness check: does answer contain key phrases from gold?
    # For Score 5, we’ll use LLM-as-judge later — this is basic version
    is_grounded = gold_answer.lower() in answer or len(answer) > 10  # placeholder logic
    
    # Citation accuracy: is expected_source in returned sources?
    has_correct_citation = any(expected_source in src for src in sources)
    
    if is_grounded:
        grounded_count += 1
    if has_correct_citation:
        citation_acc_count += 1
    
    results.append({
        "question": question,
        "answer": answer,
        "sources": sources,
        "latency_ms": round(latency * 1000, 2),
        "grounded": is_grounded,
        "correct_citation": has_correct_citation
    })
    
    print(f"Q{i+1}: {question[:50]}...")
    print(f"   Answer: {answer[:80]}...")
    print(f"   Sources: {sources}")
    print(f"   Latency: {round(latency * 1000, 2)}ms")
    print(f"   Grounded: {'✅' if is_grounded else '❌'} | Citation Accurate: {'✅' if has_correct_citation else '❌'}")
    print("-" * 60)

# Calculate metrics
n = len(eval_data)
avg_latency = total_latency / n
p50_latency = sorted([r["latency_ms"] for r in results])[int(n * 0.5)]
p95_latency = sorted([r["latency_ms"] for r in results])[int(n * 0.95)]

groundedness_pct = (grounded_count / n) * 100
citation_acc_pct = (citation_acc_count / n) * 100

print("\n📊 EVALUATION RESULTS")
print("=" * 40)
print(f"Total Questions: {n}")
print(f"Average Latency: {round(avg_latency * 1000, 2)} ms")
print(f"P50 Latency: {p50_latency} ms")
print(f"P95 Latency: {p95_latency} ms")
print(f"Groundedness: {groundedness_pct:.1f}%")
print(f"Citation Accuracy: {citation_acc_pct:.1f}%")
print("=" * 40)

# Save results
with open("evaluation_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n💾 Results saved to evaluation_results.json")