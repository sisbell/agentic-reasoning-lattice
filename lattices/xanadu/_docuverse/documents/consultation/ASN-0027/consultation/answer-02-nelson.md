## Question 2 [nelson]

> When a user edits a document by inserting or deleting content, must the addresses of all other existing content remain unchanged?

# Editing and Address Stability

The answer depends entirely on **which** address space you mean. Xanadu has two, and they behave oppositely.

## I-Space Addresses: Never Change

I-space (invariant space) addresses are permanent and immutable. Editing a document does not — and must not — alter them.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Every byte ever created has an eternal I-address encoding its origin (node, user, document, element). No editing operation touches I-space content. INSERT adds new bytes to I-space; DELETE removes bytes from the current V-space view but leaves I-space untouched.

The tumbler permanence guarantee applies here:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## V-Space Addresses: Explicitly Shift

V-space (virtual space) addresses are the document's current arrangement — positions in the "virtual byte stream" as the user sees it now. These **do** change on every edit. Nelson specifies this directly in the INSERT operation:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

And from the general description of V-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are always dense and contiguous (no gaps), so insertions push everything after the insertion point forward, and deletions close the gap.

## Why This Works

The separation is the architectural key. Links and transclusions point to **I-space** addresses, so they survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Users work with V-space positions (intuitive, sequential). The system resolves those to I-space addresses (permanent, immutable). Editing changes the V→I mapping — the document's arrangement — while the underlying content and all references to it remain stable.

## Summary

| Address Space | Changes on edit? | Why? |
|---|---|---|
| **I-space** | Never | Content identity is permanent; this is the guarantee that makes links, transclusion, and correspondence work |
| **V-space** | Always | The document's arrangement is what editing *means*; V-addresses shift to maintain a dense, contiguous byte stream |

The invariant is: **I-space addresses of existing content must never change.** V-space addresses are expected to change — that is editing.
