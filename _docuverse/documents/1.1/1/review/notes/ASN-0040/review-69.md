# Review of ASN-0040

## REVISE

### Issue 1: Citation cycle between Bop and B1 (with an unnecessary dependency)
**ASN-0040, Bop proof / B1 Formal Contract**: Bop's freshness proof asserts "By B1, children(s.B, p, d) = {c₁, ..., cₘ}" and "a = next(s.B, p, d) = c_{m+1} where m = hwm(s.B, p, d)." B1's contract then states: "Preservation: Each baptism preserves B1 in the target namespace (by Bop, B0, B4, S0, TA5(c))."

**Problem**: Bop cites B1 (and hwm/B2), while B1 cites Bop — a citation cycle. The cycle is gratuitous: Bop's freshness does **not** need B1. With `a = next(s.B,p,d)`, either `children = ∅` (then `a = c₁ ∈ S(p,d)`; if `a ∈ s.B` it would be in `children`, contradiction) or `a = inc(max(children),0)`, which by S0/TA5(a) is strictly greater than `max(children)` and hence `a ∉ children`, so `a ∉ s.B`. Neither branch uses contiguity. Symmetrically, B1's preservation does not use Bop — the new element's identity comes from the `next` definition + B0b, not from Bop's freshness.

**Required**: Rewrite Bop's freshness using only `next > max(children) ∈ S(p,d)` (dropping the B1/hwm/B2 invocations), and remove "by Bop" from B1's preservation citation. Each result then cites only genuine antecedents and the cycle disappears.

### Issue 2: Proofs depend on results established later in the document
**ASN-0040, B1 proof and Bop proof**: B1 (in "The contiguous prefix property") invokes B7 ("Both (p₀, d₀) and (p, d) meet B7's preconditions, so B7 gives S(p₀, d₀) ∩ S(p, d) = ∅") and B_fin — both proved several sections later ("Namespace disjointness," "The contiguous prefix property" respectively). Bop (in "The baptism operation") invokes B1, B2, hwm, and B_fin, all introduced afterward.

**Problem**: The logical dependency graph is acyclic, but the presentation order inverts it, so no proof can be verified in reading order. A reader reaching Bop or B1 cannot check the cited facts because they have not yet been established. This is the forward-reference accretion the note asks to surface.

**Required**: Reorder so antecedents precede consumers — at minimum: S0/S1/S(p,d), B0a→B0→B0★→B0b, B₀ conf, B_fin, B6, B7, then B1, hwm, B2, then Bop, B8, B9. Alternatively make the forward dependencies explicit and confirm acyclicity, but the cleaner fix is reordering.

### Issue 3: B0b restates B0a
**ASN-0040, B0b**: "Every transition `s → s'` has exactly one of two shapes... This union form is immediate from B0a's partition of Σ."

**Problem**: B0b is B0a re-expressed at the transition level; its "proof" is "immediate from B0a's partition." Two statements saying the same thing in different words is a flagged anti-bloat pattern. B0b does earn a clean dichotomy used in the B1/B_fin/B10 inductions, so it is borderline — but as written it adds a label and paragraph without advancing content beyond B0a.

**Required**: Either fold the transition-level dichotomy into B0a's statement (so the inductions cite B0a directly), or reduce B0b to a one-line named restatement without the surrounding re-derivation.

### Issue 4: Over-elaboration in B6 necessity
**ASN-0040, B6 necessity sub-case (a)**: For the singleton `p = [0]` at d=2: "...preserves (cₙ)₁ = 0 from p for every n (and additionally exhibits adjacent zeros at positions 1 and 2 within c₁)."

**Problem**: The `t₁ ≠ 0` violation already discharges this case. The parenthetical noting a *second*, independent violation adds nothing to the necessity argument and is defensive thoroughness.

**Required**: Drop the parenthetical; one surviving T4 violation suffices.

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) and the `Occupied` predicate
**Why out of scope**: B3 introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and an invariant constraining content placement. Content storage and retrieval are explicitly out of scope. The ghost-element *concept* (baptism without content) legitimately belongs to characterizing baptism, and framing B3 as a forward requirement is reasonable, but the `Occupied` machinery and the permitted-configurations enumeration are content-storage territory for a future ASN — flagged per the instruction to mark defined claims touching out-of-scope topics, not as an error in the present reasoning.

VERDICT: REVISE
