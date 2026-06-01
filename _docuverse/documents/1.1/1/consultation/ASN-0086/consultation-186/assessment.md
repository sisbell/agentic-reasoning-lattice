# Channel Assignment — ASN-0086 review-186

**Date:** 2026-06-01 12:36

## Issue 1: Forward reference into not-yet-defined notation in "state-local-conforming state"
Reason: Pure document-ordering fix — swap the two definitions so "(b)–(c)" and the containment chain resolve backward. Both definitions and the antichain machinery are already present in the ASN; no design intent or implementation evidence is required.

## Issue 2: Dangling term — "full state space" introduced, never consumed
Reason: Internal editorial fix — the term has no downstream consumer, while the `↝*` closure clause does; whether to drop the named noun phrase is settled by inspecting the ASN's own later usage. No external channel needed.

## Issue 3: Duplicate statement of coverage-class indexing
Reason: Internal redundancy — the `L_K^Σ` definition and TypeEquivalence already establish coverage-class indexing; collapsing the third restatement is derivable from the ASN's own definitions.

## Issue 4: Defensive "not a gating condition" prose in Definition — Nullify
Reason: Internal anti-bloat fix — R-Scope already proves arity-independence and the gating set (P0/P1/PC) is stated separately, so reducing the defensive paragraph to a one-clause pointer needs only the ASN's own content.

## Issue 5: Computability re-argued at length inside Definition — ActiveSubset
Reason: Internal de-duplication — CoverageEqualityDecidable and L-fin are already named lemmas in the ASN; stating computability once and citing them is fully derivable from existing content.
