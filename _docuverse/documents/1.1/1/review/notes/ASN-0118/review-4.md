# Review of ASN-0118

I checked the resolution/placement decomposition, the composite-validity argument for provenance, the displacement arithmetic, the link-survival wp, and the worked example. The worked example computes correctly, the displacement tiling (left / placement / shifted-right intervals abut without gap by TS1/TS4) is sound, and the K.μ⁻+K.μ⁺ decomposition of the displacing case is faithful. Two licensing gaps remain in the composite-validity argument for CP8.

## REVISE

### Issue 1: CP8 invokes P4★, a composite-boundary property, but the standing precondition only licenses per-state invariants

**ASN-0118, "The COPY operation" (CP8 derivation)**: "*by P4★ (`Contains_C(Σ) ⊆ R`, ASN-0047) `(cᵢ, d) ∈ Σ.R` already holds, and provenance permanence (P2) carries it into `Σ'`.*"

**Problem**: In ASN-0047, P4★ is collected under *composite-boundary properties* ("Every state at a composite boundary additionally satisfies … P4★ ∧ P4a ∧ P7a"), **not** under the per-state invariants. The standing precondition of this ASN establishes only reachability "under the sequential transition order" and enumerates which **per-state** invariants that licenses (S0/S1, S2/S3★, S7, S8-fin/D-SEQ, L12) — it never establishes that the pre-state `Σ` is a composite boundary. A state reachable under the *atomic* sequential order may be mid-composite, where P4★ can fail. The "already-referenced" branch of CP8 therefore appeals to a property the standing precondition does not supply. (P2 is genuinely per-state and fine; only the P4★ step is unlicensed.)

**Required**: Either (a) add to the standing precondition that COPY's pre-state `Σ` is a composite boundary (so P4★ holds at `Σ`), or (b) justify "`cᵢ` already in `d`'s content-subspace range ⟹ `(cᵢ, d) ∈ Σ.R`" from a per-state invariant rather than from the boundary-only P4★. As written, the inference is the same shape as P4a (TraceWitnessing), which is also boundary-only — so the boundary scoping must be made explicit.

### Issue 2: The ValidComposite argument discharges J1★ and J1'★ but is silent on J0

**ASN-0118, "The COPY operation" (CP8 derivation)**: "*we exhibit COPY as a valid ASN-0047 composite (ValidComposite)*" — the argument then walks the transition preconditions and the couplings J1★ (ExtensionRecordsProvenance) and J1'★ (ProvenanceRequiresExtension).

**Problem**: ASN-0047's ValidComposite requires **all three** couplings initial-to-final: "*J0, J1★, and J1'★ hold for the composite as a whole.*" The ASN never addresses J0 (AllocationPlacementCoupling). To claim COPY is a valid composite, J0 must be discharged. It is vacuous here — COPY allocates no content (CP1: `dom(Σ'.C) = dom(Σ.C)`), so `dom(C') ∖ dom(C) = ∅` and J0's universal quantifier is empty — but a complete composite-validity argument must state this rather than skip the conjunct.

**Required**: Add one sentence discharging J0 vacuously from CP1 (no K.α step, hence no freshly allocated I-address to place).

## OUT_OF_SCOPE

### Topic 1: Partially-bound spans, repeated/overlapping source spans, cross-depth assembly, later removal of transcluded positions, correspondence relation, link-subspace transclusion

**Why out of scope**: These are the ASN's own Open Questions and concern future operations or future invariants (correspondence, DELETE interaction, MAKELINK-style placement). The resolution definition already handles partial binding at the membership level via `act(ρ,Σ) = dom(Σ.M(d_s)) ∩ ⟦σ⟧`; the deeper guarantees are new territory, not errors in this ASN.

VERDICT: REVISE
