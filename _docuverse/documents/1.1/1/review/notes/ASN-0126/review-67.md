# Review of ASN-0126

I checked all six properties (P1–P6) against their proofs, the K.λ_sh precondition set and its edge cases, the weakest-precondition derivation (guarded-command lifting, the K ∈ T_admissible / L3 / precondition-(0) absorptions, the C2/C3 witnesses), the projection bridge, the registry well-formedness/decidability argument, and the worked illustration's address arithmetic and born-nullified trace. The core is sound: the gate is completely specified, effect-identity and the bridge are correctly used, the boundary cases (empty F, |F| ≥ 2 abutting spans, empty G, arity > 3, unregistered K, self-nullifying retraction, non-unit region retraction, first emission, ghost endsets) are all handled, and the wp analysis genuinely finds the non-trivial born-nullified case. Foundation usage (ASN-0043/0086) is accurate and there are no improper cross-ASN references. One cleanup remains.

## REVISE

### Issue 1: `touched` is dead inventory in the worked illustration
**ASN-0126, Worked illustration**: "Consider five registry entries: `approved`: Unary · `succession`: Binary · `citation`: Multi · `touched`: Multi · `retract`: Binary"
**Problem**: `touched` (Multi) is declared in the five-entry list and then never appears again — no emit, no conformance check, no failing variant exercises it. The Unary case uses `approved`, Binary uses `succession`, Multi uses `citation`, and the born-nullified scenario uses `retract` and `citation`. In a section whose entire purpose is concrete exercise, a reader scanning the inventory hunts for `touched`'s use-site and finds none. This is precisely the use-site/inventory residue the anti-bloat classifier targets: a declared item the reader must skip past.
**Required**: Either drop `touched` from the list, or actually exercise it. If the intent is to show two distinct Multi coverage-classes coexisting under C0's key-uniqueness (`citation` and `touched`), then emit under `touched` and contrast it with `citation` so the entry earns its place; otherwise remove it.

## OUT_OF_SCOPE

### Topic 1: Operational disposition of born-nullified emits and Binary region-retraction
The note correctly *specifies* two consequences of refining the emit without re-importing ASN-0086's unit-depth discipline: a gate-clearing emit can be born nullified (wp Case, Born-nullified illustration), and a single non-unit Binary G-span withdraws a whole region at once (Single-source), so R-Scope's single-tuple scope holds only when an app self-routes through the unit-depth wrapper. What the note leaves open is the *policy* question — should the substrate warn against, reject, or otherwise protect an app emitting into a pre-retracted range, and should region-retraction be disciplined back toward single-tuple scope, or is the wrapper-vs-range choice simply the app's to make?
**Why out of scope**: This is behavioral/operational semantics layered on top of the static gate, squarely in the territory the note defers (Open questions 1–3). The framework's task here is to define the gate, the registry, and their invariants — which it does, and which correctly *determine* the born-nullified behavior via ASN-0086's existing `nullified`/`A_K` machinery. Disposition policy belongs to the successor note, not to a revision of this one.

VERDICT: REVISE
