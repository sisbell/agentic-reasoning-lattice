# Channel Assignment — ASN-0058 review-18

**Date:** 2026-05-13 19:25

## Issue 1: V_{u₁}(d_s) notation extends ASN-0036 without explicit definition
Reason: Pure notation/definition hygiene — the fix is to either define V_S(d) explicitly or annotate the first use as a generalization. Derivable from existing ASN-0036 references and the surrounding text; no design intent or implementation evidence is at stake.

## Issue 2: M6(d) origin-traceability claim implicitly requires a ∈ dom(C)
Reason: Internal precondition tightening — M16 already works out the same #(N.0.U.0.D) < #a step using S7b/S7c, so the fix is to state the hypothesis at M6 and either inline or forward-reference. No external channel needed.

## Issue 3: M16 hypothesis on I-address structure is implicit in the claim text
Reason: Same family as Issue 2 — the proof already discharges the right machinery; the claim text just needs the explicit `a₁, a₂ ∈ dom(C)` precondition. Internal precision fix.

## Issue 4: M7's overlap case has a small gap at k = 0
Reason: Proof-case bookkeeping — split k = 0 (direct contradiction with v₁ < v₂) from k ≥ 1 (B2 violation). Wholly internal to the existing proof; no external evidence required.

## Issue 5: C0a's interpretation of J at indices beyond #t is unstated
Reason: Predicate well-formedness clarification — add one sentence noting J's membership requires j ≤ #t so the J non-empty / J = ∅ split is exhaustive. Internal proof-hygiene fix derivable from the existing structure.
