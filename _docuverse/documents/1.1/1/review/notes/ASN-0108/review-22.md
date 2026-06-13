# Review of ASN-0108

## REVISE

### Issue 1: The W5 "iff" overclaims — its left side is broader than the proof establishes

**ASN-0108, W5 (OrderStability)**: "Resumption is *coherent* — it skips no still-matching link and re-delivers none already seen, judged against each call's own matching set (W7's present-tense reading) — *if and only if* the key satisfies **clause 1 (cut-point preservation)** at every cursor the reader actually holds."

**Problem**: The proof scopes "skip" narrowly — "A **skip** is a still-matching tail link `a` (`κ_Σ(c) <_K κ_Σ(a)`) falling to or below the cursor" — where `κ_Σ(a)` presupposes `a` *matched at the cursor-setting state* `Σ`. But the headline says "skips no still-matching link" with no such restriction, and the parenthetical "(W7's present-tense reading)" pushes toward judging against `Σ'` in full.

These differ exactly on the W6 phenomenon. Clause 1 quantifies *only* over links matching in both states, so it is silent about a link `L_new` created (or first becoming discoverable) after the cursor was set. Take a content-position key in a run with no rearrangement of existing matched content — clause 1 holds for every both-states link — and create `L_new` matching at `Σ'` whose endpoint sorts *below* the cursor. Then `L_new ∉ After(c, Σ')`, `L_new` stays below every advancing cursor, and is permanently skipped. `L_new` is a *still-matching link that is skipped while clause 1 holds*. So under the literal headline, clause 1 ⇏ coherent, and the biconditional is false. The iff is true only for the narrow notion (skip/duplicate restricted to links present in both states), which the proof uses but the statement does not.

**Required**: Narrow the left side to match the proof — "skips no link that was already an undelivered tail matcher when the cursor was set (matching in both the cursor-setting and resume states), and re-delivers none already seen" — and state explicitly that omission of a newly-created/newly-discoverable matcher landing below the cursor is the separate W6 blind spot, not a coherence failure. The "(W7's present-tense reading)" parenthetical, as written, contradicts the narrowing and should be dropped or qualified.

### Issue 2: W9b's multiplicity bound is not an upper bound under the stated event definition

**ASN-0108, W9b**: "A **tail-inflow event** is any single later transition that places a link into the reachable tail ahead of the then-current cursor. The total inflow is `|initial tail| + |tail-inflow events|`." … "the charge is injective and the total number of deliveries is at most `|initial tail| + |tail-inflow events|`."

**Problem**: The injective charge in the derivation maps each delivery to "the most recent transition that placed *it* into the tail" — a *per-link* placement. But the definition counts a tail-inflow event as a *transition*. One atomic `K.μ⁺` step can add several V→I mappings whose I-addresses lie in the coverage of several distinct orphaned links, resurrecting many of them ahead of the cursor at once (the LP18 mechanism W9b's source (3) invokes). If `|tail-inflow events|` counts transitions, that single transition absorbs multiple deliveries, so the charge is not injective into the counted set and the stated bound `deliveries ≤ |initial tail| + |tail-inflow events|` fails to bound deliveries. The termination *conclusion* survives (finitely many transitions, each placing finitely many links by S8-fin ⟹ finite deliveries), but the bound the proof advertises does not.

**Required**: Define a tail-inflow event as a (link, transition) placement and count `|tail-inflow events|` with multiplicity over links, consistent with the derivation's "the transition that placed *it*." Then injectivity and the bound hold as stated.

### Issue 3: Recap and realism meta-prose (anti-bloat)

The note carries `review-mode.anti-bloat`. The following do not advance reasoning and force the reader to skip past them:

- **W2, closing paragraph**: "The asymmetry this section advertises is real but lies on the *identity* side: the identity obligation (`κ(c)` recoverable) *is* the genuine weakest precondition…". "The asymmetry this section advertises" is self-referential, and "is real but lies on the X side" is a reviser correction of a prior framing, not new content — the wp derivation immediately above already established that the identity obligation is the weakest precondition met for free. Delete the recap.
- **W9b**: "The resurrection route is not exotic — W8's own walk orphans a delivered link, `a_2`, and resurrection ahead (LP18) is its symmetric move". This is a realism assertion plus back-reference. The sentence that *follows* it ("clause 1 cannot exclude it, since W5 quantifies only over links matching in *both* states…") is load-bearing and must stay; the "not exotic / W8's own walk" lead-in should go. Likewise "Unlike a blanket 'no link is consumed twice'" frames the bound against a rejected alternative rather than stating it.
- **W4 proof**: "(count: W9a)" — W4 needs only that the cut-points `S_i` strictly increase past `m` (immediate from `N_i ≥ 1`); the forward pointer to W9a's *count formula* is gratuitous, since W4 produces no count.

**Required**: Remove the recaps, realism assertions, and the gratuitous forward pointer; retain the substantive justifications.

### Issue 4: Duplicated caveat and a self-answered open question (anti-bloat)

- The multi-document non-monotonicity caveat is stated twice: at the end of W6 ("The address key is allocation-monotone only *within a single home document*… That multi-document case is deferred here") and again as Open Question 1. Two paragraphs deferring to the same downstream location.
- **Open Question 6**: "Under what conditions on the ordering key is the no-gap/no-duplicate partition of W4 preserved across state changes, rather than only against a frozen matching set?" W5 answers exactly the no-skip/no-duplicate part (clause 1 / state-stability), and W7 shows the *full single-set partition* cannot persist across mutation at all (there is no single `Match` to partition), making the residual ill-posed. As written, OQ6 re-asks what W5 settles.
- Minor: W7's opening restates M-mut's mechanism verbatim ("still resident in `dom(Σ.L)`, no longer discoverable") already imported in the State section; keep W7's distinctive content (present-tense completeness motivating W8) and drop the re-derivation.

**Required**: State the multi-document caveat once (W6 or OQ1, not both). Drop OQ6 or sharpen it to the genuine residual beyond W5/W7. Trim W7's restatement of M-mut.

## OUT_OF_SCOPE

None. The genuinely future-territory topics (multi-document global ordering, eventual-delivery guarantees, cross-window completeness invariants) are correctly confined to the Open Questions section rather than claimed; the out-of-scope operations named in the Scope block (count-only, full-set, MAKELINK, FOLLOWLINK, BEBE) are not given claims here.

VERDICT: REVISE
