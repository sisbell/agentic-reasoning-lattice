# Review of ASN-0087

## REVISE

### Issue 1: Depth convention re-derived three times
**ASN-0087, Inputs + Effect**: M-DepthConv is stated in "Inputs" (with Nelson "subdivision of links by further digits" and Gregory `findnextlinkvsa` citations), then re-argued in "Effect" twice — "We must be precise about where the depth comes from" and "The depth is 2 for every link MAKELINK places." The second Effect paragraph re-derives the scoped universal via an exhaustiveness sweep of the substrate vocabulary (K.μ⁺ amendment, J4/ForkComposite, "No other transition kind touches M(d)"), and the Nelson/Gregory citations appear a second time.
**Problem**: One claim (depth = 2 by convention, scoped to MAKELINK-placed links, general `m_L(d)` retained downstream) is established, then restated and re-justified across three passages. The substrate-vocabulary exhaustiveness argument is a use-site enumeration that does not advance the operation's meaning.
**Required**: State M-DepthConv once at its definition site. Cite Nelson/Gregory once. Drop the "exactly one operation writes a link-subspace V-position" sweep — the scoped universal stands on M-DepthConv alone.

### Issue 2: Defensive reviser-drift prose in invariant preservation
**ASN-0087, Per-State Invariants**: M0 — "This is not a content-frame argument: M0 quantifies over dom(M), not dom(C)." S7d — "Its preservation has nothing to do with the content frame Σ'.C = Σ.C." S4 — "(The 'no new content *allocation events*' clause is the genuinely vacuous part.)"
**Problem**: These sentences explain why a *prior categorization* was wrong rather than stating what preserves the invariant. They are prior-finding content relocated into the prose. The claim "M0 holds because dom(Σ'.M) = dom(Σ.M)" is complete without the negation of an alternative argument.
**Required**: State the preserving frame and stop. Remove the "this is not X" rebuttals.

### Issue 3: Reflexive case treated in four places
**ASN-0087, Worked Example / wp Case 2 / Reflexive Endsets / M-Reflexive**: The reflexive-endset outcome (`v_ℓ ∈ project(ℓ, i, d, Σ')`, forced home-document discovery, structural exclusion under StandardAuthoring) appears in the worked example's "Reflexive variant," the wp Case 2 "reflexive route," the dedicated "Reflexive Endsets" section, and the M-Reflexive claim. Within "Reflexive Endsets," the "Consistency with M-DiscSymmetry" paragraph restates M-DiscSymmetry and "Boundary case for LP12" restates the worked-example computation.
**Problem**: The same result and its StandardAuthoring exclusion are derived up to four times. "Consistency with M-DiscSymmetry" is a restatement of an already-stated claim in a structural slot.
**Required**: Keep one derivation (the dedicated section), let the worked example *exhibit* it without re-deriving, and delete the M-DiscSymmetry restatement.

### Issue 4: wp enabledness/membership distinction over-explained
**ASN-0087, Weakest Precondition**: The "Operation enabledness" and "Membership precondition" paragraphs establish the `enabled ∧ membership` split; the same split is then re-explained in Case 1 ("the two membership obligations are independent"), in Case 2 ("here the membership clause … is not a separate obligation"), and again in the M-WP claim. Each wp expression re-inlines "where `enabled(MAKELINK) ≡ d ∈ dom(Σ.M) ∧ N ≥ 3 ∧ …`".
**Problem**: The distinction is load-bearing once; restating it at every case and re-expanding `enabled(MAKELINK)` four times is noise the reader must skip.
**Required**: Define `enabled(MAKELINK)` once, state the enabled/membership rule once, and let the two cases differ only in the predicate they add.

### Issue 5: Cross-document cascade paragraph is an accreted forward-looking essay
**ASN-0087, Side Effects**: "Cross-document discovery cascade across composite MAKELINK sequences" asserts that cascades "preserve every per-state invariant by LP9 + LP13 + L12 … These close composition; the cascade redistributes which links are discoverable from which documents but corrupts no state component."
**Problem**: This is a multi-operation property dressed as a single-operation claim, with a one-line "these close composition" standing in for a derivation. It does not advance MAKELINK's own specification, and "redistributes which links are discoverable" is essay content, not a contract clause.
**Required**: Remove it, or reduce to a single sentence stating that composition preservation follows from the per-step lemmas — without the redistribution narration. The duplicated M-PriorLinkDisc text in this claim's table cell should also be trimmed.

### Issue 6: Home-document restriction duplicated
**ASN-0087, Side Effects, "Restriction to the home document"**: This paragraph derives `discoverable_from(ℓ', d_target, Σ') = discoverable_from(ℓ', d_target, Σ)` for `d_target ≠ d` from K.μ⁺_L's frame — which M-PriorLinkDisc's `d_target ≠ d` clause already states with the same justification.
**Problem**: Two passages in the same section say the same thing in different words.
**Required**: Fold into M-PriorLinkDisc; drop the standalone paragraph.

### Issue 7: Symmetry stated redundantly
**ASN-0087, Discoverability Is Symmetric / worked example / Reflexive Endsets / M-DiscSymmetry**: The "home document has no privileged role in discovery" point appears in its own section, in the worked example's "M-DiscSymmetry" aside, in "Consistency with M-DiscSymmetry," and in the claim.
**Problem**: Four statements of one property.
**Required**: One section plus the claim suffice; remove the in-line asides.

## OUT_OF_SCOPE

### Topic 1: Endset well-formedness for spans referencing unallocated I-addresses
**Why out of scope**: The first Open Question ("What well-formedness constraints, beyond e₃ ≠ ∅, must endsets satisfy when their spans reference I-addresses not currently in dom(C) or dom(L)?") is genuinely new territory — L4 (ASN-0043) permits forward-reaching endsets, and constraining them is a future ASN, not a defect here.

### Topic 2: Protocol-layer composite atomicity
**Why out of scope**: The mechanism enforcing composite-level atomicity above the substrate is correctly identified as belonging to a higher layer; the ASN's job is to establish that the substrate does *not* supply it, which it does.

META: The ASN stays within abstract state/operation/invariant territory — it specifies MAKELINK as a composite transition with verifiable contracts, not implementation mechanics — so it is incomplete-by-bloat, not drifted.

VERDICT: REVISE
