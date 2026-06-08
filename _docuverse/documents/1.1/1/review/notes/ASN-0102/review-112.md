# Review of ASN-0102

The arithmetic core is sound. I checked the X16 tiling (`[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W] = [1,n_S+W]` under `1 ≤ p ≤ n_S+1`), the wp(COPY, S3★) reduction, the J1★/J1'★ case split, the S8a inheritance for copied/displaced positions, and the full `ExtendedReachableStateInvariants` discharge. Boundary cases (empty subspace, append, self-transclusion with overlapping source, cross-origin) are all covered, several with concrete worked examples. The invariant coverage is complete and the proofs hold.

The findings are confined to the residual meta-prose this note's anti-bloat classifier targets.

## REVISE

### Issue 1: Defensive methodology prose in the P4a discharge
**ASN-0102, X17 (P4a paragraph)**: "We discharge P4a parametrically, as one operation-preservation step in the reachability induction — *not by claiming anything about all traces to the state value Σ'*." and "We do *not* assert that every trace reaching the state value Σ' passes through this Σ; the universal-over-traces form of P4a follows from the reachability induction over all valid traces, in which each trace's final transition is discharged by its own preservation step — this COPY step being one such."
**Problem**: These clauses explain what the proof is *not* doing rather than advancing it. The inductive framing is standard for a preservation step; stating the COPY-terminated-trace argument is sufficient. The "not by claiming…" and "We do not assert…" sentences are defensive justification of methodology — exactly the noise the precise reader must skip past. The substantive content (carried pairs witnessed by IH on the prefix, recorded pairs witnessed at Σ') stands on its own.
**Required**: Delete the two defensive clauses; keep only the per-step witnessing argument.

### Issue 2: P3 restated after it is already discharged conjunct-by-conjunct
**ASN-0102, X17 (final P3 paragraph)**: "Of COPY's two mutated components (Definition), R changes by extension only (R ⊆ R'), so M is the only component that can *contract or lose information*, which is exactly what P3 guarantees."
**Problem**: P3 is discharged immediately above, conjunct by conjunct, directly from the frame. This trailing sentence re-explains P3's significance ("M is the only component that can contract") — essay content in a structural slot, restating the guarantee rather than establishing it. It adds no inference.
**Required**: Remove the restatement; the conjunct-by-conjunct discharge is complete without it.

### Issue 3: Design-rationale aside in X15
**ASN-0102, X15 (non-displacing-case paragraph)**: "In the append (`p = n_S+1`) and empty-subspace (`n_S = 0`) cases COPY coincides with a contiguous extension expressible as a valid composite, so the elementary-transition model is a uniform *choice*, not forced."
**Problem**: The substantive, valuable result in X15 is that atomicity is *forced* in the displacing case (no decomposition survives the per-state invariants). The non-displacing discussion justifies a modeling decision — why define COPY as elementary even where it is decomposable — which is rationale, not a system guarantee. The single claim worth keeping (non-displacing COPY is expressible as a valid composite) can be stated in one line without the "uniform choice, not forced" editorializing and the "the obstruction is different and worth stating precisely" meta-commentary in the displacing paragraph.
**Required**: Compress to the forced-atomicity result plus a one-line statement that the non-displacing cases are also composite-expressible; drop the choice-vs-forced framing and the meta-commentary.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after subsequent displacement
**Why out of scope**: The first open question (origin-to-discoverability tie under later displacement) is genuinely future territory — it depends on link-projection behavior across further operations, not on COPY's own postconditions.

### Topic 2: Transitive provenance when a by-reference document is itself a source
**Why out of scope**: The second open question concerns provenance composition across chained references, which belongs to a later note on provenance algebra, not to COPY's effect clause.

VERDICT: REVISE
