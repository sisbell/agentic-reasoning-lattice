# Review of ASN-0100

This is a rigorous specification. The invariant coverage in §Verifying the Invariants and §Atomicity is genuinely thorough — every conjunct of ExtendedReachableStateInvariants is discharged, the composite-boundary vs. per-state distinction is handled correctly, the K.α freshness chain is sound, and the worked examples (interior, append, empty, re-insertion-after-clearance) confirm the regions. The wp analysis is non-trivial, and INS.chain-shift / INS.proj are correctly derived. I found no proof gaps in the mathematics. The findings below are prose-accretion items surfaced under the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Consequence prose lodged in the precondition slot
**ASN-0100, §The Operation: Formal Contract (composite-boundary premise of INS.pre)**: "These hold only at composite boundaries, not at arbitrary elementary-reachable states. INSERT realises Σ →* Σ' as one composite, so Σ' is again a composite boundary."
**Problem**: A precondition is a structural slot — it states what the pre-state must satisfy. The first sentence justifies *why* the premise is needed (scope-explanation of a foundation property); the second asserts a fact about the *output* state Σ', which is a verification consequence, not a precondition. Both belong elsewhere (the post-state reasoning already establishes Σ' is a boundary in §Atomicity).
**Required**: Reduce the premise to its content — "Σ is a composite boundary (ASN-0047), so P4★, P4a, P7a are available" — and drop the trailing explanatory/consequence sentences.

### Issue 2: Forward-defer meta-prose
**ASN-0100, §The Question**: "The word 'atomically' raises a sub-question: *in what sense* is the post-state reached without observable intermediate violation? We defer the answer to the Atomicity section, which states and discharges the precise guarantee."
**Problem**: This is a downstream pointer that advances no reasoning. The Atomicity section states and discharges the guarantee regardless of the announcement; the deferral sentence is noise the reader must skip.
**Required**: Delete the deferral. If the precise sense of "atomically" matters at the outset, state it in one clause; otherwise let the Atomicity section carry it.

### Issue 3: Retired-claim remnant restating an INS.proj consequence
**ASN-0100, §INSERT vs. COPY (after the cross-document corollary)**: "The same value-vs-address distinction settles a link-survivability question without further derivation: a tight endset cannot silently expand to capture freshly inserted content, since INS.proj's tight-endset case (N_{ℓ,i} = ∅) already establishes that a fresh a_new lies outside the endset's coverage..."
**Problem**: This is the third statement of the tight-endset `N_{ℓ,i} = ∅` consequence (already in §Coverage's "fresh-address discoverability" and again in the wp analysis). The self-flagging phrases "without further derivation" and "already establishes" confirm it adds nothing. It reads as prose left behind after the retired INS.identity.tightsurv claim row rather than removed.
**Required**: Delete the sentence; the consequence is established at INS.proj and need not be re-asserted to make the identity-by-allocation point.

## OUT_OF_SCOPE

(none — the INSERT-vs-COPY contrast stays minimal and serves INS.identity; it does not specify COPY mechanics.)

VERDICT: REVISE
