# Review of ASN-0047

I read the full transition model, checked the per-elementary verification matrix against each transition's effect/frame, traced the K.μ~ decomposition and its admissibility clauses, and verified the five worked examples against their cited postconditions. The core mathematics is sound: the J0/J1★/J1'★ coupling discharge of P4★/P4a/P7a, the FrontierEquivalence/ChildSpawnFreshness freshness reads, the D-SEQ★ derivation (both m=2 and m≥3), the K.μ~-FIX/RANGE/LRP cluster, and the fork φ-bijection (order- and multiplicity-preservation) all check out. I found no correctness or missing-edge-case defect. The remaining findings are the forward-reference/redundancy patterns the active `review-mode.anti-bloat` classifier asks me to surface at source.

## REVISE

### Issue 1: Verbatim-duplicated evidence phrase across J4 and a worked example
**ASN-0047, J4 step (ii) and *Worked example: fork of a duplicate-I-address source***: J4 step (ii) reads "Gregory's docreatenewversion copies the source document's entire content subspace in source order ... re-seating each content piece at a fresh sequential V-position, retaining duplicate I-addresses at distinct V-positions as separate entries". The duplicate-source worked example restates this nearly verbatim: "Gregory's docreatenewversion re-seats each content piece at a fresh sequential V-position, 'retaining duplicate I-addresses at distinct V-positions as separate entries' — exactly this count-preserving behaviour."
**Problem**: The "retaining duplicate I-addresses at distinct V-positions as separate entries" clause is stated twice in the same document. The J4 occurrence is the load-bearing one (it grounds the multiplicity-preservation clause of φ). The worked-example occurrence adds no new grounding — it re-cites the same implementation behaviour the abstract claim already carries. This is the "two paragraphs in the same document say the same thing in different words" pattern.
**Required**: Drop the implementation-evidence restatement from the worked example; the example need only check that `|dom(M'(d_new))| = 2 = |V_{s_C}(d_op)|` against the φ-injectivity postcondition. Keep the single evidence statement at J4.

### Issue 2: Coupling "imposed (not derived)" rationale stated in multiple slots
**ASN-0047, ValidComposite★ clause (2) and the J0 Properties-Introduced entry**: ValidComposite★ clause (2) states "The couplings J0, J1★, and J1'★ are *imposed* validity conditions, not axioms of the elementary transition system", and the J0 table row independently states "**Imposed (not derived)** — a clause-(2) validity constraint of ValidComposite★". The same "imposed not derived" rationale also surfaces in J0's definition preamble discussion.
**Problem**: The imposed-vs-derived status is a single fact about the coupling layer; restating it in the table, in clause (2), and in the J0 narrative is defensive justification that does not advance the argument. The authoritative statement belongs in ValidComposite★ clause (2) (where validity is defined); the table and J0 narrative can simply point there.
**Required**: State the imposed/derived distinction once (clause (2)); remove the restatements from the J0 table row and definition preamble, leaving a bare pointer.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal (DELETEVSPAN)
**Why out of scope**: K.μ⁻ models contraction as suffix removal only, which is faithful to the gap-free POOM for suffix deletions but not for the implementation's interior compact-and-renumber. The ASN itself correctly routes this to a named operation and flags it as an open question; modeling interior withdrawal belongs to the (out-of-scope) operation layer, not this transition taxonomy.

META: not applicable — the ASN defines abstract state, transitions, and invariants of state, and stays out of operation/implementation territory.

VERDICT: REVISE
