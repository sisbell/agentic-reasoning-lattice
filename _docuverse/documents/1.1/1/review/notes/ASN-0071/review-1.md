# Review of ASN-0071

## REVISE

### Issue 1: S3 cited but state model is ASN-0047 (which supersedes S3 with S3★)

**ASN-0071, "The query" and "Resolution" sections**: "satisfying functionality (S2), referential integrity (S3), and content immutability (S0)" and "By S3, every element of `iaddrs(Q)(Σ)` lies in `dom(Σ.C)` — every resolved address is a valid content address."

**Problem**: The ASN says "We assume content has been allocated and arranged through the standard transitions of ASN-0047." But ASN-0047 explicitly supersedes S3 with S3★: "Supersedes S3 (ASN-0036)." Under S3★, `M(d)(v) ∈ dom(C)` iff `subspace(v) = s_C`; for link-subspace V-positions, `M(d)(v) ∈ dom(L)`. The categorical claim "every element lies in `dom(Σ.C)`" is incorrect in the extended state.

**Required**: Cite S3★, and either (a) restrict vspecs to content-subspace V-positions (so S3★'s content branch applies) or (b) generalize the codomain to `P(dom(C) ∪ dom(L))`. The choice must be explicit.

### Issue 2: vspec admits link-subspace positions silently; F-iaddrs codomain inconsistent

**ASN-0071, "The query"**: "A **vspec** is a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc` names a source document and `σ = (u, ℓ)` is a level-uniform V-span"

**Problem**: The vspec imposes no constraint on `subspace(u) = u₁`. Under ASN-0047's extended state with link-subspace V-positions (per K.μ⁺_L), a vspec with `u₁ = s_L` is well-formed and `iaddrs_one(d_s, σ)` would return link addresses in `dom(L)`. Yet F-iaddrs claims codomain `P(dom(C))`. The operation's semantics under link-subspace queries are undefined.

**Required**: Either add `subspace(u) = s_C` to vspec preconditions (aligning with the operation's name "containing this content"), or specify the link-subspace semantics explicitly.

### Issue 3: Reinvents ASN-0058's ContentReference

**ASN-0071, "The query" and "Resolution" sections**: defines vspec `(d_s, σ)` and `iaddrs_one(d_s, σ)`.

**Problem**: ASN-0058 (a foundation) already defines `ContentReference` as `(d_s, σ)` and `resolve(d_s, σ)` returning per-block I-address sequences. The current ASN's vspec is a relaxation of ContentReference (drops `V_{u₁}(d_s) ≠ ∅`, common-depth requirement, and well-formedness of `⟦σ⟧ ⊆ dom(M(d_s))`), and `iaddrs_one` is essentially the set-flattening of `resolve`. Per the standards, "if an ASN invents its own notation for something a foundation already defines, flag it as a REVISE item."

**Required**: Either use ASN-0058's ContentReference and derive iaddrs from resolve (set-flatten plus expansion), or justify the deliberate relaxation by stating exactly which conditions are dropped and why.

### Issue 4: No concrete example verifying the operation

**ASN-0071, throughout**: Eleven introduced claims, no worked scenario.

**Problem**: Standards require: "The ASN should verify its key postconditions against at least one specific scenario from the implementation evidence." Without a concrete example, claims like F-SHARE (cross-document discovery) and F-PART (partial overlap sufficient) have no operational grounding.

**Required**: A worked scenario, e.g.: state with `M(d₁) = {v₁ ↦ a₁}`, `M(d₂) = {v₂ ↦ a₁}` (transclusion), `M(d₃) = {v₃ ↦ a₂}`. Query `find({(d₁, σ)})` with `σ` covering `v₁`. Verify: `iaddrs = {a₁}`, `find = {d₁, d₂}`. Check F-SHARE (both discovered), F-DIST (each once), F-CUR (depends only on M and E_doc).

### Issue 5: Eleven claims, no derivations

**ASN-0071, "Claims Introduced"**: All eleven claims marked "introduced".

**Problem**: Several are tautological consequences of the definition (F-COMP and F-SOUND are the two directions of the iff defining `find`; F-PART is the iff with quantification unfolded; F-DIST is the type signature; F-SHARE is one direction of the defining iff; F-FILT is the intersection in the definition). Others (F-CUR, F-LOC, F-FIN) require derivation that is not shown. The ASN does not distinguish definitional restatements from non-trivial consequences.

**Required**: For each claim, either show a derivation step or mark it as "definitional" / "direct from definition." For non-trivial claims (F-CUR, F-LOC, F-FIN), provide the derivation chain.

### Issue 6: Finiteness argument incomplete

**ASN-0071, "Finiteness"**: "At any reachable state, `Σ.E_doc` is finite — it grows by one with each K.δ document-creation event, and there have been finitely many transitions from `Σ₀`."

**Problem**: The argument requires three steps: (a) `E₀ = {n₀}` has `|(E₀)_doc| = 0` (since `IsNode(n₀)`); (b) K.δ adds at most one entity per transition (from `E' = E ∪ {e}`); (c) reachability implies finite transition count from `Σ₀`. None of these is cited explicitly. The third is particularly important and not made formal anywhere in ASN-0047.

**Required**: Make the three-step derivation explicit, or cite the reachability finiteness invariant if it exists in the foundation.

### Issue 7: Empty-query behavior unspecified

**ASN-0071, throughout**: A vspec-set "is a finite collection" — does not exclude `Q = ∅`.

**Problem**: For `Q = ∅`, the union in `iaddrs(∅)(Σ) = ⋃_{q ∈ ∅} ...` is empty, so `find(∅)(Σ) = ∅`. This is a well-defined edge case, but the ASN does not state it. Standards require boundary cases to be addressed.

**Required**: An explicit claim that `find(∅)(Σ) = ∅` (or `iaddrs(∅)(Σ) = ∅`), or specify whether `Q` is required to be non-empty.

### Issue 8: vspec-set notation inconsistent with operation

**ASN-0071, "The query"**: "A **vspec-set** is a finite collection `Q = ⟨q₁, q₂, ..., q_k⟩`"

**Problem**: The notation `⟨...⟩` denotes a sequence; the term "vspec-set" denotes a set. The operation `iaddrs(Q) = ⋃_{(d_s, σ) ∈ Q}` treats `Q` as a set (duplicates absorbed by union). Pick one: if Q is a set, write `{q₁, ..., q_k}` and say so; if Q is a sequence with set semantics for iaddrs, state that duplicates do not affect the result.

**Required**: Resolve the notation/type mismatch.

### Issue 9: Existential body malformed

**ASN-0071, F-PART claim**: "`d ∈ find(Q)(Σ) ⟺ d ∈ Σ.E_doc ∧ (E a : a ∈ ran(Σ.M(d)) ∧ a ∈ iaddrs(Q)(Σ) ::)`"

**Problem**: Eindhoven `(E a : P :: Q)` requires a body Q. The pattern `(E a : P ::)` with empty body is malformed. Should be `(E a :: a ∈ ran(Σ.M(d)) ∧ a ∈ iaddrs(Q)(Σ))`.

**Required**: Fix the notation in F-PART and the corresponding prose ("Partial overlap suffices" section).

### Issue 10: F-COMP and F-SOUND framing muddled

**ASN-0071, "Completeness and soundness"**: "Every `d` satisfying the predicate is in the result" and "Every `d` in the result satisfies the predicate."

**Problem**: These are the two directions of the iff defining `find(Q)(Σ)`. They are not properties the operation has — they restate the definition. The discussion ("implementations that omit any qualifying document fails completeness") conflates "the abstract operation's biconditional" with "implementation conformance to the operation." Prose makes it sound like these are independent guarantees rather than two sides of a definition.

**Required**: Clarify that F-COMP and F-SOUND together are the membership iff; the implementation-conformance discussion is a separate concern about what it means to realize the abstract operation correctly.

## OUT_OF_SCOPE

The seven Open Questions at the end correctly identify future work: relationship to R for historical queries, strict resolution failure semantics, distributed replica consistency, visibility filtering, transition invariants for `find`'s result under contraction. None of these need to be specified in this ASN.

VERDICT: REVISE
