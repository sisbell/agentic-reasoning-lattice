# Review of ASN-0047

## REVISE

### Issue 1: S3★-aux is both a K.μ~ admissibility hypothesis and an unconditionally-derived invariant

**ASN-0047, Decomposition of K.μ~**: clause (i) reads "the induced post-state M'(d) would satisfy the arrangement-*shape* invariant package on M'(d) — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, **and S3★-aux**, from which the derived D-SEQ★ follows".

**Problem**: S3★-aux is listed as an admissibility filter on the candidate π (clause (i)), yet:
- the D-SEQ★ derivation it supposedly feeds uses only D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a — S3★-aux plays no role in it;
- the Class (a) verification matrix proves S3★-aux holds for K.μ~ *unconditionally* via the decomposition ("K.μ⁻ (full-clearance) restriction preserves subspaces... K.μ⁺ amendment adds only content-subspace positions, so every post-state V-position has subspace s_C or s_L").

If S3★-aux is established for every K.μ~ by the decomposition, it is not a filtering condition on which π are admissible — it cannot exclude any π. Listing it in clause (i) misrepresents it as a per-π hypothesis. The companion sentence ("the remaining per-state arrangement invariants ... S3★, CL-OWN, CL-UNIQ, S2, and S8★ — are *not* admissibility hypotheses but derived consequences") pointedly omits S3★-aux, so the two passages are in direct tension about its status.

**Required**: Decide S3★-aux's role. Either drop it from clause (i) and treat it like S3★/S2/S8★ (derived consequence of the decomposition), or, if it is genuinely needed as an input to Step (A)'s subspace-preservation argument, state that it is consumed at the *pre-state* Σ (where it is an inductive hypothesis) rather than stipulated as a *post-state* admissibility filter on M'(d).

### Issue 2: Four near-duplicate K.μ~ paragraphs in the Class (a) discharge prose

**ASN-0047, ExtendedReachableStateInvariants, per-property prose** (S8a/S8-depth/S8-fin; S8★; D-CTG★/D-MIN★; D-SEQ★): each paragraph's K.μ~ clause repeats the same template — "stipulated by admissibility (i); the K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises..." For example, S8a: "stipulated by admissibility (i); S8-fin(Σ') is discharged ... The K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises the stipulated invariants"; D-CTG★/D-MIN★: "stipulated by admissibility (i); the K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises the stipulation"; D-SEQ★: "derived at Σ' from the K.μ~-chain post-state values ... The K.μ⁻ (full-clearance) + K.μ⁺ decomposition mechanically realises each constituent".

**Problem**: The identical argument is restated four times in different words. Per the anti-bloat classifier, "two paragraphs in the same document say the same thing in different words." The substantive content — admissibility (i) stipulates the shape invariants and the full-clearance decomposition realises them — is one argument, not four.

**Required**: State the "admissibility (i) stipulates; full-clearance decomposition realises" argument once for the shape-invariant package, and have the per-property cells reference it. Keep only the genuinely per-property delta (e.g., S8-fin's independent finite+finite discharge, which is the one non-templated piece).

### Issue 3: "Link store and extended system state" section is a use-site inventory plus forward reference

**ASN-0047, Link store and extended system state**: "This ASN uses link-store properties — `Endset`, `Link`, ... and the inlined invariants L0, L1, L1a, L3, L12, L14 — all inherited unchanged from the foundation. Their formal statements and foundation sources are collected once in the *Inherited from foundation* table below; we do not restate them here." Followed by "A note on preservation specific to this ASN: all existing elementary transitions ... hold L in their extended-state frame (`L' = L`); only K.λ extends L. L12 ... and L-fin follow from this split..."

**Problem**: The section advances no reasoning — it inventories which properties are inherited, points forward to a table, and pre-announces a preservation fact (L' = L for all but K.λ) that the verification matrix and P3 already establish. This is the "definition's introduction enumerates downstream consumers / multiple paragraphs defer to the same downstream location" pattern.

**Required**: Delete the inventory and the preservation pre-announcement; keep only the genuinely local content — the empty-endset reading of L3 (the one item explicitly "not present in the foundation").

### Issue 4: Defensive/scope meta-prose in clause (i) and Coupling-and-isolation

**ASN-0047, Decomposition of K.μ~** and **Coupling and isolation**: e.g. "The admissibility filter (clause (i)) is a hypothesis on the candidate π, non-vacuous and witnessed by the transposition `π_swap` in *Necessity and sufficiency of the precondition* below" (forward reference to a construction developed later), and "S3★ at the post-state is not part of clause (i) but is established as a derived consequence by Step (B)" (defensive statement of what is *not* in clause (i)); and the opening "A clarification on scope. The frame conditions stated above describe individual elementary transitions: K.μ⁺ alone does not modify R, K.α alone does not modify M, and so on."

**Problem**: These are forward references and defensive clarifications that explain the surrounding machinery rather than advance a claim. The "A clarification on scope" paragraph restates frame facts already given at each elementary definition before the substantive J1★ range-trigger point.

**Required**: Remove the forward reference to π_swap (the construction speaks for itself where it appears), drop the "not part of clause (i)" disclaimer once Issue 1 settles S3★-aux's status, and cut the "clarification on scope" preamble — open directly with the range-based-trigger statement of J1★.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The J4 fork composite leaves d_new's link subspace empty and explicitly defers a link-inheritance mechanism ("if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope"). This is correctly future territory, consistent with the named-operations exclusion, not a gap in this ASN.

### Topic 2: Link-subspace-specific invariants beyond shared sequential structure
The open question asking what invariants the link subspace must satisfy *beyond* D-SEQ★ (capacity bounds, endset-reference structure) is genuinely new territory for a future ASN, not a defect here.

META: not applicable — the ASN defines state (Σ = C,L,E,M,R), elementary transitions, and per-state/composite-boundary invariants stated abstractly, squarely within specification territory.

VERDICT: REVISE
