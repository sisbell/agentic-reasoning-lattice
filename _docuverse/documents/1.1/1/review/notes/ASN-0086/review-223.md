# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable carries an unnecessary empty-gap / immediate-successor derivation

**ASN-0086, Lemma CoverageEqualityDecidable**: "A gap `(c_k, c_{k+1})` is empty exactly when `c_{k+1}` is the zero-extension `c_k.0` of `c_k` ... We derive inline from T1 that no tumbler lies strictly between `c_k` and `c_k.0` ... [≈20-line multi-case argument] ... Empty gaps are `∅` in both coverages and are excluded from the comparison."

**Problem**: The empty-gap detection — and the entire inline derivation that `c_k.0` is the immediate T1-successor of `c_k` — does not advance the decidability conclusion. An empty gap is `∅` in *both* coverages (the author states this), so the two coverages can never differ on it and never falsely match on it. The decision procedure works unchanged if the indicator vector is computed over *all* cells (points and gaps alike), including the trivially-`∅` ones; restricting to "non-empty cells" is what forces the detour, and that restriction buys nothing — the cell set is finite either way (`m` points + `m−1` gaps + 2 exterior, all bounded by `[c₁, c_m)` for coverage membership). The long T1 case analysis re-establishes a fact ASN-0034 already discusses (T0(b)/TA5: `t.0` is the immediate successor) and adds reasoning a precise reader must work past to reach the indicator-comparison argument that actually decides the predicate.

**Required**: Drop the empty-gap characterization and its immediate-successor derivation. State that each coverage is constant on every cell (points and gaps), and decide equality by comparing the two indicator vectors over the finitely many cells — empty gaps contribute matching entries automatically.

### Issue 2: Document-referential meta-phrases in structural slots

**ASN-0086, Definition — relational layer**: "Its one discipline commitment, **not stated elsewhere**: the layer never invokes `Emit_K` at a type index `K ~ R` except through the `Nullify` alias..."
**ASN-0086, Weakest-Precondition Analysis (opening)**: "...admit explicit precondition analyses in two operationally-relevant cases **that differ in kind**: Case 1 ... is a sufficient-precondition and load-bearingness analysis, while Case 2 ... is a genuine weakest precondition..."

**Problem**: "not stated elsewhere" is a self-referential claim about the document's organization, not about the object. The wp opening is a roadmap classifying the *kind* of analysis before any analysis appears; the per-case headers ("Case 1 — a sufficient precondition...", "Case 2 — wp(...)") already carry this signal at point of use. Both are meta-prose the reader must read past to reach content.

**Required**: Delete "not stated elsewhere." Compress the wp opening to a single sentence naming the two postconditions analyzed, letting the per-case headers carry the kind-of-analysis distinction.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and binary projections
**Why out of scope**: The Open Questions correctly defer `L_K^{(n)}` for `|Σ.L(a)| > 3` to a future ASN; this note legitimately restricts `L_K` to standard triples and documents that higher-arity links inhabit `dom(Σ.L)` indexing no tuple. New territory, not an error.

### Topic 2: Concurrency/atomicity model for Emit vs. Observe
**Why out of scope**: The consistency model under which `A_K` transitions are observed is genuinely new state-machine territory (the note's `→` is sequential per ASN-0093's SequentialTransitionAxiom). Belongs in a later ASN.

VERDICT: REVISE
