# ASN-0088: FINDLINKS Operation

*2026-05-24*

We are looking for a specification of link discovery. A reader has selected content somewhere in some document; the system must report every link whose endsets reference that content. The promise is simple. The mechanics, on close inspection, are not.

The complication is that the user sees V-positions and the system stores links against I-addresses. By S0 (ContentImmutability, ASN-0036), I-addresses are the permanent identity of content; by S5 (UnrestrictedSharing, ASN-0036), a single I-address may inhabit many V-positions across many documents simultaneously. Two readers viewing what they perceive as identical V-content may be looking at the *same* bytes (when transclusion has placed shared I-addresses at different V-positions) or at *different* bytes that happen to read the same (when independent allocations carry the same value). Discovery must work despite — or, more precisely, *because of* — this distinction.

Nelson states the user-facing guarantee plainly: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections" [LM 2/46]. The phrase "all these outside connections" is the load-bearing one. Discovery is total. The system must enumerate every link whose endsets reference the queried bytes — not "many," not "those nearby," not "those in this document" — all of them.

We derive the specification by asking what must be true for this guarantee to hold.

## The Query Surface

What does the user supply, and what does the system actually search against?

The user supplies a V-coordinate selection: a document `d_s` together with a V-span `σ`. We capture this as a *content reference* `(d_s, σ)` in the sense of ASN-0058, satisfying the well-formedness conditions stated there. But the user's V-selection is not what the link store indexes. By the strand model, links — like any reference to content identity — are stated in I-coordinates: V-positions are mutable arrangement metadata, while I-addresses are permanent content identity. The first work the operation does is *resolve* the V-selection into an I-coordinate description.

The resolution function `resolve(d_s, σ)` (ASN-0058) returns a sequence of (I-start, width) pairs

  resolve(d_s, σ) = ⟨(a_1, n_1), …, (a_k, n_k)⟩

— one per maximal correspondence run in `M(d_s)` over `σ`'s positions. The decomposition is canonical by M11 + M12 (ASN-0058) and need not be contiguous: a V-region whose content was assembled from N different sources via transclusion will resolve into N separate I-runs, one per original allocation. The resolution is *lossy with respect to V-coordinates* (V-starts are discarded by ASN-0058's `resolve`) and *faithful with respect to I-coordinates* (every (V-position, I-address) pair in M(d_s) over σ contributes to exactly one run).

