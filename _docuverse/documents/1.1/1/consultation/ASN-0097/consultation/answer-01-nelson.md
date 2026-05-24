## Question 1 [nelson]

> When content that a link points to is edited — words inserted before or after the linked passage — must the link continue to address exactly the same content it originally addressed?

# Yes — absolutely and by design.

This is one of the most fundamental properties of Xanadu links. I designed them specifically so that editing operations — insertions, deletions, rearrangements — do not disturb existing links.

## The Mechanism: Links Attach to Bytes, Not Positions

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

A link is a strap binding bytes together. If you insert words before, after, or around the linked passage, the strap stays attached to the same bytes. The visual positions shift — of course they do — but the link doesn't care about visual positions. It cares about *which bytes*.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

## Why This Works: Two Address Spaces

The architecture has two separate address spaces:

- **Istream** (permanent): where content lives forever. Every byte gets a permanent I-address at creation. That address never changes.
- **Vstream** (ephemeral): the document's current arrangement. V-addresses shift with every edit.

Links point to **Istream addresses**. Editing changes **Vstream addresses**. The two are independent. When you insert a word before a linked passage, the V-addresses after the insertion point all shift — but the I-addresses of the linked bytes remain exactly as they were.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The user and front end work with V-addresses (intuitive positions). The link system works with I-addresses (permanent identity). This separation is the whole point.

## The Survivability Guarantee

I stated this explicitly as a system property:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

Note the boundary condition: links survive as long as *any* bytes remain at each end. You could delete most of a linked passage and the link would still hold onto whatever bytes remain. Only the complete deletion of all bytes at one end breaks the connection.

> "This also works for alternative versions in which part of each end has survived." [LM 4/42]

## Why This Matters

Without this property, Xanadu's entire vision collapses. If editing broke links, then:

- Every edit would damage the web of connections others had built to your content
- Published documents could never be revised without destroying scholarship built upon them
- The "ongoing braid" of document evolution would shred the literature's connective tissue

The whole point of the system is that **literature is interconnected** and those connections must survive the continuous editing that living documents require. Span-based, content-addressed linking is how I solved that.
