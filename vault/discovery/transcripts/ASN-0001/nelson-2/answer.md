## Yes — containment is structurally readable from the address alone.

A tumbler address encodes its full containment hierarchy through **three zero delimiters** that act as structural punctuation:

```
Node.0.User.0.Document.Version.0.Element
```

Nelson is explicit about this:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

Given any tumbler — say `1.3.0.5.2.0.7.1.0.2.4` — you can parse it mechanically:

| Field | Value | How found |
|-------|-------|-----------|
| **Node** | `1.3` | Before first `.0.` |
| **Account** | `5.2` | Between first and second `.0.` |
| **Document.Version** | `7.1` | Between second and third `.0.` |
| **Element** | `2.4` | After third `.0.` (subspace 2 = link, instance 4) |

The element subspace is also readable: `0.1.x` for bytes, `0.2.x` for links. From the link address examples:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

### One nuance: document vs. version within the Document field

The three zeros reliably separate the four major fields. But within the Document field, the boundary between "base document" and "version" is **not syntactically marked** — it depends on the forking tree. Nelson is candid:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

So `7.1` in the document field could mean "version 1 of document 7" or "sub-document 7.1" — the address alone doesn't distinguish these. You can always read that the content belongs to the document-lineage `7.1`, but interpreting whether `.1` is a version or a daughter document requires knowing the tree's shape.

### The server field has a known root

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

This means the first digit is always `1`, and sub-digits represent server forking — also readable from the address.

### Summary

**Account, document-lineage, and element type are always readable from the address alone.** The zeros are unambiguous structural delimiters, and ownership follows directly from address parsing:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

The only aspect that requires external knowledge is the document-vs-version boundary within the document field — a deliberate design choice, since Nelson treats versions as "accidental extensions" of document numbers rather than structurally distinct entities.