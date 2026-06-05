# ASN-0108 Claim Statements

*Source: ASN-0108-findnextnlinksfromtothree-operation.md (revised 2026-06-04) — Extracted: 2026-06-05*

## Definition — MatchingSet

`Match(q, Σ) ⊆ dom(Σ.L)` — the links the request presently reaches, determined at each state `Σ` by query `q`.

- **(M-fin)** `Match(q, Σ)` is finite, being a subset of the finite `dom(Σ.L)` (L-fin).
- **(M-mut)** `Match(q, ·)` is *not* monotone in state evolution. It may gain members — a link created between calls (L12a adds to `dom(Σ.L)`) — and it may lose members — a link whose endpoint content is removed from every consulted arrangement ceases to be discoverable while remaining permanently in the store (orphaning, ASN-0098 LP17; persistence without discoverability, LP13).

---

## Definition — EnumerationOrder

An **ordering key** is a function `κ` assigning to each link address a value in some totally-ordered set `(K, <_K)`. The enumeration order is defined by

> `a ≺ b  ≡  κ(a) <_K κ(b)`.

For `≺` to order `Match` as needed, `κ` must be injective on it.

---

## Definition — SuccessorSet

> `After(c, Σ)  =  { a ∈ Match(q, Σ) : κ(c) <_K κ(a) }`,  and  `After(⊥, Σ) = Match(q, Σ)`.

The next window is the `≺`-least `min(N, |After(c, Σ)|)` elements of `After(c, Σ)`.

---

## Definition — Window

> `Window(q, c, N, Σ)  =  the ≺-least min(N, |After(c, Σ)|) elements of After(c, Σ)`.

The **next cursor** returned to the caller is the `≺`-maximum of `Window` (the last link of the batch), or `c` unchanged if the window is empty.

---

## W0 — TotalEnumerationOrder (LEMMA, lemma)

On `Match(q, Σ)`, the relation `≺` induced by an injective key `κ` into a totally-ordered codomain is a strict total order: irreflexive and transitive (inherited from `<_K`), and trichotomous (any two distinct matching links are `≺`-comparable, since `κ` injective gives `κ(a) ≠ κ(b)`, and `<_K` is total). A finite totally-ordered set has a unique enumeration; so `Match(q, Σ)` has a unique listing `a_1 ≺ a_2 ≺ … ≺ a_m`.

---

## W1 — PositionUniqueness (LEMMA, lemma)

No two distinct matching links occupy the same enumeration position. The rank map `rank_Σ : Match(q, Σ) → {1, …, m}` sending the `≺`-least to `1` and counting up is a bijection; in particular it is injective. This is the formal content of "no two links could ever share a position": it is exactly the injectivity of `κ` on the matching set, and it is what lets "the `k`-th matching link" denote unambiguously.

---

## W2 — CursorByIdentity (PRE, requires)

The cursor is the *identity* of the last link returned — a permanent link address — and not a positional offset into the result list. Resumption is defined relative to the cursor's key, not relative to a count of how many links preceded it.

Postcondition demanded of any resume step:

> `R  ≡  the delivered window = the ≺-least min(N, |After(c, Σ')|) elements of After(c, Σ')`

Weakest preconditions under each cursor design:

- *Identity cursor:* `wp(resume_id, R)  ≡  κ(c) recoverable`
- *Offset cursor (sufficient, not weakest):* `frozen-prefix(resume_offset)  ≡  |{a ∈ Match(q, Σ') : κ(a) ≤_K κ(c)}| = j`
- *Offset cursor (genuine weakest):* `wp(resume_offset, R)  ≡  j' = j  ∨  (j ≥ m' ∧ j' ≥ m')`

where `j` is the count of links already delivered, `j' = |{a ∈ Match(q, Σ') : κ(a) ≤_K κ(c)}|`, and `m' = |Match(q, Σ')|`.

Three conditions nest strictly: membership-identity ⟹ frozen-prefix `j' = j` ⟹ the genuine weakest.

---

## W3 — DeterministicWindow (INV, predicate)

`Window(q, c, N, Σ)` is a deterministic function of its arguments alone. It reads no hidden per-reader session state. Two requests with the same `(q, c, N)` against the same `Σ` return the identical batch. The protocol is *stateless* in the sense that the server retains nothing between calls: the entire continuation state the reader needs is the cursor it carries, and re-presenting the same cursor re-derives the same continuation.

---

## W4 — PartitionUnderStability (LEMMA, lemma)

