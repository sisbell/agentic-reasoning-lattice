# ASN-0108: FINDNEXTNLINKSFROMTOTHREE Operation

*2026-06-04*

## The Question

A link search can produce an avalanche. The matching set for a broad request may be larger than the caller wishes to receive, or can hold, in one reply. So the system hands the matching links back a *window* at a time: the caller asks for "no more than `N` links past the one I last saw", receives a batch, and asks again, marking its place by the last link of the batch. Nelson designed the protocol this way deliberately — "the quantity of links not satisfying a request does not in principle impede search on others" (LM 4/60) — so that a reader can page through results incrementally without the volume defeating the search.

Our task is to say, with precision, what windowed retrieval must guarantee. Four sub-questions sharpen the topic, and they are not independent:

- **Order.** In what order do matching links arrive, and what makes that order well-defined?
- **Stability.** What does the enumeration order preserve as the system evolves *between* one window request and the next?
- **Termination.** How does the reader know the final window has come and every matching link has been seen?
- **Progress.** How does the reader know how far along it is?

We are looking for the abstract laws — the claims any correct windowing implementation must honour, whatever index it walks. We develop the windowed operation as resumable enumeration of a state-dependent matching set under a total order, and we will find that the order's *choice of key* is the single decision on which the no-skip guarantee turns.

## State, the Matching Set, and What Windowing Operates On

We work over the link store `Σ.L : T ⇀ Link` of ASN-0043: a partial function from tumbler addresses to link values, finite at every reachable state (L-fin), monotone non-decreasing across transitions (L12a), with entries immutable once written (L12). An endset denotes an address set through `coverage(e)` (ASN-0043), a combinatorial projection of its spans consulting no state component.

A windowed request fixes a query `q` — its from, to, and type parts — and we take for granted that `q` determines, at each state `Σ`, a finite **matching set**

> `Match(q, Σ) ⊆ dom(Σ.L)`

the links the request presently reaches. We deliberately do *not* re-derive the satisfaction predicate here: which links match, and against which anchoring, is the concern of the full-set and count operations and lies outside this note. Windowing takes the matching set as given and asks only how to *deliver* it in resumable batches. We import exactly two qualitative facts about `Match`, both derivable from the foundations, and use nothing more:

- (M-fin) `Match(q, Σ)` is finite, being a subset of the finite `dom(Σ.L)` (L-fin).
- (M-mut) `Match(q, ·)` is *not* monotone in state evolution. It may gain members — a link created between calls (L12a adds to `dom(Σ.L)`) — and it may lose members — a link whose endpoint content is removed from every consulted arrangement ceases to be discoverable while remaining permanently in the store (orphaning, ASN-0098 LP17; persistence without discoverability, LP13). This stands in contrast to `dom(Σ.L)` itself, which only grows.

The asymmetry in (M-mut) is the source of every subtlety to come. The store is append-only; the *view the request reaches* is not.

## The Enumeration Order

Windowing means resumption: each batch must continue exactly past where the last ended. That is meaningless unless the matching set carries a definite order in which "past the last one" picks out a unique remainder. So before anything else we must equip `Match` with an order, and the order must be *total* — Nelson is explicit that a span on the tumbler line never leaves two addresses incomparable (the line is a total order, foundation T1), and the result list inherits that linearity.

We posit an **ordering key**: a function `κ` assigning to each link address a value in some totally-ordered set `(K, <_K)`, and define the enumeration order by

> `a ≺ b  ≡  κ(a) <_K κ(b)`.

For `≺` to order `Match` as we need, `κ` must be injective on it. We record the requirement and its immediate consequences.

> **W0 (TotalEnumerationOrder).** On `Match(q, Σ)`, the relation `≺` induced by an injective key `κ` into a totally-ordered codomain is a strict total order: irreflexive and transitive (inherited from `<_K`), and trichotomous (any two distinct matching links are `≺`-comparable, since `κ` injective gives `κ(a) ≠ κ(b)`, and `<_K` is total). A finite totally-ordered set has a unique enumeration; so `Match(q, Σ)` has a unique listing `a_1 ≺ a_2 ≺ … ≺ a_m`.

> **W1 (PositionUniqueness).** No two distinct matching links occupy the same enumeration position. The rank map `rank_Σ : Match(q, Σ) → {1, …, m}` sending the `≺`-least to `1` and counting up is a bijection; in particular it is injective. This is the formal content of "no two links could ever share a position": it is exactly the injectivity of `κ` on the matching set, and it is what lets "the `k`-th matching link" denote unambiguously.

