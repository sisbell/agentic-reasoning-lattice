## Question 20 [nelson]

> Must the addressing scheme guarantee that content positions, link positions, and structural positions can never collide — that their regions are permanently disjoint?

## Yes — Permanent Disjointness Is Guaranteed by the Tumbler Structure

The tumbler addressing scheme guarantees that content positions, link positions, and structural positions can never collide. This falls out of two structural mechanisms that Nelson designed into the system.

### Mechanism 1: Three Zero Delimiters Create Four Permanent Fields

A tumbler address has four major fields separated by zeros:

```
Node . 0 . User . 0 . Document.Version . 0 . Element
```

Nelson specifies:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

The zeros are not values but **punctuation** — structural delimiters that permanently partition the address space. A server address (one zero-delimited field) can never be confused with an account address (two fields), a document address (three fields), or an element address (four fields). The count of zero delimiters in the address uniquely determines what level of the hierarchy it names.

This means structural positions (servers, accounts, documents) and element positions (bytes, links) are permanently disjoint by their position in the hierarchy.

### Mechanism 2: Subspace Identifiers Separate Bytes from Links

Within the fourth field (Contents/Elements), a subspace identifier permanently separates content from links:

- **Bytes**: `...0.1.position` — subspace 1
- **Links**: `...0.2.number` — subspace 2

The curated link source confirms:

> `N.0.U.0.D.V.0.2.1` — the first link of the document [LM 4/31]
> `N.0.U.0.D.V.0.2.755` — the 755th link [LM 4/31]

And for bytes:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

Because `1` and `2` are different digits at the same position in the tree, no byte address can ever equal a link address. The subspace identifier is the first digit after the third zero delimiter, and it is permanently fixed at creation time.

### Forking Cannot Cross Boundaries

The forking mechanism — the only way new addresses are created — operates strictly within a region:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

Forking under `2.x` produces `2.x.y`, never anything in the `1.x` space. Children are always beneath their parent in the tree. The zero delimiters and subspace identifiers are structural, not subject to forking or reassignment.

### The Humber Foundation

The disjointness guarantee rests ultimately on the humber encoding, where:

> "The Completeness bit is zero if the actual number is within the byte, 1 if it is not; this choice makes an all-zero byte a true zero (a fact which will be seen to be a useful choice for the tumbler mechanism)." [LM 4/13]

Zero is unambiguously representable, so the three zero delimiters can always be parsed without ambiguity. There is no encoding collision between a zero-as-delimiter and a zero-as-value.

### Summary

The disjointness is guaranteed at two levels:

| Boundary | Mechanism | What It Separates |
|----------|-----------|-------------------|
| Hierarchical fields | Three zero delimiters | Structural positions (server, account, document) from element positions |
| Element subspaces | Subspace identifier (1 vs 2) | Content positions from link positions |

Both are permanent by construction — they are part of the address syntax, not metadata that could be lost or corrupted. Nelson designed them as "lexical significance" built into the number system itself. The disjointness holds for all time because no operation in the system can move an address from one field or subspace to another; the boundaries are structural punctuation, not values.

Nelson also noted that the link subspace could be further subdivided:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

Any such subdivision would remain within the `2.x` region, preserving disjointness with the byte subspace.
