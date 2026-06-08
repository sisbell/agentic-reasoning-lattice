# ASN-0111: READLINK — Reading a Link's Structure by Its Own Address

*2026-06-04*

## The problem

A Xanadu link is not markup buried in content; it is a first-class object with its own
permanent address in the link subspace. Because it is addressable, we can name it
directly and ask the system a question that has nothing to do with where the link points:
*what relationship does this object record?* This note specifies the operation that answers
that question — the direct read of a link by its own identity. We call it `readlink`.

We must be careful to separate `readlink` from three neighbouring operations that are out
of scope here. *Following* a link takes one of its endsets and resolves it against a chosen
document's arrangement to obtain current positions. *Searching* for a link supplies content
regions and asks which links touch them. *Counting* asks how many do. All three combine the
link with something beyond it — an arrangement, or a query's spec-set. `readlink` is the operation
by which the link discloses, in full and unconditionally, the relationship it was built to hold.

## The link as a readable object

We take from the foundations the shape of a stored link. The *link store* `Σ.L : T ⇀ Link`
(ASN-0043) maps addresses to link values, where a link value is a finite sequence of endsets

> `Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`,  `Endset = 𝒫_fin(Span)`

with the standard-triple convention assigning slot 1 the *from*-endset, slot 2 the *to*-endset,
and slot 3 the *type*-endset. Each endset is a finite set of spans over the tumbler line; each
span `(s, ℓ)` denotes a contiguous region `{t : s ≤ t < s ⊕ ℓ}` (T12, ASN-0034). The relationship
a link records is therefore not a pair of points but a triple of *span-sets*, each reaching —
possibly discontiguously — anywhere in the docuverse. The address-set a span-set denotes is its
`coverage` (ASN-0043):

> `coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})`.

Every link address is, by the substrate invariants, an element-level, T4-valid tumbler in the
link subspace: `zeros(a) = 3`, `subspace_I(a) = s_L`, `#E(a) ≥ 2` (L0, L1, L1b, L0b of ASN-0043).
These facts are what make a link nameable in the same address space as content; the `readlink`
lookup itself reads none of them, but a reader holding a candidate tumbler can test them as a
structural screen before invoking the read (RL0).

## Deriving the read

A standing precondition governs everything below: `readlink` is specified over `→*`-reachable,
invariant-satisfying states `Σ` (ASN-0047, ASN-0093). Where we write "for a state `Σ`," read "for a
reachable, invariant-satisfying `Σ`."

We are looking for an operation that, given an address, returns the relationship recorded there.
The minimal honest specification is a lookup in the link store. For such a state `Σ` and address `a`:

> `readlink(a, Σ)`
>   *defined when*  `a ∈ dom(Σ.L)`
>   `≡  Σ.L(a) = (e₁, e₂, ..., eₙ)`.

It is a pure read: its frame condition is that it changes nothing, `Σ' = Σ`.

The first commitment is on the domain. The read is defined exactly on allocated link addresses.

**RL0 (Definedness).** `readlink(a, Σ)` is defined iff `a ∈ dom(Σ.L)`. Reasoning backward from
the postcondition "the result is the recorded relationship at `a`" — a postcondition that does not
dereference `Σ.L` off its domain — the weakest precondition is precisely membership:

> `wp(readlink request at a, result is the recorded relationship at a) ≡ a ∈ dom(Σ.L)`.

The postcondition is well-formed on every state: it asserts that a recorded relationship exists at
`a` and that the result is it, which is satisfiable exactly when `a ∈ dom(Σ.L)` and fails (rather
than becoming ill-defined) when `a ∉ dom(Σ.L)`.

A reader holding a candidate tumbler can test the *necessary* structural conditions from the
address alone — `zeros(a) = 3 ∧ subspace_I(a) = s_L` — by T4 parsing and the subspace projection
(ASN-0034). These conditions are necessary but not sufficient: an address may parse as a
well-formed link tumbler yet name no allocated link. Definedness is a fact about `dom(Σ.L)`, not
about the address's syntax, so the read either delivers the whole relationship or reports that no
link lives at `a`. There is no partial-success middle state at the level of *whether* a link is there.

## Completeness: the read returns the whole relationship

A direct read answers no query, so there is no satisfying fragment at which it could stop. It
must return the endsets *entire*.

**RL1 (Completeness).** For each slot `i`, the returned endset equals the recorded one exactly —
omitting nothing and introducing nothing:

