# Review of ASN-0036

## REVISE

### Issue 1: S5's proof forward-depends on the entire downstream invariant set

**ASN-0036, Sharing (S5 proof, "Genuine strand state")**: "The always-on state-level requirements are: the functionality and integrity predicates S2 and S3; the content-side design requirements S7a ... and S7b ...; the document-side requirement S7d ...; the domain-restriction axiom ...; the arrangement-side requirements S8-fin ..., S8-depth ..., and the text-subspace contiguity constraints D-CTG and D-MIN."

**Problem**: S5 is positioned before the Structural-attribution section (S7a/S7b/S7d), the Singleton-partition section (S8-fin, S8a, S8-depth), and the Contiguity section (D-CTG, D-MIN). Its proof — and its `Depends` list — pulls all of them forward. A reader verifying in document order cannot discharge the proof, because the claims it relies on have not yet been stated. The dependency is also self-contradictory with the headline: the claim asserts "S0–S3 ... place no constraint on `|{...}|`," yet the witness is required to satisfy a dozen invariants S0–S3 know nothing about. Logically there is no circularity, but the textual ordering makes S5 unverifiable where it sits.

**Required**: Either relocate S5 after the sections defining S7*, S8*, and D-* (so every cited invariant is already established), or scope the witness obligation to exactly the invariants in force at S5's position and state explicitly that later invariants are checked once introduced.

### Issue 2: Use-site inventory and citation-convention prose in structural slots

**ASN-0036, S5 proof ("Genuine strand state") and S8a**: e.g. "S0 and S1 are transition invariants ... so a single witnessing state cannot violate them and they need not be checked"; and S8a's "We cite this per-component form as 'S8a' where it is more convenient than the `zeros`-based form; the two are interchangeable by the equivalence above."

**Problem**: The "Genuine strand state" paragraph is a defensive justification — it enumerates which downstream invariants must be checked and argues why S0/S1 are exempt — rather than advancing the argument. S8a's closing sentence justifies a citation convenience rather than stating content. Both are the meta-prose the anti-bloat classifier targets; the reader must work past them to reach the two actual constructions.

**Required**: Reduce "Genuine strand state" to the bare statement of which predicates the witness satisfies (no exemption rationale), and delete S8a's citation-convenience sentence — the equivalence to the domain-restriction axiom is already stated.

### Issue 3: S8-depth postcondition asserts existence of a common depth without guarding emptiness

**ASN-0036, S8-depth, Postconditions**: "Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`."

**Problem**: The axiom only constrains *pairs* of co-subspace positions to share depth. The postcondition's existential `m_s` is well-founded only when the subspace is non-empty; for an empty `V_s(d)` no witness depth exists and "(by S8a)" cannot supply one. Downstream consumers (S8 "Uniqueness within a subspace," D-SEQ Step 1) implicitly assume non-emptiness, but the postcondition states the existence unconditionally.

**Required**: Guard the postcondition with `V_s(d) ≠ ∅`, matching how D-CTG/D-MIN/D-SEQ already condition on non-emptiness.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG/D-MIN/S2
The Open Questions correctly defer how INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants. This is operation-specific frame/postcondition territory, explicitly out of scope — not a gap in this ASN.

### Topic 2: Subspace alignment between `subspace(v)` and the element-field of `M(d)(v)`
The note flags this as an operations-layer obligation rather than a state invariant. Treating it as a future operation-layer concern is appropriate; no state-level claim is owed here.

VERDICT: REVISE
