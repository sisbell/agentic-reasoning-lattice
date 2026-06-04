# Review of ASN-0087

## REVISE

### Issue 1: Redundant second derivation of `ℓ ∉ ran(Σ_mid.M(d))`
**ASN-0087, Preconditions**: "SD (StoreDisjointness, ASN-0093) confirms internal consistency at `Σ_mid`: ... `dom(Σ_mid.C) ∩ dom(Σ_mid.L) = ∅` gives `ℓ ∉ dom(Σ_mid.C)` — so no `s_C`-subspace V-position at `Σ_mid` can image to `ℓ` either, matching the conclusion derived above."
**Problem**: The S3★ + S3★-aux chain immediately above already establishes `ℓ ∉ ran(Σ.M(d)) = ran(Σ_mid.M(d))` in full. This paragraph re-reaches the same conclusion by a second path and explicitly notes it "matches" — it discharges no additional obligation and is meta-prose the precise reader must skip past.
**Required**: Delete the SD confirmation paragraph (or, if SD is genuinely needed for a distinct step, state only that step, not a parallel re-derivation of an already-closed conclusion).

### Issue 2: "Discoverability Is Symmetric" is mostly essay
**ASN-0087, Discoverability Is Symmetric**: "This realizes Nelson's intent that all parties reaching a link's endpoints ... discover it by querying their own content; the home document holds the link for ownership and naming only." and "The MAKELINK operation respects this symmetry by treating all `N ≥ 3` endsets uniformly in storage. No endset is given special treatment ..."
**Problem**: The technical content of this section is a single sentence (by LP12, any document reaching an endset coverage discovers `ℓ`), and that fact is already captured by claim M-DiscSymmetry. The remaining two paragraphs are Nelson interpretation and a behavioral restatement that advance no reasoning.
**Required**: Reduce to the one LP12 consequence; drop the interpretive paragraphs or relegate to a single motivating clause.

### Issue 3: Second "Permanence" section restates the content/arrangement split
**ASN-0087, Permanence**: "This separation of permanent I-stream content ... is the content/arrangement split that P3 (ArrangementMutabilityOnly, ASN-0047) names: arrangement `M` is the only state component that can lose information, while `L` is immutable." and "The two-stream architecture makes link permanence cleanly separable from link visibility."
**Problem**: The P3 content/arrangement split is already discharged clause-by-clause in *Invariant Preservation* and framed in *What Does Not Change*. The closing sentence is an interpretive summary. The load-bearing technical claim here is only the K.μ~ link-subspace-fixing argument; the surrounding split-restatement duplicates earlier prose.
**Required**: Keep the K.μ~ fixity derivation; remove the P3-restatement and the two-stream-architecture closer.

### Issue 4: Defensive "load-bearing" meta-prose in side-effects derivation
**ASN-0087, Side Effects on Prior Links' Discoverability**: "The temporal direction of the inclusion is load-bearing — freshness at `Σ_ℓ` is propagated *backward* to `Σ_{ℓ'}`, which is precisely what Store Monotonicity★ supplies."
**Problem**: The sentence immediately preceding already performs the backward-propagation step with the Store Monotonicity★ citation. This sentence only asserts that the step matters and names the lemma again — defensive justification, not reasoning.
**Required**: Delete; the derivation stands on its own.

### Issue 5: Atomicity section re-derives the WP Case 2 / reflexive comparison
**ASN-0087, Atomicity**: "for `d_target = d`, the post-state arrangement gains `ℓ`: `ran(Σ'.M(d)) = ran(Σ_mid.M(d)) ∪ {ℓ}`. The two values differ precisely when some endset `eᵢ` *reflexively* covers `ℓ` ... (M-Reflexive)."
**Problem**: Since `Σ_mid.M = Σ.M`, this comparison is mathematically identical to the WP Case 2 disjunction and the reflexive sub-case is M-Reflexive verbatim. The valid atomicity point is the *existence* of an observable intermediate state with `ℓ ∈ dom(L)` but `ℓ ∉ ran(M(d))`; the discoverability re-derivation duplicates earlier work.
**Required**: State the intermediate-state observation and cite M-Reflexive/M-WP for the discoverability delta rather than re-deriving it.

### Issue 6: Claims table enumerates downstream consumers of StandardAuthoring
**ASN-0087, Claims Introduced (StandardAuthoring)**: "This is the named discipline cited by M-Reflexive, M-WP, and the cascade-vacuity discussion."
**Problem**: Matches the flagged pattern — a definition's entry enumerating its use sites rather than advancing its meaning. These pointers rot as the note evolves and add nothing to the predicate's content.
**Required**: Remove the consumer inventory; the definition `coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` is self-contained.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets (Open Question 1)
**Why out of scope**: Constraints on endsets whose spans reference not-yet-allocated addresses are governed by L4 (EndsetGenerality) and belong to a future endset-discipline ASN, not to MAKELINK's transition semantics.

### Topic 2: Deferred-consistency discoverability model (Open Question 3)
**Why out of scope**: Whether a deferred-consistency model is admissible is a protocol-layer question; this ASN correctly scopes itself to substrate post-state guarantees.

META: (none — the ASN is squarely a state/operation/invariant specification; its issues are accumulated meta-prose, which is fixable.)

VERDICT: REVISE
