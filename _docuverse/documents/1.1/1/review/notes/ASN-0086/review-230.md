# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 conflates the closed operation set with the open substrate domain

**ASN-0086, Weakest-Precondition Analysis, Case 2 (Result)**: "For this note's operation set `{Emit_K, Observe_K, Nullify}`, and over the sub-space of pre-states Σ that are both →*-reachable *and* unit-depth-disciplined (the domain restriction stated below), the weakest precondition is …"

and (load-bearing paragraph): "a direct K.λ caller can emit a crafted-span retraction that is L-invariant-conforming and leaves the state `→*`-reachable, yet violates the unit-depth retraction discipline."

**Problem**: The two framings are incompatible as written. `→` is defined as `K.σ ∪ K.α ∪ K.λ` (full substrate), so `→*`-reachable includes states produced by raw K.λ calls. But the relational layer's own discharge proof (Definition — relational layer) establishes that **every state the layer reaches is unit-depth-disciplined**. So:
- If the domain really is "this note's operation set," restriction (ii) is a *derived invariant*, already proven, and should not appear as an independent domain hypothesis on the wp.
- If the domain is the full `→*`-reachable substrate (which is what makes the load-bearing paragraph's "direct K.λ caller" non-vacuous), then (ii) is a genuine caller obligation — but that caller is by construction *outside* the operation set, so "for this note's operation set" mis-describes the domain.

The load-bearing justification only works by reaching outside the operation set it claims to be analyzing. This is reviser drift: a paragraph imagining a case (the direct K.λ caller) that the stated carrier (the three-operation set) excludes.

**Required**: Pick one framing. Either (a) state the wp over the layer's reachable states and cite the discipline discharge to discharge (ii) as derived — removing it from the domain — or (b) drop "for this note's operation set," state the wp over full `→*`-reachable substrate states, and present (ii) explicitly as a caller obligation that the relational layer (but not an arbitrary K.λ caller) automatically satisfies.

### Issue 2: Same content restated across multiple sections (anti-bloat)

The note carries `review-mode.anti-bloat`; the following are duplicated explanations, not distinct reasoning steps:

- **Unit-depth retraction discipline** is explained three times: *Definition — Unit-depth retraction discipline*, the multi-paragraph discharge in *Definition — relational layer*, and again in wp Case 2's "unit-depth discipline is load-bearing." The third largely re-narrates the first two.
- **The self-emit branch** (`a = a_emit(Σ, d)`, P1 false) is explained in *Definition — Nullify*, *R-Scope*'s proof, wp Case 1's "Self-emit branch," and again in Worked Sketch Step 4 — four restatements of the same `a = e ⟹ a ∈ A_rel^{Σ'} ⟹ R0a-antichain` argument.

**Problem**: A precise reader must skip past the duplicate prose to find which instance carries the load-bearing argument. Two paragraphs saying the same thing in different words is the pattern the classifier flags.

**Required**: Keep the load-bearing statement at one site (the lemma/definition that owns it) and reduce the others to a one-line citation. The wp analysis should cite R-Scope and the discipline-discharge rather than re-deriving them.

### Issue 3: "Scope" sub-paragraph placement under Definition — Nullified

**ASN-0086, Definition — Nullified, *Scope***: "The witnessing tuple `(b, F', G')` ranges over the triple-restricted `L_R^Σ` … so only standard-triple links can retract …"

**Problem**: The content (only standard-triple links retract) is object-level and worth keeping, but it sits in a labeled "Scope" slot — exactly the structural-slot essay pattern the classifier targets. The fact belongs in the definition body or as a postcondition, not in a rationale-labeled aside.

**Required**: Fold the consequence into the definition or state it as a numbered postcondition; drop the "Scope" label.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe, and cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are already enumerated in Open Questions; they concern a consistency model and a structural-ratio guarantee the substrate does not yet specify. Not errors in this ASN.

### Topic 2: Multi-arity links as higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note deliberately confines `L_K` to standard triples (`|Σ.L(a)| = 3`) and parks the n-ary generalization in Open Questions. New territory, not a defect here.

VERDICT: REVISE
