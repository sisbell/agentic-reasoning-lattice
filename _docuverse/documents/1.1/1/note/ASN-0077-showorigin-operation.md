# ASN-0077: SHOWORIGIN Operation

*2026-05-25*

Suppose a reader confronts a passage — perhaps a single character, perhaps an entire chapter — and asks: *where did this come from?* In what document was it first set down, by what allocator was it first baptised? The answer must not depend on what the reader is doing or where the passage currently appears. A quote in a tenth-generation derivative document still has one true source. A character copied from one paragraph to another still has one true author. Whatever mechanism we build, it must give one answer, and the same answer in every state of the system.

Nelson states the requirement plainly: *"You always know where you are, and can at once ascertain the home document of any specific word or character."* [LM 2/40] The phrase *any specific word or character* sets the lower bound on scale; the phrase *at once* rules out any procedure that walks chains of indirection. The operation we are searching for is called SHOWORIGIN. Its input is a span of content. Its output is the identity of the home document — or, when the span draws from multiple sources, the set of home documents present. We must show that this operation can be specified abstractly, that its result is determined by the content alone, and that the specification extends uniformly from one address to spans of any size.

## Where origin already lives

The origin of a single I-address is not a new fact we must compute — it is recorded in the address itself. Foundation ASN-0036 establishes this as S7: for every `a ∈ dom(Σ.C)`, the *origin* is the document-level tumbler obtained by truncating the element field,

> `origin(a) = N(a).0.U(a).0.D(a)`,

a projection that is total on `dom(C)`, single-valued, and document-level (`zeros(origin(a)) = 2`). By S7d (DocumentAllocationDiscipline), distinct documents have distinct tumblers, so `origin(a₁) = origin(a₂)` says exactly that `a₁` and `a₂` were allocated by the same document. By S7's clause (d), `origin(a)` is invariant across every state in which `a ∈ dom(C)`. The structural projection reads only components of `a` itself; no registry, no index, no external context is consulted.

What we do not yet have is an operation that takes a *span* — not just one address — and reports the documents present. That is what we now construct.

## Lifting origin to an I-span

Let σ be an I-span (foundation ASN-0053, T12), with start `s` and width `ℓ`, denoting the half-open interval

> `⟦σ⟧ = { t ∈ T : s ≤ t < s ⊕ ℓ }`.

Not every position in `⟦σ⟧` need lie in `dom(C)`; only those that do are content. We define the I-span lift of origin:

