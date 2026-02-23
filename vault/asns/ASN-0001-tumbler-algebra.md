# ASN-0001: Tumbler Algebra

*2026-02-22*

We wish to understand the algebraic structure that the Xanadu addressing
system must satisfy. The system assigns every piece of content a permanent
address — a "tumbler" — and these addresses must support ordering,
containment queries, arithmetic for editing operations, and
coordination-free allocation across a global network. We seek the minimal
set of abstract properties that any correct implementation of this
addressing scheme must provide.

## The carrier set

A tumbler is a finite sequence of non-negative integers. We write a tumbler
as `t = d₁.d₂.d₃. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of
all tumblers is `T`. We require `T` to be closed under the operations we
shall introduce, and we require `T` to be unbounded — there is no maximum
tumbler, and between any two tumblers in the system, fresh addresses can
always be generated.

Nelson is explicit about unboundedness: each component is a "humber," an
accordion-like notation that is "very short when a number is small, and as
large as it needs to be when the number is big." The guarantee is that the
address space within any subtree is inexhaustible. We state this as our
first property:

**T0 (Unbounded components).** For every tumbler `t = d₁. ... .dₙ` and
every component position `i` with `1 ≤ i ≤ n`, and every bound `M ∈ ℕ`,
there exists a tumbler `t'` in `T` that agrees with `t` on all components
except `i`, where `t'.dᵢ > M`.

This property is what separates the tumbler system from fixed-width
addressing. An implementation that silently truncates when a component
exceeds some representation limit violates T0. We observe that Gregory's
implementation uses a fixed 16-digit mantissa with an exponent field,
giving it a large but finite representable range. When `tumblerincrement`
overflows this range, the system terminates with a fatal error; when
`tumbleradd` overflows, it silently truncates. Both behaviors violate T0 —
the abstract specification demands unbounded components, and any correct
implementation must either provide them or prove that the reachable state
space never exercises the bound.

## The total order

We need a total order on `T`. Nelson describes the tumbler line as "a flat
mapping of a particular tree" — the depth-first traversal of the docuverse's
containment tree. Two tumblers are compared by the following rule:

