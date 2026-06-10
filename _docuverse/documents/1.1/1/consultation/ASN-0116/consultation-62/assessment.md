# Channel Assignment — ASN-0116 review-62

**Date:** 2026-06-09 22:39

## Issue 1: F-SUB states a set equality its cited lemma does not establish
Reason: Neither channel is needed — this is a formal-corpus citation/derivation cleanup, not a question of design intent or implementation evidence. The ASN's own composite realization already supplies the missing ⊆ direction (its K.μ⁻ step retains the link subspace in full at `n'_{s_L} = n_{s_L}`, and its amended K.μ⁺ step adds only `subspace(v) = s_C` positions — clause (iv)), so no cross-subspace position is added or removed; alternatively the review itself supplies I3-CX's exact statement from ASN-0082 to cite. Both routes are internal to the formal development.

## Issue 2: K.μ⁺ precondition discharge omits the finiteness conjunct
Reason: Neither channel is needed — the omitted finiteness conjunct is pure formal hygiene, discharged by the standard invariant set the ASN already operates within (S8-fin gives `dom(M(d))` finite at the intermediate state, and K.μ⁺ adds finitely many positions — the block plus shifted suffix), or by citing ASN-0082's I3-fin. Nothing turns on design intent or implementation behavior.
