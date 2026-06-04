# Review of ASN-0077

This is a thorough, largely rigorous note: concrete worked example present, two non-trivial wp evaluations, boundary cases (empty intersection, singleton, cross-subspace, link-subspace, empty document) all addressed, and the K.μ⁺/K.μ⁺_L preservation proofs write out each case rather than waving. The proofs I spot-checked (O11 sub-cases (a)/(b), O11★★ exhaustiveness, the singleton I-span squeeze) hold. My findings are confined to the forward-reference accretion the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: C1a machinery and O2 introduced as worked-example scaffolding, framed by meta-prose

**ASN-0077, "Lifting origin to a V-span" / O2**: The note builds the full C1a block-decomposition apparatus and then states: *"The C1a block decomposition is not needed to define `origins_V`, but it is the bridge to ASN-0058's block algebra that the worked example uses to narrate a transcluded span block by block. The following claim is what licenses that narration..."* Earlier in the same section: *"We use C1a rather than `resolve` because C1a's decomposition covers both subspaces, whereas `resolve` confines I-targets to `dom(C)` (C1)."*

**Problem**: By the note's own admission the decomposition is "not needed to define `origins_V`" — the definition uses (F1), `{origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d))}`, which never mentions blocks. The justificatory framing ("the bridge... that the worked example uses to narrate," "what licenses that narration," "We use C1a rather than `resolve` because") explains why the apparatus exists and names its downstream consumer rather than advancing the claim. A reader following O2 must skip past the role-of-the-claim prose to reach the claim's content. This is the narration-bridge accretion (the prior commit explicitly "inline[d] O2's role as narration bridge").

**Required**: Motivate O2 by its content (block uniformity — every I-address in a block shares one origin), not by the worked example that consumes it. Drop the "not needed... but it is the bridge... licenses that narration" framing and the "rather than `resolve`" rationale, or reduce the latter to a one-clause precondition note.

### Issue 2: Forward use-site pointers in the V-span lift and WF_V definition

**ASN-0077, "Lifting origin to a V-span" and WF_V definition**: *"The reader-facing form — the form that the operation specification will use — is: (F1)..."* and, closing WF_V, *"These are exactly the well-formedness conjuncts of the SHOWORIGIN_V operation specified below; the operation's precondition is `WF_V(Σ, d, σ)`."*

**Problem**: Both sentences point forward to "the operation specification" / "specified below" as the consumer of the definition. They enumerate a downstream use site rather than advance the definition's meaning. The coupling (precondition = WF_V) is already clear at the operation section itself.

**Required**: State (F1) and WF_V on their own terms; drop the "the form that the operation specification will use" and "specified below" forward pointers.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation
The Open Questions correctly defer a single operation reporting both content and link origins over an I-stream range to a future ASN; the I-span lift's deliberate content-only confinement is settled here.

### Topic 2: Historical containment from Σ.R, intermediate-chain surfacing
Reporting historical containment and surfacing the transclusion chain are named as separate future operations — appropriately out of scope.

VERDICT: REVISE
