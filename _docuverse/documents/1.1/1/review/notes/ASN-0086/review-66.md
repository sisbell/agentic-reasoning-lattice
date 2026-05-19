# Review of ASN-0086

## REVISE

### Issue 1: R6c-Corollary's induction hypothesis is too weak to apply R6c's induction step

**ASN-0086, R6c-Corollary proof, induction step**: "assume `(a, F, G) ∉ A_K^{Σ_k}` at chain position `Σ_k`, and consider the `↦`-step `Σ_k ↦ Σ_{k+1}`. Split on which type of `↦`-step is taken: (i) if `Σ_k → Σ_{k+1}` is a `→`-step (one of classes (i)/(ii)/(iii)), the inductive step is exactly R6c's induction step at chain position `k`, delivering `(a, F, G) ∉ A_K^{Σ_{k+1}}`"

**Problem**: R6c's induction step preserves the *antecedent* (`(a, F, G) ∈ L_K^{Σ_k}` AND `a ∈ nullified(Σ_k)`), not the conclusion (`(a, F, G) ∉ A_K^{Σ_k}`). From the corollary's stated IH `∉ A_K^{Σ_k}` alone, one cannot directly invoke R6a (which consumes `a ∈ nullified(Σ_k)`) and R3 (which consumes `(a, F, G) ∈ L_K^{Σ_k}`). The argument is correct in spirit — the antecedent IS preserved across both `→`-steps (R6a + R3) and arrangement-modifying steps (L12 + L12a holding Σ.L invariant) — but the IH formulation as written doesn't carry what R6c's preservation argument requires.

**Required**: Strengthen the IH to either (a) include the antecedent: "Assume `(a, F, G) ∈ L_K^{Σ_k} ∧ a ∈ nullified(Σ_k)` at Σ_k", then verify preservation across each ↦-step type and derive `∉ A_K^{Σ_{k+1}}` from Definition of A_K; or (b) restructure: observe that arrangement-modifying steps make `A_K^Σ`, `L_K^Σ`, `L_R^Σ`, and `nullified(Σ)` pointwise constant (since all depend only on Σ.L, which is invariant by L12 + L12a), so any ↦*-chain reduces to a →*-chain with possibly-intervening Σ.L-fixed steps that don't affect membership, and the corollary lifts from R6c directly.

### Issue 2: R0's "(IH)" labels without an explicit outer induction

**ASN-0086, R0 proof, L-invariant preservation subsection**: Multiple "(IH)" annotations — e.g., "L14 at Σ' requires `dom(Σ'.L) ∩ dom(Σ'.C)|_{s_C} = ∅`. Splitting on the K.λ Frame: (i) `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`, which is L14 at Σ (IH)..." and "L11a (LinkUniqueness, ASN-0043) at Σ' transfers from L11a at Σ (IH) together with K.λ's freshness postcondition...".

**Problem**: R0 is an existential claim about extending an arbitrary reachable Σ to Σ' via one K.λ-step, not an induction. There's no chain length being inducted on within R0. The "(IH)" labels suggest an outer induction on reachability from Σ_init, but this isn't explicitly set up. The intended meaning — "by L14 at Σ, which holds because Σ is reachable from Σ_init and the L-invariants are substrate-level invariants over reachable states" — is correct, but the labeling is misleading.

**Required**: Either explicitly frame R0 as the induction step of an outer "all reachable states satisfy L-invariants" theorem (so "(IH)" has a referent), or replace each "(IH)" with explicit citation: "(by L14 at Σ, holding because Σ is reachable from Σ_init under the substrate's invariant preservation chain)". The argument's correctness is unaffected; presentation needs clarification.

## OUT_OF_SCOPE

### Topic 1: Concurrent operation semantics
Whether Emit must be atomic with respect to concurrent Observe — already flagged as an open question. Cannot be addressed without first specifying the substrate's concurrency model.

### Topic 2: Higher-arity links (|Σ.L(a)| > 3)
The relational vocabulary's extension to multi-arity links — already flagged as an open question. The standard-triple scope here is sufficient for establishing the active/audit distinction.

### Topic 3: Multi-step retraction chain policies
Conditions under which `Nullify(b)` for `b ∈ L_R` is operationally meaningful — already flagged. The single-depth R6b semantics is well-defined; policy choices about second-order retraction belong in a higher layer.

### Topic 4: Type catalog coordination across layers
How higher layers extend `T_cat` dynamically without coordination — already flagged. Fundamentally a layer-level naming convention question.

### Topic 5: Tightening L1b to #E = 2
R0a-Cor2 establishes #E = 2 unconditionally under ASN-0093's K.λ contract, but L1b in ASN-0043 admits #E ≥ 2. Whether to tighten L1b at the source — already flagged as an open question. This belongs in a revision of ASN-0043, not in ASN-0086.

VERDICT: REVISE
