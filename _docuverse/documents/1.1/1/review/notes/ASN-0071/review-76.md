# Review of ASN-0071

I checked the four load-bearing proofs (PC, PC-RANGE, F-DEEP, the `iaddrs ⊆ dom(C)` subset claim) line by line, plus every boundary the operation could hide a gap behind, plus the reachability of the worked state. I could not break any of them.

**PC derivation.** The componentwise fact correctly conditions on existence (`t_p` exists), and totality establishes `#t ≥ #u` before prefix agreement quantifies over `1 ≤ j < #u` — no circularity, since the componentwise fact's proof uses only TumblerAdd prefix-copy, T0, and T1. The `t > u⊕ℓ` horn correctly relies on `t` agreeing with `u⊕ℓ` below `p` (prefix copy holds because `p < #u = actionPoint`). The totality dichotomy (proper prefix vs. first disagreement at `p ≤ #t`) is exhaustive and both horns reach contradictions. Rigorous.

**PC-RANGE.** The depth case split (`#v < #u`, `#v = #u`, `#v > #u`) is exhaustive and well-typed — the `#v ≥ #u` guard is what makes `v_{#u}` referenceable, and the shallow case is excluded from *both* sides (totality on the left, undefined component on the right). The `v = u` boundary is correctly admitted by *equality* while `v = r` is excluded by *exclusivity of reach*, not by an order relation. Link-subspace positions are excluded implicitly but correctly: the `j = 1` conjunct (`#u ≥ 2`) forces `v_1 = s_C`.

**Boundary coverage is complete.** Empty query (F-EMPTY), empty content subspace (`V_{s_C}(d_s) = ∅` → trivially empty), deep anchor (F-DEEP), cross-depth shallow anchor (full subtree capture), and multi-source dedup are each specified and each illustrated by a concrete worked computation. Zero-width spans are excluded by `Pos(ℓ)`. The vspec deliberately drops ASN-0058's non-emptiness clause precisely so the empty-source case is in-domain — that case is then handled.

**Worked scenario is reachable.** Each composite (e.g. steps 6–8: K.δ + K.μ⁺ + K.ρ) discharges its intermediate preconditions and the J0/J1★/J1'★ couplings; the transclusion binds (steps 7, 13, 15) introduce no K.α and correctly leave J0 vacuous while J1★ forces the recorded provenance. Step 13's `a₁, a₂, a₁` arrangement satisfies S8★ as three length-1 runs.

**Depth is present, not hand-waved.** Consequences are derived rather than asserted: currency (F-CUR), finiteness (F-FIN, with the elementary-vs-composite count distinction made explicit), partial-overlap (F-PART), self-inclusion (F-SELF), origin separability (F-ORIGIN). F-CONTENT holds from `iaddrs ⊆ dom(C)` alone, independent of L14.

No correctness defect, no missing conjunct, no proof-by-"similarly," no checkmark standing in for a multi-case argument. The anti-bloat sweep found no surviving forward-reference accretion, defensive axiom-rationale, use-site inventories, or duplicated paragraphs — the vspec's "minus three clauses" framing is a legitimate foundation reuse, and the two reachability remarks cover distinct states (Σ and Σ⁺).

## OUT_OF_SCOPE

### Topic 1: Relationship between current result and the historical relation R
**Why out of scope**: The first Open Question. `find` deliberately reads only `E_doc` and `M`; reconciling current containment against permanent `R` (P2) is genuinely new territory, correctly deferred.

### Topic 2: Rejecting vs. silently filtering unresolvable vspec positions
**Why out of scope**: The second Open Question. F-FILT specifies the silent-filter semantics this ASN chose; a rejection regime is an alternative policy for a future ASN, not an error here.

### Topic 3: Invariant connecting results across a contracting transition
**Why out of scope**: The third Open Question. Cross-transition invariants involve K.μ⁻ operation mechanics, which are out of scope for a query-only specification.

VERDICT: CONVERGED
