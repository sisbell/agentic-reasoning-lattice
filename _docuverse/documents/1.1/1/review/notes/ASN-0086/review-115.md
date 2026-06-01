# Review of ASN-0086

## REVISE

### Issue 1: R0/Emit_K/wp domain declared as the full `↝*` state space, but the proofs rely on state-local invariants the full space explicitly need not preserve

**ASN-0086, Definition — Categorical reachability**: "states produced by higher-layer operations that need not preserve the L/S/M/C invariant catalog or the ASN-0093 chain discipline … **The bare operations `Emit_K`/`Nullify` and the weakest-precondition computations below range over the full (`↝*`-reachable) state space**."

**ASN-0086, R0 proof (subsequent emission)**: "the state-local invariant L1c (LinkAllocatorConformance, ASN-0043) holds at every state the substrate admits, the non-conforming `↝*`-reachable states included (a non-conforming state violates only R0a's antichain, never L1c)."

**Problem**: These two statements contradict each other. L1c (and L-fin, L0, L12a) are members of the L/S/M/C invariant catalog — L1c is listed in ASN-0043's `StateLocalInvariants`. The categorical-reachability definition explicitly admits states that do **not** preserve that catalog. Yet R0's subsequent-emission branch consumes L1c in a load-bearing way:

- It derives `T4-valid(ℓ_prev)` via "L1c … so `ℓ_prev` is the terminus of a T10a-conforming allocation chain and T10a.4 gives `T4-valid(ℓ_prev)`," then applies TA5-SigValid to conclude `inc(ℓ_prev, 0)` advances only the terminal position (hence `zeros(a) = 3`). If `ℓ_prev` is **not** T4-valid (permitted in the full `↝*` space), `sig(ℓ_prev) < #ℓ_prev` is possible, `inc(ℓ_prev, 0)` advances a non-terminal position, and the resulting `a` need not be a valid link address — breaking both the freshness derivation and the L-invariant preservation claim.
- It also relies on L-fin ("the homed set is finite") for `max{…}` to exist; the full space need not preserve L-fin either. The Lemma — Emit_K function-ness inherits the same dependence.

The parenthetical "a non-conforming state violates only R0a's antichain, never L1c" is an unproven universal. The note's only witness (the `a'' = inc(a, 1)` example) happens to preserve the L-catalog while breaking R0a — but that is one example, not a characterization of the full `↝*` space.

**Required**: Restrict the domain of R0, Emit_K, Nullify, and the wp computations to states satisfying the state-local L/S-invariants (in particular L1c and L-fin) — a sub-space of `↝*` strictly larger than the `→*`-conforming states (so the `a'' = inc(a,1)` target case is retained). Alternatively, prove that no `↝*`-reachable state can violate L1c/L-fin (which contradicts the categorical-reachability definition's own text and so would require redefining `↝`). The current "full state space" declaration over-reaches what the proofs establish.

### Issue 2: WP Case 1 conflates per-conjunct load-bearingness with weakest-precondition; P2c (full conformance) is strictly stronger than weakest

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "*Necessity (each conjunct is load-bearing):* necessity needs only one counterexample. … Hence `P0 ∧ P1 ∧ P2c` is weakest, not merely sufficient."

**Problem**: A weakest precondition must **exactly** characterize the set of pre-states from which the postcondition is guaranteed: `σ ⊨ wp(S,R) ⟺ (S from σ yields σ' ⊨ R)`. The argument only checks that dropping each single conjunct admits *some* failing state. That establishes load-bearingness, not weakestness. P2c (`Σ` substrate-conforming) is a **global** condition, but the postcondition `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` is **local** to `a`'s prefix-subtree.

Concrete counterexample to weakestness: take `Σ` non-conforming with exactly one nested link pair `(c, c'')`, `c ≼ c''`, both homed at a document `d_c ≠ home(a)`, with `a`'s prefix-subtree containing no link address other than `a`. Then `P0 ∧ P1` holds and `¬P2c`. Choosing `d_retr = home(a)`, the chain at `home(a)` is locally clean, so `b = inc(ℓ_prev, 0)` is a sibling of the homed chain with `a ⊀ b`, and `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` — the postcondition **holds** from a `¬P2c` state. Therefore `wp ⊋ P0 ∧ P1 ∧ P2c`, and the "weakest, not merely sufficient" claim is false.

Note Case 2 correctly uses local conditions (`NoCraftedSpanReachesD(Σ, d)`, a universal over the actual `L_R^Σ` tuples) rather than global conformance — which is exactly what Case 1's true weakest precondition should be (a local antichain condition on `a`'s subtree plus non-collision of the fresh emitter), not blanket conformance.

**Required**: Either (a) replace P2c with the genuine local weakest condition — roughly "`{t : a ≼ t} ∩ dom(Σ.L) = {a}` and the fresh emitter `a_emit(Σ, d_retr) ∉ {t : a ≼ t}`" — and prove that exact characterization, or (b) downgrade the claim from "weakest" to "a sufficient precondition; each conjunct load-bearing," and stop asserting weakestness. As written, the wp is not weakest.

### Issue 3: Duplicated justification prose around forward references (anti-bloat)

**ASN-0086, R0a Case 2** vs **R0a-Cor1 proof**: Case 2 says "By R0a-Cor1 (… stated and proved below — its argument rests on conformance clause (b) and the chain lemmas alone, not on R0a, so the forward reference is non-circular)." The R0a-Cor1 proof then repeats: "the argument never invokes R0a, so the forward reference in R0a Case 2 is non-circular."

**ASN-0086, R0 proof**: The rationale "we discharge freshness directly, *without* ASN-0093's [FirstEmissionFreshness | ChainMembershipForOrigin / SubsequentEmissionFreshness] — … established only at `→*`-reachable (conforming) states — so that the argument carries over to the non-conforming `↝*`-reachable states the wp computations range over" appears near-verbatim in both the first-emission and subsequent-emission branches.

**Problem**: The non-circularity of the R0a/R0a-Cor1 forward reference is asserted twice (once at the citation site, once at the definition site) — exactly the flagged pattern "prose justifies document ordering / the forward pointer is non-circular by Y argument" plus "two paragraphs defer to the same downstream location." The conformance-free rationale is also restated across R0's two branches. This is reviser-drift accretion: the non-circularity claim belongs once, at the proof that establishes it; the citation site needs only "by R0a-Cor1." (Issue 1 further undermines the "carries over to non-conforming states" rationale, since the domain should be restricted in the first place.)

**Required**: State the non-circularity once (in R0a-Cor1's proof), and let R0a Case 2 cite R0a-Cor1 plainly. Collapse the duplicated conformance-free rationale in R0 to a single statement.

## OUT_OF_SCOPE

### Topic 1: Consistency model for concurrent Emit/Observe and ordering of Observe results
**Why out of scope**: The Open Questions raise atomicity of Emit vs. Observe and the ordering guarantee on Observe results. These are genuine future concerns but the present note specifies single-step transition semantics; concurrency/consistency is new territory, not a defect here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note deliberately restricts to standard triples (`|Σ.L(a)| = 3`). Generalizing `L_K` to arity > 3 is a separate construction the note flags but does not pursue.

META: not applicable — the ASN defines abstract state slices, operations, and invariants on the link store; it has not drifted into implementation mechanics.

VERDICT: REVISE
