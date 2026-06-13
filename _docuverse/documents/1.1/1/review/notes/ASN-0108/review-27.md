# Review of ASN-0108

The mathematics here is sound. I checked the wp derivations (W2), the partition induction (W4), the iff of coherence (W5), the multiplicity-charge termination argument (W9b), and all four termination walks (W9d) — each holds, including the boundary cases (`m=0`, `N>m`, exact multiple). The remaining findings are the residual meta-prose the `anti-bloat` classifier is reacting to, plus one internal inconsistency in a boundary walk. Substance has converged; what remains is trimming.

## REVISE

### Issue 1: W5 states the resurrection/inflow aside twice and over-explains clause 1's already-excluded cases
**ASN-0108, W5 (OrderStability)**: The claim block says
> "*Symmetrically on the re-delivery side:* a link that left `Match` and re-entered ... is re-delivered, but it does *not* match across the transition that resurrects it ... so clause 1 is silent on it and its re-entry is no coherence breach; it is the W9b cumulative-inflow phenomenon..."

and then the follow-up paragraph ("Clause 1 is exactly the requirement.") says the same thing again:
> "(a delivered link that instead *left* `Match` and *resurrected* above the cursor is re-delivered too, but lies outside clause 1's both-states scope — the W9b inflow case, not a coherence breach)"

**Problem**: Two paragraphs in the same claim assert the identical point in different words. More broadly, clause 1's quantifier ("for every `a` matching in both states") *already* excludes newly-created and resurrected links; the claim block then spends several sentences explaining that these excluded cases are handled elsewhere (W6 blind spot, W9b inflow, D-ZERO present-tense), and the follow-up re-states the resurrection half. This is defensive elaboration of cases the precondition's scope already rules out — the reader must work past it to reach the skip/duplicate derivation that is the actual content.
**Required**: State the both-states scoping once (one sentence: the scope excludes newly-created matchers → W6 and resurrected matchers → W9b, neither a coherence concern). Drop the follow-up paragraph's resurrection parenthetical, since the claim block already scoped it out.

### Issue 2: The "ladder of key conditions" carries use-site inventory and pre-states W8's conclusion
**ASN-0108, "A ladder of key conditions"**:
> "Five conditions on the key recur below, and keeping them distinct is exactly what stops the order-stability question (W5) from being conflated with cursor-survival (W8) and termination (W9)."

and
> "Each one's logical role is fixed where it is used — coherence at W5, termination at W9c/W9d — so the ladder only places them in this family rather than re-tagging them."

**Problem**: Both sentences are downstream-consumer enumeration / use-site inventory — they describe *where* the conditions get used and *what the ladder does* (places them in a family), rather than advancing the conditions' meaning. Additionally, the ladder's closing sentence —
> "So cursor-survival-under-orphaning (W8) is delivered by **value-totality**, not by state-stability: state-stability constrains only surviving/matching links and is silent on an orphaned cursor's key."

— pre-states the exact conclusion W8 then establishes ("What makes κ(c) computable through the disappearance of c is **value-totality** (the ladder above), *not* state-stability..."). The point is made twice.
**Required**: Keep the term *definitions* (computability, value-totality) and the converse-failure example (state-stable-but-not-value-total content key) — those are load-bearing and used downstream. Cut the use-site inventory sentences and the sentence that pre-states the W8 conclusion; let W8 own it.

### Issue 3: W9 restates the computability-vs-clause-1 distinction three times within W9/W9b
**ASN-0108, W9 / W9b**: The distinction is stated at the W9 opening ("'Recoverable' (computability) and 'cut-point preserved' (clause 1) are *not* the same condition, and W9 needs both, named distinctly"), restated at the W9 closing ("...the two must be kept distinct"), and restated again in W9b's condition (i) parenthetical ("this is the everything-delivered proviso W9's global reading isolates, *distinct* from the single-state computability its local fact needs").
**Problem**: The distinction is correct and important, but the closing recap duplicates the opening, and W9b(i)'s parenthetical re-explains it in a third place. A reader following the local-fact derivation has to absorb the same caveat three times.
**Required**: State it once (the opening, where the local/global split is introduced and the W5 walk serves as witness). Drop the closing recap and trim W9b(i)'s parenthetical to a bare cross-reference.

### Issue 4: The `m=0` walk says "zero windows" but the reader receives one (empty) window
**ASN-0108, W9d walks (empty matching set case)**: "The loop stops on this first call. Total **1 call** ... W4's partition holds vacuously: the empty union of zero windows is `M = ∅`, with no rank delivered."
**Problem**: This is internally inconsistent with its own framing. The reader makes **1 call**, which delivers `W_0 = ∅` — W4 calls this a window ("the successive windows `W_0, W_1, …`"), and it is the short window that signals exhaustion. So there is one (empty) window, not "zero windows." The conflation is between "windows delivered by calls" (one, empty) and "parts of the partition of `M`" (zero, since a partition has no empty parts).
**Required**: Reword to "the single empty window `W_0` is delivered; its union is `∅ = M`, no rank delivered" — consistent with the "1 call" tally and with W4's own use of `W_0`.

## OUT_OF_SCOPE

### Topic 1: Multi-document enumeration discipline and progress/cardinality correspondence
**Why out of scope**: The address key's allocation-monotonicity holds only within a single home document (correctly hedged at W6, T9), and the front-end "k of m" display depends on a companion cardinality query (W10). Both are correctly deferred — to Open Question 1 and Open Question 5 respectively — and belong to future ASNs, not this one.

### Topic 2: Count-only and full-set retrieval, MAKELINK
**Why out of scope**: Per the scope exclusions. The ASN does not define claims for these — it defers the cardinality query at W10 ("a distinct operation, out of scope here"), imports `Match` from `findlinks_V` rather than defining full-set retrieval, and uses K.λ's existing contract for the creation-inflow mechanism (W6, W9b) without redefining MAKELINK. No scope violation.

VERDICT: REVISE
