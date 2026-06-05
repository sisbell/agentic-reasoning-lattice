# Review of ASN-0101

I worked through the operation specification (D0), the gap-closure and preservation claims (D1–D8), the projection and wp analyses (D9–D10), the composite extension (D11), and the three worked examples. The mathematics is sound: the D0 containment reduction, the D1 shift-bijection argument (via TS1/TS2), D8's source-correspondence discharge of S3★/CL-OWN/CL-UNIQ/S8★(c), the D9 projection split, and the D10 weakest preconditions all check out, including the boundary cases and the cross-document/cross-subspace handling. I have one anti-bloat finding.

## REVISE

### Issue 1: The structural form of `σ_d` is derived three times
**ASN-0101, "What shifts: closing the gap" (first paragraph) vs. D0 (effect) vs. D1 (justification)**:

- D0 effect: "for each `v = [S, 1, ..., 1, k] ∈ Π` ... the tumbler `u := [S, 1, ..., 1, k − n]` ... satisfies `shift(u, n) = v` ... So `σ_d(v) = [S, 1, ..., 1, k − n]`."
- "What shifts": "The D0 effect already establishes the structural form of the inverse: for each `v = [S, 1, ..., 1, k] ∈ Π` with `k ≥ p + n`, `σ_d(v) = [S, 1, ..., 1, k − n]` — the unique length-`m_S` tumbler whose shift by `n` recovers `v` ..."
- D1 justification: "Structural form of `σ_d(v)`: by the D0 effect's existence argument, for each `v = [S, 1, ..., 1, k] ∈ Π` ... `σ_d(v) = [S, 1, ..., 1, k − n]` — the unique length-`m_S` tumbler whose shift by `n` gives `v`."

**Problem**: The same structural-form statement appears in D0 (where it belongs, as part of the effect's existence argument) and is then re-derived nearly verbatim in two later places. The "What shifts" first paragraph explicitly announces it is repeating D0 ("The D0 effect already establishes...") and then restates the derivation before D1 restates it a third time. This is exactly the kind of accretion the anti-bloat classifier targets: a reader following D1's bijection proof must re-read material already established in D0 and narrated again in "What shifts." The genuinely new content of the "What shifts" section is narrow — the dense-sequence design rationale (no placeholders) and the "no reconciliation across the gap" observation, both of which are unique and worth keeping.

**Required**: Derive `σ_d`'s structural form once (in D0, where the effect is defined). Have "What shifts" and D1 cite that derivation rather than restate it. Retain the unique narrative (dense-sequence convention, no-reconciliation note) and the boundary observation `σ_d(r) = s`, and trim the re-derivation prose so the section advances the argument instead of recapitulating it.

## OUT_OF_SCOPE

The Open Questions section already correctly defers versioning, reconstruction, full reversibility, orphan re-discovery, and cross-document causal ordering to downstream ASNs. No additional out-of-scope topics surfaced.

VERDICT: REVISE
