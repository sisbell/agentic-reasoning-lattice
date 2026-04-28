## Formal summary

We collect the structure. The tumbler algebra is a tuple `(T, <, ⊕, ⊖, inc, fields, Z)` where `Z = {t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0)}` is the set of zero tumblers:

- `T` is the carrier set of finite sequences of non-negative integers, with unbounded component values (T0(a)) and unbounded length (T0(b))
- `<` is the lexicographic total order on `T` (T1), intrinsically computable (T2), with canonical representation (T3)
- The hierarchical parsing function `fields` extracts four-level containment (T4), yielding contiguous subtrees (T5); decidable containment (T6, corollary of T4) and element subspace disjointness (T7, corollary of T3, T4) follow
- `T8` establishes allocation permanence — once allocated, an address is never removed from the set of allocated addresses
- `T9–T10` establish forward allocation and partition independence; `T10a` constrains each allocator to use `inc(·, 0)` for sibling outputs, reserving `k > 0` exclusively for child-spawning
- `⊕` and `⊖` are order-preserving operations on T (TA0–TA3, with TA0 requiring `k ≤ #a`), with weak order preservation universally (TA1 `≤`, TA3 `≤`) and strict preservation under tighter conditions (TA1-strict when `k ≤ min(#a, #b) ∧ k ≥ divergence(a,b)`, TA3-strict when `#a = #b`); strict increase (TA-strict); partially inverse when `k = #a`, `#w = k`, and all components of `a` before `k` are zero (TA4)
- `inc` is hierarchical increment for allocation (TA5)
- Zero tumblers (all components zero, any length) are sentinels, not valid addresses (TA6); positivity is defined as having at least one nonzero component
- `TA7a` confines element-local shifts to their subspace (algebraic closure)
- Spans are self-describing contiguous ranges (T12)
- D0–D2 characterize displacement recovery: D0 is the well-definedness precondition, D1 is the round-trip identity a ⊕ (b ⊖ a) = b, D2 is uniqueness (corollary of D1, TA-LC)
- OrdinalDisplacement and OrdinalShift define the shift apparatus — ordinal displacement δ(n, m) and shift(v, n) = v ⊕ δ(n, #v); TS1–TS5 establish that shift preserves order (TS1), is injective (TS2), composes additively (TS3), strictly increases (TS4), and is monotone in amount (TS5)

Each property is required by at least one system guarantee:

| Property | Required by |
|----------|-------------|
| T0(a), T0(b) | Unbounded growth of docuverse |
| T1, T2 | Span containment, link search, index traversal |
| T3 | Address identity, uniqueness, total order consistency |
| T4, T5 | Hierarchical queries, self-describing spans |
| T6 *(corollary of T4)* | Decidable containment |
| T7 *(corollary of T3, T4)* | Subspace isolation |
| T8 | Link stability, transclusion identity, attribution |
| T9 | Per-allocator monotonicity; partition monotonicity derived from T9 + T10 + T1 |
| T10, T10a | Decentralized allocation, global uniqueness |
| T12 | Content reference by span |
| TA0–TA4, TA-strict | Span computation, position advancement, span non-emptiness (T12) |
| TA5 | Address allocation |
| TA6 | Sentinel and lower bound |
| TA7a | Subspace isolation (algebraic closure) |
| TA-LC, TA-RC, TA-MTO *(lemmas)* | Cancellation characterization of ⊕; TA-MTO equivalence classes constrain span-endpoint recovery |
| D0 | Displacement recovery precondition |
| D1 | Displacement round-trip: span-endpoint recovery from start + displacement |
| D2 *(corollary of D1, TA-LC)* | Displacement uniqueness |
| OrdinalDisplacement, OrdinalShift | Element-level position advancement (Istream allocation, V-enfilade traversal) |
| TS1–TS5 *(lemmas/corollaries)* | Order-safe shifting: TS1 order preservation for sorted-sequence maintenance, TS2 injectivity for address uniqueness under shift, TS3 composition for multi-step allocation, TS4–TS5 monotonicity for forward progress |

Removing any independent property breaks a system-level guarantee. T6 and T7 are derived (corollaries of T4, T3 respectively) and are stated for emphasis, not as independent axioms. TA-LC, TA-RC, and TA-MTO are structural lemmas derived from TumblerAdd's constructive definition and T3 — they characterize cancellation asymmetry and the many-to-one equivalence classes of `⊕`, but introduce no independent content beyond the definition.
