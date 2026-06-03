# Review of ASN-0071

I worked through the load-bearing proofs — PC (prefix confinement), PC-RANGE (cross-depth capture), F-DEEP, F-SELF, the `iaddrs ⊆ dom(C)` subset claim, finiteness, and currency — and checked the worked scenario against the postconditions.

## Verification notes

**PC derivation (The query).** The componentwise fact correctly localizes disagreement via T1 case (i) at the least disagreeing position, using TumblerAdd prefix-copy below the action point to align `u` and `u ⊕ ℓ` on positions `< #u`. The totality clause (`#t ≥ #u`) is properly handled by the proper-prefix / first-disagreement split. No gap.

**PC-RANGE.** The three-way `#v` split (`= #u`, `> #u`, `< #u`) is not over-general: since `#u` is a free vspec parameter and S8-depth pins every content position at `m_C`, each sub-case is realized by an appropriate anchor depth (`#u = m_C`, `#u < m_C`, `#u > m_C`). Boundary handling at component `#u` (exclusive reach, proper-prefix promotion to T1 case (ii)) is correct in both depth sub-cases.

**F-DEEP / empty-source split.** Correctly separated: `V_{s_C}(d_s) = ∅` (empty intersection) versus `#u > m_C` (every content position excluded by the depth guard). The dual worked example (`Q_F`) confirms it concretely.

**Worked scenario.** Boundary coverage is thorough — empty query (F-EMPTY), empty source, deep anchor (F-DEEP), cross-depth full-subtree capture (`Q_E`), single/multi-address, multi-source dedup (`Q_G`), shared I-address at non-adjacent positions, self-inclusion, and a concrete exclusion (`d_C`). Reach computations and `⟦σ⟧ ∩ dom(M)` intersections check out; the infinite-`⟦σ⟧` / finite-intersection distinction is correctly drawn.

**Cross-ASN.** References stay within foundations (0047, 0053, 0058) plus foundation tumbler primitives (T0, T1, T12, TumblerAdd) used by those foundations; no non-foundation ASN is cited by number, and no foundation notation is reinvented (σ.denotation/reach explicitly applied, not restated).

**Anti-bloat scan.** Examined the introduction, the two `Reachability` notes, and the per-step scenario narration for accreted meta-prose. The Nelson quotes motivate PC-RANGE's coarse-coordinate capture; the second Reachability note back-references the first economically ("again," "like Σ"); the per-step P8/K.δ-ID narration is load-bearing for the reachability claim. No paragraph imagines a precondition-excluded case, no axiom-rationale prose, no downstream-consumer inventories in definition slots. Nothing rises to a finding.

## REVISE

None. The proofs show their cases, boundaries are covered, claims carry explicit bases, and the scenario verifies the key postconditions against concrete states.

VERDICT: CONVERGED
