## Question 9 [nelson]

> If a document contains content placed from two different sources, must the system preserve the distinct origin identity of each portion, or may it treat the combined result as a single undifferentiated span?

## The system MUST preserve distinct origin identity. This is not optional — it is structural.

### The Architectural Reason

Every byte in Xanadu has a permanent Istream address encoding its home document:

```
Node.0.User.0.Document.0.Element
```

When you COPY (transclude) content from two different sources into your document, each portion retains its original I-addresses. The Vstream arranges them into a contiguous sequence for the reader, but the underlying I-addresses remain distinct. Merging them into one undifferentiated span is architecturally impossible without destroying the addressing model itself.

Nelson states this as a user-facing guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And from the technical specification:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The phrase "home locations" (plural) is significant. Each non-native span has its own home, and retrieval goes back to that home. A compound document with content from two sources necessarily makes two separate requests to two separate homes.

### Identity Is Based on Creation, Not Value

Even if the content from two sources happens to be textually identical, the system treats them as distinct:

Content identity is based on creation origin, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address only when it shares the same origin. This is how the system distinguishes "wrote the same words" from "quoted from the original."

### Why Merging Would Violate Core Guarantees

Treating combined content as a single undifferentiated span would break at least four fundamental mechanisms:

1. **Attribution.** If portions from Source A and Source B were merged, you could no longer "ascertain the home document of any specific word or character" [LM 2/40]. The attribution guarantee is structural — encoded in the I-address — not metadata that could survive a merge.

2. **Royalties.** Different owners receive royalties for their respective content:

   > "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

   "Determined automatically" means from the I-addresses. If the system cannot distinguish which bytes came from which source, it cannot split royalties.

3. **FINDDOCSCONTAINING.** This operation "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. It works by tracing I-addresses. If origin identity were lost, this operation would fail — you could not find which documents share content with a given source.

4. **Correspondence and version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. Correspondence is determined by shared I-addresses. Merging destroys this signal.

### The Glass Pane Metaphor Confirms It

Nelson's metaphor for compound documents makes the separation visual:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Each window is a distinct opening to a distinct source. The glass pane model has no concept of "merging" two windows into one — each remains a separate transparent region showing content from its specific origin.

### Summary

The system **must** preserve distinct origin identity for each portion. This is not a policy choice but an architectural invariant: the I-address of every byte permanently encodes its home document, and the system's guarantees of attribution, royalty, discoverability, and correspondence all depend on this encoding being preserved through all operations, including composition of content from multiple sources.
