# Review of ASN-0051

## REVISE

### Issue 1: SV6 proof contains a false intermediate claim

**ASN-0051, "Content Allocation and Coverage Stability" § SV6**: "First, #t ≥ #s: if #t < #s, then either t agrees with s on all positions 1 through #t — making t a proper prefix of s, so t < s by T1(ii), contradicting s ≤ t — or t diverges from s at some j ≤ #t with tⱼ > sⱼ = (s ⊕ ℓ)ⱼ, giving t > s ⊕ ℓ, contradicting t < s ⊕ ℓ."

**Problem**: The equality `sⱼ = (s ⊕ ℓ)ⱼ` holds only when `j < k` (positions before the action point). The proof assumes this holds for all `j ≤ #t`, but when `k ≤ #t < #s`, the divergence point `j` can equal `k`, where `(s ⊕ ℓ)ₖ = sₖ + ℓₖ ≠ sₖ`.

Counterexample: let `s = [1, 0, 1, 0, 1, 0, 2, 3]` (element-level, `#s = 8`, `p₃ = 6`) and `ℓ = [0, 0, 0, 0, 0, 0, 5, 1]` (action point `k = 7 > p₃`). Then `s ⊕ ℓ = [1, 0, 1, 0, 1, 0, 7, 1]`. The tumbler `t = [1, 0, 1, 0, 1, 0, 3]` has `#t = 7 < 8 = #s`, is element-level (`zeros(t) = 3`), and satisfies `s < t < s ⊕ ℓ` (divergence at position 7: `2 < 3 < 7`). So `t ∈ ⟦(s, ℓ)⟧` with `#t < #s`.

The final conclusion of SV6 is still correct because the proof only needs `#t ≥ k`, not `#t ≥ #s`. The claim `#t ≥ k` is provable directly: if `#t < k`, then either `t` is a proper prefix of `s` (giving `t < s`, contradiction), or `t` diverges from `s` at some `j ≤ #t < k`, where `(s ⊕ ℓ)ⱼ = sⱼ` does hold (since `j < k`), giving the desired contradiction.

**Required**: Replace the intermediate claim with `#t ≥ k` and prove it directly via the two cases (prefix divergence and component divergence at `j < k`). The derivation of `#t ≥ k` from `#t ≥ #s` and `k ≤ #s` should be replaced with the direct argument. The rest of the proof (agreement on positions `1..k−1`, origin equality) follows from `#t ≥ k` without change.

### Issue 2: SV2 proof covers only K.μ⁺, not K.μ⁺_L as claimed

**ASN-0051, "Extension Preserves and May Enlarge" § SV2 proof**: "Proof: ... ran(M'(d)) ⊇ ran(M(d)) (K.μ⁺ frame) ..." and the locate proof: "Since K.μ⁺ preserves existing mappings (dom(M(d)) ⊆ dom(M'(d)) with M'(d)(v) = M(d)(v) for all v ∈ dom(M(d)))..."

**Problem**: SV2 is stated for both K.μ⁺ and K.μ⁺_L, but the formal proof only references K.μ⁺'s frame conditions. The prose before SV2 establishes that K.μ⁺_L has the same monotonicity structure, but the proof parenthetical and the locate argument each name only K.μ⁺. The argument extends trivially (K.μ⁺_L adds one mapping `v_ℓ ↦ ℓ` while preserving all existing ones), but the proof as written doesn't match the claim's scope.

**Required**: The proof parenthetical should read "(K.μ⁺/K.μ⁺_L frame)" or equivalent, and the locate proof should note that K.μ⁺_L also preserves existing mappings — one additional sentence suffices.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to endset projection structure

The SV11 decomposition analyzes only the text-subspace projection `π_text(e, d)`. The full projection `π(e, d)` may additionally include I-addresses reached through link-subspace V-positions (K.μ⁺_L maps `v_ℓ ↦ ℓ` where `subspace(v_ℓ) = s_L`). The structural characterization of the link-subspace contribution — including endsets whose coverage intersects `dom(Σ.L)` per L13 (ReflexiveAddressing) — is explicitly deferred.

**Why out of scope**: The ASN correctly identifies this as belonging to a Link Subspace ASN. The core survivability guarantees (SV1–SV10, SV12, SV13(a)–(e)) operate on the full `π(e, d)` and are not affected by this deferral.

### Topic 2: Discovery function generalization beyond `dom(Σ.C)`

The `discover_s(A)` definition restricts `A ⊆ dom(Σ.C)`, but the proofs (SV8, SV9) work for any `A ⊆ T`, and practical discovery through a document's arrangement may yield link-subspace I-addresses (in `dom(Σ.L)`, not `dom(Σ.C)`).

**Why out of scope**: The restriction doesn't invalidate any stated result — every use of `discover_s` in the ASN can be witnessed with `A ⊆ dom(Σ.C)` by restricting to text-subspace V-positions. Broadening the definition is a future refinement, not a correctness issue.

VERDICT: REVISE
