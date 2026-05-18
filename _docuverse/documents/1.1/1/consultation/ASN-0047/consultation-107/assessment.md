# Channel Assignment — ASN-0047 review-107

**Date:** 2026-05-18 07:01

## Issue 1: K.δ k=0 maximality precondition fails to isolate t's own allocator at "version of document" and deeper levels
Reason: The fix is internal — the ASN already commits to `A_v(d)` as per-document (in *Sub-allocator names*) and ASN-0034's T10a provides per-`(t, k)` uniqueness on each allocator's inc-chain. Replacing the broken maximality clause with a direct freshness predicate `inc(t, 0) ∉ E` discharged via T10a's per-`(t, 0)` uniqueness uses only machinery already present in the ASN and foundation.

## Issue 2: Logical fallacy in the inference justifying the #t' = #t conjunct
Reason: This is a pure logical defect — the inference from T10a.1's within-allocator length uniformity to between-allocator length distinction is invalid, and the "unique allocator" claim contradicts the ASN's own description of per-document `A_v(d)`. The fix (remove the inference, or remove the paragraph entirely if Issue 1's option (a) is taken) is internal.

## Issue 3: Forward-reference accretion in K.δ case (ii) k=0 precondition slot
Reason: Pure editorial reorganization — move per-conjunct justification from the precondition slot into a separate rationale paragraph, or omit it. The fix requires no external evidence.

## Issue 4: K.μ⁻ effect clause "at least one subspace contracts strictly" treated as derivable, but only verified informally
Reason: The fix is internal — making the chain `dom(M'(d)) ⊂ dom(M(d)) ⟹ dom(M(d)) ≠ ∅ ⟹ at least one V_S(d) ≠ ∅` explicit (or adding `dom(M(d)) ≠ ∅` as a stated precondition) uses only K.μ⁻'s own effect clause.

## Issue 5: ExtendedReachableStateInvariants verification matrix uses "frame" without distinguishing K.μ⁺'s amended form for L
Reason: Pure editorial clarification — annotate matrix entries to indicate that K.μ⁺ and K.μ⁻ "frame" entries on L refer to the amended forms whose `L' = L` conjuncts are introduced at the extended-state amendments. The fix requires no external evidence.
