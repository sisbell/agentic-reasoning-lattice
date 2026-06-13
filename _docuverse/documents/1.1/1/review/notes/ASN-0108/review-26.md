# Review of ASN-0108

The mathematics is sound and the rigor is real. I checked the load-bearing pieces against the substrate: the W2 weakest-precondition nesting (membership-identity ⟹ frozen-prefix `j'=j` ⟹ the genuine `j'=j ∨ (j ≥ m' ∧ j' ≥ m')`, with the past-the-end corner correctly admitted); the W4 variable-schedule partition induction; the W9a count `⌈m/N⌉ + [N divides m]` against all four boundary walks (`m=4,5,0` and `N>m`, including the `[N divides m]` term firing at `m=0` and `m=4`); the W9b injective-charge termination bound; and the W9c/W9d necessity-vs-non-necessity split for clauses 1 and 2. They hold. The concrete walks are each earned (every one demonstrates a distinct property — offset duplicate, cut-point skip, harmless tail reorder, blind-spot omission, orphan survival, ping-pong non-termination), the wp analysis is non-trivial, and the computability-vs-clause-1 refinement in W9 is a genuine distinction correctly drawn. The W6 multi-document caveat properly bounds the address key's append-at-tail guarantee rather than overclaiming, and the W6a frame argument correctly grounds in K.λ's `M'=M, C'=C`. No correctness defect, no cross-ASN reference outside the foundations, no drift into implementation mechanics.

The findings are anti-bloat: two specific accretions in the freshly-added key-condition material.

## REVISE

### Issue 1: Defensive justification of a rejected scoping, plus a key-class aside
**ASN-0108, "Stability of the Order Across Evolution" (W5)**: "Were the re-delivery half left *unscoped*, the iff would be false outright — clause 1 can hold throughout a delivered–orphaned–resurrected episode while the link is delivered twice. (An allocation-monotone address key recovers even the *unscoped* no-re-delivery guarantee, since a resurrected link returns at its permanent low key, below the advancing cursor, and is never reached again — W9b; but that is a property of *that key class*, not of clause 1 in general.)"

**Problem**: The iff already carries its scoping inline ("for every `a` matching in both states"), and the per-step skip/duplicate unpacking immediately below establishes it. This sentence justifies the scoping by describing what the *rejected, unscoped* version of the claim would do; the parenthetical then describes how *one specific key class* would behave *under that rejected version* — a doubly-removed aside (a variant the ASN does not adopt × a key class), with a second forward-deferral to W9b on top of the one already made one clause earlier. A reader following "coherence iff clause 1" must skip past a defense of a road not taken.

**Required**: Delete the "Were the re-delivery half left unscoped…" sentence and its parenthetical. The W6-blind-spot and resurrection clarifications immediately preceding already explain the scoping; the rejected-version counterfactual and the allocation-monotone-key behavior under it add nothing the claim needs.

### Issue 2: The "state-stable but not value-total" cursor-survival argument is stated twice
**ASN-0108, "Stability of the Order Across Evolution" (the ladder) and "Disappearance and Cursor Survival" (W8)**:
- Ladder: "a content-position key with frozen values but removable content is state-stable (its comparisons never move over surviving links) yet not value-total (orphaning the cursor's content loses `κ(c)`). So cursor-survival-under-orphaning (W8) is delivered by value-totality, not by state-stability…"
- W8: "State-stability does *not* close it: a content-position key with frozen values but removable content would be state-stable (W5) yet still lose `κ(c)` on orphaning, because state-stability constrains only surviving links and says nothing about an orphaned cursor's key."

**Problem**: The same example (content-position key, frozen values, removable content) reaching the same conclusion (state-stable but not value-total ⟹ W8 cursor-survival needs value-totality, not state-stability) appears in both sections. The ladder pre-derives W8's punchline; W8 re-derives it. One of the two is redundant — two paragraphs in different sections saying the same thing in different words.

**Required**: State the argument once. Either let the ladder define value-totality and the value-totality⟹state-stability (not conversely) relation, and have W8 cite it; or keep the orphaning example in W8 where cursor-survival is the subject and let the ladder introduce value-totality without re-running it. While consolidating: the ladder's per-entry use-site tags — "Necessary and sufficient for coherence (W5) and necessary for termination (W9c)", "Not necessary for coherence (W5) or termination (W9d)", "discharges W5, W8, and W9 together and for free" — are use-site inventory; each condition's logical role is established at its point of use, so the ladder need only carry what is genuinely new (value-totality, and the computability-vs-comparison-stability split), not a tagged re-listing of clause 1, clause 2, and state-stability, all defined two paragraphs above.

## OUT_OF_SCOPE

### The five Open Questions
**Why out of scope**: Multi-document enumeration order (no global allocation-monotone key), eventual-delivery under non-allocation-monotone keys, the cross-call completeness invariant over a mutating result set, distinguishing cursor-invalidation from exhaustion, and delivery/sizing correspondence are all genuine future territory. The ASN defers them correctly as Open Questions rather than half-answering them; the W6 multi-document caveat bounds the claim instead of overreaching. No finding.

VERDICT: REVISE
