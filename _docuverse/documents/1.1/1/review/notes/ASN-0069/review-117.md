# Review of ASN-0069

## REVISE

### Issue 1: V11a's prefix-chain derivation rests on an unpublished foundation property
**ASN-0069, §"Composability: Fork of a Fork", V11a**: "The prefix relation `≼` is transitive — a generic property of the foundation Prefix relation (ASN-0034), which we cite here rather than re-prove (see foundation-gap note below)."

**Problem**: V11a's chain `d_src ≼ d¹_new ≼ ... ≼ d^k_new` is assembled by "`k − 1` applications of single-triple transitivity" of `≼`. But the foundation Prefix contract (ASN-0034) exposes only the definition `p ≼ q iff #p ≤ #q ∧ (∀i ≤ #p : qᵢ = pᵢ)` and the derived `p ≺ q ⟹ #p < #q`. Transitivity is **not** a published postcondition — the ASN says so itself in Open Questions ("transitivity is not a published postcondition... V11a depends on an unpublished foundation property"). A proof that knowingly rests on an unpublished claim is incomplete; the rigor standard forbids derived guarantees stated without derivation. Compounding this, the gap is documented in two places — the inline "(see foundation-gap note below)" pointer in V11a and the standalone "Foundation gap (V11a)" paragraph in Open Questions — which is the duplicated-forward-reference pattern this review mode targets.

**Required**: Prove `≼`-transitivity inline at V11a. From `p ≼ q` and `q ≼ r`: `#p ≤ #q ≤ #r` gives `#p ≤ #r`; for `1 ≤ i ≤ #p`, `i ≤ #p ≤ #q` so `rᵢ = qᵢ` (from `q ≼ r`) and `qᵢ = pᵢ` (from `p ≼ q`), hence `rᵢ = pᵢ`; therefore `p ≼ r`. One application makes V11a self-contained. Then delete both the inline forward pointer and the redundant Open Questions "Foundation gap" paragraph.

## OUT_OF_SCOPE

### Topic 1: Concurrent modification of source during fork
**Why out of scope**: The Open Questions correctly pose this as future territory beyond the sequential atomic transition axiom; it is not a defect in this ASN's sequential-model derivation.

### Topic 2: Living vs. snapshot fork semantics, transcludent sources, version-space coherence
**Why out of scope**: These are raised as open questions for downstream ASNs; this ASN commits to snapshot semantics (V10a, V4) and need not resolve the alternatives.

VERDICT: REVISE