**T1 (Lexicographic order).** For tumblers `a = a₁. ... .aₘ` and
`b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that
`(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (a is a proper prefix of b).

This is the standard lexicographic extension with the convention that a
prefix is less than any proper extension. The result is a total order: for
any `a, b ∈ T`, exactly one of `a < b`, `a = b`, or `a > b` holds.

The order must be decidable from the addresses alone — no index
consultation required. Nelson is unambiguous: "you always know where you
are, and can at once ascertain the home document of any specific word or
character." We state this as:

**T2 (Decidable comparison).** For any two tumblers `a, b ∈ T`, the
relation `a < b`, `a = b`, or `a > b` is decidable from the addresses
alone in time proportional to the lengths of `a` and `b`.

An important consequence of T1 is that equality of tumblers means
component-wise equality. There must be no representation in which two
distinct bit patterns denote the same abstract tumbler. We state this
as a separate requirement because it is exactly where implementations can
go wrong:

**T3 (Canonical representation).** Each tumbler `t ∈ T` has exactly one
representation. If two representations compare as order-equivalent under
T1, they are identical.

Gregory's implementation reveals a subtle violation: the tumbler struct
carries metadata fields (`xvartumbler`, `varandnotfixed`) that are ignored
by the ordering comparison (`tumblercmp`) but checked by the equality test
(`tumblereq`). The normalization routine (`tumblerjustify`) canonicalizes
the mathematical value (sign, exponent, mantissa) but leaves the metadata
fields untouched. This means two tumblers can be order-equivalent yet
compare as unequal — a violation of T3. The abstract specification demands
that order-equivalence and equality coincide. Any representation metadata
that can cause them to diverge must either be excluded from equality testing
or included in order comparison.

## Hierarchical structure

Tumblers are not flat identifiers. They encode a containment hierarchy:
server, account, document, element. Nelson uses zero-valued components as
delimiters — a tumbler has at most three zero components, partitioning it
into four fields:

```
Node . 0 . User . 0 . Document . 0 . Element
```

We formalize this. Let `0` denote a component with value zero. A tumbler in
the Xanadu I-space has the form:

```
t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ
```

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are the **node field**
(server), **user field** (account), **document field** (which may encode
version ancestry through further subdivision), and **element field** (which
distinguishes content subspaces). Not every tumbler need have all four
fields — a tumbler with only one zero addresses a document family, a
tumbler with no zeros addresses a server.

**T4 (Hierarchical parsing).** Every tumbler `t ∈ T` used as an I-space
address contains at most three zero-valued components, and these occur in
the order dictated by the four-field structure. The number of zeros
determines the specificity: zero zeros addresses a node, one zero a user
account, two zeros a document, three zeros an element.

From T1 and T4 together, a fundamental property follows: every subtree of
the containment hierarchy maps to a contiguous range on the tumbler line.
If server 2 contains accounts 2.0.1 through 2.0.47, then every tumbler
beginning with prefix `2` lies between `2` and the next server `3` (or
whatever follows). No tumbler from server 3 can interleave with server 2's
addresses, because the lexicographic order on the first component
separates them completely.

**T5 (Contiguous subtrees).** For any tumbler prefix `p`, the set
`{t ∈ T : p ≼ t}` (where `≼` denotes the prefix relation) forms a
contiguous interval under the total order T1. That is:

  `(A a, b, c : p ≼ a ∧ p ≼ c ∧ a < b < c : p ≼ b)`

This is the property that makes spans work. A span is a pair of tumbler
endpoints, and everything between them is determined by the tree structure.
Nelson: "The first point of a span may designate a server, an account, a
document or an element; so may the last point. There is no choice as to
what lies between; this is implicit in the choice of first and last
point." T5 is what makes this possible — if subtrees were not contiguous,
a span between two endpoints might include content from unrelated parts
of the hierarchy.

## Decidable containment

From T4 and T5, containment relationships are decidable by prefix
comparison:

**T6 (Decidable containment).** For any two tumblers `a, b ∈ T`, the
following are decidable from the addresses alone, by inspecting the
appropriate field:

  (a) Whether `a` and `b` belong to the same node (node fields equal).

  (b) Whether `a` and `b` belong to the same account (node and user fields
  equal).

  (c) Whether `a` and `b` belong to the same document family (node, user,
  and document-prefix fields equal).

  (d) Whether `a` is an ancestor-version of `b` within a document family
  (document field of `a` is a prefix of document field of `b`).

One qualification is necessary. Nelson warns that the version hierarchy
encoded in the document field records *structural subordination* — who
allocated the address — not *content derivation*. The address `5.3` tells
us that version `5.3` was created under document `5`, but not whether it
was forked from version `5`, from version `5.2`, or created empty. Formal
derivation history requires consulting the version graph, not just the
address. T6(d) captures the structural relationship; the semantic
relationship is outside the tumbler algebra.

## Permanence

The most consequential algebraic property is that once a tumbler is
assigned to content, the assignment is irrevocable:

**T7 (Address permanence).** If tumbler `a` is assigned to content at any
point in the system's history, then `a` remains assigned to that same
content for all subsequent states. No operation removes an address from
I-space, and no operation changes the content at an assigned address.

This is Nelson's P0: "any address of any document in an ever-growing
network may be specified by a permanent tumbler address." T7 is what makes
links stable — links reference I-space tumblers, and because those tumblers
are permanent, links survive all editing operations.

A consequence of T7 is that the I-space is append-only. New content
receives fresh addresses; existing addresses are never reused:

**T8 (Monotonic allocation).** Within any partition of the address space
(any fixed prefix), the allocation of new addresses is strictly monotonic.
If address `a` is allocated before address `b` within the same partition,
then `a < b` under the total order T1.

Gregory confirms this: I-address allocation uses `tumblerincrement` with
`rightshift=0`, producing a strictly increasing sequence like `2.1.0.1.0.1.3.1`,
`2.1.0.1.0.1.3.2`, `2.1.0.1.0.1.3.3`. The counter never retreats. T8 is
what prevents address collision within a partition — combined with the
hierarchical partitioning (T9 below), it prevents collision globally.

## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate
addresses without communicating. Nelson: "The owner of a given item controls
the allocation of the numbers under it." The mechanism is structural
partitioning — no two owners share a prefix:

**T9 (Partition independence).** The address space is partitioned by prefix
into ownership domains. Each domain has exactly one allocator. Two
allocators with distinct prefixes can allocate simultaneously, and the
resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of
the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any `a` with prefix `p₁`
and any `b` with prefix `p₂`, we have `a ≠ b`. This follows immediately
from the definition of prefix and the lexicographic order, but it is
worth stating explicitly because it is the mechanism by which a global
address space avoids global coordination.

Together, T8 and T9 guarantee address uniqueness:

**Theorem (Uniqueness).** No two distinct pieces of content ever receive
the same tumbler address.

*Proof.* Consider two allocations producing addresses `a` and `b`. If
they occur within the same partition (same owner prefix), T8 guarantees
`a ≠ b` because allocation is monotonic. If they occur in different
partitions, T9 guarantees `a ≠ b` because distinct prefixes produce
distinct addresses. ∎

## Tumbler arithmetic

We now come to the most delicate part of the algebra: the arithmetic
operations that editing requires. When content is inserted into a document
at virtual position `p`, all content after `p` must shift forward by the
length of the insertion. This shifting is performed by tumbler addition.
When content is deleted, the inverse shift is performed by tumbler
subtraction.

We must be careful here. The shift operations apply to **V-space positions**
— the mutable arrangement layer — not to I-space addresses (which are
permanent by T7). V-space positions are themselves tumblers, but they
represent "where this byte appears in the document right now," and that
changes with every edit.

### Addition for shifting

Let `⊕` denote tumbler addition, used to shift V-positions forward. We need:

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w`
represents a positive width, `a ⊕ w` is a well-defined tumbler in `T`.

**TA1 (Order preservation of addition).** For tumblers `a, b, w ∈ T` with
`w > 0` (positive width):

  `a < b ⟹ a ⊕ w < b ⊕ w`

This is the critical property for INSERT correctness. If two bytes were in
order before the insertion, they must remain in order after shifting.
Without TA1, an INSERT could scramble the relative ordering of content
within a document.

Gregory's implementation evidence reveals that TA1 likely holds for
same-exponent operands — i.e., when the positions and the width are at the
same hierarchical level — but is not proven for the general case. The
fixed-precision representation means that addition across widely different
exponent ranges may lose information. We observe that the system's correct
operation for INSERT depends on shifts occurring within a single subspace,
where exponents match. The abstract specification demands TA1 universally;
a correct implementation must either provide it or prove that only
same-exponent additions are reachable.

### Subtraction for shifting

Let `⊖` denote tumbler subtraction, used to shift V-positions backward
after deletion. We need:

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where
`a > w` (the position exceeds the width), `a ⊖ w` is a well-defined
tumbler in `T`.

**TA3 (Order preservation of subtraction).** For tumblers `a, b, w ∈ T`
with `w > 0` and `a > w` and `b > w`:

  `a < b ⟹ a ⊖ w < b ⊖ w`

**TA4 (Inverse).** For tumblers `a, w ∈ T` with `w > 0`:

  `(a ⊕ w) ⊖ w = a`

TA4 ensures that INSERT followed by DELETE at the same point restores the
original positions. Without it, the system could accumulate drift —
repeated insert-delete cycles shifting content progressively.

### Increment for allocation

A separate operation, distinct from the shifting arithmetic, is the
allocation increment. When the system allocates a new address, it takes
the highest existing address in a partition and produces the next one.
This is not addition of a width; it is advancement of a counter at a
specified hierarchical level.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`,
there exists an operation `inc(t, k)` that produces a tumbler `t'` such
that:

  (a) `t' > t` (strictly greater),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) the increment point is determined by `k` — when `k = 0`, the last
  significant component advances by one; when `k > 0`, a new component is
  created `k` positions deeper, producing a child rather than a sibling.

