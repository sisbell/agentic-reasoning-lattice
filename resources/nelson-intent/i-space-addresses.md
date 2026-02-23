# I-Space Addresses (Identity Space)

Source: Literary Machines, 4/10-4/11, 4/26-4/30

## What It Means

I-Space is the permanent address space where content resides. Every byte ever stored in Xanadu has a permanent I-Space address that never changes.

An I-Space address is a tumbler with four major fields separated by zeros:

```
Node.0.User.0.Document.0.Element
```

**The four fields:**
1. **Node** — Which server stores the document. Always begins with digit 1 (the entire docuverse).
2. **User** — Who owns the document. Continually subdividable for sub-accounts.
3. **Document** — The logical entity. Can be subdivided for versions: "an accidental extension of the document number" (4/29).
4. **Element** — Individual contents. Two types: Bytes and Links.

**Element field structure:**
- Bytes: sequential positions in the content stream
- Links: "The digit after the '3' is a link-address designating the link's serial position" — links are currently not rearrangeable

## How I-Space Differs from V-Space

I-addresses are permanent; V-addresses are ephemeral:
- I-address: "where this byte lives forever"
- V-address: "where this byte appears in the document right now"

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

## User Guarantee

- Every byte you create gets a permanent I-address
- That address will always return that exact content
- Content at an I-address never changes
- Links can reference I-addresses and survive editing
- "Deleted" content is still at its I-address

## Principle Served

I-Space addresses enable permanent citation. Because I-addresses are permanent, citations never break, links survive edits, transclusions always resolve, and history is preserved.

## Nelson's Words

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." (4/28)

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." (4/28)

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (4/29)

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)
