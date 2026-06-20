note pins them" — but fixing `Unary/⊤/{}` for both *inside the spec body* reads as settled when it is genuinely a build-time agreement. Surface it as a named coordination point alongside the `ReservedAddrs` addresses so a builder treats the registrations as an M9-negotiated constant, not a derived fact.

10. **[SHARPENING] Carry the §2 slot convention (F=old, G=new) explicitly into the M8 contextual-discovery seam.** The design routes archival `in/out` through `match_links + type_slice` and states the convention in Conflict §2, but EL11(a)'s contextual discovery (`project(eᵢ, d) ≠ ∅ ⟺ listed(endpoint, d)`) is left for M8 to assemble. Since the design flipped ASN-0125's slots, note at the M8 seam that contextual discovery must project the **FROM** slot for `listed(old)` and **TO** for `listed(new)` — so M8 doesn't implement EL11(a) against ASN-0125's original (opposite) convention.

---

The module is buildable from this document alone, calls every upstream interface as given, honors the source notes' contracts (Permanence, L3-at-write-boundary, L8 exactness on the matched surface, ML1 coverage-exactness via `iextent`-equals-subtree, I1/I2 dedup-and-resurrection, DR no-sterilization, the BH1–BH4 atoms, EL6/EL7/EL12), keeps within its boundary (delegates minting to M3, arrangement/seating/R to M5, ordering to M2, cursoring/counting/projection to M8, L14a enforcement to M5), and resolves all nine cross-note conflicts with stated, sound resolutions. The two-surface architecture, the append-only-`links`-plus-recomputable-hints spine, and the `coverage_class` totality argument are internally consistent. No item above would stop or mislead a competent builder.

VERDICT: CONVERGED
