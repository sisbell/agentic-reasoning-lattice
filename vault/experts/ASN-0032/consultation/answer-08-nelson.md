## Question 8 [nelson]

> How do links relate to quotation and transclusion — is a transclusion a special kind of link, or are they fundamentally different operations?

## Links and Transclusion: Architecturally Distinct

This is a question that reveals a common confusion, and I want to be precise about the architecture because I was admittedly looser with terminology in Chapter 2 than in Chapter 4.

**Transclusion and links are fundamentally different operations.** They operate at different levels of the system and are implemented by different FEBE commands.

### Transclusion Is a V-Space Structural Operation

Transclusion is performed by the **COPY** command. It makes bytes from one document appear in another document's virtual byte stream:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The result is that non-native bytes become part of the document's V-stream:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

No link is created. The content simply appears in the document, fetched from its permanent I-space location. The system always knows the origin because:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### Links Are Separate Meta-Virtual Structures

A link is created by the **MAKELINK** command — a different FEBE operation entirely. Links are connective units with their own addresses, their own owners, and three endsets (from, to, type):

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

Links don't move or include content. They create navigable connections between content that exists independently.

### The Quote-Link Is Where the Confusion Arises

In Chapter 2, when describing the user experience, I used "quote-window" and "quote-link" somewhat interchangeably:

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link." [LM 2/32]

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

But in the technical specification, I drew the distinction explicitly:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated." [LM 4/53]

This is the critical sentence. A **quote-link** is a link that *marks* a transclusion — it is "the author's acknowledgment of material origin" [LM 4/53]. The **inclusion** (transclusion) is the structural fact; the quote-link is an optional annotation layered on top.

### How They Work Together

A compound document involves both mechanisms:

1. **COPY** operations that structurally include content from other documents in the V-stream (transclusion)
2. **MAKELINK** operations that optionally create quote-links marking those inclusions for the reader

An inclusion *without* a quote-link still works perfectly — the content appears, and the system can always trace its origin via I-addresses. But the reader may see no visual indication that the content came from elsewhere. The quote-link adds that visible signal.

Think of it through the glass pane metaphor:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else." [LM 2/34]

The clear glass — the window — is the transclusion (COPY). It is structural: content from below shows through. A quote-link would be a frame painted around that window, telling the reader "you are looking through to another document here."

### Why This Matters

The separation serves the principle that **attribution is structural, not metadata**:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee holds whether or not a quote-link exists, because the I-address of every byte encodes its origin. The quote-link is a courtesy to the reader; the I-space architecture is the guarantee to the system.

The separation also means transclusion can exist without cluttering the link space, and links can exist without requiring structural inclusion. You can link to a passage without quoting it. You can include a passage without explicitly marking it. The two mechanisms compose freely.

### Summary

| Mechanism | FEBE Command | What It Does | Creates a Link? |
|-----------|-------------|--------------|-----------------|
| **Transclusion** | COPY | Includes bytes in V-stream from another document's I-space | No |
| **Quote-Link** | MAKELINK | Marks an inclusion with visible attribution | Yes |
| **Ordinary Link** | MAKELINK | Connects spans without inclusion | Yes |

Transclusion is the plumbing. The quote-link is the label on the pipe. Both exist because literature needs both structural quotation and navigable connection — but they are not the same thing.
