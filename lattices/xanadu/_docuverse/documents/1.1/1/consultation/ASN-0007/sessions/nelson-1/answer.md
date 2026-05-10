Let me check the key pages where Nelson discusses this most directly.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-209.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-197.png</file_path>
</parameters>
</tool_call>

This is a precise question, and the answer is clear from the architecture: **endsets point to the content itself — to permanent I-space addresses — not to positions within any document's current arrangement (V-space).**

Here is the evidence, with citations.

## The Core Statement

Nelson describes links as attaching to bytes, not to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

And more explicitly on the addressing side:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The phrase "to the bytes themselves" is the key. Bytes have permanent I-space addresses. Positions in a document's current arrangement are V-space addresses that shift with every edit. Links attach to the former, not the latter.

## Why This Must Be I-Space

The survivability guarantee makes this architecturally necessary:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

If endsets pointed to V-space positions (e.g., "position 47 in document D"), then every INSERT before position 47 would invalidate the link. The guarantee that links "survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43] is only possible if endsets reference content identity (I-space), not content arrangement (V-space).

The mechanism:

- **V-space addresses** change with every edit — they are ephemeral positions in the current arrangement
- **I-space addresses** are permanent — a byte's I-address never changes after creation
- When you edit a document, V-space shifts but I-space is untouched
- Links reference I-space, so editing has no effect on them

As Nelson states about V-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space is "constantly changing." You cannot build survivable links on something that constantly changes.

## What This Means Across Documents

When a link connects spans in two different documents, each endset contains I-space addresses identifying specific bytes by their permanent identity — which encodes their home document, their owner, and their position in the append-only content store.

This means:

1. **The from-set** is a span-set of I-space addresses (possibly in multiple documents)
2. **The to-set** is a span-set of I-space addresses (possibly in multiple documents)
3. **The type (three-set)** is also a span-set of I-space addresses (or ghost addresses where nothing is stored)

Nelson confirms that endsets map to the universal tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

And each endset can span multiple documents:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

## The User-Facing vs. Storage-Level Distinction

There is a subtlety worth noting. At the **FEBE protocol level**, users work with V-space addresses — they INSERT at V-space position 5, they DELETE a V-span. But when they create a link (MAKELINK), the system translates the user's selection into permanent I-space addresses for storage. The user says "link from this visible passage to that visible passage"; the system records "link from these I-space bytes to those I-space bytes."

This is why Nelson can say users don't need to know about I-space:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The front end handles translation. The back end stores links in I-space terms. The user sees content; the link grabs the content's permanent identity.

## Summary

Each endset points to **content** — identified by permanent I-space addresses — not to positions within any document's current V-space arrangement. This is the architectural foundation for link survivability. The link is a "strap between bytes" [LM 4/42] that holds onto the bytes' permanent identities, regardless of how those bytes are currently arranged in any document's view.