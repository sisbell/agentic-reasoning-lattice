**AX-1 (InitialEmpty).** The protocol designates a base state `Σ₀` — the configuration that holds before any operation — in which no arrangement maps any V-position:

`(A d :: dom(Σ₀.M(d)) = ∅)`

Every reachable state is generated from `Σ₀` by the transition relation `Σ → Σ'`. Before any content has been allocated, and before any document arranges any position, each arrangement `Σ₀.M(d)` is the empty partial function, so its domain is empty. We are not deriving this from anything; we are fixing the starting configuration. The point of naming it is methodological: an invariant on `M` proved by induction on transitions needs an explicit, citable anchor for its base case, and the empty base state is that anchor — the configuration on which every such invariant holds vacuously, there being no mapped position to witness a violation.

*Formal Contract:*
- *Axiom:* The base state `Σ₀` satisfies `(A d :: dom(Σ₀.M(d)) = ∅)` — no V-position is mapped by any arrangement in the initial configuration. This is a protocol design posit on the designated start state of the state signature, not derived from any other claim.
