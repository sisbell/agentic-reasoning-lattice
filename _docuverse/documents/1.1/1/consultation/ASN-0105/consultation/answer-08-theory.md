## Question 8 [theory]

> Must reading the same span twice, with no intervening edits, return content identical in both substance and order, and what guarantees this stability?

## Yes — reading the same span twice with no intervening edits must return identical content in both substance and order. This is a foundational guarantee of the design.

The stability rests on the **Istream/Vstream separation**, and breaks down into two distinct guarantees:

### Substance is guaranteed by Istream immutability

Content lives permanently in the Istream (Invariant Space), where addresses are "absolute and immutable" and "content at an Istream address **never changes**" (see `i-space-v-space.md`). A read resolves a span's Vstream positions down to Istream addresses, then returns the bytes stored there. Because those bytes are immutable, the *substance* you get back is fixed:

> "Content you create gets a permanent Istream address. That address will always return that exact content. Content is immutable - it never changes after creation."

This is why "deleted" content is still recoverable and why links survive editing — the bytes themselves are never altered, only re-arranged.

### Order is guaranteed by the stable V→I mapping (absent edits)

A document *is* its Vstream mapping from V-addresses to I-addresses. Order is not a property of the content but of this arrangement. The reason it can change at all is editing:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The phrase "may be constantly changing" is precisely about **editorial operations**. INSERT/DELETE/REARRANGE alter the V→I mapping (see `operations.md`). With *no intervening edits*, the mapping is unchanged, so the same span enumerates the same I-addresses in the same sequence.

### Why order within a span is deterministic

A span is not a list of bytes you assemble freely — its extent and ordering are fixed by its endpoints:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

The Vstream is also dense and totally ordered ("V-address 1 is always the first byte... no gaps" — see `v-space-addresses.md`), so a span resolves to one definite ordered sequence.

### The retrieval operation is a deterministic function

`RETRIEVEV` is defined purely in terms of its argument: "This returns the material (text and links) determined by `<spec set>`" (4/67). Given the same spec-set against an unchanged document state, it is a pure function of (span, document arrangement, Istream). The "part-pounce" model materializes the part on demand from fragments — "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16) — but reconstruction is deterministic, not regenerative.

### Summary of what guarantees stability

| Guarantee | Mechanism | Source |
|-----------|-----------|--------|
| Same *substance* | Istream content is immutable | `i-space-v-space.md`; 4/11 |
| Same *order* | V→I mapping changes only on edit | 4/11; `operations.md` |
| Deterministic span extent | Endpoints fix everything between | 4/25 |
| Deterministic retrieval | RETRIEVEV is a function of its spec-set | 4/67 |

---

**One caveat / inference flag:** Nelson never states an explicit "reads are idempotent/deterministic" theorem in the curated sources. The conclusion above is a direct, well-grounded inference from Istream immutability + the edit-only mutability of the Vstream arrangement, not a verbatim Nelson guarantee. If you want his exact wording on read determinism or any subtlety around transcluded (non-native) bytes whose *home* document is edited concurrently — note that "no intervening edits" must mean no edits to any home document supplying the span, since a span may include bytes native elsewhere (4/11) — then: NEED_RAW: 4/61-4/70 (RETRIEVEV semantics), 2/16-2/19 (part-pounce/prismatic retrieval).
