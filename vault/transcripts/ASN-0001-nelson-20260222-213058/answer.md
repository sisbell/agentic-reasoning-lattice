## Yes, With One Important Qualification

The tumbler address system is designed so that field-level relationships are **syntactically decidable from the addresses alone**, with no index consultation required. But the *derivation history* between versions within a document family is not fully encoded.

### Why It Works: Self-Describing Structure

Tumbler addresses have **at most three zero digits** that serve as unambiguous field separators:

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

This parsing is purely syntactic. Given any address, you find the zeros and extract four fields:

```
Node . 0 . User . 0 . Document . 0 . Element
```

Given two addresses, comparing these fields tells you:

| Question | Method | Index needed? |
|----------|--------|---------------|
| Same account? | Compare Node and User fields | No |
| Same document family? | Compare Document field prefixes | No |
| Same version? | Exact match through Document field | No |
| Entirely separate accounts? | Node+User fields differ | No |

### The Version Subtlety

Within the Document field, versions are created by forking — appending sub-digits:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

So document `5` may have versions `5.1`, `5.2`, `5.3`, and `5.1` may have sub-versions `5.1.1`, `5.1.2`. From addresses alone, you can determine:

- `5.3` is **under** `5` (prefix match)
- `5.1.1` is **under** `5.1`, which is **under** `5` (prefix chain)
- `5.3` and `5.7` are **siblings under** `5`

This is decidable by simple prefix comparison — no index required.

### What Is NOT Decidable: Derivation

Here is the qualification. Nelson explicitly warns:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The address `5.3` tells you it was *created under* document `5` — the owner of `5` allocated it. But it does not tell you:

- Whether `5.3` was produced by `CREATENEWVERSION(5)` or `CREATENEWVERSION(5.2)`
- Whether `5.3` has any content relationship to `5` at all (it could be a blank sub-document)
- Which version was the *source* for any given fork

The FEBE spec says `CREATENEWVERSION` will produce an address that "will indicate its ancestry" [LM 4/66], but Nelson's qualification at 4/29 limits how much you may infer from that indication. The address encodes *ownership hierarchy* (who allocated it), not *content derivation* (what it was forked from).

### The Element Subspace Is Also Decidable

Within the Element field (after the third zero separator), the subspace indicator distinguishes content types:

- Byte subspace: `...0.1.N` (text positions)
- Link subspace: `...0.2.N` (link instances)

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

So you can also determine from two addresses alone whether they refer to bytes or links within the same document — again, no index needed.

### Summary

The tumbler system is deliberately designed so that the **structural relationships** between addresses — same account, same document family, same version, same subspace — are decidable from the addresses alone through syntactic parsing and prefix comparison. The one thing that escapes purely address-based reasoning is the **derivation graph**: which version was actually the source for which. That requires consulting the system's version history, not just the tumbler strings.