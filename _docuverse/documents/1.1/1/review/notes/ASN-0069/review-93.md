# Review of ASN-0069

## REVISE

### Issue 1: B8 same-namespace clause invoked without discharging its precondition package

**ASN-0069, §"Identity by Sub-Allocation" item (iii), and V10(a)**: "distinct emissions of one namespace are distinct addresses under a single authority by B8 (Uniqueness)" and "B8 (Uniqueness, ASN-0040), same-namespace clause, gives `d_new¹ ≠ d_new²` directly."

**Problem**: B8's same-namespace contract (ASN-0040) has a substantial precondition package: "committed under a single baptismal authority (so B-Seq applies), in a system conforming to B-Seq, B0★ (which subsumes B0), B0a, B1, B2, and B4." ASN-0069 invokes the same-namespace clause by merely asserting "under a single authority" — it never establishes that the ASN-0047 transition system satisfies B-Seq (let alone B0a, B1, B2, B4). The cross-namespace clause of B8 is unconditional, but here both forks are emissions of the *same* namespace `S(d_src, 1)`, so the conditional same-namespace clause is the one in force, and its premises are load-bearing. This is the central uniqueness argument for sequential forks; an asserted "single authority" is not a discharge.

**Required**: Show that ASN-0047's SequentialTransitionAxiom (total ordering of atomic transitions) discharges ASN-0040's B-Seq (states under one serialized commit path totally ordered by →*), and that the registry-discipline prerequisites B0a, B1, B2, B4 hold for `A_v(d_src)` in the ASN-0047 model — or, if they are inherited rather than re-proved, cite the inheritance explicitly. The bridge from "transitions are sequentially ordered" to "B-Seq applies" must be a stated step, not an asserted phrase.

### Issue 2: V5a's "d* ∈ E_doc" has no temporal anchor, leaving the K.δ sub-argument unjustified

**ASN-0069, V5a derivation**: "K.δ preserves every document other than its fresh `d_new` (which is `≠ d*`, since `d* ∈ E_doc ⊆ E` while the K.δ precondition `e ∉ E` places `d_new ∉ E` pre-step)."

**Problem**: The derivation asserts `d* ∈ E_doc ⊆ E` *at the pre-step of each K.δ transition in the sequence*, but the lemma statement only says "any document `d* ∈ E_doc`" with no anchor to a state. If `d*` is read as belonging to `E_doc` at the final state `Σ'`, it might have been created by a K.δ step *within* the sequence; for that step the antecedent `d* ∈ E` at the pre-step is false, and `d_new = d*` is exactly the document whose arrangement changes (∅ → populated), breaking the frame composition. The argument silently needs `d* ∈ Σ.E_doc` (initial state) plus P1 to keep it in `E` at every intermediate pre-step.

**Required**: Anchor `d*` to the initial state — `d* ∈ Σ.E_doc` — and cite P1 (EntityPermanence) for the standing membership `d* ∈ E` at each intermediate K.δ pre-step. Both fork applications (`d* = d_src`, `d* = d_new`) satisfy this, so the fix is a precision tightening, not a scope change.

### Issue 3: V9 closes with defensive meta-prose about logical direction

**ASN-0069, V9 derivation**: "This is precisely what *discharges* J1★ (ExtensionRecordsProvenance) for the composite: the coupling obligation is satisfied by V9's records, not a premise from which they are derived."

**Problem**: The derivation already establishes `R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}` and the per-`a` membership. The trailing sentence adds no reasoning step — it pre-empts a confusion about whether J1★ is premise or conclusion. This is the defensive justification the anti-bloat pass targets: a precise reader does not need the direction-of-implication disclaimer, and the actual J1★ discharge is already performed concretely in the composite verification ("J1★ holds because every `a`...").

**Required**: Delete the closing sentence. If the discharge needs a pointer, the composite-verification coupling check is the canonical site.

### Issue 4: Dependency Audit's ASN-0040 paragraph restates §"Identity by Sub-Allocation"

**ASN-0069, §"Dependency Audit"**: "ASN-0040 (Tumbler Baptism) grounds version identity (§"Identity by Sub-Allocation"): the version sub-allocator `A_v(d_src)` is the baptism sibling stream `S(d_src, 1)`; the next fork address is `next(s.B, d_src, 1)` (NextAddress); the depth-1 baptism from a document is valid by B6 ... by B8 (Uniqueness); and ... by B9 (UnboundedExtent)."

**Problem**: This paragraph re-enumerates the same B6/B8/B9/NextAddress/T4-validity grounding already given substantively in §"Identity by Sub-Allocation" — two passages in the same document saying the same thing in different words. The Dependency Audit's purpose is to confirm each declared dependency is consumed; it does not need to reproduce the consumption argument.

**Required**: Reduce the ASN-0040 entry to a one-line confirmation that the dependency is consumed in §"Identity by Sub-Allocation" (and which results), without re-listing each baptism result and its discharge.

## OUT_OF_SCOPE

### Topic 1: Fork of a transcludent source

**Why out of scope**: When `M(d_src)` references I-addresses with `origin ≠ d_src`, the inherited-attribution behavior is genuinely new territory. The ASN correctly defers it to an Open Question, and V9b's `origin(a) ≠ d_new` claim remains true regardless.

### Topic 2: Concurrent fork during source modification

**Why out of scope**: Beyond what SequentialTransitionAxiom supplies, concurrency guarantees are a future concern. The ASN already lists this as an Open Question; no claim in this ASN over-reaches into it.

VERDICT: REVISE
