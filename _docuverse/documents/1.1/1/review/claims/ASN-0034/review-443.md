# Regional Review — ASN-0034/TA2 (cycle 1)

*2026-04-23 05:21*

### TA2 duplicates TumblerSub's carrier-membership postcondition
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: TA2 (WellDefinedSubtraction) — "For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`." Proof performs its own Case 1 / Case 2 split mirroring TumblerSub's proof.
**Issue**: TumblerSub already establishes `a ⊖ w ∈ T` and `#(a ⊖ w) = L` in its formal contract's postconditions, with a proof that walks the same no-divergence / divergence split. TA2 re-proves the weaker subset (dropping Pos and actionPoint) and depends on TumblerSub, so its body repeats reasoning already discharged upstream. The `≥` precondition, the zero-padded case split, the sub-case (i) / sub-case (ii) analysis at the divergence point, and the tail argument all appear in both proofs.

### Depends entries embed use-site inventories rather than naming what is used
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: TumblerSub contract — e.g., "NAT-closure … Required in scope for the consumed contracts of TA-Pos, ActionPoint, Divergence, and ZPD, each of which cites `1 ∈ ℕ`, the additive identity `0 + n = n`, or closure under `+` in its body." Same pattern for NAT-wellorder, NAT-cancel, NAT-discrete.
**Issue**: The Depends slot should say *what this ASN uses from the foundation*. These entries instead catalog where transitively-consumed contracts reach for the axiom. That is essay content defending the dependency's presence rather than naming the clause and its use site in this proof. The reader has to parse through meta-prose to recover the actual dependency.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 160s*
