# Review of ASN-0094

## REVISE

### Issue 1: AllocatedAddressAntichain Sub-case 3b's "vacuous on substrate-conforming layer" rationale misattributes the scaffolding

**ASN-0094, AllocatedAddressAntichain proof, after Sub-case 3b Step 3.3b**: "Sub-case 3b (`x ∈ dom(Σ.C), a ∈ dom(Σ.L)`) is *vacuous on the substrate-conforming layer*: under R0a-Cor2 (a strict strengthening of L1b to `#E(·) = 2`), `x ∈ dom(Σ.C)` element-level gives `#E(x) = 2` (via the scaffolding's content-side reading) and `a ∈ dom(Σ.L)` gives `#E(a) = 2` directly; the prefix relation `x ≼ a` with both `zeros(·) = 3` and `#E(·) = 2` forces `#x = #a`... R0a-Cor2 closes the case by length-counting alone, before the subspace partition argument fires."

**Problem**: R0a-Cor2 (ASN-0086) is a link-side lemma applying only to `dom(Σ.L)`; it has no "content-side reading" yielding `#E(x) = 2`. The *Element-level content addresses* scaffolding clause (Scope and Substrate Scaffolding) gives `#E(a) ≥ 2` for `a ∈ dom(Σ.C)`, not `= 2`. The vacuity argument *does* close — via `#E(x) ≥ 2` (scaffolding) + `#E(a) = 2` (R0a-Cor2) + same zero positions (Step 3.1) + Prefix's `#x ≤ #a` forcing `n_3 + 2 ≤ #x ≤ #a = n_3 + 2` hence `#x = #a`, then T3 + L14 contradiction — but this requires multiple steps, not "length-counting alone".

**Required**: Either (a) rephrase to acknowledge the content-side scaffolding gives `#E(·) ≥ 2`, and the equality `#x = #a` arises from combining this with R0a-Cor2 and the prefix constraint; or (b) strengthen the *Element-level content addresses* scaffolding clause to commit to `#E(a) = 2` on the content side (matching R0a-Cor2's link-side strengthening). The formal Sub-case 3b proof via Steps 3.1, 3.2, 3.3b (subspace contradiction) is unaffected; this is purely a description-of-vacuity issue.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate / cross-process atomicity for Sh4/FDD/SHCD contracts

**Why out of scope**: The framework explicitly commits to single-process substrate scope, with within-call sequentiality as the atomicity reading. Cross-process consistency would extend the framework's scope rather than fix a defect; correctly listed in Open Questions as a scope boundary.

### Topic 2: Mechanical derivation of per-shape body-shape uniformity at shape-mate rows

**Why out of scope**: Sh5(a) explicitly downgrades per-shape body-shape uniformity from "commitment" to "aspiration". The framework supplies no mechanical gate to force a future catalog extension to register identical bodies at the same shape; the current catalog's shape-mate convergences (DirectedPair/Resolution; the two `(0, 1)` rows) are exhibited by hand-curation. Sharpening to a procedural recipe is acknowledged as future work, not a defect.

### Topic 3: Document-container target-domain symbol (`dom(Σ.M)` addresses)

**Why out of scope**: The framework's *Reach of the framework's target-domain symbols* note commits to `A_doc = dom(Σ.C)` (content addresses) with no symbol for document containers in `dom(Σ.M)`. Layers needing document-container relations must use designated content addresses. The structural limitation is acknowledged explicitly.

VERDICT: REVISE