> `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.

The result is a finite set of document-level tumblers — finite because `dom(C)` is finite (C-fin, foundation ASN-0047). The set may be empty (no positions in σ are allocated), a singleton (all allocated addresses come from one document), or larger (σ crosses content subspaces of distinct documents).

By S7a (DocumentScopedAllocation, foundation ASN-0036), every I-address allocated by document `d` carries `d`'s prefix. Two addresses share an origin iff they share the prefix `N(a).0.U(a).0.D(a)`. The structural fact this delivers is what we call subspace homogeneity:

**Claim O1 (Subspace homogeneity).** *For any I-span σ such that every element of `⟦σ⟧ ∩ dom(C)` lies wholly within one document's content subspace, `|origins_I(Σ, σ)| ≤ 1`.* The inequality (rather than equality) covers the case where `σ` happens to contain no allocated addresses at all.

The contrapositive is what justifies treating multi-origin results as informative: if `|origins_I(Σ, σ)| > 1`, then σ has positions in two or more distinct content subspaces, hence necessarily crosses document allocation boundaries in the I-stream. Such spans are admitted by T12 (since T12 places no upper limit on width) but do not arise from any single document's allocation activity.

## Lifting origin to a V-span

A reader more naturally has access to a V-span — a contiguous region of positions in the document they are reading. The content at those positions may be native (allocated by the reader's document) or transcluded (allocated elsewhere, included by reference). SHOWORIGIN must resolve this question through the document's arrangement.

Foundation ASN-0058 supplies the machinery. A content reference is a pair `(d, σ)` where `d` is a document and `σ = (u, ℓ)` is a level-uniform V-span in `d`'s arrangement. The resolution function returns a sequence of mapping blocks:

> `resolve(d, σ) = ⟨ (a₁, n₁), ..., (aₖ, nₖ) ⟩`,

where each block `(aⱼ, nⱼ)` denotes the I-address run `aⱼ, aⱼ + 1, ..., aⱼ + (nⱼ − 1)`. The V-positions in `⟦σ⟧` map to exactly the I-addresses in these runs (M2, M3 of ASN-0058).

We lift origin over this resolution:

> `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`.

The expression simplifies. Within a single mapping block `(aⱼ, nⱼ)`, every I-address has the form `aⱼ + i` for `0 ≤ i < nⱼ`. By M16a (OrdinalInvarianceUnderShift, ASN-0058), `origin(aⱼ + i) = origin(aⱼ)` for every `i` in this range. Each block contributes exactly one origin, and:

> `origins_V(Σ, d, σ) = { origin(aⱼ) : 1 ≤ j ≤ k }`.

This delivers our second uniformity claim:

**Claim O2 (Block uniformity).** *For each mapping block `(vⱼ, aⱼ, nⱼ)` arising in a decomposition of `M(d) ↾ ⟦σ⟧`, every I-address in `I(βⱼ)` shares `origin(aⱼ)`.*

The set `origins_V(Σ, d, σ)` may be smaller than `k` if multiple blocks share an origin — for instance, two separately-transcluded passages drawn from the same source document, or transcluded content interleaved with native content of `d` where the native portions and `d` itself share an origin (`d` itself, for native).

## Structural derivation

The most important claim about SHOWORIGIN is not what it computes but what it does *not* need.

**Claim O3 (Structural derivation).** *`origin(a)` is computable from `a` alone, consulting no further state. `origins_I(Σ, σ)` is computable from `⟦σ⟧ ∩ dom(C)` alone; `origins_V(Σ, d, σ)` is computable from `M(d) ↾ ⟦σ⟧` alone.*

The first sub-claim follows immediately from the form of the projection: `N(a).0.U(a).0.D(a)` reads only the components of `a`. The two lifts inherit structurality: each evaluates the projection pointwise. Beyond `dom(C)` (to recognise which positions in `⟦σ⟧` are allocated) and the arrangement `M(d)` (to resolve V-positions to I-addresses), no further state is consulted.

The consequence for transclusion is decisive. A document whose server is unreachable still has its tumbler recorded in every transcluded I-address that originated from it; SHOWORIGIN reports this tumbler from the address structure alone. The unreachability of the source bears on whether the bytes can be *fetched*, not on whether the origin can be *named*.

This is what Nelson means when he insists attribution is *unstrippable within the docuverse* [Q1]: there is no metadata to strip. The origin claim is part of the address, and the address is the means by which the bytes are retrieved.

## Direct resolution through transclusion

Suppose content was allocated in document `d₁`. Document `d₂` transcludes it; `d₃` transcludes from `d₂`; this continues to `dₙ`. A reader of `dₙ` asks SHOWORIGIN. What does it return?

Because each transclusion is by reference rather than copy, the I-address recorded in every intermediate document's arrangement is the *same* — it points to the bytes baptised by `d₁`. Each intermediate document `d₂, d₃, ..., d_{n-1}` holds an arrangement entry mapping its own V-positions to this single I-address, but the address does not change as it propagates. SHOWORIGIN at `dₙ` resolves the V-position to that I-address and projects to `d₁` directly:

**Claim O4 (Direct resolution through transclusion).** *For any V-position `v ∈ dom(M(dₙ))` with `M(dₙ)(v) = a`, `origin(a)` is determined by `a` alone — independently of the depth or composition of any chain of intermediate transclusions whose arrangements happen to map V-positions to `a`.*

This is what Nelson means by *at once* [Q10]: the resolution mechanism does not walk a chain. The chain may be arbitrarily deep — each intermediate document contributes its own arrangement entry — but the address recorded in every entry is identical, and the projection consults that address alone.

The same point in calculational form. Let `f_M = origin ∘ M(dₙ)` be the composite *reader's-view-to-origin* function. Then

> `f_M(v) = origin(M(dₙ)(v)) = origin(a) = d₁`,

with no occurrence of `d₂, ..., d_{n-1}` anywhere in the chain of reasoning. The intermediate documents are *parallel witnesses* — they each independently established that they contain content with origin `d₁` — but the answer can be read off without consulting any of them.

## Permanence

We turn to the question raised at the start: does the answer change?

**Claim O5 (Origin permanence).** *For any `a ∈ dom(Σ.C)` and any reachable transition `Σ → Σ'`, if `a ∈ dom(Σ'.C)`, then `origin'(a) = origin(a)`.*

