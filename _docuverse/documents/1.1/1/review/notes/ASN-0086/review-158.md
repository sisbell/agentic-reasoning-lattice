# Review of ASN-0086

I checked the major proofs (R0, R0a, R-Scope, R6a–c, R7a, L-ContiguousPrefix, Cor1, and the wp analysis) and the worked example against the foundation contracts. The rigor is strong: first/subsequent emission branches, cross/same-home freshness, empty link store, and nested-witness cases are all handled, and the wp Case 2 derivation is genuinely two-directional with load-bearing counterexamples. The findings below are the anti-bloat patterns this note is classified to surface — proof-narration and restatement accreted into structural slots.

## REVISE

### Issue 1: Properties table cells carry proof-structure commentary, not statements
**ASN-0086, Properties Introduced table**:
- R0 row: "...and yields a state-local-conforming post-state Σ' (**full state-local L/S-invariant catalog re-derived conjunct-by-conjunct at the fresh key**)"
- L-ContiguousPrefix row: "...the reachable case is ChainMembershipForOrigin (ASN-0093), and L-ContiguousPrefix extends it to all substrate-conforming states; **proof independent of R0a**"
- R0a row: "...same-home via L-ContiguousPrefix"

**Problem**: A summary table should state *what* a property guarantees. "re-derived conjunct-by-conjunct," "proof independent of R0a," and the proof-dependency notes are commentary about *how* the proof runs — essay content in a structural slot. A reader scanning the table has to skip the method-narration to extract the claim. These notes belong in (and already appear in) the proof bodies.

**Required**: Reduce each cell to the property statement and its type. Move proof-method and dependency remarks ("re-derived conjunct-by-conjunct," "proof independent of R0a," "reachable case is ChainMembershipForOrigin") out of the table; they are already present where they are load-bearing.

### Issue 2: `→ ≡ K.σ ∪ K.α ∪ K.λ` is stated three times in immediate succession
**ASN-0086, State transition relation**: the equation `→ ≡ K.σ ∪ K.α ∪ K.λ`, then the single-bullet list "each →-step is one of: — a K.σ-step extends `dom(Σ.M)`, a K.α-step extends `dom(Σ.C)`, and a K.λ-step extends `dom(Σ.L)`...", then "Every dom-extending transition in `→` is one of the three K-ops; the substrate exposes no removal, replacement, or in-place mutation transition..."

**Problem**: Three consecutive constructs assert the same fact — that `→` is exactly the three K-ops and nothing else. The degenerate one-item bullet list adds no structure over the equation, and the following sentence restates closure a third time. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: Keep the equation plus one sentence naming each K-op's affected component and the closure/no-removal property. Drop the single-bullet list.

## OUT_OF_SCOPE

### Topic 1: Atomicity/consistency of Emit relative to concurrent Observe
The note's open questions (Emit atomicity w.r.t. Observe, consistency model for `A_K` transitions, ordering of Observe results) are correctly deferred — they concern a concurrency model the substrate does not yet specify, not a gap in the present single-authority transition semantics.

### Topic 2: Multi-arity typed relations
Higher-arity links (`|Σ.L(a)| > 3`) are explicitly excluded from `L_K` and from this note's scope; their binary-projection-vs-`n`-ary treatment is future territory.

VERDICT: REVISE
