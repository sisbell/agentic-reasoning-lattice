# Channel Assignment — ASN-0043 review-65

**Date:** 2026-05-14 16:54

## Issue 1: L9's formal statement restricted to standard-triple links, while the worked example demonstrates arity 4
Reason: The fix is structural and derivable from the ASN alone — L3 already admits arity N ≥ 3 with non-emptiness required only at slot 3, so the witness construction generalizes by padding slots 4..N with ∅. No design-intent or implementation evidence needed.

## Issue 2: Worked example exercises L8 only reflexively
Reason: Adding a second ghost type `g'` and a fifth link `a₄` to exercise discrimination is purely constructional — disjointness of `{t : g ≼ t}` and `{t : g' ≼ t}` follows from PrefixSpanCoverage and T1, both already in-ASN.

## Issue 3: L1c clause (i) is presented as an axiom but its justification depends on clause (ii)
Reason: The fix is presentational — restructuring what is axiomatic versus derived within L1c. The substantive content (T4-validity follows from T10a.4 applied to the chain output) is already established in the ASN; choosing between the two restatement options is internal bookkeeping.

## Issue 4: L1c's chain-origin clause admits k₁ = 1 which is operationally unreachable
Reason: The ASN's own "Why k₁ = 1 is admitted but operationally unreachable" paragraph already proves k₁ = 1 contradicts t₀ = h(a). Tightening to k₁ = 2 is a formal cleanup using reasoning already in-ASN; no external evidence required.

## Issue 5: Worked example does not re-verify state-local invariants at intermediate states Σ_1, Σ_2
Reason: The required per-state verifications follow patterns already established in the L9 and L11b proofs (sibling-chain L1 via T10a.8, L1a via chain-prefix preservation, L1c via chain extension, L11a via T10a.7 injectivity). Mechanical application of in-ASN reasoning.