> `(A i : 1 ≤ i ≤ |Σ.L(a)| : readlink(a, Σ).eᵢ = Σ.L(a).eᵢ)`.

The set equality captures both directions at once: every recorded span `(s, ℓ) ∈ Σ.L(a).eᵢ` is
returned, and no span outside `Σ.L(a).eᵢ` appears in the result. The justification is immediate from
the definition: `readlink(a, Σ) = Σ.L(a)` componentwise.

This is why the read recovers the arbitrary, broken collections that endsets are permitted to be.
An endset may scatter spans across many documents and across discontiguous regions within one;
the read returns every piece, because completeness is over the recorded structure, not over any
region a caller happened to name. Because the read copies the recorded spans unmodified, it
inherits their L4-generality (ASN-0043) without adding any confinement: a returned span may point
across documents, within the home document, or into the link subspace at other links. The link's
home document `home(a) = N(a).0.U(a).0.D(a)` is no part of this returned value; it is read off the
*key* `a` by T4 field projection (L2, ASN-0043), recoverable by any caller who already holds `a`.

Because `readlink(a, Σ) = Σ.L(a)` verbatim, every link-store invariant transfers to the output in
one line. In particular the returned value satisfies, as corollaries of RL1: **L3** — arity at
least three with non-empty type slot `e₃ ≠ ∅`, while the connective from- and to-slots may
individually be `∅` (`∅` is a valid endset); **L5** — within an endset there is no operator
selecting "the j-th span", so the read exposes membership, not sequence; and **Endset
well-formedness** — `Endset = 𝒫_fin(Span)` with each span `(s, ℓ)` T12-well-formed
(`Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`), denoting a non-empty contiguous region (ASN-0034). The read can
return neither a malformed nor an empty span, and it always returns a usable type endset.

## The structure the read must preserve

A span in the from-set asserts something different from the same span in the to-set or the
type-set, so the read carries an obligation beyond returning a bag of spans: it must keep each
endset aligned with its slot.

**RL2 (Role preservation).** The read preserves the link's arity, and slot position is part of the
value:

> `|readlink(a, Σ)| = |Σ.L(a)|`,  and for each `1 ≤ i ≤ |Σ.L(a)|` the positional accessor
> `readlink(a, Σ).eᵢ` is a model primitive (L6, ASN-0043), with link equality componentwise.

In the arity-3 case slot 1 is *from*, slot 2 is *to*, and slot 3 is *type*; for `N > 3` (L3,
ASN-0043) the higher slots are returned under their own indices. The read keeps every endset
aligned with its slot — this is exactly the alignment that any role-respecting use of the link
depends upon.

## Type is interpreted by address, not by content

The type endset deserves separate treatment, because it is the one part of the structure whose
spans need not reference anything that exists.

**RL5 (Type-by-address).** The relationship the type records is fixed by `coverage(e₃)` — the set
of addresses the type-set names — and not by whatever is, or is not, stored at those addresses.
Two links share a type exactly when their type endsets have equal coverage (L8, ASN-0043), a
relation on address sets, decided without dereferencing a single one. The read therefore delivers
a fully interpretable type even when the type address holds nothing at all: ghost types are
permitted (L9, ASN-0043), and the read of a ghost-typed link is no less complete than any other.

## Faithful disclosure of nesting

Because links live in the same address space as content, an endset may name another link. The
to-set of a link can carry a span of width one over a link's own address (the canonical reflexive
span of L13, ASN-0043), making the link's target itself a link.

**RL6 (Nesting fidelity).** If `a' ∈ dom(Σ.L)` and `a' ∈ coverage(readlink(a, Σ).eᵢ)`, the read
discloses `a'` as the tumbler address it is — returned as an address whether it names content or
another link, not flattened into whatever further reading of `a'` might yield.

## Determinacy and the immutability of the recorded relationship

A read is only as trustworthy as the stability of what it reads. The link store is append-only and
its values are frozen: once allocated, a link's address persists and its value never changes
(L12, L12a of ASN-0043). The read inherits this stability.

**RL7 (Determinacy).** `readlink` is a pure function of `(a, Σ.L)`: two reads of the same address
in the same link store return identical values. Moreover, the read is stable across the whole
future:

> `(A Σ, Σ' : Σ →* Σ' ∧ a ∈ dom(Σ.L) : readlink(a, Σ') = readlink(a, Σ))`.

Stability across `Σ →* Σ'` follows from LP13 (UnconditionalLinkPersistence, ASN-0098), giving
`a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`; hence `readlink(a, Σ') = Σ'.L(a) = Σ.L(a) = readlink(a, Σ)`.

