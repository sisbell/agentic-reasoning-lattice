# Review of ASN-0100

This ASN is mature and substantively rigorous: the three-region partition, S2/S3★/D-SEQ★ discharge, boundary cases (j=0, append, empty document, empty-arrangement-vs-fresh-allocator sub-case), the wp analysis, and the projection-shift derivation all hold up under scrutiny. All cross-ASN references are to foundation ASNs (0034, 0036, 0047, 0058, 0082, 0093, 0098), so no self-containment violation. The remaining issues are duplication/accretion, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Invariant arguments duplicated within §Atomicity
**ASN-0100, §Atomicity and Canonical Order**: The grouped-by-component list ("Several per-state invariants ... preserved by frame ...") argues C-fin in full ("The pre-state has |dom(C)|<∞; each K.α firing adds exactly one address ... < ∞ at every intermediate") and argues L0's content clause in full ("For each freshly emitted a_k, subspace_I(a_k)=s_C by DisjointSubAllocatorChains ... So L0's content clause holds at every K.α intermediate"). The subsequent per-step bullet "After each of the n K.α firings" re-argues both: "Per-state invariants on C (C-fin, ...)" and "L0's content clause holds because subspace_I(a_k)=s_C (DisjointSubAllocatorChains, ASN-0093 ...)."
**Problem**: The same two arguments (C-fin finitude, L0-content-clause via DisjointSubAllocatorChains) appear in two different organizational schemes — the grouped-by-component list and the per-step list — in the same section. This is the "two paragraphs say the same thing in different words" pattern; the grouped list reads as a reorganization layer accreted on top of the pre-existing per-step list.
**Required**: Discharge each invariant in exactly one location. Either fold the grouped exceptions (S4, C-fin, L0-content) into the per-step K.α bullet, or have the per-step bullet cite the grouped argument rather than restate it.

### Issue 2: Effect statements stated verbatim in two sections
**ASN-0100, §Discovering the Three Effects (Effect One) and §The Operation: Formal Contract**: Effect One closes with "dom(C') = dom(C) ∪ {a_0,…,a_{n−1}}; C'(a_k) = v_k; C'(a) = C(a)"; the Formal Contract's "Effect — Content Store" restates the identical three-clause block. The same verbatim duplication holds between Effect Three's shift clause and the Formal Contract's "Shifted right" clause.
**Problem**: The discovery section legitimately carries the *reasoning* (freshness, Nelson Q-refs, the INS.chain-shift proof), but the bare effect equations are then repeated unchanged in the formal contract. The equation blocks are noise the reader must reconcile across two sections.
**Required**: Let §Discovering carry the motivation/derivation and defer the canonical equation statements to §The Operation: Formal Contract (or vice versa), so each effect equation appears once.

### Issue 3: "Definitional atomicity" justification repeated
**ASN-0100, §Atomicity and §Claims Introduced (INS.atomicity)**: The prose states "Composite-level atomicity is *definitional* — not an extra property the substrate must separately supply"; the claims-table entry repeats "composite-level atomicity is definitional under ValidComposite★ (ASN-0047)." A near-identical sentence also opens §Atomicity ("Composite-level atomicity is *definitional* ...").
**Problem**: A defensive justification (why atomicity needs no separate proof) is restated three times. One statement suffices.
**Required**: State the definitional-atomicity point once; remove the restatements.

## OUT_OF_SCOPE

(none — the ASN correctly bounds DELETE/COPY/REARRANGE/link-subspace/version/replication in §Bounding the Scope and §INSERT vs. COPY, and does not over-specify them.)

VERDICT: REVISE
