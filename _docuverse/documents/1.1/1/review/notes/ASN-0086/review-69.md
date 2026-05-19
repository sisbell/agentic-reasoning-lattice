# Review of ASN-0086

## REVISE

### Issue 1: R0 proof — "IH for L1" wording is loose
**ASN-0086, R0 proof, subsequent-emission branch**: "By ChainUniformLength and ChainUniformZeroCount, the result has the same length and zero count as `ℓ_prev` (which by the IH for L1 carries zeros = 3)"
**Problem**: R0 is not proved by induction — it is a per-step argument about an emission at any reachable conforming state Σ. There is no "IH for L1" structurally present. `ℓ_prev ∈ dom(Σ.L)` carries zeros = 3 by L1 directly as a substrate-level invariant at Σ.
**Required**: Replace "IH for L1" with a direct citation to L1 as a state invariant at the reachable Σ. Audit the proof for other inductive-hypothesis terminology that should be replaced with direct invariant references.

### Issue 2: R7a proof — substrate-conformance discharge is too informal
**ASN-0086, R7a proof, after enumerating directly-cited invariants**: "the remainder transfers by input-substitution against Frame conditions, and the abbreviation 'substrate-conforming' stands in for the full conjunction."
**Problem**: The substrate-conforming layer Definition lists roughly 30 invariants (the full L-, S-, M-, C-catalogs). R7a's proof cites perhaps a third directly. For a categorical closure lemma over `↝`, "the remainder transfers" is too loose — a future consumer cannot reconstruct which invariant is needed where.
**Required**: Enumerate per replay step type (K.σ-step, K.λ-step) which substrate invariants are discharged and how (Frame condition, structural property of the address, reachability inheritance). At minimum, group the catalog and indicate which group transfers by which mechanism.

### Issue 3: Notation `L_K^Σ` conflates K with its coverage class [K]
**ASN-0086, Definition of TypedRelation**: "`L_K^Σ = {(a, F, G) : ... coverage(Σ.L(a).e₃) = coverage(K)}`"
**Problem**: The membership criterion at slot 3 is coverage-equality, so `L_K^Σ` depends only on `[K]` under `~`, not on `K`. Two `K, K' ∈ T_admissible` with `K ~ K'` give `L_K^Σ = L_{K'}^Σ` as sets. The notation `L_K` reads as parameterized by `K`, masking that the relevant index is `[K]`.
**Required**: Either rename to `L_{[K]}^Σ` (and adjust `Emit_K`, `Observe_K`, `A_K^Σ` accordingly) or add a notation note immediately after the Definition explicitly stating that the subscript is read modulo `~`. This is the TypeEquivalence-by-coverage gap.

### Issue 4: R5's generalization paragraph should be a separate corollary
**ASN-0086, R5 proof, "Generalization to arbitrary endset contents" paragraph**: "any endset content `(F, G, K)` satisfying L3 admits the same R0 emission argument..."
**Problem**: This establishes a substantive claim — R0's emission argument is endset-content-uniform — but ships it as an in-proof remark for a claim labelled specifically `TupleSelfTargeting`. R5's stated content is about self-targeting; readers consulting R5 do not necessarily see that R0's verification has been shown content-uniform.
**Required**: Either expand R5's claim statement to make the generalization explicit, or extract a separate named corollary (e.g., R5-Cor: EmitContentUniformity) that downstream claims can cite without unpacking R5's proof.

### Issue 5: R0a-Cor2 — Route A's "T10a.4 ⟹ T4-validity" citation should route through ASN-0093's named lemma
**ASN-0086, R0a-Cor2 proof, Route A**: "By T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every chain element is T4-valid, so by TA5-SigValid..."
**Problem**: ASN-0093 packages this step as the named lemma `ChainElementT4Validity` (with `A_L(d)` discharged as a T10a-discipline-satisfying chain via SubAllocatorAxiom.ChainDiscipline). Citing T10a.4 directly bypasses ASN-0093's stated abstraction layer and forces the reader to redo the chain-discipline correspondence inline.
**Required**: Cite ChainElementT4Validity (ASN-0093) directly, with T10a.4 named once as ChainElementT4Validity's own underlying ASN-0034 hook if attribution is wanted.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets
The ASN explicitly restricts `L_K^Σ` to arity-3 (standard-triple) links and flags multi-arity (`|Σ.L(a)| > 3`) as an Open Question. Extending `A_K^Σ` machinery to `A_K^{(n),Σ}` is future-ASN territory, not a deficiency in this one.

### Topic 2: Concurrency / atomicity model for Emit vs Observe
Properly flagged as Open Question. Atomic-emission semantics under concurrent observation is an operational/runtime concern beyond substrate invariants.

### Topic 3: Cardinality bounds on `nullified(Σ)`
Properly flagged as Open Question. Whether unbounded retraction is permitted or a structural ratio against `dom(Σ.L)` must hold is a future design choice, not a missing invariant here.

### Topic 4: Cross-layer coordination on type-address collisions
Properly flagged as Open Question. L9 admits dynamic type introduction by higher layers; collision resolution is a layer-coordination concern, not a substrate guarantee.

### Topic 5: Whether unit-depth retraction discipline should be a substrate-level constraint
Properly flagged as Open Question. Current design — layer convention rather than K.λ shape constraint — is internally consistent. WP Case 2 makes the consequence of admitting crafted-span retractions explicit, so the design tradeoff is documented.

### Topic 6: Whether L1b's `#E ≥ 2` should be tightened to `#E = 2` at the substrate
Properly flagged as Open Question. R0a-Cor2 establishes `#E = 2` strictly under K.λ; whether to push this back into L1b's ASN-0043 statement is upstream-ASN scope.

VERDICT: REVISE
