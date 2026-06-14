# Review of ASN-0131

The technical substance of this note is, to its credit, rigorous. I checked the worked instance (the field-agreement argument seating `θ` disjoint from content is sound; the width-2 first span of `e₁` correctly covers `[a₂, a₄)` via `shift(a₂,2)=a₄`), the union-distributivity proof, the contraction weakest-precondition (RE-CWP), the retraction net-effect, transclusion blindness, and the boundary cases. These hold. The findings below are therefore mostly about claims that outran their prose and about residue this `anti-bloat`-flagged note still carries.

## REVISE

### Issue 1: RE-EXST is an orphaned claim — no prose section derives it
**ASN-0131, Claims table**: "RE-EXST | Existence-of-anchoring deliverable — by withholding identity the answer certifies the *presence and shape* of anchoring without making it followable; the foundation's existence/discovery axis (query mode: fixed vs arrangement-resolved) and the designer's existence/discovery axis (deliverable: structure vs named-and-followable) are orthogonal — RE is discovery on the first, existence-of-anchoring on the second"

**Problem**: Every other introduced claim has a prose home: RE-SND/RE-CMP in "Soundness and completeness," RE-SEL in "Existence and discoverability," RE-UNIT in "The unit of the answer," and so on. RE-EXST does not. The section "Existence and discoverability: which side does this answer for?" establishes *only* RE-SEL (`sel = findlinks_V ∩ addressable`, hence discovery-anchored). It never introduces, defines, or argues a *second* "designer's existence/discovery axis," and it never argues the orthogonality of two axes. The phrases "existence-of-anchoring deliverable," "designer's axis," and "orthogonal" appear *only* in this table row. The claim's substantive content ("withholding identity certifies presence and shape without making it followable") is a verbatim restatement of RE-UNIT; the remainder is an undefined taxonomy asserted as a structural fact ("are orthogonal") with no derivation. A claim labeled "introduced" that asserts a non-trivial orthogonality with no supporting argument is precisely a derived guarantee stated without derivation — and, in this `anti-bloat` note, it is a meta-framing surviving in a structural slot after its prose was removed.

**Required**: Either (a) restore a prose paragraph that *defines* the deliverable axis and *argues* its independence from the query-mode axis, or (b) cut RE-EXST, folding its only non-redundant phrasing into RE-UNIT. Given the note's anti-bloat posture and that the substance duplicates RE-UNIT + RE-SEL, (b) is the cleaner fix.

### Issue 2: Redundant claims and a duplicated passage (anti-bloat)
**ASN-0131, Claims table**: "RE-DET | Determinism — `RE(W, d, Σ)` is a function of `(W, d, Σ)`" alongside "RE-LOC | Locality — for fixed `(W, d)`, `RE` is a function of `(Σ.M, Σ.L)` alone."

**Problem**: RE-LOC logically entails RE-DET. If `RE` depends, for fixed `(W,d)`, only on `(Σ.M, Σ.L) ⊆ Σ`, then across varying inputs it is a function of `(W,d,Σ)`. RE-DET's bare content ("is a function of its arguments") is moreover near-tautological for any pure query. RE-LOC carries the substantive narrowing (no dependence on `Σ.C`, `Σ.E`, `Σ.R`); RE-DET adds only a determinism *gloss*, not a separable guarantee. Two claims where the weaker is subsumed by the stronger.

A second instance: the retraction section makes the same R6a/R6c point twice. Early — "Retraction is permanent at the *link* level — once nullified, a link stays nullified (R6a) … the only way an identical anchoring value re-enters the store is by emitting a *fresh* link with a new identity (R6c)" — and again, fully developed, under "Two senses of permanence must therefore be kept apart. The *specific retracted link's* membership in `addressable` is gone forever (R6a) … the *pair value* `(i, e)` is not permanently gone: an identical value re-enters … by emitting a freshly emitted link with a new identity (R6c)." The later paragraph supersedes the earlier (it adds the pair-value/link-level distinction); the early preview can be cut.

**Required**: Drop RE-DET (or merge its determinism note into RE-LOC's one line). Cut the early permanence preview, keeping the developed "Two senses of permanence" paragraph.

### Issue 3: A universal claim immediately contradicted by its own exception
**ASN-0131, "Under link emission"**: "Either way the move is monotone — a fresh emission can only add pairs, never remove one … Retraction is the distinguished sub-case in which the emitted link is a *withdrawal*; there the same `K.λ` machinery produces a *net* removal, which we take up now."

**Problem**: "a fresh emission can only add pairs, never remove one" is stated unconditionally, then the very next sentence exhibits a fresh emission (retraction) that nets a *removal*. A retraction *is* a `K.λ` emission, so the universal is literally false of it. The intended distinction — the *emission qua add* contributes `b`'s pairs, while the *nullification side-effect* (only for retraction-typed links) removes `ℓ` — is real and handled correctly two paragraphs later, but it is left implicit exactly where the universal is asserted, so the universal reads as contradicted by its stated exception.

**Required**: Scope the claim — "a *non-retraction* (`K ≁ R`) emission can only add pairs, never remove one" — and let the retraction sub-case stand as the `K ~ R` complement.

## OUT_OF_SCOPE

### Topic 1: The Open Questions are correctly placed
**Why out of scope**: The deferred items — entirety vs touching-spans surfacing (OQ1), rendered-into-V-order answers (OQ3), intersection-composability under non-injective arrangements (OQ4, M13/M14, ASN-0058), completeness against a non-co-resident link store (OQ5, the BEBE layer), type-slot-against-content meaning (OQ6), and link-subspace regions (OQ7) — are each genuinely new territory, not gaps in this ASN. The operation itself is fully specified for the content-subspace region; these defer *meaning* or *extension*, not the operation. No action needed. In particular, OQ6 is the right home for the one place RE-RET's forward half is conditional (`coverage(Θ) ∩ dom(Σ.C) = ∅`); the note correctly carries that as a hypothesis rather than overclaiming.

VERDICT: REVISE
