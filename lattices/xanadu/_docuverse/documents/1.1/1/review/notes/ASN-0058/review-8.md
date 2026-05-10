# Review of ASN-0058

## REVISE

### Issue 1: Wrong foundation citation in M6(d) and M16 — TA5(c) does not justify general ordinal shift

**ASN-0058, M6(d)**: "origin(a + k) = origin(a), since ordinal increment via TA5(c) changes only the element field"

**ASN-0058, M16**: "Ordinal increment via TA5(c) (ASN-0034) changes only the last significant component of a tumbler"

**Problem**: Both proofs cite TA5(c) to establish that `origin(a₁ + n₁) = origin(a₁)`. TA5(c) defines `inc(t, 0)`, which increments by exactly 1 at position `sig(t)`. The operation actually used is OrdinalShift: `a + n₁ = a ⊕ δ(n₁, #a)`. For `n₁ > 1`, this is not a single application of `inc(t, 0)` — it requires either an induction argument (decomposing shift into repeated inc) or a direct argument from TumblerAdd. The direct argument is one step: by TumblerAdd definition, `rᵢ = aᵢ` for all `i` before the action point `#a`, so all components encoding the document prefix `N.0.U.0.D` are preserved. The TA5(c) route requires an unstated induction.

This matters most in M16, where the claim is the core of the cross-origin merge impossibility proof. A reader checking TA5(c) finds it governs `inc(t, 0)` — incrementing by 1 — which does not directly support the general-`n₁` case.

**Required**: In both M6(d) and M16, replace the TA5(c) citation with a direct appeal to TumblerAdd's definition: for displacement `δ(n₁, #a)` with action point `#a`, TumblerAdd copies `aᵢ` for all `i < #a`, preserving the document prefix. This is a one-step argument that holds for any `n₁ ≥ 1` without induction.

## OUT_OF_SCOPE

### Topic 1: Lattice structure of equivalent decompositions
**Why out of scope**: The ASN establishes the canonical (maximally merged) decomposition as the coarsest element of a refinement ordering and poses the lattice question explicitly. Answering it requires new algebraic machinery (characterizing all valid refinements, showing meets/joins exist) — a natural extension, not a gap in the current work.

### Topic 2: Block count bounds relative to V-extent
**Why out of scope**: The ASN poses this as an open question. Answering it likely requires analysis of allocation patterns and operation histories — territory that depends on the operation semantics ASNs excluded from scope.

VERDICT: REVISE
