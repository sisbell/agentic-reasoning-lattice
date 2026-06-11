# Channel Assignment — ASN-0121 review-34

**Date:** 2026-06-11 15:38

## Issue 1: FL-JUNK is quantified over a single atomic step but claims invariance under arbitrary quantity
Reason: The fix is internal — restating the lemma over `Σ →* Σ'` and adding the inductive lift uses only facts the ASN already records (F-PRES per step, L12/LP13 value persistence, link-store and `nullified` monotonicity across the closure). No design intent or implementation evidence is required.

## Issue 2: Consultation Q14 as cited contradicts FL-EMP's load-bearing distinction
Reason: The abstract unit/zero distinction is already settled from Nelson's NOSPECS; what is missing is an implementation fact — whether Gregory's wire encoding renders an empty type spec as the absent-slot (NOSPECS) representation or as a constrained slot that can resolve to no addresses. Only Gregory can say which reconciliation clause is true.
Gregory question: In the udanax-green find-links request format, is an empty type specification structurally identical to an omitted/NOSPECS type slot (so the slot is simply not consulted in the intersection), or can a caller supply a present-but-empty type spec that, like Q7's vacuously-resolving slot, short-circuits the find to the empty link-set — i.e., does the encoding make the abstract `Θ = ∅` request expressible at all?

## Issue 3: The Σ.L-only-dependence fact is stated four times and twice used by forward deferral before it is established
Reason: Internal restructuring — the one-line lemma's content (`nullified` and `sat` read only `Σ.L`, `home(a)`, and `q`) is already fully derived in FL-STB; the fix is hoisting it after FL-DEF and rewiring citations backward.

## Issue 4: FL-REACH (d) stages a wrong claim and its correction instead of stating the result
Reason: Internal prose surgery — the containment, strictness condition, and `(∗, ∅, ∗, ∗)` counterexample are all already present and correct; the fix only deletes the temptation/correction narrative framing around them.

## Issue 5: Local duplication and meta-prose instances
Reason: Internal editorial consolidation — each instance is a duplicate or meta-announcement of content established elsewhere in the ASN; deletion and one-formulation rewrites need no external input.

## Issue 6: First-class retrieval of a standing retraction link is asserted but never witnessed
Reason: Internal — the missing positive witness is computed entirely within the ASN's own machinery (FL-DEF membership for `r₁`, addressability from the trace's constructed `L_R`, FL-EMP's link-side wildcard rule), and the underlying first-class-retrieval claim already carries its consultation Q2 citation.
