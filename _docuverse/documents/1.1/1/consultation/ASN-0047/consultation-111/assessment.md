# Channel Assignment — ASN-0047 review-111

**Date:** 2026-05-19 09:14

## Issue 1: Foundation axioms claimed as new in Properties Introduced table
Reason: Pure bookkeeping inconsistency between the body text (which correctly attributes the three axioms to ASN-0093) and the summary table. Fix is restructuring the table — derivable from the ASN and its declared foundation source.

## Issue 2: L0 C-clause attribution
Reason: Table contradicts the body text, which already correctly attributes both clauses to ASN-0093's L0. Pure attribution fix internal to the ASN.

## Issue 3: K.δ k=0 frontier requirement under-specified for K.δ discharge
Reason: Formal proof question about whether `inc(t, 0) ∉ E` plus the other K.δ k=0 conjuncts force `t` to be its sub-allocator's frontier, or whether the precondition needs strengthening. Resolvable from the ASN's own T10a discipline and K.δ structure.

## Issue 4: Initial state existential consistency
Reason: Asks for an explicit Σ₀ invariant verification subsection consolidating what's already scattered through the proof. All invariants and Σ₀'s composition are defined within the ASN.

## Issue 5: Bijection equation interpretation needs disambiguation for empty domains
Reason: Asks to make the empty-domain exclusion explicit. K.μ~'s bijection equation, admissibility clauses, and its K.μ⁻+K.μ⁺ decomposition (which already requires `dom(M(d)) ≠ ∅` via K.μ⁻) are all in the ASN. Derivable internally.

## Issue 6: V-position uniqueness check at link arrangement
Reason: Restructures an existing argument into two separate disjointness checks. All facts cited (TS4, SC-NEQ, T3, S3★-aux) are established in the ASN; pure expositional refactor.