Gregory's analysis confirms this structure precisely. `tumblerincrement(t, 0, 1)`
advances the last significant digit: `1.1.0.3` becomes `1.1.0.4`.
`tumblerincrement(t, 1, 1)` extends one level deeper: `1.1.0.2` becomes
`1.1.0.2.1`. The `rightshift` parameter controls whether we produce the
next sibling (`k = 0`) or the first child (`k > 0`).

This is the mechanism by which the four-level hierarchy is populated:
creating a new account under a server uses `k = depth-1` to produce the
first child, while allocating successive documents under an account uses
`k = 0` to produce the next sibling at the document level.

## Subspace confinement

A document's element space is subdivided into subspaces: text content
lives in the `1.x` subspace, links in the `2.x` subspace. When INSERT
shifts text positions forward, link positions must not be affected. This
is a crucial structural invariant:

**TA6 (Subspace confinement).** Let `S₁` and `S₂` be distinct subspaces
within a document (e.g., text subspace `1.x` and link subspace `2.x`).
A shift operation (addition or subtraction of width `w`) applied to
positions in `S₁` must not alter any position in `S₂`.

Formally: if `a ∈ S₁` and `b ∈ S₂` with `S₁ ≠ S₂`, then the result of
shifting `a` by `w` produces a tumbler that is still in `S₁`, and the
position `b` is unchanged by the shift operation.

