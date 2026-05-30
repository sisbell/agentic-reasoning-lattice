# Review of ASN-0084

## REVISE

### Issue 1: Post-state S8 (canonical/maximal decomposition) discharge stated three times

**ASN-0084, "Correspondence-Run Decomposition Transformation" (Canonical decomposition paragraph)**: "Foundation S8 (CorrespondenceRunPartition, ASN-0036) supplies this maximal-run partition and its uniqueness for any arrangement satisfying the ASN-0036 invariants, the post-state M'(d) among them."

**Problem**: The identical fact — foundation S8 supplies the maximal-run partition + uniqueness for M'(d) — is asserted in three separate places: (1) the Invariant-preservation audit's *Post-state S8 discharge* ("foundation S8 (ASN-0036) applies to M'(d) directly: it supplies the post-state maximal correspondence-run partition and its uniqueness"); (2) the *Canonical decomposition* paragraph quoted above; (3) R-BLK's closing ("The existence and uniqueness of the post-state maximal ... decomposition is the post-state S8 discharge recorded in the Invariant-preservation audit above"). The audit is the load-bearing derivation; the *Canonical decomposition* paragraph re-derives it rather than pointing to it. This is the "multiple paragraphs deferring to / restating the same downstream fact" accretion pattern.

**Required**: Let the *Canonical decomposition* paragraph *define* the canonical (maximal) decomposition and reference the audit's discharge; drop its independent re-assertion that S8 supplies it for M'(d). Keep one derivation (the audit) and pointers elsewhere.

### Issue 2: Worked-example introductions carry use-site/coverage inventories

**ASN-0084, "Worked Example: 3-Cut Pivot with a Non-S (Link-Subspace) Position"**: "The five preceding examples all have `dom(M(d))` confined to the text subspace, so they never exercise the non-S pass-through machinery — R-NS(NS-π), R-FRAME-P(a), R-BLK's verbatim carry of non-S runs, and the cross-group S8-uniq disjointness invoking T10 (ASN-0034)."

**Problem**: This (and the analogous openers of the w_β<w_α and boundary examples — "The preceding 4-cut examples exercise the μ-displacement branches in...", "The four preceding examples illustrate typical configurations...") is a coverage inventory enumerating which lemmas prior examples did or did not exercise. The example's *content* (the trace) advances the argument; the cross-example bookkeeping does not — the reader must skip it to reach the verification. This is the "use-site inventory" pattern the anti-bloat mode flags.

**Required**: Reduce each example opener to a one-line statement of the configuration it traces (e.g., "A 3-cut pivot whose arrangement also references the link subspace"). Drop the enumeration of which machinery the prior examples left latent.

## OUT_OF_SCOPE

### Topic 1: Whether iterated Merge reaches the S8-unique canonical partition
**Why out of scope**: R-BLK produces a valid but possibly non-maximal B'; the termination/confluence of Merge toward the canonical decomposition is correctly deferred to the Open Questions, not an error here.

### Topic 2: Composition of multiple rearrangements; k>4 cuts; m_1>2 depth
**Why out of scope**: Each is explicitly excluded by scope (depth-2, n∈{3,4}) or listed as an open question; new territory, not a defect in this ASN.

The mathematics is sound: R-PIV/R-SWP totality, R-PPERM/R-SPERM bijectivity (finite-set self-injection), R-COMM region-commutativity, R-BLK split/classify/reassemble, and all six worked traces verify correctly against their postconditions, including the three μ sub-cases and both empty-exterior boundaries. The findings are accretion, not correctness.

VERDICT: REVISE
