# Xanadu Specification

Formal specification of the Xanadu hypertext system (udanax-green), derived from Ted Nelson's design intent (Literary Machines) and Roger Gregory's implementation (udanax-green C source).

## Pipeline

ASN production follows a four-step pipeline:

1. **Questions** — Decompose inquiry into focused sub-questions for Nelson and Gregory
2. **Consult** — Run all expert consultations in parallel
3. **Discover** — Synthesize consultation answers into a formal ASN
4. **Commit** — Commit vault changes

```
python scripts/run-asn.py --inquiries 4 questions    # preview sub-questions
python scripts/run-asn.py --inquiries 4 consult      # questions + consultations
python scripts/run-asn.py --inquiries 4 discover     # consult + discover
python scripts/run-asn.py --inquiries 4              # full pipeline
```

## Scripts

| Script | Purpose |
|--------|---------|
| `run-asn.py` | Pipeline runner — steps up to the specified target |
| `consult-experts.py` | Decompose inquiry into sub-questions, run all consultations |
| `discover.py` | Synthesize expert consultation answers into a formal ASN |
| `consult-nelson.py` | Nelson consultation — design intent from Literary Machines |
| `consult-gregory.py` | Gregory consultation — KB synthesis + code exploration in parallel |
| `extract-vocab.py` | Extract structural conventions from finalized ASNs |

## Prompt Templates

| Template | Used by | Purpose |
|----------|---------|---------|
| `discovery.md` | `discover.py` | Discovery agent — Dijkstra-style ASN writing |
| `nelson-questions.md` | `consult-experts.py` | Generate Nelson sub-questions from inquiry |
| `gregory-questions.md` | `consult-experts.py` | Generate Gregory sub-questions from inquiry + KB |
| `nelson-agent.md` | `consult-nelson.py` | Nelson answering agent |
| `gregory-synthesis-agent.md` | `consult-gregory.py` | Gregory KB synthesis agent |
| `gregory-code-agent.md` | `consult-gregory.py` | Gregory code exploration agent |

## Directory Structure

```
vault/
  asns/           — Abstract Specification Notes (ASN-NNNN-title.md)
  consultations/  — Orchestrated consultation output (answers.md per ASN)
  transcripts/    — Individual agent call logs (Nelson/Gregory subagent runs)
  reviews/        — Review outputs
  inquiries.yaml  — Inquiry definitions driving ASN production
  vocabulary.md   — Shared vocabulary for ASN authors

scripts/          — Pipeline and consultation scripts
  prompts/        — Prompt templates for all agents

resources/        — Source materials (Literary Machines, Nelson's notes, concept maps)

udanax-test-harness/  — Test harness for udanax-green (golden tests, findings, KB)
```