We capture the discarded-V property by lifting the resolved pairs into the span-set algebra of ASN-0053. Given resolved pairs `(a_j, n_j)`, the *I-extent* of `(d_s, σ)` is the span-set

  Iext(d_s, σ) = { (a_j, δ(n_j, #a_j)) : 1 ≤ j ≤ k }

where `δ(n_j, #a_j)` is the ordinal displacement of magnitude `n_j` at depth `#a_j` (OrdinalDisplacement, ASN-0034) and each pair `(a_j, δ(n_j, #a_j))` is the level-uniform span at I-start `a_j` of ordinal width `n_j`. Each constituent span satisfies T12 (SpanWellDefinedness, ASN-0034) by construction: `δ(n_j, #a_j)` is positive with action point `#a_j ≤ #a_j`. The span-set is then a well-formed object in the sense of ASN-0053, admitting the union, intersection, and difference machinery developed there.

The discovery operation will search against `Iext(d_s, σ)`. The conversion from V to I is performed once, by `Iext`, and the I-coordinate description is what the link store sees. The V-coordinate description is not consulted again.

## The Match Predicate

A link, by L3 (NEndsetStructure, ASN-0043), is a sequence of `N ≥ 3` endsets. Each endset is a set of spans. The slot positions are distinguishable (L6, ASN-0043) — slot 3 is conventionally the type endset; slots 1 and 2 are conventionally from and to. A query may constrain some, all, or none of these slots.

We model a *query specification* abstractly as a partial function

  Q : ℕ ⇀ SpanSet

assigning, to each constrained slot index `i ∈ dom(Q)`, a span-set `Q(i)` against which the link's i-th endset must be checked. Slots `i ∉ dom(Q)` are unconstrained. In Nelson's terms, FINDLINKSFROMTOTHREE supplies up to three slot constraints: `Q(1)` (from-set), `Q(2)` (to-set), `Q(3)` (three-set, or type). Each may be NIL, in which case it is omitted from `dom(Q)`. The general N-slot case extends to any subset of `{1, …, N}` for any link arity.

The substantive question is: when does a link match a query?

An endset `e` *overlaps* a span-set `S` when at least one span in `e` shares at least one position with at least one span in `S`:

  ovrlp(e, S) ≡ (E σ_e ∈ e, σ_s ∈ S : ⟦σ_e⟧ ∩ ⟦σ_s⟧ ≠ ∅)

The denotations `⟦σ_e⟧` and `⟦σ_s⟧` are span denotations in the sense of ASN-0053. Their intersection is a set of positions (I-addresses); non-empty intersection is the match condition. This is "the AND of the ORs" Nelson describes [LM 4/58]: an OR within each endset (any of e's spans suffices), an AND across endsets (every constrained slot must match).

The match predicate is then:

  match(L(a), Q) ≡ (A i ∈ dom(Q) : ovrlp(L(a).e_i, Q(i)))

A link at address `a` *matches* the query iff its endset at each constrained slot overlaps the slot's corresponding span-set.

Three observations are worth recording, because each is contestable.

*Single-byte intersection suffices.* The condition `⟦σ_e⟧ ∩ ⟦σ_s⟧ ≠ ∅` requires non-empty intersection, not containment. A link whose endset covers I-bytes `[4, 7)` matches a query for `[5, 7)` because they share `[5, 7)` — even though the endset extends beyond the query, and even though the query covers a strict subset. The endset need not be entirely within the query, nor vice versa. We name this *F-PARTIAL*.

*Slot independence.* The match predicate is symmetric across slot indices. The universal quantifier `(A i ∈ dom(Q) : …)` treats each constrained slot uniformly; no slot is searched first and used to filter the others. We name this *F-SYM*. The convention that slot 3 is "type" and slots 1, 2 are "from" and "to" is an interpretive overlay on the link structure; the match mechanics treat all three identically.

*Identity-based discovery.* The predicate ranges over `⟦σ_e⟧` and `⟦σ_s⟧` — sets of I-positions, not span identifiers. Two endset spans that denote the same I-positions match identically. This is *F-ID*, and it is the structural reason that transclusion is transparent to discovery.

## The Operation

The FINDLINKS operation, parameterized by a query `Q` and an optional scope `H ⊆ dom(L)`, returns the set of link addresses whose links match the query:

  find(Q, H) = { a ∈ H : match(L(a), Q) }

When `H` is omitted, the default is `H = dom(L)` — the entire link store. We will discuss scope further in §VI.

find is a *query*, not a state transition. The state `Σ` is unchanged: `Σ' = Σ`. find is a pure function of `Σ` and `(Q, H)`. We name this *F-FRAME*: every component of `Σ` is preserved across an invocation of find.

A consequence: find can be invoked repeatedly without affecting subsequent invocations. It can be invoked speculatively, cached, replayed, or memoized, and none of these affect any other operation, because nothing else depends on whether find has been invoked. find depends on `Σ.L` (the link store), `Σ.M(d_s)` (the source document's arrangement, used by `Iext` for V→I resolution), and indirectly on `Σ.C` (since `resolve` requires referential integrity). It does not depend on `Σ.E` directly. Operations that modify only `Σ.R` or only the arrangement of some document `d ≠ d_s` cannot change find's results for a query rooted at `d_s`.

## Soundness and Completeness

By construction, find satisfies two formal properties.

*F-SOUND*: `(A a : a ∈ find(Q, H) :: match(L(a), Q) ∧ a ∈ H)`.

*F-COMPLETE*: `(A a : a ∈ dom(L) ∧ match(L(a), Q) ∧ a ∈ H :: a ∈ find(Q, H))`.

Both follow tautologically from the definition `find(Q, H) := { a ∈ H : match(L(a), Q) }`. They are stated as named properties because each carries a commitment beyond the formula. F-SOUND says: no spurious matches; the operation does not invent links. F-COMPLETE says: no missed matches; the operation does not omit links that satisfy the predicate.

F-COMPLETE is the architectural commitment Nelson made and emphasized. He guarantees that "all these outside connections" are returned [LM 2/46], and that FINDLINKSFROMTOTHREE returns "all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`" [LM 4/69]. The word *all* is the commitment.

Consider a relaxed alternative: find returns *a* subset of matching links — any subset — possibly empty. Under this relaxation, every property F-SOUND, F-SYM, F-ID, F-PARTIAL, F-FRAME would still hold. F-COMPLETE would not. The system would be free to return whatever it found convenient. Nelson rejects this directly. The completeness commitment is what makes link discovery the connecting tissue of the docuverse: "There is essentially nothing in the Xanadu system except documents and their arbitrary links" [LM 4/41]. If link discovery were partial, the reader's question "what connects here?" would receive an answer that is provably incomplete in unknown ways. The reader would have no way to distinguish "there are no other links" from "the system did not look hard enough."

F-COMPLETE is therefore not redundant with the definition; it is the substantive commitment that distinguishes Xanadu's link discovery from approximate alternatives. Any specification that omitted it would describe a different (and weaker) operation. Any implementation that fails to demonstrate it has a defect, not merely a specification difference.

## Semantic Properties

The match predicate has consequences that are worth naming, because each is an architectural commitment about *what the operation depends on*.

*F-V-INVAR (Resolution-Invariance).* The operation depends on the V-selection only through its I-extent. Formally:

  ⟦Iext(d_1, σ_1)⟧ = ⟦Iext(d_2, σ_2)⟧
    ⟹ find({i ↦ Iext(d_1, σ_1)}, H) = find({i ↦ Iext(d_2, σ_2)}, H)

for every slot index `i` and scope `H`. The justification is direct: the overlap predicate `ovrlp(e, S)` is purely a function of `⟦S⟧`, since

  ovrlp(e, S) ⟺ ⟦e⟧ ∩ ⟦S⟧ ≠ ∅

where `⟦e⟧ := (∪ σ : σ ∈ e : ⟦σ⟧)` and `⟦S⟧` is defined analogously. Two span-sets with the same denotation yield the same overlap result for any endset; therefore two queries with equal `Iext` denotations yield identical results.

What F-V-INVAR guarantees is the property Nelson calls central: discovery follows content identity, not arrangement. A V-region that resolves to I-positions `P` discovers the same links whether the user pointed at it in d_s's original arrangement or at a transclusion of the same I-content elsewhere. The arrangements differ; the I-content does not; the result is the same.

*F-TRANSC (Transclusion Transparency).* Suppose `(d_1, σ_1)` and `(d_2, σ_2)` are content references such that the V-regions arrange the same I-content — formally, `⟦Iext(d_1, σ_1)⟧ = ⟦Iext(d_2, σ_2)⟧`. Then by F-V-INVAR, queries against the two are indistinguishable.

This is what allows Nelson's "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26]: versions share I-content; queries against equivalent V-regions return identical link sets. The link does not need to be re-bound to each new appearance; it is implicitly bound, by identity, to every appearance of its target I-addresses.

The property is not weaker than the underlying mechanism — it is exactly as strong. It does *not* say that two V-regions reading the same characters but allocated independently yield the same result. By S4 (OriginBasedIdentity, ASN-0036), independent allocations produce distinct I-addresses. Discovery is by I-identity, not by content value. Authors who independently type the same string create content at distinct I-addresses, and links to one do not appear on the other.

*F-AGGREGATE (Multi-Source Disjunction).* The resolve function returns a sequence of I-runs, possibly more than one, when the queried V-region spans content drawn from multiple I-origins. `Iext` aggregates these into a span-set with multiple constituent spans, and the overlap predicate ranges over the entire span-set via the existential

  (E σ_s ∈ Iext(d_s, σ) : ⟦σ_e⟧ ∩ ⟦σ_s⟧ ≠ ∅).

So a link whose endset matches *any one* of the constituent I-spans matches the overall query. A user pointing at a V-passage assembled from N transcluded sources sees, in one query, every link to any of those N sources. The system does not require N separate queries with a manual merge; the merge is built into the span-set quantifier.

We observe that F-AGGREGATE generalizes F-PARTIAL: a query whose span-set has multiple constituents matches a link whose endset overlaps *any one* of them, *even partially*. The architecture for compound queries reduces to the same overlap predicate.

## Operational Properties

Two further properties concern find's interaction with the rest of the system.

*F-ATOMIC (Post-Allocation Discoverability).* By K.λ (LinkAllocation, ASN-0047 / ASN-0093) and SequentialTransitionAxiom (ASN-0047 / ASN-0093), the allocation of a link is an atomic, uninterruptible transition. K.λ commits the new entry `(ℓ, value)` to L in a single indivisible step; either the pre-state holds (`ℓ ∉ dom(L)`) or the post-state holds (`ℓ ∈ dom(L) ∧ L(ℓ) = value`). There is no intermediate state.

The match predicate is evaluated against the current state Σ. Therefore:

  (A Σ_pre →_{K.λ} Σ_post, Q, H :: 
      (match(L(Σ_post)(ℓ), Q) ∧ ℓ ∈ H) ⟹ ℓ ∈ find_{Σ_post}(Q, H))

— a newly-allocated link is discoverable at every state subsequent to its K.λ event. The specification admits no model in which K.λ commits a link to L but the link is not yet discoverable by a query that should match it. Any implementation that indexes links lazily must complete the indexing inside the K.λ atomic step.

Symmetrically: a find executed at state Σ does not return links that exist only in some later state. The result set is bounded to `dom(L)` at the state of execution. Two consecutive finds with identical inputs at the same state return identical outputs; if the second find executes after an intervening K.λ committing a matching link, the second result may strictly extend the first by that link.

*F-ORDER (Canonical Result Order).* By L11a (LinkUniqueness, ASN-0043), distinct allocation events produce distinct link addresses; each link in `dom(L)` therefore has a unique tumbler address. By T1 (LexicographicOrder, ASN-0034), tumblers carry a total order. So `find(Q, H)`, as a subset of `dom(L)`, inherits a canonical total order from T1: links ordered by their addresses.

  (A Q, H, a_1, a_2 : a_1, a_2 ∈ find(Q, H) ∧ a_1 ≠ a_2 :: a_1 < a_2 ∨ a_2 < a_1)

Three consequences follow. *Determinism:* for a fixed state Σ and inputs `(Q, H)`, the ordered result is uniquely determined. *Resumability:* stable ordering permits pagination — a request for "the next N links past address `a`" yields a determinate slice, requiring no auxiliary state beyond the last-returned address. *Boundary independence:* the ordering is a property of the link addresses themselves, not of the query Q; queries that share matching links share the relative ordering of those links.

The implementation may impose other orderings (by document, by creation time, by relevance) as conveniences, but T1-by-address is the underlying canonical order from which any other is a permutation.

## Scope

We turn finally to the scope parameter `H`.

Nelson permits a *home-set* parameter narrowing the search to links owned by a specified set of documents [LM 4/69]. In its absence — the default — the search ranges over the entire link store. We model this as an explicit second argument:

  find(Q, H) = { a ∈ H : match(L(a), Q) }

with the convention `find(Q) := find(Q, dom(L))`. The completeness commitment F-COMPLETE is *relative to H*: every link in `H` that matches `Q` is in the result; links outside `H` are not searched, regardless of whether they would match.

Two observations:

*Default global scope is architecturally required.* Nelson's "What connects here from other documents?" [LM 2/46] is satisfiable only with global default scope. Restricting by default to the document containing the queried content would omit incoming links from elsewhere — which is precisely the question the user is asking about. The mechanism by which a link in document `d_1` can reference content in document `d_2` is built into L4 (EndsetGenerality, ASN-0043), which permits cross-document endsets without constraint. Restricting search by default would suppress these. Global scope is the architectural default for the same reason that endsets are cross-document: the docuverse is a single connected fabric, and discovery must traverse it.

*Scope is a filter, not a constraint on match semantics.* `H` partitions `dom(L)` into searched and unsearched; the match predicate evaluates identically on both. A link is in the result iff it is in `H` and matches. Scope can therefore be composed with the match predicate without rederiving the search: `find(Q, H_1) ∩ H_2 = find(Q, H_1 ∩ H_2)`.

Privacy is one motivation for scoping. If `H` excludes links in private documents that the querying user cannot access, find behaves consistently with link concealment as an emergent property of document privacy applied to links-as-contents: the unauthorized user sees no evidence of those links. We do not specify the access-control predicate that would define `H` for a given user; we observe that scope is the mechanism through which any such predicate would be enforced.

A consequence worth noting: scoping does not preserve F-V-INVAR across scope boundaries in general. Two queries with equivalent `Iext` denotations applied with different scopes `H_1 ≠ H_2` may yield different results. F-V-INVAR holds within a fixed scope; scoping interacts orthogonally with the I-coordinate semantics.

## Summary

We have specified the FINDLINKS operation `find(Q, H)` as a pure query against the current state, returning the set of link addresses whose endsets satisfy a slot-indexed family of overlap conditions against a span-set query. The operation is defined by an overlap predicate that ranges over I-coordinate denotations of endset spans and query span-sets, applied uniformly across the slot indices the query constrains.

The architectural commitments — that the operation is complete (F-COMPLETE), symmetric across slots (F-SYM), based on I-identity rather than V-position (F-ID, F-V-INVAR, F-TRANSC), tolerant of partial and multi-source overlaps (F-PARTIAL, F-AGGREGATE), atomic with respect to link creation (F-ATOMIC), and produces a canonically ordered result (F-ORDER) — are what makes find the right primitive for the docuverse Nelson designed. Each property has a single justification rooted in either the formal definition or a foundation invariant. None is incidental.

The operation does not modify state (F-FRAME). It is parameterized by a scope `H` that defaults to the entire link store. Implementations of find that respect the abstract specification must satisfy each of these properties; any deviation is an implementation defect, not a specification compromise.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F.Iext | `Iext(d_s, σ) = { (a_j, δ(n_j, #a_j)) : 1 ≤ j ≤ k }` where `resolve(d_s, σ) = ⟨(a_j, n_j)⟩` | introduced |
| F.Q | A query is a partial function `Q : ℕ ⇀ SpanSet` from slot indices to span-sets | introduced |
| F.ovrlp | `ovrlp(e, S) ≡ (E σ_e ∈ e, σ_s ∈ S : ⟦σ_e⟧ ∩ ⟦σ_s⟧ ≠ ∅)` | introduced |
| F.match | `match(L(a), Q) ≡ (A i ∈ dom(Q) : ovrlp(L(a).e_i, Q(i)))` | introduced |
| F.find | `find(Q, H) = { a ∈ H : match(L(a), Q) }`; default `H = dom(L)` | introduced |
| F-SOUND | `a ∈ find(Q, H) ⟹ match(L(a), Q) ∧ a ∈ H` | introduced |
| F-COMPLETE | `a ∈ dom(L) ∧ match(L(a), Q) ∧ a ∈ H ⟹ a ∈ find(Q, H)` | introduced |
| F-FRAME | find leaves every component of Σ unchanged | introduced |
| F-SYM | match treats all slot indices in `dom(Q)` symmetrically | introduced |
| F-ID | match is a function of I-position denotations, not span identifiers | introduced |
| F-PARTIAL | Non-empty intersection of any endset span with any query span suffices for match | introduced |
| F-V-INVAR | `⟦Iext(d_1, σ_1)⟧ = ⟦Iext(d_2, σ_2)⟧ ⟹` equal find results (under fixed slot index and scope) | introduced |
| F-TRANSC | Content references with equivalent I-extent denotations are discovery-equivalent | introduced |
| F-AGGREGATE | A query whose `Iext` has multiple constituents matches links overlapping any one constituent | introduced |
| F-ATOMIC | A link committed by K.λ is discoverable at every subsequent state | introduced |
| F-ORDER | `find(Q, H)` is canonically totally ordered by T1 on link addresses | introduced |

## Open Questions

- What guarantees must FINDLINKS provide when the queried V-region contains positions not in `dom(M(d_s))`?
- Under what conditions must two FINDLINKS invocations against the same state with identical inputs yield identical results?
- What completeness guarantees must FINDLINKS provide when slot constraints with empty span-sets are supplied?
- Must FINDLINKS distinguish, in its result, the slot at which each returned link matched, or is slot information collapsed?
- What invariants must hold between `dom(L)` and the supporting indexing structure for F-COMPLETE to be reliably satisfiable across all reachable states?
- Under what conditions may scope refinement `H' ⊆ H` lose completeness within `H'` — and when must this never happen?
- Must FINDLINKS results remain stable across operations that modify arrangements of documents other than `d_s`?
- What guarantees does FINDLINKS provide about links whose endsets reference I-content currently arranged in no document?
