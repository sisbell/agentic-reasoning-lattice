# Review of ASN-0086

I checked the six relational properties, the three operations, both weakest-precondition cases, and the worked sketch. The core arguments are sound: R0a's two-case antichain proof is correct, R-Scope's self-emit branch is handled properly, and both wp derivations close in both directions. The worked sketch's tumbler arithmetic checks out at every step. No proof gaps, no missing edge cases, no forbidden cross-ASN references (all citations are to foundations 0034/0036/0040/0043/0093). The note correctly stays in abstract state/operation/invariant territory — no META.

The note carries the anti-bloat classifier, and a few residual meta-prose instances remain.

## REVISE

### Issue 1: Redundant dual-citation in AddressUniverse
**ASN-0086, Definition — AddressUniverse**: "By SD (StoreDisjointness, ASN-0093) — equivalently ASN-0043 L14 (DualPrimitive) together with ASN-0093 L0 supplying global `s_C`-residency of content — `A^Σ` is the entirety of stored-entity addresses at Σ; no third category exists."
**Problem**: The fact `A^Σ` exhausts stored-entity addresses follows from SD alone (a foundation already stating the global disjointness this note needs). The "— equivalently ASN-0043 L14 … content —" parenthetical supplies a second, longer derivation route the reader must parse and verify the equivalence of, advancing no claim. This is the defensive double-derivation pattern the anti-bloat lens flags.
**Required**: Cite SD only; drop the L14+L0 alternative route.

### Issue 2: Proof meta-commentary describing strategy instead of advancing it
**ASN-0086, L-ContiguousPrefix proof**: "This is ChainMembershipForOrigin (ASN-0093, link half) restated at `→*`-reachable states in the `home`/`J_d^Σ` notation; we cite the foundation rather than re-derive it."
**Problem**: The clause "we cite the foundation rather than re-derive it" describes the proof's intent, then the paragraph proceeds to do the re-derivation (the HomeOriginCoincidence identification plus the `j = position − 1` re-indexing) — so the meta-claim is both skippable and contradicted by what follows. Same pattern appears in the R0 proof ("R0 contributes only the structural postconditions … and cites ASN-0093's FirstEmissionFreshness …"), which narrates the division of labor rather than executing it.
**Required**: Delete the strategy-narration sentences; keep the actual derivation steps.

### Issue 3: Non-advancing aside in Reachability
**ASN-0086, paragraph after Definition — Reachability**: "Equivalently, `Σ →* Σ'` implies `Σ' ⊒ Σ` in ASN-0043's sense; the converse need not hold."
**Problem**: The `⊒` restatement plus "the converse need not hold" is a defensive clarification that no later claim consumes — nothing in the note relies on `→*` being strictly stronger than `⊒`. It is the precise reader's noise to skip past.
**Required**: Remove, or fold the one load-bearing direction into the preceding sentence if any downstream use exists (I found none).

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and cross-layer type collision
The Open Questions correctly defer multi-arity projections (`L_K^{(n)}`), inter-layer dynamic type allocation under L9, and the substrate-vs-layer placement of the unit-depth retraction discipline. These are new territory, not defects here.

VERDICT: REVISE
