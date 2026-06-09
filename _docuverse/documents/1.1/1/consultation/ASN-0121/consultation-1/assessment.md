# Channel Assignment — ASN-0121 review-1

**Date:** 2026-06-08 18:44

## Issue 1: Reinvents a foundation concept as a fresh posited set
Reason: The fix is internal — ASN-0086's `nullified(Σ)` and its R6a monotonicity are foundation content already available to this ASN; grounding `addressable(Σ)` in it and citing R6a requires no design intent or implementation evidence, only correct reuse of the foundation.

## Issue 2: FL-REACH (d) overclaims membership from a single-slot match
Reason: Purely a logical correction against the ASN's own `sat` definition (AND of the four lifted criteria); strengthening the antecedent to full `sat(a, q, Σ)` is derivable from FL-DEF alone.

## Issue 3: FL-DIR asserts existence without a witness
Reason: Constructing an explicit link/request pair and checking both requests against FL-DEF is a self-contained mathematical exercise using only the ASN's definitions; no channel needed.

## Issue 4: No concrete worked example anywhere
Reason: Building a small store and tracing FL-DEF/FL-SND/FL-CMP/FL-WILD/FL-DIR over it is internal model construction; the abstract definitions fully determine the trace without external input.

## Issue 5: FL-CUR is tabled but never stated as a claim
Reason: Internal bookkeeping — stating FL-CUR with its one-line derivation as the conjunction of FL-SND and FL-CMP against `addressable(Σ)` follows directly from claims already present.

## Issue 6: `coverage(·)` applied to request components whose type is left unreconciled
Reason: Reconciling span-set (`⟦·⟧`, ASN-0053) with endset `coverage` (ASN-0043) and stating the address-set equality is a type-discipline fix derivable from the two cited foundations; no design or implementation question is involved.

## Issue 7: Empty (non-wildcard) request component left unaddressed
Reason: The abstract semantics (`lift(e, ∅) = false ⇒ ∅`) are forced by the AND-of-ORs structure and statable internally, but Gregory can confirm whether the back end actually distinguishes an empty constrained slot from NOSPECS — relevant because Q15 already shows wildcard/empty conflation in the implementation.
Gregory question: When a search request supplies a constrained endset slot whose span-set is empty (coverage `∅`), does the back end treat it the same as a NOSPECS/wildcard slot, or does it yield an empty link-set for that slot — and is this distinct from the all-wildcard handling in `intersectlinksets` (Q15)?
