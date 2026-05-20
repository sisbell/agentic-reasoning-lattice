# Review of ASN-0047

## REVISE

### Issue 1: Incorrect logical relationship for L14a supersession

**ASN-0047, Properties Introduced — Local extensions table, L14a row**: The "Foundation source" column states *"ASN-0043's L14a (NonTranscludability) is implied by S3★ + CL-OWN and not separately stated in the extended state"*.

**Problem**: L14a is logically *contradicted* by S3★ + CL-OWN, not implied. L14a says `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))` — no V-position maps to a link. S3★'s link clause explicitly permits link-subspace V-positions to map into dom(L), and CL-OWN states ownership constraints for exactly such mappings. So S3★ + CL-OWN ⟹ ¬L14a in the extended state where link-subspace V-positions exist.

The body text uses correct wording: *"In the extended state, S3★ + CL-OWN supersede ASN-0043's L14a"* (supersede = replace, accurate). The Statement column also says "Superseded by S3★ + CL-OWN". Only the Foundation source column has the misleading "implied by".

**Required**: Replace "is implied by S3★ + CL-OWN" with "is superseded by S3★ + CL-OWN" or "is replaced by S3★ + CL-OWN, which permit link-subspace V→I mappings (forbidden by L14a) but constrain them via subspace partitioning and ownership."

### Issue 2: K.μ⁻ admissible contraction shape proof glosses depth/inner-1s preservation

**ASN-0047, K.μ⁻ admissible contraction shape paragraph**: The proof reads *"Otherwise D-SEQ★ applied at the post-state gives `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for some `n'_S ≥ 1` directly. ... `V_S(d') ⊆ V_S(d)` (from K.μ⁻'s contraction effect) forces `n'_S ≤ n_S`. ∎"*

**Problem**: The step "⊆ forces n'_S ≤ n_S" implicitly assumes V_S(d') and V_S(d) have the *same canonical shape* — same subspace identifier S, same depth m_S, same inner "1, ..., 1" segment length. D-SEQ★ at Σ' only delivers some D-SEQ★-shaped V_S(d') with some n'_S; the proof must explicitly note that S8-depth at Σ' preserves m_S (restriction inherits pre-state depth), so the canonical shapes match position-by-position and the prefix relationship follows.

**Required**: Insert one sentence between "for some n'_S ≥ 1 directly" and "V_S(d') ⊆ V_S(d) forces n'_S ≤ n_S" stating: "S8-depth at Σ' inherits m_S from the surviving V-positions of Σ, so V_S(d') and V_S(d) share the same canonical D-SEQ★ shape (S, depth, intermediate 1s); set inclusion then reduces to comparison of the trailing-component bound n'_S ≤ n_S."

### Issue 3: Worked example "Step 2: K.α" freshness discharge for cross-document case

**ASN-0047, *Worked example: fork with subsequent insertion*, "Insert new content into d₂" Step K.α**: The freshness derivation reads *"Distinctness from addresses under d₁ (cross-document). The pre-state content store dom(C₂) = dom(C₁) = {a₁, a₂} contains only addresses with origin d₁ (≠ d₂), so the Cross-document disjointness lemma — the consequence of T10a.{2,5} → T10 applied at the namespace level, with d₁'s and d₂'s content sub-allocators occupying disjoint prefix subtrees by S7a — yields a₃ ∉ {a₁, a₂}."*

**Problem**: This freshness step routes through the Cross-document disjointness chain lemma at the document-pair (d₁, d₂). But d₁ = 1.0.1.0.1 and d₂ = 1.0.1.0.1.1 satisfy d₁ ≺ d₂ (d₁ is a *prefix* of d₂ — d₂ is a version of d₁). The Cross-document disjointness lemma's hypothesis requires "distinct same-level entities" but does NOT require prefix-incomparability — its Case A explicitly handles prefix-comparable pairs (`e₁ ≺ e₂`). However, the body text here cites "disjoint prefix subtrees by S7a" which is ambiguous: S7a establishes origin scoping, not subtree disjointness. The lemma's actual operation here is Case A's length-comparison argument at the divergence position, not S7a.

**Required**: Replace "with d₁'s and d₂'s content sub-allocators occupying disjoint prefix subtrees by S7a" with the correct citation: "applied at the document-pair (d₁, d₂) where d₁ ≺ d₂ activates Case A of the lemma — the divergence at position #d₁+1 (d₂[#d₁+1] = 1 ≠ 0 = b_C(d₁)[#d₁+1]) puts every address under b_C(d₁) and every address under b_C(d₂) into prefix-incomparable subtrees."

### Issue 4: Implicit step in P7a proof — content-subspace V-position derivation

**ASN-0047, *Class (b)* matrix — P7a row, and accompanying prose**: The P7a discharge says *"J0 supplies `v ∈ dom(M'(d))` with `M'(d)(v) = a`; S3★ + L14 + S3★-aux force `subspace(v) = s_C`; J1★ then supplies `(a, d) ∈ R'`"*.

**Problem**: The prose later expands this: *"Suppose for contradiction `subspace(v) = s_L`. Then by S3★ at Σ' (link clause), `M'(d)(v) ∈ dom(L')`, i.e., `a ∈ dom(L')`. But `a ∈ dom(C')` (J0's defining membership) and L14 at Σ' gives `dom(C') ∩ dom(L') = ∅`, contradiction."* The contradiction relies on L14 *at Σ'*, but L14 in the extended state is itself derived from L0 + SC-NEQ + T7. At the intermediate state immediately after K.α (before K.μ⁺ adds the V-position), L14 must hold — and K.α's frame `L' = L` plus K.α's `E(a)₁ = s_C` precondition (per ASN-0093) ensure dom(C') ∩ dom(L) = ∅. But the P7a proof references "Σ'" as the composite endpoint, not the intermediate. Between K.α and K.μ⁺ within the composite, the V-position `v` does not yet exist; J0's existential is realised at the composite endpoint Σ' after K.μ⁺ has fired. The argument is correct but the prose elides the temporal positioning.

**Required**: Clarify in the P7a discharge prose that the V-position `v` carrying the new I-address `a` is created by K.μ⁺ at the composite endpoint Σ', not present at the post-K.α intermediate state; the K.μ⁺ amendment then forces `subspace(v) = s_C` directly, with the S3★ + L14 contradiction argument serving as an independent verification that no link-subspace V-position can carry a dom(C) target.

## OUT_OF_SCOPE

(None — the ASN's Scope section explicitly enumerates OUT OF SCOPE topics, and the ASN stays within its stated bounds.)

VERDICT: REVISE
