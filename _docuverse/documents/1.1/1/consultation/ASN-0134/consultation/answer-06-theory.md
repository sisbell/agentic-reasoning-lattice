## Question 6 [theory]

> If two users add content to the very same document at the same instant, what must the design promise about whether their additions can be tangled together or must remain cleanly separated?

## The short answer

The design must promise **clean separation by identity — never silent tangling.** Two users' additions can be *arranged* next to each other, even interleaved character by character, but they can never be fused into one undifferentiated stream in which authorship is lost. Separation is structural and permanent; any combination is explicit, by reference, and origin-preserving.

But the premise needs correcting first.

## A document has exactly one owner — so "co-writing the same document" is not a primitive

There is no such thing in my design as two users *natively* writing the same document. A document has a single owner, and only that owner may change it:

> "Every document has an owner, the person who created and stored it… Only the owner has a right to withdraw a document or change it." [LM 2/29]

So when "two users add content to the same document at the same instant," at most one of them is the owner performing a native write. The other is not editing that document at all — in my design, the second writer **forks**. Writing always succeeds, but for the non-owner it succeeds as a *version*, not as a mutation of the shared original:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." [LM 2/45]

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/32–2/40]

The consequence is decisive: the two contributions land in two different home documents — the owner's, and the forker's new version — so they are *born separated*. They were never in danger of tangling, because they were never bytes of the same native stream.

## Why separation holds even when the content sits side by side

The separation is not a courtesy of the editor; it is built into the address space. Every byte has a permanent Istream identity encoding its home document and owner (`Node.0.User.0.Document.0.Element`, [LM 4/26]). Identity is by *creation*, not by appearance — two passages that happen to read alike but were authored independently hold *different* I-addresses; only genuinely shared (transcluded) content shares an address. Therefore no arrangement can lose track of who wrote what:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

That is the guarantee. Even if a front end lays two users' material out so they *look* braided, every character still answers truthfully to "whose are you, and where do you live?"

## Where "tangling" *is* permitted — and what it really is

I do allow contributions to be combined to any degree. Via `COPY`/windowing, a compound document can transclude content from many homes and interleave it arbitrarily — that is the whole point of collage and the glass-pane model. But this is combination *by reference*, not by fusion:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

Note carefully what the braid is *not*. It is one document's strands re-twisted through *its own* versions over time — added, subtracted, rearranged by its owner. It is never two owners' bytes melted into a single strand. Tangling, in my system, is always an arrangement of distinct, separately-owned, separately-addressed spans: **tangled in view, separate in identity.**

## Storage serializes; it does not blend

At the storage layer the contributions are *filed*, not blended. The store is append-only and chronological, so two arriving changes become two distinct entries at two distinct addresses:

> "…suppose we create an append-only storage system… filed, as it were, chronologically." [LM 2/14]

Even arriving "at the same instant," each addition is assimilated as its own fragment at its own permanent address. No operation in the model overwrites one with the other or coalesces them into a single indivisible unit.

## What I did *not* specify

I fixed the *semantics* — one owner; the second writer forks; identity is permanent and traceable. I did **not** specify the *concurrency mechanism* that resolves the literal same-instant race. There is no locking protocol, no `OPEN`/`CLOSE` session state, and no rule in *Literary Machines* for who "wins" the instant or exactly how the loser is redirected; the 17 FEBE commands carry no session state at all. That layer was left to the implementation — Roger Gregory's back end supplied it, a request-token/lock scheme in which a denied write becomes a branch ("denial-as-branching"). It is consistent with my intent, but it is not mine, and should not be quoted as design doctrine. (My only words on *simultaneity* concern shared *reading/search*, not concurrent authorship of one document.)

## Bottom line

- **Must remain cleanly separated: yes — by identity, always.** No two users' native contributions are merged into one undifferentiated stream; the authorship of every character stays permanently recoverable. [LM 2/40]
- **May be tangled in arrangement: yes — by reference, never by fusion.** Compound and version documents interleave distinctly-owned spans, and the seam is always there to be read. [LM 2/45, 2/32–2/40]
- **The same-instant race itself: unspecified by me.** Single ownership plus fork-on-write makes a true symmetric collision impossible *in principle*; the lock/serialization detail is the implementer's job, not the design's promise.
