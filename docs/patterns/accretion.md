# Accretion

## Pattern

Claims grow the lattice by adding new claims, not by mutating existing ones. Each new fact becomes its own citable unit with its own formal contract. Existing claims stay untouched as the lattice grows around them.

## Forces

- **New facts need homes.** As downstream reasoning develops, it uses facts the lattice has not yet stated. These facts need to live somewhere.
- **Mutation invalidates citations.** Adding a clause to an existing claim changes what "citing P" means. Every prior dependent of P may now have an incomplete citation.
- **Addition preserves citations.** Adding a new claim changes nothing about existing ones. Prior dependents stay valid; only new dependents pick up the new claim.
- **Locality wants mutation; stability wants addition.** Editing one file looks smaller per edit. Adding a new file stays smaller across the whole lattice. The two optimizations point in opposite directions.

## When it works

- The new fact is genuinely new — not a correction of an existing fact
- The fact can be stated independently enough to stand as its own claim
- Downstream consumers cite the new claim directly, rather than relying on the old one

## Design for accretion

Whether growth happens by accretion or by mutation is determined at the moment a concept is introduced. Two design signals tell the reviser where new facts should go:

**Enumerated surface vs. open surface.** A claim named `T10a` with numbered consequences `T10a.1, T10a.2, T10a.3` signals that facts about allocator discipline live in new numbered siblings. When a proof discovers a missing fact, the natural move is `T10a.6` — a new claim. A claim whose contract says "with its standard claims" leaves the surface open; new facts have nowhere to go except inside the existing contract.

**One concept vs. bundled concepts.** A claim that introduces one concept has a finite, cohesive set of consequences. A claim that bundles two concepts — especially when one has an unbounded set of axioms — becomes a [Genesis Attractor](../equilibrium/contract-sprawl.md#cause-genesis-attractor) for whichever concept is least pre-structured. T0 bundled the carrier set `T` (cohesive) with the ambient system ℕ (unbounded standard claims). ℕ's axioms accumulated in T0 because T0 was the only home they had.

Pre-structure the lattice for accretion by:
- Enumerating named claims for each sub-fact a concept has, even before downstream needs surface
- Keeping one concept per claim — if a claim introduces both `X` and ambient `Y`, factor `Y` out before `Y`'s axioms start accumulating
- Naming claims in a way that signals "more like this will appear" — numbered families (`T10a.N`), prefixed groups (`NAT-*`), tagged variants (`foo-strict`)

The reviser reads the structure and follows it. Structure determines behavior.

## Leads to

[Contract Sprawl](../equilibrium/contract-sprawl.md) — Accretion is the discipline that prevents Contract Sprawl. A Genesis Attractor forms when downstream reasoning has nowhere to put new facts; Accretion provides that home as a new claim rather than a mutation of the introducer.

[Reasoning lattice](reasoning-lattice.md) — Accretion is how the lattice grows inward (new foundational facts) and outward (new derived facts). [Scope Promotion](scope-promotion.md) is accretion applied to boundary observations; [Extract/Absorb](extract-absorb.md) is accretion applied to shared concepts pulled from existing claims.

## Origin

Observed as the resolution to Contract Sprawl. During ASN-0034's regional sweep, T0 accumulated ℕ axioms (well-ordering, discreteness, ordering, additive identity) as different proofs discovered they needed them. Each addition invalidated prior citations. The fix was structural: split T0's accumulated clauses into independent claims.

After the split, review/revise iteration found that more ℕ axioms were needed than the initial split enumerated — `NAT-addassoc`, `NAT-cancel`, `NAT-sub` were discovered as proofs used them. Each was added as a new claim rather than as a clause extension to an existing NAT-* axiom. Full-review converged after the accreted axioms were in place and all downstream citations pointed at specific NAT-* claims. The pattern worked not just as a theoretical fix but as the operational response mechanism once the attractor was dissolved.
