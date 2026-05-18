# Channel Assignment — ASN-0086 review-46

**Date:** 2026-05-18 02:09

```
## Issue 1: R5 status row claims more than the proof delivers
Reason: Pure alignment between table claim and proof body. The fix (trim the claim or add a one-line note about ASN-0034/0036 invariant orthogonality to endset content) is derivable from the ASN's own scope without external evidence.
```

```
## Issue 2: R7a's "factors through class (iii)" is ambiguous at categorical scope
Reason: Logical-precision rephrasing. The corrected wording (net-effect rather than implementation-invocation) is supplied by the review itself and follows from L12/L12a/Frame already in the note.
```

```
## Issue 3: R6b's proof body restates META content without proof depth
Reason: Structural/labeling choice (Remark vs Proof) internal to the note. The META framing already states the property as a Definition reading; either tightening or strengthening is an editorial decision.
```

```
## Issue 4: wp Case 1's P3-SFD relationship is unclear
Reason: Resolve a contradiction between simplification text and parenthetical. Internal consistency fix; the two valid forms are spelled out in the review.
```

```
## Issue 5: R0 Step 4's ASN-0036 invariant preservation is asserted without enumeration
Reason: Requires verifying that every ASN-0036 S-invariant has free variables only in (Σ.C, Σ.M). The ASN-0036 invariants' free-variable scope is derivable by reading ASN-0036 directly within the foundation stack, not from Nelson's intent or implementation evidence.
```

```
## Issue 6: Emit_K seed-independence depends on conditional R0a without flagging
Reason: Bridge sentence connecting Emit_K's definitional discipline commitment to R0a's conditionality. The composition is already in the note; only the explicit linkage is missing.
```

```
## Issue 7: Defensive rationale paragraphs accumulate around design choices
Reason: Editorial trimming/reorganization. Move or condense rationale paragraphs; no external evidence required to decide structural placement.
```

```
## Issue 8: R5 Stage 2's "Permissive/Orthogonal" inventory is verbose
Reason: Editorial condensation. The load-bearing observation (L4(c) permits link-subspace targets; no L-invariant constrains endset target content) is already in the proof and can replace the per-invariant enumeration.
```

```
## Issue 9: Navigation/scoping paragraphs add meta-overhead
Reason: Editorial cleanup of labels and duplicated discipline-conditional notes. Internal restructuring with no external dependency.
```

```
## Issue 10: R0's defensive prose about L1c chain semantics repeats Sparse-allocator hypothesis
Reason: Editorial deduplication. The Sparse-allocator hypothesis is already stated in Implementation hypotheses; recurring justifications can be cut and replaced with one citation.
```

```
## Issue 11: Worked Sketch's "Allocator scaffolding" interrupts the main narrative
Reason: Editorial — replace duplicated derivation with a back-reference to SharedDepthOneAllocator. The lemma already supplies the structure; no external evidence needed.
```
