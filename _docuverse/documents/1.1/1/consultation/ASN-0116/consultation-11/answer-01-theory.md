## Question 1 [theory]

> Is the binding of newly inserted content to its inserting document meant to be established as part of the insertion itself, or is provenance a separately-maintained relation distinct from the act of placing content?

Based on the curated sources, I can answer this directly. The short answer: **for natively inserted content, the binding to the inserting document IS the act of insertion** — provenance is intrinsic and structural, not a separately-maintained relation layered on afterward.

## The binding is structural, established by the I-address assigned at insertion

When you INSERT content, it becomes a *native byte* of that document, and native bytes receive a permanent Istream address under that document's tumbler space. The Istream address has the form `Node.0.User.0.Document.0.Element`, and the **Document field directly encodes which document created the byte**. That assignment happens by virtue of placing the content — there is no separate "record the origin" step.

From `i-space-addresses` (4/11):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."

The `operations` and `tumblers` sources confirm that INSERT is precisely the act that mints these addresses: "INSERT, APPEND | New content gets fresh tumbler addresses." The FEBE definition (4/66) is purely about placement — "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`" — yet that placement is what assigns the I-address, and the I-address is what carries the provenance.

## Provenance is explicitly *not* strippable metadata

The `origin-traceability` source makes the strongest statement that this is structural rather than a separately-maintained relation:

> "In conventional systems, attribution is a property attached to content — an author field, a copyright notice, a citation. These can be copied without the attribution... In Xanadu, the origin IS the address."

And Nelson's own words (2/40):

> "You always know where you are, and can at once ascertain the home document of any specific word or character."

Because fetching the content requires requesting it from its home location (the I-address), "the connection cannot be severed because the fetching mechanism requires it" (`origin-traceability`). Provenance is therefore not a relation maintained alongside the content — it is the content's identity.

## The important contrast: INSERT vs. COPY (transclusion)

The one nuance worth flagging is *which* document provenance binds to. Your question says "newly inserted content," which I read as native INSERT — that binds to the inserting document. But the parallel placing operation, COPY, behaves differently:

From `operations` (4/67): COPY "is transclusion — the copy shares I-addresses with the source." And from `sporgl-provenance` (4/11):

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies."

So COPY *places* content into a document without binding its provenance to that document — the I-address still points to the original home. This actually reinforces the answer to your question: provenance tracks **where bytes were created**, not **where they were placed**. For native INSERT the two coincide (creation happens at placement), so the binding is part of the insertion. For COPY they diverge, precisely because placement and origin are different events.

## Summary

Binding of newly inserted (native) content to its inserting document is established **as part of the insertion itself** — the INSERT mints a fresh Istream address whose Document field *is* the provenance. It is not a separately-maintained relation. The system deliberately makes origin a structural property of the address rather than detachable metadata, which is why COPY/transclusion can place content *without* re-binding its provenance: provenance follows creation, and for native insertion creation and placement are the same act.
