# Review of ASN-0130

The core machinery is sound: the registration-order grounding of `sig` (PR-SIG) is non-circular (PR2 rests on parse + condition (iv), never on `sig`), the acyclicity-by-construction argument (PR2) is clean, the split-permanence treatment of PR1's conjuncts is honest, and PR3a's substitution induction is fully worked (WT-α, WT-W, the no-capture/no-interference discharge of the sequential PC2 substitution all check out). The wp analyses (PR0, PR5a) are non-trivial and the born-nullified/surface-discipline boundary is handled correctly. My findings are at the clarity and prose level, plus one future-allocation concern.

## REVISE

### Issue 1: Worked composition reuses occupied/reserved symbols

**ASN-0130, Worked composition (steps 2 and 4)**:
- Step 2 introduces "`H` the builder's lease class, Binary, registered at construction" (so `A_H` is the active slice of a *coverage class*), then a few lines later writes "**Take instead a definition `H`** with body `(E x ∈ M_W :: a₁(x))`" and proceeds to compute `expand(H)`. The single symbol `H` now denotes both a registered coverage class and a predicate-definition artifact, in the same step.
- Step 4 names "the builder's **marker class `M`**" with active/audit reads `L_M`, while the same note uses `M_W` (step 2) and `M_pdef` (PR5's lint, a normative claim) where `M_·` is ASN-0129's `members(K)` domain operator (D1). The letter `M` is thus simultaneously the members operator (`M_W`, `M_pdef`) and a class name (`M`, `L_M`).

**Problem**: The worked composition exists to ground the abstractions concretely; these collisions force the reader to disambiguate `H`-the-class from `H`-the-definition and to read `M` as an operator in one expression and a class in the next. This is exactly the kind of confusion the example is meant to dispel.

**Required**: Rename the capture-example definition to something not already in use (e.g. `chkW`), and rename the marker class away from `M` (e.g. `Done`, so `L_Done`) so it does not clash with the `M_K` members notation.

### Issue 2: Forward-reference and editorializing meta-prose (anti-bloat)

Representative instances where the reader must skip past meta-prose to reach the claim:

- **ASN-0130, PR-ENC**: "with a decidable parse and **one further discipline the rest of the note leans on**: prefix-freeness" — the run is characterized by its downstream use rather than stated; the clause adds nothing to *what prefix-freeness is*.
- **ASN-0130, PR-ENC**: "The domain is **deliberately** syntax only — grammatical well-formedness, no typing requirement, **typing being stratified onto registration order instead (PR-SIG)**." The stratification rationale is PR-SIG's content; PR-ENC needs only "the domain is syntactic terms (no typing requirement)."
- **ASN-0130, PR1**: "but permanence divides across the conjuncts, **and the honest statement respects the division**." The division across conjuncts is the substance; "the honest statement respects the division" is self-praise.

**Problem**: The note carries the `review-mode.anti-bloat` classifier. These are the forward-gesture/editorializing accretions that pattern targets — they recharacterize claims by their role or virtue instead of advancing them.

**Required**: Trim the forward-gesture and editorializing fragments, stating each discipline/fact directly and letting the consuming claim (PR-SIG, etc.) carry its own rationale.

## OUT_OF_SCOPE

### Topic 1: Guaranteeing a contiguous content run under concurrent allocation

PR0 (i) requires `A_def = {shift(a, k) : 0 ≤ k < n}` — one contiguous segment of an origin's K.α chain. The worked composition silently assumes this is achievable ("with no other K.α scoped to `d_b` interleaved"), but `SequentialAtomicTransitions` (ASN-0093) sequentializes but does not *prevent interleaving* of two writers' K.α steps to the same document. Another actor's content allocation to `d_b` between the builder's value-steps would split the run, making the term unregisterable.

**Why out of scope**: PR0 correctly takes contiguity as a *precondition* and verifies it mechanically; *how* a builder obtains a guaranteed-contiguous run (a single-writer discipline for definition-bearing documents, or an atomic multi-content-allocation primitive) is an operations/allocation question, not a defect in ASN-0130's claims. It belongs in a future ops ASN, alongside the encoding byte-format the note already defers.

VERDICT: REVISE
