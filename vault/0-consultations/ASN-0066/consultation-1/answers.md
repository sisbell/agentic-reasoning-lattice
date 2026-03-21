# Revision Consultation — ASN-0066

**Review:** review-1.md
**Date:** 2026-03-21 12:59

## Summary

6 REVISE items analyzed: 5 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 6: Starting-position constraint absent

**Category:** NELSON
**Reason:** Nelson's quote specifies "addresses 1 through 100," implying positions start at 1. Whether this is a prescriptive design constraint or merely an illustrative example is a question about design intent that only the Nelson source can resolve.

**Nelson question:** Does the Vstream design require that V-positions within a subspace always start at ordinal 1 (i.e., addresses are 1 through n), or is the starting position determined by the allocation mechanism and intentionally left unspecified?

**Nelson's Answer:**

The raw page files aren't available in this repository. Let me work from the curated sources, which contain verified quotes from the relevant pages.

---

## Answer: V-positions start at 1, by structural necessity

The Vstream design **requires** that positions within a subspace start at ordinal 1. This is not explicitly stated in a single sentence by Nelson, but it follows necessarily from the tumbler numbering conventions he does specify.

### Evidence 1: Link positions explicitly start at 1

Nelson's example of link addressing within a document [LM 4/31]:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.2    → second link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

The first link in subspace 2 is at position **1**, not 0. This establishes the convention for element-level addressing within subspaces.

### Evidence 2: Forking always starts at 1

Nelson specifies the general numbering convention [LM 4/20]:

> "if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2."

The first child is always **.1**. This convention applies uniformly throughout the tumbler system — servers, accounts, documents, versions, and element positions all begin numbering at 1.

### Evidence 3: Zero is structurally reserved

Zero has a special role in tumblers as a field separator [LM 4/13]:

> "this choice makes an all-zero byte a true zero (a fact which will be seen to be a useful choice for the tumbler mechanism)."

The three major dividers in a tumbler address are zeros [LM 4/28]:

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

Position 0 within a subspace would be structurally ambiguous — it could be confused with a field separator. This makes 0 unavailable as a content position, forcing 1-based numbering.

### Evidence 4: V-stream positions are dense and ordinal

Nelson describes V-stream byte positions [LM 4/30]:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."

And INSERT shifts all following positions [LM 4/66]:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

V-positions form a dense, gap-free sequence. Combined with 1-based numbering, this means a document with *n* bytes always has V-positions 1 through *n*.

### Conclusion

The starting position is **not left unspecified** — it is determined by the tumbler numbering convention. All ordinal positions in the tumbler system start at 1 because:

1. Zero is reserved for field separation (structural constraint)
2. Forking/numbering starts at 1 (explicit convention, 4/20)
3. Link subspace positions start at 1 (explicit example, 4/31)
4. There is no mechanism or precedent for position 0 anywhere in the tumbler system

The byte subspace follows the same convention as the link subspace: the first element is at position 1. This is consistent across both I-stream (permanent) and V-stream (ephemeral) addressing, since both are expressed as tumbler digits within the element field.
