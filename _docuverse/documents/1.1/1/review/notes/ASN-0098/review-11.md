# Review of ASN-0098

## REVISE

### Issue 1: Cross-subspace tightness case missing in achievability argument

**ASN-0098, achievability discussion within the tight endset section**: The case split is stated as "Cross-chain interference splits into three cases by the prefix relation between distinct document tumblers `d' ≠ d_0`: non-nesting…descendant…ancestor."

**Problem**: The case split is restricted to *distinct* documents (`d' ≠ d_0`). This misses the same-document, cross-subspace case: for a span on `A_C(d_0)`'s chain, chain elements of `A_L(d_0)` are also in F and could potentially fall in `[s, s ⊕ ℓ)`. Without an argument that they don't, the achievability claim is not fully established, and LP19a/LP19's "for any endset e tight at Σ_e" preconditions become uncertain about whether canonical construction actually produces such endsets.

**Required**: Add a fourth case (same document, cross subspace). The argument is direct: A_L(d_0) chain elements have value `s_L = 2` at position `#d_0 + 2`, while `s` and `s ⊕ ℓ` carry `s_C = 1` at that position (since `actionPoint(ℓ) = #s = #d_0 + 3 > #d_0 + 2` places this position in TumblerAdd's prefix-copy region). By SC-NEQ and T1 case (i) at position `#d_0 + 2`, A_L(d_0) elements exceed `s ⊕ ℓ`, so none fall in `[s, s ⊕ ℓ)`. The symmetric case (span on `A_L(d_0)` vs `A_C(d_0)` elements) needs the same treatment.

### Issue 2: Loose operation descriptions in descendant/ancestor cases

**ASN-0098, descendant case proof**: "By the K.δ rules for document allocation (ASN-0047), the only way to obtain a T4-valid document with `d_0 ≺ d'` is via the version sub-allocator, i.e. a chain of `inc(_, 1)` steps from `d_0`."

**Problem**: This is factually incorrect. Descendants of `d_0` can be obtained by interleaving `inc(·, 0)` and `inc(·, 1)` operations — e.g., `inc(d_0, 1) = d_0.1`, then `inc(d_0.1, 0) = d_0.2`, then `inc(d_0.2, 1) = d_0.2.1`. The latter is a descendant of `d_0` not reachable by `inc(·, 1)` steps alone. The ancestor case proof contains the symmetric error ("`d_0` was obtained from `d'` by a chain of `inc(_, 1)` version steps").

**Required**: Either reframe the argument structurally (which it actually is — the induction is on length difference `q = #d' - #d_0`, and the structural form `d_0.x_1.…x_q` with each `x_i ≥ 1` follows from T4-validity of `d'` and `zeros(d') = 2`, since zeros count of `d_0` is preserved means no `x_i` can be zero), or correctly describe the operation chain as "starting with `inc(d_0, 1)` and continuing with combinations of `inc(·, 0)` and `inc(·, 1)` operations". The structural conclusion is sound; the prose description should be corrected so a reader is not misled about the operation lattice.

### Issue 3: v_ℓ ∉ dom(Σ.M(d)) asserted without derivation in LP9

**ASN-0098, LP9 K.μ⁺_L sub-case**: "After K.μ⁺_L fires, `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}` with `v_ℓ ∉ dom(Σ.M(d))` — (E1) holds."

**Problem**: The "with `v_ℓ ∉ dom(Σ.M(d))`" clause is the strict-superset witness, but its derivation is left implicit. While ASN-0047's K.μ⁺_L effect specification asserts the strict superset, the link-subspace structural argument deserves explicit citation since two sub-cases must be discharged: (i) `V_{s_L}(d) = ∅` case where `v_ℓ = [s_L, 1]` is the D-MIN★ minimum and cannot coincide with any `V_{s_C}(d)` member by subspace divergence, and (ii) `V_{s_L}(d) ≠ ∅` case where `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (StrictIncrease, ASN-0034).

**Required**: Either cite K.μ⁺_L's effect clause as authoritative source for the strict superset (single sentence), or walk through the two-sub-case argument above so the reader can verify the freshness independently.

### Issue 4: Reference-frame remark overstates invariance

**ASN-0098, opening reference-frame remark**: "we will cite operations from whichever frame names them most directly without further reconciliation, since projection-level claims are invariant under the choice."

**Problem**: This is too strong. LP20's corollary (and its per-subspace refinement) cites S3★ from ASN-0047, which is strictly stronger than ASN-0036's S3 — S3 covers only the content subspace, whereas S3★ adds the link-subspace clause. The per-subspace split into `dom(C)` and `dom(L)` is not derivable from S3 alone. The claim of invariance under frame choice is therefore false in the literal direction stated; what actually holds is that the ASN works in the ASN-0047 frame and inherits ASN-0093's substrate, with the ASN-0036 frame being a strict subset of the operation vocabulary (no K.μ⁺_L, no link-subspace mappings) where S3 happens to suffice vacuously.

**Required**: Restate the remark to identify ASN-0047 + ASN-0093 as the working frame, and note that the projection definition and per-document lemmas (LP4-LP8) hold structurally identically in any sub-frame that lacks link-subspace mappings, while LP20's per-subspace refinement and LP9's K.μ⁺_L sub-case require the link-subspace machinery from ASN-0047.

VERDICT: REVISE
