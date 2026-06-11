# Channel Assignment — ASN-0128 review-4

**Date:** 2026-06-10 18:48

## Issue 1: `retract_stale`'s "voiding the batch rather than truncating it" is contradicted by its own parenthetical
Reason: Internal fix. The contradiction is between two sentences of the note's own contract; resolving it is a design choice between the two repairs the review already names (condition the void claim on no interleaved allocation, or check P0 once at batch start and refuse to issue), both fully expressible from the note's existing P0/interleaving machinery. Neither authority has a batch-retraction operation to consult.

## Issue 2: The wp analysis stops at Case 1 — no consolidated contract or weakest precondition for idem=⊤ `Emit_K`
Reason: Internal fix. All the ingredients are already in the note — I1's per-branch behavior, I3's born-nullified caveat, I4's lands-active fact, DR's discipline argument — and the required work is consolidation plus a wp derivation in the style DR already demonstrates. No new design-intent or implementation question arises.

## Issue 3: R-C0's BH4 compatibility row is stipulated, never argued — and the Multi requirement is unused by BH4's own machinery
Reason: Internal fix. The `idem = ⊥` rationale is derivable from I1's hit semantics (a dedup hit returns the incumbent's address, so re-emission cannot refresh age), and the Multi clause is exercised by nothing — the reviser can state the former and relax or argue the latter from the note's own catalog. BH4 is this note's invention, so neither authority has standing evidence on it.

## Issue 4: Enumeration predicates match their arguments inconsistently — denotation-keyed forward, coverage-keyed reverse — and AD's regime taxonomy is silent on it
Reason: The argument-matching rule should follow the substrate's actual matching doctrine, which the note grounds in Gregory's I-address-intersection discovery; whether the implementation matches from-side and to-side query arguments symmetrically is evidence that decides between unifying on coverage-keying or defending the asymmetry. The reconciliation with I0's subtree-assertion reading is then internal, in the style of D2's bridge.
Gregory question: When udanax-green answers a link-discovery query (e.g., find-links with from-set and to-set patterns), does it match the from-side and to-side arguments symmetrically by span/I-address intersection, or does either side require exact-address (rather than containment) matching?
