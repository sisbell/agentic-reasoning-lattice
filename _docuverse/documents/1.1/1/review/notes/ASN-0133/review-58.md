# Review of ASN-0133

I traced the central proofs (Q0, Q1, Q3, Q5, Q5a, Q6) and the worked composition against the foundations; each holds. The specific load-bearing points I checked:

- **Q0 view rewrite.** The "audit always serves" claim survives its one hard case, `chain`. `chain` is a fixed-view *active* atom, so at a top-level audit term it delivers the unfiltered walk natively (UV does not filter at audit), while any *Boolean* consumption of a chain must route through `elems` to a set — V-PRIM exposes no other `Seq_fin` operation — and `elems(chain_default) = filter(elems(chain_active))`, reconstructible at audit. No constituent's intended value is unreachable at audit. The heterogeneous Σ* example then earns its length: both naive merges genuinely fail, and at *different* conjuncts, so the rebuild is required rather than cosmetic.
- **Q3 idem=⊤ marker.** Firing an audit-slice trigger rules out a dedup hit structurally — a hit-witness would be active, hence in `L_K` (`A_K ⊆ L_K`), hence a witness contradicting the fire; born-nullified deposits still satisfy the audit existential. Sound, and the "decidable syntactic match" claim is justified.
- **Q5 / Q5a.** The per-σ injection real-fire ↦ `(ρ,x,k)` is sound (distinct fires occupy distinct indices); Q5a's domain bound follows from Q-EXT, and the "strictly stronger than H-RF in the open sequence, equivalent in the closed case" asymmetry checks out (the flag-and-retract-before-fire witness for the open direction is admissible).
- **Q6.** The regime split is correct. Regime (i) closes any registry under H-RF+H-FAIR; grow-only + Q5a package reaches-and-holds under weak fairness, with **bounded growth supplying the last argument-appearance index that rescues *holding*** (I checked that a late-appearing trigger-true argument would otherwise break it). Both counterexamples are admissible (environment retracts through the same surface) and genuinely require the extra hypothesis; H-SFAIR's regime form (no argument trigger-true infinitely often) excludes *both* failure σ's, since each has an argument true at infinitely many indices.
- **Worked example.** The Σ₀→Σ₁→Σ₂ trace evaluates `quiescent_R(Σ₂)=⊤` correctly; the acyclic-coupling argument is sound (ρ_P→ρ_R a real but bounded one-way feed; ρ_R→ρ_P type-isolated), and the producer's possible non-reaching under weak fairness is trigger-persistence, not cmt-divergence, so it does not unbound the resolver's grow-only domain.
- **Terminology.** "Real fire = non-no-op = trigger-true" is decoupled from state-change (an idem=⊤ dedup hit is a *real* fire with `Σ'=Σ`); awkward, but explicitly defined in H-FAIR and used consistently — N as last real fire still gives "no state change past N," and zero-step real fires contribute nothing to H-FIN's step count.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Realizing H-ATOM against ASN-0134 A5
A fire is a multi-step batch, which A5 establishes is *not* substrate-atomic ("the all-or-nothing guarantee stops at the single step"). H-ATOM therefore is not a substrate property but a per-fire critical section layered above it — compatible with the substrate (MIC permits reader/writer exclusion), but requiring a discipline the note explicitly defers ("the serialization of multi-step fires that discharges H-ATOM"). Constructing that "MIC for fires" and proving it composes with MIC clauses 6/7 is implementation/future-ASN territory, correctly scoped out.

### Topic 2: Registry well-formedness and contract satisfiability
RG assumes rules exist and that each `Post_ρ` is satisfiable (a fire applies "*some* emission set satisfying `Post_ρ`"); an unsatisfiable or ineffective contract has no defined fire. Registry governance — who may register rules, and the registration-time well-formedness of contracts — is the deferred "activation binding." Future ASN.

VERDICT: CONVERGED
