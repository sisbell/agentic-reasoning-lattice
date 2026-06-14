# Review of ASN-0125

This is a strong, carefully-staged note. I checked the central architecture (EL0–EL3), both operation contracts (EL6/ASSERTop, EL7/EDITop), the discipline induction (EL-DM), and the relational results (EL11–EL16) against the foundations, and traced the worked example end to end. The mathematics holds: EL0 is L12/LP13 read as a wp; the K.λ-only validity argument and Vocabulary fact V correctly license reachability of every intermediate state; the EL9(2) de-listing construction handles the `j=1`/`j=n` boundaries and the prefix-only retention of `K.μ⁻`; EL11(a)'s biconditional is sound (the content-address-extending-`y` exclusion via C1/L0/SC-NEQ is correct); and EL14's cardinality cases (1, ≥2, 0) and the activity-agnostic-membership construction (e) are all reachable as claimed. The worked example's address arithmetic (`H.0.s_L.1..6`, `P.0.s_L.1..2`) and the standoff/repair sequence check out.

I found no correctness defect. The one finding is anti-bloat residue, which this note's classifier asks me to surface at source.

## REVISE

### Issue 1: The "attribution is by home, not named principal — ASN-0042's office, not a function of Σ" point is stated three to four times

**ASN-0125, EL8(b)**: "it carries no principal set, so resolving a home further to a named owner is the office of an ownership layer (ASN-0042) overlaid on the substrate, not a function of Σ — an overlay the attribution guarantee neither needs nor invokes"

**ASN-0125, EL3**: "(the scope of this attribution — home, not named principal — is fixed at EL8(b))"

**ASN-0125, EL13**: "(A per-asserter 'latest' is not a state function: principal resolution is the ASN-0042 overlay's office, EL8(b), not a function of Σ.)"

**ASN-0125, claim table (EL13 entry)**: "not per-principal (principal resolution is the ASN-0042 overlay's office, EL8b, not a function of Σ)"

**Problem**: EL8(b) is the canonical statement. EL3 forward-defers to it (a deferral to a downstream location), and EL13 both *cites* EL8(b) *and restates its content* — then the EL13 table entry restates it a fourth time. The new content in EL13's parenthetical is only "per-asserter latest is not a state function"; the justification ("principal resolution is the ASN-0042 overlay's office, not a function of Σ") is EL8(b) reproduced. This is the "two paragraphs say the same thing in different words" + "multiple paragraphs defer to the same downstream location" pattern, compounded into the claim table.

**Required**: State the home-vs-named-principal / ASN-0042 boundary once, at EL8(b). In EL13 replace the restated justification with a bare citation (e.g., "a per-asserter 'latest' is not a state function — it needs principal resolution, placed outside Σ by EL8(b)"), and trim the EL13 table entry to "not per-principal (EL8b)". Drop or compress the EL3 forward-deferral so the scope note doesn't pre-announce a downstream paragraph.

A lighter instance of the same shape: EL14(d) re-explains EL13's mechanism ("across homes that order has no state witness") in addition to citing EL13. Since EL14(d) is deriving a genuinely new conclusion (no canonical temporal selector), a citation to EL13 for the mechanism would suffice without re-narrating it.

## OUT_OF_SCOPE

### Topic 1: Authority governing retraction/assertion by a non-asserter

The note (RQ2, EL8c) deliberately makes authorship open and attributes claims only to a *home*, not a named principal, because Σ carries no principal set. Enforcing who may retract whose claim therefore genuinely belongs to the ownership overlay (ASN-0042), and the note correctly defers it (Open Question 1). Not a gap in this ASN.

### Topic 2: Span-level correspondence when an edit reshapes an endset

EDITLINK gives the reshaped reading a fresh identity plus a supersession claim; it does not record *which* span widened or narrowed. The note flags this as Open Question 7. Recording a finer old↔new endset correspondence is a distinct, future refinement (and would need its own carrier), not a defect in the supersession architecture defined here.

VERDICT: REVISE
