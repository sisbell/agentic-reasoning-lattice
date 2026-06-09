# Review of ASN-0118

I worked through the operation's proof obligations against the Dijkstra standard: every case, every invariant conjunct, every boundary. This ASN is unusually self-defending — it anticipates the underdetermination traps (CP3c, CP6) that most arrangement specs hand-wave — so I focused on the places where "place by reference" could quietly skip work.

## Verification performed

**Resolution integrity (CP0).** The bridge from `expand(resolve(R))` to the per-position reading is *derived*, not asserted — including the interior addresses `aⱼ+k`, which are grounded in S8 maximal-run lockstep (`M(d_s)(vⱼ+k)=aⱼ+k`) rather than left as bare arithmetic on `aⱼ`. CP0(a) routes through S3★ over the bound subset, correctly avoiding ASN-0058 C1's full-binding precondition that COPY discards. Run ordering (C1b) → ascending enumeration is sound because correspondence runs are ordinal-contiguous intervals, hence linearly ordered.

**Composite decomposition (CP8).** Checked both cases. Append/empty = single K.μ⁺; displacing = K.μ⁻(`n'_{s_C}=j<N`, `n'_{s_L}=n_{s_L}`) + K.μ⁺. The strict-contraction requirement is met by the text subspace; link-subspace full retention is correctly justified as admissible non-strict. The intermediate `Σ₁` is shown to satisfy per-state invariants, and couplings (J0 vacuous via CP1, J1★/J1'★ range-based initial-to-final) are discharged across all three provenance branches (range-new+unrecorded → K.ρ; range-new+recorded → P2; not-range-new → P4★+P2). P4★'s use is correctly licensed by the composite-boundary standing precondition.

**Tiling without gaps.** The hardest invariant to maintain — derived explicitly from ordinal arithmetic (left `[min,p)`, placement `[p,p+W)`, shifted `[p+W,max+W]`), with disjointness from TS1/TS4. Not a checkmark.

**Boundary cases.** Empty destination (D-MIN/D-SEQ *established* not preserved, `m` fixed by `#p`), append (CP3a vacuous), displacing (`j=0` D-MIN vacuity noted), self-transclusion (CP9, pre-state read fixes `cᵢ`), partial/empty binding (`act` restriction, `W≥1` excludes no-op). Gap-fill placement positions are correctly handled by OrdShiftHom(b)+ValidInsertionPosition where I3-VP/I3-VD do not reach.

**Consequences derived, not stated.** CP5 origin invariance (S7d), CP7b link survival via LP12 with a genuine non-trivial wp, CP11 origin-multiset via M16, CP4 multiplicity. Worked two-source example checks CP1/CP2/CP3a/CP8/CP11 numerically including the already-recorded provenance branch.

All inter-ASN citations are to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058, 0082, 0093, 0098); new notation (`act`, `expand`) is an explicit abbreviation of foundation constructs, not reinvention.

I noted one acknowledged asymmetry: CP8 is membership-only and delegates `Σ'.R`-determinism to the composite (J1'★) rather than a closure frame analogous to CP3c. This is not a defect — unlike the CP3c double-binding case (which would violate S2), a loosely-specified R admits only invariant-*satisfying* states (P2/P4★/P7 all hold), so no invariant-discharge obligation is breached. The ASN explicitly scopes its "dischargeable from postconditions alone" standard to S2/CL invariants and openly states CP8's production comes from the composite.

## OUT_OF_SCOPE

### Topic 1: Width relationship under partial binding (ASN-0058 C2)
The ASN correctly identifies that C2's width-preservation does not survive partial binding and that COPY never uses it (its arithmetic is self-consistent on the actual `W`). Listed as an open question — future territory, not an error here.

### Topic 2: Correspondence relation, link-subspace transclusion, differing-depth assembly, deletion-after-COPY discoverability
Enumerated in the Open Questions and correctly deferred; none threatens a stated invariant of this ASN.

VERDICT: CONVERGED
