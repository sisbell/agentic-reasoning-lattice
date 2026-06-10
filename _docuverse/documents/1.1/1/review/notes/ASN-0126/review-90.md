# Review of ASN-0126

I checked the core results for soundness before turning to the anti-bloat pass. P3, P5, P6, the three-move retraction proof, the refined wp, and the worked illustration all hold — I verified the address arithmetic (`a_R = …2.3`, `a = a_emit(Σ₁,d) = …2.4 = g`, `g ∈ coverage(G_rng) = […2.4, …2.7)`), the born-nullified attribution to C3 (not C2, since `citation ≁ R`), and the `A_rel^{π(Σ')} = A_rel^{Ψ}` framing in the retraction proof. The framework's central guarantee (every stored tuple is shape-conforming) is established correctly. The findings below are one rigor gap in a transfer lemma plus accumulated forward-reference and defensive prose.

## REVISE

### Issue 1: B2's transition-transfer clause is unjustified and its precondition is too weak
**ASN-0126, The projection bridge (B2)**: "Take any ASN-0086 result whose conclusion is a predicate over the C/M/L components — either of a single →*-reachable state, or of a transition between two states each separately exhibited as →_sh-reachable. For each state Σ this note reasons about, π(Σ) is →*-reachable (ProjectionBridge), so the result holds at π(Σ); ... its conclusion transfers to Σ directly."

**Problem**: B2 advertises two transfer modes — single-state and transition — but the justification establishes only the single-state mode ("For each state Σ ... π(Σ) is →*-reachable ... transfers to Σ directly"). The transition mode is unsupported, and its stated precondition is wrong. ASN-0086's transition invariants (e.g., L12) are quantified over →-*steps* `Σ → Σ'`, not over arbitrary pairs of reachable states. To apply such an invariant to a pair you need `π(Σ) → π(Σ')` as a single ASN-0086 step — which ProjectionBridge yields from `Σ →_sh Σ'`, **not** from "two states each separately exhibited as →_sh-reachable." Two independently-reachable states need not be adjacent, and L12's antecedent is then false, so it constrains nothing about the pair. The looseness is not exercised: the only transition-transfer in the note (P6's appeal to L12) re-derives the step mapping inline ("each →_sh-step projecting to a →-step with the L-component shared"). So the clause is both unjustified and, as worded, unused — P6 does not actually rely on it.

**Required**: Either (a) restate the transition clause to require a →_sh-step `Σ →_sh Σ'` between the endpoints and justify it via ProjectionBridge's step-to-step mapping, or (b) drop the clause and let P6 carry the L12 transfer inline, as it already does.

### Issue 2: "The registry" section pre-narrates the operation set and transition relation
**ASN-0126, The registry**: "The operation set — the methods an app invokes against the link store — refines ASN-0086's {Emit_K, Observe_K, Nullify}. Emit_K and Observe_K carry over unchanged; ASN-0086's empty-from Nullify, however, has no →_sh image ... and is superseded by the attributed-Binary wrapper Nullify_Binary (defined in Retraction as an attributed Binary) ... The transition relation is refined: ASN-0086's → ≡ ... becomes →_sh ≡ ... (The shape-gated emit) ..."

**Problem**: This paragraph sits in the section that *defines the registry*, yet discusses neither the registry's structure nor its contents. It pre-narrates the operation-set and transition-relation refinements — the subject matter of "The shape-gated emit" — and forward-references that section twice, plus "Retraction as an attributed Binary" and "P1, Registry permanence." The reader must hold three not-yet-defined notions (`→_sh`, the gate, `Nullify_Binary`) to parse content that belongs to later sections. This is forward-reference accretion.

**Required**: Confine "The registry" to the registry itself (type, coverage-class keying, shape-vs-label distinction, declaration at `Σ_init`, C0). Move the operation-set and transition-relation refinement into "The shape-gated emit," where `→_sh` and the gate are defined.

### Issue 3: "Empty-from Nullify has no →_sh image" stated three times
The same fact appears in three sections:
- **The registry**: "ASN-0086's empty-from Nullify ... has no →_sh image — its |F| = 0 source fails the gate."
- **The shape-gated emit**: "ASN-0086's Nullify ... is one such empty-from emit, so it too has no →_sh image. Retraction must therefore be re-expressed ..."
- **Retraction as an attributed Binary**: "The shape-gated emit observed that ASN-0086's empty-from Nullify has no →_sh image."

**Problem**: Only "The shape-gated emit" *derives* the fact (it has both the Nullify formula and the gate). The registry statement is premature (Issue 2); the Retraction opening is a back-reference restating the conclusion. The claim is load-bearing once; stating it three times is exactly the meta-prose this pass targets.

**Required**: Derive it once in "The shape-gated emit." Open "Retraction as an attributed Binary" with the re-expression directly, citing the derivation rather than restating it. Remove it from "The registry."

### Issue 4: Defensive justifications around the wp and P6 proofs
**ASN-0126, Weakest precondition**: "(the arity guard (0) contributes no conjunct to g_sh: the emit vehicle is Emit_K, which always constructs the standard triple (F, G, K) of arity 3, so (0) is a value-condition the operation satisfies by construction — not a state-precondition that can fail and block the step — hence vacuously true here, contributing ⊤; this same arity-3 fact discharges L3's arity clause below)". And **Reachable conformance**: "The induction hypothesis being carried is the predicate '...' not merely value-persistence."

**Problem**: These justify why a conjunct is *absent* and what the IH is *not* — prose explaining the proof rather than advancing it. The wp parenthetical runs longer than the conjunct it removes.

**Required**: Compress. "(0) is discharged by construction — Emit_K always builds an arity-3 triple — and contributes no wp conjunct" suffices; the L3 remark belongs where L3 is discharged. State the P6 induction hypothesis once, positively.

## OUT_OF_SCOPE

### Topic 1: A shape that constrains target *depth*, not just span count
The catalog varies only by G span *count* (Unary/Binary/Multi), so registering R as Binary cannot express the unit-depth property retraction needs — which is why the note correctly demotes single-tuple-scope to an app obligation rather than a gate guarantee (the interior-prefix `a = d_retr.0.s_L` witness clears the Binary gate yet blows scope). A shape predicate constraining span *depth* (a unit-depth-target shape) would let the gate enforce what is currently delegated to the app.

**Why out of scope**: This enlarges the catalog along a new axis (depth, not count). OQ6 already flags loosening the `F=1`/`N=3` constraints; a depth-aware shape is the same class of future extension, not a defect in the present count-based catalog.

VERDICT: REVISE