This property has a fascinating implementation history. Gregory reveals
that INSERT and DELETE achieve subspace confinement through entirely
different mechanisms:

- **INSERT** uses a structural mechanism: a "two-blade knife" that
  explicitly computes the boundary of the current subspace and classifies
  entries on either side. Entries beyond the boundary are never passed to
  the addition operation at all. The confinement is achieved by *not
  calling* the arithmetic, not by any property of the arithmetic itself.

- **DELETE** relies on an arithmetic accident: `strongsub` (the subtraction
  routine) contains an exponent guard that returns the minuend unchanged
  when the subtrahend has a lower exponent. Since text widths have lower
  exponents than link positions, subtracting a text width from a link
  position is a no-op. The confinement is achieved by an *incidental
  property* of the arithmetic.

The abstract specification does not prescribe either mechanism. TA6 states
what must hold; how it is achieved is an implementation choice. But the
asymmetry is instructive: the abstract property is the same, yet the two
operations rely on fundamentally different invariants to provide it. An
implementation that "fixes" the subtraction to handle cross-exponent
operands correctly would break DELETE's subspace isolation while leaving
INSERT's intact.

This teaches us something about the relationship between abstract
properties and implementation strategies: **TA6 is one property, but it
may require different proof obligations depending on the operation and
the implementation's arithmetic characteristics.** The specification must
state the property; the verification must check each operation separately.

## What tumbler arithmetic is NOT

We must note explicitly what the tumbler algebra does *not* guarantee.

**Non-associativity.** We do NOT require `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`.
Gregory's analysis suggests that fixed-precision implementations will
violate associativity when operands span different exponent ranges, and
even the abstract operation has no design need for associativity — shifts
are always applied as a single operation (shift by the inserted width),
never composed from multiple smaller shifts.

**Non-commutativity.** We do NOT require `a ⊕ b = b ⊕ a`. Tumbler
addition is a shift — "move position `a` forward by width `b`" — and
the operands play asymmetric roles. The first operand is a position; the
second is a displacement. Swapping them is not meaningful.

