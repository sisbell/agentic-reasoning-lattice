# Review of ASN-0075

## REVISE

### Issue 1: Synchronised-edits claim asserted under a lemma whose precondition excludes it

**ASN-0075, "Supplementary lemma (R-disjointness implies Q0...)"**: "Documents with synchronised edits (each deletion mirrored in the partner) satisfy `Q0` non-vacuously: for shared content, removal from one is matched by removal from the other."

**Problem**: This sentence sits at the end of a lemma whose stated premise is *R-disjointness* (`{a : (a, d_A) ∈ R} ∩ {a : (a, d_B) ∈ R} = ∅`). Synchronised-edit documents share content history — their R-projections overlap — so they fall *outside* the lemma's precondition. The sentence asserts a Q0 result for a case the lemma did not (and cannot, under its premise) establish, with no derivation. This is precisely the reviser-drift pattern: a paragraph imagining a case the claim's precondition already excludes.

**Required**: Either remove the sentence, or promote the synchronised-edit case to a separately stated claim with its own one-line derivation (for shared `a`, `DELETED(a, d_A) ⟹ DELETED(a, d_B) ⟹ ¬CURRENT(a, d_B)`, falsifying conjunct 1; symmetric for conjunct 2). It does not belong as an unproven coda to the disjointness lemma.

### Issue 2: Essay/significance prose in structural justification slots

**ASN-0075, D-ORIG "Justification"**: "This matters operationally because it scopes recovery rights and accounting. The originating document is recoverable from the address; recovery operations can verify permissions against `origin`; royalty or attribution mechanisms have the data they need."

**ASN-0075, D-SYM "Justification"**: "This matches the design intent that correspondence between documents is a structural fact about shared content and not an asymmetric query over arguments."

**ASN-0075, D-IDENT "Justification"**: "The architectural significance is foundational."

**Problem**: These passages advance no reasoning toward the claims they sit under. D-ORIG's formal content is "`origin(a)` is determined on every output element"; the recovery-rights/royalty paragraph is motivational essay. D-SYM's formal content is the component-swap identity, already established by name-substitution; the "design intent" sentence is editorial. "The architectural significance is foundational" is vacuous editorializing. This is the accreted meta-prose the anti-bloat classifier targets — a reader must skip past it to reach the next claim.

**Required**: Delete the significance/motivation sentences. Keep only what derives or states a guarantee. (The genuine derived consequences under D-IDENT — link survival, transclusion integrity, each with cited premises — should remain; it is the framing prose around them that should go.)

### Issue 3: Redundant validity-justification embedded in the K.δ shorthand convention

**ASN-0075, D-DISCR, "A second bundling concerns document creation"**: "...The composite is valid by ValidComposite★: each elementary step satisfies its precondition at its intermediate state, and J0/J1★/J1'★ are vacuous because no K.α, K.μ⁺, or K.ρ steps appear."

**Problem**: The convention only needs to *define* `K.δ(d)` as shorthand for the precursor-account-plus-document composite. The trailing validity argument restates a generic property of any K.δ-only composite (vacuous coupling) that the reader already has from ValidComposite★. It is defensive prose explaining why the shorthand is well-formed rather than advancing the discrimination argument.

**Required**: Reduce to the shorthand definition (`K.δ(d) ≡ K.δ(A); K.δ(d)` with `A = inc(n_0, 2)`, `d = inc(A, 2)`). Drop the per-clause vacuity recitation.

## OUT_OF_SCOPE

### Topic 1: Three-or-more-document deletion reports and witness structure
The Open Questions raise reporting deletions across families of more than two documents and content deleted from both compared documents but current in a third. These are legitimate extensions requiring new witness machinery beyond the binary asymmetric pair — future ASN territory, not defects here.

### Topic 2: Restoration/recovery operation consuming SHOWDELETIONS output
The closing open question about a restoration operation reintroducing deleted content while preserving origin and link-resolvability is a separate operation on state, correctly deferred.

VERDICT: REVISE
