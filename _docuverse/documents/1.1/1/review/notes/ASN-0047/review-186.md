# Review of ASN-0047

The technical core is mature: the elementary-transition taxonomy, the per-state vs. composite-boundary invariant partition, the K.μ~ link-subspace fixity proof, the D-SEQ★ derivation (both m=2 and m≥3), and the five worked examples (covering empty subspaces, singletons, full clearance, and the three replacement shapes) all hold up under scrutiny. Boundary behavior is genuinely exercised, not hand-waved. My findings are confined to accreted defensive prose flagged by the active anti-bloat classifier.

## REVISE

### Issue 1: M-total "Typing note" is a use-site survival inventory
**ASN-0047, The state model — "Typing note (M total — overrides foundation)"**: "The claim that (†) suffices is not blanket — we enumerate the inherited foundation results phrased over `dom(M)` and verify each survives the substitution: *ASN-0093 M0 ... Survives. ... M1 ... Survives. ... K.α / K.λ ... K.σ ... SubAllocatorAxiom activation ...*"

**Problem**: This matches the flagged "use-site inventory / exhaustiveness claim" pattern. The load-bearing content is the single identity (†) `d ∈ dom(M) ⟺ d ∈ E_doc` plus the reading "dom(M) ↦ E_doc," and the one genuinely non-trivial fact that M2 (EmptyArrangement) is *not* inherited. The bullet-by-bullet restatement of each foundation result only to conclude it "Survives" carries no reasoning the substitution doesn't already supply; a reader must skip past it to reach the M2 point that actually matters.

**Required**: Collapse the enumeration to: every `dom(M)`-phrased foundation result reads under (†) with `dom(M) ↦ E_doc` (M0, M1, the K.α/K.λ/K.σ preconditions, SubAllocatorAxiom activation carry verbatim); the sole exception is M2, deliberately superseded by K.μ⁺/K.μ⁺_L. Drop the per-result "Survives" restatements.

### Issue 2: K.μ⁺_L precondition restates a discharge it doesn't need
**ASN-0047, K.μ⁺_L precondition** (clause `ℓ ∉ ran(M(d))`): "With `ℓ ∉ ran(M(d))` and `v_ℓ ∉ dom(M(d))` (verified below), the post-state arrangement maps `v_ℓ` to a value absent from `ran(M(d))`, so no two V-positions share the image `ℓ` and CL-UNIQ holds at the post-state. Combined with CL-OWN ... the freshness condition `ℓ ∉ ran(M(d))` is equivalent — under the precondition `origin(ℓ) = d` — to `ℓ ∉ ran(M(d)|_{dom_L})` ... so the unrestricted `ℓ ∉ ran(M(d))` clause suffices."

**Problem**: This is a justification-of-the-precondition that does not advance the operation's definition. The CL-UNIQ-at-post-state argument is already discharged in the verification matrix and its prose ("precondition: ℓ∉ran(M(d)) ensures unique placement"); restating it here duplicates that work. The derived equivalence to `ran(M(d)|_{dom_L})` is never subsequently used — the operation simply checks `ℓ ∉ ran(M(d))`. The clause should state the precondition; the proof that it is sufficient for CL-UNIQ belongs only at the invariant-preservation site.

**Required**: Reduce the precondition line to the condition itself (`ℓ ∉ ran(M(d))`, first-arrangement). Remove the inline CL-UNIQ re-derivation and the unused equivalence; if the equivalence is wanted, move it to the CL-UNIQ preservation prose where it would actually be consumed.

## OUT_OF_SCOPE

### Topic 1: Link-subspace arrival-order invariant
**Why out of scope**: K.μ⁺_L appends at `shift(max(V_{s_L}(d)), 1)`, so link V-position order follows arrangement order, not K.λ allocation order; no invariant ties the two. Whether the link subspace must reflect Nelson's "permanent order of arrival" at the V-position level is genuinely new territory and is already recorded in Open Questions, not a defect here.

VERDICT: REVISE