W0 and W1 are abstract: any implementation, however it walks its indices, must deliver the matching links in *some* fixed total order, or the phrase "past that link on that list" (LM 4/69) has no referent. What it must not do is leave the order ambiguous — return links in an order that is recomputed differently between calls, or that admits ties.

**What `κ` is, concretely — two readings, and the discrepancy that matters.** The design intent and the implementation evidence name *different* keys, and the difference is the heart of this note.

- *Nelson's reading: the key is the link's own permanent address.* Links homed in a document are "in their permanent order of arrival" (LM 4/31); each is assigned a sequential creation-order address that is never renumbered and never reused. Under `κ(a) = a` — ordering by the link's tumbler address — the enumeration is exactly arrival order within a home document. We adopt this as the *intended* key.

- *Gregory's reading: the key is the position of the matched content.* The udanax-green implementation orders the result list not by link address but by the address of the *content endpoint* each link matched, established by an insertion-sort during the index traversal (the sort key is the matched span's boundary, not the link's identity). Two links homed adjacently can therefore arrive far apart, and a link's place in the list is governed by *where its endpoint sits*, not by *when the link was made*.

A caution at once: the bare content-position key is **not injective on `Match`**, and therefore fails W0's injectivity premise and W1's position-uniqueness directly. Two distinct matching links can reference the same content endpoint — the same matched-span boundary — yielding `κ(a) = κ(b)` for `a ≠ b`. The implementation evidence is concrete: the insertion-sort that builds the result list keys solely on the matched span's start boundary and provides *no* secondary comparison on link address; when two links tie at the same boundary their relative order is decided by traversal-insertion accident (a head-tie prepends, a mid-list tie appends), never by a permanent tiebreaker. Such ties are exactly what W0 and W1 forbid. To make the content-position reading order `Match` at all, the key must be composed with a permanent tiebreaker — `κ(a) = (endpoint-position, a)` — appending the link's own address as the low-order component to restore injectivity. We carry the content-position key *only in this composite form* whenever we speak of it satisfying W0–W5; the uncomposed boundary-only key does not order the matching set.

We do not elevate either key to a claim — the choice is a design parameter. What we *can* state abstractly is which key-properties each guarantee below requires. The discrepancy is not a detail: it decides whether a newly created link appends at the tail or can be silently skipped (W6), and whether the cursor survives deletion of the content it marked (W8).

## The Cursor: Identity, Not Offset

A window request carries a **cursor** `c` — the marker by which the reader names its place — and a size `N ≥ 1`. The cursor is either the start sentinel `⊥` (begin at the head) or a link the reader last received. The crucial design decision is *what kind of thing* the cursor is.

> **W2 (CursorByIdentity).** The cursor is the *identity* of the last link returned — a permanent link address — and not a positional offset into the result list. Resumption is defined relative to the cursor's key, not relative to a count of how many links preceded it.

Why must it be identity and not offset? Consider the weakest precondition for correct resumption. We want the next window to contain exactly the links that follow the cursor and none already seen. Write the **successor set**

> `After(c, Σ)  =  { a ∈ Match(q, Σ) : κ(c) <_K κ(a) }`,  and  `After(⊥, Σ) = Match(q, Σ)`.

The next window is the `≺`-least `min(N, |After(c, Σ)|)` elements of `After(c, Σ)`. Now ask: does this definition resume correctly across a state change `Σ → Σ'`? An *offset* cursor names "resume at the 100th". If links are inserted before position 100, or deleted before it, the 100th element of `Σ'` is not the successor of the 100th element of `Σ` — the offset slides under insertion and deletion, producing overlap or omission. An *identity* cursor names a specific link; `After(c, Σ')` is computed afresh from `κ(c)` against the current matching set, so it picks up exactly past that link regardless of what else changed. The wp of "no link seen twice and none skipped" over a mutable result set is satisfiable by an identity cursor and not by an offset cursor. This is the abstract justification for Nelson's "items past *that link* on that list" rather than "items 100 through 200": the anchor must be a position-in-the-order *named by identity*, immune to renumbering.

We can now state the operation. Given `(q, c, N, Σ)`, the window is

> `Window(q, c, N, Σ)  =  the ≺-least min(N, |After(c, Σ)|) elements of After(c, Σ)`,

