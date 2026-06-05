# Review of ASN-0108

This is a careful, mature design note. The total-order/cursor/termination/progress decomposition is sound, the wp analysis in W2 is correct (I verified the three-way nesting membership-identity ⟹ frozen-prefix ⟹ genuine-weakest, and the empty-window corner), the W4 partition proof correctly generalizes to variable `N_i`, and the W9a count formula `⌈m/N⌉ + [N|m]` checks against all four boundary walks (m=4, m=5, m=0, N>m). Boundary coverage (empty set, exact multiple, first-window-short, orphaned cursor, new-link-before/after-cursor) is unusually complete. One precision gap remains.

## REVISE

### Issue 1: W6a's "Regardless of key" universal is broader than its proof
**ASN-0108, W6a (CreationDoesNotDisturbSeenLinks)**: "Regardless of key, the *creation* of `a_new` does not alter the key or the relative order of any already-enumerated link." ... "Hence under *any* key that is a function of `(address, matched-content-position)` — which covers both the address key ... and the content-position key alike — every already-enumerated link retains its key".

**Problem**: The bold claim is universally quantified over keys ("Regardless of key," "under *any* key"), but the K.λ-frame justification establishes the conclusion only for keys that are *functions of `(address, matched-content-position)`*. W0 admits "an injective key `κ` into a totally-ordered codomain" with no further restriction — so the key space W6a quantifies over (inherited from W0) is strictly larger than the subclass the proof covers. A key admitted by W0 that consults other state — e.g. one whose value depends on `|Match(q, Σ)|` — would be perturbed by `a_new`'s creation, since creation grows the matching set, falsifying "Regardless of key." The recent strengthening to the K.λ-frame argument (per the heading "strengthen ... to K.λ frame") tightened the body's scope but left the heading's universal stale.

**Required**: Either restrict the W6a heading to "for any key that is a function of `(address, matched-content-position)`" (matching the body), or add to W0/W6a a constraint establishing that every admissible ordering key must be a function of `(address, matched-content-position)`, so the universal quantifier is licensed. As written, the quantifier in the claim outruns the quantifier the proof discharges.

## OUT_OF_SCOPE

### Topic 1: Multi-document global allocation-monotonicity
W6 correctly notes that across home documents whose link allocators advance independently, even the address key is not globally allocation-monotone (T9 gives forward ordering only `same_allocator`), reopening the W6 blind spot. This is properly deferred to the first Open Question.

**Why out of scope**: It is new territory requiring a cross-allocator ordering invariant, not an error in this note's single-allocator treatment; the ASN explicitly defers it.

VERDICT: REVISE
