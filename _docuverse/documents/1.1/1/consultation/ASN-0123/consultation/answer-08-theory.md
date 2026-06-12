## Question 8 [theory]

> Must the new version be independently editable from the instant of its creation, such that no subsequent edit to either the version or the source can ever propagate to the other?

# On whether a new version must be permanently, bidirectionally isolated from its source

**Short answer: No.** Your question bundles together two things I deliberately kept separate. One half is a firm guarantee; the other half is a *choice* I designed into the system — and I built it so that source changes *can* propagate into a derivative when that is what you want. "Independently editable" and "permanently isolated" are not the same property, and conflating them misreads the design.

Let me take the two directions apart, because they are not symmetric.

## What *is* guaranteed: the version is independently editable, and can never damage the source

From the instant you fork it, the version is its own document with its own arrangement and its own identity. `CREATENEWVERSION` "creates a new document with the contents of document `<doc id>`... The new document's id will indicate its ancestry" [LM 4/66]. You may edit it immediately. And there is "no 'basic' version of a document set apart from other versions" [LM 2/19] — it is a full, free-standing alternative arrangement.

The version → source direction is locked down hard. This is the non-destruction guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." [LM 2/45]

Even deletion in the version cannot reach back into the source:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So nothing you do to the version ever propagates to the source. *That* half of your sentence is true and required.

## What is *not* required: that source edits can never reach the version

Here the premise fails. I did **not** mandate that later edits to the source are forever invisible to the version. On the contrary — making a derivative *track* its source is one of the things the inclusion mechanism exists to do:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update-- especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

That is propagation, by design. Whether you get it depends on *how the window is fixed*, and I gave you both options:

> "A quotation-- an inclusion window-- may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

- **Fixed in time** → a frozen snapshot. Source edits do not appear unless you go ask for them. This is the isolated behavior your question assumes.
- **Fixed in location** → a live window. "Updates are seen automatically." Source edits *do* propagate into the derivative.

A derivative is "permanently defined (and stored) in terms of the originals and the changes" [LM 2/37] — so what it shows of the unchanged portions is whatever the inclusion resolves to under the chosen mode. And the reader is never trapped either way: "The old viewpoint is still present too-- you can always say, 'Show me what this originally was.'" [LM 2/45]

## Why both behaviors are safe

I could offer the live option without endangering anyone because the *content itself* is immutable. A version and its source share the same underlying Istream bytes, and no one can rewrite those bytes. "Editing" is never mutation of existing content — it is rearrangement of a document's own virtual stream, or the appending of fresh, immutable content. So when a live window "sees an update," it is not that the source reached in and altered bytes the version already held; it is that the window is pinned to a *place* in an evolving document and faithfully shows what is now there. Nothing changes underneath you silently. You have simply asked to follow.

## Conclusion

To your precise question: the new version **must** be independently editable from the instant of creation, and edits to it **can never** propagate back to the source — that much is required. But the further claim — that no edit to the *source* can *ever* reach the version — is **not** a requirement of the design. Permanent, bidirectional isolation is *available* (fix the window in time), but a derivative that automatically follows its source's revisions is equally legitimate and was an explicit goal (fix the window in location). I separated independent editability from permanent isolation on purpose; an implementation that froze every version against all future source changes would be *one* correct configuration, not a mandate of the architecture.
