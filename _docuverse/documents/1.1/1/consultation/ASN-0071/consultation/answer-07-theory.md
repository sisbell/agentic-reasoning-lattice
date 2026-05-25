## Question 7 [theory]

> What must the system promise about the freshness of the result — is the answer guaranteed to reflect the moment of the query?

The system makes NO absolute freshness guarantee. This is a deliberate consequence of Xanadu's distributed architecture, and I was honest about it.

**What I promised was USER CHOICE about freshness, not automatic currency.**

For windowing (transclusion), I specified two modes:

> "A quotation--an inclusion window--may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

Freshness is a user choice between frozen and live references.

**For supersession**, the front end is expected to check explicitly:

> "A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52-4/53]

The check must be requested; staleness is the default unless you ask. Similarly for following old links to newer versions:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

Note: "may easily be set up to" — this is a front-end configuration, not a back-end guarantee.

**The distributed reality I acknowledged.** Each server holds a "continuously valid model or subrepresentation" of the docuverse [LM 4/72], but this is incrementally improved, not instantaneously current:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

And I was candid about the network:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

**What IS absolutely guaranteed about identity, not currency:**

Istream content at an I-address never changes. Reading the bytes at a permanent address always returns those exact bytes — that is the permanence guarantee [LM 4/19]. But "the current state of document D" or "all links into this passage right now" is a query against a distributed system that includes caching, replication, and possibly disconnected nodes.

**The deeper design principle**: I built the system around PERMANENCE of content (absolute) rather than CURRENCY of views (which no honest distributed system can absolutely guarantee). The user chooses: frozen citation (time-fixed, perfectly reproducible) or live view (location-fixed, latest-known, with eventual consistency).

What the system DOES promise about a query is best-effort: your local server will return what it knows, forward what it must, and the answer reflects the network's state as seen from your access point at that moment — not necessarily the latest state of the originating server.
