## Question 1 [theory]

> Were inclusions / virtual copies intended to transclude content spans only, or was copying a link-subspace span ever an intended COPY input?

I don't have file-reading tools available in this session, so I'll answer from the verified curated sources and flag where the question exceeds them.

## Answer

The verified sources describe COPY and transclusion **exclusively in terms of content (byte/text) spans**, not link-subspace spans. But Nelson never gives an explicit statement either including *or* excluding link-subspace spans as a COPY input, so the strongest honest answer is "content spans were the clear intent; link-span copying is not specified."

### What the sources do say

**COPY is the transclusion operation, and it targets a virtual byte-stream address.** From the operations summary (4/67):

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." (4/67)

The destination is a **vsa** — a virtual byte-stream address. The Vstream is the byte arrangement of a document, and v-addressing is explicitly a byte-position concept:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

Placing copied material *at a vsa* presupposes the material occupies positions in the byte stream — i.e., content, not links.

**Links live in a separate subspace and are not rearrangeable.** Links occupy the `0.2` subspace, addressed by permanent order of arrival, not by byte position:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Because links keep their creation-order addresses permanently and are not repositioned in the Vstream the way bytes are, the notion of "copying a link to a vsa" does not map cleanly onto the operation as defined. This is the structural reason transclusion is framed around content.

**Transclusion docs consistently describe windowing of content.** Every description of inclusion/virtual copies is about seeing "a portion of the old" document's content:

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old. We may also call this an inclusion." (2/32)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

Note Nelson's own term: "non-native **byte-spans**... are called inclusions or virtual copies." Inclusions are defined over byte-spans.

### The one nuance that complicates a flat "no"

Retrieval over a spec-set is *not* restricted to bytes — RETRIEVEV returns both:

> "This returns the material (text and links) determined by `<spec set>`." (4/67)

So a `<spec set>` can reference material whose retrieval yields links as well as text (the links that apply to a retrieved content span). This shows spec-sets are not byte-only as an addressing construct. What it does **not** show is that you can name a *link-subspace span itself* as the thing being COPYed into another document at a vsa. The "text and links" RETRIEVEV returns are the links *attached to* a content span, consistent with link survivability (links travel with the bytes they strap), not links being relocated as standalone copied objects.

### Bottom line

- **Intended input to COPY/inclusion: content spans (byte-spans).** This is consistent across 2/32, 4/11, 4/30, and 4/67, and is reinforced by links being a non-rearrangeable, separately-addressed subspace.
- **Copying a link-subspace span as a standalone COPY input: never affirmatively specified.** The mechanics (destination = vsa; links fixed in arrival order) argue against it, but Nelson does not state the exclusion in the verified material.

NEED_RAW: 4/66–4/67 (full COPY / RETRIEVEV / spec-set definitions and any surrounding restriction on what a spec-set may designate as a COPY source), and 4/63 (which the operations doc cites for COPY/link-residence context) — these would confirm whether Nelson ever scopes the COPY `<spec set>` to exclude the link subspace, which the curated excerpts do not settle.
