## Question 5 [nelson]

> What happens to content already occupying the target position in the document — is it displaced, overwritten, or must the operation only target empty positions?

Let me check the original pages for the INSERT and COPY operation specifications to give you the most precise answer.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-233.txt</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-234.txt</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-233.png</file_path>
</parameters>
</tool_call>
<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>resources/literary-machines/raw/page-234.png</file_path>
</parameters>
</tool_call>

Content is **displaced (shifted forward), never overwritten**. There is no overwrite operation in Xanadu. This follows from both the explicit operation specifications and the deeper architectural principles.

---

## The Explicit Specification

**INSERT** is unambiguous:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The phrase "increased by the length of the inserted text" is the definition of displacement. Content at and after the target position shifts rightward to make room. Nothing is overwritten.

**COPY** follows the same pattern:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY places transcluded content at a V-address. Since V-addresses form a dense, gapless sequence (positions 1 through N), inserting material at position K necessarily shifts everything from K onward — exactly as INSERT does.

**APPEND** avoids the question entirely:

> "This appends \<text set\> onto the end of the text space of the document \<doc id\>." [LM 4/67]

It targets the position after the last byte. There is nothing to displace.

**REARRANGE** transposes regions — it swaps, not overwrites:

> "Rearrange transposes two regions of text." [LM 4/67]

---

## Why Overwrite Is Architecturally Impossible

Three layers of the design rule out overwrite:

**1. Istream is append-only.** Content in Istream never changes:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Overwriting would require destroying Istream content, which contradicts the append-only guarantee.

**2. Vstream is an arrangement, not a container.** The document's V-stream is a mapping from positions to I-addresses. "Editing" means changing the mapping:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

INSERT changes the mapping by shifting all subsequent V→I entries forward and inserting new entries at the target. DELETE changes the mapping by removing entries and closing the gap. Neither operation touches the underlying I-stream content.

**3. The non-destruction guarantee is absolute:**

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

An overwrite operation would "damage" whatever was at the target position — destroying the V-stream reference to that content. This violates the guarantee. The correct operation is always: INSERT (which preserves everything) plus optionally DELETE (which removes from V-stream only, preserving I-stream).

---

## The Operation Must Only Target Occupied or End Positions

V-stream addresses are always dense — there are no gaps:

> "The digit after the one indicates the byte position in the current ordering of bytes." [LM 4/30]

If a document has 100 bytes, valid V-addresses are 1 through 100 (for targeting existing content) plus position 101 (for appending). There are no "empty positions" to target. Every INSERT goes between or before existing content, shifting what follows.

---

## Summary

| Operation | What happens to existing content at target? |
|-----------|---------------------------------------------|
| **INSERT** | Displaced — V-addresses shift forward by insertion length |
| **COPY** | Displaced — same as INSERT (material inserted at target) |
| **APPEND** | N/A — targets position after last byte |
| **REARRANGE** | Transposed — regions swap positions |
| **DELETE** | N/A — removes from V-stream, gap closes |

There is no OVERWRITE, REPLACE, or PUT operation. If you want to "replace" content, you DELETE the old span and INSERT the new content — two operations, preserving the old content in Istream for historical backtrack.
