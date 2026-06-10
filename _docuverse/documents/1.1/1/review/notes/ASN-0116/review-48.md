# Review of ASN-0116

I worked through the composite decomposition, the coupling discharge, all four named invariants, the boundary cases, and the worked example. The technical content is sound: the K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n) sequence is correctly exhibited as a valid composite (per-step preconditions discharged at the right intermediate states, J0/J1★/J1'★ discharged initial-to-final), the block-disjointness argument correctly partitions left/block/shifted-suffix so I3's gapped values transfer without overwriting the block fill, the range identity RAN correctly isolates `A_new` as the only range-new content so the provenance couplings hold, and IP4/IP6 derive the genuinely non-obvious facts (witness V-position sets are *not* simply ordered; discoverability preservation is a containment, not an emptiness). The append, empty-subspace (both first-emission and re-insertion-after-clearance), and front-insertion (`n'_{s_C}=0` strict contraction) boundaries are each walked concretely. I found no correctness defect.

## REVISE

### Issue 1: Precondition-discharge prose is duplicated between the Effect/allocation sections and the valid-composite section

**ASN-0116, "What shifts…" (clause I-PROV) vs. "INSERT as a valid composite…" (the K.ρ step):**

I-PROV: "Each K.ρ step's precondition `shift(a, k) ∈ dom(C') ∧ d ∈ E_doc` is met: `shift(a, k)` is in the store the moment its K.α step commits it, and `d ∈ dom(M) = E_doc` by precondition."

Valid-composite K.ρ step: "its precondition `shift(a, k) ∈ dom(C') ∧ d ∈ E_doc` holds because `shift(a, k)` entered the store at its K.α step and `d ∈ dom(M) = E_doc`."

**Problem**: These discharge the same K.ρ precondition with the same two reasons, in different words. The pattern recurs:
- K.α freshness is argued once in "What is allocated, and why it must be fresh" ("FirstEmissionFreshness … and SubsequentEmissionFreshness … discharge `a ∉ dom(C) ∪ dom(L)`") and again, more completely, in the valid-composite K.α step (the full first/subsequent/k≥1 split). The first occurrence re-proves what the second proves in full.
- The equation `d ∈ dom(M) = E_doc` is re-derived at nearly every step.

ValidComposite★ clause 1 makes the valid-composite section the *authoritative* place for these per-step discharges; the inline copies in the Effect/allocation prose restate it. Under the active anti-bloat directive this is the "two paragraphs say the same thing in different words" pattern — a reader must reconcile two discharges of one obligation.

**Required**: Have the Effect clauses state their postconditions and name the K-atomic, deferring achievability to the valid-composite section with a single pointer; have "What is allocated" introduce K.α's freshness mechanism (and its `findpreviousisagr` grounding, which *is* distinct content) without re-proving the branch split. Discharge each precondition once.

## OUT_OF_SCOPE

The Open Questions correctly fence off the new territory — insertion at a transclusion-shared position, concurrent-insertion freshness without a serializing authority, transclusion provenance, and post-edit fragmentation of the inserted run. These belong to transclusion (ASN-0118) and the concurrency model, not here. The in-text mentions of sharing (IP5) and link resurrection (IP4) stay within INSERT's own obligations and do not stray into defining those operations. Nothing to add.

VERDICT: REVISE
