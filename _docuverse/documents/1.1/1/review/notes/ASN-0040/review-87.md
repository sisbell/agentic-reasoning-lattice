# Review of ASN-0040

The formal core is genuinely rigorous: the freshness proof in Bop is established independently of contiguity, B7's three cases (length-split, equal-length parents, unequal-length parents) are all discharged and all three are illustrated in the trace, the co-reachability restriction in B8 is correctly scoped (divergent branches legitimately re-baptize the same address), and edge cases (empty children, first child, the trivial `m ≥ M` branch of B9, seed conformance) are handled. The remaining issues are the meta-prose accretion the anti-bloat classifier flags.

## REVISE

### Issue 1: Duplicate Nelson "Items 2.1, 2.2, 2.3, 2.4" illustration
**ASN-0040, §The sibling stream and §A baptism traced**: After S1 — "Nelson describes exactly this process… 'Items 2.1, 2.2, 2.3, 2.4… are successive items being placed under 2.' The stream is traversed monotonically, not sampled." And in the trace — "Nelson's 'Items 2.1, 2.2, 2.3, 2.4' is exactly this mechanism — successive baptisms under parent 2 at depth 1…"
**Problem**: The same Nelson quotation makes the same point (sequential sibling baptism via repeated `inc(·, 0)`) in two sections. The second occurrence advances no new reasoning — it is the "two paragraphs say the same thing in different words" pattern.
**Required**: Keep one. The trace occurrence is the more concrete; drop the post-S1 restatement (or vice versa).

### Issue 2: B9-exhibited recaps the general result the proof already proved
**ASN-0040, §A baptism traced (B9 unbounded extent exhibited)**: "for any target M' > 5, an additional M' − 5 baptisms in ([1], 2) extend B₇ to a registry with hwm = M' along the same pattern… so the trace simultaneously witnesses B9 (unboundedness) and B1 (contiguity) under iteration."
**Problem**: B9's proof is already fully general and constructive for all M, and B1 preservation is already proven. The concrete M = 5 walkthrough is the contribution of this passage; the trailing "for any M'…" generalization and the "simultaneously witnesses B9 and B1" recap re-assert proven results — use-site bloat.
**Required**: End the exhibition at the concrete M = 5 result; delete the generalization and the recap sentence.

### Issue 3: The baptismal postcondition is stated verbatim in three structural slots
**ASN-0040, B0a / B4 / Bop**: `op(s).B = s.B ∪ {next(s.B, p, d)}` (B0a), `baptize(p, d)(s) = s' with s'.B = s.B ∪ {next(s.B, p, d)}` (B4), and `POST: s'.B = s.B ∪ {next(s.B, p, d)}` (Bop).
**Problem**: The same equation appears three times. The distinct purposes (closure / atomicity / operation spec) justify three labels, but each restates the full equation rather than referencing it.
**Required**: State the equation once (in Bop), and have B0a and B4 cite it ("the action specified by Bop") rather than reproduce it.

## OUT_OF_SCOPE

### Topic 1: B3's `Occupied` predicate and content constraint
**Why out of scope**: B3 introduces a content predicate `Occupied : T × 𝒮 → {⊤, ⊥}` and a constraint that content live only at baptized addresses. Content storage is explicitly deferred. B3 is correctly framed as a *forward requirement* on a future ASN rather than a claim this ASN proves, so it is appropriately handled — the formal definition of `Occupied` and its operations belongs to the future content-storage ASN, not here.

### Topic 2: Parent-prerequisite question (Bop PRE "no parent-baptized prerequisite is imposed")
**Why out of scope**: Whether a parent must be baptized before its children depends on the ownership model (deferred to Tumbler Ownership). The ASN correctly records this as an open question rather than deciding it.

VERDICT: REVISE
