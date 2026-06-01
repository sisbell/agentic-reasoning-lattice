# Review of ASN-0086

## REVISE

### Issue 1: R7a's proof invokes L-ContiguousPrefix at Σ' without requiring the pre-state Σ to be substrate-conforming

**ASN-0086, R7a (NoExtraClassAffectsL), discharge (4)(i)**: "By clauses (b)–(c) of substrate-conformance ... every key in `dom(Σ'.L)` was emitted at its home's sibling frontier, so L-ContiguousPrefix (ContiguousPrefix) holds at Σ'."

**Problem**: R7a's hypothesis is only that the transition is "issued by a substrate-conforming layer." The *Definition — substrate-conforming layer* guarantees only that the layer's operations carry **substrate-conforming states to substrate-conforming states** — i.e., conformance is preserved *given a conforming input*. The lemma never assumes Σ itself is substrate-conforming. But clauses (b)–(c) constrain only the single transition `Σ → Σ'`; they say nothing about how the keys already present in `dom(Σ.L)` were deposited. The assertion "every key in `dom(Σ'.L)` was emitted at its home's frontier" therefore covers the pre-existing keys only if the *prior* trajectory was also conforming — exactly what L-ContiguousPrefix's own induction requires (`Σ_init = Σ_0, …, Σ_N = Σ`, each step preserving (a)–(c)). If Σ is reached partly through a non-conforming actor, pre-existing keys may be off-frontier (the Remark — NestedLinkWitness state is state-local-conforming but not substrate-conforming), L-ContiguousPrefix fails at Σ', and discharge (4)'s claim that K.λ's emission rule selects exactly `a_k` collapses (K.λ only ever lands at the frontier; it cannot reproduce a nested key).

**Required**: Add "Σ substrate-conforming" (equivalently, Σ reachable from `Σ_init` via conforming steps) to R7a's hypotheses, and derive Σ' substrate-conformance from the layer's preservation property *before* invoking L-ContiguousPrefix at Σ'. The reduction corollary should then confirm the relational layer satisfies this from `Σ_init`.

### Issue 2: Definition — Nullified carries a defensive justification enumerating a downstream consumer

**ASN-0086, Definition — Nullified**: "The set-builder restriction `a ∈ A_rel^Σ` is intentional: only tuple addresses are eligible for nullification, since `A_K^Σ` (the consumer of `nullified`) ranges over tuple addresses alone."

**Problem**: This is the "definition's introduction enumerates downstream consumers" pattern flagged by the anti-bloat classifier. The clause justifies *why* the restriction is present by naming its downstream use site (`A_K^Σ`) rather than advancing the definition's meaning. The set-builder already states the restriction; the editorial defense ("is intentional," "the consumer of `nullified`") is meta-prose.

**Required**: Drop the justification. State the set-builder and, if a scope note is genuinely needed, keep it to the substantive fact ("ghost/content addresses in `coverage(G')` are not collected") without the consumer inventory.

### Issue 3: Emit_K Definition states the type-index/value-argument distinction twice

**ASN-0086, Definition — Emit_K**: "K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation with the same shape" and, in the same block, "*Precondition.* `K ∈ T_admissible` (discharged at the type-index, not at the value-argument list)."

**Problem**: Two sentences in one Definition block assert the same point (K is a subscript/type-index, not a value argument). This is the "two paragraphs saying the same thing" pattern.

**Required**: Keep the distinction once (in the signature line) and remove the duplicate parenthetical from the Precondition.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, cardinality bounds on `nullified(Σ)`, multi-arity typed relations

**Why out of scope**: These are correctly deferred in the Open Questions list. They concern a consistency model and higher-arity relational algebra not yet defined; they are new territory, not defects in this note's standard-triple development.

VERDICT: REVISE
