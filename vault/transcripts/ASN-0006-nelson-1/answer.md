Let me check the raw page for the COPY operation to see exactly what Nelson says about identity there.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-234.png"}}
</tool_call>

Let me also check the page describing inclusions and native vs non-native bytes.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-178.png"}}
</tool_call>

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-177.png"}}
</tool_call>

And the page on FINDDOCSCONTAINING, which depends on this identity question.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-237.png"}}
</tool_call>

---

## Transclusion preserves identity. Copying creates new identity.

This is the central architectural distinction, and Nelson builds the entire system around it.

### The I-address IS identity

Every byte created in Xanadu gets a permanent I-space address encoding its origin — which server, which account, which document, which element position. That I-address is the byte's **identity**, not its value.

Two documents containing the word "hello" typed independently have **different** I-addresses. The bytes are value-identical but identity-distinct. Conversely, when content is transcluded, both the original and the transclusion reference the **same** I-address. The bytes are not merely value-identical — they are the *same bytes*.

### Transclusion: same identity, different arrangement

When you transclude content (Nelson's COPY operation in FEBE, or his "quote-window" / "inclusion"), the receiving document's V-space maps to the **original** I-addresses. No new content is created in I-space. The transclusion is a reference, not a reproduction.

Nelson is explicit about the mechanism:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The term "virtual copies" is precise: they appear as if copied but are not. The bytes live at their home location. The receiving document merely points to them.

### INSERT: new identity

By contrast, INSERT creates **new** content in I-space:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Inserted text gets fresh I-addresses under the receiving document. It is new content with a new identity — even if the bytes happen to be identical to something already in the docuverse.

### Why this distinction matters: three consequences

**1. Attribution is structural, not metadata.**

Because transclusions share I-addresses with the original, the system always knows where content came from:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This cannot be stripped or falsified within the system. The fetching mechanism itself requires consulting the home location. Attribution is not a tag on the content — it is the address *of* the content.

**2. FINDDOCSCONTAINING works.**

The operation that finds all documents containing a given piece of content depends entirely on shared I-addresses:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

If transclusion created new I-addresses, this operation would be impossible — you could not trace from a passage in one document to all other documents containing that same passage. Shared identity is what makes the web of transclusion discoverable.

**3. Correspondence across versions is computable.**

SHOWRELATIONOF2VERSIONS returns corresponding span pairs between two versions. This works because versions created by CREATENEWVERSION share I-addresses for unchanged content. Shared I-address *means* correspondence:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

The system does not compare text values to find matches. It compares I-addresses. Identity, not equality.

### The glass pane metaphor

Nelson's visual metaphor makes the identity point intuitive:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else; the next pane may be in turn made of more layers of painted glass, with more windows, and so on indefinitely." [LM 2/34]

Painted content (INSERT) is new material — new I-addresses, new identity. Clear glass (transclusion) is a window onto existing material — same I-addresses, same identity. You are not looking at a reproduction of the other document. You are looking *through* to the other document itself.

### Live vs dead

This identity-preservation is what makes transclusions "live" and copies "dead":

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

A transclusion participates in the network because it shares identity with the original. Links made to the original content reach the transclusion. New links made to the transclusion reach the original. A true copy (outside the system) severs this — it creates new bytes with no I-address, no identity, no connection.

### Summary

| Operation | I-addresses | Identity | Nelson's term |
|-----------|-------------|----------|---------------|
| INSERT | Fresh (new content) | New identity | "native bytes" |
| COPY (transclusion) | Shared (same as source) | Same identity | "inclusions," "virtual copies" |
| External copy | None (outside system) | No identity | "frozen and dead" |

The answer to your question is unambiguous: transcluded content retains the **same identity** as the original. It does not acquire a new one. This is not a design choice among alternatives — it is the foundation on which permanence, attribution, correspondence, and the entire economic model rest.