# Review of ASN-0063

## REVISE

### Issue 1: CL1/CL2 claim coverage equals image, but the equality is false

**ASN-0063, Endset Resolution**: "there exists an endset `E ∈ Endset` with `coverage(E) = image(d, Ψ)`" (CL1) and "coverage(resolve(d, Ψ)) = image(d, Ψ)" (CL2)

**Problem**: `image(d, Ψ)` is a finite set of element-level I-addresses (since `dom(M(d))` is finite by S8-fin). But the coverage of any non-empty endset is infinite. A span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}`, which includes all tumblers in the range — including those deeper than `s`. By T0(b) and T1(ii), any tumbler that has `s` as a proper prefix satisfies `s < t`, and for the CL0 I-spans, such extensions satisfy `t < reach` as well (the extension agrees with `s` at the action point where `reach` is strictly larger). So every non-trivial span denotation contains infinitely many tumblers of depth `> #s`. No endset can have coverage equal to a finite non-empty set.

This means the `resolve` definition is vacuous — it defines a function as "the normalized endset satisfying CL2," but no such endset exists. CL2 and CL1 are unprovable as stated.

**Required**: Replace the equality with containment: `image(d, Ψ) ⊆ coverage(resolve(d, Ψ))`. Define `resolve` by construction (the CL1 proof's I-span collection, normalized) rather than by a property no endset can satisfy. If exact representation matters, define an element-level restriction of coverage: `coverage(E) ∩ {a : zeros(a) = 3} ⊇ image(d, Ψ)`, and show equality holds at element level (since the only same-depth tumblers between consecutive ordinal increments are those increments themselves).

---

### Issue 2: Step 2 of CREATELINK is not a defined elementary transition

**ASN-0063, The CREATELINK Composite**: "Extend M(d) at a fresh V-position v_ℓ in the link subspace, mapping v_ℓ to ℓ"

**Problem**: This step is not any of ASN-0047's elementary transitions. K.μ⁺ (ArrangementExtension) requires `a ∈ dom(C)` for every new mapping `M'(d)(v) = a`. Here `ℓ ∈ dom(L)` and `ℓ ∉ dom(C)` (by L0/L14). The ASN acknowledges that step 2 "parallels K.μ⁺" but never defines it as an elementary transition with preconditions and frame. Without a formal definition:

- The preconditions on `v_ℓ` are unstated. What value must `v_ℓ` take? The first link must use `[s_L, 1, ..., 1]` (D-MIN). Subsequent links must extend the contiguous range (D-CTG). None of this is specified.
- The frame is unstated. We cannot verify that step 2 preserves C, E, R, or other documents' arrangements, because no frame condition is given.
- The composite cannot be validated against ASN-0047's "valid composite" definition, which requires elementary transitions from a defined set.

**Required**: Define a new elementary transition (e.g., K.μ⁺_L) for link-subspace arrangement extensions, with explicit preconditions (including V-position choice satisfying D-CTG, D-MIN, S8-depth for the link subspace), effect (`M'(d)(v_ℓ) = ℓ` with `ℓ ∈ dom(L')`), and frame conditions. Alternatively, generalize K.μ⁺ with subspace-specific referential integrity. Either way, extend the "valid composite" definition to include the new transition.

---

### Issue 3: S3 violated by link-subspace arrangement mappings

**ASN-0063, CL11**: "S3 (ReferentialIntegrity): holds for text-subspace mappings since those are unchanged; the link-subspace mapping v_ℓ ↦ ℓ satisfies ℓ ∈ dom(L'), the link-subspace analogue."

**Problem**: S3 as stated in ASN-0036 is: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`. There is no subspace guard. After step 2, `v_ℓ ∈ dom(M'(d))` and `M'(d)(v_ℓ) = ℓ`. Since `ℓ ∈ dom(L')` and `dom(L') ∩ dom(C') = ∅` (L14), `ℓ ∉ dom(C')`. S3 is violated. The "link-subspace analogue" invoked by the proof is never defined — it is not S3, and no substitute invariant is stated.

**Required**: Either (a) generalize S3 to a subspace-conditional referential integrity invariant (text mappings → dom(C), link mappings → dom(L)), state this generalization explicitly, and use it in CL11; or (b) adopt a design where link-subspace positions are tracked in a separate component from M(d), leaving S3 intact.

---

### Issue 4: J1 and P7 are mutually unsatisfiable for link-subspace mappings

**ASN-0063, The CREATELINK Composite / CL11**: The composite omits K.ρ. CL11 claims "P7, P7a (Provenance): R is unchanged and dom(C) is unchanged."

**Problem**: Two ASN-0047 invariants conflict when link addresses enter `ran(M(d))`:

- **J1** (ExtensionRecordsProvenance): `a ∈ ran(M'(d)) \ ran(M(d)) ⟹ (a, d) ∈ R'`. After step 2, `ℓ ∈ ran(M'(d)) \ ran(M(d))`, so J1 requires `(ℓ, d) ∈ R'`.
- **P7** (ProvenanceGrounding): `(a, d) ∈ R ⟹ a ∈ dom(C)`. If `(ℓ, d) ∈ R'`, then P7 requires `ℓ ∈ dom(C)`. But `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅`.

So J1 demands provenance recording for the new link-subspace mapping, but P7 forbids it. The composite omits K.ρ (violating J1). Adding K.ρ would violate P7. Neither option works under the current framework.

**Required**: The coupling constraints and provenance invariants must be generalized for the extended state. Options: (a) scope J1 and P7 to content-subspace mappings, (b) generalize R to cover both dom(C) and dom(L) entries, or (c) keep link-subspace positions out of M(d) so J1 never fires.

