# Review of ASN-0106

## REVISE

### Issue 1: R0 contradicts R-SPLIT — the full extent is not one block per subspace
**ASN-0106, "What is returned" / Claims (R0)**: "The document-extent instance `read(d, Σ_full)` returns exactly one text block and one link block — the two subspace extents."
**Problem**: This is inconsistent with R-SPLIT, which the same ASN proves: "A requested V-span yields more than one block exactly when its content spans non-contiguous I-regions." The full text V-extent of a transcluded or repeatedly-edited document spans non-contiguous I-regions (different origins, different insertions), so by R-SPLIT and ASN-0058 M16/M14a its maximally-merged decomposition is *several* blocks, not one. R0 holds only for the degenerate case of a never-transcluded, contiguously-typed document. Nelson's "number of characters of text" is a V-*width* (recoverable as a single V-span by D-SEQ contiguity), not a single mapping block — `read` returns blocks, so the canonical reading does not collapse to 1+1 blocks.
**Required**: Either restate R0 in terms of the V-extent span-set (two V-spans whose widths are the character/link counts, independent of I-fragmentation), or acknowledge that `read(d, Σ_full)` yields possibly-many blocks per subspace whose V-widths sum to the count. Reconcile with R-SPLIT explicitly.

### Issue 2: R-GAP assumes V-order but `read` is defined in request order
**ASN-0106, "Gaps and adjacency" (R-GAP)**: "From `read(d, Σ)` one may decide, for each consecutive pair of fragments, whether they abut in the arrangement or are separated…"
**Problem**: `read(d, Σ)` is defined as concatenation "in request order." R-ORDER establishes V-order only "for normalized `Σ`." R-GAP carries no normalization precondition, yet "consecutive pair of fragments" + abutment/separation is only meaningful when consecutive-in-list equals consecutive-in-arrangement. For a non-normalized request, two list-adjacent blocks may be arbitrarily far apart in V-space, and the abutment test (R-GAP) is vacuous or misleading.
**Required**: Add the normalization precondition to R-GAP (as R-FID does), or restate R-GAP over the V-ordered view rather than the request-ordered result list.

### Issue 3: the `read(d, Σ)` definition omits the preconditions its own machinery requires
**ASN-0106, "What is returned"**: "Given a span `σ` over `d`, let `f = M(d)|⟦σ⟧` … By ASN-0058 (C1a, M11, M12) this restriction admits a *unique maximally-merged* block decomposition."
**Problem**: ASN-0058 C1a requires the induced domain `dom(f)` to lie within a single subspace (and inherits level-uniform/depth preconditions). The definition of `read`/`blocks(d, σ)` is stated for an arbitrary requested `σ`; the necessary single-subspace, level-uniform conditions are introduced only later, inside R-FID. If a caller supplies a span crossing the `s_C`/`s_L` boundary, C1a's precondition fails and `blocks(d, σ)` is undefined. A definition that is well-defined only under conditions stated three sections downstream is not yet a definition.
**Required**: Attach the per-span well-formedness precondition (level-uniform, single subspace) to the definition of `read`/`blocks`, not solely to R-FID.

### Issue 4: R-CORR's derivation invokes M14a on the wrong case
**ASN-0106, "Correspondence" (R-CORR)**: "If span `σᵢ` covers one such V-position and `σⱼ` covers the other, then `read(d, Σ)` contains two blocks whose I-extents overlap. By ASN-0058 M14a such blocks *cannot* be merged…"
**Problem**: `read` concatenates per-span decompositions and never merges across spans, so for the cross-span case (`σᵢ` vs `σⱼ`) the survival of both blocks owes nothing to M14a — they were never merge candidates. The case that genuinely *needs* M14a is when both shared V-positions fall within a *single* requested span, where the maximally-merged decomposition would otherwise be tempted to coalesce them. The proof attaches M14a to the case that doesn't use it and omits the case that does.
**Required**: Split the argument: (a) within one span, M14a forbids merging the two shared-I blocks in the maximally-merged decomposition; (b) across spans, the blocks survive trivially because `read` performs no cross-span merge.

### Issue 5: R-EMPTY conflates an ill-formed designation with an inactive-but-well-formed one
**ASN-0106, "The degenerate designation" (R-EMPTY)**: "If `σ` denotes `∅` (the degenerate limit of a span — note ASN-0053 S2: no well-formed span denotes `∅`, so this is a boundary input)…"
**Problem**: Two distinct boundary cases are merged. (i) A span denoting no V-positions at all is *ill-formed* by S2 — it should be rejected as an input, not silently dropped. (ii) A *well-formed* span whose denotation contains positions but where `V_req ∩ ⟦σ⟧ = ∅` (no active arrangement entries) yields the empty restriction — this is the meaningful "contributes nothing" case and the one fidelity should cover. R-EMPTY's phrasing "a span designating no positions" reads as (i) while the intended faithful behavior is (ii).
**Required**: State R-EMPTY over well-formed spans whose requested positions are absent from `dom(M(d))`, and handle ill-formed (S2-violating) spans as a rejected input, not a contributing-nothing fragment.

## OUT_OF_SCOPE

### Topic 1: the overlap contract (set vs. multiset semantics)
**Why out of scope**: The ASN correctly declines to settle the overlapping-`Σ` contract and records it as the principal open question; R-FID is properly scoped to disjoint/normalized `Σ`. This is future territory, not a defect here.

VERDICT: REVISE