This is a direct consequence of foundation ASN-0047's P0 (ContentPermanence): `dom(C)` is append-only and content values are immutable. The address `a` does not move and its component structure is fixed; the projection `N(a).0.U(a).0.D(a)` reads those fixed components. Identical inputs to a pure projection deliver identical outputs.

For the I-span lift, permanence has a directional character.

**Claim O6 (Monotonic growth under state).** *For any reachable `Σ → Σ'` and any I-span `σ`: `origins_I(Σ, σ) ⊆ origins_I(Σ', σ)`.*

The result set can only grow. By P0, `dom(C) ⊆ dom(C')`, so `⟦σ⟧ ∩ dom(C) ⊆ ⟦σ⟧ ∩ dom(C')`; and origin is fixed pointwise. New allocations within σ may introduce new origins, but existing origins cannot be reassigned or removed.

The V-span lift is more nuanced. `origins_V(Σ, d, σ)` depends on the arrangement `M(d)`, which is mutable under editing operations. A passage transcluded today may be removed tomorrow, in which case the corresponding source document is no longer represented at those V-positions. The strongest claim we can make about V-span permanence requires fixing the arrangement:

**Claim O7 (V-span stability under fixed arrangement).** *For any reachable `Σ → Σ'` such that `M'(d) ↾ ⟦σ⟧ = M(d) ↾ ⟦σ⟧`, we have `origins_V(Σ', d, σ) = origins_V(Σ, d, σ)`.*

The frame condition is what reads the same answer back. Once the arrangement over `σ`'s range is unchanged, the resolved I-addresses are unchanged, and origins are unchanged.

## Scale invariance

Nelson is explicit that the system must distinguish no scale below *any specific word or character*. The same mechanism that names the home of a million-character chapter must name the home of a single character [Q8].

In our formalisation, scale invariance is structural: `origins_I` is parameterised by σ but performs the same pointwise projection whether `⟦σ⟧ ∩ dom(C)` has one element or millions. There is no procedural case distinction on size.

**Claim O8 (Scale invariance).** *For I-spans `σ₁, σ₂` with `⟦σ₁⟧ ⊆ ⟦σ₂⟧`: `origins_I(Σ, σ₁) ⊆ origins_I(Σ, σ₂)`.*

The smallest case is the singleton: for any `a ∈ dom(C)`, the singleton span (containing only `a`) yields `origins_I = {origin(a)}`. The largest case is unbounded — by T0(b) of ASN-0034, there is no maximum tumbler length, so spans can be arbitrarily wide. The mechanism is the same at both extremes.

This corresponds to Nelson's remark that *spans work naturally from the smallest to largest units* [Q8]. The uniformity is not an engineering convenience but a semantic necessity: if attribution at a paragraph level were not reducible to attribution at a character level, the architecture would fail at boundaries between fragments. SHOWORIGIN's well-definedness on single characters is what makes its lift to spans coherent.

## Identity, not equivalence

The system distinguishes *wrote the same words* from *quoted from the original* [Q1, Q9]. Two documents that independently produce identical text have distinct I-addresses; transcluded content shares an I-address with its source. SHOWORIGIN tracks the I-address, so it reports identity-of-origin, not equivalence-of-text.

**Claim O9 (Origin tracks creation, not content).** *Let `a₁, a₂ ∈ dom(C)` with `C(a₁) = C(a₂)` (identical content values). If `a₁` and `a₂` were produced by distinct allocation events, then `origin(a₁) ≠ origin(a₂)`.*

