# Review of ASN-0058

## REVISE

### Issue 1: M16 omits T4-validity verification of `a₁ + n₁`

**ASN-0058, M16 (CrossOriginMergeImpossibility)**: "every index of the document prefix lies strictly below the action point and is preserved by TumblerAdd. Therefore origin(a₁ + n₁) = origin(a₁)."

**Problem**: For the conclusion `origin(a₁ + n₁) = origin(a₁)` to be meaningful, both sides must be defined. `origin(·)` is defined via T4b's projections N, U, D, which require their argument to be T4-valid. The proof shows the document prefix components are preserved but does not verify that `a₁ + n₁` itself satisfies T4. In particular, the proof does not establish: (a) the three zeros of `a₁` remain at the same positions in `a₁ + n₁` (now needs an explicit observation that the zero positions all lie strictly below `#a₁`, hence are preserved); (b) the last component `(a₁ + n₁)_{#a₁} = (a₁)_{#a₁} + n₁ ≥ 1` (preserving T4 conjunct (iv)); (c) no new adjacent zeros are introduced (only the last component is modified, and it is nonzero before and after).

**Required**: Add a brief verification that `a₁ + n₁` is T4-valid — i.e., that the four T4 conjuncts hold under TumblerAdd, given that (a₁)_{#a₁} ≥ 1 by T4(iv) and n₁ ≥ 1 by the block-width axiom. Without this, `origin(a₁ + n₁)` is asserted to exist without being shown to exist.

### Issue 2: M7 overlap exclusion conflates depth bounds

**ASN-0058, M7 (MergeCondition)**: "Hence J = ∅, so (v₂)_j = (v₁)_j for all 1 ≤ j < m"

**Problem**: The statement "(v₂)_j = (v₁)_j for all 1 ≤ j < m" presupposes `(v₂)_j` is defined at every j < m, hence `#v₂ ≥ m − 1`. But the very purpose of this paragraph is to *derive* `#v₂ = m` from S8-depth — depth equality cannot be both an output and an implicit assumption of the same step. The set-builder notation for J implicitly restricts to indices where `(v₂)_j` is defined, so the rigorous conclusion from J = ∅ is only `(v₂)_j = (v₁)_j for all 1 ≤ j ≤ min(#v₂, m−1)`. The argument is recoverable: `(v₂)_1 = (v₁)_1` (using only `#v₂ ≥ 1` from S8a) suffices for `subspace(v₂) = subspace(v₁)`, after which S8-depth forces `#v₂ = m`. But as written, the proof's intermediate statement is stronger than what J = ∅ delivers without already knowing `#v₂ ≥ m`.

**Required**: Replace "(v₂)_j = (v₁)_j for all 1 ≤ j < m" with the weaker conclusion that actually follows from J = ∅ (`(v₂)_1 = (v₁)_1` is sufficient), then derive `#v₂ = m` from S8-depth before invoking the prefix agreement on the full range 1 ≤ j < m in subsequent steps.

### Issue 3: First worked example does not state the same-origin assumption

**ASN-0058, "A Worked Example" (after M12)**: "I-adjacent? a₂ = [1, 13] = [1, 10] + 3 ✓. Both conditions hold — the blocks merge to β₁ ⊞ β₂ = ([1, 1], [1, 10], 5)."

**Problem**: The example computes I-adjacency by raw tumbler arithmetic in the elided-prefix notation, without addressing whether the implicit document prefix is identical across `[1, 10]` and `[1, 13]`. M16 (which the ASN has just established) implies the merge is valid *only if* `origin([1, 10]) = origin([1, 13])`. The example tacitly assumes this — fine if stated — but never says so. A reader following the algebra strictly would not know whether the example exhibits a same-origin merge (valid by M7) or asserts a merge across origins (which M16 forbids). The first example is the introductory illustration of the canonical-decomposition construction and should not require the reader to infer its origin assumption from the second example (where origins are stated explicitly).

**Required**: Add one clarifying sentence at the start of the example: e.g., "Assume all eight I-addresses originate from a single source document, so the elided prefix `N.0.U.0.D.0.` is the same for every address shown." Or explicitly note that this example demonstrates within-origin I-discontinuity (a gap from [1, 14] to [1, 40] within one document), reserving cross-origin examples for the second worked example.

## OUT_OF_SCOPE

None. The Open Questions section correctly defers operation-effects, decomposition-lattice structure, and depth-relationship questions to future ASNs; nothing in the body of ASN-0058 strays outside the bundle-algebra topic.

VERDICT: REVISE