and the **next cursor** returned to the caller is the `≺`-maximum of `Window` (the last link of the batch), or `c` unchanged if the window is empty.

> **W3 (DeterministicWindow).** `Window(q, c, N, Σ)` is a deterministic function of its arguments alone. It reads no hidden per-reader session state. Two requests with the same `(q, c, N)` against the same `Σ` return the identical batch. The protocol is *stateless* in the sense that the server retains nothing between calls: the entire continuation state the reader needs is the cursor it carries, and re-presenting the same cursor re-derives the same continuation.

W3 records a structural fact the evidence is emphatic about: there is no server-side iterator, no cached list, no generation counter. Each call re-derives `Match(q, Σ)` and `After(c, Σ)` from scratch. The only thing that persists across calls is the cursor in the reader's hand. We treat this as abstract because *any* implementation that wishes resumption to survive crashes, reconnections, and concurrent readers must locate the continuation state in the cursor rather than in the server — a session iterator over a mutable set is exactly what the stateless design refuses.

## No Gap, No Duplicate — Under Stability

We can now prove the central pagination-correctness property, and see precisely what it depends on. Suppose a reader pages through to exhaustion: `c_0 = ⊥`, and `c_{i+1}` = the next cursor returned by the `i`-th window. Suppose further — for now — that the matching set and the key are *unchanged* across the whole run: `Match(q, Σ) = M` fixed, `κ` fixed.

> **W4 (PartitionUnderStability).** Against a fixed `(M, κ)`, the successive windows `W_0, W_1, W_2, …` are pairwise disjoint, consecutive in `≺`, and their union is all of `M`, each link appearing exactly once. The reader sees every matching link, in `≺`-order, with no gap and no repeat.

*Proof.* Let `M = {a_1 ≺ a_2 ≺ … ≺ a_m}` (W0). We show by induction that `W_i` is the block of ranks `[iN+1, … , min((i+1)N, m)]`. Base: `After(⊥) = M`, and `W_0` is its `≺`-least `min(N, m)` elements — ranks `1 … min(N, m)`; its `≺`-max is `a_{min(N,m)}`, so `c_1 = a_{min(N,m)}`. Step: assume `c_i = a_{iN}` (when `iN ≤ m`). Then `After(c_i) = {a_{iN+1}, …, a_m}` — exactly the links whose key exceeds `κ(a_{iN})`, by W0's strict order — and `W_i` takes its least `min(N, m-iN)` elements, ranks `iN+1 … min((i+1)N, m)`. Consecutive blocks share no rank (disjoint) and abut (consecutive). The union over `i` is ranks `1 … m` (cover, each once). Termination: the bound function `t_i = |After(c_i, Σ)| = m - iN` strictly decreases by `N ≥ 1` per call that delivers a full batch, and the loop stops on the first window that is *short* (fewer than `N`, possibly zero). Two regimes: when `N` does *not* divide `m`, the final non-empty window is already short — it carries the remainder `m mod N ∈ {1, …, N-1}` — and the reader stops *on that window*, with no extra empty call. When `N` divides `m`, every non-empty window is full, the last full window leaves `t = 0`, and exactly *one additional* empty call is needed to expose the short (zero) signal. The total call count is thus `⌈m/N⌉ + [N divides m]` (the extra `+1` precisely when `N | m`), matching W9a. ∎

W4 is the no-skip/no-duplicate guarantee — but read the hypothesis. It assumed `(M, κ)` *fixed*. The guarantee is unconditional only against a frozen result set. The moment the matching set or the key moves between calls, the proof's induction step — "`After(c_i)` is exactly the tail past rank `iN`" — can fail. The rest of this note is the study of what survives when the hypothesis is relaxed, and what conditions restore it.

## Stability of the Order Across Evolution

For resumption to remain coherent across a real state change, the *order itself* must not be rewritten under the reader's feet. Two links the reader has already seen must keep their relative order; the link it stopped at must keep the same key, so "past that link" still cuts the set in the same place.