This follows from S4 (OriginBasedIdentity, ASN-0036) combined with S7d (DocumentAllocationDiscipline, ASN-0036): distinct allocation events produce distinct I-addresses, and distinct documents have distinct allocation prefixes. Reading the same value back from two addresses tells you the bytes match; it does not tell you they came from the same place. SHOWORIGIN distinguishes these cases by construction.

## The operation

We can now specify SHOWORIGIN as a non-state-modifying operation in two arities.

**SHOWORIGIN over an I-span.**
- *Preconditions*: `σ` is a well-formed I-span (T12 of ASN-0034 — `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s`).
- *Postcondition*: the result is `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }`.
- *Frame*: `Σ' = Σ`. The operation does not modify `C`, `L`, `E`, `M`, or `R`.

**SHOWORIGIN over a content reference.**
- *Preconditions*: `(d, σ)` is a well-formed content reference (ASN-0058).
- *Postcondition*: the result is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.
- *Frame*: `Σ' = Σ`.

**Claim O10 (Read-only frame).** *SHOWORIGIN preserves the entire state. Two consecutive applications at the same state produce identical results.*

Idempotence is essential: SHOWORIGIN must be a passive observation. Without the read-only frame, the act of asking would alter the answer, which would defeat the purpose of having an answer at all.

## What SHOWORIGIN does not promise

The claims above bound what SHOWORIGIN guarantees. Three exclusions deserve explicit statement.

*Not historical containment.* SHOWORIGIN reports origin, not the set of documents that *have ever contained* the queried content. A document that once transcluded the content and then contracted its arrangement (`K.μ⁻`) is no longer represented by `M(d)` and does not appear in `origins_V`. Historical containment is recorded in the provenance relation `Σ.R` (foundation ASN-0047) and is a separate concern. Gregory's investigation of the spanfilade [Q17] confirms that the implementation's `find_documents_containing` mixes these two notions and returns a superset of currently-containing documents — a behaviour distinct from SHOWORIGIN.

*Not human authorship.* As Nelson notes [Q2], the User field of the tumbler identifies an owning *account*, not necessarily a known human. *John Doe publication* is permitted: anonymous and pseudonymous content has well-defined origin without revealing identity. SHOWORIGIN reports what the address structure encodes, and no more.

*Not transitive provenance.* SHOWORIGIN follows no chain. When `dₙ` transcludes from `d_{n-1}` which transcluded from `d_{n-2}`, etc., the result names `d₁` (the original allocator), not the chain `d₁ → d₂ → ... → dₙ`. Users who wish to see the chain of intermediate documents must perform a different operation — for instance, step pane-by-pane through each layer's arrangement [Q10]. SHOWORIGIN gives them the direct answer only.

## A worked example

