## Question 9 [nelson]

> When content is quoted or transcluded into a new document, must the address visible to the reader be the original author's address, preserving the connection to source?

## Yes — and it's structural, not optional

When content is transcluded, the original author's I-space address **is** the address of that content. There is no separate copy with a different address. The connection to source is not a feature that could be turned on or off — it is an architectural consequence of how transclusion works.

### The mechanism

Transclusion (COPY in FEBE) creates a V-space mapping to **existing** I-space content. The I-space address encodes the originating document:

```
Node.0.User.0.Document.0.Element
```

When a reader encounters transcluded content, the system fetches it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The transcluded bytes are not duplicated — they are referenced. The I-address of every byte permanently encodes which document created it, which user owns that document, and which server stores it. This cannot be severed because the fetching mechanism requires it.

### The guarantee

Nelson states this as an absolute:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And from the fundamental guarantees: attribution is **structural, not metadata that can be stripped**. In conventional systems, an author field or copyright notice can be removed during copying. In Xanadu, the I-address IS the attribution — to access the content at all, you must resolve its home address.

### What the reader sees

The reader interacts through V-space — the document's current arrangement. Transcluded content occupies V-space positions in the quoting document "just as if they were native to the document" [LM 4/11]. But the system always knows the difference:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Nelson's glass-pane metaphor makes the reader experience vivid:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

The reader can always "step through the window" to reach the original work. And from any character, the reader can query which document is its home. The front end determines how prominently this information is displayed, but the system must always make it available.

### Bidirectional discovery

The connection works in both directions. Not only can a reader of the quoting document trace content back to its source, but a reader of the **original** document can discover all documents that transclude from it:

> FINDDOCSCONTAINING: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This is possible precisely because transcluded content shares I-addresses with the original — the system can find every document that references a given piece of I-space content.

### Why this matters

This is not an incidental property. It is the mechanism that makes automatic royalties, permanent attribution, and the "pluralistic publishing form" possible. When content is transcluded and delivered to a reader, the system knows exactly whose content it is delivering and can route payment accordingly:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

The original author's address is preserved not merely as a courtesy but as the structural foundation of the entire economic and intellectual model. Sever the connection, and you break attribution, royalties, bidirectional discovery, and the web of literature itself.
