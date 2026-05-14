# Review of ASN-0058

## REVISE

### Issue 1: "v + 0 = v" convention used before formal introduction

**ASN-0058, M0 and M1 proofs**: "if `j = 0`, then `v + j = v` and `v + k > v` by TS4..."

**Problem**: The convention "v + 0 = v" (extending ASN-0034's `shift`, which is defined for `n ≥ 1`) is consumed in the proofs of M0 and M1 but is only formally introduced in M-aux, which appears *after* M1. The phrase "extended to `k = 0` as the identity" in the Mapping Block definition mentions the convention informally but does not establish it. Since TS5 (ShiftAmountMonotonicity, ASN-0034) requires `n₁ ≥ 1`, the case split on `j = 0` truly depends on this convention being in force.

**Required**: Introduce the convention `v + 0 = v` (and the analogous one for I-addresses) before M0 — either as part of the Mapping Block definition itself or as a labeled preliminary. The convention is foundational to every block-arithmetic claim that follows; it should not appear three sections later as a side remark in M-aux.

### Issue 2: Mapping blocks are subspace-confined, but the property is never stated

**ASN-0058, throughout (M7, M12, C0a, C1a)**: Multiple proofs argue from "v + k has the same subspace as v" (via OrdShiftHom, ASN-0036), then chain through S8-depth to get common depth.

**Problem**: The fact that every position in V(β) shares a single subspace (and hence a single depth) is a structural property of mapping blocks, repeatedly invoked but never elevated to a labeled claim. M7's proof of the overlap contradiction, M12's argument that two runs sharing `v` share subspace, and C1a's transfer of S8-depth to `dom(f)` all rely on it. The reader is left to reconstruct the same OrdShiftHom + S8-depth chain at each site.

**Required**: State subspace confinement as a labeled corollary near the Mapping Block definition — e.g., "M-sub: for every block β = (v, a, n), every position in V(β) shares subspace(v); and by S8-depth, when V(β) ⊆ dom(M(d)) every position in V(β) has the same depth `m`." The downstream proofs can then cite M-sub once rather than re-deriving it.

### Issue 3: Resolution V-ordering claim is informal commentary, ambiguously worded

**ASN-0058, paragraph after the definition of resolve**: "if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence."

**Problem**: The phrasing "the I-address at p precedes the I-address at q" is ambiguous between (a) the run pair containing `M(d_s)(p)` appears earlier in the sequence than the run pair containing `M(d_s)(q)`, and (b) the tumblers `M(d_s)(p)` and `M(d_s)(q)` are ordered under T1. Only (a) is intended — (b) fails in general across block boundaries (in the worked example, run 2 begins at `b` which need not exceed `(a+1) + 2`). The claim is also not given a label or formal statement, even though it is invoked as a structural property of the construction.

**Required**: Either elevate the claim to a labeled proposition (e.g., "C0b: ResolutionSequenceOrder — the runs in `resolve(d_s, σ)` are listed in strictly increasing V-start order, by B2") with explicit phrasing that distinguishes sequence position from tumbler order; or remove the sentence entirely, since it is already implicit in the "ordered by V-start" phrase of the resolution definition.

### Issue 4: M16 relies on T4-validity of a₁ but never cites the source

**ASN-0058, M16 proof, paragraph 1**: "T4(iv) of `a₁` gives `(a₁)_{#a₁} ≥ 1`..."

**Problem**: The verification of T4-validity for `a₁ + n₁` inherits clauses from T4-validity of `a₁`, but the proof never establishes that `a₁` is itself T4-valid. The chain `a₁ ∈ dom(C) ⟹ a₁ allocated by a T10a-conforming allocator (S7a/S7d) ⟹ a₁ is T4-valid (T10a.4, ASN-0034)` is implicit. Without this anchor, "T4(iv) of `a₁`" is asserted without warrant.

Additionally, the same paragraph references "(with `#a₁ ≥ 2` from S7b/S7c below, so index 1 lies strictly below the action point)" — "below" here means the next paragraph of the same proof, not a downstream claim. This usage invites confusion about the logical structure of the proof.

**Required**: Open M16's proof with one sentence establishing `a₁` (and `a₂`) as T4-valid via S7b/S7d + T10a.4, then proceed with the T4-validity of `a₁ + n₁`. Replace "S7b/S7c below" with a forward reference that names the paragraph or simply restructure the proof so the document-prefix location comes before the conjunct-(iii) check.

## OUT_OF_SCOPE

### Topic 1: Lattice structure of equivalent decompositions
**Why out of scope**: Already flagged in the ASN's own Open Questions; refinement-ordering between equivalent decompositions is a structural extension, not a gap in the algebra established here.

### Topic 2: Resolution ordering across multi-source content reference sequences
**Why out of scope**: Whether an implementation may reorder source references is correctly deferred to the Open Questions section — the abstract algebra fixes the per-reference resolution order but the cross-reference composition order is a downstream policy choice.

### Topic 3: Constraints on V-extent vs. block count
**Why out of scope**: Quantitative bounds relating the canonical block count to arrangement size belong in a downstream analysis ASN, not in the algebra itself.

VERDICT: REVISE
