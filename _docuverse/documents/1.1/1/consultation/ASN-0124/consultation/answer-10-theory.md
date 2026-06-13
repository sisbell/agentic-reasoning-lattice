## Question 10 [theory]

> Does containment rest on the permanent identity of the content itself rather than on resemblance — so that two documents holding coincidentally identical text are not reported as sharing, while documents holding the same identified material always are?

# Containment Rests on Identity, Not Resemblance

**Yes — emphatically.** In Xanadu, "sharing" or "containment" is defined by the *permanent identity* of content (its Istream / I-address origin), never by how the bytes happen to look. Two documents that independently typed the same words are not reported as sharing; two documents holding the same *identified* material always are. This is one of the architecture's load-bearing distinctions.

## The mechanism: identity lives in the I-address, not the bytes

Every byte has a permanent home. Nelson splits a document into **native bytes** (stored under its own control) and **non-native bytes** (inclusions fetched from elsewhere):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

The crucial word is *virtual* copies — an inclusion is not a byte-duplicate but a **reference to the same native bytes**. Identity is conferred at creation, not by value. As the curated `sporgl-provenance` concept summarizes the consequence:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'"

(That sentence is the curated synthesis of the architecture, not a verbatim Nelson quote — but it follows necessarily from the verified passages above: if identity is the home location, then independently authored bytes simply *have different homes*.)

## The operation that embodies it: FINDDOCSCONTAINING

The discovery operation searches by *identified material*, resolving the requested V-positions to their I-addresses and then finding every document whose arrangement maps onto those same addresses:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

Note "regardless of where the native copies are located" — the search follows the *identity* of the bytes to wherever they are included. It is not a text-matching scan. The curated `documents` and `i-space-v-space` concept maps make the basis explicit: FINDDOCSCONTAINING "Searches Istream origin, returns Vstream locations" and "Uses shared origin to find transclusions."

## The two halves of your question

**(a) Coincidentally identical text is *not* reported as sharing.** Because each independently authored run of bytes gets its own I-address, a vspec-set pointing at one document's "hello world" resolves to I-addresses that the other document simply does not contain. FINDDOCSCONTAINING finds nothing in common. The texts *resemble* each other, but resemblance is invisible to the containment machinery. (If a user *wants* to assert that such look-alikes are equivalent, they must do so by hand with a **counterpart link** — a "user-created assertion that two distinct things are equivalent," not anything the system infers automatically. That is the deliberate home Nelson gives to resemblance-without-identity.)

**(b) The same identified material is *always* reported as sharing.** Transclusion (the `COPY` operation) installs a Vstream reference to the source's *existing* I-addresses — "the copy shares I-addresses with the source" (curated annotation to 4/67). Editing, rearranging, or moving the including document never changes those I-addresses, so the shared identity is permanent and the two documents will always surface in each other's containment results. The same principle drives correspondence between versions: as the `correspondence` concept puts it, two positions correspond precisely "if [they] map to the same I-address," not if their text matches.

## Why Nelson designed it this way

This is the same structural property that guarantees attribution: because origin *is* the address rather than a strippable label, you "can at once ascertain the home document of any specific word or character" (2/40). A system that matched on resemblance would conflate coincidence with quotation, break attribution, and misroute royalties. By anchoring containment to permanent identity, Xanadu reports sharing if and only if material is *literally the same material*, wherever it has been included.

---

**One transparency note:** the verified Nelson quotes establish the native/non-native (identity-based) model and the FINDDOCSCONTAINING semantics. The explicit conclusion that *coincidentally identical text is excluded* is an architectural inference from those quotes (and is stated outright in the curated `sporgl-provenance` synthesis), not a sentence I can quote Nelson saying verbatim. If you want his ipsissima verba on the coincidence case specifically, the place to look would be the inclusion discussion at **4/10–4/11** and the FINDDOCSCONTAINING discussion at **4/63** and **4/70** — but the curated extracts of exactly those passages already entail the answer.