> **W5 (OrderStability).** Resumption is well-defined across `Σ → Σ'` only if the ordering key preserves *relative order* among the links present and matching in both states, and preserves the cursor's cut-point. Precisely: for every pair `a, b` matching in both states, `κ_{Σ'}(a) <_K κ_{Σ'}(b) ⟺ κ_Σ(a) <_K κ_Σ(b)`; and for every such `a`, the cursor's discrimination is unchanged — `κ_{Σ'}(c) <_K κ_{Σ'}(a) ⟺ κ_Σ(c) <_K κ_Σ(a)`. Absolute key invariance — `κ_{Σ'}(a) = κ_Σ(a)` for every surviving link — is the *simplest sufficient* discipline: it trivially implies both preservations. But it is stronger than necessary. A key that shifts every value uniformly (say, every key incremented by a fixed amount) violates absolute invariance yet preserves every comparison `κ_{Σ'}(c) <_K κ_{Σ'}(a)`, so resumption stays well-defined. What resumption actually requires is that the order not be *permuted* under the reader's feet and that the cut "past the cursor" fall in the same place; absolute invariance is one way to secure this, not the only way. Without relative-order preservation, the successor set `After(c, Σ')` no longer continues the enumeration the reader was traversing.

W5 is a requirement, and it discriminates the two candidate keys sharply. An **address-based key** `κ(a) = a` is absolutely invariant *unconditionally* — hence relative-order preserving, the sufficient condition met for free: a link's address is permanent — never changed, never reused (foundation T8, allocation permanence) — so the order of any two surviving links is frozen for the lifetime of the search, exactly as Nelson requires ("links keep their creation-order addresses permanently"; deleting one "doesn't renumber" the others). A **content-position key** preserves relative order only while the matched content keeps its relative arrangement; an edit that moves one endpoint past another permutes the order, and the enumeration the reader was walking is silently re-laid. Order-stability is therefore the first concrete advantage of ordering by link identity over ordering by matched-content position: the sufficient discipline (absolute invariance) is free for the former and not even the weaker necessary condition is guaranteed for the latter.

## Where New Links Land

Suppose a link is *created* partway through a windowed reading. Where must it appear relative to the links already delivered? Nelson's answer is unambiguous: at the tail. "Any link that comes into being during a windowed reading must fall *after* all links already received" — the ordering is append-only, which is exactly what makes "show me what has arrived since I last looked" well-defined (LM 4/55). But whether the system *realises* append-at-tail is not a free fact; it follows from a property of the key.

> **W6 (AllocationMonotoneKeyGivesMonotoneAppend).** If the ordering key is *allocation-monotone* — a link allocated later receives a key strictly greater than every key already issued — then a newly created matching link is `≺`-greater than every previously enumerated link: append-at-tail. We claim only this forward direction, which is the one the analysis below uses. We do *not* assert the converse (append-at-tail ⟹ allocation-monotone), and it does not hold in general: append-at-tail quantifies only over the *enumerated matching* links, whereas allocation-monotonicity is a property of *all* allocated links, so a key could append every matching link at the tail while ordering non-matching links arbitrarily. Under an address-based key the forward hypothesis holds within a single home document's link allocator, whose successive links carry strictly increasing addresses (foundation T9, forward allocation; a single allocator chain is strictly increasing). Under a content-position key the hypothesis fails: a new link's key is the position of *its endpoint content*, which may sort anywhere — before, between, or after existing keys — so the append-at-tail conclusion is unavailable.

The consequence under a content-position key is the *blind spot*. Let the reader's cursor sit at `c`, and let a link `a_new` be created between calls whose endpoint content sorts *below* `κ(c)`. Then `κ(a_new) <_K κ(c)`, so `a_new ∉ After(c, Σ')`: the new link lands permanently behind the cursor and is never delivered in this pagination pass, though it genuinely matches. The cursor faithfully marks the reader's place; nothing is corrupted; yet a matching link is silently skipped. This is not a bug in the cursor — it is the unavoidable cost of pairing stateless re-execution with a key that is not allocation-monotone. With an address-based key the hazard vanishes for links homed where the reader is paging, because fresh addresses there exceed every prior key.

> **W6a (CreationDoesNotDisturbSeenLinks).** Regardless of key, the *creation* of `a_new` does not alter the key or the relative order of any already-enumerated link: addresses are not reused, so no existing key changes (W5). Creation can only *insert* into the order; it never *permutes* the part already seen. The hazard of W6 is one of omission (a new link landing behind the cursor), never of duplication or reordering of delivered links.

The reconciliation: Nelson's append-at-tail is the *intended* behaviour, and it is *attained* exactly when the key is the link's permanent arrival-order address. An implementation that orders by matched-content position can satisfy W0–W5 *only once its key is composed with a permanent link-address tiebreaker* (the composite `κ(a) = (endpoint-position, a)` of the previous section); the uncomposed boundary-only key fails W0/W1 outright by admitting ties. Even in the composite form, the content-position key forfeits W6's append guarantee — the high-order endpoint-position component is not allocation-monotone — and so admits the blind spot. An alternative implementation seeking Nelson's guarantee must adopt an allocation-monotone key, which the address-based key supplies directly.

## Disappearance and Cursor Survival

The dual of a link appearing late is a link *vanishing*. A link enumerated in an earlier window can be absent from a later one — not because anything removed it from the store, but because it ceased to match.

> **W7 (ResultMembershipNonMonotone).** `Match(q, ·)` may lose members across evolution even though `dom(Σ.L)` only grows. A link delivered in window `i` may be absent from the recomputed matching set at window `j > i` if, between the calls, its matched endpoint content was removed from every consulted arrangement — the link is then orphaned: still permanently resident in `dom(Σ.L)` (L12, L13 of ASN-0098), but no longer discoverable (LP17). Windowed completeness (W4) is therefore *relative to a fixed state*; across mutation, a link the reader already saw may no longer be among the matchers, and the total it is paging toward may shrink.

This forces a careful reading of "the reader has seen them all". It can only mean: the reader has seen every link that matches *at the states its successive calls observed*. There is no single frozen population the windowed protocol enumerates; there is a sequence of populations, one per call, and the cursor stitches them. The completeness W4 guarantees is completeness against each call's own matching set.

W7 raises a hazard for the cursor: what if the link the reader stopped at is itself the one that vanished? Here the key choice pays a second dividend.

> **W8 (CursorSurvivesUnderStableKey).** Resumption past a cursor `c` is well-defined whenever `κ(c)` is recoverable, *even if `c` itself has left `Match`*. `After(c, Σ')` is defined by `κ(c)` alone — it does not require `c ∈ Match(q, Σ')`. With a state-stable key (W5), `κ(c)` survives the disappearance of `c`, so the reader can continue past a cursor whose link has been deleted or orphaned. With an address-based key this is unconditional: the cursor's address — hence its key — is permanent (T8) regardless of whether the link still matches. With a content-derived key, the cursor's key may itself become irrecoverable when the content it was drawn from is gone; then the successor set collapses and the call returns the empty window — *indistinguishable from genuine exhaustion* (W9). This ambiguity is the abstract hazard of an identity cursor whose key is not state-stable.

W8 is the strongest structural argument for ordering by permanent link address: it makes the cursor robust to deletion. A reader can hand back the address of a link that has since been withdrawn, and the system still knows where to continue, because the address still has a definite place in the order.

## Termination: The Short Window

How does the reader learn the final window has come? Not from a terminal marker — none is required — but from the *length* of the batch.

> **W9 (ExhaustionByShortWindow, under a recoverable cursor key).** *Provided the cursor key is recoverable* — equivalently, provided the key is state-stable in the sense of W5, so that `κ(c)` still names the same cut-point — a window returning fewer than `N` links signals exhaustion: every matching link reachable past the cursor has been delivered. Formally, when `κ(c)` is recoverable, `|Window(q, c, N, Σ)| < N ⟹ After(next-cursor, Σ) = ∅`. The reader detects the end by comparing the batch size against the requested `N`; a short — possibly empty — batch is the terminal signal. The recoverability proviso is essential and not cosmetic: W8 exhibits the counterexample. When the key is *not* state-stable and the cursor's content has been removed, `κ(c)` becomes irrecoverable, the successor set collapses, and the call returns an empty window that is *indistinguishable from genuine exhaustion* — a short window then signals cursor-invalidation, not exhaustion. So "short window ⟹ exhaustion" holds unconditionally only in the regime W8 identifies as safe: a recoverable (state-stable) cursor key, which an address-based key supplies for free (W8).

*Derivation.* Assume `κ(c)` recoverable, so `After(c, Σ)` continues the enumeration the reader was traversing. `Window` returns `min(N, |After(c, Σ)|)` links. If this is `< N`, then `|After(c, Σ)| < N`, the whole successor set fit in the batch, and the new successor set is empty: nothing remains. Contrapositive: a *full* batch of exactly `N` means the reader must call again — possibly to receive more, possibly to learn there is no more.

The boundary case is the one an implementation must get right. If `|Match|` is an exact multiple of `N`, the last *full* window delivers the final `N` links and looks no different from a non-final window; the reader, seeing a full batch, calls once more and receives an **empty** window — count zero — which is the short-window signal in its degenerate form. So "fewer than `N`" must be read as *including zero*, and a reader that stops only on a strictly-positive short batch will miss the exact-multiple terminator and loop one call too few. The empty window is not an error; it is the proof of completeness.

> **W9a (TerminationGuaranteed).** Against a fixed matching set of size `m`, the paging loop terminates in exactly `⌈m / N⌉ + [N divides m]` calls, the bound function `m - iN` decreasing by `N` each non-final call until it falls below `N`. Over a *mutating* matching set the loop still terminates whenever the set does not grow without bound below the cursor — but W7 and W6 show that under a non-allocation-monotone key, growth below the cursor is invisible to the loop, so termination reflects exhaustion *of the reachable tail*, not of the matching set as a whole.

*Two concrete walks, `N = 2`.* Fix a stable address-keyed enumeration so W4 applies, and trace the cursor and the batch sizes against the W9/W9a formulas.

- *Exact multiple: `m = 4`* (links `a_1 ≺ a_2 ≺ a_3 ≺ a_4`). Call 1: `After(⊥) = {a_1,…,a_4}`, window `{a_1, a_2}` (size 2 = `N`, full), cursor `→ a_2`. Call 2: `After(a_2) = {a_3, a_4}`, window `{a_3, a_4}` (size 2 = `N`, full — *looks no different from a non-final window*), cursor `→ a_4`. Seeing a full batch, the reader must call again (W9 contrapositive). Call 3: `After(a_4) = ∅`, window `{}` (size 0 < `N`, short), the W9 terminal signal. Total **3 calls** = `⌈4/2⌉ + [2|4] = 2 + 1`. The trailing empty call is the degenerate short window — present precisely because `N | m`.

- *Non-divisible: `m = 5`* (links `a_1 ≺ … ≺ a_5`). Call 1: window `{a_1, a_2}` (full), cursor `→ a_2`. Call 2: window `{a_3, a_4}` (full), cursor `→ a_4`. Call 3: `After(a_4) = {a_5}`, window `{a_5}` (size 1 < `N`, *short*) — the reader stops *here*, on a non-empty short window, with no extra empty call. Total **3 calls** = `⌈5/2⌉ + [2|5] = 3 + 0`. Contrast the divisible case: the remainder `5 mod 2 = 1` rides out in the last delivered batch, so the short signal arrives *with content* rather than in a separate empty call.

Both walks confirm W4's partition (each `a_k` delivered exactly once, in `≺`-order), W9's short-window terminator (the stopping batch has size `< N` in each case — zero for `m = 4`, one for `m = 5`), and W9a's count formula including its `[N divides m]` term.

## Progress: What the Cursor Withholds

Finally: how far along is the reader? The windowed protocol's answer is austere — the cursor tells the reader how to continue, and nothing about its position in the whole.

> **W10 (CursorCarriesNoAbsoluteProgress).** The cursor exposes only the resume key — enough to request the next window — and reveals neither the rank of the cursor within `Match(q, Σ)` nor the cardinality `|Match(q, Σ)|`. The window reply is a batch of `≤ N` links and no more; it carries no "position `k` of `m`" field. Absolute progress is therefore *not derivable from the windowed protocol alone*. A reader who wants "`k` of `m`" must obtain `m` from a separate cardinality query — a distinct operation, out of scope here — and tally `k` itself by counting delivered links; and even then, because each windowed call re-derives the matching set (W3) and that set may move (W7), the separately-obtained `m` is only a snapshot, not a guarantee about what the next window will find.

W10 is a frame condition: it states what the operation does *not* return. The design pushes progress presentation entirely to the front end — "none of these commands are to be seen by the user … the complications of the protocol are to be handled invisibly" (LM 4/61). The back end provides the two primitives — a way to size the set, and a way to page it — and the "you are at link `k` of `m`" experience is something the front end *synthesises*, never something the windowed reply asserts. We make the boundary explicit so that no implementation mistakes the absence of a progress field for an omission to be fixed: it is a deliberate division of labour.

## Window Boundaries Are Objective

A last guarantee ties the threads together. The point at which one window ends and the next begins is not a private convenience of the reader — it is a stable property of the system, observed identically by all.

> **W11 (BoundaryObjectivity).** The boundary between successive windows is fixed by `(q, c, N, Σ)` through the deterministic `Window` function (W3). Any two readers issuing the same query with the same cursor and the same `N` against the same state receive the identical batch and the identical next cursor. The split is a system property — determined by the enumeration order and the window size — not a reader-side choice. What a reader may freely vary is only `N` (how much to take per call) and how it *displays* the results; *where* the cut falls, for a given `N`, is objective.

W11 is the windowed analogue of Nelson's principle that "you can at once ascertain the home document of any specific word or character" (LM 2/40): the structure is determinate and shared, not imposed by the viewer. Two readers paging the same search with the same window size traverse the same boundaries, because those boundaries are computed from the order and the size, both of which are properties of the system rather than of the reader.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `Match` | `Match(q, Σ) ⊆ dom(Σ.L)` — the finite (M-fin), non-monotone (M-mut) matching set windowing delivers | introduced |
| `κ` / `≺` | `a ≺ b ≡ κ(a) <_K κ(b)` — enumeration order from an injective ordering key into a total order | introduced |
| `After` | `After(c, Σ) = {a ∈ Match(q, Σ) : κ(c) <_K κ(a)}`; `After(⊥, Σ) = Match(q, Σ)` — the successor set | introduced |
| `Window` | `Window(q, c, N, Σ)` = the `≺`-least `min(N, |After(c, Σ)|)` elements of `After(c, Σ)`; next cursor = its `≺`-max | introduced |
| W0 | `≺` is a strict total order on `Match`; the matching set has a unique enumeration | introduced |
| W1 | No two distinct matching links share an enumeration position (rank is injective) | introduced |
| W2 | The cursor is a link identity (permanent address), not a positional offset; required for correct resumption over a mutable set | introduced |
| W3 | `Window` is a deterministic, stateless function of `(q, c, N, Σ)`; continuation state lives entirely in the cursor | introduced |
| W4 | Against a fixed `(Match, κ)`, successive windows partition the matching set: disjoint, consecutive, exhaustive, no repeat | introduced |
| W5 | Coherent resumption requires preservation of relative `≺`-order among links in both states and of the cursor's cut-point; absolute key invariance is the simplest sufficient discipline, attained free by an address-based key (T8), only conditionally by a content-position key | introduced |
| W6 | If the key is allocation-monotone then a new matching link appends at the tail (forward direction only; converse disclaimed); a content-position key is not allocation-monotone and admits a permanent blind spot (silent skip) | introduced |
| W6a | Creation never permutes or duplicates already-delivered links; its only hazard is omission | introduced |
| W7 | `Match(q, ·)` is non-monotone (can lose members by orphaning) though `dom(Σ.L)` only grows; completeness is relative to each call's state | introduced |
| W8 | Resumption past a cursor is well-defined whenever its key survives, even if the cursor link has left `Match`; unconditional under an address-based key | introduced |
| W9 | Under a recoverable (state-stable) cursor key, a window of fewer than `N` links (zero included) signals exhaustion; no terminal marker is needed. Absent recoverability, a short window is indistinguishable from cursor-invalidation (W8) | introduced |
| W9a | The paging loop terminates; over a mutating set, termination reflects exhaustion of the reachable tail, not of the whole matching set | introduced |
| W10 | The cursor carries only the resume key — no rank, no total; absolute progress is not derivable from the windowed protocol alone | introduced |
| W11 | Window boundaries are objective: same `(q, c, N, Σ)` yields the same batch for every reader; the cut is a system property | introduced |

## Open Questions

What must the enumeration order guarantee when the matching set spans multiple home documents whose link allocators advance independently, so that no single allocation-monotone key orders the whole result globally?

Under what conditions must a windowed reading guarantee that a link created between calls is eventually delivered, rather than permanently skipped, when the ordering key is not allocation-monotone?

What invariant must relate the matching sets observed at successive windowed calls so that the stitched-together delivery has a well-defined completeness guarantee across a mutating result set?

When the cursor link has been orphaned between calls, what must distinguish a genuinely empty successor set from an irrecoverable cursor, so that exhaustion and cursor-invalidation are not conflated?

What must the system guarantee about the relationship between the order in which windowed retrieval delivers links and the order in which any companion progress-sizing query counts them, so that a front-end "k of m" display cannot drift out of correspondence with the delivery?

Under what conditions on the ordering key is the no-gap/no-duplicate partition of W4 preserved across state changes, rather than only against a frozen matching set?
