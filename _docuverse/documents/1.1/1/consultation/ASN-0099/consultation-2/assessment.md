# Channel Assignment — ASN-0099 review-2

**Date:** 2026-05-26 16:29

## Issue 1: F11 derivation uses single-step L12 for a multi-step claim
Reason: Pure formal bookkeeping — invoke ASN-0098's LP13/LP3★ (already-formalized multi-step lemma) or write explicit induction. Derivable from cited dependencies alone.

## Issue 2: F8 and F9 state essentially the same proposition
Reason: Internal restructuring choice (merge vs. sharpen as K.μ frame condition). All needed material is in ASN-0099 and ASN-0093; no design intent or implementation evidence required.

## Issue 3: `result(I, Σ)` vs `findlinks(I, Σ)` notational distinction not formal
Reason: Pure formalism choice — either collapse `result` into `findlinks` or introduce it as a distinct implementation-output symbol with F2/F3 as conformance obligations. Internal.

## Issue 4: Filter-to-union conversion lacks explicit slot index range
Reason: Notational fix — pin the index range and specify behavior when `i > |L(a)|`. The natural reading (constraint unsatisfiable, link excluded) is derivable from the existing definitions plus L3 (ASN-0043).

## Issue 5: F5 wording "are independent" is ambiguous
Reason: Pure rewording — recast as a property of the match predicate rather than the result sets. No external input needed.

## Issue 6: Empty link store boundary not addressed
Reason: One-sentence addition citing ASN-0047's L₀=∅. Derivable from the comprehension's definition; no channel input required.

## Issue 7: Worked example does not exercise F11
Reason: Extend the existing instance with a K.μ⁻ step and recompute. The K.μ⁻ semantics is in the ASN-0093/operations layer already cited; example construction is internal expository work.

## Issue 8: Connection to ASN-0098 LP12 unstated
Reason: Pure cross-reference — state that `findlinks(ran(Σ.M(d)), Σ) = {a : discoverable_from(a, d, Σ)}`. Both sides are defined in the cited ASNs; no external input needed.
