**AX-1 (Initial empty state).** In the initial state `Σ₀`, the content store is empty and no document possesses any V-mappings: `dom(Σ₀.C) = ∅` and `(A d : dom(Σ₀.M(d)) = ∅)`.

Before any operation has been performed, neither content nor arrangement exists. This is the ground on which inductive invariants over the operation history stand: without it, properties such as S3 (referential integrity) that are proved by induction have no base case, and existence proofs such as S5 (unrestricted sharing) cannot determine the content store at the trace's origin. The axiom captures the system's starting condition — all structure, both content and arrangement, is introduced by explicit operations.

*Formal Contract:*
- *Axiom:* `dom(Σ₀.C) = ∅` — the content store is empty in the initial state; `(A d : dom(Σ₀.M(d)) = ∅)` — no document possesses any V-mappings in the initial state.
