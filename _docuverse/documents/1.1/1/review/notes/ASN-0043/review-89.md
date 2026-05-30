# Review of ASN-0043

## REVISE

### Issue 1: Notation paragraph enumerates a downstream consumer instead of advancing the definition

**ASN-0043, The Link Store ("Notation from ASN-0036")**: "We treat `Σ.M` itself as a partial function over the tumbler space ... and write `dom(Σ.M) = {d ∈ T : Σ.M(d) is defined}` ... **This is the set that S7d (DocumentAllocationDiscipline, ASN-0036) presupposes when asserting that every `d ∈ dom(Σ.M)` is a T10a-allocated node in the system's allocator tree 𝒯.**"

**Problem**: The final sentence does not extend the meaning of `dom(Σ.M)`; it inventories a downstream consumer (S7d) and pre-stages an argument used later in the L9 witness. This is the "definition's introduction enumerates downstream consumers" accretion pattern. The notation `dom(Σ.M)` is fully specified by the set-builder; the S7d clause is reasoning that belongs at the L9 selection step (where it is, in fact, restated).

**Required**: Drop the S7d sentence. The set-builder defines the notation; cite S7d only where the allocator-tree fact is actually used.

### Issue 2: L3 prose develops at length a case the invariant already excludes

**ASN-0043, L3 (NEndsetStructure)**: "Arity-2 'untyped' links are not part of the design — Gregory's implementation admits a relaxation Nelson's design does not: `docreatelink` short-circuits the third-endset insertion when the client passes an empty type specset (`insertendsetsinorgl` and `insertendsetsinspanf` both guard on `threesporglset` being non-NULL ...) ... Where the implementation can store such links via this empty-type-specset short-circuit, the resulting state lies outside this ASN's conforming link store."

**Problem**: L3 already requires `|Σ.L(a)| ≥ 3 ∧ Σ.L(a).e₃ ≠ ∅`. A full paragraph then reconstructs the *excluded* arity-2 / empty-type case and its implementation provenance. This is the "imagines a case the precondition already excludes" pattern. The invariant statement plus a one-line "the implementation can produce non-conforming arity-2 links; these lie outside the conforming store" carries all the content; the function-name-level walkthrough is excess around the axiom.

**Required**: Compress to the single sentence that the implementation can store sub-arity links outside the conforming store. The verb-by-verb account of `docreatelink`'s guard does not advance the invariant.

### Issue 3: The invariant-vs-lemma distinction is explained defensively in two places

**ASN-0043, FSP statement**: "(L11a is the one cross-event claim in this list, not a per-state predicate; FSP 'preserves' it by extending its conclusion to the new event ...)"

**ASN-0043, L11b**: "The derived L-lemmas (L2, L9, L10, L11b, L12a, L12b, L13) are consequences, not preconditions, so a state is not 'checked against' them."

**Problem**: Both passages exist only to defend terminology — what "preserve" means for a cross-event claim, and which labels are invariants versus consequences. Neither advances a proof step; the reader skips both to follow the actual argument. The same conceptual distinction (state-local invariant vs. derived lemma) is litigated in two sections. This is the "new prose explains why a claim is framed as it is, rather than what it says" pattern, compounded by duplication across sections.

**Required**: The enumerated invariant list in FSP and L11b already names exactly which predicates are preserved. Delete both defensive clauses; if a one-time clarification is wanted, state once (e.g., at FSP) that L11a is discharged as a per-event distinctness obligation, and let the L11b list stand without the "consequences, not preconditions" gloss.

### Issue 4: L3 closing sentence restates the conjunct it just stated

**ASN-0043, L3**: "The non-emptiness conjunct `Σ.L(a).e₃ ≠ ∅` excludes arity-3 links `(F, G, ∅)` whose type slot is structurally present but vacuously inhabited: such a link carries no classifying address."

**Problem**: This paraphrases the formal conjunct `Σ.L(a).e₃ ≠ ∅` back into prose without adding constraint — "excludes links whose type slot is empty" is the literal reading of "`e₃ ≠ ∅`". Two statements of the same thing.

**Required**: Drop the sentence, or fold the single substantive phrase ("a non-empty type slot guarantees a classifying address") into the invariant's one-line gloss.

## OUT_OF_SCOPE

### Topic 1: Removal / discoverability of superseded links
**Why out of scope**: L12 correctly defers "how an old link ceases to be discoverable or resolvable" to operations, which are explicitly out of scope. No revision needed; the single deferral is appropriate.

### Topic 2: Global (non-`s_C`-scoped) content disjointness
**Why out of scope**: L0a's scoping to the `s_C`-resident slice is forced by ASN-0036 not fixing a global content-subspace constant. The first Open Question correctly identifies this as a future ASN-0036 revision, not an error here.

VERDICT: REVISE
