## Question 6 [theory]

> Must the returned set always describe the same kinds of content for every document, so that two documents' reports can be meaningfully compared?

## Short answer

Yes. The operation that reports a document's content extent — **RETRIEVEDOCVSPANSET** — always returns the *same kinds* of content for every document, which is precisely what makes two documents' reports comparable.

## Why

Nelson defines the operation this way:

> "RETRIEVEDOCVSPANSET ... This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

The returned span-set always describes the same two categories — **text bytes** and **links** — because every Xanadu document is structured into the same fixed subspaces. The document-local address space is uniform across the docuverse:

| Subspace | Address Pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.position` (1.x) | Text content |
| Links | `version.0.2.N` | Links stored in this document |

Since this subspace division (`1` for bytes, `2` for links) holds for *every* document, the span-set returned for document A reports the same two dimensions as the span-set returned for document B. An empty document simply reports zero text and zero links — still the same kinds. The structure of the report is invariant; only the magnitudes differ.

This is what permits meaningful comparison: you are always comparing like with like (text-count to text-count, link-count to link-count).

## A caveat on scope

The comparison guaranteed here is a *structural/quantitative* one (how much text, how many links). Genuine **content** intercomparison — "what parts of two versions are the same" — is a different facility, handled by SHOWRELATIONOF2VERSIONS, which relies on shared Istream origin rather than uniform span-set structure:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

So: RETRIEVEDOCVSPANSET gives you uniformly-shaped reports (text + links) that are always comparable across documents; SHOWRELATIONOF2VERSIONS gives you semantic correspondence between two specific documents/versions.

If you meant a different "returned set" than RETRIEVEDOCVSPANSET, the most likely alternative is RETRIEVEDOCVSPAN, which returns only origin-and-extent of the V-stream (4/68) — also uniform in kind across documents, but reporting a single span rather than the text/link pair.
