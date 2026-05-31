# Review of ASN-0084

This ASN is mathematically careful. I checked the postcondition well-definedness lemmas (R-PIV, R-SWP), the permutation bijectivity arguments (R-PPERM, R-SPERM), the shift-commutativity lemma (R-COMM), the run-transformation (R-BLK), and the canonicity argument (R-CANON), including boundary cases (empty exteriors, minimum widths, the three μ-displacement sub-cases, and a non-S subspace). The five worked examples correctly exercise distinct branches and the arithmetic checks out. The core findings are accreted meta-prose, which the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: Local-vs-global maximality stated three times across two sections
**ASN-0084, R-BLK closing + R-CANON preamble**: R-BLK first states the operative fact — "B′ is therefore not necessarily maximal." — then immediately restates it editorially: "R-BLK delivers a partition that is disjoint, covering, and consistent, but explicitly *not* claimed maximal: mergeable-pair-freeness is a *local* property of adjacent pairs, whereas canonicity is the *global* maximality of S8." R-CANON's preamble then previews the same distinction a third time: "We must reconcile two notions of 'no more structure to extract.' Merge (above) is a local rewrite ... S8's maximality is a global property of a run ..."
**Problem**: The local/global framing is the content of R-CANON's proof (it shows the local merge-freeness condition coincides with global maximality). Stating it twice more as editorial preamble is exactly the "two paragraphs in different sections say the same thing" accretion pattern. The reader must skip past it to reach the actual argument.
**Required**: Keep the factual "B′ is not necessarily maximal (see R-CANON)" once in R-BLK. Delete the editorial restatement paragraph in R-BLK and the "We must reconcile two notions" preamble in R-CANON; let the R-CANON proof carry the distinction.

### Issue 2: Downstream use-site inventory in the termination paragraph
**ASN-0084, R-CANON "Termination and confluence of merging"**: "Each worked example below verifies the R-CANON hypothesis by its *merge check* — exhibiting that the displayed partition has no mergeable adjacent pair — and the resulting partition is canonical by R-CANON."
**Problem**: This is a forward inventory of downstream consumers (the worked examples) rather than content advancing the termination/confluence argument. Each worked example already labels and performs its own merge check; the inventory adds nothing the examples don't state at their own site.
**Required**: Delete the sentence. The termination/confluence claim stands on the strictly-decreasing run count and R-CANON alone.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition characterization of REARRANGE_K
The ASN proves every ASN-0036 invariant is preserved but never computes a wp for a non-trivial post-state guarantee (it is listed as Open Question 5). The framing there — what R-PRE(iv) adds beyond D-SEQ — is genuine: R-PRE(iv) forces `c_{n−1} ≤ [S, N+1]`, a constraint D-SEQ does not supply, so the question is non-trivial and legitimately future work, not a defect here.

### Topic 2: k-cut generalization (k > 4) and composition of rearrangements
The displacement/region machinery is stated only for n ∈ {3, 4} (CS1). Whether it generalizes, and whether composed rearrangements stay within the class, is new territory (Open Questions 1–2), not an error in this ASN.

VERDICT: REVISE