**No additive identity.** We do not require a zero tumbler that acts as
an identity for addition. Gregory notes that the implementation has two
representations of zero (positive and negative), which already complicates
identity. And the zero tumbler serves a different role — it is used as a
sentinel for uninitialized values, not as a neutral element.

The absence of these properties means tumbler arithmetic is NOT a group,
NOT a ring, NOT a field. It is a more modest structure: an ordered set
with a monotone shift operation. This is all that editing requires.

## The two address spaces

We have so far spoken of "tumblers" as if they formed a single space. In
fact, the system maintains two distinct spaces, each using tumblers as
addresses but with radically different algebraic contracts:

**I-space (identity space)** uses tumblers as permanent content identifiers.
The algebraic contract is:

  - T7 (permanence): once assigned, never removed or changed
  - T8 (monotonic allocation): new addresses always increase
  - T9 (partition independence): disjoint owners, no coordination
  - TA5 (hierarchical increment): allocation produces siblings or children

The arithmetic operations TA0–TA4 (addition, subtraction) are NOT used on
I-space addresses. I-space addresses are compared and allocated, never
shifted.

**V-space (virtual space)** uses tumblers as mutable document positions.
The algebraic contract is:

  - T1 (total order): positions are ordered
  - TA0–TA4 (arithmetic): positions shift on INSERT and DELETE
  - TA6 (subspace confinement): shifts respect subspace boundaries

