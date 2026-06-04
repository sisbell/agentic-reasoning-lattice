# Review of ASN-0101

I worked through the operation specification (D0), the gap-closure proof (D1), the containment-reduction argument, all seven preservation claims (D2–D8), the projection characterisation (D9), the ValidComposite★/LP-family extension (D10), and the weakest-precondition calculations (D11), checking each against the foundation contracts and the boundary-case enumeration.

## Findings

The proofs hold up under scrutiny. Spot-checks of the load-bearing arguments:

- **D1 / gap closure.** The shift-inverse `σ_d([S,1,…,1,k]) = [S,1,…,1,k−n]` is correctly grounded in TS2 (injectivity) and TS1 (order preservation) at arbitrary depth `m_S ≥ 2`, and `Λ ∪ Q = {[S,1,…,1,k] : 1 ≤ k ≤ n_S−n}` is contiguous in both the `Π = ∅` and `Π ≠ ∅` sub-cases (the precondition forces `n_S − n = p − 1` exactly when `Π = ∅`).
- **Containment reduction.** The least-divergence-index argument correctly rules out both `v_{j₀}=0` (gives `v < s`) and `v_{j₀} ≥ 2` (gives `v > r`), and the `m_S = 2` vacuous base is handled separately. Uses only T1 + T0, not S8a — correctly noted since `v` is an arbitrary candidate.
- **D8 coverage.** The Group (i)/(ii)/(iii) partition covers every per-state invariant of ExtendedReachableStateInvariants and the transition invariant P3. The non-trivial cases (S3★, S8★(c), CL-OWN, CL-UNIQ under `Q ∩ X ≠ ∅` re-mapping) are discharged by the source-correspondence argument with disjoint-image injectivity, and S8★(c) correctly routes through M12 only on the content subspace.
- **D10 vacuity vs. composite-level coupling.** The distinction between one-step vacuity of J0/J1★/J1'★ and the non-automatic composite-level obligation is correctly drawn, with a concrete K.α→K.μ⁺→DEL counterexample showing endpoint J0 failure.
- **D11 wps.** The determinism/partiality treatment is correct (`wp(S,¬Q) ≡ enabled ∧ ¬wp(S,Q)` for partial deterministic `S`), and the cardinality identity collapses correctly via `Λ ∩ Π = ∅` and the `V_S = Λ ⊎ X ⊎ Π` partition.

Boundary enumeration (empty post-state, deletion-at-start with the lone non-vacuous D-MIN★ witness, deletion-at-end, singleton/non-singleton interior) is complete; `n = n_S` correctly forces `p = 1` via the containment precondition. The three worked examples exercise content-subspace depth-3, link-subspace depth-2 (CL-OWN/CL-UNIQ), and cross-document transclusion (D5/D9 bullet 1) respectively.

I did not re-raise the K.σ vocabulary-list findings; the body list at "The operation" already includes K.σ and is consistent with D10.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction / reversibility mechanism
The Open Questions defer reversibility, version-based reconstruction, and DELETE-then-INSERT recovery to a versioning mechanism. This is correctly framed as outside DEL's scope — DEL supplies the non-destruction substrate (D2, D5) but not the versioning mechanism, and the ASN says so explicitly.

### Topic 2: Orphaned-I-address enumeration and auxiliary-index maintenance
The "Boundaries" section correctly classifies stale indices, tree-height retention, and orphan enumeration as implementation concerns the abstract specification does not adopt. No abstract claim drifts into these.

VERDICT: CONVERGED
