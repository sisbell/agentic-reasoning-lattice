# Review of ASN-0075

## REVISE

### Issue 1: Version-fork shorthand carries reviser-drift and a forward reference into the proof

**ASN-0075, D-DISCR ("A second bundling concerns document creation")**: "The second document is not minted through a fresh account: re-running `K.δ(A)` would re-mint an account already in `E`, violating K.δ freshness (`e ∉ E`). Instead the second document `d'` is a version fork `d' = inc(d, 1)` ... The same holds in the worked example below: only `K.δ(d_A)` uses the account-precursor convention, while `d_B = inc(d_A, 1)` is a version fork."

**Problem**: The load-bearing fact is one clause: `d' = inc(d, 1)` (K.δ case (ii), `k = 1`). The surrounding prose imagines and refutes an excluded alternative (re-running `K.δ(A)`, which K.δ freshness already forbids) — the "imagines a case the precondition already excludes" pattern — and then forward-references the worked example to re-assert the same convention. This is accretion around the shorthand, not reasoning that advances the indistinguishability argument.

**Required**: State that the second document is a version fork `d' = inc(d, 1)` and that this needs only `d ∈ E_doc`. Drop the refutation of the re-mint alternative and the forward pointer to the worked example.

### Issue 2: The "Supplementary lemma (R-disjointness implies Q0)" is untracked and scatters the emptiness analysis

**ASN-0075, SHOWDELETIONS section**: "*Supplementary lemma (R-disjointness implies Q0 at composite-boundary states).* Documents with disjoint `R`-projections on the content subspace ... satisfy `Q0` ..."

**Problem**: This is a fully-proved derived result (three-group case analysis) but appears in no row of the Claims Introduced table, unlike every other result in the note. It also overlaps the existing emptiness treatments: `wp(SHOWDELETIONS, Q0)` gives the general empty-report condition, the edge case "Documents with no shared content" defers to that wp, and "Both arrangements empty" handles a special case. The reader now meets the "when is the report empty" question in four scattered places with three different framings, one of them unlabeled and untracked.

**Required**: Either promote it to a labeled, table-tracked claim (it does add a genuine sufficient condition not given by the `wp(Q0)` formula), or fold the R-disjointness sufficient condition into the `wp(Q0)` derivation so the emptiness analysis lives in one place. Make the edge-case pointers reference that single location.

### Issue 3: Defensive axiom-non-use commentary in D-NEED

**ASN-0075, D-NEED**: "This step consults `R`-membership only; it does not invoke `P4★`, so the discrimination holds at every reachable state, not merely at composite boundaries."

**Problem**: The clause explaining which axiom is *not* invoked is defensive scaffolding rather than a step in the argument. The substantive content — testing `(a, d) ∈ R` distinguishes the two predicates by their definitions — is already complete in the preceding sentence; the scope strengthening can be stated without narrating the absence of `P4★`.

**Required**: Replace with a direct statement that R-membership distinguishes DELETED from NEVER_INCLUDED definitionally, hence at any reachable state. Drop the "does not invoke P4★" narration.

## OUT_OF_SCOPE

### Topic 1: Restoration operation consuming SHOWDELETIONS output
The final open question (a restoration operation reintroducing deleted content while preserving origin and link-resolvability) is correctly posed as future work — it defines a new operation, not a guarantee of this one.

### Topic 2: Multi-document and concurrent-snapshot generalizations
Generalization beyond the binary pair and the concurrency consistency model are appropriately deferred; they require new witness structure and a transition-concurrency model this ASN does not introduce.

VERDICT: REVISE
