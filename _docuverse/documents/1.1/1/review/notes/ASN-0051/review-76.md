# Review of ASN-0051

## REVISE

I read this ASN closely against Dijkstra's standards — explicit proofs, all cases dispatched, no proof-by-similarly, edge cases handled, foundation citations rather than reinvention. The work is unusually rigorous; nearly every place I tried to find slip, the proof had already handled it (Sub-claim (ii)'s case (1) t=s explicitly handles the boundary case #t=k; the structural lemma at SV11 disjoint-pair case (b) exhaustively partitions the y-space; the witness shapes W(m, p) carry verifications for the SV11 attainment biconditional at every link). The few items below are presentational and verifiability concerns, not correctness defects.

### Issue 1: SV13 clause (i) bundles four distinct system-level facts

**ASN-0051, SV13(i)**: The clause combines L-frame discovery invariance (SV7), K.λ monotonicity (SV9), discovery/projection independence (SV10 + CrossDocumentDecoupling), and document-derived non-permanence (SV14) into a single prose block.

**Problem**: Each sub-claim is independently citeable downstream and warrants its own anchor. As written, a downstream consumer wanting to cite "discovery permanence under L-frame" cannot point to a labelled fragment within (i); they must cite the whole clause and have the reader sort the four points.

**Required**: Split (i) into four sub-bullets matching the prose paragraphs, or break out the four sub-points as (i₁)–(i₄) at the same indent level as (a)–(h).

### Issue 2: The W(2, 2) explicit witness is structurally orphaned from the lift family

**ASN-0051, SV11 multi-block (p ≥ 2) attainment, W(2, 2) construction and the "Relationship to the W(m, 2) shape template" paragraph**: Two distinct W(2, 2) witnesses are described — the explicit multi-element-span one (block sizes 10, 5; two spans of widths 7 and 2) and the shape-template one at m=2 (block sizes 8, 3; two single-element spans). The ASN keeps the explicit multi-element-span witness "for shape diversity in the witness catalogue rather than because the (α_2) recipe is structurally undefined at m = 2", and (α_2)'s base is W(3, 2), not W(2, 2).

**Problem**: A reader following the lift schema looks for a uniform witness family. The explicit W(2, 2) follows a different shape than W(3, 2), W(4, 2), …, and the prose footnote tries to reconcile them after the fact. The reconciliation is correct but adds cognitive load.

**Required**: Either replace the explicit W(2, 2) with the shape-template instance (sizes 8, 3 with single-element spans) so the witness family is uniform from m=2 upward, or drop the W(2, 2) shape-template detour and present only the explicit multi-element-span witness with a one-line note that the (α_2) lift starts at W(3, 2) by choice of base.

### Issue 3: Cross-origin exclusion subsection in the Worked Example uses tumblers disjoint from the rest of the example

**ASN-0051, Worked Example, "Cross-origin exclusion (SV6)" subsection**: This subsection introduces s = 1.0.1.0.1.0.1.2.3 (9 components), ℓ = 0.0.0.0.0.0.0.0.5, t, and b that share no values with the a₁..a₅ used throughout the rest of the Worked Example.

**Problem**: The worked-example reader expects continuity. The cross-origin subsection is a fresh verification with no shared tumblers, but it's titled and positioned as if it continues the example. A reader scrolling through expects the values to relate; they don't.

**Required**: Either rebuild the cross-origin verification on the worked-example's existing tumblers (e.g., construct an explicit b under a different document prefix and verify b ∉ ⟦(s_link, ℓ_link)⟧ for the worked example's link), or move the standalone verification into a separate subsection clearly titled "Standalone SV6 verification with explicit tumbler arithmetic" so the change of values is signalled.

### Issue 4: The "degenerate" After-reordering subcase in the Worked Example is acknowledged but not removed

**ASN-0051, Worked Example, "After reordering" subsection followed by "Reordering that changes locate"**: The first subsection swaps v₂ and v₃, both inside the locate set, and the prose explicitly tags this as "degenerate w.r.t. demonstrating the SV5 locate-set-change behaviour" with a "Degeneracy note". The second subsection then exhibits the strict locate-set-change case.

**Problem**: The first subsection is documented to add no information beyond what the second carries. Keeping both subsections — with the first labelled as not demonstrating what it appears to demonstrate — costs reader attention without paying it back.

**Required**: Either remove the degenerate "After reordering" subsection entirely (the "Reordering that changes locate" subsection alone exhibits both SV5's π-invariance and SV5b's locate-transformation), or fold them into a single subsection that first establishes π-invariance via the non-degenerate swap and notes the within-locate-set swap as a one-line observation.

### Issue 5: The W(1, p ≥ 4) construction recipe contains two schedules and the relationship is ambiguous

**ASN-0051, SV11 "(m = 1, p ≥ 4)" generalisation**: The explicit (m=1, p=4) construction uses an excision schedule producing block sizes [2, 2, 1, 1]. The "offset-1 schedule" for arbitrary p≥5 produces [1, 1, …, 1, 3]. The note clarifies "both schedules satisfy the size-≥3 invariant".

**Problem**: At p=4 the explicit construction does not use the offset-1 schedule, so the inductive recipe presented for p≥5 has no base case explicitly demonstrated using it. The reader has to verify offset-1 termination correctness at p=4 independently — and the explicit p=4 construction (which does terminate) uses a different schedule, so it doesn't serve as the offset-1 base case.

**Required**: Either rewrite the explicit (m=1, p=4) construction to use the offset-1 schedule (yielding sizes [1, 1, 1, 3] at p=4), making it the explicit base case of the inductive offset-1 family; or state explicitly that for each p≥4 the construction is independent from Σ₀ (which is already the framing), and present the offset-1 schedule as one recipe among possibly several, dropping the "for p ≥ 5 the recipe extends" inductive framing.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link survivability (|Σ.L(a)| > 3)

**Why out of scope**: ASN-0043's L3 admits arity ≥ 3, but this ASN's "Scoping note" explicitly restricts to the standard triple. The generalisation is mechanical (slot-wise application of SV2–SV5), and the ASN is right to defer it. The "Properties Introduced" table records the scope restriction.

### Topic 2: Link-subspace contribution to projection (links whose endsets reference link addresses, L13)

**Why out of scope**: SV11 operates on π_text(e, d), with the note that link-subspace contributions are deferred to the Link Subspace ASN. This is a deliberate scoping choice — handling reflexive addressing requires the Link Subspace ASN's machinery and would expand SV11 substantially without changing the partial-survival result for the content-subspace.

### Topic 3: Broader-level span survivability (k ≤ p₃)

**Why out of scope**: SV6 is explicitly element-level (k > p₃). Broader-level spans — those whose action point sits at or before the third field separator — admit open coverage growth by design (Nelson's "A span that contains nothing today may at a later time contain a million documents"). The ASN scope-limits to element-level and notes the deferral to ASN-0034's allocator and address-hierarchy treatment.

VERDICT: REVISE
