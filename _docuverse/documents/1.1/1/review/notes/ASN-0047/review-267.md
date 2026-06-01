# Review of ASN-0047

I checked the elementary transitions, the K.δ allocation cases, the D-SEQ★ derivation, the K.μ~ admissibility/realisability argument, and the Class (a)/(b) verification matrices. The mathematics is sound — the D-SEQ★ infinite-family contradiction, the necessity/sufficiency construction for K.μ~, the link-subspace fixity chain, and the cross-document/cross-subspace disjointness lemma all hold. No correctness defects found. The findings below are the meta-prose / forward-reference accretion patterns this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Ping-pong deferral of the K.δ freshness/parent-allocator discharge
**ASN-0047, K.δ case (ii) and §*K.δ case (ii) discharge and parent-allocator activation***: The definition says "the parent entity-level sub-allocator on which each step acts and the allocator-discipline properties the guard maintains are discharged in §*K.δ case (ii) discharge and parent-allocator activation*," and introduces a "*Per-k freshness mechanism (stated once here)*" paragraph — yet the downstream section then defers back: "the step's freshness is supplied by the definition's per-k mechanism (referenced here, not re-derived)."

**Problem**: Two sections each point at the other for the same fact (the k=0/k∈{1,2} freshness guard). A reader following the discharge bounces between the definition and the discharge section without either being self-contained. This is the "multiple paragraphs defer to the same downstream location" pattern, compounded by a back-reference.

**Required**: Put the per-k freshness statement in exactly one place and have the other site cite it once, directionally. The discharge section should not re-announce that freshness is "referenced here, not re-derived."

### Issue 2: "Modeling choice (layer separation)" is a three-paragraph defensive essay
**ASN-0047, D-CTG★/D-MIN★, *Modeling choice (layer separation)***: Three consecutive paragraphs of Nelson/Gregory exegesis ("Nelson locates link permanence in I-space... the withdrawn link keeps its permanent order-of-arrival address... In udanax-green the V-space POOM is kept gap-free...") sit between the invariant statement and its first use, all making one load-bearing point: link permanence is discharged on `dom(L)` by L12, so an arrangement-layer contiguity contract does not contradict tombstoning.

**Problem**: The justification for dropping ASN-0036's exemption is load-bearing, but it is restated three ways (I-space permanence, Vstream-renumbering, POOM gap-freeness) before the one-sentence conclusion "We adopt D-CTG★/D-MIN★ ... with link permanence discharged independently on `dom(L)` by L12." A precise reader skips two paragraphs to reach the operative claim.

**Required**: Condense to the load-bearing core: the strengthening is admissible because L12 carries link permanence on `dom(L)`, independent of `M(d)`. One sentence of Nelson grounding suffices; the renumbering detail belongs in the interior-withdrawal Open Question (where it already appears).

### Issue 3: K.μ⁺_L origin-restriction paragraph carries an implementation-mechanics inventory
**ASN-0047, K.μ⁺_L, origin-restriction paragraph**: "Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check."

**Problem**: The abstract guarantee is `origin(ℓ) = d` as a precondition; the routine-level inventory (`docreatelink`, `acceptablevsa`, `docopy`) is implementation mechanics, not a system guarantee, and does not advance the precondition's meaning. Per the review standard, implementation mechanics in a structural slot is drift. The surrounding Nelson quotation block (LM 4/31, 4/10, 4/12) likewise over-justifies a single design fact (links are not transcludable; byte stream is).

**Required**: Keep the operative statement (link transclusion excluded; `origin(ℓ) = d` enforced structurally) plus at most one Nelson grounding sentence. Drop the per-routine implementation inventory or relocate it to evidence, not the operation definition.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
**Why out of scope**: The ASN correctly confines K.μ⁻ to suffix removal and logs interior `DELETEVSPAN`/compaction as an Open Question. A renumbering-aware contraction operation is new machinery for a future ASN, not a defect here.

### Topic 2: Type-only / one-sided links (`e₁ ∪ e₂ ≠ ∅`)
**Why out of scope**: Whether to admit empty from/to endsets is raised as an Open Question; it is a future design choice, not a gap in this ASN's link-allocation contract (which already mandates only `e₃ ≠ ∅`).

VERDICT: REVISE