---

### Issue 5: "Already normalized" claim is incorrect

**ASN-0063, Endset Resolution**: "the endset from CL1, sorted by start position, is already normalized (N1, N2, ASN-0053) within each V-span's contribution."

**Problem**: The non-adjacency argument proves that V-consecutive blocks in the canonical decomposition cannot produce I-adjacent CL0 outputs. This is correct. But it does not establish N2 (non-overlap) for the sorted I-span set because non-consecutive blocks can produce I-overlapping projections.

Counterexample: Block β₁ = (v₁, a, 3) maps V-positions 1–3 to I-addresses a, a+1, a+2. Block β₃ = (v₃, shift(a,1), 3) maps V-positions 7–9 to I-addresses a+1, a+2, a+3 (transcluded content — permitted by S5). A V-span covering positions 1–9 produces CL0 I-spans covering [a, shift(a,3)) and [shift(a,1), shift(a,4)). These overlap at a+1 and a+2. The sorted I-span set violates N2.

The endset is still valid (coverage is correct), but it is not "already normalized" — it requires the S8 normalization sweep.

**Required**: Remove the "already normalized" claim. State that the CL0 I-span collection forms a valid (but potentially un-normalized) endset, and that normalization via S8 is applied to produce the final endset.

---

### Issue 6: Normalization invokes S8 without checking level-compatibility

**ASN-0063, Endset Resolution**: "resolve(d, Ψ) is the normalized endset (per S8, ASN-0053)" and "resolve(S) = normalize(resolve(d₁, Ψ₁) ∪ ... ∪ resolve(dₘ, Ψₘ))"

**Problem**: S8 (NormalizationExistence, ASN-0053) has precondition: "Σ is a span-set whose component spans are level-uniform and mutually level-compatible." CL0 I-spans have `#start = #width` (level-uniform), but different blocks can produce I-spans of different depths when the arrangement maps V-positions to I-addresses from different sources. Within a single document, content transcluded from documents with different tumbler prefix lengths produces I-addresses of different depths. The CL0 I-spans from such blocks have different-length starts, failing `level_compat`. Cross-document resolution compounds this.

S3 (MergeEquivalence) and S4 (SplitPartition) also require level-compatibility. Without it, the S8 normalization sweep cannot merge adjacent or overlapping spans.

**Required**: Either (a) show that all I-spans produced by CL0 within a single resolution are level-compatible (this would require all I-addresses in the arrangement to share the same depth — unlikely in general), (b) define normalization for mixed-depth span sets (trivial when different-depth spans are automatically separated by T10, but this must be stated), or (c) drop the normalization requirement and define resolve as producing a finite set of well-formed I-spans without normalization.

---

### Issue 7: CL11 incorrectly claims D-CTG and D-MIN are text-subspace-scoped

**ASN-0063, CL11**: "S8-fin, S8a, S8-depth, D-CTG, D-SEQ: these are scoped to the text subspace and are unaffected by link-subspace extension. ✓"

**Problem**: D-CTG is stated as: "For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position..." This quantifies over ALL subspaces S, not just the text subspace. After step 2, V_{s_L}(d) contains one or more positions. D-CTG requires these to form a contiguous range. D-MIN requires `min(V_{s_L}(d)) = [s_L, 1, ..., 1]`. S8-depth requires all link-subspace V-positions to share the same depth. These per-subspace invariants apply to the link subspace and must be verified.

S8a IS text-subspace-scoped (guarded by v₁ ≥ 1), and S8-fin is trivially preserved (adding one position to a finite set). But claiming D-CTG and D-MIN are text-subspace-scoped is wrong.

**Required**: Verify D-CTG, D-MIN, and S8-depth for the link subspace after step 2. This requires specifying v_ℓ's value (which is part of Issue 2's fix).

---

### Issue 8: No concrete worked example

**ASN-0063, throughout**: The ASN mentions a scenario — "'AABB' where 'AA' was transcluded from document X and 'BB' from document Y" — but only in prose. No formal verification of postconditions against concrete tumbler addresses is provided.

**Problem**: The review standards require at least one specific scenario verifying key postconditions. For CREATELINK: define specific document tumblers, V-positions, I-addresses, and a mapping block decomposition; compute the CL0 projections; form the endset; execute the composite; and verify CL3(a–e), CL4, CL8 against the concrete post-state.

**Required**: Add a worked example with specific addresses (e.g., home document at `1.0.1.0.1`, content blocks with explicit V→I mappings, a V-span selection, and the resulting link). Verify CL3 postconditions and CL8 discovery against the concrete result.


## OUT_OF_SCOPE

### Topic 1: Link subspace arrangement invariant design
**Why out of scope**: The ASN correctly raises this as an open question ("What invariants must the link subspace of a document's arrangement satisfy..."). Designing these invariants is future work. What this ASN must do (and currently doesn't — see Issues 2 and 7) is acknowledge that existing per-subspace invariants apply and verify step 2 against them, but the broader design of link-subspace-specific invariants belongs in a dedicated ASN.

### Topic 2: Discovery efficiency requirements
**Why out of scope**: The ASN defines disc as a mathematical function on the state. The implementation requirement that "the quantity of links not satisfying a request does not in principle impede search" is an efficiency constraint on the implementation, not an abstract invariant. A future ASN on the link enfilade would address this.

### Topic 3: Concurrent link creation semantics
**Why out of scope**: The ASN correctly raises this as an open question. The sequential transition model of ASN-0047 does not address concurrency. Concurrent allocation semantics belong in a separate ASN on concurrency control.

VERDICT: REVISE
