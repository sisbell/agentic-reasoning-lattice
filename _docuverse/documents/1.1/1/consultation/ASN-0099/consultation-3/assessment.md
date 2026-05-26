# Channel Assignment — ASN-0099 review-3

**Date:** 2026-05-26 16:42

## Issue 1: F1 and F12 listed in claims table but never labeled in prose
Reason: Pure bookkeeping fix internal to the ASN — either insert F1/F12 labels at the existing inline definitions or reclassify them as DEF in the table. No design intent or implementation evidence is involved.

## Issue 2: F10's cross-document ordering claim lacks derivation
Reason: The fix is to add citations to ASN-0034 (PrefixOrderingExtension) and ASN-0093 (CrossDocDisjointness) or to derive the cross-document step from those existing claims. Internal to the lattice; the dependencies are already formal properties.

## Issue 3: F9 frame citation imprecise for K.μ⁺ and K.μ⁻
Reason: The choice between "L preservation follows from effect-clause convention" and "ASN-0047 has a frame-clause gap" is a question about the formal specification convention used in ASN-0047, not about design intent or implementation behavior. The reviser can resolve by reading ASN-0047's framing convention and either citing it or flagging the gap.

## Issue 4: Filtered form behavior at out-of-range slot indices is informal
Reason: This is a definitional cleanup — make the out-of-range semantics explicit in the formal expression. The author's prose already states the intended interpretation ("unsatisfiable"); the fix transcribes that into the formal definition. Internal.

## Issue 5: Empty filter constraint set boundary not addressed
Reason: Standard boundary-case addition derivable from the vacuous universal over an empty set. No design or evidence input needed; just verify `findlinks_filtered(∅, Σ) = dom(Σ.L)` and state it.

## Issue 6: F8 conflates abstract determinism with implementation conformance
Reason: Refactoring the claim's referent (`findlinks` vs `result`) is a formal hygiene fix. The reviser can restate F8 against `findlinks` and note the implementation consequence via F2+F3 composition. Internal.

## Issue 7: Phase 1 formal definition's precondition incomplete
Reason: The prose already states the two preconditions; the fix lifts them into a `defined when` clause to match the companion `project` definition's form. Pure formal-hygiene fix internal to the ASN.

## Issue 8: F5 not exercised in the worked example
Reason: The worked example's existing structure already discriminates `α₂` from `α₃` by address regardless of value; the fix is a brief annotation pointing out that the match consults coverage, not Σ.C. No external input needed.
