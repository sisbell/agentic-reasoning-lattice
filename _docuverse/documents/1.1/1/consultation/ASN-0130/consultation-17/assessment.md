# Channel Assignment — ASN-0130 review-17

**Date:** 2026-06-13 02:10

## Issue 1: The certificate's asserted class is not PD0's ST class
Reason: Internal. The note already commits to the correct semantics — PR5 defines the certified property as "every `Γ_D`-instantiation … is ⊤-stable" under the parameter reading, already establishes that this reading extends PD0's "ℕ literal" threshold to any bound ℕ value, already proves its soundness ("PD0's own ground … consumes only the fixity of bound values"), and already states PD0's rules certify a subclass of the extensionally stable terms. The fix is to name this property uniformly and correct PS2's mislabeled one-line summary so it matches what PR5 already commits — a consistency edit needing no design intent (the semantics are settled in-note) and no implementation evidence (PD0's aggregate side condition is already characterized in the note).

## Issue 2: PR-VIEW opens with motivation that precedes the load-bearing derivation
Reason: Internal. The fix reorders existing PR-VIEW content to lead with the PC3 derivation already present, and re-frames the udanax-green paragraph as a motivating aside. The review explicitly flags placement, not the existence or accuracy of the udanax-green claims, so no implementation verification (Gregory) is needed; it is a pure editorial reordering.

## Issue 3: The entry-point seal is deferred forward across several sections
Reason: Internal. The fix removes redundant discharge-by-seal forward references from PR0 and the commitments summary, keeping the single statement at PR-DISC. The seal mechanism and its needed anchor point are already in the note; this is editorial deduplication requiring no external channel.
