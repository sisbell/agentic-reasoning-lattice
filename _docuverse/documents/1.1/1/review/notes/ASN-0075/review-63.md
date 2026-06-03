# Review of ASN-0075

## REVISE

### Issue 1: wp analysis is load-bearing on D-OBS, which is proven later
**ASN-0075, "The SHOWDELETIONS Operation" (wp paragraph)**: "Because the operation reads state and writes none (D-OBS, below), wp computations for state-level predicates pass through unchanged from the pre-state: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)` whenever `P` depends only on `Σ`."
**Problem**: The general wp rule — and the Q0/Q1 derivations that depend on it — is justified entirely by observationality, but D-OBS is not established until the "Observational Frame" section several sections downstream. The argument that "post-state = pre-state, so P holds after iff P holds before" cannot be made until the no-write fact is in hand. This is a forward dependency: the reasoning consumes a result that has not yet been proven.
**Required**: Establish the no-write fact (D-OBS) before the wp analysis, or relocate the wp section after the Observational Frame. A bare "(D-OBS, below)" pointer is not a substitute for having the premise in scope at the point of use.

### Issue 2: Meta-prose preambles motivate lemmas rather than advance them
**ASN-0075, before Lemma D-WIT**: "We isolate the inference that recurs throughout this note: a content-store address found in a document's current arrangement must have a provenance record."
**ASN-0075, before Lemma D-EXH**: "We must show these are exhaustive and mutually exclusive — otherwise the operation's outputs would have undefined classifications."
**Problem**: Both sentences explain *why* the following lemma is wanted (it "recurs throughout this note"; results would otherwise be "undefined") rather than stating content. The first is a use-site preview; the second is an exhaustiveness-motivation claim. Under the anti-bloat classifier these are the accretion patterns to remove at source — the lemma statements themselves carry their own justification.
**Required**: Delete the preambles (the lemma names and statements stand on their own), or fold any necessary qualification into the lemma statement.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (Vstream) deletion visibility
**Why out of scope**: The ASN correctly scopes out distinguishing which of several V-positions holding the same I-address was removed, classifying at I-address-set granularity. This is appropriately handled (a stated non-goal), not a gap — no action needed.

Note (not a REVISE): the predicate definitions CURRENT and NEVER_INCLUDED are mutually exclusive only at composite boundaries (off-boundary the "impossible row" `a ∈ ran(M(d)) ∧ (a,d) ∉ R` can occur, making both hold). D-BOUND and D-EXH correctly confine the operation to boundaries, so this is sound as written — flagged only so a future editor does not weaken the boundary precondition.

VERDICT: REVISE
