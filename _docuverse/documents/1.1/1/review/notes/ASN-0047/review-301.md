# Review of ASN-0047

## REVISE

### Issue 1: J4 fork range bound is weaker than the version-copy semantics it claims
**ASN-0047, J4 (Fork composite)**: "(ii) K.μ⁺ populating M'(d_new) from `d_op`'s content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_op)|_{V_{s_C}(d_op)})` … This matches Nelson's CREATENEWVERSION, which copies the contents of whatever document it is invoked on (LM 4/66, 'the contents of document `<doc id>`')".

**Problem**: J4's allocation discipline confines `d_new` to `d_src`'s version chain `A_v(d_src)` with `d_src ≼ d_new` — i.e. exactly CREATENEWVERSION, which copies *all* source contents (Gregory's `docreatenewversion` reads the full POOM). But the only constraint on the forked arrangement is `⊆`, which admits a "version" that silently drops source content — directly contradicting "copies the contents of document `<doc id>`." The worked examples all achieve range *equality* (`ran(M'(d₃)) = {a₁,a₂,a₃}` = full `d₂`), but nothing in J4 requires it. Compounding this, the V-position depth and positions are independently free ("d₂'s own free choice ≥ 2 … the transclusion copies d₁'s I-addresses, not its V-position depths"), so a J4-valid fork need not resemble its source's arrangement at all. Finally, **Open Question 1** ("must it be identical, or may it be a proper subset?") poses as open precisely what J4 has already decided with `⊆` — an internal inconsistency.

**Required**: Either (a) tighten the version-fork to require content-subspace range equality `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` (resolving and removing OQ1), or (b) drop the CREATENEWVERSION full-copy fidelity claim, state explicitly that J4 also subsumes partial-copy split/extract, and retitle it from "Fork composite" to a general new-document-with-transclusion composite. The current text asserts (a)'s semantics while specifying (b)'s constraint.

### Issue 2: Class (a) matrix S3★/K.μ~ cell is essay-length, re-deriving rather than indexing
**ASN-0047, Class (a) verification matrix, S3★ row, K.μ~ column**: "elementary decomposition K.μ⁻+K.μ⁺ (this row's restriction + amendment Class (a) cells); realisable π are exactly the admissible ones — subspace-preserving (K.μ⁺ content-subspace precondition) and link-subspace fixing (clause (v)); the realisation establishes S3★(Σ') by **K.μ~-S3★**."

**Problem**: The matrix preamble states "each cell summarises the load-bearing argument," and every neighbouring cell is a short pointer ("restriction", "frame", "precondition: …"). This cell instead restates the conclusion of Step (A) (π is subspace-preserving and link-fixing) and Step (B) (S3★(Σ') established) inline — meta-prose occupying a structural slot, the navigational-index value lost. It is the same content as Step (A)/(B) in different words.

**Required**: Reduce the cell to a citation, e.g. "K.μ~-S3★ (Decomposition, Step (B))." The derivation already lives in the body; the matrix should index it.

### Issue 3: FrontierEquivalence is re-glossed at every invocation
**ASN-0047, K.δ box and both worked examples**: the parenthetical "FrontierEquivalence (the derived form of T10a's chain-advancement uniqueness at `(t,0)`)" recurs — entity-hierarchy example Step 4: "discharged by … FrontierEquivalence (the derived form of T10a's chain-advancement uniqueness at (d₂,0))"; subsequent-version fork: "discharged via FrontierEquivalence (the derived form of T10a's chain-advancement uniqueness at (d₂, 0))"; plus the K.δ box's "FrontierEquivalence … characterizes it as the condition that `t` is the frontier."

**Problem**: FrontierEquivalence is stated and proved in full as a named lemma. The repeated inline gloss restating *what it is* at each use site is accretion — the precise reader who knows the lemma must skip past the re-explanation. This matches the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier flags. The same accretion appears as a deferral chain for K.δ case (ii): the K.δ box forward-points to "§K.δ case (ii) discharge and parent-allocator activation," which in turn defers per-k identification to ParentAllocatorDispatch.

**Required**: Cite FrontierEquivalence by name at each use site without the repeated definitional parenthetical. Consolidate the K.δ case (ii) discharge so a single location owns the per-k parent-allocator identification rather than three sections each restating part of it.

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
**Why out of scope**: Whether link/content allocation must be serialized under contention is genuinely new territory (the SequentialTransitionAxiom already totally orders transitions); it is correctly deferred to an Open Question, not a defect of this ASN.

### Topic 2: Renumbering-aware interior arrangement contraction
**Why out of scope**: K.μ⁻'s suffix-only contraction faithfully models the gap-free POOM for suffix deletion; interior `DELETEVSPAN` compaction is operation-semantics territory (operations are explicitly out of scope) and is already flagged as an Open Question.

VERDICT: REVISE
