# Channel Assignment — ASN-0040 review-30

**Date:** 2026-05-11 12:01

```
## Issue 1: B0a's "Equivalently" formulation has ambiguous quantifier scope
Reason: Purely notational fix — rewriting the existential's scope using the ASN's own quantifier conventions. No design intent or implementation evidence needed.
```

```
## Issue 2: Type invariant Σ.B ⊆ T justified informally relative to other invariants
Reason: Proof restructuring using material already present (B₀ conf., B0a, TA5(c), TA5(d)). The induction pattern mirrors B_fin, B10, B1 — all internal.
```

```
## Issue 3: wp analysis is incomplete relative to the invariants the ASN must preserve
Reason: Adding wp(baptize(p, d), B10) follows the same decomposition as the existing wp derivations, citing B10, B6, B0a, TA5a — all defined in this ASN.
```

```
## Issue 4: B9 quantifier conflates registry and state
Reason: Formal alignment with the framework defined in *State Space and Transitions*; the proof's substance is unchanged, only the quantifier ranges over 𝒮 instead of registry sets.
```

```
## Issue 5: Bridge1's witness uniqueness is silently assumed in downstream usage
Reason: Uniqueness follows from B7 (namespace disjointness), which is established in this ASN. The one-line proof — any two B6-valid pairs sharing a stream element coincide — is fully internal.
```
