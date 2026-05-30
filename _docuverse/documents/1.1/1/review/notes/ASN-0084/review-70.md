# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 contains reviser-drift framing and duplicated content
**ASN-0084, "Necessity of CS3" / R-CS3 proof, *CS3 is the sole rejecting clause***: "The previously-supposed redundancy of CS3 rested on R-PRE(iv) becoming *unsatisfiable* whenever a cut left subspace 1. That argument holds only when c₀ remains in subspace 1..."
**Problem**: This paragraph is framed as a rebuttal to a prior review's hypothesis ("previously-supposed redundancy," "That argument holds only when") rather than advancing the lemma. Worse, its technical content — that a higher-subspace c₀ makes R-PRE(iv) vacuous rather than contradictory — is already stated verbatim in the section intro ("The discriminating case is a cut sequence whose *first* cut c₀ already lies above the entire subspace-1 range: then R-PRE(iv) is satisfied vacuously rather than violated"). Two paragraphs state the same discriminating insight in different words, one of them as a refutation of a refuted claim.
**Required**: Delete the "previously-supposed redundancy" rebuttal paragraph. The counterexample paragraph plus the section intro already establish independence affirmatively; the rebuttal adds nothing the reader needs and forces them to re-parse a hypothesis the ASN does not hold.

### Issue 2: Local-label scaffolding around NS-run is meta-prose the reader must work around
**ASN-0084, R-BLK, *Non-S runs are carried verbatim (NS-run)***: "We name these four facts — V-extent confinement, cut separation, verbatim carry, and post-state consistency — collectively *(NS-run)*."
**Problem**: The four named sub-facts are then cited back ("as recorded by *(NS-run)*, verbatim carry, above") at least four times across Phase 2, Phase 3, and the contiguity/S8-cons paragraphs. The naming apparatus exceeds the reasoning it organizes — each citation requires the reader to jump back, locate the sub-label, and re-read. The non-S case is short (π is the identity there); the bookkeeping is heavier than the argument.
**Required**: Inline the non-S handling where it is used (π = identity ⟹ run unchanged ⟹ S8-cons inherited) and drop the four-fact naming and the repeated back-citations.

### Issue 3: Defensive "valid at j = 0 / without separate treatment" clauses
**ASN-0084, "Reduction of compound shifts" and R-COMM**: e.g. "Extended Associativity holds for all arguments in ℕ, so each step above is valid at j = 0 without separate treatment."
**Problem**: Extended Associativity is defined over ℕ × ℕ including 0; restating "so j = 0 needs no separate treatment" at each use site is defensive meta-prose anticipating an objection the definition already forecloses. The "Reduction of compound shifts" subsection itself re-derives, step by step, reductions that are immediate from the already-stated Extended Associativity identity.
**Required**: State the compound-shift reduction once as a one-line consequence of Extended Associativity; remove the per-site "valid at j = 0" disclaimers.

### Issue 4: Naming-rationale and self-reference prose in the run-decomposition section
**ASN-0084, "Correspondence-Run Decomposition Transformation"**: "To avoid colliding with the foundation's own clause lettering (where S8's postconditions are (a) lockstep consistency, (b) well-defined label, (c) unique decomposition), we name two local labels: *S8-uniq* ... and *S8-cons* ..." and **R-BLK opening**: "R-BLK names both the lemma below and the constructive transformation (B, C, M(d), M'(d)) ↦ B' it specifies."
**Problem**: Both are prose about how labels are assigned rather than content that advances the argument. The S8-uniq/S8-cons relabeling exists only to sidestep a lettering clash; the R-BLK "names both" sentence narrates the lemma's own bookkeeping.
**Required**: Pick label names that do not require a justifying paragraph, and drop the "R-BLK names both…" sentence — the lemma statement and the construction can share the label without comment.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements
**Why out of scope**: Whether two REARRANGE_K applications compose into a single cut-point rearrangement is genuinely new territory and is already correctly deferred to the Open Questions; it is not an error in this ASN.

### Topic 2: Operational recovery of the maximal partition from B′
**Why out of scope**: R-BLK correctly establishes that B′ is valid and that the foundation S8 supplies the maximal decomposition; the *procedure* (and its confluence) for merging B′ to maximal is appropriately listed as an Open Question, not a gap here.

The technical core is sound: the pivot/swap displacement structure (α → +w_β / +w_β+w_μ, β → −w_α / −w_α−w_μ, μ → w_β−w_α), the tiling and disjointness arguments in R-PIV/R-SWP, the bijection proofs in R-PPERM/R-SPERM (self-injection on a finite set), and all five worked examples check out against the postconditions. The remaining issues are accreted meta-prose, not correctness.

VERDICT: REVISE
