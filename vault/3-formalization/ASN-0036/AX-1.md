**AX-1 (Initial empty arrangement).** In the initial state `Σ₀`, no document possesses any V-mappings: `(A d : dom(Σ₀.M(d)) = ∅)`.

Before any operation has been performed, no arrangement exists. This is the ground on which inductive invariants over the operation history stand: without it, properties such as S3 (referential integrity) that are proved by induction have no base case. The axiom captures the system's starting condition — all structure is introduced by explicit operations.

*Formal Contract:*
- *Axiom:* `(A d : dom(Σ₀.M(d)) = ∅)` — no document possesses any V-mappings in the initial state.
