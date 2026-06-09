# Review of ASN-0121

## REVISE

### Issue 1: FL-WP's case partition is not exhaustive over fresh links in the full vocabulary

**ASN-0121, FL-WP cases (a) and (c)**: "We call the link *ordinary (non-retraction)* exactly when its committed type endset does not fall in the retraction coverage class — `coverage(Σ'.L(ℓ).e₃) = coverage(Θ) ∉ [coverage(R)]`" ... and case (c) "whose type endset *does* fall in the retraction coverage class — `coverage(Θ_b) ∈ [coverage(R)]` — so by ASN-0086's slot-3 test `b ∈ L_R^{Σ'}`".

**Problem**: FL-WP claims to characterize the three result-changing K.λ cases, but the partition by coverage class alone leaves admissible fresh links uncovered. Two leaks:

- **Arity > 3.** `L_R^Σ` is triple-restricted (`|Σ.L(a)| = 3`, ASN-0086; the ASN itself notes "a higher-arity K.λ at `K ~ R` enters `dom(Σ'.L)` but not `L_R` (triple-restricted)"). A fresh link with arity `N > 3` and slot-3 coverage in `[coverage(R)]` is *not* "ordinary" by case (a)'s definition, yet case (c)'s derivation `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}` is false for it (it never enters `L_R`). Its true wp is the case-(a) form (since `L_R` is unchanged), but no stated case licenses that. Such a link is still result-changing: a type-`Θ` query touching the retraction class returns it (sat tests `coverage(e₃)`, not `L_R` membership).

- **Non-empty from-slot.** The ASN explicitly declines the unit-depth retraction discipline ("This ASN works over the *full* ASN-0047 transition vocabulary, which imposes no such discipline"), yet case (c) fixes the committed value as `(∅, G', Θ_b)` "following ASN-0086's RetractionDirectionality convention, empty from-slot." A discipline-free K.λ may commit an arity-3 retraction-coverage link with non-empty from-endset `F_b`; case (c)'s matching conjunct `lift(∅, q.F)` is then the wrong test (should be `lift(F_b, q.F)`).

**Required**: Re-cut the partition on `L_R^{Σ'}` membership rather than coverage class: case (a) = `ℓ ∉ L_R^{Σ'}` (which subsumes non-retraction-coverage *and* arity ≠ 3), case (c) = `ℓ ∈ L_R^{Σ'}` (arity 3 ∧ retraction-class slot-3). Replace `lift(∅, q.F)` in case (c) with `lift(F_b, q.F)` for the link's actual committed from-endset, so the wp holds for retraction links regardless of from-slot content.

### Issue 2: FL-WP — the load-bearing hazards are derived but never exercised concretely

**ASN-0121, FL-WP and "A worked instance"**: Traces 1–6 verify FL-SND, FL-CMP, FL-DIR, FL-TYP, FL-WILD, FL-EMP, FL-RET, and FL-RES against the concrete store, but none of FL-WP's three cases is exercised.

**Problem**: FL-WP is the most intricate and most recently revised claim, and its two subtle, load-bearing terms — the ghost-pre-coverage conjunct (`ℓ ∉ nullified(Σ')` failing because a standing retraction tuple already covers the freshly-allocated `ℓ`) and the self-retraction conjunct `b ∉ coverage(G')` — are exactly the kind of non-obvious behavior the review standards require to be pinned against a specific scenario. They are derived in prose but never instantiated. A concrete instance (e.g. a standing retraction whose to-coverage names the future address `ℓ`, so `sat(ℓ,q,Σ')` holds yet `ℓ ∉ findlinks(q,Σ')`) would demonstrate that the addressability conjunct is non-vacuous in the way the derivation claims.

**Required**: Add a worked trace exercising at least the case-(a) ghost-pre-coverage hazard and the case-(c) self-retraction term against the concrete store, verifying the wp predicts answer membership.

## OUT_OF_SCOPE

(none beyond the Open Questions already recorded, which correctly defer version-scoped inquiry, the V-spec/I-address correspondence invariant, and cross-federation completeness to future ASNs.)

VERDICT: REVISE
