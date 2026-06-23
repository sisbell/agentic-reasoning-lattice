## Audit

### Dependency chains across claims

**S3 → WF**: S3 invokes WF at (s, r) with the preconditions s, r ∈ T, s < r, and #s = #r. All four are discharged:
- s ∈ T: min of two span starts. ✓
- r ∈ T: each reach placed in T by TumblerAdd; r is whichever is larger. ✓
- s < r: TA-strict at α gives reach(α) > start(α) = s; max(reach(α), reach(β)) ≥ reach(α) chains via T1 mixed transitivity. ✓
- #s = #r: level_compat(start(α), start(β)) gives #start(α) = #start(β); S6 gives #reach(σ) = #start(σ) for each well-formed level-uniform σ; both reaches share that common length; r is one of them. ✓

**S4 → WF (twice)**: λ at (s, p): s ∈ T, p ∈ T, s < p (interiority), #s = #p (level_compat precondition). ρ at (p, reach(σ)): p ∈ T, reach(σ) ∈ T by TumblerAdd, p < reach(σ) (interiority), #p = #reach(σ) since S6 gives #reach(σ) = #s and level_compat gives #p = #s. Both WF invocations are fully discharged. ✓

**WR → D2 at (s, reach(σ), ℓ)**: The five non-trivial preconditions: (1) s < reach(σ) from TA-strict; (2) Pos(ℓ) and actionPoint(ℓ) ≤ #s from T12; (3) s ⊕ ℓ = reach(σ) by definition of reach; (4) #s ≤ #reach(σ), both equal #s (from TA0's result-length identity); (5) divergence(s, reach(σ)) ≤ #s — established via T1 case analysis: #s = #reach(σ) eliminates case (ii) (it would force #s+1 ≤ #s, refuted by NAT-addcompat's successor inequality + NAT-order irreflexivity), leaving case (i) with k ≤ #s, and Divergence's uniqueness clause identifies k = divergence(s, reach(σ)). All five discharged. ✓

**WF → D1 at (s, r)**: The critical fifth precondition divergence(s, r) ≤ #s is established by the same case-analysis pattern: #s = #r eliminates T1 case (ii); case (i) gives k ≤ #s; Divergence uniqueness identifies the index. D1's other four preconditions are immediate from the hypotheses. ✓

**S4a → S3, then → WR**: S3 is applied to (λ, ρ) with start(λ) = s, start(ρ) = p. Level_compat(s, p) is a precondition of S4a, so S3's level_compat precondition is met. Adjacency reach(λ) = p = start(ρ) holds by S4's postcondition (c). S3 produces γ = (s, reach(σ) ⊖ s). WR then gives reach(σ) ⊖ s = ℓ (σ is level-uniform, which is S4a's precondition), so γ = (s, ℓ) = σ. ✓

### Union characterization in S3

Forward direction: every t ∈ ⟦α⟧ satisfies s ≤ t (since s = start(α)) and t < r (since reach(α) ≤ r = max(reach(α), reach(β))). Every t ∈ ⟦β⟧ satisfies s ≤ t (since start(β) ≥ start(α) = s, WLOG) and t < r (since reach(β) ≤ r). ✓

Backward direction, Case 2: t ≥ reach(α) and t < r forces r > reach(α), so r = reach(β) by definition of max. Then t < reach(β). The reduced overlap/adjacency condition reach(α) ≥ start(β) gives t ≥ start(β), so t ∈ ⟦β⟧. The case where reach(α) = reach(β) = r makes Case 2 vacuous (t ≥ r contradicts t < r). ✓

### WLOG validity in S3

The claim is symmetric in α and β: level_compat is symmetric, overlap-or-adjacent is symmetric, ⟦α⟧ ∪ ⟦β⟧ is symmetric, and min/max are symmetric. WLOG start(α) ≤ start(β) is valid. Under this assumption, the adjacency disjunct reach(β) = start(α) is vacuous: it would give reach(β) = start(α) ≤ start(β) < reach(β) (by TA-strict at β), collapsing via T1 mixed transitivity to reach(β) < reach(β), refuted by T1 irreflexivity. ✓

### Partition proof in S4

Part (a): every t with s ≤ t < reach(σ) satisfies t < p or t ≥ p by T1 trichotomy; the two sets partition the range. Part (b): a t in the intersection would satisfy t < p and p ≤ t, giving p < p via T1 transitivity, contradicting irreflexivity. Part (c): WF's postcondition at (s, p) directly yields reach(λ) = s ⊕ (p ⊖ s) = p; start(ρ) = p by construction. ✓

### S6 as a definitional anchor

S6 establishes that for a well-formed level-uniform span all of start, width, and reach share a common tumbler length. The chain #reach(σ) = #(s ⊕ ℓ) = #ℓ = #s is earned from TumblerAdd's result-length postcondition once its preconditions (Pos(ℓ) and actionPoint(ℓ) ≤ #s from T12) are in hand. Every downstream use — S3's WF call needing #s = #r, S4's WF call for ρ needing #p = #reach(σ), WR's D2 call needing #s = #reach(σ), WF's length bound on actionPoint — resolves to this chain. ✓

### Examples

S3 example: reach([1,3]) = [1,7], reach([1,5]) = [1,11], s = [1,3], r = [1,11], width = [1,11] ⊖ [1,3] = [0,8] (divergence at position 2, 11−3=8), reach(γ) = [1,3] ⊕ [0,8] = [1,11] = r. ✓

S4 example: σ with 7-component start and width [0,0,0,0,0,0,8], reach [1,0,1,0,1,0,13]; split at p=[1,0,1,0,1,0,9]; d = [0,0,0,0,0,0,4], d' = [0,0,0,0,0,0,4]; reach(λ) = p, reach(ρ) = reach(σ); partition and disjointness verified at position 7 component. ✓

VERDICT: CONVERGED