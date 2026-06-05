## Question 3 [theory]

> What relationship must each reported span bear to the body of content it measures — must it account for every character or link present, and nothing outside it?

## Exact coverage: complete and exclusive

A reported span must stand in a relationship of **exact coverage** to the content it measures: it must account for *every* character and link that belongs to that body of content, and *nothing* that lies outside it. These are two distinct requirements — completeness (account for everything present) and exclusivity (admit nothing foreign).

**The "exactly, including nothing else" principle.** Nelson states the requirement directly when discussing how to designate a precise body of content:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

This is why measurement uses a **span-set** rather than a single span when content is discontiguous. A single contiguous span carries no freedom in what it includes — its contents are fixed by its endpoints:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

So within a span there is no slack: the boundaries *determine* exactly what is covered. To cover content that is broken up (so as to exclude intervening foreign material), you assemble a span-set of multiple spans, each contiguous, together covering exactly the desired items and nothing else.

**Application to document measurement.** This is precisely the contract of the operation that reports a document's extent:

> **RETRIEVEDOCVSPANSET**: "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

Because a document's content lives in two subspaces — bytes (text) and links — a single span cannot exclusively cover both without also embracing addresses that are neither. A span-set lets the report account for *all* the text and *all* the links the document is home to, while excluding everything else. The companion operation gives the outer bound:

> **RETRIEVEDOCVSPAN**: "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)

**Why this matters structurally.** A span is not a count — it is a designation of "from here to there" over the tree:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

Therefore the relationship a reported span(-set) bears to its content is definitional, not approximate: the boundaries select a subtree, and a correct report is one whose selected subtree coincides with the body being measured — covering each character and each link present, and admitting nothing beyond it. The curated note on spans summarizes the design goal: "Any set of tumbler addresses can be covered exactly by a series of spans."

In short: **yes** — each reported span must account for every character or link present in the body it measures and for nothing outside it, achieving that exclusivity through a span-set whenever the content is not perfectly contiguous.
