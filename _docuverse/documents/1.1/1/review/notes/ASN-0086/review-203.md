# Review of ASN-0086

This is a mature, heavily-revised note. The core proofs (R0, R0a, R-Scope, R1–R6, the wp Case 2 derivation, the worked sketch) are sound and the concrete five-step example genuinely exercises the key postconditions. My findings concern over-reach beyond the note's core, not errors in the central argument.

## REVISE

### Issue 1: The `↝` / conformance-taxonomy / R6d / R7a apparatus generalizes to higher-layer operations that do not exist
**ASN-0086, "State transition relation" through R6d/R7a**: "We write `↝` for the *categorical* state-transition relation: the union of `→` with every state-transition relation any higher-layer operation may admit over `(Σ.C, Σ.M, Σ.L)`."

**Problem**: The note explicitly states that within its substrate there are no operations other than K.σ/K.α/K.λ ("*Arrangement modification is out of scope... the substrate admits no arrangement-modifying transition*"). So `↝` quantifies over a set of operations that is presently empty. R7a ("for any `Σ ↝ Σ'` issued by a substrate-conforming layer...") and R6d ("no conforming higher-layer op un-nullifies a tuple") are guarantees about those hypothetical operations. R7a's long decomposition proof has exactly one consumer — R6d — and R6d has no in-ASN consumer at all. The supporting apparatus (`↝`, `↝*`, categorical reachability, Definition — substrate-conforming layer) is forward-reference setup whose entire payoff is this terminal, hypothetical-layer generalization.

The conformance taxonomy itself (substrate-conforming vs state-local-conforming, Remark — NestedLinkWitness, Definition — state-local-conforming state) exists chiefly to support this generalization: R0a/R-Scope/R0/L-ContiguousPrefix could all be stated over `→*`-reachable states of the K-substrate, where R0a's antichain is automatic from the K.λ discipline. The "substrate-conforming" abstraction earns its keep only by asserting these survive `↝`-conforming layer steps.

**Required**: Cut R6d, R7a, the `↝`/categorical-reachability definitions, and the substrate-conforming/state-local-conforming taxonomy, and state the core results (R0, R0a, R-Scope, R0, L-ContiguousPrefix) over `→*`-reachable states. Defer "what nullification guarantees survive higher-layer operations" to the future ASN that actually introduces those operations. If R6d/R7a are retained, justify why a guarantee over a currently-empty class of operations belongs in this note rather than in the layering ASN.

### Issue 2: L-ContiguousPrefix re-proves a foundation lemma for the reachable case
**ASN-0086, L-ContiguousPrefix**: "`{a ∈ dom(Σ.L) : home(a) = d} = {incʲ(d.0.s_L.1, 0) : 0 ≤ j ≤ J_d^Σ}`"

**Problem**: With `home = origin` on link addresses and the chain enumeration coinciding with `A_L(d)`, this is ASN-0093's ChainMembershipForOrigin (link half) for reachable states — the note itself concedes this ("L-ContiguousPrefix here is its reachable case, which coincides with ChainMembershipForOrigin (ASN-0093)"). The note re-derives the reachable case by induction rather than citing the foundation. The only new content is the extension to `↝`-conforming-but-not-reachable states, which serves only the Issue-1 apparatus.

**Required**: Cite ChainMembershipForOrigin (foundation) for the reachable case instead of re-deriving it. If Issue 1 is accepted, L-ContiguousPrefix collapses entirely into the foundation lemma and the local lemma should be removed in favor of a direct citation.

### Issue 3: "Tuple address" / `A_rel^Σ` terminology overclaims relative to the arity-3 restriction
**ASN-0086, Definition — Partition**: "`A_rel^Σ = dom(Σ.L)` — relation-tuple addresses"; and Definition — TupleAddress: "`addr : L^Σ → A_rel^Σ`".

**Problem**: `L^Σ = ⨆ L_K^Σ` is restricted to standard-triple links (`|Σ.L(a)| = 3`); higher-arity links live in `dom(Σ.L)` but in no `L_K`. So `A_rel^Σ = dom(Σ.L)` — labeled "relation-tuple addresses" — contains addresses that correspond to no tuple, and `addr`'s codomain strictly exceeds its image. Consequently `nullified(Σ)` (restricted to `A_rel^Σ`) can collect a higher-arity link address that is in no active subset, and `Observe`/`A_K` silently ignore such addresses. The behavior is consistent, but the "tuple address" label and the `addr` codomain assert a bij_correspondence the arity-3 restriction breaks.

**Required**: Either restrict `A_rel^Σ` to arity-3 link addresses, or rename it (e.g. "link-store addresses") and note explicitly that higher-arity addresses inhabit `A_rel^Σ` without participating in any `L_K`. State `addr`'s codomain as the image, or note it is into-but-not-onto.

## OUT_OF_SCOPE

### Topic 1: Atomicity and consistency model for concurrent Emit/Observe
**Why out of scope**: The note's own Open Questions defer this ("Must Emit be atomic with respect to concurrent Observe... what is the consistency model"). Correctly deferred — this ASN's transitions are sequential and atomic by SequentialTransitionAxiom (ASN-0093).

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note flags the `|Σ.L(a)| > 3` generalization as future work; the standard-triple restriction is a legitimate scoping choice for this note (modulo the Issue-3 terminology fix).

META: Not applicable — the core (typed relations, active/audit distinction, three operations) defines state, operations, and invariants abstractly and belongs in the specification; the note has over-generalized toward hypothetical layers, not drifted into implementation mechanics. Trim, do not terminate.

VERDICT: REVISE
