# Review of ASN-0076

## REVISE

### Issue 1: Definition introduction enumerates its downstream consumers
**ASN-0076, §The Composite**: "In particular `ℓ_old ∈ coverage(E_from)`, which is all the downstream proofs (E4, E7) require."
**Problem**: The trailing clause is a use-site inventory — it names which later claims consume the fact rather than advancing the coverage computation itself. This is the consumer-enumeration accretion pattern; the reader does not need E4/E7 named here to follow the coverage claim.
**Required**: Drop "which is all the downstream proofs (E4, E7) require." The sentence `ℓ_old ∈ coverage(E_from)` stands on its own.

### Issue 2: Structural-vs-semantic / `τ_sup`-convention point restated in three places
**ASN-0076, §The Composite, §The Supersession Relationship, E4 interpretation**: The claim that the supersession link is only a *structural* witness and that semantic identification rests on an external `τ_sup` convention is made three times: at the `τ_sup` definition ("The convention by which a reader recognizes `τ_sup`… is external to the link model and deferred to a future ASN"), in the two opening paragraphs of §The Supersession Relationship ("The link model alone cannot *identify* such a link as a supersession…"), and again in E4's interpretation ("What makes it a *supersession* link is the external `τ_sup` convention… not any structural mark").
**Problem**: Two/three paragraphs in different sections say the same thing in different words, and all defer to the same downstream location. This is the duplicated-prose / shared-deferral accretion pattern.
**Required**: State the structural-vs-semantic distinction once (the `τ_sup` definition in §The Composite is the natural site) and have E4 and §The Supersession Relationship rely on it rather than re-deriving it. The two opening paragraphs of §The Supersession Relationship can collapse to a single sentence pointing at E4.

### Issue 3: Mutual deferral between §The Composite and E0 for ValidComposite★
**ASN-0076, §The Composite ("EDITLINK as a valid composite") and E0 ("Invariant inheritance")**: §The Composite discharges ValidComposite★ but routes clause (i) elsewhere — "as discharged in E0 below" — while E0's invariant-inheritance paragraph in turn states "EDITLINK is a ValidComposite★ (discharged in §The Composite)."
**Problem**: The two passages defer to each other for the same conclusion, forcing the reader to bounce between sections to confirm ValidComposite★ is actually established. This is forward-reference accretion around a single result.
**Required**: Consolidate the ValidComposite★ discharge in one location. Since E0 is where K.λ's preconditions (clause (i)) are proved in full, fold the J0/J1★/J1'★ vacuity argument (currently in §The Composite) into E0 and let the §The Composite paragraph be a one-line pointer, or vice versa — but not a two-way deferral.

## OUT_OF_SCOPE

### Topic 1: Convention by which a reader identifies the supersession type and selects the successor span
**Why out of scope**: The recognizability of `τ_sup` as a supersession marker and the span-selection convention within an unordered to-endset (L5) are correctly deferred to a future ASN on type-endset conventions; they are new territory, not errors here. (The deferral itself is fine; only the *repetition* of the deferral is flagged under Issue 2.)

### Topic 2: Supersession-chain invariants, cycles, and "current successor" computation
**Why out of scope**: Termination of supersession-chain traversal and conflict-resolution policy are reader-side/future-ASN concerns, appropriately listed in Open Questions rather than resolved here.

VERDICT: REVISE
