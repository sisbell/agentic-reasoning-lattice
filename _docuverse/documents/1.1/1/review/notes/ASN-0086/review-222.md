# Review of ASN-0086

## REVISE

### Issue 1: R0 first-emission branch mislabels the chain's first emission as its "anchor"
**ASN-0086, R0 proof, first-emission bullet**: "By ChainDiscipline + FirstEmission (ASN-0093), the link sub-allocator chain `A_L(d)` is active at every state with `d ∈ dom(Σ.M)`, and `a = [d.0.s_L.1]` is its anchor — so `a ∈ A_L(d)`..."

**Problem**: This contradicts the note's own "Allocator Structure" section, which correctly states the chain is "anchored ... at `b_L(d) := [d.0.s_L]`, with first emission ... `[d.0.s_L.1]`." Per ASN-0093 FirstEmission, the anchor is `b_L(d) = [d.0.s_L]` and `[d.0.s_L.1] = inc(b_L(d), 1) = c₁` is the *first stream element*, not the anchor. Worse, the anchor `b_L(d)` is the parent `p` of the stream `S(p, 1)` and is **not** a member of `A_L(d)` at all — so the asserted reason ("is its anchor ⟹ `a ∈ A_L(d)`") is doubly off. The conclusion `a ∈ A_L(d)` is correct (because `a = c₁`), but the justification is wrong and internally inconsistent.

**Required**: Replace "`a = [d.0.s_L.1]` is its anchor" with "`a = [d.0.s_L.1]` is its first emission `t₁^L(d) = inc(b_L(d), 1)`," so the on-chain conclusion rests on the stream's first element rather than on the (non-member) anchor.

### Issue 2: Leftover defensive meta-prose around R0's precondition (anti-bloat / reviser-drift)
**ASN-0086, R0 statement paragraph**: "The earlier outer condition `dom(Σ.M) ≠ ∅` is subsumed: when `dom(Σ.M) = ∅` the universal over `d` is vacuous." And **Emit_K, *Precondition***: "R0's home precondition `d ∈ dom(Σ.M)` is enforced by parameter typing: the `d ∈ dom(Σ.M)` argument is exactly the home R0 quantifies over, and cannot be supplied unless the document-allocation domain is non-empty."

**Problem**: Both sentences explain why a precondition is *enforced* or *no longer needed* rather than advancing the reasoning. The phrase "The earlier outer condition" signals content relocated from a prior formulation rather than removed — exactly the reviser-drift pattern flagged for this note. The Emit_K sentence restates `d ∈ dom(Σ.M)` and then justifies its enforceability ("cannot be supplied unless ...") instead of simply listing it as a precondition. A precise reader must skip both to follow the claim.

**Required**: Drop the "earlier outer condition ... is subsumed" sentence (the universal over `d ∈ dom(Σ.M)` carries the vacuity automatically; no commentary needed). Reduce the Emit_K precondition to its statement: "`K ∈ T_admissible`, `d ∈ dom(Σ.M)`."

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations and dynamic type introduction
**Why out of scope**: The treatment of `|Σ.L(a)| > 3` links as higher-arity relations `L_K^{(n)}` and the coordination question for layers choosing colliding type addresses are genuine new territory, correctly deferred to the Open Questions rather than forced into this note's standard-triple `L_K` model.

VERDICT: REVISE
