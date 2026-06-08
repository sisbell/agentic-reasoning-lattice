# Review of ASN-0103

The technical core is sound. I checked the central proofs and they hold:

- `D_A = E ∩ S(A,2)` — both inclusions are correct; the unique-parse argument for `D_A ⊆ S(A,2)` is valid, and the length filter `#e = #A+2` genuinely separates documents from versions (`≥ #A+3`).
- Freshness (`d ∉ E`) is established uniformly over all of `E` via `d ∈ S(A,2)\D_A`, with no case split — and it is robust to non-contiguity of `D_A`, since it relies only on `d > max(D_A)`, not on B1.
- Distinctness (same-chain via S0, version/cross-account via B7) covers present and future addresses correctly.
- The single-`K.δ` decomposition satisfies its case-(ii) preconditions at `Σ`, atomicity follows, and the invariant discharge (direct / vacuous-on-empty / frame-inherited) is complete.
- The worked example is concrete and correctly demonstrates the collision the length filter averts.

The findings below are the anti-bloat items the classifier directs me to surface.

## REVISE

### Issue 1: Meta-framing in "The Question" and "Background"
**ASN-0103, "The Question"**: "The answer must be sharp enough to measure an implementation against, and abstract enough that two implementations meeting it are externally indistinguishable."
**Problem**: This is commentary about specification quality, not object content — essay framing in a structural slot. The four rhetorical sub-questions are a roadmap restating the section headers ("What is allocated / preserved / distinguishes / invariants"). Similarly in Background: "This separation is the whole point of the operation we are specifying." These sentences are skipped past to reach the reasoning.
**Required**: Reduce "The Question" to a one-line statement of the operation under specification; cut the indistinguishability sentence and the "whole point" sentence.

### Issue 2: Ghost-element principle stated three times
**ASN-0103, Background / Effect Three / Referability**: Background derives the ghost-element principle with its Nelson quote; Effect Three restates "The document is, at the instant of creation, a ghost element: a position in `E` with nothing stored beneath it in `C`"; Referability invokes "the ghost-element principle again" with a second Nelson quote.
**Problem**: The same point — an address may be referable with no content stored — is presented three times across three sections in different words. Two of the three do not advance the local claim.
**Required**: State the ghost-element principle once (Background), and have Effect Three and Referability reference it rather than re-expound it.

### Issue 3: "What Distinguishes Creation From Forking" re-derives an already-established result
**ASN-0103, "What Distinguishes Creation From Forking"**: "A freshly created document shares *nothing* by default. Its arrangement is empty: `ran(M'(d)) = ∅`."
**Problem**: `ran(M'(d)) = ∅` is established in Effect Two and frame-stated again here before the genuinely new content (the S4 origin-based identity point) arrives. The opening re-presents Effect Two rather than building on it.
**Required**: Open the section from the established `ran(M'(d)) = ∅` by reference, and keep only the S4 argument (value coincidence does not create shared identity), which is the section's actual contribution.

## OUT_OF_SCOPE

### Topic 1: Effective-owner reading of ownership
The ASN delivers structural ownership (`owns(π,d) ≡ pfx(π) ≼ d`) and explicitly leaves `ω_Σ'(d) = π` open pending an entity-set/baptismal-registry coupling. The deferral (CND.own note + Open Question 6) is legitimate — effective ownership depends on machinery not in this ASN's scope.

### Topic 2: Concurrency, partial-failure recovery, write-readiness
The Open Questions on serialisation of concurrent creates, recovery semantics, and session write-readiness are correctly posed as future territory, not gaps in this operation's contract.

VERDICT: REVISE