V-space has NO permanence guarantee. Nelson is explicit: "The address of
a byte in its native document is of no concern to the user or to the front
end; indeed, it may be constantly changing." V-positions are ephemeral,
dense (contiguous from 1 to the document's current length), and
rearranged by every editing operation.

The document is the **mapping** between these two spaces: a function from
V-positions to I-addresses. INSERT, DELETE, and REARRANGE modify this
mapping. The I-addresses themselves are untouched — content does not move,
only the arrangement changes.

**T10 (Dual-space separation).** The permanence properties (T7, T8, T9)
apply to I-space addresses. The arithmetic properties (TA0–TA4, TA6) apply
to V-space positions. No operation applies shifting arithmetic to I-space
addresses, and no operation claims permanence for V-space positions.

This separation is the architectural core of the tumbler system. Links
attach to I-space addresses and therefore survive editing. Editing
operations modify V-space positions and therefore do not break permanence.
The two spaces share the same carrier set `T` and the same ordering T1,
but their algebraic contracts are disjoint.

## Spans as an algebraic consequence

A span is a pair `(start, length)` where `start ∈ T` and `length ∈ T`
represent a contiguous range of addresses. From T1 (total order) and T5
(contiguous subtrees), we can derive that a span in I-space identifies a
contiguous set of addresses at any level of the hierarchy — a single
byte, a range of bytes, an entire document, everything by one author,
or everything on one server.

**T11 (Span well-definedness).** A span `(s, ℓ)` with `s ∈ T` and
`ℓ > 0` denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is
non-empty (it contains at least `s`) and contiguous under T1 (there
are no gaps — any tumbler between two members of the set is also a
member).

The contiguity of spans follows from T5: the set of all tumblers sharing
a prefix is contiguous, and a span within a subspace is a sub-interval
of such a set. Spans are the fundamental unit of content reference in the
system — links reference spans, transclusion copies spans, and the POOM
(the permutation of the original media) is a sequence of spans mapping
V-positions to I-addresses.

## Formal summary: the tumbler algebra

We collect the structure. The tumbler algebra is a six-tuple
`(T, <, ⊕, ⊖, inc, fields)` where:

- `T` is the carrier set of finite sequences of non-negative integers (T0)
- `<` is the lexicographic total order on `T` (T1, T2)
- `⊕ : T × T → T` is order-preserving addition for V-space shifts (TA0, TA1)
- `⊖ : T × T → T` is order-preserving subtraction for V-space shifts (TA2, TA3)
- `⊕` and `⊖` are mutual inverses (TA4)
- `inc : T × ℕ → T` is hierarchical increment for allocation (TA5)
- `fields : T → Node × User × Document × Element` is the parser that
  extracts the four hierarchical fields (T4)

The algebra satisfies:

- Unbounded components (T0)
- Canonical representation (T3)
- Contiguous subtrees (T5)
- Decidable containment (T6)
- Address permanence for I-space (T7)
- Monotonic allocation (T8)
- Partition independence (T9)
- Dual-space separation (T10)
- Span well-definedness (T11)
- Subspace confinement for V-space arithmetic (TA6)

This is a minimal set. Each property is required by at least one system
guarantee: T7 for link stability, T5 for span queries, T9 for
decentralization, TA1 for INSERT correctness, TA6 for subspace isolation.
Removing any property breaks a system-level guarantee.

## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| T0 | Every tumbler component is unbounded — no maximum value | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison with prefix-less-than convention | introduced |
| T2 | Tumbler comparison is decidable from the addresses alone in time proportional to their length | introduced |
| T3 | Each tumbler has exactly one canonical representation; order-equivalence implies equality | introduced |
| T4 | An I-space tumbler has at most three zero-valued components, partitioning it into four hierarchical fields (node, user, document, element) | introduced |
| T5 | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | Containment (same node, same account, same document family, ancestor-version) is decidable from addresses alone | introduced |
| T7 | Once a tumbler is assigned to content, the assignment is permanent and the content at that address is immutable | introduced |
| T8 | Within any partition (fixed prefix), new allocations are strictly monotonically increasing | introduced |
| T9 | Disjoint ownership prefixes guarantee distinct addresses without coordination | introduced |
| T10 | Permanence (T7–T9) applies to I-space; arithmetic (TA0–TA4, TA6) applies to V-space; the contracts are disjoint | introduced |
| T11 | A span (start, length) denotes a contiguous, non-empty set of tumblers | introduced |
| TA0 | Tumbler addition `a ⊕ w` is well-defined for positive width `w` | introduced |
| TA1 | Addition preserves the total order: `a < b ⟹ a ⊕ w < b ⊕ w` for `w > 0` | introduced |
| TA2 | Tumbler subtraction `a ⊖ w` is well-defined when `a > w` | introduced |
| TA3 | Subtraction preserves the total order: `a < b ⟹ a ⊖ w < b ⊖ w` when both are defined | introduced |
| TA4 | Addition and subtraction are mutual inverses: `(a ⊕ w) ⊖ w = a` | introduced |
| TA5 | Hierarchical increment `inc(t, k)` produces `t' > t` at the specified level, yielding a sibling (k=0) or child (k>0) | introduced |
| TA6 | Shift operations (⊕, ⊖) applied within one subspace do not affect positions in any other subspace | introduced |

## Open Questions

How must tumbler arithmetic interact with the zero-valued field separators — can addition ever produce or consume a zero component, and what constraint prevents shifting a V-position across a field boundary?

What algebraic property of the POOM (the V→I mapping) must hold for span intersection to be computable from the mapping alone, without enumerating individual positions?

Must the width used in shift operations (⊕, ⊖) always share the same hierarchical depth as the positions being shifted, or can the system guarantee TA1 and TA6 for widths at arbitrary depths?

What must a correct implementation guarantee about allocation counter durability across crashes — is monotonicity (T8) a per-session or a global-history requirement?

Under what conditions does tumbler addition compose — are there system states where two successive shifts `(a ⊕ w₁) ⊕ w₂` must equal a single shift `a ⊕ (w₁ + w₂)`, and if so, what precondition restricts the operands?

What must the system guarantee when comparing tumblers from different subspaces — does the total order T1 extend meaningfully across the text/link boundary, or is cross-subspace comparison only well-defined for containment queries?

If version-derivation is not decidable from addresses alone (T6 qualification), what minimal auxiliary structure must the system maintain to reconstruct the derivation graph?
