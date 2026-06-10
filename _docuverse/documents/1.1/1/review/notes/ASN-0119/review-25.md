# Review of ASN-0119

I checked the imported facts (RA0–RA2 from ASN-0084), the worked pivot and swap against explicit ordinals, the invariant accounting against ASN-0047's two theorems, and the inline re-derivation of footprint transport. The arithmetic is correct (I re-verified both worked examples, the π tables, the tiling, and the two-move composite reaching `A C D E B` through the observable intermediate `A C D B E`). The hard value-dependent invariants (S3★, S8★) are discharged with real arguments rather than checkmarks, and the RA7c run-structure claim, its non-necessity counterexamples, and the degenerate-input analysis are sound. Two issues remain.

## REVISE

### Issue 1: J1★ vacuity rests on the wrong fact

**ASN-0119, "What is preserved: I-address correspondence" (invariant-accounting paragraph)**: "As a transition in ASN-0047's model REARRANGE allocates no content and records no provenance, with `ran(M'(d)) = ran(M(d))` by RA1, so the model's coupling obligations J0, J1★, and J1'★ hold vacuously."

**Problem**: The three obligations are lumped under one reason-conjunction, but they have three distinct vacuity reasons, and the one attached to J1★ is insufficient.

- J0 (no fresh I-address appears unplaced): correct — `dom(C') = dom(C)`, antecedent empty.
- J1'★ (no fresh provenance entry): correct — `R' = R`.
- **J1★** fires whenever an I-address is *new to the content-subspace range* of `M'(d)` — and J1★'s own statement (ASN-0047) makes this explicitly range-based, "regardless of whether the V-position carrying it existed in `dom(M(d))`." So a *pre-existing* content address that newly enters the content-subspace range would trigger it; "allocates no content" does not rule that out. And `ran(M'(d)) = ran(M(d))` is *full*-range invariance, which does not by itself entail content-subspace-range invariance.

The fact J1★ actually needs — `{M'(d)(v) : subspace(v) = s_C} = {M(d)(u) : subspace(u) = s_C}`, from π permuting the text subspace onto itself — is proved in the *very next sentence*, but the note attaches it to P4★, not J1★. (It is also reachable from RA1 + S3★ + SD, since content-subspace range = full range ∩ `dom(C)`, but that composition is unstated.) As written, J1★'s vacuity is justified by a fact that does not establish it.

**Required**: Justify J1★ vacuity from content-subspace-range invariance (π's subspace-preservation, already in hand for S3★/P4★), and stop lumping the three obligations behind a single reason-conjunction — give each its own.

### Issue 2: Forward-reference / citation-policy meta-prose in "The two streams"

**ASN-0119, "The two streams" and the invariant-accounting section**:
- "(ASN-0098's single-state characterisations — properties of one Σ rather than of a transition — carry over directly and are cited as usual.)"
- "Because REARRANGE_K sits outside ASN-0047's transition vocabulary, ASN-0098's link-projection lemmas about transitions ... are proved by case analysis over that vocabulary and do not cover it; where this note needs their conclusions for REARRANGE it re-derives them inline rather than cites them."
- "discharged here so the invariant accounting lives in one place"

**Problem**: These three passages explain *proof technique and document organization* (which ASN-0098 results are cited vs. re-derived, why, and where the re-derivation lives) rather than advancing what REARRANGE does. The middle passage is a forward reference whose fulfillment is the inline coverage-invariance derivation in the Links section (RA7a); the methodological framing can collapse to a one-clause parenthetical at that use-site. The third is a document-ordering justification. A reader following RA0–RA9 skips all three. The substantive content nearby — that REARRANGE realizes the same net change as K.μ~ *without vacating content*, which is load-bearing for content permanence — should stay; the citation-policy and proof-provenance scaffolding around it should not.

**Required**: Move the re-derive-vs-cite remark to RA7a as a brief aside; drop the standalone citation-policy parenthetical and the "lives in one place" placement justification.

## OUT_OF_SCOPE

### Topic 1: Rearrangement at depth > 2 and in non-text subspaces
**Why out of scope**: The note explicitly confines itself ("We make no claim about other subspaces or other depths"), matching ASN-0084's depth-2, `S = 1` scope. Higher-depth and link-subspace transposition is a future extension, not a defect here.

### Topic 2: Cross-document boundary coherence under transclusion, concurrency, discovery-index invariants, prior-arrangement recoverability
**Why out of scope**: These are correctly deferred to the Open Questions. RA9 establishes isolation of *this* document's rearrangement; how a cut interior to one document resolves against another document's independent arrangement of shared content, and how concurrent rearrangements compose, are new territory.

META: not applicable — the note specifies state (the arrangement), an operation on it (the position permutation), and the invariants it preserves, all stated abstractly enough to bind any conforming implementation; the Gregory uniform-displacement discussion is grounding evidence for the tiling requirement, not implementation mechanics.

VERDICT: REVISE
