# Review of ASN-0108

I verified the mathematics in detail. The wp analysis for the offset vs. identity cursor (W2) is correct, including the strict nesting of membership-identity ⟹ frozen-prefix ⟹ the genuine weakest precondition `j' = j ∨ (j ≥ m' ∧ j' ≥ m')`, with valid witnesses for each non-implication. W4's partition induction is sound under the variable schedule, the four termination walks (m=4, m=5, m=0, N>m) all confirm W9a's `⌈m/N⌉ + [N divides m]` count, and the five W5/W8/W9c walks each exercise the case they claim (I re-traced the cut-point skip, the harmless tail reorder, the clause-1 cancellation, the cursor-survival-under-orphaning, and the zero-inflow loop). The W9b charge argument is injective as claimed. Edge cases are covered thoroughly; cross-ASN references are confined to foundations; there is no drift into implementation mechanics (the `onlinklist`/spanfilade/POOM material is evidence, not normative). The note is mathematically converged.

The remaining item is anti-bloat residue, consistent with the `review-mode.anti-bloat` classifier and the recent centralization edit.

## REVISE

### Issue 1: Residual organizational meta-prose in the permanence statement
**ASN-0108, "The Enumeration Order" (Gregory's matched-content key reading)**: "This key is **permanent** — established here once, as the basis the downstream guarantees draw on: an I-address is never reassigned, and content is never moved or removed from the Istream (S0)..."

**Problem**: The interjected clause "— established here once, as the basis the downstream guarantees draw on" states no fact about permanence. It announces the note's centralization decision (where the justification lives) and soft-enumerates downstream consumers ("the downstream guarantees draw on") — both flagged patterns. A reader following the permanence argument must skip past this clause to reach the actual content ("an I-address is never reassigned..."). The downstream back-references that depend on it — W5's "(established above, where the key was introduced)" and W8's "(established above)" — already do the linking on their own; they point back to the permanence statement regardless of whether the source announces itself.

**Required**: Delete the clause. "This key is **permanent**: an I-address is never reassigned, and content is never moved or removed from the Istream (S0), so the key's value is immutable under rearrangement (LP11) and survives orphaning (...)." The back-references remain functional.

### Issue 2: Same pattern — non-repetition announcement in W8
**ASN-0108, "Disappearance and Cursor Survival" (W8)**: "Allocation enters only *orthogonally* here, exactly as set out under W5 — we do not repeat the argument."

**Problem**: "— we do not repeat the argument" announces a non-repetition rather than advancing reasoning. The cross-reference "exactly as set out under W5" already tells the reader where the argument lives; the trailing meta-comment adds nothing a precise reader needs.

**Required**: End the sentence at the cross-reference: "Allocation enters only *orthogonally* here, exactly as set out under W5."

## OUT_OF_SCOPE

No findings. The Open Questions (multi-home-document enumeration order, eventual-delivery conditions under a non-allocation-monotone key, the cross-state completeness invariant, irrecoverable-cursor detection for non-permanent keys, delivery/sizing-order correspondence) are genuine future territory, not gaps in this note. In particular, Open Question 4 is not answered-then-re-asked: W8 shows a *permanent* key dissolves the exhaustion/invalidation conflation, and the open question correctly targets the *position-key* case the note leaves unsolved. The scope-deferred items (which region a query fixes; the query's type-part refinement, ASN-0086) are appropriately punted, and because W0–W11 depend only on M-fin and M-mut — which hold under any satisfaction predicate — the windowing laws are robust to that deferral.

VERDICT: REVISE
