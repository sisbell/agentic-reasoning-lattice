# Review of ASN-0108

This is a strong note — the weakest-precondition analysis in W2 is genuinely rigorous (I verified the offset-cursor `wp` formula against all four boundary regimes and it is exactly right), the W9b per-link multiplicity bound is sound, and every boundary case the operation hinges on (`m = 0`, `N > m`, exact multiple, orphaned cursor) is walked concretely. The technical content holds. The findings below are a citation-precision issue and — given the `review-mode.anti-bloat` classifier — accreted meta-prose.

## REVISE

### Issue 1: "Never reused" miscited to T8; address-key stability is definitional, not an allocation consequence
**ASN-0108, W5**: "an address is permanent — never changed, never reused (foundation T8, allocation permanence)"
**ASN-0108, W2**: "Under an address-based key this is true unconditionally (foundation T8: the address, hence the key, is permanent)"
**Problem**: Two distinct precision faults, in a note that is otherwise meticulous about which foundation discharges which step.
 (a) T8 (AllocationPermanence) gives *never removed* (the allocated set grows monotonically). It does **not** give *never reused* — address uniqueness across allocation events is **GlobalUniqueness** (ASN-0034). The conjunct "never reused (T8)" attributes to T8 a guarantee T8 does not make.
 (b) More substantively: for the address key `κ(a) = a`, state-stability (W5's clauses 1 and 2) holds because `κ` is a *state-independent function of the address* — `κ_Σ(a) = κ_{Σ'}(a) = a` for every state, so no key value can move. This is definitional and needs no allocation axiom at all. T8 (or, more directly, LP13, link persistence) is needed only for the *orthogonal* fact that the cursor `c` remains an allocated, uniquely-identifying address. The note collapses "the key value is stable" into "the address is permanent (T8)," conflating two different obligations. Likewise the W2 `wp(resume_id, R) ≡ κ(c) recoverable` is discharged for the address key simply because the reader *holds* `c`; T8 is not what makes `κ(c)` recoverable.
**Required**: Split the attribution — cite GlobalUniqueness for uniqueness, T8/LP13 for the cursor address remaining valid — and ground the address key's clause-1/clause-2 satisfaction in `κ` being state-independent by construction, not in allocation permanence.

### Issue 2: Essay-length entries in the "Claims Introduced" table
**ASN-0108, Claims Introduced**, W9b row: "Over a mutating set, termination holds under clause-1 cut-point preservation at each cursor (W5) together with *finite cumulative tail inflow counted with multiplicity* = |initial tail| (finite by M-fin) + creations-ahead + becomings-discoverable-ahead (LP18, resurrection or born-ghost); a per-link multiplicity bound caps total deliveries at |initial tail| + |inflow events|, and bounded instantaneous tail size is not sufficient"
**Problem**: The table is a structural index — its sibling rows (`Match`, `κ`, `After`, W0, W1) are one-line summaries, and the foundation ASNs use the same terse `| Label | Statement | Status |` convention. The W5, W9, and W9b rows are full paragraphs re-deriving the claim body verbatim. Essay content in a summary slot is duplication the reader must read twice; it does not advance the argument.
**Required**: Reduce W5/W9/W9b rows to one-line summaries; the derivations already live in the claim bodies.

### Issue 3: Self-acknowledged cross-section duplication (W5 ↔ W9d)
**ASN-0108, W5**: "a free tail permutation that keeps every tail link above the cursor is a pure clause-2 violation with clause 1 intact, and it skips nothing (the walk below; **W9d records the same for termination**)"
**ASN-0108, W9d**: "a free tail permutation only reshuffles delivery order, never whether the pass ends"
**Problem**: W5 states the free-tail-permutation consequence for coherence and then defers, in-line, to a downstream location it admits "records the same." This is precisely the flagged pattern — a paragraph deferring to a downstream paragraph that restates it. The clause-1-necessary / clause-2-not-necessary scaffolding is legitimately load-bearing where it does distinct work (W9c/W9d *are* the termination analogues of W5), but the "records the same" parenthetical and the verbatim free-permutation example in both slots are redundant.
**Required**: Keep the free-tail-permutation walk in one place; in the other, cite it by label without re-narrating, and drop the "records the same" deferral.

### Issue 4: Defensive meta-prose justifying authorial choices rather than stating claim content
**ASN-0108, W10**: "We make the boundary explicit so that no implementation mistakes the absence of a progress field for an omission to be fixed: it is a deliberate division of labour."
**ASN-0108, W3**: "We treat this as abstract because any implementation that wishes resumption to survive crashes, reconnections, and concurrent readers must locate the continuation state in the cursor rather than in the server"
**Problem**: Both sentences defend *why the claim is stated* (and at what abstraction level) rather than asserting what the operation does or guarantees. W10 has already said the substantive thing ("the cursor exposes only the resume key … carries no 'position k of m' field"); the appended "we make explicit so that no implementation mistakes …" is justificatory padding. The abstraction-level self-assessment in W3 is reviewer-facing judgment, not claim content.
**Required**: Cut the justificatory tails; the frame condition (W10) and the stateless-determinism guarantee (W3) stand without the editorializing.

## OUT_OF_SCOPE

### Topic 1: Multi-home-document enumeration discipline
**Why out of scope**: The note correctly observes (W6 caveat) that the address key is allocation-monotone only *within* a single home document, while `Match` generically spans home documents (links discoverable from `d_q` are homed anywhere), so the W6 blind spot is generically reopened. This is honestly surfaced and routed to Open Question 1 rather than papered over — a future ASN's territory, not an error here.

### Topic 2: Query construction and type-part refinement
**Why out of scope**: `Match(q, Σ)` is taken as given from ASN-0127's `findlinks_V`, with *which* region a query fixes and any ASN-0086 type refinement explicitly deferred to query construction. Taking the matching set as an import and specifying only delivery is a clean separation, not an omission.

VERDICT: REVISE
