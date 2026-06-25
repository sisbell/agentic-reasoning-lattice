| Σ.M(d) domain restriction (S8a) | `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — arrangements map only V-positions; per-component form stated at the S8a definition site | axiom (definitional); T0 (ASN-0034) |

- *Depends:*
  - T0 (ASN-0034) — supplies the equivalence `zeros(t) = 0` iff every component is positive, used in the S8a per-component reformulation of the domain restriction
  - Σ.C (ContentStore) — supplies the immutable content-store component; the strand is defined as the paired object `(Σ.C, Σ.M)`, and the separation `C` invariant / `M(d)` mutable is the premise this claim's invariants rest on