A reader who has once read a link may rely on that reading permanently.

## Recorded relationship versus resolved position

A link records its endsets as spans over the *permanent* address space. Resolving those spans
against a particular document's arrangement — mapping them to current positions — is a separate
act, the business of traversal and projection, conditional on the arrangement.

**RL8 (Recorded, not resolved).** `readlink(a, Σ)` depends only on `Σ.L`; it is independent of every
document arrangement. Consequently the read succeeds and returns the complete structure even for an
*orphaned* link — one whose endpoint content is currently arranged in no document, so that resolving
its endsets would yield nothing (cf. the ghost-projection situation, ASN-0098). The link's structure
persists unconditionally (L12; LP13 of ASN-0098), and the read surfaces it unconditionally.

## A worked read

The claims above are abstract; we check them against one concrete link. Fix the subspace
convention `s_C = 1`, `s_L = 2` (ASN-0093). Take two documents

> `d₁ = [1.0.1.0.1]`,  `d₂ = [1.0.1.0.2]`  (each `zeros = 2`, T4-valid),

and a link homed in `d₁` at address

> `a = [1.0.1.0.1.0.2.1]`   (`zeros(a) = 3`; element field `E(a) = [2, 1]`, so
> `subspace_I(a) = E(a)₁ = s_L`, `#E(a) = 2` — the first emission of `d₁`'s link sub-allocator).

Let the stored value `Σ.L(a) = (F, G, Θ)` be the standard triple

- **from-set** `F = {([1.0.1.0.1.0.1.1], δ(2, 8)), ([1.0.1.0.2.0.1.1], δ(1, 8))}` — two spans
  scattered across *two* documents. `coverage(F)` is a *union of two half-open intervals*, not a
  finite list of points. The first span runs from `[1.0.1.0.1.0.1.1]` up to but not including
  `[1.0.1.0.1.0.1.1] ⊕ δ(2, 8) = [1.0.1.0.1.0.1.3]`; by T1 case (ii) that interval contains the
  entire subtrees beneath `…1.1` and `…1.2` (e.g. `[1.0.1.0.1.0.1.1.0]`, `[1.0.1.0.1.0.1.2.5]`),
  an infinite tumbler set, *not* the two addresses `…1.1` and `…1.2` alone. The second span is the
  interval `[ [1.0.1.0.2.0.1.1], [1.0.1.0.2.0.1.2] )` under `d₂`. The element-level content
  I-addresses lying within `coverage(F)` are `[1.0.1.0.1.0.1.1]` and `[1.0.1.0.1.0.1.2]` under `d₁`
  and `[1.0.1.0.2.0.1.1]` under `d₂` — three `dom(C)` members that host content and are unarranged.
- **to-set** `G = ∅` — a legitimately empty connective slot.
- **type-set** `Θ = {([1.0.1.0.9.0.1.1], δ(1, 8))}` — a single span whose address sits under a
  document `[1.0.1.0.9]` that hosts no content: a *ghost* type, a label by location.

A direct read returns the whole triple, grouped by slot:

> `readlink(a, Σ) = (F, ∅, Θ)`,
> with `readlink(a, Σ).e₁ = F`, `readlink(a, Σ).e₂ = ∅`, `readlink(a, Σ).e₃ = Θ`.

We can now check the load-bearing postconditions against this instance.

- *RL1 (completeness).* The read returns *both* from-spans, the empty to-set, and the type-span —
  every recorded span and nothing more.
- *RL2 (role preservation).* The three endsets come back under slots 1/2/3, not pooled. Were the
  read to return the bag `F ∪ Θ`, the reader could no longer tell that `[1.0.1.0.9.0.1.1]`
  classifies the link while the others are its source — a different relationship (L6). The read
  copies the stored `Σ.L(a).eᵢ` into `readlink(a, Σ).eᵢ` by a per-index rule that names no other
  slot (link equality is componentwise, L6): an arity-4 value `(F, ∅, Θ, e₄)` returns `e₄` under
  slot 4 by exactly the same copy.
- *RL5 (ghost-type completeness).* `Θ`'s address holds nothing, yet the read returns it intact.
  Its single span `([1.0.1.0.9.0.1.1], δ(1, 8))` is the canonical unit-depth span (`#s = 8 = #δ(1, 8)`),
  so by PrefixSpanCoverage (ASN-0043) `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` — the *subtree*
  beneath that address, an infinite tumbler set, not the single point `[1.0.1.0.9.0.1.1]`. As with
  the from-set above, the type is interpreted as this coverage *address-set* (L8) and matched against
  another type's coverage without dereferencing anything stored there.
- *Structural corollary (arity/type).* Arity is 3 and `Θ ≠ ∅` (L3), while the connective slot
  `G = ∅` is permitted — exactly the mandatory-type / permissive-direction split.

*A nested instance (RL6).* Links share the address space with content, so an endset may target
another link. Let `a' = inc(a, 0) = [1.0.1.0.1.0.2.2]` be a second link homed in `d₁` — the next
sibling on `d₁`'s link sub-allocator, so `a' ∈ dom(Σ.L)` — and consider a third link
`c = [1.0.1.0.1.0.2.3]`, also homed in `d₁`, whose to-set is the canonical reflexive span over `a'`:

> `Σ.L(c) = (∅, G_c, Θ)`,  `G_c = {([1.0.1.0.1.0.2.2], δ(1, 8))}`   (`#a' = 8 = #δ(1, 8)`, the
> canonical unit-depth span of L13, ASN-0043; `c` reuses the ghost type `Θ`, so it is a conforming
> arity-3 link with non-empty type slot).

The read returns `readlink(c, Σ).e₂ = G_c`, the span intact. By PrefixSpanCoverage (ASN-0043) its
coverage is the subtree `coverage(G_c) = {t : a' ≼ t}`, so `a' ∈ coverage(readlink(c, Σ).e₂)` and the
read discloses `a'` *as the tumbler address it is* — unflattened, not resolved into whatever `a'`
itself records. This verifies RL6 against a concrete link→link target — the construction underlying
compound and faceted structures.

*An orphaned instance (RL8).* Suppose `a` is orphaned at `Σ` — no document arrangement maps any
V-position into the coverage of any of its endsets, so a *follow* of `F` against any arrangement
would resolve to the empty set and a *search* would find nothing to match (the ghost-projection
situation, LP17, ASN-0098). The READLINK obligation is unaffected by this hypothesis: the read
consults only `Σ.L`, never an arrangement (RL8), so `readlink(a, Σ) = (F, ∅, Θ)` still returns the
complete structure. The read thus distinguishes *the relationship is unwitnessed* (true here) from
*the relationship is gone* (false — `a ∈ dom(Σ.L)` and its value is fixed by L12 / LP13).

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `readlink` | `readlink(a, Σ) ≡ Σ.L(a)`, defined when `a ∈ dom(Σ.L)`; pure read, frame `Σ' = Σ` | introduced |
| RL0 | The read is defined iff `a ∈ dom(Σ.L)`; `wp = a ∈ dom(Σ.L)`; link-shape of the address is necessary but not sufficient | introduced |
| RL1 | Completeness — the read returns every recorded span of every endset and no other; `readlink(a, Σ) = Σ.L(a)`; inherits L4-generality of the recorded spans. Corollaries (since the output is `Σ.L(a)`): satisfies L3 (arity ≥ 3, non-empty type slot, connective slots may be `∅`), L5 (membership not sequence within an endset), and Endset well-formedness (T12 spans) | introduced |
| RL2 | Role preservation — the read preserves arity (`|readlink(a, Σ)| = |Σ.L(a)|`) and exposes slot position as a model primitive (L6); from/to/type grouping delivered as structure | introduced |
| RL5 | Type-by-address — the type is interpreted via `coverage(e₃)`, not via content at those addresses; ghost types read completely | introduced |
| RL6 | Nesting fidelity — link addresses in an endset's coverage are returned as addresses, unflattened | introduced |
| RL7 | Determinacy — `readlink` is a pure function of `(a, Σ.L)` and stable across all `Σ →* Σ'` by link immutability | introduced |
| RL8 | Recorded, not resolved — the read depends only on `Σ.L`, succeeds for orphaned links, and returns the complete structure independent of any arrangement | introduced |

## Open Questions

What must the system guarantee a reader can conclude about a relationship's continued validity from a direct read alone, given that the read does not consult any arrangement?

What must FOLLOWLINK guarantee so that an endset legitimately empty at the read level stays distinguishable from one whose spans reference only currently-unwitnessed content, given that resolution against an arrangement collapses both to the empty position set?

What guarantee must hold so that reading two distinct links with identical recorded structure always yields results distinguishable by the reader, given that addresses, not values, carry link identity?
