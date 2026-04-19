# Scoped Inquiry

## Pattern

A complex question asked broadly produces shallow answers. An agent given "analyze this system" returns surface observations. The question is too large for the context to focus on.

Decompose the question along authority boundaries. One line of questioning targets what should be true — the claims, guarantees, and purpose of the system. Another targets how it works — the mechanisms, internals, and observed behavior. Each line is scoped to what that authority is qualified to evaluate. Neither line crosses into the other's territory.

The decomposition is not splitting the question in half. It is translating one question into two different investigations that approach the same subject from directions that cannot contaminate each other.

## Forces

- **Broad questions get broad answers.** "Analyze this" produces observations scattered across purpose, mechanism, history, and speculation. Nothing goes deep.
- **Authorities have different competencies.** A theory authority reasons about guarantees and constraints. An evidence authority reasons about implementation and behavior. Asking either to do the other's job produces weak results.
- **Scope creates depth.** Ten targeted questions about guarantees produce deeper findings than one open question about everything. The constraint forces the authority to exhaust what it knows within its scope.
- **Cross-contamination destroys independence.** If the theory channel is asked about implementation details, it speculates. If the evidence channel is asked about design intent, it infers. Both produce plausible but ungrounded answers. Scoping prevents this.

## Structure

```
one question
  │
  ├──→ theory scope: what, why, what guarantees
  │      → 10 targeted sub-questions
  │      → theory authority responds
  │
  ├──→ evidence scope: how, what internals, what behavior
  │      → 10 targeted sub-questions
  │      → evidence authority responds
  │
  └──→ synthesis: 20 responses → consultation report
```

The sub-questions are designed, not generated. Each one extracts a specific piece of the answer that the authority is qualified to give. The synthesis sees all responses and constructs what no single response contains.

## Enables

[Two data authorities](two-data-authorities.md) — scoped inquiry is how you operate the two-authority architecture effectively. Without it, two data authorities degrades to asking two agents the same vague question and hoping they disagree productively. With it, each authority investigates what it's qualified to evaluate, and the disagreements are meaningful.

## When it works

- The question is complex enough that a single investigation misses significant dimensions
- The authority boundaries map to real differences in evidence (design documents vs source code, specifications vs test results, theory vs observation)
- The sub-questions are specific enough to exhaust the authority's knowledge within its scope

## When it fails

- The sub-questions are too broad — they reproduce the original problem at smaller scale
- The authority boundaries are artificial — both channels have access to the same evidence
- The synthesis treats responses as independent facts rather than looking for agreement and disagreement

## Applications

### ASN discovery consultation

**One question**: "What are the claims of document arrangement in the Xanadu system?"

**Theory scope** (Nelson's design): What guarantees does the arrangement provide? What invariants must hold across state transitions? What is the purpose of separating content from arrangement? What constraints does permanence impose? What does "transclusion" require of the arrangement model?

**Evidence scope** (Gregory's implementation): How does the FEBE protocol modify arrangements? What data structures represent M(d)? How do editing commands (INSERT, DELETE, REARRANGE, COPY) operate on arrangement state? What invariants does the code maintain? What edge cases does the implementation handle?

**Synthesis**: produces ASN-0036 (Strand Model) with 29 claims — each traced to theory, evidence, or both. The arrangement functionality invariant (S2) came from theory. The V-position well-formedness constraint (S8a) came from evidence. The two-stream separation (S9) emerged from the disagreement between what theory requires (immutability) and what the implementation provides (which editing commands exist).

## Origin

Discovered during the first discovery runs. Initial attempts asked each authority a single broad question about the topic. The responses were shallow and overlapping — both channels said similar things at a surface level. Restructuring the inquiry into targeted sub-questions scoped to each authority's evidence base transformed the quality of findings. The disagreements became specific and actionable rather than vague and interpretive.
