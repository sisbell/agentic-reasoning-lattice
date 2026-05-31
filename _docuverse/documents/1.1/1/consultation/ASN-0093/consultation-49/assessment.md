# Channel Assignment — ASN-0093 review-49

**Date:** 2026-05-31 09:22

## Issue 1: The load-bearing fact `M(d) = ∅` is asserted in prose but never enumerated or inductively discharged
Reason: Internal. The proposition `M(d) = ∅` follows directly from the substrate's own operation definitions (K.σ sets `M'(d) = ∅`; K.α/K.λ frame `M`); adding the M2 invariant ID, base case, and matrix row is mechanical bookkeeping fully derivable from the ASN's existing effect clauses.

## Issue 2: SD invariant carries naming-justification meta-prose
Reason: Internal. Dropping the ID-selection rationale and retaining the substantive derivation (`L0 + SC-NEQ + StoreT4Validity + T7`, full union justified by C1 + L0's C-clause) is an editorial trim using content already present in the note.

## Issue 3: Freshness lemmas appear as circular rows in the lemma-preservation matrix
Reason: Internal. Removing or rewriting the self-referential rows is a structural fix; the freshness obligations are already discharged at the K.α/K.λ binding preconditions and the SD matrix row, all derivable from the ASN's existing lemmas.

## Issue 4: Scope "Entity allocation" bullet enumerates a downstream primitive's internal composition
Reason: Internal. Removing the speculative component list of a future primitive is editorial trimming; the legitimate deferral statement requires no design-intent or implementation evidence.
