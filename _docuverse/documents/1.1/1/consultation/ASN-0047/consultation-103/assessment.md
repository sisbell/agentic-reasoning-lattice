# Channel Assignment — ASN-0047 review-103

**Date:** 2026-05-18 04:12

## Issue 1: K.δ k=1 discharge prose conflates T1 and T2 cases
Reason: Derivable internally. T10a's per-(t, k') uniqueness (foundation, ASN-0034) makes inc(t, 1) fire at most once per t, forcing K.δ k=1 to always be a T2 spawn step on A_v(t); subsequent versions arise from K.δ k=0 events (T1 siblings) on prior versions. The correction follows from T10a + K.δ's own spec.

## Issue 2: A_v(d) activation discipline is implicit
Reason: Both channels needed. The activation discipline (at d's creation K.δ vs. at first K.δ k=1 on d) is a design choice requiring Nelson's intent on whether version sub-allocators are latent at document birth, and Gregory's evidence on what the implementation does at `docreatenewdocument` vs. `docreatenewversion`.
Nelson question: Did the design intend that a document's version-allocation capability exists from the moment the document is created, or that it is brought into being by the first CREATENEWVERSION operation on that document?
Gregory question: In udanax-green, when a document is created (`docreatenewdocument`), is any version-sub-allocator state established at that moment, or does the version allocator only become observable when `docreatenewversion` is first invoked on the document?

## Issue 3: SubAllocatorAxiom's T10a.6 non-violation paragraph mixes meta-prose with substance
Reason: Derivable internally. The structural disjointness statement is substantive content that folds into SubAllocatorAxiom's body; the why-explanation is pure meta-prose to remove. No external input needed.

## Issue 4: L3's relationship-to-foundation essay content
Reason: Derivable internally. The reachability-closure derivation is recoverable from K.λ's precondition and L12 (both already in this ASN); the higher-arity defensive note and citation are removable without losing content.

## Issue 5: ValidComposite★ notation disambiguation is a use-site inventory
Reason: Derivable internally. Notation choice is a presentational decision (e.g., `→ₐ` vs. `→*`) within the ASN's own scope.

## Issue 6: K.μ⁻ has a redundant precondition
Reason: Derivable internally. Strict-contraction over V_S(d) ≠ ∅ implies dom(M(d)) ≠ ∅ directly; the redundancy is provable from the existing K.μ⁻ amendment.

## Issue 7: D-SEQ★ derivation dangling reference to ASN-0036's D-CTG-depth
Reason: Derivable internally. The D-SEQ★ derivation already stands on D-CTG★ + S8-fin + S8a; the reference is removable without consequence.

## Issue 8: K.μ⁻ exhaustiveness lemma proves cases that are immediately excluded
Reason: Derivable internally. The lemma can be restructured to derive case (a) directly from D-CTG★ + D-MIN★ + D-SEQ★ at the post-state; restructuring is internal to the proof.

## Issue 9: ExtendedReachableStateInvariants "Foundation invariants" subsection duplicates the main iteration
Reason: Derivable internally. Restructuring (consolidating per-transition vs. per-invariant) is a proof-organisation decision within the ASN's scope.

## Issue 10: Worked example for K.δ k = 1 is missing
Reason: Derivable internally once Issues 1 and 2 are resolved. The example instantiates the chosen activation discipline and spawn-step characterisation on the existing Fork trace; no external input is needed beyond what 1 and 2 supply.
