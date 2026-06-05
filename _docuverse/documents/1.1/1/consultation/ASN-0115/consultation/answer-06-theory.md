## Question 6 [theory]

> When a single request gathers spans whose content originates in different documents, what must the design guarantee about presenting that material as one coherent delivery rather than disconnected fragments?

## The guarantee: seamless ordered assembly *without* severing origin

When a single request (e.g. `RETRIEVEV` over a spec-set) pulls spans whose native homes are scattered across the docuverse, Nelson's design imposes two simultaneous obligations that are in tension but must both hold.

**1. The fragments must occupy positions in one ordered virtual stream, as if native.**

Coherence is supplied by the Vstream. A document is defined by its arrangement, not by where the bytes physically live, and non-native bytes are slotted into that arrangement indistinguishably from native ones:

> "The virtual byte stream of a document may include bytes from any other document." (4/10)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

So the delivery is not "disconnected fragments" — each gathered span has a determinate ordinal place in a single logical sequence, and the user experiences one continuous document. Where it physically came from is deliberately hidden at this level:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

This is also why the request abstracts over physical location entirely — `FINDDOCSCONTAINING` finds material "regardless of where the native copies are located" (4/63), and FEBE hides "how content is physically stored" and "network distribution details."

**2. That seamlessness must never erase traceability to the home document.**

The coherence of the assembled view is not allowed to collapse the distinct origins into an anonymous blob. The opposite guarantee runs underneath: every character in the merged delivery remains attributable.

> "This world nevertheless remains simple in design. The virtuality is simple in structure and regular in layout. You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

Because the assembly is by reference (transclusion/windowing), not by copying, each piece is *fetched from* its home, which is precisely what keeps attribution structural rather than discardable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

## Why both at once

The design must guarantee that a multi-origin retrieval is delivered as a **single ordered stream the user reads as one document, while each constituent span simultaneously retains its permanent identity and resolvable home document.** Coherence comes from the Vstream ordering (fragments take ordinal positions "just as if they were native"); integrity comes from inclusion-by-reference (so you can always "ascertain the home document of any specific word or character"). Losing the first gives disconnected fragments; losing the second gives an unattributed copy — the "frozen and dead" detached copy Nelson warns against in the transclusion material. The contract is that one request yields one coherent delivery *and* a still-traceable set of origins.

One nuance not spelled out in the verified sources: the **mechanics of how the back end orders/merges spans from multiple servers into the single returned stream** (sequencing, gap handling, interleaving of returned text and links within `RETRIEVEV`). If you need that operational detail rather than the semantic guarantee, NEED_RAW: 4/61-4/67, 4/9.
