# Review of ASN-0117

## REVISE

### Issue 1: DELETE's operation definition omits the link-store frame condition
**ASN-0117, "DELETE(`d`, `p`, `w`)" Effect/Frame, and P4**: The operation lists effect clauses (DEL-REMOVE, DEL-SHIFT, DEL-LEFT, DEL-DOM, DEL-CIMM) and frame clauses (DEL-FSUB, DEL-FDOC) — but no clause constrains the link store `Σ.L`. DEL-CIMM frames only `Σ.C`; DEL-FSUB/DEL-FDOC frame only `Σ.M`. P4 then asserts "the link store untouched (L12)."

**Problem**: L12 (LinkImmutability) only guarantees that *existing* links keep their values (`a ∈ dom(Σ.L) ⟹ Σ'.L(a) = Σ.L(a)`); it does **not** forbid the addition of new links to `dom(Σ.L)`. As specified, nothing in DELETE's contract prevents `dom(Σ'.L) ⊋ dom(Σ.L)`. This is load-bearing: the wp derivation quantifies over "every prior link `a ∈ dom(Σ.L)`" and concludes `D(d, Σ') = D(d, Σ)`, which is only correct if `dom(Σ'.L) = dom(Σ.L)`. If DELETE could add a link, `D(d, ·)` could grow and the wp would be wrong. ASN-0082's frame supplies no help — ASN-0082's state is `(C, M)` and has no `Σ.L`.

**Required**: Add an explicit frame clause `Σ'.L = Σ.L` (both domain and per-address value) to DELETE's Effect/Frame, and cite it — not L12 — where P4 and the wp rely on full link-store invariance.

### Issue 2: LP10 (ContractionMonotonicity) is misapplied to DELETE
**ASN-0117, P4**: "DELETE shrinks `d`'s range — `ran(M'(d)) ⊆ ran(M(d))` — by removing the deleted mappings (foundation **LP10 (ContractionMonotonicity)**, ASN-0098)."

**Problem**: LP10's stated premise is *a K.μ⁻ transition*, and K.μ⁻ (ASN-0047) is a prefix-retention truncation in which surviving mappings are unchanged (`M'(d)(v) = M(d)(v)`, no shift). DELETE is a middle-span contraction that *left-shifts* the suffix (DEL-SHIFT relabels `q_k → q_{k−c}`) — it is not a K.μ⁻ transition. Worse, LP10's actual conclusion is a *projection* inclusion `project(e, d, Σ') ⊆ project(e, d, Σ)` over V-positions, which is **false** for DELETE: the post-state projection contains shifted positions `q_{k−c}` absent from the pre-state projection. The note borrows LP10 to assert a *range* fact LP10 never states, from a premise DELETE does not satisfy.

**Required**: Derive `ran(M'(d)) ⊆ ran(M(d))` directly from DELETE's own clauses (DEL-LEFT and DEL-SHIFT preserve I-address values; DEL-REMOVE drops the deleted block; DEL-DOM fixes the surviving domain) — the wp section already does exactly this computation. Drop the LP10 citation, or justify formally that DELETE is an instance to which LP10 applies (it is not).

## OUT_OF_SCOPE

### Topic 1: DELETE's registration in the operation vocabulary
DELETE (middle-span deletion with gap-closing left-shift) is not one of ASN-0047's atomic K-operations (K.μ⁻ truncates a prefix; K.μ~ preserves the domain). Whether DELETE should be admitted as a new atomic operation — and ASN-0047's ExtendedReachableStateInvariants theorem extended to cover it, so that the per-operation ASN-0098 lemmas transfer cleanly — is integration work for a future ASN, not an error here. (It does, however, motivate fixing Issue 2 by direct derivation rather than borrowed per-operation lemmas.)

### Topic 2: Backtrack reconstruction, concurrency, content-discovery index
The Open Questions on prior-arrangement reconstructibility, concurrent same-scope edits without a serializing authority, and a content-based discovery index after deletion are genuinely new territory, correctly left open.

VERDICT: REVISE
