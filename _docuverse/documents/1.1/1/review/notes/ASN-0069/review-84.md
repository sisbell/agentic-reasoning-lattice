# Review of ASN-0069

## REVISE

### Issue 1: V8a and V11 reproduce the same content-identity induction
**ASN-0069, §"Structural Correspondence" (V8a) and §"Composability: Fork of a Fork" (V11)**: V8a proves "the I-addresses inherited by `wᵏ` are the same I-addresses `d_src` held at `Σ`" by induction composing V4 + V5 along a chain whose each operand is the chain predecessor; V11 proves "`M^k(d^k_new)(v)` ... equals `M(d_src)(v)`" by an induction of identical structure.

**Problem**: The two inductions are the same proof. V8a's own preamble concedes this: "Content inheritance is governed entirely by the operand — V4 reads `M` of the operand and is silent on whether the *allocation* step was `inc(·, 0)` or `inc(·, 1)` — so the induction below is carried by V4 and V5 alone." If the content induction is indifferent to step type, then the *only* difference between V8a (sibling stream, `inc(·,0)` steps) and V11 (nesting chain, `inc(·,1)` steps) is the tumbler-length/prefix bookkeeping — which V11 already isolates into the separate V11a. The core content-identity argument is therefore written out twice. This is the "two passages say the same thing" pattern at the granularity of full named lemmas. Compounding this, V8a does not appear to be consumed anywhere downstream (the worked example and later prose cite V8 and V11, not V8a), so the duplicated lemma is also orphaned.

**Required**: State the content-identity induction once as a single lemma parameterized by an emission chain whose each operand equals the chain predecessor (the step type being immaterial, per V8a's own remark), and instantiate it for both the sibling stream and the nesting chain. Keep V11a (the prefix/length chaining) separate since it is genuinely chain-specific. If V8a has no consumer, remove it rather than retaining a second copy of the proof.

### Issue 2: K.δ sub-case A and sub-case B repeat identical precondition discharges
**ASN-0069, §"The Fork Composite", K.δ sub-case A and sub-case B**: Both sub-cases discharge `T4-valid(d_new)` ("by T10a.4 ... applied to `A_v(d_src)` ... T10a-conforming per ASN-0047's Allocator hierarchy definition"), `¬Element(d_new)` ("follows from `Document(d_new)`"), `parent(d_new) ∈ E` ("V1 gives `parent(d_new) = parent(d_src)` ... P8 ... yields `parent(d_src) ∈ E`. Composing..."), and `Document(d_new)` ("V1's identity postcondition") in near-verbatim repeated text.

**Problem**: These four discharges do not depend on `k` and are reproduced word-for-word across the two sub-cases. The only genuinely sub-case-specific discharges are the freshness argument (ChildSpawnFreshness at `(d_src,1)` vs FrontierEquivalence at `d_prev`) and the per-sub-case operand preconditions. The shared block is duplication of the kind the anti-bloat pass targets.

**Required**: Factor the `k`-independent discharges (T4-validity via T10a.4, `¬Element` via `Document`, `parent(d_new) ∈ E` via V1 + P8, `Document(d_new)` via V1) into a single statement before the sub-case split, leaving only the freshness mechanism and per-sub-case operand preconditions inside the A/B branches.

### Issue 3: Narration of authorial method in place of reasoning
**ASN-0069, §"Identity by Sub-Allocation"**: "We use these in place of re-deriving stream structure, T4-validity, uniqueness, and extent from T10a primitives." and "What ASN-0040 does not supply — and what the inductions below establish — is the *level* and *parent* of each emission..."

**Problem**: These sentences describe what the authors are doing (citing rather than re-deriving; dividing labor between ASN-0040 and the local inductions) rather than advancing the argument. The citations themselves carry the content; the meta-narration is the forward-reference/method-commentary accretion flagged for this note.

**Required**: Delete the method-narration sentences. Cite ASN-0040 for stream structure/T4/uniqueness/extent at the point of use, and let the inductions establish level/parent without prefatory commentary on what they will establish.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork while source is being modified
**Why out of scope**: The first and several later Open Questions raise concurrency, descendant-discoverability time bounds, snapshot-vs-living forks, and version-space presentation. These are correctly deferred — they concern guarantees beyond the sequential-atomic transition model this ASN builds on, and belong in future ASNs.

### Topic 2: Counterpart correspondence for textually-identical, distinctly-typed content
**Why out of scope**: The closing Open Questions about relating equal-byte content at distinct I-addresses describe machinery (counterpart correspondence) that I-address identity deliberately does not provide; this is new territory, not a defect here.

VERDICT: REVISE
