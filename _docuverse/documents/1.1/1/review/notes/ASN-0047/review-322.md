# Review of ASN-0047

## REVISE

### Issue 1: Forward-reference accretion — repeated deferral to the temporal-scope preamble
**ASN-0047, multiple sections (P4a definition box, verification-matrix preamble, Composite-boundary matrix, ExtendedReachableStateInvariants)**: the per-state vs composite-boundary distinction is deferred to one location from ≥4 sites: "(temporal-scope per the *Extended reachable-state invariants* preamble)" (P4a box), "temporal scopes per the section preamble" (matrix preamble), "classified per the preamble" (Composite-boundary matrix), and "classified per this preamble" (closing sentence).
**Problem**: This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The reader must re-navigate to the preamble at each occurrence; the pointers carry no content.
**Required**: State the distinction once at the preamble and let the matrix/definition boxes stand on their own, or inline a one-clause reminder at each site — but drop the chain of "per the preamble" pointers.

### Issue 2: "clause (i)'s scope" deferral scaffolding
**ASN-0047, *Decomposition of K.μ~***: "**Clause (i)'s scope** is the arrangement-*shape* package only … Later references to clause (i)'s scope point here." The pointer is then exercised repeatedly: "clause (i)'s scope, above," "see the admissibility definition," "S8★ falls outside clause (i)'s scope (see the admissibility definition)."
**Problem**: A single definitional point ("clause (i) constrains shape, not referential targets") is wrapped in a pointer-and-back-reference apparatus across the section. The scaffolding is meta-prose around the definition rather than the definition advancing.
**Required**: Fix clause (i)'s scope inline at its first statement and state, at each of S3★ and S8★, the one fact needed ("S3★/S8★ discharged separately by Step (B) / the decomposition"); delete the "point here" / "see the admissibility definition" pointers.

### Issue 3: "Freshness discharge (scope note)" explains the guard rather than advancing the argument
**ASN-0047, FrontierEquivalence, *Freshness discharge (scope note)***: "Every K.δ case-(ii) sub-case discharges its freshness conjunct `e ∉ E` as a single live-state read… The sub-cases differ solely in *which* state fact the guard `e ∉ E` encodes."
**Problem**: This is the flagged pattern "new prose around an axiom/guard explaining why it is needed rather than what it says." The two load-bearing facts (k=0 reads the frontier; k∈{1,2} reads the at-most-once-per-`(t,k')` discipline) are already stated in the K.δ box's per-sub-case lines; the scope note restates them as commentary.
**Required**: Fold the two facts into the K.δ sub-case lines (k=0 → frontier read; k∈{1,2} → at-most-once read) and delete the standalone note.

### Issue 4: Contradictory classification of P4★ and P7a
**ASN-0047, *Extended reachable-state invariants***: the preamble lists "P4★ ∧ P4a ∧ P7a" as *composite-boundary properties* that "may transiently fail at intermediate states," yet the following paragraph states "P4★ and P7a are per-state properties holding at boundaries."
**Problem**: "Per-state invariant" is defined two paragraphs earlier as holding at *every* reachable state. The Composite-boundary matrix itself shows P7a failing "After K.α before K.μ⁺/K.ρ" and P4★ failing "After K.μ⁺ before K.ρ." Calling them "per-state properties" directly contradicts both the established term and the matrix.
**Required**: Use one term. If P4★/P7a are state-predicates guaranteed only at composite boundaries, name them as such (composite-boundary state-predicates) and drop "per-state properties holding at boundaries."

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
**Why out of scope**: K.μ⁻ models only suffix removal; interior withdrawal with V-position compaction (the implementation's `DELETEVSPAN`) is a distinct contraction operation. The ASN correctly defers this to its Open Questions rather than specifying it — no revision is needed, and the named-operation `DELETEVSPAN` is explicitly out of scope.

VERDICT: REVISE
