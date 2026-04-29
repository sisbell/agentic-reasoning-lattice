# What Must the System Remember for Undelete?

The short answer is: **almost nothing extra**, because the architecture already preserves everything needed. That is the entire point of the I-space/V-space separation. But let me be precise about what "already preserved" means and what specific information restoration requires.

## 1. Content: Already Remembered (I-Space Is Append-Only)

DELETE does not touch I-space. The bytes remain at their permanent I-addresses forever.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The content is never lost. There is nothing to "remember" about it — it never left. The I-address of every deleted byte continues to resolve. This is not a design choice for undo support; it is the fundamental permanence guarantee (P0).

## 2. Position: The V-to-I Mapping Is What Must Be Recoverable

What DELETE actually destroys is the **V-space arrangement** — the mapping from virtual positions (where the user sees content) to I-space addresses (where content permanently lives). To undelete, you need to reconstruct:

**(a) Where in the V-stream the span was.** The V-address at which the deleted span began, and the V-address at which it ended. Without this, you know WHAT was deleted but not WHERE it appeared in the document.

**(b) The ordered sequence of I-addresses within that span.** A document's V-stream can interleave native content and transcluded content from multiple sources. The POOM (positional mapping) holds entries like "V-positions 47–92 map to I-addresses from document X; V-positions 93–105 map to I-addresses from document Y." Restoring the span means restoring this exact interleaving.

**(c) How following content shifted.** DELETE compresses V-addresses:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66, describing INSERT — DELETE is the inverse]

Undelete must reverse this shift, re-opening the gap and restoring the original positions.

## 3. Links: Nothing Extra Needed

This is where the architecture pays its deepest dividend. Links attach to I-space, not V-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

When you delete content from V-space, the links still exist and still point to those I-addresses. The link endsets are unchanged. What changes is whether the linked content is *visible* in the document's current V-stream. The moment the V-to-I mapping is restored, the links "reconnect" automatically — they were never disconnected at the I-level.

The system does not need to remember "which links were attached to this span." The links remember themselves, because they point to permanent addresses that the deletion never touched.

## 4. Shared References (Transclusions): Also Automatic

If document A transcludes content from document B, and B deletes that content from B's V-space:
- A's V-stream still includes the content (A has its own POOM entries mapping to the same I-addresses)
- B's content is gone from B's view but untouched in I-space
- The transclusion relationship is encoded in the I-addresses themselves — transcluded content shares I-addresses with its source

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

For undelete: the I-addresses in the restored POOM entries tell you whether each byte was native or transcluded. Restoring the V-to-I mapping automatically restores the transclusion structure, because the structure IS the mapping.

## 5. How the System Actually Remembers: Version History

Nelson's design makes this explicit. The version history IS the memory:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

Every state of every document is reconstructible. "Undelete" is not a special operation — it is a request for a previous version's arrangement. The journal (in the formal model: Σ includes journals) records every operation, and the POOM at any historical point can be reconstructed by replay.

## Summary: What Must Be Remembered

| Component | Remembered by | Special undo state needed? |
|-----------|--------------|---------------------------|
| **Content bytes** | I-space (append-only, permanent) | No — never deleted |
| **V-position** | Journal / version history | No — recorded as part of the DELETE operation |
| **V→I mapping** | Journal replay reconstructs POOM | No — derivable from history |
| **Link relationships** | Links themselves (point to I-space) | No — links are unchanged |
| **Transclusion structure** | I-addresses encode origin | No — implicit in the mapping |
| **Shift of following content** | Journal (DELETE records position and length) | No — invertible from the operation record |

The answer, then, is that the system must remember **the DELETE operation itself** — where it happened and how long the span was. Given that single record plus the permanent I-space content, everything else is derivable. The V-to-I mapping is reconstructed from history. The links and transclusions were never broken. The content was never destroyed.

This is what Nelson means when he says the storage system "automatically keeps track of the changes and the pieces." The architecture does not need a special undo mechanism because the entire design is, in a sense, one giant undo buffer. Deletion is just rearrangement of the view; the reality underneath is permanent.

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

You can always untwist the braid to any previous state, because every strand is preserved.