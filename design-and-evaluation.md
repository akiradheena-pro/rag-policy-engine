# Design and Evaluation Report

## Architecture Choices

### Embedding Model: all-MiniLM-L6-v2

- Free, runs locally via HuggingFace Transformers
- Fast enough for small corpus (<20 docs)
- No API key needed → reproducible across environments

### Vector DB: ChromaDB

- Lightweight, persistent local storage
- Easy to set up, no cloud dependency → ideal for grading/demo

...

## Evaluation Approach

We created 5 gold-standard questions covering PTO, expenses, remote work, holidays.

Metrics calculated:

- **Groundedness**: % of answers fully supported by retrieved context → **100%**
- **Citation Accuracy**: % where expected_source appears in returned sources → **100%**
- **Latency**:
  - Average: 9717ms (cold start)
  - P50: 8313ms
  - P95: 16259ms

> *Note: High initial latency due to embedding model download/cache miss. Warm starts show <1s latency.*

Results stored in `evaluation_results.json`.

## Ablations (Optional)

Tested:

- k=2 vs k=3 → k=3 gave better coverage without introducing irrelevant chunks.
- Chunk size 300 vs 500 → 500 preserved more context without exceeding token limits.
