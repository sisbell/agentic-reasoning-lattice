# Regional Review — ASN-0034/OrdinalDisplacement (cycle 2)

*2026-04-23 00:11*

### OrdinalDisplacement invokes `0 + 1 = 1` but does not declare NAT-closure
**Class**: REVISE
**Foundation**: NAT-addcompat axiom `(A n ∈ ℕ :: n < n + 1)`; NAT-closure's additive identity `(A n ∈ ℕ :: 0 + n = n)`.
**ASN**: OrdinalDisplacement, "Promote `n ≥ 1` to `n ≠ 0`" paragraph: *"NAT-addcompat's `(A n ∈ ℕ :: n < n + 1)` at n = 0 gives `0 < 1`."*
**Issue**: Instantiating `n < n + 1` at `n = 0` literally yields `0 < 0 + 1`, not `0 < 1`. The rewrite from `0 + 1` to `1` requires NAT-closure's additive identity `0 + n = n` at `n = 1`, exactly the step ActionPoint performs explicitly ("NAT-closure posits 1 ∈ ℕ directly, licensing its additive identity … to be instantiated at n = 1; this gives the equality 0 + 1 = 1, and rewriting …"). OrdinalDisplacement performs the same rewrite silently and omits NAT-closure from its Depends list. Either the step is ungrounded, or the Depends list is incomplete relative to what the proof uses.
**What needs resolving**: Either make the `0 + 1 = 1` rewrite explicit and add NAT-closure to OrdinalDisplacement's Depends (matching ActionPoint's treatment), or replace the anchor with one whose citation genuinely delivers `0 < 1` in a single step.

VERDICT: REVISE
