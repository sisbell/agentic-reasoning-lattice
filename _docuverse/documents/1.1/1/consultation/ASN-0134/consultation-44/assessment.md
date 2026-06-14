# Channel Assignment — ASN-0134 review-44

**Date:** 2026-06-14 13:53

## Issue 1: K.σ-as-`A_doc`-emission is grafted across two state models, and the H0/H1/H2 carry-over is asserted, not derived
Reason: The identification of K.σ with an `A_doc` emission rests on two external grounds the fix must check — a design-intent claim (the account is a home in the owned-numbers tree, allocating documents one tier up) and an implementation claim ("Gregory confirms the mechanism is literally the same"). Choosing between option (a) deriving necessary `A_doc`-conformance and option (b) the conditional scoping requires knowing both what document allocation was meant to do and what the code actually does.
Nelson question: Was document creation intended to draw addresses from an account-level owned-numbers sub-allocator — the account handing out contiguous document addresses by order of arrival, exactly as a document hands out content addresses — or did the design leave document-address freshness unspecified?
Gregory question: Does udanax-green allocate document/orgl addresses by reading a shared per-account frontier and depositing contiguously (so two same-account creations read one frontier and compute the same address), or by a freshness-test that admits gaps in document numbering?

## Issue 2: the account-tier H2/H1 claim is restated five times
Reason: Pure consolidation — the act of stating the carry-over once and having H3/clause 2/SAFE cite it is editorial, and follows whatever content Issue 1 resolves. Derivable from the ASN alone.

## Issue 3: §4's two closing summaries recap the per-instance conclusions
Reason: Each instance analysis already states its governing discipline and that its read is global, so deleting the duplicate summary is an internal edit needing no external input.

## Issue 4: G0's claim statement carries a sequential-consistency essay
Reason: Editorial trim of a claim slot to its load-bearing cross-home-program-order sentence; the content to keep is already identified in the note and the G1 forward-reference is removable internally.

## Issue 5: A6's invariant-taxonomy prose does not advance "every state is canonical"
Reason: The chain-contiguity mechanism already lives in full in W3 and the P2/R2 exclusion-justification is removable; both fixes are internal to the note's own division of labor.
