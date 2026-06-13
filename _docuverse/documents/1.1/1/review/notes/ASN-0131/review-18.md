# Review of ASN-0131

This is a mathematically sound note. I checked the worked instance (the `e₁`/`e₂`/`e₃` touch tests, the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-segment argument, the width-2 span reaching `a₄` exclusively), the union-distributivity derivation, the contraction wp (RE-CWP), and the retraction analysis (RE-RET, including the unit-depth `coverage = {t : s ≼ t}` argument for the to-set and the honest conditional on `coverage(Θ) ∩ dom(Σ.C) = ∅`). All hold. No proof is hand-waved, edge cases are covered, the wp analyses are non-trivial, and the foundation citations (all from the listed foundation ASNs) are used correctly rather than reinvented.

The findings below are anti-bloat issues — this note carries the `review-mode.anti-bloat` classifier, and there is genuine accretion of derivation into structural slots and repeated re-derivation of one invariant.

## REVISE

### Issue 1: Claims-table cells reproduce their prose derivations
**ASN-0131, Claims Introduced (RE-RET, RE-EDIT)**: RE-RET's cell runs to a full multi-paragraph derivation — "**Backward (other bearer ⟹ survives) is *unconditional*:** R0a/FlatLinkDomain and R-Scope/SingleTupleScope (ASN-0086) confine the fresh nullification to `ℓ`, so any other bearer survives with value fixed by L12…" — which is the *Under retraction* prose verbatim in intent. RE-EDIT's cell is worse: it carries the entire transition-by-transition classification ("the content-subspace edits to `d` … move the answer *through the image* (F-IMG-MONO/-CONTR/-SWING…); … every other transition fixes it — `K.α` (LP6), `K.δ` (LP8), `K.ρ` (LP14)…") and then ends with "**Derivation in the *Stability* prose.**" — explicitly pointing at the prose that holds the same derivation it just reproduced.
**Problem**: The claims table is a structural summary slot (cf. the terse one-line cells in foundation ASN-0034 TA5, ASN-0058, ASN-0098). Packing paragraph-length derivations into it duplicates the prose and degrades the table's function. The RE-EDIT cell admits the duplication in its own last sentence.
**Required**: Reduce RE-RET, RE-EDIT (and trim RE-CWP) to terse claim statements — the result and its status — and leave the derivations to the prose sections that already carry them.

### Issue 2: Coverage-permanence (RE-IDENT) re-derived rather than referenced
**ASN-0131, *Anchoring reached through borrowed content* and *Stability***: RE-IDENT is established in the transclusion section — "The endset's coverage is permanent: links are immutable (L12, ASN-0043), and no transition alters an endset's coverage (LP3, ASN-0098)." The stability section's rearrangement bullet then re-derives it from the same two premises — "reports content-identity endsets (RE-DEF, RE-IDENT), whose coverage is permanent (L12, ASN-0043; LP3, ASN-0098), so under `K.μ~` no surfaced endset's spans change shape" — and the stability closer states it a third time.
**Problem**: The L12+LP3 → spans-don't-move derivation is performed twice (transclusion, then rearrangement bullet) for the identical conclusion; the rearrangement bullet should invoke RE-IDENT, not rebuild it from its premises.
**Required**: Derive RE-IDENT once; in the stability section cite RE-IDENT for the K.μ~ case rather than re-citing L12/LP3.

### Issue 3: Meta-prose digressions into deferred territory
**ASN-0131, *Stability* (rearrangement bullet)**: the parenthetical "(One *could* display a contiguous run of content as several pieces by displacing it piecewise; but that fragmentation is a property of the V-order *display* of the content (ASN-0082) — the rendered mode deferred to open question 3 — not of the content-identity answer RETRIEVEENDSETS returns here…)" interrupts the K.μ~ derivation to raise and dismiss a display mode the content-identity answer excludes by construction.
**ASN-0131, *Existence and discoverability***: the orthogonal-axes payload is RE-SEL (`sel = findlinks_V ∩ addressable`, a real derivation) and the RE-EXST characterization — but it is wrapped in resolution-of-tension scaffolding ("The tension is only apparent, and resolving it is the point."; "That it stops short is the whole reason the operation exists distinct from its link-naming sibling.") that does not advance a guarantee.
**Problem**: A hypothetical the claim's carrier already excludes (piecewise fragmentation) is imagined only to be set aside, mid-derivation; and the existence/discovery section carries rhetorical connective tissue beyond the claims it establishes. (The existence/discovery *distinction itself* is a legitimate statement of what the operation certifies — keep it; trim only the framing.)
**Required**: Move the rendered-mode note out of the K.μ~ derivation (a one-line forward pointer to OQ3 suffices). Trim the resolution-of-tension scaffolding around RE-SEL/RE-EXST to the substantive distinction.

## OUT_OF_SCOPE

No scope violations found. The note respects its boundaries: it cites ASN-0127's image machinery and existence/discovery taxonomy (E-MONO, D-ZERO, D-NONMONO, F-V, F-IMG-*) rather than rebuilding them, and defines no claims straying into link enumeration, counting, pagination, READLINK, FOLLOWLINK, MAKELINK, or BEBE. The Open Questions (whole-endset entirety, multiplicity, rendered mode, intersection-composability, cross-server completeness, type-slot-against-content, link-subspace regions) are correctly deferred as future territory, not asserted as gaps in this ASN.

VERDICT: REVISE
