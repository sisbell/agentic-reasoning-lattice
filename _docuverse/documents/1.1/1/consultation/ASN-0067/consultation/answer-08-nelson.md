## Question 8 [nelson]

> Does the act of placing content at a position establish any persistent relationship between the source location and the destination, or is it a one-time arrangement with no ongoing dependency?

## COPY Establishes a Persistent Structural Relationship; INSERT Does Not

The answer depends entirely on *which* operation places the content.

### INSERT / APPEND: No Ongoing Relationship

INSERT and APPEND create **new native bytes** in the document's Istream. These bytes get fresh I-addresses belonging to that document. There is no source to maintain a relationship with — the content is born here.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

### COPY (Transclusion): Persistent Structural Dependency

COPY does not duplicate bytes. It creates a Vstream mapping that points to the **same I-addresses** as the source. This is not a one-time snapshot — it is an ongoing structural reference.

The persistence manifests in five ways:

**1. Shared identity.** The transcluded bytes in the destination have the *same* I-addresses as in the source document. Two documents containing identical text created independently have *different* I-addresses. Transcluded content shares them. This is how the system distinguishes "wrote the same words" from "quoted from the original."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

**2. Origin is permanently traceable.** Because the I-address encodes the home document (Node.0.User.0.Document.0.Element), you can always determine where transcluded content came from — not by metadata that could be stripped, but by the address itself.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

**3. Discovery works because the relationship persists.** FINDDOCSCONTAINING "returns a list of all documents containing any portion of the material included by \<vspec set\>" [LM 4/70]. This operation is only possible *because* the shared I-addresses create an ongoing, queryable relationship between source and destination.

**4. Version correspondence derives from it.** SHOWRELATIONOF2VERSIONS computes which parts of two documents correspond by examining shared I-addresses. This is not metadata — it is a structural property that emerges from the COPY relationship and persists as long as the content exists.

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

**5. Royalty accounting depends on it.** The system splits payment between original author and quoter precisely because the shared I-addresses identify who created what:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

### The Retrieval Mechanism Enforces the Dependency

Non-native bytes are not cached copies — they are fetched from their home:

> "All other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This means the destination document *operationally depends* on the source's continued existence in Istream. The relationship is not just bookkeeping; it is the retrieval path.

### Two Modes of Ongoing Relationship

Nelson specifies that transclusions can be either:

- **Location-fixed** (floating in time): updates propagate automatically — you always see the current state of the source
- **Time-fixed**: shows the version at a specific moment, but you can ask "What has this passage become?"

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

Both modes maintain the relationship. The difference is only whether the *view* floats or is pinned.

### Summary

| Operation | Creates new I-addresses? | Ongoing relationship? | Discoverable via FINDDOCSCONTAINING? |
|-----------|-------------------------|----------------------|--------------------------------------|
| INSERT | Yes (native bytes) | No | No — content is native |
| COPY | No (shares source I-addresses) | Yes — structural, permanent | Yes — shared I-addresses are the mechanism |

COPY establishes a persistent, structural, queryable dependency between source and destination. It is not a one-time arrangement. The dependency is encoded in the address system itself and cannot be severed within the system.
