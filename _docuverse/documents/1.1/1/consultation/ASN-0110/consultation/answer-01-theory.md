## Question 1 [theory]

> When the system is asked which endsets touch a region of content, must it return the endsets themselves rather than the identities of the links that own them?

Yes. Nelson specifies two distinct operations that answer two distinct questions, and the endset-retrieval operation returns the endsets themselves.

**RETRIEVEENDSETS** is the operation that returns endsets for a region:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

This is contrasted with the link-discovery operation, which instead returns link *identities*:

**FINDLINKSFROMTOTHREE**:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

So the protocol cleanly separates the two concerns:

- Ask "what links touch here?" → **FINDLINKSFROMTOTHREE** → get link IDs (the links that own the endsets).
- Ask "what endsets are in this region?" → **RETRIEVEENDSETS** → get the endsets (from-sets and to-sets) themselves.

This separation is consistent with Nelson's link model, where a link is a structure with three endsets and its own home address. The endsets are the actual byte-spans attached to content; the link is the owning unit located at its home document. As the endsets concept describes it, `RETRIEVEENDSETS` "Returns the from-set and to-set of specified links" — i.e., it surfaces the span-sets, not merely a roster of link identifiers.

So to answer directly: when the system is specifically asked for the *endsets* in a region (via RETRIEVEENDSETS), it must return the endsets — the spans — not the link identities. The identities of owning links are what the separate FINDLINKSFROMTOTHREE family returns.

One caveat on framing: the phrase "which endsets touch a region" maps onto RETRIEVEENDSETS. The curated sources confirm RETRIEVEENDSETS returns endsets and FINDLINKSFROMTOTHREE returns link IDs, but they do not give Nelson's prose explaining *why* one would choose endsets over link IDs at the protocol level. If you want his reasoning on that design choice, NEED_RAW: 4/61-4/70.
