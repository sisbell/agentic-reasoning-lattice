# Review of ASN-0108

This note is unusually careful — the W2 wp-nesting, the W4 partition induction (including its variable-`N_i` generalization), and the W9/W9a count walks (`m=0`, `m=N|m`, `N>m`) all check out, and the concrete walks for W5/W6/W8 each correctly demonstrate the hazard they advertise. The defects are one load-bearing gap in the W9a termination derivation and several instances of the accreted meta-prose the anti-bloat classifier was set to catch.

## REVISE

### Issue 1: W9a's termination derivation rests on a false lemma

**ASN-0108, W9a**: "cut-point preservation at each cursor guarantees that no delivered link ever re-ascends above the advancing cursor, so every delivered link's key stays permanently below every later cursor, no delivered link ever re-enters After, no link is consumed twice, and this finite supply is exhausted in finitely many calls."

**Problem**: Cut-point preservation (W5 clause 1) is quantified over links *"matching in both states"* — the note states this explicitly. A delivered link that **orphans** (leaves `Match`; W7, ASN-0098 LP17) falls outside that quantifier, and on **resurrection** (ASN-0098 LP18 — a foundation fact this note builds on and nowhere excludes) it may re-enter `Match` with a key *above* a later cursor and be re-delivered. So "no delivered link ever re-ascends" does **not** follow from cut-point preservation, and "no link is consumed twice" is false in general. This is realizable while W5 still holds: W5 constrains only links matching in both states of a transition, and a resurrecting link is matching only in the post-state, so a W5-compliant content-position key permits delivered-orphan-resurrect-ahead. The "finite supply exhausted in finitely many calls" count then collapses, because the *same* supply element can be consumed unboundedly. (The hazard is specific to non-stable keys — under the address key, delivered keys are fixed below a strictly-monotone cursor, so re-ascension is structurally impossible; but W9a states the claim generally, "under a state-stable cursor key (W5).")

This also exposes an ambiguity the proof turns on: "finitely many matching links are ever added ahead of the cursor" reads as a **set** in the argument ("is a finite set"), but only a **count-with-multiplicity** reading (each resurrection-ahead = one inflow event) makes the termination claim true.

**Required**: Repair the derivation along one of: (a) count every re-entry-ahead (resurrection included) as tail inflow, replace the false "no link consumed twice" lemma with a per-link multiplicity bound, and state "inflow" as a count, not a set; (b) add an explicit hypothesis that delivered links never resurrect ahead of a later cursor; or (c) restrict the termination claim to allocation-stable keys (the address key), under which the "no re-ascension" step *is* valid via the monotone-cursor argument. Note that the note's own W8 walk already orphans a delivered link (`a_2`), so the escape hatch is not exotic.

### Issue 2: W9a is an essay packed into one claim body, which is how the Issue 1 gap stayed hidden

**ASN-0108, W9a**: a single ~600-word paragraph establishes (i) the fixed-set count formula, (ii) the cumulative-inflow sufficiency condition, (iii) the bounded-vs-cumulative distinction with a replenishment walk, (iv) the cut-point-necessity result with a walk and the re-ascension counterexample, and (v) the clause-1-vs-clause-2 non-necessity result.

**Problem**: These are five independent results, two of them carrying their own counterexamples, fused into one structural slot. The fusion is not cosmetic — it is precisely what let the invalid "no link consumed twice" step (Issue 1) pass unaudited inside a much larger correct-looking argument. "Essay content in structural slots" degrades auditability.

**Required**: Decompose into separate labelled sub-claims (e.g., fixed-set termination + count; cumulative-inflow sufficiency; cut-point necessity; clause-2 non-necessity), each with its own derivation, so the termination chain can be checked step by step.

### Issue 3: Match-section carries a defensive rationale and a use-site inventory

**ASN-0108, "State, the Matching Set..." section**: "(M-mut) in particular is *not* something we must argue afresh or defer to a satisfaction predicate fixed elsewhere: it is D-NONMONO... The choice between the two readings is therefore the choice between `findlinks_V` and fixed-`I` `findlinks`, both already in the foundation; we adopt the discoverability reading because..." and "The entire windowing analysis below — W7, the W2 offset-failure analysis, and W9a's termination subtleties — turns on (M-mut), hence on D-NONMONO; a windowing layer over the monotone fixed-`I` reading would inherit a strictly simpler theory."

**Problem**: Two of the patterns the anti-bloat mode names. The first sentence is a defensive justification of an import choice ("not something we must argue afresh or defer to … fixed elsewhere") — it pre-empts an objection rather than advancing the argument; the substantive content (`Match` = `findlinks_V`, non-monotone by D-NONMONO) is already in the `(M-mut)` bullet. The last sentence is a downstream-consumer inventory ("W7, the W2 offset-failure analysis, and W9a … turns on (M-mut)") plus a counterfactual about a different ASN that is never built.

**Required**: Keep the `(M-mut) = D-NONMONO` bullet and at most one sentence naming the discoverability reading as the adopted one. Drop the objection-defense and the W7/W2/W9a enumeration.

### Issue 4: The W6 "reconciliation" paragraph restates W6 and the W1 two-readings section

**ASN-0108, paragraph after W6a**: "The reconciliation: Nelson's append-at-tail is the *intended* behaviour, and it is *attained* exactly when the key is the link's permanent arrival-order address. An implementation that orders by matched-content position can satisfy W0–W5 *only once its key is composed with a permanent link-address tiebreaker* … the uncomposed boundary-only key fails W0/W1 outright by admitting ties. Even in the composite form, the content-position key forfeits W6's append guarantee…"

**Problem**: Most of this paragraph re-says material already stated: append-at-tail-when-address-keyed (W6), the boundary-only-key-fails-W0/W1 / must-compose-tiebreaker point (the W1 "two readings" subsection), and the content-key-forfeits-append point (W6). The only new content is the multi-document caveat ("even the address-based key is not globally allocation-monotone — T9 gives forward ordering only within one allocator…"), which motivates Open Question 1.

**Required**: Cut to the new multi-document caveat and its pointer to Open Question 1; delete the restatement of W6/W1.

## OUT_OF_SCOPE

### Topic 1: cross-state partition theorem (Open Question 6)
**Why out of scope**: The body proves W4 only "against a fixed `(Match, κ)`" and supplies the ingredients (W5 stability, W9a termination) but does not compose them into a no-gap/no-duplicate guarantee across a mutating set. Open Question 6 correctly defers this; it is new territory, not a gap in W4 as stated.

### Topic 2: disambiguating exhaustion from cursor-invalidation under a content key (Open Question 4)
**Why out of scope**: W8/W9 establish that the address key resolves the ambiguity and the content key conflates the two; what *discipline* would disambiguate a content-derived cursor is a future operation's concern. Appropriately listed as an Open Question.

VERDICT: REVISE
