# Review of ASN-0091

This note carries `review-mode.anti-bloat`. The technical content is sound — the abstract/concrete split is legitimate, the witnesses for RE-frag/coal/eq are concrete, and no circularity arises in the RE-subpres derivation (S3★ at Σ' is discharged by ExtendedReachableStateInvariants, not by RE-subpres). The findings below are accumulated meta-prose around the forward-reference structure.

## REVISE

### Issue 1: Counterfactual clause-necessity prose around RA-dom
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "RA-dom pins the bijection's two domains equal, sharpening the bijection to a permutation of a single finite set; **without RA-dom, RA-π alone would only assert equicardinality of the pre- and post-state V-position sets, leaving open the possibility that the post-state domain consists of *different* V-positions than the pre-state.**"
**Problem**: The clause after the semicolon explains *why RA-dom is needed* via a counterfactual ("without RA-dom...would only assert..."), not what RA-dom says. This is the "explains why the axiom is needed rather than what it says" pattern. The definition stands on its own; the reader does not need the imagined RA-dom-free system to understand the clause.
**Required**: Delete the counterfactual; the clause "RA-dom pins the two domains equal, making π a permutation of a single finite set" suffices.

### Issue 2: Repeated "independent of how π was generated, so every concrete realization inherits…" boilerplate
**ASN-0091, abstract S2 derivation and RE-subpres derivation**:
- "The derivation is abstract — it relies only on RA-dom, RA-π (bijection), and pre-state S2 at Σ … **independent of how π was generated, so every concrete realization of the class (including REARRANGE_K) inherits S2 at Σ' without case-specific verification.**"
- "The derivation is abstract — it relies only on RA-π, RA-frame's Σ'.C = Σ.C and Σ'.L = Σ.L, pre-state S3★, RA-adm…, and foundation L14 — **independent of how π was generated, so every concrete realization of the class inherits subspace preservation as an abstract consequence.**"
**Problem**: The same closing sentence recurs nearly verbatim, and both restate information already carried by the Provenance column of the Claims table ("abstract" = derivable from RA-* alone). The use-site dependency inventory ("relies only on X, Y, Z") plus the inheritance claim is a duplicated boilerplate trailer.
**Required**: Drop the trailing "independent of how π was generated…inherits" sentence; the "abstract" provenance label already carries it. Keep at most a once-stated convention that abstract-tagged claims hold for every realiser.

### Issue 3: Tabulation meta-narration in a structural slot
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: "The substantive RA-adm work follows in the per-invariant layers; **the two correspondences are tabulated rather than re-narrated.**"
**Problem**: Prose about the document's own structure (we use tables, not narration). It advances no reasoning.
**Required**: Delete the sentence; the tables themselves make the point.

### Issue 4: Cluster of forward pointers deferring to the same downstream locations
**ASN-0091, multiple sections**:
- "…the exclusion of content↔link subspace crossings is **derived once below as RE-subpres**, not pre-empted here."
- "…the set-image invariance **proved concretely in the 'Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses' below.**"
- "**A concrete two-step trace realising direction (+, −) appears in the 'Worked Example — Two-Step Composition (+, −)' section below.**"
- "RE-sub **below** strengthens this to pointwise fixity…"
**Problem**: Multiple paragraphs in different sections forward-point to named downstream content. The patterns compound: each forward pointer asks the reader to hold an unresolved promise. The claims should either be made where they belong or pointed to once.
**Required**: Remove the navigational forward pointers; let the downstream sections stand on their own labels (RE-subpres, the worked examples) without prose announcing them in advance.

### Issue 5: Inline provenance prose duplicates the Claims-table Provenance column
**ASN-0091, RE-sub / RE-ext sections and Claims table**: The RE-sub and RE-ext sections each narrate "The *abstract* property…is captured by RE-subpres… RE-sub adds…the pointwise form" and "The pointwise-fixity strengthening…is REARRANGE_K-specific, not abstract: a different concrete realisation could non-trivially permute the link subspace…and would still satisfy RA-adm." The Claims table's Provenance column already records exactly this (RE-subpres = abstract; RE-sub/RE-ext = REARRANGE_K).
**Problem**: The "abstract vs REARRANGE_K-specific" distinction is stated three times — in the RE-sub prose, the RE-ext prose, and the table column. The "a different concrete realisation could…and would still satisfy RA-adm" sentence imagines a hypothetical realiser purely to motivate the distinction; it is essay content justifying the strengthening's existence rather than advancing it.
**Required**: State the abstract/REARRANGE_K split once (the table already does). Drop the hypothetical-realiser justification sentences.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer link-subspace rearrangement semantics, the cardinality-increase bound, and the bijection-realizability question to future ASNs.)

VERDICT: REVISE
