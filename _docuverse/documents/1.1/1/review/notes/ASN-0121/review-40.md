# Review of ASN-0121

## REVISE

No REVISE items. The findings below record what was checked and why each suspect point survived scrutiny.

**The forcing argument (FL-DEF).** The soundness/completeness pair pins the answer uniquely; I verified the slack argument is genuine — without the addressability conjunct, both `R_min` and `R_max` satisfy the two demands, so the conjunct is doing real work, and the derivation correctly identifies retraction as the residual freedom it closes.

**Monotonicity of `nullified` across the full vocabulary.** The structural argument holds: `L_R^Σ` is selected from `dom(Σ.L)` by arity-3 and slot-3 stored-value tests, so it is a function of `Σ.L` (given the fixed representative `R`); F-PRES steps preserve it outright, and across K.λ the witnessing tuple persists by L12 while `dom(Σ.L)` grows, matching R6a. The induction to `→*` is sound.

**FL-JUNK.** Both inclusions verified. The hypothesis `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` is consumed only on existing links, exactly as claimed; the ⊇ half is indeed automatic from non-decrease plus `nullified(Σ) ⊆ dom(Σ.L)`. The weakening that admits born-nullified junk is consistent with the Trace 7(a) construction.

**FL-WP, all three cases.** (a) The ordinariness cut on retraction-relation membership (not coverage class) is correct and necessary — the arity-`N > 3` retraction-typed sub-case would be misclassified by a coverage-only cut; under the cut, `L_R^{Σ'} = L_R^Σ` follows from L12 plus the single fresh address. The ghost-pre-coverage conjunct is non-vacuous (Trace 7(a) witnesses it concretely), so retaining it is right given no retraction discipline is assumed. (b) The fresh-link space is exhaustively partitioned by `ℓ ∈ L_R^{Σ'}`; the existential split over the disjoint union is valid, and the self-retraction term `b ∉ coverage(G')` is live by reflexivity of `≼` (Trace 7(b) exercises it). (c) The membership equation `a ∈ nullified(Σ') ⟺ a ∈ nullified(Σ) ∨ a ∈ coverage(G')` is derived in both directions, which is what licenses calling the result *weakest*; the equation is correctly restricted to the existing-link slice. The exhaustiveness claim for result changes holds: existing non-members cannot enter (sat constant; R6a), and ordinary K.λ admits no exits since `L_R` is fixed.

**Worked traces.** All seven recomputed. The five length-8 addresses are pairwise prefix-incomparable, so subtree disjointness via T10 is correctly invoked. Trace 4's `nullified(Σ) = {a₁}` is right — the equal-length siblings `a₂, a₃, r₄` lie outside `a₁`'s subtree. Trace 6's residence flips check out, including reflexivity admissions and the node-granularity case. Trace 7's answer `{r₁}` for `(∗, ∗, ∗, Θ_ρ)` is correct: `b` self-nullified, `ℓ` fails the type slot (and is independently nullified by `r₁`), and `r₁`'s empty from-endset is admitted only under the wildcard, per FL-EMP's link-side rule.

**Boundary cases.** Empty constrained slot (zero), wildcard (unit), all-empty vs all-wildcard, empty link-side endsets, ghost targets, self-retraction, and the element-rooted wide home span are all handled concretely. I verified the arithmetic of the home-grammar example: `[1,0,1,0,1,0,1,1] ⊕ [0,0,0,0,1,1,1,1] = [1,0,1,0,2,1,1,1]`, and `[1,0,1,0,2]` does lie in the half-open interval, so the caveat about wide element-rooted spans is correct, not hypothetical. The empty-store case is definitionally immediate from the comprehension and needs no separate clause.

**FL-DEC.** The reuse of ASN-0086's cell decomposition for intersection-nonemptiness rather than equality is legitimate — same cells, same finitely many T2 tests, different final predicate. `home(a)` is well-defined on `dom(Σ.L)` directly by L0b (the foundation states this itself).

**Anti-bloat scan.** I looked specifically for the flagged patterns. The labeled "Scope of the wp" sub-paragraph is not rationale-noise — it fixes what "weakest" quantifies over (additional precondition given an enabled step), without which the wp claims are ill-posed. The FTT-subscript paragraph carries the load-bearing non-restriction facts (higher-slot matches; nullified-but-satisfying links) that prevent conflation with F-FIND. The FL-JUNK hypothesis-weakening paragraph specifies the hypothesis's reach and is exercised by Trace 7(a). Forward references are isolated single pointers, not deferral chains; I found no duplicated paragraphs and no cases argued that a precondition already excludes.

## OUT_OF_SCOPE

### Topic 1: Result enumeration order
Nelson's phrasing "returns a *list* of all links" (4/69) raises the question of a canonical order on the returned set (e.g., by tumbler order on addresses). The present ASN correctly specifies the answer as a set; a deterministic enumeration order only acquires force with paginated retrieval (FINDNEXTNLINKSFROMTOTHREE), which is explicitly out of scope here.
**Why out of scope**: ordering is a property of the pagination front-end, not of the membership semantics this ASN forces; nothing in FL-DEF through FL-REACH depends on it.

VERDICT: CONVERGED
