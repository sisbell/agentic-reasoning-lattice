# Review of ASN-0084

I checked the five region-permutation lemmas (R-PIV, R-SWP, R-PPERM, R-SPERM), the run-decomposition transformation (R-BLK, R-COMM), the boundary handling (EXT-VAC), and all five worked examples against the foundation contracts. The arithmetic, the bijection constructions, the tiling identities, and the invariant-preservation audit are sound — I found no correctness, boundary, or completeness gaps. The depth-2 confinement of subspace S, the empty-exterior cases, both μ-displacement directions, the w_α = w_β fixed-μ case, and the non-S pass-through are each traced explicitly. The findings below are the meta-prose / accretion patterns the active `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Tiling of [c₀, c₃) is proved twice

**ASN-0084, "Reduction of compound shifts" (after REARRANGE_K) and R-SWP, clause (a) Exhaustiveness**: The paragraph beginning "We must verify that the clauses cover [c₀, c₃) without overlap... so the three ranges tile [c₀, c₃) exactly" duplicates R-SWP's "Exhaustiveness: the union of R-S1, R-S2, R-S3 covers ordinals [p, p + w_β + w_μ + w_α)... So the union of all four clauses covers V_S(d)."

**Problem**: The same tiling fact — that R-S1/R-S2/R-S3 exactly partition [c₀, c₃) via `ord(c₀) + w_β + w_μ + w_α = ord(c₃)` — is established in two places. The version attached to the operation definition pre-proves a result that R-SWP (the well-definedness lemma where it is actually consumed) re-proves in full. This is the "two paragraphs in the same document say the same thing in different words" pattern; the reader must reconcile the two before trusting either.

**Required**: Delete the tiling verification from the post-REARRANGE_K "Reduction of compound shifts" block and let R-SWP carry it. Keep only the left-associativity reading of the compound shifts there (the part R-SWP cites), not the coverage argument.

### Issue 2: Front-loaded depth-invariance justification with downstream-consumer pointer

**ASN-0084, "Correspondence-Run Decomposition Transformation," opening run-convention paragraph**: "...the underlying TS3 (ShiftComposition, ASN-0034) instance behind Extended Associativity holds for any tumbler v ∈ T irrespective of depth, so that identity transfers unchanged to the I-address arithmetic in Split and Merge below."

**Problem**: The depth-invariance step is load-bearing only inside Split and Merge (where `(a+c)+k = a+(c+k)` is applied to depth-8 I-addresses). Stating it up front, with the forward enumeration "in Split and Merge below," is the "definition's introduction enumerates downstream consumers" accretion pattern — the reader meets a justification for a step that has not yet appeared.

**Required**: Move the "TS3 holds at any depth" justification into Split and Merge at the point each applies Extended Associativity to I-addresses; in the section opener, retain only the fact that `+` on I-addresses denotes `shift`.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The Open Questions correctly defer the general k-cut permutation class; this ASN fixes n ∈ {3, 4} by CS1 and proves exactly those two.

### Topic 2: Composition of successive rearrangements
**Why out of scope**: Whether two REARRANGE_K compose into one is new territory — this ASN specifies a single operation's postcondition, not the algebra of the operation set.

### Topic 3: Operational recovery of the canonical partition from B′
**Why out of scope**: R-BLK honestly delivers a *valid but possibly non-maximal* B′ and the worked 4-cut example exhibits a mergeable pair; iterated-merge termination/confluence is a separate result.

### Topic 4: Weakest precondition for the full post-state invariant suite
**Why out of scope**: The wp question (and what R-PRE(iv) adds beyond D-SEQ) is explicitly posed as future work; the ASN establishes the postconditions without computing wp.

VERDICT: REVISE
