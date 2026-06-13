# Review of ASN-0122

I verified the formal content closely: the worked example is arithmetically correct end to end (the relation, the two maximal pairs γ₁/γ₂, the swap tie-break, the window clip, and the self-comparison detector all recompute exactly as stated); X11's partition argument discharges its load-bearing facts (single-valued succ, in-degree ≤ 1 via TS2 under S8-depth, acyclicity via TS4); X10(a) correctly invokes TS4/TS5; X4c's interval-clipping reduction is sound; the X5/X7 division correctly handles reordering (X5 indifference deliberately excludes the reordered document since res|P changes, and X7(i) supplies the transport), so there is no overclaim there; X-T and X6's composition are well-formed; and boundary cases (empty spec-set, empty document, clipped-to-nothing spans, self-comparison, fan-out, n=1 chains, contraction-to-empty) are all covered. The substance is converged.

What remains is the residual forward-reference meta-prose the anti-bloat pass targets.

## REVISE

### Issue 1: Forward-reference editorializing around the kernel definition and in the intro
**ASN-0122, "What 'Correspond' Must Mean" (following the corr definition) and "The Problem"**:
- "The kernel observation does real work: symmetry and transitivity of correspondence are inherited algebra, not properties to design in."
- "We record kernel transitivity now, for the chain theorems: res p = res q and res q = res r give res p = res r — correspondence composes through a shared instance."
- "...Completeness and soundness then become obligations, not aspirations, and every stability property becomes a theorem."

**Problem**: Each of these points downstream (to X3, the chain theorems, the stability section) or editorializes about derivation strategy ("does real work," "not properties to design in," "now, for the chain theorems," "every stability property becomes a theorem") without advancing the local reasoning. The substantive content stands on its own and is used where derived: corr is the kernel of res; the transitivity implication `res p = res q ∧ res q = res r ⟹ res p = res r` is consumed at X6(d); symmetry is X3. The framing is the part a precise reader skips, and it is exactly the "essay content / downstream-consumer / forward-pointer" residue this note is classified to catch.

**Required**: Keep the kernel framing of corr and the transitivity implication itself; delete the editorial and placement framing ("does real work," "not properties to design in," "now, for the chain theorems," "every stability property becomes a theorem"). Let symmetry and transitivity carry their weight at X3 and X6(d) rather than as previews.

## OUT_OF_SCOPE

The ASN's Open Questions correctly defer genuine future territory — n-way alignment composed from pairwise reports, derived correspondence-index/cache consistency across edits, matching-vs-position-level information equivalence, and extension of the subspace vocabulary. These are new ASNs, not defects here, and none is smuggled into the X12 contract as a binding claim. No action needed.

VERDICT: REVISE
