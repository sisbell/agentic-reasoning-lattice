# Dependency Lint — ASN-0079

Declared depends: [34, 36, 43, 47, 53, 58]


## Uncertain (needs LLM verification)

- UNCERTAIN ASN-0040: uses [B3]

## LLM Verification

## Analysis: ASN-0079 — FLAGGED ASN-0040: uses [B3]

### B3 — Flagged against ASN-0040

**Search for B3 in ASN-0079:**

The text contains this passage in the "From Visible Content to Content Identity" section:

> "By B3 (Consistency, ASN-0058), M(d₁)(v₁) = aⱼ + p."

The citation is explicit: B3 is cited *with a parenthetical identifying it as from ASN-0058*, not ASN-0040.

**Check declared dependencies for B3:**

ASN-0058 (a declared dependency) exports exactly this label:

> **B3 — Consistency (PREDICATE, predicate)**
> `(A j : 1 ≤ j ≤ m : (A k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k))`

This is the block decomposition consistency predicate. ASN-0079 invokes it to conclude `M(d₁)(v₁) = aⱼ + p` from the maximally merged block decomposition of `M(d₁)|⟦σ₁⟧`.

**Classification: COLLISION** — The label B3 exists in ASN-0040 (the flagged source), but ASN-0079 is using B3 as defined in ASN-0058, which is a declared dependency and does export this label. The scan picked up the label text and attributed it to ASN-0040, but the actual reference is to ASN-0058's Consistency predicate. No missing dependency.

---

**RESULT: 0 MISSING, 1 COLLISION, 0 LOCAL, 0 CLEAN**
