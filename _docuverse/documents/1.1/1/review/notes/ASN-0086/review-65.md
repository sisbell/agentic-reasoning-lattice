# Review of ASN-0086

## REVISE

### Issue 1: WP Case 2 incomplete for K ~ R with self-targeting G

**ASN-0086, Weakest-Precondition Analysis, Case 2**: 

`wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ NoCraftedSpanReachesD(Σ, d)`

`NoCraftedSpanReachesD` is explicitly defined as a universal over **L_R^Σ** (pre-state retractions only): "no *pre-existing* retraction's to-span coverage contains the address Emit_K is about to deposit under d." For K ~ R, the fresh emission contributes to L_R^{Σ'} = L_R^Σ ∪ {(a, F, G)}, and the *fresh* tuple's own G could include a in its coverage (a self-targeting R-typed emission). In that case a ∈ nullified(Σ') via the just-emitted tuple itself, and (a, F, G) ∉ A_K^{Σ'}, but the stated wp gives no witness of this.

**Problem**: The proof distinguishes regime (i) (unit-depth discipline) and regime (ii) (crafted-span retractions in pre-state), but does not name the third regime: K ~ R with self-targeting G at the emission step itself. The relational-layer discipline (Nullify-as-sole-R-producer) prevents this, but the wp is presented as a substrate-level analysis applicable independently of layer commitments.

**Required**: Either include the additional conjunct `K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G)` in the wp formula, or restrict Case 2's stated scope to K ≁ R explicitly and treat K ~ R separately. The Worked Sketch's Step 1 implicitly relies on this — the fresh emitter b₁ is shown not to be in coverage(G) because b₁ ≠ a₁ and they're prefix-incomparable siblings — but the wp formalization should make the underlying conjunct explicit.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b to #E = 2 at the substrate level
R0a-Cor2 establishes #E = 2 strictly within the ASN-0093 substrate; whether L1b in ASN-0043 should be tightened from #E ≥ 2 is appropriately flagged in the Open Questions list, not the present ASN's concern.

### Topic 2: Higher-arity typed relations
Multi-arity links (|Σ.L(a)| > 3) and their projection into typed relations is acknowledged as out-of-scope and listed as an Open Question. The arity-3 restriction is honestly stated.

### Topic 3: Elevating the unit-depth retraction discipline to substrate
The Implementation Notes carefully partition substrate-level vs. layer-level commitments; whether the discipline should become a substrate-level K-operation constraint is correctly deferred.

### Topic 4: Concurrent emit/observe semantics, Observe ordering, type catalog dynamics
All appropriate Open Questions.

VERDICT: REVISE