Against a fixed `(M, κ)`, the successive windows `W_0, W_1, W_2, …` are pairwise disjoint, consecutive in `≺`, and their union is all of `M`, each link appearing exactly once. The reader sees every matching link, in `≺`-order, with no gap and no repeat.

*Formal structure (variable window sizes `N_i ≥ 1` permitted):* Define cumulative cut-points `S_0 = 0` and `S_{i+1} = S_i + N_i`. Then `W_i` is the block of ranks `[S_i+1, … , min(S_{i+1}, m)]`. Consecutive blocks share no rank (disjoint) and abut (consecutive); the union over `i` is ranks `1 … m` (cover, each once).

Bound function: `t_i = |After(c_i, Σ)| = m - S_i` strictly decreases by `N_i ≥ 1` per call that delivers a full batch; the loop stops on the first short window (fewer than the size `N_i` requested on that call, possibly zero).

---

## W5 — OrderStability (PRE, requires)

Resumption past a cursor `c` is well-defined across `Σ → Σ'` only if the ordering key preserves the cursor's *cut-point* and the relative `≺`-order *among the links in `After(c, ·)`* — the unseen tail the next window draws from. Precisely:

- **(clause 1 — cut-point preservation):** the cursor's discrimination is unchanged — for every `a` matching in both states, `κ_{Σ'}(c) <_K κ_{Σ'}(a) ⟺ κ_Σ(c) <_K κ_Σ(a)`.
- **(clause 2 — tail-order preservation):** for every pair `a, b` lying in the tail in `Σ` (`κ_Σ(c) <_K κ_Σ(a)` and `κ_Σ(c) <_K κ_Σ(b)`), `κ_{Σ'}(a) <_K κ_{Σ'}(b) ⟺ κ_Σ(a) <_K κ_Σ(b)`.

This necessary condition is *tight*: the relative order of two *already-delivered* links `a, b` with `κ(a), κ(b) <_K κ(c)` may swap freely between calls without disturbing resumption. Absolute key invariance — `κ_{Σ'}(a) = κ_Σ(a)` for every surviving link — is the *simplest sufficient* discipline (implies both clauses) but is strictly stronger than necessary.

---

## W6 — AllocationMonotoneKeyGivesMonotoneAppend (LEMMA, lemma)

If the ordering key is *allocation-monotone* — a link allocated later receives a key strictly greater than every key already issued — then a newly created matching link is `≺`-greater than every previously enumerated link: append-at-tail.

The forward direction only is claimed: allocation-monotone ⟹ append-at-tail. The converse (append-at-tail ⟹ allocation-monotone) is *not* asserted and does not hold in general.

Under an address-based key the forward hypothesis holds within a single home document's link allocator, whose successive links carry strictly increasing addresses (foundation T9, forward allocation; a single allocator chain is strictly increasing). Under a content-position key the hypothesis fails: a new link's key is the position of *its endpoint content*, which may sort anywhere — before, between, or after existing keys.

---

## W6a — CreationDoesNotDisturbSeenLinks (LEMMA, lemma)

For any key that is a function of `(address, matched-content-position)`, the *creation* of `a_new` does not alter the key or the relative order of any already-enumerated link.

*Justification (frame fact):* link creation is a `K.λ` operation (ASN-0093), whose frame leaves the arrangement family `M` and the content store `C` unchanged and adds only a fresh address to `dom(Σ.L)` (addresses are never reused). So creation alters neither any existing link's *address* (no address is reused) nor any existing link's *matched-content position* (`M` and `C` are framed, so no matched endpoint moves). Hence under *any* key that is a function of `(address, matched-content-position)` — which covers both the address key `κ(a) = a` and the content-position key alike — every already-enumerated link retains its key, and thereby its relative `≺`-order (W5). Creation can only *insert* into the order; it never *permutes* the part already seen. The hazard of W6 is one of omission (a new link landing behind the cursor), never of duplication or reordering of delivered links.

---

## W7 — ResultMembershipNonMonotone (LEMMA, lemma)

`Match(q, ·)` may lose members across evolution even though `dom(Σ.L)` only grows. A link delivered in window `i` may be absent from the recomputed matching set at window `j > i` if, between the calls, its matched endpoint content was removed from every consulted arrangement — the link is then orphaned: still permanently resident in `dom(Σ.L)` (LP13 of ASN-0098), its stored value immutable (L12 of ASN-0043), but no longer discoverable (LP17). Windowed completeness (W4) is therefore *relative to a fixed state*; across mutation, a link the reader already saw may no longer be among the matchers, and the total it is paging toward may shrink.

---

## W8 — CursorSurvivesUnderStableKey (LEMMA, lemma)

Resumption past a cursor `c` is well-defined whenever `κ(c)` is recoverable, *even if `c` itself has left `Match`*. `After(c, Σ')` is defined by `κ(c)` alone — it does not require `c ∈ Match(q, Σ')`.

- With a state-stable key (W5), `κ(c)` survives the disappearance of `c`, so the reader can continue past a cursor whose link has been deleted or orphaned.
- With an address-based key this is unconditional: the cursor's address — hence its key — is permanent (T8) regardless of whether the link still matches.
- With a content-derived key, the cursor's key may itself become irrecoverable when the content it was drawn from is gone; then the successor set collapses and the call returns the empty window — *indistinguishable from genuine exhaustion* (W9).

---

## W9 — ExhaustionByShortWindow (LEMMA, lemma)

*Provided the cursor key is recoverable* — that `κ(c)` still names its cut-point against the current set — a window returning fewer than `N` links signals exhaustion: every matching link reachable past the cursor has been delivered.

Formally, when `κ(c)` is recoverable:

> `|Window(q, c, N, Σ)| < N ⟹ After(next-cursor, Σ) = ∅`

The reader detects the end by comparing the batch size against the requested `N`; a short — possibly empty — batch is the terminal signal. "Fewer than `N`" includes zero: a reader that stops only on a strictly-positive short batch (`0 < |batch| < N`) will miss the exact-multiple terminator.

The recoverability proviso is essential: absent recoverability, a short window is indistinguishable from cursor-invalidation (W8), not genuine exhaustion. "Short window ⟹ exhaustion" holds unconditionally only when the cursor key is recoverable, which an address-based key supplies for free (W8) since the permanent address remains a valid cut-point regardless of membership (T8).

---

## W9a — TerminationGuaranteed (LEMMA, lemma)

Against a fixed matching set of size `m`, and *for the constant schedule `N_i = N`* (a fixed window size held across every call), the paging loop terminates in exactly

> `⌈m / N⌉ + [N divides m]`

calls, the bound function `m - iN` decreasing by `N` each non-final call until it falls below `N`.

Over a *mutating* matching set, the sufficient termination condition is: **cut-point preservation at each successive cursor (W5's clause 1) together with finite tail inflow**. Termination reflects exhaustion of the reachable tail, not of the whole matching set.

- *Instantaneous boundedness of the tail is not sufficient:* if each call consumes the single link then in the tail while exactly one fresh matching link is created ahead of the cursor between every two calls, the instantaneous tail is always size 1 — bounded — yet every window is full and the loop runs forever.
- *The genuinely sufficient condition:* finite total tail inflow together with cut-point preservation at each successive cursor. When inflow is finite, the total consumable population is finite; cut-point preservation guarantees no delivered link ever re-ascends above the advancing cursor, so no link is consumed twice, and the finite supply is exhausted in finitely many calls.
- *Absent cut-point preservation, even zero inflow can loop forever:* a key violating cut-point preservation can lift a previously delivered link's key back above the current cursor, returning it to the tail to be re-delivered indefinitely.
- *Tail-order preservation (W5 clause 2) is sufficient via full W5 but not necessary for termination:* clause 2 failure reshuffles only the order of delivery, not whether the pass ends.
- *Growth behind the cursor (keys `< κ(c)`) cannot impede termination:* the W6 blind spot, invisible to the loop.

---

## W10 — CursorCarriesNoAbsoluteProgress (INV, predicate)

The cursor exposes only the resume key — enough to request the next window — and reveals neither the rank of the cursor within `Match(q, Σ)` nor the cardinality `|Match(q, Σ)|`. The window reply is a batch of `≤ N` links and no more; it carries no "position `k` of `m`" field. Absolute progress is therefore *not derivable from the windowed protocol alone*. A reader who wants "`k` of `m`" must obtain `m` from a separate cardinality query — a distinct operation, out of scope here — and tally `k` itself by counting delivered links.

---

## W11 — BoundaryObjectivity (LEMMA, lemma)

The boundary between successive windows is fixed by `(q, c, N, Σ)` through the deterministic `Window` function (W3). Any two readers issuing the same query with the same cursor and the same `N` against the same state receive the identical batch and the identical next cursor. The split is a system property — determined by the enumeration order and the window size — not a reader-side choice. What a reader may freely vary is only `N` (how much to take per call) and how it *displays* the results; *where* the cut falls, for a given `N`, is objective.
