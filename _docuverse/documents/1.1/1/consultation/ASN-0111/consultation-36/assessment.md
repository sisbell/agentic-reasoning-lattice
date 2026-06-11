# Channel Assignment — ASN-0111 review-36

**Date:** 2026-06-10 22:23

## Issue 1: The structural screen is not evaluable on its declared domain
Reason: The fix is internal — T4-validity is already established as necessary (L0b is cited in the note's own prose), its decidability from the address follows from the T4 constraints in ASN-0034 which the note already invokes, and the change is adding it as a guarding conjunct plus updating the claims table. No design-intent or implementation question is open.

## Issue 2: The insufficiency-of-address-tests claim is misquantified and unwitnessed
Reason: The fix is internal — the requantification is a logical correction, and the witness (`dom(Σ₀.L) = ∅` at the initial state of ASN-0047, which the note already cites for its standing precondition) discharges insufficiency in one line. The note already records Nelson's and Gregory's positions on totality; nothing further is needed from either.

## Issue 3: False statement about the codomain
Reason: The fix is internal — replacing the codomain-structure claim with the per-invocation statement `readlink(a, Σ) ∈ {Σ.L(a), ⊥}` follows immediately from the operation's own definition. Pure logic repair, no external facts involved.

## Issue 4: RL4's no-flattening corollary rests on an unconstructed existential
Reason: The fix is internal — the review specifies the two-state construction and the worked example already supplies every ingredient (the `c`/`a'` pair, K.λ's acceptance of any conforming value per ASN-0093, the K.λ frame, L12). Writing out the branch-and-rejoin proof requires only claims the note already cites, not new design or implementation evidence.

## Issue 5: RL5 is silent on the instability of `⊥`
Reason: The fix is internal — the asymmetry remark is witnessed by the note's own machinery: K.λ (ASN-0093) allocating a previously-unallocated frontier address flips that address's read from `⊥` to a link value, and the worked example's first-emission address is a ready-made instance. No channel needs to confirm that the store grows.

## Issue 6: Duplicated meta-prose (anti-bloat)
Reason: The fix is internal — purely editorial consolidation of duplicated insufficiency prose and forward pointers, with RL5 citing RL4 instead of restating it. No semantic content changes, so no consultation is needed.
