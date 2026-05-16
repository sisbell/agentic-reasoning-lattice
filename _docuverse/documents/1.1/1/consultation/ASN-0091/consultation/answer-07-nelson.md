## Question 7 [nelson]

> Does rearrangement change what content the document contains, or only the order in which that content appears — and is this distinction a fundamental design guarantee?

## Rearrangement Changes Order, Not Content — and This Is Architectural

**Yes**, rearrangement changes only the order in which content appears, never what content the document contains. **Yes**, this distinction is a fundamental design guarantee — it falls directly from the Istream/Vstream separation, which is the deepest architectural invariant in Xanadu.

### What REARRANGE Does

The REARRANGE operation transposes regions of text within a document:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

Transposition is pure reordering. Region A moves to where Region B was, and vice versa. No bytes are created, destroyed, or modified. The same Istream content is present in the document before and after — only the Vstream positions change.

### Why This Is Architecturally Guaranteed

The Istream/Vstream separation makes this inevitable, not merely conventional:

- **Istream** is where content permanently lives. Addresses are absolute and immutable. Content at an Istream address never changes.
- **Vstream** is the document's current arrangement — a mapping from visual positions to permanent Istream addresses.

A document IS this mapping. Nelson says:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

REARRANGE modifies the V→I mapping (which Istream bytes appear at which Vstream positions) but cannot touch Istream itself. The bytes are the same bytes, at the same permanent addresses, with the same identity. They just appear in a different sequence.

### REARRANGE Is More Conservative Than DELETE

This is worth noting. DELETE removes content from the Vstream — the bytes vanish from the current view (though they survive in Istream and remain accessible via historical backtrack). REARRANGE doesn't even do that. It keeps every byte visible in the current version; it only permutes their positions. Of all editing operations, rearrangement is the most purely structural.

### Link Survivability Confirms the Guarantee

The fact that links survive rearrangement is not a happy accident — it's a direct consequence of content-addressed linking:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

Links attach to Istream addresses (content identity), not Vstream positions (current arrangement). Rearrangement changes positions, not identity. Therefore links are completely unaffected.

### The Braid Metaphor

Nelson's metaphor captures this precisely:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

The strands of the braid (Istream content) are permanent. Rearrangement re-twists the weaving (Vstream arrangement) — the same strands, a different pattern. The braid changes shape; its fibers do not.

### Summary

| Property | Changed by REARRANGE? |
|----------|----------------------|
| Istream content (what bytes exist) | No — immutable |
| Istream addresses (where bytes live permanently) | No — permanent |
| Vstream arrangement (what order bytes appear) | **Yes** — this is all it does |
| Links to content | No — they attach to I-addresses |
| Version history | No — previous arrangement preserved |
| Document identity | No — same content, different view |

The distinction between content and arrangement is not a policy choice or implementation detail. It is the foundational invariant of Xanadu's architecture — the separation of identity (Istream) from view (Vstream). Rearrangement, by definition, operates entirely within Vstream. It cannot touch Istream because nothing can.
