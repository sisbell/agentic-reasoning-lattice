# Channel Assignment — ASN-0099 review-8

**Date:** 2026-05-26 18:38

## Issue 1: Implementation Notes section is borderline scope
Reason: This is a scope/editorial decision about whether to retain non-normative implementation guidance. The fix is derivable from the ASN's own statement that conformance equals F2 ∧ F3 — no design intent or implementation evidence is at stake.

## Issue 2: The unfiltered=union identity uses misleading infinite indexing
Reason: Purely notational. The ASN already proves the union has finitely many non-empty terms; rewriting as a finite-bounded union with `N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}` uses only definitions and reasoning already present.

## Issue 3: Worked example doesn't exercise filtered/scoped variants or monotonicity claims
Reason: Mechanical extension of the existing instance against the ASN's own named claims. The instance, state transitions, and claim definitions are all in scope; verification is internal.

## Issue 4: A1 axiom is a meta-axiom workaround for ASN-0047
Reason: This is a spec-consistency cleanup. Either path (proposing an ASN-0047 amendment or restating A1 with explicit closure premise) is editorial work over the published frames, which the ASN already enumerates. Design intent isn't in dispute and implementation evidence doesn't bear on which operations the published frames cover.

## Issue 5: F10's cross-document ordering claim is potentially misleading
Reason: One-sentence clarification distinguishing T1 lexicographic order from K.λ chronological order. Both facts are already derived inside F10's discussion; the fix consolidates what's there.

## Issue 6: F9 doesn't cover K.ρ (and other non-K.μ, non-K.λ operations)
Reason: The ASN already enumerates which operations modify which state components (in F9's derivation) and identifies K.λ as the unique L-modifier. The corollary is a consolidation of facts already present — no new evidence or intent needed.
