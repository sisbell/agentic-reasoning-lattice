# Review of ASN-0111

## REVISE

### Issue 1: "link store empty" is false in the orphaned worked example

**ASN-0111, "A worked read" (orphaned instance, Slot 1 from)**: "by the same corollary, `coverage(F) ∩ dom(Σ.C)` is exactly the three named chain-member I-addresses, unarranged by hypothesis; **with the link store empty** and every arrangement range confined to `dom(Σ.C) ∪ dom(Σ.L)` (LP20 RangeConfinement…), `coverage(F) ∩ ran(Σ.M(d)) = ∅` for every `d`."

**Problem**: The link store is not empty here — the entire example reads link `a = [1.0.1.0.1.0.2.1] ∈ dom(Σ.L)`, and the nested instance adds `a'` and `c`. So `dom(Σ.L) ≠ ∅`. The premise the argument actually needs is `coverage(F) ∩ dom(Σ.L) = ∅`, which was derived one sentence earlier ("the link store meets neither coverage: `coverage(F) ∩ dom(Σ.L) = coverage(Θ) ∩ dom(Σ.L) = ∅`"). Notably, the parallel Slot 3 (type) argument gets this right — it writes "with the link store also disjoint (above)" — so Slot 1's "empty" is an isolated slip that contradicts the example's own setup.

**Required**: Replace "with the link store empty" with "with `coverage(F) ∩ dom(Σ.L) = ∅` (above)", matching the Slot 3 phrasing.

### Issue 2: Defensive parentheticals accrete around RL1/RL2 boundary

**ASN-0111, Claims table and RL2 body**: table entry RL1 "(rejects the satisfaction model)"; table entry RL2 "from/to/type grouping delivered as structure, **not reconstructed from RL1's per-slot equality**"; body "slot position is part of the value, **not a label a reader reconstructs from an unordered pool**."

**Problem**: These clauses do not advance the claims; they pre-empt an objection that RL2 might be redundant with RL1. This is the reviser-drift pattern the anti-bloat classifier targets — defensive justification of why one claim differs from a neighbour, accreted in a structural slot (the claims table). RL2 stands on its own (`|readlink| = |Σ.L(a)|` plus the L6 positional accessor); it does not need to argue against RL1.

**Required**: Drop the parenthetical justifications. State RL2 as the arity-and-slot-primitive guarantee and let the contrast with RL1 stand implicitly.

## OUT_OF_SCOPE

None. The note correctly confines itself to the direct read and routes following/searching/counting/creation to their own ASNs; the three Open Questions defer genuinely new territory (continued-validity inference, empty-vs-unwitnessed distinguishability, identity distinguishability) to future work rather than smuggling claims in.

VERDICT: REVISE
