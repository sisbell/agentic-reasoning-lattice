## Question 6 [theory]

> Must subsequent edits to the source document be reflected in the fork, or are the two versions independent from the moment of forking?

The answer requires distinguishing two things: **ownership independence** (always) and **content propagation** (your choice).

## Ownership: Always Independent

The moment you fork, the new version is a separate owned document. CREATENEWVERSION returns a new document ID — "The new document's id will indicate its ancestry" — but it is *your* document now. Only you can modify it. The source's owner cannot reach into your fork; you cannot reach into the source. This is absolute.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

## Content: Your Choice

A fork is built from inclusion links (windows) into the source. I designed two modes, and the forker chooses:

> "A quotation--an inclusion window--may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

So:

- **Time-fixed inclusion**: Your fork holds the source as it stood at the instant of forking. Subsequent edits to the source do *not* appear in your fork. You can later ask "what has this passage become?" — but that is an active query, not automatic.
- **Location-fixed inclusion**: Your fork windows the *living* source. Subsequent edits propagate automatically into the windowed portions. Your own additions and modifications remain yours.

## The Design Intent

I did not want to force a choice between "snapshot" and "living reference" — both are legitimate. A scholar citing a specific revision needs the frozen reference. A derivative work tracking ongoing corrections needs the live one. The same mechanism (inclusion links) serves both, and the forker decides at the moment of forking.

Either way, **correspondence is always preserved** through shared Istream origin. The system can always show you which parts of the fork correspond to which parts of the source, in any current or future state of either. That is non-negotiable, because intercomparison across versions is what makes versioning meaningful at all.

What you must never confuse: changes propagating into the *windowed* portions of a fork (when location-fixed) is *not* the source owner modifying your fork. The source owner modified their document; your fork happens to be looking through a live window at it. Your fork is still yours.
