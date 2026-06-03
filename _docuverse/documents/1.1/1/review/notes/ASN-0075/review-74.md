# Review of ASN-0075

## REVISE

### Issue 1: The wp section restates "boundary conjunct is not part of the weakest precondition" four times
**ASN-0075, "The SHOWDELETIONS Operation" (wp analysis)**: The same observation recurs across three consecutive paragraphs:
- "Hence the genuine weakest precondition for q carries no boundary conjunct…"
- "That conjunct is not needed to compute q… while noting it is not part of the weakest precondition for q."
- "the boundary conjunct of the stated precondition is no part of the weakest precondition…"

**Problem**: One fact (D-BOUND is strictly stronger than `wp(op, q)`) is asserted four times. The paragraph beginning "The operation's stated precondition (D-BOUND) is strictly stronger…" is additionally a "why the precondition is retained" rationale essay — it explains why D-BOUND is kept ("load-bearing for the report's meaning rather than its bare production… We retain the boundary conjunct… for this semantic guarantee") rather than advancing the wp computation. This is exactly the new-prose-around-a-precondition-explaining-why-it-is-needed pattern the anti-bloat pass targets. A precise reader has to skip past the repetition to track that the wp result has not changed.
**Required**: State the `wp(op, q) = d_A ∈ E_doc ∧ d_B ∈ E_doc` result once, note in one clause that the stated precondition adds the boundary conjunct for the D-WIT/D-EXH semantic guarantee, and delete the remaining two restatements. Fold the state-level `wp(SHOWDELETIONS, P)` rule in without re-litigating the boundary conjunct.

### Issue 2: Output-half finiteness derived in two places
**ASN-0075, wp termination paragraph vs. D-ORD**: The wp paragraph closes with "The same finiteness of dom(C) makes each output half a finite set" (with C-fin/S8-fin); D-ORD then re-derives "Each output half is a finite subset of dom(C) ⊆ T, finite by C-fin (ASN-0047)."
**Problem**: Identical finiteness fact established twice from the same premise. The wp termination prose ("scans finitely many addresses and performs finitely many bounded membership tests, so the operation halts") also leans toward describing an enumeration procedure rather than stating an abstract guarantee.
**Required**: Establish output finiteness once (it is genuinely needed in D-ORD for orderability); in the wp section, cite termination/finiteness by reference rather than re-deriving the membership-test walk.

## OUT_OF_SCOPE

### Topic 1: Restoration consuming SHOWDELETIONS output, third-document witnesses, n-ary families
**Why out of scope**: The Open Questions correctly route restoration mechanics, multi-document witness structure, and concurrency consistency to future ASNs. These are new territory, not gaps in the SHOWDELETIONS specification. (Minor: questions 3 and 5 — "deleted from both, current in a third" and "families of more than two documents" — overlap and could be merged, but this is not a correctness issue.)

VERDICT: REVISE
