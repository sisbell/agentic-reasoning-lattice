# Channel Assignment — ASN-0043 review-62

**Date:** 2026-05-14 15:49

## Issue 1: L9 Case B's "frontier" assumes a single allocator
Reason: The fix is a proof restructuring exercise — the reviewer supplies a concrete allocator-agnostic construction (pick existing `b ∈ dom(Σ.L)` with `home(b) = d'`, use T10a.7/T10a.8 + L-fin + chain-prefix-preservation). All cited machinery is already in this ASN and ASN-0034; no design intent or implementation evidence is needed.

## Issue 2: L11b's sibling-chain wording is opaque
Reason: Pure wording fix with the replacement text given verbatim in the review. The mathematical content is unchanged — only the metalanguage is being simplified. No external input is needed.

## Issue 3: L1c's k₁ ∈ {1, 2} is loose given the chain-origin constraint
Reason: The argument is a structural derivation from TA5(d) (which `inc` step types add a separator zero) and T4b parsing (where zeros land determines field boundaries) — both internal to ASN-0034. The choice between tightening to `k₁ = 2` and adding a remark is an authorial decision derivable from the ASN's own content.

## Issue 4: Worked example L8 verification leaves the coverage-vs-span-set distinction abstract
Reason: This is a span-algebra question about whether the prefix interval `{t : g ≼ t}` admits two distinct span decompositions, answerable from ASN-0034's span definitions and ASN-0043's `coverage` definition. The fallback (drop the parenthetical) is a writing decision. Neither design intent nor implementation evidence informs the choice.
