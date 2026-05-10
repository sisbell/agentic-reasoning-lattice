## Question 8 [nelson]

> When two previously non-adjacent segments become adjacent through rearrangement, does the system treat the boundary between them differently from content that was originally contiguous?

## Boundary Treatment After Rearrangement

**Short answer:** The system structurally distinguishes the boundary at the Istream level, but the user sees no difference at the Vstream level. This is not a special case — it's how *every* edit works.

### The Architecture Makes This Clear

Xanadu's two-address-space design means every document is a sequence of **spans** — contiguous runs of V-addresses that map to contiguous I-addresses. Whenever consecutive V-positions map to non-contiguous I-positions, there is a span boundary in the internal mapping (the POOM enfilade).

After REARRANGE transposes two regions, the V-addresses are re-densified — no gaps, contiguous from 1 to N. But the V→I mapping now has additional discontinuities at the new adjacency points. Where segments A and B have been placed next to each other, the last I-address of A and the first I-address of B are not consecutive.

### What the User Sees: No Difference

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**" [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream **just as if they were native** to the document." [LM 4/11]

The V-stream presents a seamless view. The user navigates across these boundaries without any indication that the content was rearranged. V-address 50 follows V-address 49 whether or not they share I-stream origin.

### What the System Knows: Structural Distinction

At the I-level, the boundary is real and detectable:

1. **Correspondence and version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. It can identify exactly where the rearrangement occurred by comparing the V→I mappings of the two versions. The span that was contiguous in version 1 is now split across two positions in version 2.

2. **Origin traceability.** Bytes on either side of the boundary still carry their original I-addresses, which encode their home document. The rearrangement doesn't change any I-address — it only changes the V→I mapping.

3. **Link behavior.** Links attach to I-addresses, not V-positions. A link spanning the pre-rearrangement boundary continues to reference the same bytes. A link that pointed to content on one side of the new boundary still works because:

   > "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

### This Is the Normal Case, Not a Special Case

Every editing operation creates or modifies span boundaries:

- **INSERT** adds new I-content at a point, creating two new span boundaries (before and after the insertion)
- **DELETE** may merge two formerly separated spans if content between them is removed
- **COPY** (transclusion) creates spans pointing to another document's I-space
- **REARRANGE** reorders existing spans

The POOM enfilade was specifically designed to handle this efficiently:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order." [LM 1/34]

### The Analogy

Think of the reading-list analogy from the Istream/Vstream model. Rearranging a reading list (moving chapter references around) changes what you see in what order, but doesn't alter the library shelves. The "boundary" between two books placed adjacent on your reading list is invisible to you as a reader — you just read one after the other — but the librarian knows they live on different shelves.

### Summary

| Level | Boundary visible? | Why |
|-------|-------------------|-----|
| **Vstream (user)** | No | V-addresses are dense and contiguous; content appears seamless |
| **POOM (mapping)** | Yes | Span boundary where V→I mapping is discontinuous |
| **Istream (storage)** | Yes | I-addresses remain at their original, non-adjacent positions |
| **Correspondence** | Yes | Version comparison reveals the rearrangement through span pairs |
| **Links** | No | Links follow I-addresses, unaffected by V rearrangement |

Nelson does not discuss this boundary explicitly — because in his architecture, there is nothing special about it. It is the *default* condition. A document that has undergone any editing at all is a patchwork of spans with boundaries between them. The entire design exists to make these boundaries invisible to users while preserving them for the system's structural guarantees.

NEED_RAW: [4/67, 4/30-4/31] — The REARRANGE operation description and the version/element addressing detail may contain additional specifics about how rearranged spans are represented internally. The curated sources cover the architectural answer well, but those pages might add implementation-level nuance.
