# Review of ASN-0084

I checked the displacement arithmetic, both well-definedness lemmas (R-PIV, R-SWP), the two permutation lemmas (R-PPERM, R-SPERM), R-COMM, the R-BLK transformation, and all six worked examples. The mathematics is sound: the per-region displacements compose correctly, the tiling arguments close, surjectivity-by-finiteness is valid, and the cross-group S8-uniq disjointness is correctly grounded. The OrdShiftHom citations are uniformly (a), consistent with the prior resolution. My findings are confined to the accreted meta-prose the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: The text-subspace scope restriction is restated five times
**ASN-0084, opening + State and Vocabulary**: "REARRANGE is confined to the text subspace (S = 1, depth 2); cross-subspace transposition is outside the scope of this ASN." then "We restrict to the text subspace (subspace identifier 1) throughout this ASN." then "The operations defined here apply only to the text subspace; outside this scope ..., neither the rearrangement postconditions nor the supporting lemmas of this ASN are claimed to apply." then "The text-subspace restriction is deliberate: REARRANGE acts on the text region ... and is not defined as a cross-subspace operation." then "CS3 and CS4 below jointly enforce this scope ...".

**Problem**: One scope fact is asserted five times across the opening and State-and-Vocabulary, twice forward-pointing to CS3/CS4. This is the "two paragraphs say the same thing in different words" anti-bloat pattern at scale; the reader re-encounters the same constraint repeatedly before the cuts are even defined.

**Required**: State the text-subspace/depth-2 scope once. The forward pointers to CS3/CS4 and the "deliberate"/"not a cross-subspace operation" editorializing add nothing the single statement plus the CS3/CS4 clauses do not already carry — delete them.

### Issue 2: Width-positivity prose imagines an excluded case and defers to R-CS3
**ASN-0084, Consequences of R-PRE / Width positivity**: "Were the cuts in a different subspace or depth, this reduction would fail and the V-position count could be 0 while the ordinal difference is positive — precisely the failure R-CS3 below constructs."

**Problem**: At this point CS3 and CS4 are in force (they are R-PRE(iii) preconditions), so cuts in a different subspace or depth are already excluded by the claim's own preconditions. The sentence reasons about a counterfactual the carrier rules out and then forward-points to a downstream lemma to justify itself — both flagged anti-bloat patterns (imagining an excluded case; deferral to a downstream location). The alignment `c_i ≤ v < c_{i+1} ⟺ ord(c_i) ≤ ord(v) < ord(c_{i+1})` follows from CS3+CS4 directly; the counterfactual is not part of that derivation.

**Required**: Delete the counterfactual sentence. The necessity of CS3 is the subject of R-CS3; it does not need to be previewed here.

### Issue 3: Use-site inventories in a definition and in R-NS
**ASN-0084, CanonicalRunDecomposition (DEF)**: "Whenever the worked examples report a 'canonical partition,' they name this S8-unique maximal-run decomposition."
**ASN-0084, R-NS**: "Consequently, since dom(M'(d)) = dom(M(d)) ..., every ASN-0036 invariant that depends only on dom and on M restricted to non-S positions is preserved unchanged on M'(d)."

**Problem**: The CanonicalRunDecomposition definition closes by enumerating where the term will later be used (the worked examples) rather than advancing the definition's meaning — a definition-introduction-as-use-inventory. R-NS's closing sentence restates a generic invariant-preservation claim already discharged by the dedicated "Invariant preservation" audit paragraph; the audit is the load-bearing statement, and R-NS's generality clause duplicates it.

**Required**: Drop the worked-example pointer from the definition (the examples can refer to the definition, not vice versa). In R-NS, keep the pointwise NS-π conclusion and remove the generic "every ASN-0036 invariant ..." sentence, leaving the invariant audit as the single site for that claim.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4, composition of rearrangements, run-count growth bounds
**Why out of scope**: These are correctly deferred to the Open Questions; they are new operational territory, not defects in the 3-/4-cut specification given here.

VERDICT: REVISE
