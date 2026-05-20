# Channel Assignment — ASN-0094 review-20

**Date:** 2026-05-20 02:53

## Issue 1: Case C of Sh4 proof claims a case that the Lemma rules out
Reason: The fix is derivable from the ASN's own content — Lemma — RetractionTargetNotOnChain (just proved in the ASN) plus R0 freshness already establish self-retraction is impossible. The revision is either to remove the self-retraction mention or note its vacuity by citing the Lemma.

## Issue 2: Case D definition contradicts its own substantive content
Reason: Pure internal inconsistency between the case definition's "non-empty subset" wording and the substantive analysis treating `leaving = ∅` as a Case D sub-case. The fix is a wording choice between widening Case D or routing the empty-leaving variant to Case B.

## Issue 3: Per-element argument cites Sh-conf clause (d) before clause (d) is gated
Reason: The fix is derivable from the ASN's own contract ordering specification. Either rephrase conditionally or restructure to separate correctness-of-C-computation (independent of clause (d)) from over-approximation-tightness (conditional on clause (d)).

## Issue 4: Disjoint-union cardinality cited but not derived
Reason: The derivation `|A ⊔ B| = |A| + |B|` is a standard consequence of NAT-card's strictly-increasing enumeration characterization (ASN-0034). The fix is to inline the derivation or cite the specific NAT-card consequence; both options work from upstream content already in scope.

## Issue 5: Prefix-suffix decomposition notation `a · w` is used without citation
Reason: The fix is derivable from ASN-0034's Prefix definition plus T0's comprehension — either define `·` locally as the suffix recovered via T0's comprehension under NAT-sub, or rewrite to use componentwise equalities directly. No external evidence needed.

## Issue 6: Coverage row `latest_K_for_addr` template — partiality return value collides with `to₁` totality
Reason: The ASN's own Codomain convention for partial templates and the `S_d = ∅ ⟹ ⊥` branch are already specified; the fix is presentational — add a consumer-side dispatch note or extend the Coverage walkthrough with an empty-`S_d` case.

## Issue 7: T0 axiom citation for tumbler length minimum is loose at AllocatedAddressAntichain Step 3.1
Reason: The fix is derivable from NAT-card's strictly-increasing enumeration of finite ℕ-subsets (ASN-0034). Inline a one-sentence citation to license the `n_1 < n_2 < n_3` decomposition from `zeros(x) = 3`.
