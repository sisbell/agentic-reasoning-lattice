# Review of ASN-0094

## REVISE

### Issue 1: SHCD attachment wording is internally inconsistent

**ASN-0094, "Per-K opt-in registry is partitioned by base shape" paragraph**: "SingleHomeCoverageDiscipline attaches only to the Coverage instantiation of NonIdempotentDirectedPair ((1, 1, A_doc, A_doc, ⊥))."

**ASN-0094, "Mutual exclusion of FDD and SHCD at the same K" paragraph (Gate Ordering)**: "SHCD attaches only to the Coverage instantiation of NonIdempotentDirectedPair, which has idem = ⊥."

vs.

**ASN-0094, "Nelson's design vocabulary on links and semantics" paragraph**: "The structural eligibility for SHCD is exactly the shape (1, 1, A_doc, A_doc, ⊥) (matched in the registry's literal shape tuple) plus the per-K registration of SingleHomeCoverageDiscipline; SHCD does *not* depend on any semantic taxonomy distinguishing 'supersession-style' from 'comment-style' relations."

**Problem**: The "Coverage instantiation" terminology conflates a layer-naming role with the structural attachment criterion. The first two paragraphs read as restricting SHCD to a particular instantiation; the third explicitly admits SHCD at any K of the right shape. Downstream reasoning (Π_K's SHCD implication in EffectiveWpSimplification, the Comment walkthrough's `K_res` parametric framing) depends on which reading is binding.

**Required**: Commit to one reading consistently. Either (a) SHCD is structurally eligible at any (1, 1, A_doc, A_doc, ⊥) K (the Nelson paragraph's reading), in which case "Coverage instantiation" should be replaced throughout with "SHCD-opt-in entry of NonIdempotentDirectedPair", or (b) SHCD is restricted to a Coverage-named layer role, in which case the Nelson paragraph's structural-eligibility claim should be removed.

### Issue 2: "Instantiation" terminology obscures the catalog row structure

**ASN-0094, NonIdempotentDirectedPair walkthrough sections**: The text references "Coverage instantiation" and "Comment instantiation" as if they were exclusive sub-categories of the NonIdempotentDirectedPair row, but the catalog row itself defines them as distinct *opt-in* and *parametric* extensions that can coexist at the same K (a layer K could register SHCD *and* be consumed by `_via` templates from other K's).

**Problem**: "Instantiation" suggests mutual exclusion when the catalog actually admits joint registration. A reader cannot determine from the catalog row alone whether the two "instantiations" partition the K's at this shape or layer atop each other.

**Required**: Replace "instantiation" with a term that reflects the framework's actual structure — "opt-in extension" for the SHCD case and "parametric consumption pattern" for the `_via` case — or state explicitly that the two are jointly registrable at a single K.

## OUT_OF_SCOPE

### Topic 1: Shape combinations not enumerated

**Why out of scope**: The catalog enumerates (0,1), (1,1), (\*,1), (1,\*), and (1, 0|1) but not (\*,\*), (0,\*), (\*, 0|1), or (0|1, \*). Whether these are admitted, deliberately excluded, or simply not yet exercised is unclear. Open Questions flags (0,0) but not these others — a future catalog extension question.

### Topic 2: Cardinality vocabulary justification

**Why out of scope**: The vocabulary {0, 1, *, 0|1} is closed without justification. No value admits "exactly 2" or "1..\*" directly. Whether the vocabulary should be extended to admit finer cardinality constraints (e.g., for a relation with a known fixed multi-element from-slot semantics) belongs in a future framework refinement.

### Topic 3: (Peano-rec) and (Peano-zero-least) routing through the foundation

**Why out of scope**: The appendix introduces two ℕ-arithmetic axioms beyond the foundation's listed NAT axioms. The framework is explicit about this and routes them through the appendix rather than the foundation. Whether to promote these to the foundation is a separate process question; the framework's correctness doesn't depend on the routing.

### Topic 4: Multi-process substrate extension

**Why out of scope**: The framework commits to single-process substrates and acknowledges this scope boundary. Extending the *Sh4 idempotency contract* and the *FDD functional-dependency contract* to multi-process substrates would require a coordination protocol outside the current framework.

VERDICT: REVISE
