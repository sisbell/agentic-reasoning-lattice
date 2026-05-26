# Review of ASN-0087

## REVISE

### Issue 1: Worked example imprecisely describes coverage

**ASN-0087, "A Worked Example"**: "e₁ = {(a₁, δ(1, #a₁))} — covers {a₁} by PrefixSpanCoverage (ASN-0043)."

**Problem**: PrefixSpanCoverage (ASN-0043) states `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` — the *prefix-closed subtree* of x, not the singleton {x}. The coverage of e₁ includes a₁ plus every tumbler extending a₁ (e.g., [a₁, 1], [a₁, 1, 1], etc.). The same imprecision repeats for e₂ ("covers {a₃}") and e₃ ("covers {τ}"). The subsequent intersection computation `{a₁} ∩ {a₁, a₂, ℓ} = {a₁}` then writes coverage(e₁) as {a₁} when in fact `coverage(e₁) ∩ ran(Σ'.M(d)) = {t : a₁ ≼ t} ∩ {a₁, a₂, ℓ}`. The intersection happens to equal {a₁} (since a₁ ⋠ a₂ and a₁ ⋠ ℓ), but the coverage labelling is wrong.

**Required**: State coverage as `{t : a₁ ≼ t}` per PrefixSpanCoverage, then derive the intersection explicitly using prefix tests against each element of `ran(M(d))`. The concrete example is the spec's verification of its own claims — it must be computed correctly.

### Issue 2: "Sibling versions" terminology contradicts the substrate's version semantics

**ASN-0087, "A Worked Example"**: "d = [1, 0, 1, 0, 1] and d' = [1, 0, 1, 0, 2] — sibling versions under the same account."

**Problem**: By ASN-0047's K.δ classification, a *version* of d is produced by `inc(d, 1)`, which appends a positive component: a version of d would be `[1, 0, 1, 0, 1, 1]` (with d as a prefix). Here `d' = [1, 0, 1, 0, 2]` is produced by `inc(d, 0)` (or a different K.δ k=0 path at D-field allocation), so d' is a *sibling document* under the same account, not a version of d. K.δ explicitly labels k=0 as "sibling" and k=1 as "version" — these are distinct.

**Required**: Replace "sibling versions" with "sibling documents".

### Issue 3: Internal editing note embedded in M-DiscSymmetry claim

**ASN-0087, Claims Introduced (M-DiscSymmetry)**: "(M-Disc was previously asserted as a separate claim restating LP12 at Σ'; it has been removed as redundant — LP12 is a theorem at every reachable state, and the MAKELINK-specific reduction to pre-state predicates is captured by M-WP.)"

**Problem**: This parenthetical is a revision-history annotation, not a claim about MAKELINK. It describes what was deleted rather than what is being asserted. A specification reader should not need to know the editing history to understand the current claim.

**Required**: Remove the parenthetical (or relocate to a separate revision-history note outside the claims table).

### Issue 4: S2 preservation argument uses imprecise language

**ASN-0087, "Invariant Preservation" (S2 row)**: "adding {v_ℓ ↦ ℓ} cannot collide with any existing image"

**Problem**: S2 (ArrangementFunctionality) requires uniqueness of the image for a given V-position, not injectivity — distinct V-positions may map to the same I-address (per S5). The correct argument is that v_ℓ is not in the existing *domain*, so no domain collision occurs and functionality is preserved. The phrase "cannot collide with any existing image" suggests an injectivity argument, which is not what S2 demands.

**Required**: Rephrase as "v_ℓ ∉ dom(Σ.M(d)) by D-SEQ★ … so v_ℓ enters dom(M'(d)) fresh, preserving functionality of M'(d)".

## OUT_OF_SCOPE

The Open Questions section appropriately defers protocol-layer atomicity, future-document discoverability, MAKELINK-invocation distinguishability, and limiting-case type-endset questions to subsequent ASNs. No additional out-of-scope items.

VERDICT: REVISE
