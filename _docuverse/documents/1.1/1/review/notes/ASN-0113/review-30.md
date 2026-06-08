# Review of ASN-0113

## REVISE

### Issue 1: W12 / "What the pair reveals" is a state-space fact, not an operation guarantee
**ASN-0113, "What the pair reveals that neither member alone could" + claim W12**: "ProfileIrreducibility — the map `d ↦ (n_{s_C}(d), n_{s_L}(d))` is determined by neither coordinate alone."
**Problem**: W12 is a property of the reachable document state space — it is true regardless of `RETRIEVEDOCVSPANSET`. The operation merely reports the pair; nothing about its specification depends on profiles being independent. The two-member structure of the result is forced by subspace disjointness (W9/W11), not by profile irreducibility. The section is explicitly motivational ("The whole point of returning *both*…", "what the pair reveals"), and it drags in a substantial ASN-0047 valid-composite witness construction that constrains no behavior of this operation. This is essay content occupying a claim slot.
**Required**: Remove W12 and the section, or demote the irreducibility observation to a single motivational sentence with no claim label and no witness derivation. The operation-relevant content (result is a span-set, never a scalar) is already carried by W0.

### Issue 2: Forward-reference accretion to W0
**ASN-0113, "The substrate we measure"**: "An *allocated empty* document (`d ∈ dom(M)`, `M(d) = ∅`) legitimately yields the defined empty span-set `⟨⟩` (see W0)…"
**Problem**: W0 is introduced two sections later ("What the caller must be handed"). The `(see W0)` pointer is exactly the forward-reference accretion this note's classifier targets — the precondition discussion reaches ahead to a result-type claim not yet stated.
**Required**: State the empty-vs-unallocated distinction where W-pre is defined without the forward pointer, and let W0 stand on its own when reached; or move the result-type stipulation forward so the pointer is unnecessary.

### Issue 3: W18 / "Permanence of the report" restates W8
**ASN-0113, "Permanence of the report" + claim W18**: "`RETRIEVEDOCVSPANSET(d)` is a pure function of the current state `Σ` (by W8), so any two queries against the *same* `Σ` return identical span-sets…"
**Problem**: "Pure function of state" is W8 (PureQuery) reworded; two queries against the same state returning the same value is the definition of a function, already discharged by W8. The only genuine increment — the result depends on `M(d)` alone, not all of `Σ` — is one clause buried under restatement. Two claims and a dedicated section assert purity.
**Required**: Fold the `M(d)`-locality increment into W8 (or a one-line corollary) and delete the duplicated purity prose.

## OUT_OF_SCOPE

### Topic 1: Version-fork and transclusion permanence of reported extents
**Why out of scope**: The open questions on extent permanence across version forks and across transclusion of an edited source belong to version-comparison (SHOWRELATIONOF2VERSIONS) and transclusion operations, not to this pure query. Correctly left as open questions, not claims.

### Topic 2: Consistency between per-subspace extents and any single overall extent
**Why out of scope**: Reconciling the span-set against a single overall extent is RETRIEVEDOCVSPAN territory (per the scope directive); the note correctly poses it as an open question rather than specifying it.

VERDICT: REVISE
