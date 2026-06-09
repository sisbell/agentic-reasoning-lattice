# Review of ASN-0126

## REVISE

### Issue 1: Conjunct-ordering / domain-discharge justification restated three times
**ASN-0126, The shape-gated emit (and Shape-conformance, and P6 proof)**: "(0) and (i) jointly discharge the domain condition for (ii)... Precondition (0) is the gate that makes (ii) well-defined"; then in the wp paragraph: "Their ordering is load-bearing: `Sh-conf(K, F, G)` carries a truth value only on registered K... so `K registered` is the domain-discharging conjunct and the conjunction is read left-to-right"; then again in the P6 proof and in Shape-conformance ("defined only for *registered* K").
**Problem**: The single fact — `Sh-conf` is undefined on unregistered K, so registration is checked first — is re-derived in four places. After the first statement it advances no reasoning; the precise reader skips it each time.
**Required**: State the domain-discharge ordering once (at the definition of `K.λ_sh`'s preconditions), then refer to it by name without re-explaining.

### Issue 2: The shape-gated emit and the Worked illustration defer to each other
**ASN-0126, The shape-gated emit**: "the born-nullified case, witnessed concretely in the Worked illustration." **Worked illustration, Born nullified**: "This is the witness that The shape-gated emit's gate-vs-landing separation forward-points to."
**Problem**: A circular cross-reference pair — each section points at the other for the payload. This is the "multiple paragraphs defer to the same downstream location" pattern, here mutual. The forward pointer in the gate section plus its anticipatory sentence ("Such a pre-existing covering tuple is attainable at a general `→_sh`-reachable state...") duplicate what the example then re-states.
**Required**: Let the gate section assert the gate-vs-landing separation and the example demonstrate it; drop the mutual "witnessed below / forward-points-to above" framing.

### Issue 3: Projection-bridge prose is padded with defensive anti-misreading
**ASN-0126, The shape-gated emit**: "This note's state carries a fourth component, so `→_sh` is not literally a subrelation of ASN-0086's three-component `→` — the two relate different state types, and 'every `→_sh*`-reachable state is `→*`-reachable' cannot be read as a set inclusion between four-tuples and three-tuples."
**Problem**: The substantive content is `π(Σ) = (Σ.C, Σ.M, Σ.L)` and `π(Σ_init) = Σ_init^{0086}`, giving `Σ →_sh Σ' ⟹ π(Σ) → π(Σ')`. The quoted sentence pre-empts a misreading no one stated, and the same projection argument is then re-walked in full inside the P6 proof ("By the projection argument above... Since `a_emit` reads only M and L..."). Two passes over one bridge.
**Required**: Define `π` and the step-correspondence once; in P6 cite it rather than re-deriving the `a_emit(π(Σ),d) = a_emit(Σ,d)` and reachability sub-steps.

### Issue 4: Use-site inventory in the no-residence-check claim
**ASN-0126, Shape-conformance**: "`Sh-conf` does not test membership in `dom(Σ.C)`, `dom(Σ.L)`, or any state-indexed address set such as ASN-0086's `A_doc^Σ`, `A_rel^Σ`, `A^Σ`."
**Problem**: The claim is "Sh-conf consults no state-indexed set." Enumerating each named set ASN-0086 happens to define is inventory that adds no content beyond the general statement, and re-binds this note to ASN-0086's vocabulary list.
**Required**: State "Sh-conf consults no state-indexed address set" once; the worked P5 example already exhibits the ghost/stored case concretely.

### Issue 5: Defensive scope-limiting in the introduction
**ASN-0126, intro**: "This note supplies that — and only that." and "The lattice's actual usage is uniformly single-source. The right level of commitment is concrete shapes the substrate can statically check, with everything operational layered on top."
**Problem**: "and only that," the usage-appeal, and the "right level of commitment" editorializing are meta-prose about the note's scope, not about substrate state or operations. They defend the boundary rather than advance a claim.
**Required**: Open with what the note adds (shape catalog, gate, immutable registry) and let the Open-questions section carry the boundary.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, behavior catalog, default predicates
**Why out of scope**: The Open-questions section correctly defers these to the operational successor note. The `idem` flag is registered and frozen here without operational meaning, which is the right minimal commitment — its semantics are genuinely new territory, not a gap in this framework.

META: (not applicable — the note defines substrate state, a gated operation, and state-independent invariants an alternative implementation would also have to satisfy; it has not drifted into implementation mechanics.)

VERDICT: REVISE