Document `d₁` allocates content at I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` containing the five characters of *Hello*. Document `d₂` arranges these five I-addresses at V-positions `[1,1,1]` through `[1,1,5]` in its own arrangement — a transclusion of the entire word, by reference. Document `d₃` similarly transcludes `d₂`'s arrangement of these positions, recording I-addresses `[d₁.0.1.1]` through `[d₁.0.1.5]` at its own V-positions — note that `d₃`'s arrangement records the original I-addresses directly, not pointers to `d₂`'s arrangement.

A reader at `d₃` asks SHOWORIGIN over the V-span containing all five positions. The resolution yields one mapping block `(v_start, [d₁.0.1.1], 5)`. By O2, this block contributes one origin: `origin([d₁.0.1.1]) = d₁`. The answer is `{d₁}`. The intermediate document `d₂` does not appear.

Now suppose `d₃` then natively appends two new characters at V-positions `[1,1,6]` and `[1,1,7]`, allocated at `[d₃.0.1.1]` and `[d₃.0.1.2]`. A SHOWORIGIN over the full seven-position V-span returns two origins:

> `origins_V = { origin([d₁.0.1.1]), origin([d₃.0.1.1]) } = { d₁, d₃ }`.

Two mapping blocks, two origins. The block for the first five positions traces to `d₁`; the block for the last two traces to `d₃`. The multi-origin case is not a degenerate case — it is the expected case for any document of mixed authorship.

## Summary

The abstract specification of SHOWORIGIN reduces to three primitives:

(1) The pointwise projection `origin : dom(C) → E_doc` (established in S7 of foundation ASN-0036), which is structural, total, and permanent.

(2) The lift to I-spans, `origins_I(Σ, σ) = origin(⟦σ⟧ ∩ dom(C))`, computable from the span and `dom(C)` alone.

(3) The lift to V-spans, `origins_V(Σ, d, σ) = origin(ran(M(d) ↾ ⟦σ⟧))`, computable from the span, the arrangement, and `dom(C)` alone.

Every other property — scale invariance, transclusion-depth invariance, permanence under state, immunity to source-document unreachability — follows from these three. The operation derives no new knowledge; it presents existing structural facts about the address space.

Any implementation of Xanadu that claims to support SHOWORIGIN must satisfy O1–O10. It may realise the operation through different mechanisms — direct tumbler-prefix decomposition, spanfilade lookup, granfilade traversal, or per-block `homedoc` records [Q12, Q13] — and these mechanisms may have different operational characteristics. But the abstract guarantees they deliver must coincide: every byte names its home, every span reveals its sources, and the answer never changes once given.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `origins_I(Σ, σ)` | `origins_I(Σ, σ) = { origin(a) : a ∈ ⟦σ⟧ ∩ dom(Σ.C) }` — I-span lift of origin | introduced |
| `origins_V(Σ, d, σ)` | `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }` — V-span lift via arrangement | introduced |
| O1 | Subspace homogeneity: an I-span confined to one document's content subspace yields at most one origin | introduced |
| O2 | Block uniformity: every I-address within a single mapping block shares one origin | introduced |
| O3 | Structural derivation: `origin(a)` and both lifts consult only the address (and, for V-span, the arrangement restricted to the span) | introduced |
| O4 | Direct resolution through transclusion: `origin(M(dₙ)(v))` is determined by the recorded I-address alone, independent of transclusion-chain depth | introduced |
| O5 | Origin permanence: `origin(a)` is identical in every reachable state containing `a` | introduced |
| O6 | Monotonic growth under state: `origins_I` is non-decreasing as content is added | introduced |
| O7 | V-span stability under fixed arrangement: `origins_V` is unchanged when the arrangement restricted to the span is unchanged | introduced |
| O8 | Scale invariance: `origins_I` is monotonic under span inclusion; the mechanism is uniform from single character to entire document | introduced |
| O9 | Origin tracks creation, not content: two independently-allocated addresses with identical content values have distinct origins | introduced |
| O10 | Read-only frame: SHOWORIGIN preserves the state; consecutive applications at the same state yield identical results | introduced |
| SHOWORIGIN (I-span) | Operation over a well-formed I-span returning `origins_I(Σ, σ)` with `Σ' = Σ` | introduced |
| SHOWORIGIN (V-span) | Operation over a well-formed content reference returning `origins_V(Σ, d, σ)` with `Σ' = Σ` | introduced |

## Open Questions

What must SHOWORIGIN guarantee when its input span crosses subspace boundaries (content addresses and link addresses both present in the I-stream range)?

When a span's content has been transcluded through several intermediate documents, must any abstract operation be provided that surfaces the intermediate chain, or is the direct origin answer sufficient?

Must SHOWORIGIN distinguish content that was natively allocated in a queried document from content transcluded into it, or is this distinction the responsibility of a separate operation?

What guarantee must hold for SHOWORIGIN when the home document's I-addresses are no longer reachable for byte-fetching, but the address itself remains well-formed?

Does the system require a complementary operation reporting historical containment (from `Σ.R`) distinct from current arrangement origins, and what invariants must couple the two?

When multiple V-positions in a single arrangement map to the same I-address (intra-document sharing per S5 of ASN-0036), what must SHOWORIGIN report at each position?
