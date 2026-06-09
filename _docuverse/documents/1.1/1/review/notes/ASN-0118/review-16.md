# Review of ASN-0118

I read this as an independent pass, checking every proof, edge case, and invariant conjunct against the foundation contracts.

## REVISE

(none)

The ASN is unusually rigorous, and the places where specifications normally fail are all closed:

- **Underdetermination of the post-state is explicitly repaired.** CP3c (text-domain closure) and the CP6 domain-equality conjunct are correctly identified as load-bearing: without them, CP2/CP3a/CP3b/CP6 leave `Σ'.M(d)` underdetermined, admitting a double-binding at `p` (violating S2) or a spurious link-subspace position. Both are pinned to the exhibited K.μ⁻/K.μ⁺ composite. S2 is dischargeable from the postconditions alone.
- **The displacing case is handled correctly.** The author recognizes a single K.μ⁺ cannot vacate the displaced positions and gives the contraction-then-extension decomposition, with per-subspace retention (`n'_{s_C}=j<N` strict, `n'_{s_L}=n_{s_L}` full) admissible, intermediate-state invariants checked, and gap-fill positions handled by a separate OrdShiftHom argument where I3-VP/I3-VD do not reach.
- **Boundary cases covered.** Empty destination (D-MIN/D-SEQ *established* not preserved), `j=0` full text contraction, append (`j=N`), empty resolution `W=0` excluded by `W≥1`, partial binding resolved by `act` restriction, self-transclusion (CP9, pre-state read).
- **The resolution bridge is derived, not asserted.** The coincidence of `expand(resolve(R))` with the per-position ascending reading is grounded in S8 maximal-run lockstep for interior addresses, and C1a is invoked via content-residence (single-subspace) rather than C0a, correctly routing around the dropped full-binding hypothesis.
- **Provenance is read off the composite.** J0 vacuous (no K.α), and the three-way CP8 branch (range-new+unrecorded → fresh K.ρ; range-new+recorded → P2; not-range-new → P4★+P2) is sound; the P4★ use is correctly licensed by the composite-boundary standing precondition.
- **Depth present.** Non-trivial wp for link discoverability, concrete two-source worked example verifying CP1/CP2/CP3a/CP8/CP11 numerically (parses check out: `origin(a₁)=1.0.1.0.7=d_A`, `Σ'.M(d)` as claimed), and derived consequences (CP4 multiplicity arithmetic, CP5 origin invariance, CP11 origin multiset) explored.

I verified the example arithmetic (`[1,1]⊕[0,2]=[1,3]`, `act` sets, `resolve=⟨a₁,a₂,b₁⟩`, displacement to `[1,5]`) and the run-concatenation/ascending-enumeration coincidence; all hold.

## OUT_OF_SCOPE

### Topic 1: Width-preservation shortfall under partial binding
The loss of ASN-0058's C2 when `W` falls below the named extent is correctly deferred to an open question; COPY never uses C2, so this is future territory, not a defect here.

### Topic 2: Later removal of transcluded positions and link re-orphaning
The conditions under which an inherited link becomes undiscoverable after the destination contracts the placed positions belong to DELETE/contraction reasoning, not COPY.

VERDICT: CONVERGED
