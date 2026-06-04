# Review of ASN-0087

## REVISE

### Issue 1: Redundant restatement and essay framing in "The Problem"

**ASN-0087, The Problem**: Paragraph 1 already states "link creation must produce three things unconditionally: an *identity* ..., a *value* ..., and a *home* .... It must also establish the *discoverability property* — the LP12 (ASN-0098) mechanism ...". Paragraph 2 then opens: "We are careful to distinguish the property from its realization. MAKELINK brings identity, value, and home into being unconditionally, and it establishes the LP12 discoverability mechanism."

**Problem**: The first two sentences of paragraph 2 re-list the identity/value/home/LP12 content verbatim from paragraph 1 — the "two paragraphs say the same thing in different words" pattern the anti-bloat directive names. The only genuinely new content is the property-vs-realization distinction (discoverability *mechanism* established unconditionally vs *actual* discoverability being arrangement-conditional). The trailing "Whether the link is *actually* discoverable ... a separate, arrangement-conditional matter that the body characterizes" is a forward-reference deferral with meta-prose, and "We ask: what is allocated, what is recorded ..." is essay roadmap framing in the problem-statement slot.

**Required**: Drop the re-listing. Keep only the property/realization distinction, stated once, without the "We are careful to distinguish" framing, the "that the body characterizes" deferral, and the rhetorical "We ask:" roadmap.

## OUT_OF_SCOPE

(none)

---

I checked the substantive content carefully and found it sound:

- The `ℓ ∉ ran(Σ.M(d))` derivation (Preconditions) is complete — the S3★-aux + S3★ + K.λ-freshness chain is shown step by step, both subspace cases discharged.
- The wp computation distinguishes Case 1 (`d_target ≠ d`) and Case 2 (`d_target = d`) correctly, including the membership-vs-enabledness split and the reflexive disjunct; the intersection-over-union distribution is valid and `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}` is justified by the prior freshness lemma.
- The worked example is internally consistent (verified `a₁ ⋠ a₂`, `a₁ ⋠ ℓ` by component disagreement at positions 8 and 7; `ℓ` is `A_L(d)`'s correct first emission).
- S2 is discharged via the explicit two-part (within-subspace + cross-subspace) exclusion rather than hand-waved; D-SEQ★ covers both `n_L = 0` and `n_L ≥ 1`; the coupling constraints J0/J1★/J1'★ are discharged separately for structurally distinct reasons.
- Boundary cases (empty middle endsets, first link, subsequent link, orphan/resurrection via LP18) are addressed.

VERDICT: REVISE
