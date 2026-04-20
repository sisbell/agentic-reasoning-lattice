# Review of ASN-0043

## REVISE

### Issue 1: L13 coverage equality proved in one direction only
**ASN-0043, Reflexive Addressing**: "The coverage therefore equals {t ∈ T : b ≼ t} — exactly b and its extensions: ... We verify this by case analysis on tumblers t ≥ b with t ≠ b"

**Problem**: The claim is an equality: `coverage({(b, ℓ_b)}) = {t : b ≼ t}`. The case analysis verifies only the exclusion direction (coverage ⊆ {t : b ≼ t}) — showing that non-extensions of b are not in `[b, b ⊕ ℓ_b)`. The inclusion direction ({t : b ≼ t} ⊆ coverage) — showing that every extension of b IS in `[b, b ⊕ ℓ_b)` — is never stated.

L10 proves the identical inclusion argument for the analogous construction: "c ≥ p by T1(ii) (the prefix precedes its extensions), and c < inc(p, 0) because c agrees with p at position sig(p)..." But L13 neither reproduces this argument nor cites L10.

Additionally, the shorter-depth case is faulty. The proof says: "agreement at positions 1..#t makes t a prefix of b, so t < b by T1(ii). Excluded." But the premise of the case is t ≥ b; if t is a proper prefix of b then t < b, which contradicts the premise — this sub-case is *impossible*, not "excluded." The sub-case that actually does the work (divergence at some k ≤ #t < #b giving t > b ⊕ ℓ_b) is omitted entirely.

**Required**: (a) Add the inclusion direction: for extension c with b ≼ c, c ≥ b by T1(ii) and c < b ⊕ ℓ_b because c_{#b} = b_{#b} < b_{#b} + 1 = (b ⊕ ℓ_b)_{#b}. (b) Fix the shorter-depth case: state that the agreement sub-case contradicts t ≥ b, and handle the divergence sub-case (t_k > b_k = (b ⊕ ℓ_b)_k for k < #b, giving t > b ⊕ ℓ_b).

### Issue 2: L9 formal statement weaker than proof; witness proof incomplete
**ASN-0043, The Type Endset (L9)**: The formal statement is existential: `(E Σ' :: Σ' satisfies L0–L14 ∧ S0–S3 ∧ ...)`. The prose claims the stronger universal: "for any conforming state Σ satisfying L0–L14 and S0–S3, there exists a conforming state Σ' extending Σ..." The proof demonstrates the universal version ("Take any conforming Σ").

**Problem (a)**: The formal statement should match what the proof establishes. If the intent is that ghost-typed links can be added to *any* conforming state (not merely that *some* conforming state happens to contain one), the formal statement needs a universal quantifier over Σ.

**Problem (b)**: The witness proof checks only T12, L3–L5, then asserts "no property of this ASN requires coverage(Σ'.L(a).type) ⊆ dom(Σ'.C)." This is a negative claim about all fifteen properties without enumeration. The proof does not verify: L0 (the new link address is in subspace s_L), L1 (element-level), L1a (scoped allocation under the creating document), L11 (the new address is distinct from all existing ones — GlobalUniqueness), or L12 (existing links are preserved in the extended state). The worked example later provides a full verification of a similar construction, but the L9 proof should stand on its own.

**Required**: (a) Align the formal statement with the universal claim: `(A Σ : Σ satisfies L0–L14 ∧ S0–S3 : (E Σ' extending Σ :: ...))`. (b) Complete the witness by showing the allocation satisfies L0, L1, L1a (these follow from allocating in s_L under the creating document's prefix); L11 follows from GlobalUniqueness; L12 holds because only a new entry is added; L14 holds by construction.

### Issue 3: L10 proof relies on sig(p) = #p without stated restriction
**ASN-0043, The Type Endset (L10)**: "The action point is k = #p = sig(p) (by T4, the last component of a valid address is positive, so sig(p) = #p). ... By TA5(c), p ⊕ ℓ_p = inc(p, 0)"

**Problem**: The identity p ⊕ ℓ_p = inc(p, 0) via TA5(c) requires sig(p) = #p — i.e., the last component of p is nonzero. The proof invokes T4 to establish this, but L10 quantifies over "type addresses p, c ∈ T" without restricting p to valid addresses. Since L9 permits ghost type addresses that are outside dom(Σ.C) ∪ dom(Σ.L), and T4's scope ("every tumbler used as an address") is ambiguous for addresses referenced by endsets but not allocated, the restriction is not clearly justified.

The issue is avoidable: p ⊕ ℓ_p can be computed directly from TumblerAdd as [p₁, ..., p_{#p−1}, p_{#p} + 1] without invoking TA5(c). The inclusion argument then follows without any assumption about sig(p): for extension c with p ≼ c, c_{#p} = p_{#p} < p_{#p} + 1 = (p ⊕ ℓ_p)_{#p}, giving c < p ⊕ ℓ_p.

**Required**: Either (a) state explicitly that L10 applies to type address prefixes whose last component is positive (citing T4), or (b) derive p ⊕ ℓ_p directly from TumblerAdd, avoiding the TA5(c) step entirely. Option (b) is cleaner — it eliminates the restriction and simplifies the proof.

### Issue 4: L14 table mischaracterizes the identity semantics distinction
**ASN-0043, The Dual-Primitive Architecture (table)**:

| | Content | Links |
|---|---|---|
| Identity semantics | Shareable via transclusion (S5) | Unique per address (L11) |

**Problem**: S5 (UnrestrictedSharing) is a *sharing* property — the same I-address can appear in multiple arrangements. L11 (IdentityByAddress) is an *identity* property — address determines entity. But content also has identity by address (S4, OriginBasedIdentity), so L11 does not distinguish links from content. The actual asymmetry, which the text below the table correctly derives, is *transcludability*: content addresses can appear in arrangements (S5); link addresses cannot, because S3 requires arrangement targets to be in dom(Σ.C) and L0 establishes dom(Σ.L) ∩ dom(Σ.C) = ∅.

The row label says "Identity semantics" but the content column describes sharing and the link column describes a property that both primitives share.

**Required**: Revise the row to reflect the actual distinction. The content entry should describe transcludability (S5); the link entry should describe non-transcludability (S3 + L0). Alternatively, split the row: one for identity (both S4/L11) and one for sharing (S5 vs S3+L0).

### Issue 5: Worked example omits L2 verification
**ASN-0043, Worked Example**: The verification checklist covers L0, L1, L1a, L3–L6, L9–L14, and S3. L2 (OwnershipEndsetIndependence) is not checked.

**Problem**: The example verifies every other property against the constructed state but skips L2. While trivially satisfied — `home(a) = origin(a) = 1.0.1.0.1 = d`, computed from `a` alone without consulting endsets (F, G, Θ) — completeness requires it.

**Required**: Add L2 verification: `home(a) = origin(a) = 1.0.1.0.1`, which is computed from the field structure of `a` and does not depend on `Σ.L(a) = (F, G, Θ)`.

## OUT_OF_SCOPE

No out-of-scope items beyond what the ASN's scope section already identifies. The ASN correctly defers operations, resolution, survivability, and deletion semantics.

VERDICT: REVISE
