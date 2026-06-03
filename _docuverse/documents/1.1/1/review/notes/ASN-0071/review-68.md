# Review of ASN-0071

## REVISE

### Issue 1: Redundant well-typedness preview ahead of the F-DEEP case split
**ASN-0071, *Resolution* (end of "Which positions resolve")**: "PC-RANGE's range condition at component `#u` couples to the arrangement's content-subspace depth `m_C` (S8-depth, which fixes `#v = m_C` for every content-subspace `v ∈ dom(M(d_s))`): the comparison `u_{#u} ≤ v_{#u} < r_{#u}` is well-typed exactly when `#u ≤ m_C`."

**Problem**: The very next paragraph ("The depth `m_C` (S8-depth) is well-defined only when `V_{s_C}(d_s) ≠ ∅`, so we split…") rigorously establishes the same `#u`-vs-`m_C` relationship by case split — the `#u > m_C` branch produces F-DEEP and the `V_{s_C}(d_s) = ∅` branch the trivial empty case. The quoted sentence is a preview of a conclusion the following paragraph derives properly, and it conflates "well-typed" (per-`v`, needs `#v ≥ #u`) with "satisfiable for some content position" (needs `#u ≤ m_C` because all content `v` have `#v = m_C`). It is the "two paragraphs say the same thing / forward-deferral to a downstream derivation" pattern.

**Required**: Delete the preview sentence; let the `V_{s_C}(d_s) = ∅` / `≠ ∅` split carry the `#u`-vs-`m_C` reasoning, which it already does completely.

### Issue 2: F-COMP and F-SOUND are the two directions of a definitional biconditional
**ASN-0071, *The operation***: "This biconditional is its own completeness and soundness statement: its (⟸) direction … is recorded as **F-COMP**, and its (⟹) direction … as **F-SOUND**." (Basis column: "direct from F-find (⟸ direction of the defining iff)" / "(⟹ direction…).")

**Problem**: `find` is *defined* by the comprehension `{ d ∈ E_doc : ran(M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`. Reading that definition forward and backward is not a derived property — both labels are tautological unfoldings of the definition, as the prose itself concedes. Promoting each direction to a separate claim label inflates the claim table without advancing any reasoning.

**Required**: Collapse to a single note that the definition is extensional (hence sound-and-complete by construction), or drop the two labels. If they are retained for downstream citation, say so explicitly rather than presenting them as established results.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state `find` and the historical relation `R`
**Why out of scope**: The first Open Question (current result vs. permanent provenance `R`) is correctly deferred. `find` reads only `E_doc` and `M`; reconciling current containment with `R` is new territory, not a defect here.

### Topic 2: Rejecting vs. silently filtering unresolvable vspec positions (F-FILT policy)
**Why out of scope**: The second Open Question asks when the system *must reject* rather than filter. F-FILT specifies the present (filtering) semantics correctly; a rejection regime is a future operation contract.

Note on correctness: the core machinery is sound. PC's three-part derivation (componentwise fact → totality → prefix agreement) is non-circular and correctly justifies re-deriving rather than citing ASN-0058 C0a, since vspecs relax C0a's `#ℓ = #u = m_C` coupling. PC-RANGE's characterization is a correct iff across all three depth regimes, the action-point `≥ 2` precondition correctly prevents subspace leakage, and the worked reach computations (`σ_A … σ_F`) and finiteness argument all check out.

VERDICT: REVISE
