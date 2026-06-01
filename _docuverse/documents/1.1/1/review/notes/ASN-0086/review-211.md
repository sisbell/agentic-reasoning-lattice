# Review of ASN-0086

I checked the six properties (R0–R6c), the wp analysis, the worked sketch, and the supporting lemmas (CoverageEqualityDecidable, L-ContiguousPrefix, R0a). The core mathematics holds: R0a's two-case antichain argument is sound, the wp Case 2 biconditional is correctly derived over its restricted domain, the unit-depth-discipline load-bearingness is properly isolated, and the worked sketch's tumbler arithmetic checks out step-by-step. The findings below are precision/anti-bloat, consistent with the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Non-load-bearing proof embedded in an Open Question
**ASN-0086, Open Questions, L1b-tightening bullet**: "(Remark: in this note's link store every address in fact has `#E = 2` — each lies on an `inc(·, 0)` chain anchored at a depth-2 element field `[s_L, 1]`, which `inc(·, 0)` advances only at the terminal non-zero position by TA5(c)/TA5-SigValid, leaving the zero positions and hence the element-field length fixed — so the tightening would be sound here; no result in this note relies on it.)"

**Problem**: This is a derivation (a soundness sub-proof) occupying a structural slot meant to pose a design question. It is explicitly self-declared non-load-bearing ("no result in this note relies on it"), which is the precise signature of accretion: a proof that advances no claim, sitting where a question should be. It also half-answers its own open question ("the tightening would be sound here"), which is neither a clean question nor a body lemma.

**Required**: Reduce the bullet to the design tradeoff it poses (tighten `#E ≥ 2` to `#E = 2` at source, or retain headroom for higher-arity/future variants?). Drop the embedded TA5(c)/TA5-SigValid derivation.

### Issue 2: Home-prefix formula mis-attributed to L1a
**ASN-0086, R0a Case 1**: "By L1a (LinkScopedAllocation, ASN-0043), `home(·) = N(·).0.U(·).0.D(·)`…"; and **R0, first-emission bullet**: "(`origin` and `home` coincide on link addresses by L1 + L1a's NUDE-prefix projection)".

**Problem**: The NUDE-prefix formula `home(a) = N(a).0.U(a).0.D(a)` is the `home(a) — Home (DEF)` definition in ASN-0043. L1a (LinkScopedAllocation) only asserts the membership invariant `home(a) ∈ dom(Σ.M)` — it does not supply the projection formula. The argument leans on the formula, not the membership claim, so the citation points at the wrong foundation clause in two places.

**Required**: Cite the `Home` definition (ASN-0043) for the projection formula; reserve L1a for membership.

### Issue 3: "Value-shape postcondition (downstream hook)" — role-labeling and an auto-discharged "requirement"
**ASN-0086, R0 proof**: "*Value-shape postcondition (downstream hook).* R0 imposes exactly one content-dependent requirement on the caller-supplied value: L3-conformance of the triple `(F, G, K)`…"

**Problem**: Two issues. (a) The parenthetical "(downstream hook)" labels the paragraph by the role it plays for R5 rather than stating R0's content — the meta-framing the anti-bloat pass is meant to catch. (b) For R0 as quantified (`F, G ∈ Endset`, `K ∈ T_admissible`), L3-conformance is *automatically* satisfied by the typed signature: arity is 3, all three slots are `Endset` members, and `K ∈ T_admissible` forces `e₃ ≠ ∅`. So R0 imposes no requirement the caller must separately discharge; the sentence describes what R0 does *not* constrain, framed as a requirement.

**Required**: State the substantive content plainly as an R0 consequence ("every L-invariant at the fresh key is value-independent given Endset-typed inputs; L3 holds by the signature"), drop the "downstream hook" role-label, and let R5 verify L3-conformance of its specific triple `(∅, G_self, K)` at its own site (which it already does).

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and higher-arity nullification
**Why out of scope**: `L_K` and `nullified` are confined to standard triples (`|Σ.L(a)| = 3`), so higher-arity links inhabit `A_rel` but index no tuple and can neither be retracted nor act as retractors. This is correctly acknowledged in the TypedRelation definition and the Open Questions (multi-arity bullet); a higher-arity relational layer is future territory, not a defect here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
**Why out of scope**: The wp Case 2 domain restriction (ii) is honestly carried as a layer commitment, and the address-vs-shape gap motivating it is correctly identified. Whether to introduce a substrate-level unit-depth retraction K-operation is a substrate-design question, properly posed in Open Questions.

VERDICT: REVISE
