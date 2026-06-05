## Question 3 [theory]

> What relationship must the returned material bear to the arrangement that binds those spans to content — must delivery reflect the exact content each span currently designates, or content as it stood at some version?

## Short answer

The returned material must be exactly what the **named arrangement** designates — and in Xanadu the spec-set you hand to retrieval already *names* the version, so the apparent dichotomy ("current content" vs. "content as it stood at some version") largely collapses. Retrieval is defined as resolving the V→I mapping of the arrangement you addressed. The one place where a genuine "live vs. frozen" choice exists is **transclusion windows**, where Nelson gives two explicit binding modes.

Let me unpack this.

## 1. The arrangement *is* the document, and it is per-version

The thing that "binds spans to content" is the Vstream→Istream mapping. Nelson makes that mapping the very definition of a document, and each version carries its own mapping:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." (4/11)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So a V-address is *ephemeral within a version* — editing re-maps it. That is exactly why links bind to I-addresses (which survive) rather than V-addresses (which shift). V-positions follow the current arrangement of *their* version.

## 2. The version is encoded in the address, so "which version" is not ambiguous

A spec-set is interpreted against a particular document/version, because the version is part of the document tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (4/29)

> "In a sense the version, or subdocument number is only an accidental extension of the document number." (4/29)

And `RETRIEVEV` is specified purely in terms of that spec-set:

> RETRIEVEV: "This returns the material (text and links) determined by `<spec set>`." (4/67)

Because the spec-set names the version, **delivery must reflect the content that that version's arrangement binds to those spans** — not a globally "latest" arrangement. There is no privileged "current" document to default to:

> "There is thus no 'basic' version of a document set apart from other versions… any [arrangement] of the same materials is a priori better than other arrangements." (2/19)

This is what prismatic storage guarantees:

> "We believe our Prismatic storage can support virtually instantaneously retrieval of any portion of any version (historical or alternative)." (2/19)

So: ask for a span of version *V*, and you get the Istream content that *V*'s mapping designates — content "as it stood" in that arrangement, delivered live by resolving the mapping at request time.

## 3. Where the live-vs-frozen choice genuinely lives: transclusion windows

The phrase "the exact content each span *currently* designates" maps onto Nelson's one explicit user-facing choice — the two window modes for *included* (transcluded) spans:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." (2/37)

So for content a document *windows in* from elsewhere:
- **Location-fixed (floating in time)** → delivery reflects what the span *currently* designates; updates propagate automatically.
- **Time-fixed** → delivery reflects content *as it stood* at the bound moment; revisions appear only on explicit request.

This is the live/frozen distinction the question gestures at — but it is a property of how the *window* was created, not of the retrieval primitive itself.

## Synthesis

- **Native content of a named version:** delivery must reflect that version's arrangement exactly. Since the version is in the address, "current" and "as it stood" coincide — you get the binding you asked for.
- **Transcluded content:** delivery reflects either the current source content (location-fixed window) or the source content as of a fixed point (time-fixed window), per the window's binding mode.

In all cases the invariant is the same: **the returned material must be precisely what the addressed arrangement binds those spans to** — never an arrangement other than the one named. The system never silently substitutes a "latest" arrangement, because Xanadu has no canonical basic version to substitute (2/19).

One caveat worth flagging: the sources specify `RETRIEVEV` returns "the material determined by `<spec set>`" (4/67) but do not give a step-by-step statement of *when* the V→I resolution is evaluated for a still-editing version. The conclusion above ("resolved against the named version's mapping at request time") follows from the V-address ephemerality (4/30) and prismatic per-version retrieval (2/19) rather than from an explicit RETRIEVEV resolution-timing statement. If you want that timing nailed down verbatim, NEED_RAW: 4/63–4/67.
