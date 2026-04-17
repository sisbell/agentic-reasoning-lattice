# Accretion

## Pattern

Properties grow the lattice by adding new properties, not by mutating existing ones. Each new fact becomes its own citable unit with its own formal contract. Existing properties stay untouched as the lattice grows around them.

## Forces

- **New facts need homes.** As downstream reasoning develops, it uses facts the lattice has not yet stated. These facts need to live somewhere.
- **Mutation invalidates citations.** Adding a clause to an existing property changes what "citing P" means. Every prior dependent of P may now have an incomplete citation.
- **Addition preserves citations.** Adding a new property changes nothing about existing ones. Prior dependents stay valid; only new dependents pick up the new property.
- **Locality wants mutation; stability wants addition.** Editing one file looks smaller per edit. Adding a new file stays smaller across the whole lattice. The two optimizations point in opposite directions.

## When it works

- The new fact is genuinely new — not a correction of an existing fact
- The fact can be stated independently enough to stand as its own property
- Downstream consumers cite the new property directly, rather than relying on the old one

## When it fails

- The "new fact" is actually a fix to an existing one — mutation is unavoidable
- The fact cannot be separated from an existing property without breaking both
- Accretion is used to avoid thinking, producing a sprawl of trivial properties that each state one clause

## Leads to

[Contract Sprawl](../equilibrium/contract-sprawl.md) — Accretion is the discipline that prevents Contract Sprawl. A Genesis Attractor forms when downstream reasoning has nowhere to put new facts; Accretion provides that home as a new property rather than a mutation of the introducer.

[Reasoning lattice](reasoning-lattice.md) — Accretion is how the lattice grows inward (new foundational facts) and outward (new derived facts). [Scope Promotion](scope-promotion.md) is accretion applied to boundary observations; [Extract/Absorb](extract-absorb.md) is accretion applied to shared concepts pulled from existing properties.

## Origin

Observed as the resolution to Contract Sprawl. During ASN-0034's cone sweep, T0 accumulated ℕ axioms (well-ordering, discreteness, ordering, additive identity) as different proofs discovered they needed them. Each addition invalidated prior citations. The fix was structural: split T0's accumulated clauses into independent properties. After the split, adding the next ℕ axiom the lattice needs is accretion — a new property — rather than mutation.
