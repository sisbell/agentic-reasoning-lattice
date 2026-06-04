# Review of ASN-0087

This is a mature note — the substrate composition (`K.λ ; K.μ⁺_L`), the precondition discharge of `ℓ ∉ ran(M(d))`, the D-CTG★ slice argument at arbitrary depth, the S2 two-part exclusion, the wp case split (including the reflexive route), and the per-state/boundary/transition invariant stratification all check out. The worked example's address-length arithmetic and prefix tests are correct. No correctness defects found. The remaining issues are the forward-reference/meta-prose patterns this note's `anti-bloat` classifier targets.

## REVISE

### Issue 1: Document-navigation meta-prose in *Inputs*
**ASN-0087, Inputs**: "the V-position `v_ℓ` is likewise system-derived, not a parameter — *its positioning rule stated once in Effect, its depth fixed per the M-DepthConv convention below*."
**Problem**: The substantive content is "`v_ℓ` is system-derived, not a parameter." The trailing clause is pure document-navigation — it tells the reader where the rule lives, not what it is. This pairs with *Preconditions* ("`v_ℓ` system-derived (see Effect)"), so two sections in different slots defer to *Effect* for the same positioning rule — the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Drop the "stated once in Effect / convention below" navigation. State that `v_ℓ` is system-derived; let *Effect* carry the rule without an advance pointer.

### Issue 2: M-DocFixity introduced by enumerating downstream consumers
**ASN-0087, Weakest Precondition**: "We establish here, once, *the document-set fixity that the rest of the ASN cites*: `dom(Σ'.M) = dom(Σ.M)` (M-DocFixity)."
**Problem**: A lemma's introduction should advance its meaning, not inventory its callers. "the document-set fixity that the rest of the ASN cites" is consumer-enumeration prose ("this is used by X, Y, Z") that rots as the note evolves and adds nothing to the derivation that follows it (M1 inclusion + K.λ frame + K.μ⁺_L effect).
**Required**: State and prove M-DocFixity directly. Delete "here, once, … that the rest of the ASN cites."

## OUT_OF_SCOPE

### Topic 1: Permission/ownership gating of referenced content
**Why out of scope**: The "No Permission Check" section correctly observes the substrate exposes no ownership state to consult. Access-control semantics over endset-referenced content are a future-layer concern, not a defect here; the section is a legitimate statement of what the operation does not do.

VERDICT: REVISE
