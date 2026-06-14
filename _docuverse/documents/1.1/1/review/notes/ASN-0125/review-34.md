# Review of ASN-0125

I worked the mathematics first, because that is where a derived composite earns its keep, and ASN-0125 holds up under it. I checked EL0's wp argument (J persists by LP13, J ⟹ ¬R_mut, so wp is false at Σ₀ for every program), the EL3 carrier-necessity case analysis, the EL6/EL7 emission and discipline-preservation proofs, the nullification reasoning (fresh address escapes pre-existing unit-depth retraction coverage by R0a), and the boundary constructions: the empty store Σ₀ (EL-DM base), prefix-only contraction in the EL9(2) de-listing construction (j = 1 boundary handled), position reuse (EL10), the three reachable currency cardinalities including the standoff `current = ∅` (EL14c), and the activity-agnostic-membership subtlety where `succ_o` filters on claim activity but not endpoint activity (EL14e). The worked example traces succ_h/succ_o/current/nullified consistently through edit, fork, demotion, revert, and registry churn. I found no correctness error and no missing case that breaks a claim.

What remains is residual meta-prose of exactly the kind this review mode exists to catch.

## REVISE

### Issue 1: Roadmap and methodology connective prose
**ASN-0125, "The supersession relation" and "What the record must satisfy"**:
- Between Df-DISC and Df-LAY: "Df-DISC describes a property of states; the next definition names a layer whose operations preserve it, and EL-DM establishes it holds wherever that layer reaches."
- Opening "The supersession relation": "We now fix the layer's definitions."
- After RQ introduction: "Each is a distillation of design intent; we name them so the architecture comparison can be conducted claim by claim rather than by taste."

**Problem**: Each of these advances no reasoning. The first is a table-of-contents-in-prose that restates, in advance, what Df-LAY and EL-DM go on to say; a reader skips it to reach the definitions. The third clause justifies the *methodology* of numbering the requirements rather than stating anything about them. These are the orientation fragments the anti-bloat classifier flags.
**Required**: Delete. Df-LAY and EL-DM stand on their own; RQ1–RQ7 need no preamble about why they are numbered.

### Issue 2: Duplicated cross-layer orientation note
**ASN-0125, Df-LAY (body) and Claims table (Df-LAY row)**: body — "This mirrors ASN-0086's RelationalLayer and its LayerReachable states."; table — "(mirrors ASN-0086's RelationalLayer/LayerReachable)".
**Problem**: A pure "this resembles X" cross-reference that carries no obligation and discharges no step, stated twice. It is orientation, not content.
**Required**: Cut both. If a pointer to the ASN-0086 analogue is wanted, one unobtrusive citation at the LayerReachable definition suffices; the doubled remark does not.

### Issue 3: `Df-LISTED` invoked before it is defined
**ASN-0125, EL7(ii)**: "so `listed(a', d, Σ₂)` is false for every `d` (Df-LISTED)" — but Df-LISTED is first stated in the later section "The original after the edit: three independent axes."
**Problem**: A self-contained reading of EL7 depends on a predicate the document has not yet introduced. The citation is clean, but the structural slot is wrong: the "born unlisted" postcondition is load-bearing for EL7 and should not lean forward to a definition two sections away.
**Required**: Move Df-LISTED ahead of EL7 (it depends only on `Contains`, M1, CL-OWN, S3★, SD — all available by "The substrate we build on"), or inline its one-line meaning at first use.

## OUT_OF_SCOPE

### Topic 1: Arity->3 successors carrying supersession-class type
`DC(ℓ')` admits a successor with `|ℓ'| > 3` and `coverage(ℓ'.e₃) = coverage(K_sup)` (the schema clause's guard `|ℓ'| = 3` is then false; the leading conjunct holds since `coverage(K_sup) ≠ coverage(R)`). Such a successor is a valid link but not a claim — ASN-0086 restricts `L_K^Σ` to arity-3 tuples — so it never enters `S^Σ`, is invisible to `Observe_{K_sup}` and to `succ_h`/`succ_o`, and breaks no invariant (EL-DM is undisturbed). It is harmless here.
**Why out of scope**: Whether the supersession coverage class should be kept free of non-claim members is a typed-relation hygiene question for the layer that owns `[K_sup]`, not a defect in this ASN's operations or invariants. The ASN's discipline-preservation claims are correct as stated.

VERDICT: REVISE
