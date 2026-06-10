# Review of ASN-0126

I worked the proofs first. The mathematical core is sound: P1 (registry framed by construction), P3 (only `K.λ_sh` extends `dom(Σ.L)`), the ProjectionBridge and its B1/B2 corollaries, the R-Scope frame transfer, the guarded-command wp, and the P5/P6 inductions all hold up. The born-nullified worked example checks out address-for-address (`a_R = ...2.3 ∉ coverage(G_rng)`, `a = g = ...2.4 ∈ coverage(G_rng)`), and the C3-liveness insight it dramatizes is correct and well-earned. I found no broken proof.

What remains are one specification-precision gap and several instances of accreted prose — the latter being exactly what this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: The `name` registry field is unconstrained and unread

**ASN-0126, The registry**: "a **name** — an opaque string identifier"; and well-formedness is "A registry is well-formed when shape values lie in `{Unary, Binary, Multi}` and ... *coverage-class keys are unique*."

**Problem**: `name` is part of the formal state component `Σ.registry` (the note writes the registry as a partial function `T_admissible/~ ⇀ (name, shape)`), yet no invariant constrains it and no property or operation reads it. P1–P6 reference only the registry's invariance; the gate, `shape(·)`, and `Sh-conf` read only `shape` and span counts. Well-formedness imposes a uniqueness condition on coverage-class keys but says nothing about `name` — so two distinct entries may carry the same `name`. The note calls it an "identifier," but an identifier that may collide identifies nothing. An implementer cannot tell from this note whether `name` uniqueness must be enforced or whether `name` carries any framework semantics at all.

**Required**: Resolve the field's status. Either give it a constrained role (require `name` uniqueness if it is a genuine identifier, and state who reads it), or declare it framework-uninterpreted app metadata — in which case drop "identifier" (which overclaims when collisions are permitted) and justify carrying it in the formal state tuple the framework reasons about.

### Issue 2: The B2-exclusion paragraph inventories two results the note never uses

**ASN-0126, The projection bridge**: "ASN-0086's R0 (TupleAddressFreshness), R5 (TupleSelfTargeting), and R6c's restoration-by-reemission each conclude `∃ Σ' : Σ → Σ' ∧ …`. ... Results of this subclass are obtained here not through B2 but by lifting (P5)..."

**Problem**: Of the three named results, only R0 is re-derived in this note — its gated analog is P5. R5 (self-targeting) and R6c (restoration) are never lifted, re-derived, or invoked anywhere. Naming them is a forward-looking use-site inventory of downstream results that does not advance the argument: the exclusion of existence-of-successor results from B2, and the lifting recipe, stand on R0 alone.

**Required**: Name only the result the note actually lifts (R0), or state the exclusion generically ("existence-of-successor results do not transfer via B2; the one needed here is re-derived by lifting in P5"). Drop R5 and R6c.

### Issue 3: P2 (ShapeStability) is stated, listed, never cited, and re-derived inline

**ASN-0126, Registry permanence**: "**P2 (ShapeStability).** For any *registered* K, `shape(K)` takes the same value at every `→_sh*`-reachable state..." — yet P4's proof re-establishes the same fact without citing P2: "since `shape(K)` is registry-determined and the registry is invariant, `Sh-conf(K, F, G)` evaluates the same..." and P6 cites P1 and P4, not P2.

**Problem**: P2 is proved and placed in "Properties established," but nothing builds on it by name; the one place shape-stability is needed (P4) re-derives it inline. Either P2 is a building block — in which case P4 should cite it instead of re-deriving its content — or it is subsumed by P4, in which case its standalone statement is accretion.

**Required**: Make P2 load-bearing (cite it at the use site in P4) or remove it and let P1 carry the weight directly in P4's derivation.

### Issue 4: The "Sh-conf is partial / undefined for unregistered K" gloss is re-explained three times

**ASN-0126, Shape-conformance**: "For an unregistered K, `shape(K)` does not exist and `Sh-conf(K, F, G)` carries no truth value." **The shape-gated emit**: "so `Sh-conf(K, F, G)`, partial and defined only for registered K, is well-defined wherever (ii) is reached." **Weakest precondition**: "so that `g_sh` is *false* (not undefined) at an unregistered K, where `Sh-conf` carries no truth value."

**Problem**: The partiality fact is *invoked* in three distinct arguments (acceptable) but *re-explained* each time. The definition at first use is canonical; the later two re-state the same fact rather than referencing it, which is the kind of cross-section restatement that compounds across cycles.

**Required**: State the partiality once at the definition; at the later use sites, invoke it by reference ("`Sh-conf` partial on unregistered K, defined above") rather than re-explaining "carries no truth value."

## OUT_OF_SCOPE

### Topic 1: Dynamic (post-init) registration

**Why out of scope**: P1 fixes the registry at `Σ_init` by design, so an app cannot register a new type at runtime — all types must be declared at substrate construction. Whether and how a substrate supports an evolving registry is a different design (it would relax P1) and belongs in a successor note; OQ4 already gestures at the init-time registration question. This is not a defect in a note whose stated contribution is an *immutable* registry.

META: not applicable — the note specifies a state component, a refined transition relation, and conformance/invariance guarantees abstractly enough that any conforming substrate would have to satisfy them; it has not drifted into implementation mechanics.

VERDICT: REVISE
