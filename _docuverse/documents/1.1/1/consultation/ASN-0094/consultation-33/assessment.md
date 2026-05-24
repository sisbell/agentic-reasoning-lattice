# Channel Assignment — ASN-0094 review-33

**Date:** 2026-05-23 18:12

## Issue 1: No catalog row added for `c_G = *`
Reason: Choosing the shape tuple requires knowing both the designer's intent for `citation.depends` (target domain, idempotency, from-slot cardinality) and the implementation's actual emission shape.
Nelson question: What was the intended shape for `citation.depends` — specifically, what does the from-slot represent, does the to-slot target documents or tuples, and is the relation meant to be idempotent (set-of-targets) or non-idempotent (sequence of dependency-events)?
Gregory question: In udanax-green, what does the `citation.depends` emission produce for `(F, G, K)` — specifically the cardinalities and address kinds in F and G, and whether duplicate emissions with identical slot-sets are suppressed or admitted?

## Issue 2: No template family for `c_G = *`
Reason: Retraction's catalog row already establishes the re-formulation pattern for `c_F = *` (using `slot_addrs(F_τ)` set bodies with membership/set-equality predicates per template role); the symmetric G-side re-formulation is derivable from that existing pattern plus Sh5(b)'s signature derivation rule.

## Issue 3: Backward compatibility for legacy single-target `citation.depends` unaddressed
Reason: Whether legacy emissions exist depends on whether `citation.depends` was previously registered (lifetime constancy forbids re-registration), which is an implementation-state question; the `match(1, *)` definitional point is internal but the legacy-vs-fresh status is not.
Gregory question: Is `citation.depends` currently registered in udanax-green's substrate (and if so, with what shape), or does the patch describe a fresh registration at a new K?

## Issue 4: Sh1, Sh3, Sh4 preservation arguments not extended
Reason: The Sh4 contract clause (i.a) already contains an explicit multi-slot generalization paragraph for F-side `c_F = *` using per-element AllocatedAddressAntichain; the G-side version is a symmetric textual application of the same argument, derivable from the ASN's own content.

## Issue 5: EffectiveWpSimplification interaction with the new shape
Reason: The corollary breaks if the new shape's coverage class is `~`-equivalent to `[R]`; confirming disjointness is a design-intent question about whether `citation.depends` is a retraction-class relation.
Nelson question: Is `citation.depends` intended to be coverage-equivalent to the retraction type R (i.e., does it carry retraction semantics under the relational vocabulary), or is it a distinct relation whose coverage class is disjoint from `[R]`?
