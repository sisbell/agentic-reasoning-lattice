**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. This is a design requirement on every reachable state: no document arrangement is permitted to hold infinitely many V-positions.

*Formal Contract:*
- *Axiom (design requirement):* For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.
- *Postconditions:* `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- *Frame:* No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

- *Depends:*
  - Σ.M(d) (Arrangement) — supplies the arrangement partial function `M(d) : T ⇀ T` whose domain finiteness this claim constrains
- *Forward References:*
  - Σ.C (ContentStore) — named in the Frame as the component whose unbounded growth this claim explicitly does not restrict