# Consultation Answers — Permutation Model

**Inquiry:** What properties must a contiguous Vstream-to-Istream mapping block preserve? How do paired spans split, merge, and maintain width coupling across the permutation?
**Date:** 2026-03-20 14:14
**Questions:** 19 (9 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a document presents content in a different order than it was originally created, must each contiguous run of consecutively-created content be represented as a single indivisible mapping unit?

### Nelson's Answer

## No. Nelson does not require contiguous I-runs to be indivisible mapping units.

The V→I mapping is conceptually **byte-level**, and operations can freely split any contiguous run of consecutively-created content.

### What Nelson specifies

The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses are always dense and contiguous (1 through N). I-addresses are permanent and immutable. The mapping between them is what changes during editing.

### REARRANGE proves splits are permitted

The REARRANGE operation explicitly breaks contiguous I-runs:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

If bytes I:100–109 form a contiguous run appearing at V:50–59, and you REARRANGE with cuts at V:53 and V:57, the result is two non-adjacent groups of the original I-run (V:50–53 gets the second region, V:54–59 gets the first). The contiguous I-run has been split across non-contiguous V-positions. No constraint prevents this.

INSERT has the same effect — inserting new content in the middle of a contiguous I-run splits it into two V-regions separated by the inserted material:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

### Spans are the natural unit, not a mandated atom

Spans are how the FEBE protocol refers to content — they are the operational currency. SHOWRELATIONOF2VERSIONS returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. The COPY operation takes a "spec set" (set of spans) as input [LM 4/67].

But Nelson never states that the mapping representation MUST keep maximal I-contiguous runs as indivisible units. He specifies:

1. The **conceptual model** — bytes have I-addresses and V-addresses
2. The **operations** — INSERT, DELETE, REARRANGE, COPY freely alter V-order
3. The **enfilades** — data structures that "manage huge agglomerates of text and their arrangement" [LM 1/33]

The internal representation of the V→I mapping is left to the enfilade implementation. Nelson describes the POOM enfilade as mapping V→I addresses but does not detail its atom of representation in Literary Machines.

### Summary

A contiguous run of consecutively-created I-addresses is a **span** — the natural and efficient unit for referring to content. But it is not an **indivisible** mapping unit. The editing operations demonstrate that any such run can be split, reordered, or interleaved with other content. The mapping granularity is conceptually per-byte; spans are an optimization for how the system *refers to* and *stores* mappings, not a constraint on what mappings are expressible.

NEED_RAW: [4/10, 4/11] — the curated sources cover these pages well, but the original pages may contain diagrams showing the V→I mapping structure that could add precision to this answer.

---

## Question 2 [nelson]

> If a mapping unit pairs a region of a document with its original content, must both sides of that pairing always describe the same number of characters?

### Nelson's Answer

## Yes — both sides must always describe the same number of bytes.

This is a structural consequence of how Istream and Vstream relate. The Vstream is a byte-level view over Istream content. Each position in the virtual byte stream corresponds to exactly one byte in the identity stream. A mapping unit groups a contiguous run of these 1:1 correspondences into a single pair of spans for efficiency, but the width is always equal on both sides.

### Why this must be so

The Vstream is defined as a sequence of byte positions, each of which resolves to a specific Istream byte:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Every V-position maps to one I-position. A mapping unit that says "V-positions 1–5 correspond to I-positions 100–104" has width 5 on both sides. There is no mechanism for a single V-byte to expand into multiple I-bytes, or for a V-position to map to a zero-width I-region. The relationship is strictly bijective within each mapping unit.

### Confirmed by the editing operations

Every operation that creates or modifies mappings preserves this width equality:

- **INSERT**: Creates new Istream bytes and new Vstream positions. "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — Same length on both sides.

- **COPY** (transclusion): "The material determined by \<spec set\> is copied to the document." [LM 4/67] — Creates V-positions pointing to existing I-positions. The transcluded region has the same byte count on both sides.

- **DELETE**: Removes V-positions entirely. Istream content is unchanged. No asymmetric mapping is created — the mapping unit is simply removed from the Vstream arrangement.

- **REARRANGE**: Transposes V-regions. The mapping units are reordered but their internal width-equality is preserved.

### The deeper reason

The Vstream is not a transformation of Istream content — it is an *arrangement* of it. Nelson's analogy is clear: Istream is the library stacks (permanent shelf locations for books), Vstream is a reading list (references to those books in a chosen order). A reading list entry that says "books on shelves 100–104" always refers to exactly 5 books. You cannot have a reading list entry that refers to 3 shelves but somehow yields 7 books.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The V-address changes; the I-address does not. But each V-byte always resolves to exactly one I-byte, making equal-width spans the only valid mapping unit.

---

## Question 3 [nelson]

> When an editing action breaks a contiguous mapping unit into two pieces, what properties must each resulting piece independently preserve about its relationship to the original content?

### Nelson's Answer

## Properties Preserved When a Mapping Unit Splits

When an editing operation (INSERT, REARRANGE, DELETE of interior content) breaks a contiguous V→I mapping unit into two pieces, each resulting piece must independently preserve these properties:

### 1. I-address Mapping Fidelity

Each piece must continue to reference the **exact same I-addresses** as the corresponding portion of the original unit. Nothing changes in Istream; only the Vstream arrangement is altered.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

INSERT explicitly modifies only V-addresses: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]. The I-addresses are untouched.

### 2. Origin Traceability

Each piece independently encodes its content's home document in the I-address structure (`Node.0.User.0.Document.0.Element`). This is structural, not metadata — it cannot be severed by splitting.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Both pieces independently answer the question "where did this come from?" because each byte's I-address carries the answer.

### 3. Link Attachment

Links attached to bytes in the original unit remain attached to those same bytes regardless of which piece they end up in. Nelson is explicit that links bind to **bytes**, not to mapping units or positions:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Each piece independently serves as a valid link anchor. A link whose endset spans the split point now has its bytes distributed across two pieces, but the link survives because content at each end still exists.

### 4. Correspondence

Each piece independently establishes correspondence with any other V-position (in other versions or documents) that shares the same I-addresses. Version comparison works piece-by-piece because correspondence is a relation derived from shared Istream origin, not from the contiguity of the mapping.

> "a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. After a split, the correspondence computation produces two pairs where it previously produced one — but the relationship to the original content is fully preserved.

### 5. Transclusion Identity

If the original mapping unit was an inclusion (virtual copy), each piece independently remains a valid reference to its portion of the source content.

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Each piece independently maintains the property of being "native elsewhere" — the transclusion relationship is per-byte, not per-mapping-unit.

### 6. Canonical Structural Validity

After the split, the document must remain in valid internal form. Nelson describes this as "canonical order" — the mandate that all changes leave the structure valid:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

Each piece is a self-contained mapping unit that the enfilade can manage independently. The split produces two units that together cover exactly the same I-addresses as the original, with no gaps and no overlaps.

---

### Summary

The core principle is that **splitting is a Vstream operation that must be invisible to Istream properties**. Each piece inherits every property that derives from I-address identity: traceability, link attachment, correspondence, transclusion identity. The split changes how content is *arranged* (Vstream) without affecting what content *is* (Istream). This is the direct consequence of Nelson's separation of content from arrangement — the design choice that makes editing non-destructive.

---

## Question 4 [nelson]

> Under what conditions may two adjacent mapping units in a document be recognized as a single larger unit, and what must be true about their original content positions for this to be valid?

### Nelson's Answer

The curated sources discuss spans and the V→I mapping extensively but don't explicitly address the coalescing conditions for adjacent mapping units. Let me check the raw pages in the spans section (4/32–4/39) where Nelson discusses span manipulation in detail.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-199.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-200.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-201.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-202.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-203.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-204.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-205.txt"}}
</tool_call>
<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-206.txt"}}
</tool_call>

<tool_result>
<file_path>resources/literary-machines/raw/page-199.txt</file_path>
<content>LITERARY MACHINES	4/32


4.4	Spans


We will discuss here the basic tumbler operations.

A tumbler-span is a range of tumblers. A tumbler-span is
represented either by an address tumbler and a difference tumbler
(together designating a span's offset and width), or by two address
tumblers (together designating a span's beginning and end). The
following operations enable conversion between these forms.


a) ADD

Add takes an address tumbler and a difference tumbler and
produces a second address tumbler that designates the other end of a
span from the given address tumbler in the given difference
direction.

b) SUBTRACT

Subtract takes two address tumblers and produces a difference
tumbler designating the direction and width of the span between
them.
</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-200.txt</file_path>
<content>LITERARY MACHINES	4/33


c) COMPARE

Compare takes two address tumblers and determines whether they are
the same, or if not, which is first on the tumbler line.


d) NEXT

Next takes an address tumbler, and produces the next larger address
on the tumbler line. For example, the next of 2 is 2.1, and the
next of 1.3 is 1.3.1. (The next is always calculated by appending
a one digit.)


e) SPLIT

Split takes a span represented by address tumbler and a difference
tumbler (the offset and width of the span), and splits the span at
a given position, producing two address-difference pairs (each pair
representing one of the resulting spans).


f) MERGE

Merge takes two spans represented as address-difference pairs,
and if the two spans are adjacent, produces a single span that
covers the full range of the two original spans.

</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-201.txt</file_path>
<content>LITERARY MACHINES	4/34


g) WITHIN

Within takes a span (represented by address-difference pair), and
an address tumbler, and determines whether or not the address tumbler
lies within the span.

h) CONTAINS

Contains takes a span (represented by address-difference pair),
and another span (represented by address-difference pair), and
determines whether or not the second span lies completely
within the first span.

i) OVERLAPS

Overlaps takes two spans (both represented by address-difference
pairs), and determines whether or not they overlap each other.

</content>
</tool_call>
<tool_result>
<file_path>resources/literary-machines/raw/page-202.txt</file_path>
<content>LITERARY MACHINES	4/35


4.4.1 Request-Sets and Spec-Sets

A request-set is a set of spans, or spanset, presented to the
back end in the FEBE protocol. A request set specifies all the
material the user wants to receive, or other spans used in search.
The manipulation of request-sets is an important aspect of what front-
end functions do; and much of the work of front-end design is
determining and manipulating request-sets.

NB a request set may be used to specify a non-existent but
addressable subtree; i.e., the content bytes of an account, or of a
node. (See treatment of ghost elements and 1-positions.)

A spec-set is a subset of a request-set: a set of spans that
cover only one of the sub-spaces: for instance, all bytes or all
links. The subset of a request-set covering only character bytes
is called a "vspec-set"; that covering only links is called an
"lspec-set."



</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-203.txt</file_path>
<content>LITERARY MACHINES	4/36


The Ispan

An I-span (identity span) describes a contiguous set of elements in
the document's v-stream which have contiguous identity (I-stream) addresses.
A document may be described completely by a sequence of I-spans
covering its entire v-stream.

I-spans have two-tumbler starting positions: a V-stream starting
position and an I-stream starting position. Their width is
defined by a single difference tumbler (the same in both spaces),
since the V-stream and the I-stream widths must be identical.

Each I-span contains elements which are contiguous in V-space as
well as I-space.

Two adjacent I-spans in a document may be combined if
they describe V-contiguous elements which are also I-contiguous.
One way to think of this is the following: two adjacent I-spans
describe elements in the same document.

They can be merged if one end of the next I-span can also be
described as one past one end of the first.

</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-204.txt</file_path>
<content>LITERARY MACHINES	4/37


A mapping of a single document's v-stream consists entirely of
I-spans. And there may be many representations of a given
v-stream. The representation with the fewest I-spans is the
most compact.

Understanding spans is a key to appropriate software design
for handling request-sets.

There is a direct resemblance between representations of
a single document's v-stream (as I-spans), request-sets, and
spec-sets. Representations of a document's v-stream are
similar to request-sets and spec-sets in that they
cover particular territory, and may be combined by the merge
operation when neighboring I-spans or spec-set spans are adjacent.

</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-205.txt</file_path>
<content>LITERARY MACHINES	4/38


The 1-Positions

The last digit of a tumbler, when it is one, is the starting
position for a given set of elements of one type. These may be
thought of as the (virtual) "1-positions" on a document's tumbler
address.

A digit of "one" may be used to designate all of a given
version, all versions of a given document, all works of a given
author, all documents in a given project, all documents on a given
server--or the entire docuverse.


The diagram on the facing page shows these 1-positions in a
typical tumbler, and their significance. This will allow
understanding request-sets more readily.


</content>
</tool_result>
<tool_result>
<file_path>resources/literary-machines/raw/page-206.txt</file_path>
<content>LITERARY MACHINES	4/39

	REQUEST-SETS AND 1-POSITIONS

1			Starts docuverse set
  0

    1		Starts node set
      0

        1	Starts account set
	  0

	    1	Starts document set
	 	  (including all versions within it)

			THE FOLLOWING OCCURS ONCE PER VERSION:
		(though in this list there is only one)

	    	  1.	Beginning of version 1

	    	    0	Sub-space divider

	    	      1	Start of contents
		            (beginning of all elements)

		    	    NOTE: THIS SPANS ALL ELEMENT TYPES.
			    The byte sub-space is at
                                version . 0.1.position

			    The link sub-space is at
                                version . 0.2.position


	    	      2	Start of second element-type
			    (i.e., links)

	    	        1    First link of document
</content>
</tool_result>

This is exactly what I needed. Page 4/36 (raw page 203) directly answers the question. Let me also check the page image to confirm the OCR is accurate.

<tool_call>
{"name": "Read", "arguments": {"file_path": "resources/literary-machines/raw/page-203.png"}}
</tool_call>

<tool_result>
<image>resources/literary-machines/raw/page-203.png</image>
</tool_result>

The OCR is accurate. Here is the answer:

---

## Merging Adjacent Mapping Units: The I-Span Rule

Nelson answers this directly on page 4/36, in his discussion of the **I-span** — the fundamental mapping unit of a document's Vstream-to-Istream structure.

### What an I-Span Is

> "An I-span (identity span) describes a contiguous set of elements in the document's v-stream which have contiguous identity (I-stream) addresses. A document may be described completely by a sequence of I-spans covering its entire v-stream." [LM 4/36]

Each I-span has **two starting positions** (one in V-space, one in I-space) and a **single width** shared between them:

> "I-spans have two-tumbler starting positions: a V-stream starting position and an I-stream starting position. Their width is defined by a single difference tumbler (the same in both spaces), since the V-stream and the I-stream widths must be identical." [LM 4/36]

### The Merging Condition

Two adjacent I-spans may be merged into one **if and only if** the elements they describe are contiguous in **both** address spaces:

> "Two adjacent I-spans in a document may be combined if they describe V-contiguous elements which are also I-contiguous." [LM 4/36]

Nelson restates this more concretely:

> "They can be merged if one end of the next I-span can also be described as one past one end of the first." [LM 4/36]

### What This Means

For two adjacent mapping units to merge:

1. **V-contiguity** (adjacency in the document's virtual stream) — the second I-span must start exactly where the first one ends in V-space. This is given by "adjacent" — they are next to each other in the document's arrangement.

2. **I-contiguity** (adjacency in permanent content space) — the original content positions must also be contiguous. The I-address at the start of the second span must be exactly "one past" the I-address at the end of the first span.

If the two spans are V-adjacent but their I-addresses are *not* contiguous (e.g., they come from different documents, or from non-adjacent regions of the same document's Istream), they **cannot** be merged and must remain separate mapping units.

### Why This Matters

Nelson notes on page 4/37 that there can be many valid representations of the same Vstream, and the most compact one uses the fewest I-spans:

> "A mapping of a single document's v-stream consists entirely of I-spans. And there may be many representations of a given v-stream. The representation with the fewest I-spans is the most compact." [LM 4/37]

> "Understanding spans is a key to appropriate software design for handling request-sets." [LM 4/37]

The MERGE operation (defined on page 4/33) is the general span operation that implements this:

> "Merge takes two spans represented as address-difference pairs, and if the two spans are adjacent, produces a single span that covers the full range of the two original spans." [LM 4/33]

### Summary

Two adjacent mapping units (I-spans) in a document may be recognized as a single larger unit when their original content positions (I-stream addresses) are contiguous — that is, when the next I-span's starting I-address is exactly one past the end of the preceding I-span's I-address. The shared-width property (V-width equals I-width) guarantees that if V-contiguity and I-contiguity both hold, the merged span is a valid I-span with a single, larger width covering the combined range in both spaces.

---

## Question 5 [nelson]

> Must every character position in a document map to exactly one position in the permanent content record, or can a document position exist without such a mapping?

### Nelson's Answer

## Every Vstream Position Maps to Exactly One Istream Position

**Yes, the mapping is total and functional.** Every character position in a document's Vstream must resolve to exactly one Istream address. A Vstream position without such a mapping is architecturally impossible—it would be a reference to nothing.

### The Document IS the Mapping

The Vstream is not an independent data structure that *happens* to reference Istream content. The document's identity at any moment IS the V→I mapping. Nelson describes the retrieval chain:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

Every byte in the virtual stream has an origin—either native (created in this document) or non-native (transcluded):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

There is no third category. Every Vstream byte is either native or included—both cases resolve to a definite Istream address.

### The Enfilade Architecture Confirms This

The POOM enfilade (V→I mapping) sits between the user's request and the content store:

```
V-address → POOM → I-address → GRAN → actual bytes
```

There is no "null" case in this chain. A V-address that the POOM cannot resolve to an I-address would be a corrupted document, not a valid state.

### Operations Never Create Unmapped Positions

Every operation that adds positions to the Vstream simultaneously establishes an I-mapping:

- **INSERT** creates new Istream content AND maps new V-positions to it [LM 4/66]
- **COPY** (transclusion) maps new V-positions to *existing* Istream content [LM 4/67]
- **APPEND** adds to Istream at document end [LM 4/67]

And every operation that removes mappings closes the gap:

- **DELETE** removes V-positions entirely; "The v-stream addresses of any following characters in the document are increased [decreased]" — the Vstream contracts, leaving no holes [LM 4/66]
- **REARRANGE** transposes regions — same mappings, different V-order [LM 4/67]

No operation creates a V-position without a corresponding I-address.

### The Converse Does Not Hold

While every V-position maps to exactly one I-position, the converse is many-to-one:

- **Multiple V-positions can map to the same I-position** — this is transclusion. When document B includes content from document A, B's V-positions map to A's I-addresses.
- **I-positions can exist with no current V-mapping** — deleted content remains in Istream but has no Vstream position in the current version. Nelson explicitly describes this state: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

### Ghost Elements Are Not Unmapped Positions

The one concept that might seem to suggest unmapped positions—ghost elements—applies to the *address hierarchy* (servers, accounts, documents), not to byte positions within a document:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

Ghost elements are organizational nodes in the tumbler tree. They say "document 1.2.3 is a valid address even if empty." They do not say "position 5 in document 1.2.3 can exist without content."

### Summary

The V→I mapping is **total** (every V-position has a mapping) and **functional** (each V-position maps to exactly one I-position). A document position without an Istream mapping cannot exist—there is no operation to create one, no state to represent one, and no semantic meaning for one.

---

## Question 6 [nelson]

> Can the same region of permanent content appear in more than one mapping unit within the same document, and if so, must each mapping be independently tracked?

### Nelson's Answer

## Yes — the same Istream content can appear at multiple Vstream positions within a single document, and each mapping must be independently tracked.

### The architecture permits it

The Vstream is a sequence of references to Istream addresses. Nothing in Nelson's specification restricts a given I-address range from appearing at more than one V-position. The COPY operation makes this explicit:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The spec-set is unconstrained — it can reference any content in the docuverse, including content already present in the target document. A user could COPY the same source span to V-position 10 and again to V-position 50, producing two independent V→I mappings for the same I-content.

Nelson's description of virtual byte streams confirms this generality:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Each inclusion gets its own ordinal position in the byte stream regardless of origin — including the case where origin is shared.

### The windowing model makes it natural

Consider a literary essay that quotes the same passage at its opening and its conclusion. Each quote is a separate window to the same source:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

Each window is an independent mapping. The glass-pane metaphor illustrates this: two transparent openings in the same sheet can both look through to the same underlying content.

### Each mapping must be independently tracked

Three properties of the architecture require independent tracking:

**1. V-addresses are dense and contiguous.** If the document has 100 bytes, V-addresses run 1–100 with no gaps. If I-addresses 500–509 appear at both V-positions 10–19 and V-positions 60–69, the positional mapping (POOM enfilade) must maintain both entries to preserve the contiguous V-address sequence.

**2. Editing operations are V-addressed.** DELETEVSPAN removes a V-span; INSERT shifts V-addresses after the insertion point:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

Deleting V-positions 10–19 must close that gap and shift subsequent V-addresses without disturbing V-positions 60–69 (now 50–59 after renumbering). This requires independent tracking of each V→I mapping.

**3. Links attach to content, not positions — but through V-addresses.** A link's endset specifies spans. If a user creates a link whose from-set covers V-positions 10–19 and another link covering V-positions 60–69, these are distinct links to distinct V-positions, even though both resolve to the same I-content. The link survivability guarantee applies independently to each:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

Deleting one occurrence leaves the other intact, and any links attached to the surviving occurrence remain valid.

### Correspondence recognizes the relationship

The correspondence mechanism detects when V-positions share Istream origin, whether across versions or within a single document:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. The same mechanism would identify that two V-regions within a single document share I-origin — useful for front-ends that want to highlight repeated content.

### Summary

The Vstream is a mapping, not a bijection. The same I-content can be mapped to multiple V-positions. Each mapping is a separate entry in the positional structure, independently subject to editing operations, independently targetable by links, and identifiable as corresponding through shared Istream origin.

---

## Question 7 [nelson]

> Within a single contiguous mapping unit, must the document order of characters match the original creation order, or can a mapping unit represent a reversal or other reordering?

### Nelson's Answer

## Within a Mapping Unit, Document Order Must Match Creation Order

A single contiguous mapping unit (span) **cannot represent a reversal or reordering**. Order-preservation is inherent in the span model.

### Why: Spans Are Defined by Endpoints on the Tumbler Line

A span is "represented by two tumblers" and "refers to a subtree of the entire docuverse" [LM 4/24]. The content within a span follows tumbler-line ordering by definition — there is no direction flag, no reversal marker, no internal permutation. A span says "from here to there," and the ordering between those endpoints is fixed by the tumbler line itself.

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

"No choice as to what lies between" is the critical constraint. The internal ordering of a span is determined by the tumbler line, not by the mapping. A V-span mapped to an I-span inherits the I-span's tumbler ordering.

### The V→I Mapping Preserves Order Within Each Unit

The Vstream is a dense sequence of positions. The POOM enfilade maps V-positions to I-positions. Each mapping entry covers a contiguous run where V-position *k* maps to I-position *k* (offset by the span's starting addresses). This is why spans are efficient: you store only start-V, start-I, and length.

Nelson's description of V-stream addressing confirms this structure:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

The V-order *across* mapping units can differ from I-order — that is the entire point of the V/I separation. But *within* a single unit, the correspondence is positional (first-to-first, second-to-second, etc.).

### No Operation Creates Reversed Mappings

None of Nelson's 17 FEBE commands produces a reversed span:

- **REARRANGE** "transposes two regions of text" [LM 4/67] — it swaps blocks but preserves internal order within each block.
- **INSERT** adds new content at a V-position — new I-bytes are appended chronologically.
- **COPY** (transclusion) maps a V-range to an existing I-range — same order.
- **DELETE** removes a V-range — no reordering involved.

There is no REVERSE operation. To achieve the effect of reversing "ABC" to "CBA," you would either:
1. **INSERT** new native bytes "CBA" (creating fresh I-stream content in the desired order), or
2. Create **three separate mapping units**, one per character, arranged in reverse V-order — each unit is order-preserving, but they appear in reversed sequence in the V-stream.

### Summary

The span is the atomic mapping unit. It maps a contiguous V-range to a contiguous I-range with identical internal ordering. Reordering is expressed by the *sequence of spans*, not by reversal within any single span. This is structural, not merely conventional — it follows from the definition of a span as a pair of tumbler-line endpoints with "no choice as to what lies between."

NEED_RAW: 4/32-4/39 — The detailed span mechanics pages may contain additional precision about the V→I mapping representation that the curated sources summarize but don't fully reproduce.

---

## Question 8 [nelson]

> If a document contains content from multiple original creation events, must the boundaries between mapping units align exactly with the boundaries between those distinct creation events?

### Nelson's Answer

## No — Nelson does not require mapping unit boundaries to align with creation event boundaries

The V→I mapping is defined by the **current arrangement** of content, not by how or when content entered Istream. Nelson's design is explicit on this point.

### The key statement

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, **regardless of their native origin.**"
> — [LM 4/11]

Vspans are defined by position in the virtual stream. The system does not require — or even expose to the front end — where creation event boundaries fall within those spans.

### What determines mapping boundaries

The V→I mapping tracks which I-address each V-position resolves to. In any span-based representation, a new mapping entry is needed whenever the I-address sequence becomes **discontinuous** in V-order. This discontinuity arises from the *arrangement*, not from creation history per se.

Consider: if two consecutive INSERTs to the same document produce I-addresses D.0.1.5 through D.0.1.10 and D.0.1.11 through D.0.1.15, and both runs remain adjacent in V-space, the I-addresses form a single contiguous range (D.0.1.5 through D.0.1.15). Nothing in Nelson's design requires a mapping boundary between them, even though they came from distinct creation events.

Conversely, a single REARRANGE operation can split one creation event's bytes across non-adjacent V-positions, forcing multiple mapping entries for content from one event:

> "Rearrange transposes two regions of text."
> — [LM 4/67]

### The front end doesn't see I-addresses at all

Nelson explicitly shields the user layer from I-space details:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this."
> — [LM 4/11]

The front end works entirely in V-addresses. Whether a contiguous V-range maps to one or many I-ranges — and whether those I-ranges came from one or many creation events — is invisible at the protocol level.

### What the system *does* track

The system tracks **I-address identity**, not creation event history. This is what enables correspondence:

> "A facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same."
> — [LM 2/20]

Correspondence works by comparing I-addresses across versions. Two V-positions correspond if they map to the same I-address. The system doesn't need to know *when* those I-addresses were created — only *that they are the same*.

### Why the distinction matters

In practice, distinct creation events almost always produce non-contiguous I-addresses (because the append-only store interleaves content from all documents chronologically: [LM 2/14]). So mapping boundaries and creation event boundaries usually coincide. But this is a **practical consequence** of the append-only storage model, not a **design requirement** of the V→I mapping.

The two cases where they diverge:

1. **Consecutive appends to the same document** with no intervening operations — I-addresses are contiguous, so a single mapping unit suffices despite multiple creation events
2. **REARRANGE splitting a creation event** — one event's bytes end up in non-adjacent V-positions, requiring multiple mapping units for a single event

### Summary

Nelson defines the V→I mapping in terms of I-address identity and V-position, not creation event provenance. Mapping unit boundaries are determined by I-address contiguity in V-order. Creation events determine *which I-addresses exist*; the arrangement determines *how they map*. These are independent concerns in Nelson's architecture.

---

## Question 9 [nelson]

> When content is shared across documents, must each document's mapping to that content be independent, so that rearranging content in one document cannot alter the mapping in another?

### Nelson's Answer

## Yes — Absolutely and by Design

Each document's Vstream mapping to shared Istream content is independent. Rearranging content in one document cannot alter any other document's mapping. This is not merely a desirable property but a structural consequence of the Istream/Vstream separation.

### The Architecture Guarantees It

A document IS its V→I mapping. Each document maintains its own independent arrangement of references to permanent Istream content:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Each document's Vstream is a separate reading list pointing into the same shared library. Two documents can reference identical Istream bytes while arranging them in completely different orders — and neither arrangement constrains the other.

### Nelson States This Explicitly

The clearest statement comes in the context of deletion:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

If even deletion — the most destructive Vstream operation — cannot affect other documents' mappings, then rearrangement certainly cannot.

### Editing Operations Are Document-Scoped

Every editing operation in FEBE takes a specific `<doc id>` and operates only on that document's Vstream:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters **in the document** are increased by the length of the inserted text." [LM 4/66]

> "This removes the given span from **the given document**." [LM 4/66]

The V-address shifts caused by insertion or deletion propagate within the affected document only. Other documents referencing the same Istream content are untouched.

### Why This Must Be So

Three of Nelson's fundamental guarantees depend on mapping independence:

1. **Ownership** — "Only the owner has a right to withdraw a document or change it." [LM 2/29] If Alice's edits could alter Bob's document's mapping, Alice would be changing Bob's document without ownership.

2. **Non-destruction** — "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45] If mappings were coupled, modifications *would* damage originals.

3. **Version integrity** — "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." [LM 2/37]

### The Mechanism

The Istream/Vstream separation makes this natural rather than enforced:

- **Istream is immutable** — content at an I-address never changes
- **Vstream is per-document** — each document holds its own V→I mapping
- **Transclusion creates a new mapping entry**, not a shared pointer into another document's Vstream

When Document B transcludes content from Document A, Document B gets its own Vstream entries pointing to the same Istream addresses that Document A points to. The two Vstream mappings share a destination (the I-addresses) but are structurally independent paths to that destination. Editing either document's Vstream is a local operation on that document's mapping alone.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are ephemeral and local. I-addresses are permanent and global. The independence of mappings follows directly from this separation.

---

## Question 10 [gregory]

> In a POOM bottom crum, must V-width and I-width always represent the same logical span length, or can they diverge — and if they must match, what mechanism enforces this coupling when `tumblerlength` computes V-width from V-address exponent while I-width is copied directly from I-space?

### Gregory's Answer

## KB Synthesis

## V-width and I-width in POOM Bottom Crums

**They must always encode the same logical span length (byte count), and the coupling is enforced structurally at crum creation — not by a runtime check.**

---

### The invariant

[INV-WIDTH-VALUE-EQUIVALENCE] states it formally:

```
forall crum c :: tumblerintdiff(c.width.dsas[V], zero) == tumblerintdiff(c.width.dsas[I], zero)
```

The two tumbler representations differ in exponent and digit count, but `tumblerintdiff` applied to either returns the same integer. [SS-POOM-BOTTOM-CRUM] makes the asymmetry concrete: for an 11-character insert, I-width is `0.0.0.0.0.0.0.0.11` (9 digits) while V-width is `0.11` (2 digits) — structurally unequal as tumblers, numerically identical as span lengths.

---

### The enforcement mechanism

The coupling is enforced by the construction path in `insertpm`, documented in [SS-INSERT-VWIDTH-ENCODING]:

1. **Extract the byte count from I-width**: `inc = tumblerintdiff(&lwidth, &zero)` — this converts the I-space tumbler to an integer, discarding its representation details.
2. **Re-encode at V-space precision**: `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` where `shift = tumblerlength(vsaptr) - 1` — this builds a fresh V-width tumbler encoding `inc` at the exponent implied by the V-address's digit length.
3. **Copy I-width directly**: `movetumbler(&lwidth, &crumwidth.dsas[I])` — no transformation.

The integer `inc` is the bridge. Both representations are derived from it, so they cannot diverge at creation time.

---

### Why it holds structurally thereafter

Crums are not mutated after creation. [SS-POOM-MUTABILITY] establishes that INSERT adds new leaf nodes, DELETE removes and frees them, and REARRANGE shifts only the displacement (`cdsp`) fields — not the width fields. Since no operation writes to an existing crum's width fields after initial construction, the invariant cannot be broken by post-creation modification.

---

### The fragility: the V-address exponent coupling

The V-width exponent is `−shift = −(tumblerlength(vsaptr) − 1)`, which means the V-width encoding precision is determined by the V-address at insertion time, not by the content itself. This creates an implicit dependency: the "same" byte count 11 encodes as `0.11` when inserted at a 2-digit V-address like `1.1`, but would encode differently at a V-address with a different digit length.

[EC-VWIDTH-ZERO-ADDRESS] flags the boundary case: if `vsaptr` is the zero tumbler, `tumblerlength = 0` gives `shift = -1`, producing `exp = +1` — a positive exponent, putting the V-width in a qualitatively different magnitude range from all normal V-widths (which have negative exponents). The 1985 comment `/*I'm suspissious of this shift*/` in `orglinks.c:106` suggests the developer was aware of this. The formal precondition should require `vsaptr` is non-zero with `tumblerlength(vsaptr) >= 1`.

---

### Summary

| Property | Status |
|---|---|
| V-width and I-width encode same span length | Required invariant [INV-WIDTH-VALUE-EQUIVALENCE] |
| Enforcement mechanism | Construction-time derivation from shared integer `inc` [SS-INSERT-VWIDTH-ENCODING] |
| Runtime check after creation | None — invariant holds by immutability of width fields |
| Comparison via `tumblercmp` | Will not detect equality; must use `tumblerintdiff` to extract values |
| Zero-address edge case | May break the encoding; developer-flagged as suspicious [EC-VWIDTH-ZERO-ADDRESS] |

---

## Code Exploration

I now have everything needed. Here is the full analysis.

---

## V-width vs I-width in POOM Bottom Crums

### Short Answer

**V-width and I-width are structurally independent tumblers that encode the same logical span count but at different address-space depths.** They are not equal as tumbler values and can diverge — no invariant enforcement exists. The only coupling is a one-time derivation at insertion time in `insertpm`, where V-width is computed from I-width using a depth-based shift. After that, both dimensions are propagated upward independently, and the code has multiple comments suggesting the mechanism was known to be fragile.

---

### 1. What the Bottom Crum Holds

A POOM bottom crum stores a `typewid cwid` — a 2-element array of tumblers (from `wisp.h`):

```c
#define I  0
#define V  1
```

So `cwid.dsas[I]` is the I-space width and `cwid.dsas[V]` is the V-space width. These are **separate tumblers** representing spans in two distinct coordinate systems. The same `typedsp cdsp` structure holds the I- and V-displacements (start addresses).

---

### 2. How V-width is Derived from I-width at Insertion

The critical code is in `insertpm` (orglinks.c:75–134). For each sprogl in the sprogl set, the function:

```c
// orglinks.c:109
movetumbler (&lwidth, &crumwidth.dsas[I]);    // I-width = direct copy of sprogl width

// orglinks.c:114–117
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength (vsaptr) - 1;
inc   = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

Step by step:

- **I-width** is copied verbatim from `lwidth` — the raw I-space width of the content being linked.
- `tumblerlength(vsaptr)` [tumble.c:259–262] returns `nstories(vsaptr) - vsaptr->exp`, which measures how many digit positions deep the V-space address is.
- `tumblerintdiff(&lwidth, &zero)` [tumble.c:591–597] extracts `lwidth.mantissa[0]` — the integer count of I-space atoms.
- `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` [tumble.c:599–622] constructs V-width as:
  ```c
  cptr->exp = -shift;       // depth matches V-address depth
  cptr->mantissa[0] = inc;  // same integer count
  ```

**Result:** V-width and I-width encode the **same integer count** (`inc` atoms) but at **different exponent positions** in the tumbler — I-width is at whatever depth the I-space address naturally falls, while V-width is placed at depth `shift = tumblerlength(vsaptr) - 1`, matching the depth of the V-address.

As tumbler values they are structurally different. The only "coupling" is that `inc` is shared. Roger Gregory himself flagged this with a 1985 comment marking his own suspicion about the shift.

---

### 3. `tumblerlength` Computes Depth, Not a Width in Common Units

```c
// tumble.c:249–257
INT nstories(tumbler *tumblerptr) {
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}

// tumble.c:259–262
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`tumblerlength` measures the **span of significant digit places** — essentially, how deep the address sits in the hierarchical address tree. This is the structural depth in V-space. When V-width is set using `shift = tumblerlength(vsaptr) - 1`, it is being placed at that depth so that the V-space span aligns with the grain of the V-address.

**I-width has no such shift applied** — it is copied as-is, maintaining the I-space grain. The two widths therefore sit at different levels of their respective address hierarchies.

---

### 4. `widdiffs` Detects Divergence but Does Not Prevent It

```c
// insertnd.c:114–122
static INT widdiffs(typecuc *crumptr) {
    INT i,v;
    if(crumptr->cenftype != POOM)
        return(0);
    i = lastdigitintumbler(&crumptr->cwid.dsas[I]);
    v = lastdigitintumbler(&crumptr->cwid.dsas[V]);
    return(i-v);
}
```

`lastdigitintumbler` returns `mantissa[nstories - 1]` — the highest-order non-zero digit. `widdiffs` computes whether the leading count digit is the same in both dimensions. It is called at the start and end of `insertnd` [insertnd.c:46, 78]:

```c
// insertnd.c:46, 78–85
olddiff = widdiffs(fullcrumptr);
// ... do the insertion ...
newdiff = widdiffs(fullcrumptr);
#ifndef DISTRIBUTION
if(FALSE&&(fullcrumptr->cenftype==POOM)&&olddiff != newdiff){
    fprintf(stderr,"insertnd  possible error dumping widdiffs%d %d\n\r",olddiff,newdiff);
    ...
}
```

Two things are notable here:

1. The check is guarded by `FALSE&&` — it **never executes** even in debug builds. The developer disabled it rather than letting it assert.
2. The fact that `widdiffs` exists at all confirms that V-width and I-width were expected to have matching leading digits — but also that they could diverge in practice, requiring detection.

No assertion runs on this invariant at any stage.

---

### 5. `setwispnd` Propagates Both Dimensions Independently

When widths are propagated upward after insertion, `setwispnd` (wisp.c:171–228) operates on the full lock (both tumblers simultaneously via `lockadd` and `lockmax`):

```c
// wisp.c:213–214
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid,
        (tumbler*)&tempwid, (unsigned)widsize(ptr->cenftype));
lockmax((tumbler*)&newwid, (tumbler*)&tempwid,
        (tumbler*)&newwid, (unsigned)widsize(ptr->cenftype));
```

This computes the bounding box in both dimensions together — the max of `cdsp[I]+cwid[I]` and max of `cdsp[V]+cwid[V]` — separately, with no cross-check between them. There is nothing here that would force `cwid.dsas[I] == cwid.dsas[V]` at any parent node.

The related `setwidnd` (wisp.c:235–247), called from `makegappm` [insertnd.c:170], has an additional bug: it resets `newwid` **inside** the loop, so it only retains the last child's width rather than the max — yet another place where widths can silently become wrong.

---

### 6. The `fixincoresubtreewids` Kluge Confirms Widths Can Drift

Multiple dead-code blocks in `insertnd.c` (lines 32, 59, 65, 98) contain this:

```c
/*fixincoresubtreewids(fullcrumptr);/*1999 // a temp kluge zzz till we find
  where setwisp isnt called// this is a brute force kluge, if this fixes
  anything it means that the wids aren't being set properly somplace else
  probably near here */
```

This 1999 kluge — a brute-force tree-wide width recomputation — was introduced specifically because `setwispupwards` was **not being called reliably**, causing the stored widths to drift from what they should be. It was subsequently commented out, leaving the underlying problem unresolved.

---

### Summary

| Question | Answer |
|----------|--------|
| Must V-width == I-width as tumbler values? | **No.** They live in different address spaces at different depths. |
| Do they represent the same logical span length? | **Intended yes** (same integer count `inc`), but not guaranteed after subsequent operations. |
| What couples them? | Only the initial derivation in `insertpm` [orglinks.c:109–117]: `inc` is taken from I-width and placed into V-width at the V-address depth via `tumblerincrement`. |
| Is this coupling enforced? | **No.** `widdiffs` can detect divergence in leading digits [insertnd.c:114–122], but the check is disabled (`FALSE&&`) and never fires [insertnd.c:80]. `setwispnd` propagates both dimensions independently [wisp.c:213–214]. `setwidnd` has a loop bug that loses all but the last child width [wisp.c:239–241]. |
| Historical evidence of drift? | Yes — the `fixincoresubtreewids` kluge [insertnd.c:32, 59, 65, 98] was a 1999 admission that widths were routinely drifting out of correct state. |

The coupling is a creation-time convention, not a maintained invariant. Once a POOM crum is in the tree, its V-width and I-width are maintained by independent propagation paths that have no coupling mechanism between them.

---

## Question 11 [gregory]

> When `isanextensionnd` detects that a new mapping's I-displacement equals the reach (origin + width) of an existing crum, does it extend the existing crum's V-width and I-width in lockstep, or does it only grow one dimension and recompute the other?

### Gregory's Answer

## KB Synthesis

The KB does not fully resolve this question at the code level.

What the KB establishes:

**For new-crum creation** (`SS-INSERT-VWIDTH-ENCODING` / Finding 0076), the process is asymmetric — the I-width is set directly (`movetumbler(&lwidth, &crumwidth.dsas[I])`), and the V-width is *derived* from it via a re-encoding step (extract integer value, re-encode at V-space precision via `tumblerincrement`). The two widths start with numerically equal values but different tumbler representations.

**For the extension path** (`ST-INSERT` / Finding 0062, `ST-VCOPY` / Finding 0046), the KB only records that the existing crum's width is extended in place at `insertnd.c:243`, without detailing whether both `dsas[V]` and `dsas[I]` in the width field are updated, or whether one is primary and the other recomputed.

**The invariant** (`INV-WIDTH-VALUE-EQUIVALENCE` / Finding 0076) states that after every operation that creates or modifies bottom crums, `tumblerintdiff(crum.width.dsas[V]) == tumblerintdiff(crum.width.dsas[I])`. This constrains what the extension must produce — both dimensions must encode the same numeric value — but does not specify the mechanism.

The KB is silent on whether the extension path mirrors the creation path (derive V-width from updated I-width) or updates both dimensions explicitly in lockstep. Answering definitively would require reading `insertnd.c:243` and the surrounding extension logic directly.

---

## Code Exploration

I now have everything needed to answer the question completely.

---

## Answer

### Short Answer

When `isanextensionnd` recognizes a new mapping as an extension, the caller (`insertcbcnd`) grows **both V-width and I-width simultaneously and independently** via a single `dspadd` call. Neither dimension is derived from or recomputed in terms of the other — each axis gets its own component of `width` added to it in lockstep.

---

### Full Trace

#### 1. Type layout — `cwid` is 2D for POOM crums

`wisp.h:53-55`:
```c
typedef struct structwid typewid;
typedef typewid typedsp;
typedef typewid typewisp;
```

The struct holds an array of tumblers:
```c
tumbler dsas[MAXLOXIZE];
```

For POOM (the 2D enfilade type used here), both `widsize` and `dspsize` equal 2 (`wisp.h:26-27`):
```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

The two slots are indexed by (`wisp.h:19-20`):
```c
#define I  0    /* I-space (ispace) dimension */
#define V  1    /* V-space (vspace) dimension */
```

So `ptr->cwid.dsas[I]` is the I-width and `ptr->cwid.dsas[V]` is the V-width.

---

#### 2. `prologuend` computes both dimensions of `reach`

`retrie.c:334-339`:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    if (reach)
        dspadd(grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`dspadd` is (`wisp.c:15-18`):
```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd(a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

And `lockadd` (`wisp.c:269-272`) iterates `loxize` times — for POOM, 2 times:
```c
int lockadd(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
    while (loxize--)
        tumbleradd(lock1++, lock2++, lock3++);
}
```

Result: `reach.dsas[I] = grasp.dsas[I] + ptr->cwid.dsas[I]` and `reach.dsas[V] = grasp.dsas[V] + ptr->cwid.dsas[V]`. Both I and V components of `reach` are computed independently.

---

#### 3. `isanextensionnd` checks **all** `dspsize` dimensions simultaneously

`insertnd.c:301-309`:
```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    bool lockeq();
    if (!tumblereq(&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq(reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` (`wisp.c:261-267`) iterates `loxize = dspsize(POOM) = 2` times, comparing each element:
```c
bool lockeq(tumbler *lock1, tumbler *lock2, unsigned loxize)
{
    while (loxize--)
        if (!tumblereq(lock1++, lock2++))
            return(FALSE);
    return(TRUE);
}
```

So the adjacency test is: **`reach.dsas[I] == originptr->dsas[I]` AND `reach.dsas[V] == originptr->dsas[V]`**. Both dimensions must match. This is a strict 2D coincidence check — the new mapping must abut the existing crum on both axes simultaneously.

---

#### 4. When the check passes, `dspadd` grows both widths in lockstep

`insertcbcnd` at `insertnd.c:250-252`:
```c
if (isanextensionnd((typecbc*)ptr, grasp, origin, infoptr)) {
    dspadd(&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
    ivemodified(ptr);
```

`dspadd(&ptr->cwid, width, &ptr->cwid, father->cenftype)` expands to:
```c
lockadd(ptr->cwid.dsas, width->dsas, ptr->cwid.dsas, dspsize(POOM));
// i.e., 2 iterations:
ptr->cwid.dsas[I] += width->dsas[I];   // I-width grows by width's I-component
ptr->cwid.dsas[V] += width->dsas[V];   // V-width grows by width's V-component
```

No recomputation, no cross-axis dependency. Each component of `cwid` is incremented by the matching component of `width`.

---

### Summary

**`isanextensionnd` and its caller grow V-width and I-width in lockstep, each by its own independent component of `width`.**

- The adjacency test (`insertnd.c:308`) uses `lockeq` over `dspsize(cenftype) = 2` slots — both I and V components of `reach` must exactly equal `originptr`. This is a joint 2D check; a crum that abuts on only one axis does not pass.
- The mutation (`insertnd.c:251`) uses `dspadd` → `lockadd` over the same 2 slots — it adds `width->dsas[I]` to `cwid.dsas[I]` and `width->dsas[V]` to `cwid.dsas[V]` in a single pass, independently. No dimension is derived from or capped by the other.

The design relies entirely on the invariant that a matching extension has equal-width in both axes (since the same `width` value is threaded through the entire FEBE protocol call chain and stored in both slots when the original mapping was created). The code does not enforce this invariant locally — it simply passes `width` straight into `dspadd` as-is.

---

## Question 12 [gregory]

> When `slicecbcpm` cuts a bottom crum at an interior point (THRUME case), how are the two resulting crums' I-displacements computed — does the second piece's I-displacement advance by exactly the V-offset of the cut within the original span?

### Gregory's Answer

## KB Synthesis

The KB does not directly document the I-displacement computation inside `slicecbcpm`. Here is what is known, and where the gap lies.

**What the KB documents about the cut:**

[INV-NO-ZERO-WIDTH-CRUM] covers `slicecbcpm` at `ndcuts.c:396-444` and establishes:
- `localcut = tumblersub(cut, &grasp, &localcut)` — this is the V-offset of the cut point within the original crum (strictly positive, since THRUME is required)
- The original crum retains V-width `localcut`
- The new crum receives V-width `locksubtract(cwid, localcut)` — the remainder

**What the KB documents about crum structure:**

[SS-POOM-BOTTOM-CRUM] establishes that each bottom crum holds dual-space coordinates:
```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

[INV-WIDTH-VALUE-EQUIVALENCE] establishes that `tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)` — both widths encode the same integer, just at different tumbler precisions.

**The inference the KB supports, but does not confirm:**

Since each bottom crum is a 1:1 linear mapping from a contiguous V-range to a contiguous I-range ([INV-POOM-BIJECTIVITY], [INV-SINGLE-CHAR-GRANULARITY]), and since V-widths and I-widths encode the same integer values, cutting at V-offset `localcut` should advance the second crum's I-origin by the same integer count. But no finding explicitly documents the `slicecbcpm` formula for the second crum's `dsas[I]` origin computation, and the code at `ndcuts.c:396-444` is not directly traced in any finding.

**Answer:** Not fully answerable from the KB. The V-side of the cut is documented — `localcut = cut - grasp`, first crum retains V-width `localcut`, second receives the remainder. The I-side advance is not directly stated in any finding. Based on [INV-WIDTH-VALUE-EQUIVALENCE] and the bijective structure of POOM crums [INV-POOM-BIJECTIVITY], the second crum's I-origin should advance by the same integer as `localcut`, but this would require reading `ndcuts.c:396-444` directly to confirm.

---

## Code Exploration

Now I have all the pieces. Let me write the full answer.

---

## How `slicecbcpm` Computes I-Displacements for the Two Resulting Crums

### Entry conditions and calling context

`slicecbcpm` is called from `makecutsbackuptohere` [ndcuts.c:84] when `whereoncrum` returns `THRUME` (the cut falls strictly inside the crum's span):

```c
// ndcuts.c:79-84
if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
    new = (typecuc *)createcrum((INT)ptr->height,(INT)ptr->cenftype);
    ...
    slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

The `dimension` field of `typeknives` is documented as *"always V, assigned by rearrange2d"* [ndenf.h:15], so `index = V = 1` for POOM.

---

### Step 1 — Compute `grasp`: absolute V-position of the crum's left edge [ndcuts.c:382]

```c
prologuend(ptr, offset, &grasp, NULL);
```

`prologuend` [retrie.c:334–338]:
```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
    dspadd(offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);
    ...
}
```
`dspadd` calls `lockadd` over all `dspsize(POOM) = 2` components [wisp.c:15–17], so:
- `grasp.dsas[I] = offset.dsas[I] + ptr->cdsp.dsas[I]`
- `grasp.dsas[V] = offset.dsas[V] + ptr->cdsp.dsas[V]`

---

### Step 2 — `localcut`: V-offset of the cut within the crum [ndcuts.c:396]

```c
tumblersub(cut, &grasp.dsas[index], &localcut);
```

This subtracts the crum's absolute V-left-edge from the knife position:

```
localcut = cut − grasp.dsas[V]
         = cut − (offset.dsas[V] + ptr->cdsp.dsas[V])
```

`localcut` is the V-distance from the crum's own left edge to the cut point. Two sanity guards enforce its structure:
- **Line 398**: `localcut.exp` must equal `ptr->cwid.dsas[V].exp` — the cut is at the same tumbler level as the crum's V-width
- **Lines 410–430**: `is1story(&localcut)` must hold — only `mantissa[0]` is non-zero

---

### Step 3 — The wid split loop [ndcuts.c:438–445]

This is where both resulting widths and the I-displacement of the second piece are determined. The code author flagged it honestly:

```c
// ndcuts.c:438-445
movewisp(&ptr->cwid, &newwid);                        // newwid ← copy of ptr->cwid
for (i = 0; i < widsize(enftype); i++) {              // i ∈ {I=0, V=1} for POOM
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0]; // overwrite mantissa[0] only
    tumblerjustify(&newwid.dsas[i]);
}
locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype)); // new->cwid = original−newwid
movewisp(&newwid, &ptr->cwid);                        // first piece gets newwid
```

**What the loop does per dimension:**

After `movewisp`, `newwid.dsas[i]` is a complete copy of `ptr->cwid.dsas[i]`, including its `exp` field. The loop then *only replaces* `mantissa[0]` with `localcut.mantissa[0]` — the `exp` of each dimension is left untouched.

For `i = V`: Since the assertion at line 398 guarantees `localcut.exp == ptr->cwid.dsas[V].exp`, the result is that `newwid.dsas[V] == localcut` as a tumbler value — the first piece gets exactly the V-distance to the cut as its V-width.

For `i = I`: `newwid.dsas[I]` gets `exp = ptr->cwid.dsas[I].exp` (the I-space exponent) but `mantissa[0] = localcut.mantissa[0]` (the V-cut count). **The I and V exponents are in general different**, because I-space and V-space live at different depths of the tumbler hierarchy.

This is visible from `insertpm` [orglinks.c:105–117], which is how POOM crums are created:

```c
movetumbler(&lwidth, &crumwidth.dsas[I]);              // I-wid = lwidth (at I-space exp)
shift = tumblerlength(vsaptr) - 1;
inc   = tumblerintdiff(&lwidth, &zero);                // inc = lwidth.mantissa[0]
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]); // V-wid: inc at V-space level
```

The I-wid is stored at `lwidth.exp` (an I-sequence address exponent); the V-wid is stored at `shift = tumblerlength(vsaptr) − 1` (a V-document exponent). These are the same **count** (`inc`) but at different tumbler levels.

The diagnostic function `widdiffs` [insertnd.c:114–122] confirms the invariant: `lastdigit[I] == lastdigit[V]`, i.e., `ptr->cwid.dsas[I].mantissa[0] == ptr->cwid.dsas[V].mantissa[0]`.

---

### Step 4 — `new->cdsp` for the second piece [ndcuts.c:446]

```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
```

At this point `ptr->cwid` has been updated to `newwid`. `dspadd` calls `lockadd` over both components:

```
new->cdsp.dsas[V] = ptr->cdsp.dsas[V] + newwid.dsas[V]
                  = ptr->cdsp.dsas[V] + localcut
                  = ptr->cdsp.dsas[V] + (cut − offset.dsas[V] − ptr->cdsp.dsas[V])
                  = cut − offset.dsas[V]

new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + newwid.dsas[I]
```

Where `newwid.dsas[I]` has:
- `mantissa[0] = localcut.mantissa[0]`   ← the V-cut's scalar count
- `exp         = ptr->cwid.dsas[I].exp`  ← the I-space exponent, NOT the V-space exponent

---

### Direct answer to the question

**The second piece's I-displacement does advance by `localcut.mantissa[0]` — the scalar count of the V-offset — but expressed in I-space coordinates, not in V-space coordinates.**

Numerically as a tumbler:
```
newwid.dsas[I] value = localcut.mantissa[0] × base^(ptr->cwid.dsas[I].exp)
localcut       value = localcut.mantissa[0] × base^(ptr->cwid.dsas[V].exp)
```

These are identical tumblers only if `ptr->cwid.dsas[I].exp == ptr->cwid.dsas[V].exp`. In practice, I-space and V-space live at different tumbler depths (I-space is sequential content addressing; V-space is document version addressing), so the two exponents differ and the I-displacement advance is **not the same tumbler** as the V-offset of the cut.

What the loop actually does — and this is what the comment `/* I really don't understand this loop */` [ndcuts.c:439] confesses to — is apply the same **scalar count** (`localcut.mantissa[0]`) to every dimension of the wid, using each dimension's pre-existing exponent as its scale. This correctly partitions the crum in all dimensions simultaneously while preserving the POOM invariant (`widdiffs == 0`): the count of I-units in each resulting piece equals the count of V-units.

In short: the I-displacement of the second piece advances by **the same count of atomic units** as the V-offset of the cut, but scaled by I-space's exponent rather than V-space's exponent. It is proportionally correct, not numerically identical to the V-offset tumbler.

---

## Question 13 [gregory]

> Can a single POOM bottom crum map a V-span to a non-contiguous I-span, or is there a strict invariant that each bottom crum represents a contiguous-to-contiguous mapping where both V and I ranges are unbroken?

### Gregory's Answer

## KB Synthesis

Each POOM bottom crum encodes a **strict contiguous-to-contiguous linear mapping**. There is no mechanism for a single crum to represent a non-contiguous I-span.

## Structural evidence

[SS-POOM-BOTTOM-CRUM] (Finding 0076) shows the bottom crum structure directly:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

A single `origin` and `width` per dimension. There is no field for a set of I-ranges or a scatter list — the representation structurally cannot express non-contiguity within a single crum.

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) establishes that `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` — the V-width and I-width encode the same integer. This enforces a 1:1 linear mapping: a V-span of width *w* maps to exactly *w* consecutive I-addresses.

## Extension invariant confirms both dimensions must be contiguous

[ST-VCOPY] / [ST-INSERT] (Finding 0046) describe `isanextensionnd()` at `insertnd.c:293-301`: a new mapping is merged into an existing crum only when (1) same `homedoc` **and** (2) the new content starts exactly where the existing crum ends — contiguous in **both** V and I simultaneously. If either dimension is non-contiguous, a new separate crum is created instead.

This means two adjacent V-positions mapping to I-addresses from different source documents (transcluded content) always produce **two crums**, not one crum with a non-contiguous I-range.

## What happens with transcluded content from multiple sources

[SS-SPORGL] (Finding 0013) and [ST-LINK-CREATE] (Finding 0037) document exactly this case. When a V-span covers content transcluded from two documents (e.g., "AA" from A and "BB" from B), `vspanset2ispanset` → `permute` → `span2spanset` walks the POOM and returns **one I-span per contiguous I-address region**. The POOM itself stores two separate crums — one per contiguous I-block — not a single crum spanning both.

[SS-POOM-MULTIMAP] (Finding 0039) confirms the multimap semantics: multiple V-positions can reference the same I-address, but this is achieved through **multiple crums** each with their own linear (V, I) pair, never through a single crum with a non-contiguous I-range.

## Summary

The invariant is strict: **every POOM bottom crum is a length-preserving 1:1 linear mapping from a contiguous V-range `[v, v+w)` to a contiguous I-range `[i, i+w)`**. Non-contiguous I-spans in a V-region are always represented as multiple crums, never as a single crum. The data structure, the extension check, and the width-equivalence invariant all enforce this together.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Answer: POOM Bottom Crum Contiguity Invariant

**The invariant is strict: each POOM bottom crum encodes exactly one contiguous I-span and one contiguous V-span, of equal integer width, in a unit-ratio bijection. Non-contiguous mappings are represented at the tree level by multiple bottom crums, never within a single one.**

Here is the code-by-code proof.

---

### 1. Data Structure

The fundamental types are defined in `backend/wisp.h` and `backend/enf.h`.

`backend/wisp.h:50-54`:
```c
struct structwid {
    tumbler dsas[MAXLOXIZE];
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

`backend/wisp.h:19-21` (the index constants):
```c
#define I  0
#define V  1
```

`backend/wisp.h:25-27` (sizes):
```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
```

`backend/enf.h:109-131` (the POOM bottom crum type):
```c
struct struct2dcbc {
    ...
    typewid cwid;   /* width in both I and V dimensions */
    typedsp cdsp;   /* displacement (origin) in both I and V dimensions */
    type2dbottomcruminfo c2dinfo;  /* homedoc: the source document ISA */
};
typedef struct struct2dcbc type2dcbc;
```

And `type2dbottomcruminfo` (`backend/wisp.h:107-109`):
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

So each bottom crum stores: `cdsp.dsas[I]` (I-origin), `cwid.dsas[I]` (I-width), `cdsp.dsas[V]` (V-origin), `cwid.dsas[V]` (V-width), and `c2dinfo.homedoc` (source document). That is four tumblers — two intervals, one per dimension. There is no mechanism to store more than one contiguous interval per dimension in a single crum.

---

### 2. Creation: Equal-Width Bijection Is Enforced at Insertion Time

`insertpm` in `backend/orglinks.c:75-134` is the entry point for inserting content into the POOM. For each item in the sporgl set, it builds `crumorigin` and `crumwidth` then calls `insertnd`:

```c
// orglinks.c:105-130
movetumbler (&lstream, &crumorigin.dsas[I]);      // I-origin = lstream
movetumbler (&lwidth, &crumwidth.dsas[I]);         // I-width = lwidth
movetumbler (vsaptr, &crumorigin.dsas[V]);         // V-origin = vsaptr
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);             // integer count of I-width
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = same count
...
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);  // advance vsaptr for next iteration
```

Key observations:
- `inc = tumblerintdiff(&lwidth, &zero)` extracts the integer count of the I-span.
- `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` constructs a V-width with the **same integer count**, just expressed at the tumbler depth of `vsaptr`.
- Both `crumorigin.dsas[I]` and `crumorigin.dsas[V]` are single tumblers (single points), so each is a single contiguous interval start.

The V and I widths are always equal in integer count. The mapping is a unit-ratio bijection: one I-position per V-position.

---

### 3. Bottom Crum Allocation: One Origin and Width Per Crum

`insertcbcnd` in `backend/insertnd.c:242-275` is where the actual bottom crum is created or extended:

```c
// insertnd.c:260-268
new = createcrum (0, (INT)father->cenftype);
...
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   // sets both cdsp[I] and cdsp[V]
...
movewisp (width, &new->cwid);                                  // copies both cwid[I] and cwid[V]
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);
```

`dspsub` subtracts the parent's grasp from `origin` across all dimensions of the POOM (`dspsize(POOM) = 2`), giving the crum's displacement relative to its parent in both I and V simultaneously. `movewisp` copies the full 2-dimensional width. One call → one crum → one I-interval and one V-interval. There is no way to construct a crum with more than one interval per dimension.

The extension path (merging into an adjacent existing crum) uses `isanextensionnd` at `insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` with `dspsize(POOM) = 2` checks that **both** `reach.dsas[I] == origin->dsas[I]` AND `reach.dsas[V] == origin->dsas[V]` simultaneously. That is, both dimensions must be exactly adjacent. If they are, the width is extended at `insertnd.c:251`:

```c
dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);
```

Again, `dspsize(POOM) = 2` — both dimensions are extended together. An existing crum can only be extended by a region that is simultaneously adjacent in both I and V. This preserves the contiguous-to-contiguous invariant.

---

### 4. Retrieval: Single-Dimension Interval Test Confirms One Interval Per Dimension

`whereoncrum` in `backend/retrie.c:345-398` is the workhorse for navigating the tree:

```c
// retrie.c:355-373
case SPAN:
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    ...
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
    cmp = tumblercmp(address, &right);
    if(cmp == LESS){
        return(THRUME);
    }else if (cmp == EQUAL){
        return (ONMYRIGHTBORDER);
    }else{
        return(TOMYRIGHT);
    }
```

For a given `index` (either `I` or `V`), the crum occupies the interval `[left, right)` where `left = offset[index] + cdsp[index]` and `right = left + cwid[index]`. This is a single closed interval. The function returns one of five positions (TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT). There is no branching for "non-contiguous sub-ranges" because the crum has exactly one interval per dimension.

The 2D area query `findcbcinarea2d` (`retrie.c:229-268`) and `crumqualifies2d` (`retrie.c:270-305`) test the two dimensions independently by calling `whereoncrum` twice with different `index` values. This is checking that the crum's rectangular region intersects a query rectangle — not that any single crum has a non-contiguous span.

---

### 5. Split Operations Preserve the Invariant

`splitcrumpm` in `backend/split.c:117-128`:

```c
int splitcrumpm(typecuc *father)
{
    typecorecrum *ptr, *correctone;
    for(correctone=ptr=findleftson(father);ptr;ptr = findrightbro(ptr)) {
        if (tumblercmp (&ptr->cdsp.dsas[SPANRANGE], &correctone->cdsp.dsas[SPANRANGE]) == GREATER)
            correctone = ptr;
    }
    peelcrumoffnd(correctone);
}
```

When a POOM upper crum has too many sons, the split peels one son into its own new parent via `peelcrumoffnd`. This is purely a tree restructuring — no bottom crum's `cdsp` or `cwid` is changed, so the contiguous-to-contiguous property of each bottom crum is preserved across splits.

`peelcrumoffnd` at `split.c:130-169` does:
```c
movewisp(&father->cdsp, &new->cdsp);   // new parent inherits father's cdsp
adopt(ptr, LEFTMOSTSON, new);           // peeled crum becomes new parent's only son
```

The peeled bottom crum's own `cdsp` and `cwid` are never touched.

---

### 6. The `homedoc` Field and Multi-Document POOM

The `c2dinfo.homedoc` field in each bottom crum (`wisp.h:107-109`) is the ISA (address) of the source document for that crum's I-span. `crumqualifies2d` checks at `retrie.c:274-279`:

```c
if ((crumptr->height == 0) && infoptr && !tumblereq (&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc))){
    return (FALSE);
}
```

This means that in a multi-document context, `homedoc` disambiguates which document's I-space the crum belongs to. But even then, each crum still has one contiguous I-span within one document's I-space, and one contiguous V-span.

---

### Summary

| Property | Enforced? | Where |
|----------|-----------|-------|
| Each bottom crum has exactly one I-interval | Yes, structurally | `enf.h:109-131` — one `cdsp.dsas[I]` + `cwid.dsas[I]` |
| Each bottom crum has exactly one V-interval | Yes, structurally | `enf.h:109-131` — one `cdsp.dsas[V]` + `cwid.dsas[V]` |
| I-width == V-width (integer count) | Yes, at insertion | `orglinks.c:115-117` — `inc` used for both |
| Extension requires simultaneous adjacency in both dimensions | Yes | `insertnd.c:308` — `lockeq` with `dspsize(POOM)=2` |
| Splits do not fragment bottom crums | Yes | `split.c:130-169` — no `cdsp`/`cwid` mutation |

**A single POOM bottom crum cannot map a V-span to a non-contiguous I-span.** The data structure physically stores only one origin and one width per dimension. The enforcement is:

1. **Structural** — only two tumblers per dimension in `cwid`/`cdsp`
2. **At insertion** — `insertpm` derives both widths from the same integer count; `insertcbcnd` stores one origin and one width from a single call
3. **At extension** — `isanextensionnd` requires simultaneous adjacency in all dimensions via `lockeq(reach.dsas, origin->dsas, dspsize(POOM)=2)`

Non-contiguous mappings at the document level are represented by **multiple bottom crums** across the tree, each individually encoding a simple, contiguous, unit-ratio piece. The enfilade tree structure is what allows an arbitrarily complex permutation to be encoded efficiently — not any internal complexity within a single leaf.

---

## Question 14 [gregory]

> When two logically distinct COPY operations produce I-address-adjacent mappings in a target POOM and `isanextensionnd` silently merges them into one crum, is there any residual record that the crum originated from two separate operations, or is the merge information-destroying?

### Gregory's Answer

## KB Synthesis

The merge is **information-destroying** with respect to operation count and per-operation boundaries.

## What the crum retains after merging

From [SS-POOM-BOTTOM-CRUM] (Finding 0076), a POOM bottom crum has exactly four fields:

```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```

No operation count, no timestamp, no list of contributing spans. When [ST-VCOPY] Finding 0046 describes the extension path — `isanextensionnd` matches, `crum.width` is widened in place at `insertnd.c:243` — the prior boundary simply vanishes. There is no residual record that the region was assembled from two operations versus one.

[INV-VSPAN-CONSOLIDATION] (Finding 0028) confirms this explicitly: after 100 separate single-character inserts, `retrieve_vspanset` returns `span_count: 1`. The enfilade makes no distinction between a single bulk operation and N sequential ones that happen to coalesce.

## What is partially preserved

The one discriminating field is `homedoc`. From [PRE-COPY] Finding 0046:

> The extension check's `homedoc` condition means crums from different source documents are never merged.

Two COPYs from **different** home documents cannot coalesce — they always produce separate crums, preserving the fact that they originated from distinct sources. But two COPYs from the **same** home document with I-address-adjacent, V-address-adjacent results are indistinguishable from a single COPY of the combined range after the merge.

## The granfilade is not affected

The underlying I-addresses allocated by each COPY remain permanently and individually in the granfilade ([INV-IADDR-IMMUTABILITY], [FC-GRANF-ON-DELETE]). What is lost is only the POOM-level record of how those I-addresses were placed — the cut point between the two operations' contributions is erased. You can still address individual bytes through the granfilade, but you cannot reconstruct from the POOM alone that two separate operations were responsible.

**Summary:** The merge loses all information about operation boundaries and count. Only cross-document provenance (via `homedoc`) survives. Same-document multi-COPY history is not preserved.

---

## Code Exploration

I now have all the source I need. Let me compile the full answer.

---

## Answer: Is the `isanextensionnd` Merge Information-Destroying?

**Yes, unconditionally. The merge destroys the boundary information. No residual record is kept.**

Here is the full trace.

---

### 1. The Bottom-Crum Data Structure Has Exactly One Identity Field

The 2D bottom crum (`type2dcbc`) is defined in `enf.h:109-131`:

```c
struct struct2dcbc {
    ...
    typewid cwid;          /* combined width in both I and V */
    typedsp cdsp;          /* displacement: origin in both I and V */
    type2dbottomcruminfo  c2dinfo;   /* ← the sole identity payload */
};
```

And `type2dbottomcruminfo` is defined in `wisp.h:107-109`:

```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;
} type2dbottomcruminfo;
```

**`homedoc` is the entire identity record for a POOM bottom crum.** It is a single tumbler — the ISA of the source document. There is no `origin_count`, no sub-span list, no operation log, no boundary marker.

---

### 2. What `isanextensionnd` Actually Tests

`insertnd.c:301-309`:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr,
                     type2dbottomcruminfo *infoptr)
{
  typedsp grasp, reach;
  bool lockeq();
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

Two conditions must both hold:

1. **Same `homedoc`** — the new crum's source document ISA equals the existing crum's `c2dinfo.homedoc` (line 305).
2. **Exact adjacency in ALL dimensions** — `lockeq` compares `reach.dsas[0..dspsize-1]` to `originptr->dsas[0..dspsize-1]`. For POOM, `dspsize(POOM) == DSPSIZEPM == 2` (`wisp.h:27`), so both the I and V right-edges of the existing crum must exactly equal the I-V origin of the new insertion.

This is a stricter condition than I-adjacency alone: the two COPY operations must land contiguously in **both** I-space and V-space simultaneously.

---

### 3. The Merge Operation

When `isanextensionnd` returns `TRUE`, `insertcbcnd` (insertnd.c:249-258) does exactly this:

```c
for (ptr = findleftson (father); ptr; ptr = findrightbro (ptr)) {
    if (isanextensionnd ((typecbc*)ptr, grasp, origin, infoptr)) {
        dspadd (&ptr->cwid, width, &ptr->cwid, (INT)father->cenftype);  /* line 251 */
        ivemodified (ptr);
        setwispupwards (father,1);
        ...
        return(FALSE);
    }
}
```

**Only one field is mutated**: `ptr->cwid` is incremented by `width` via `dspadd`. This is integer addition on the tumbler — a write-only, non-invertible operation.

| Field | Before merge | After merge |
|---|---|---|
| `cdsp.dsas[I]` | I-origin of op1 | **unchanged** |
| `cdsp.dsas[V]` | V-origin of op1 | **unchanged** |
| `cwid.dsas[I]` | width1_I | **width1_I + width2_I** |
| `cwid.dsas[V]` | width1_V | **width1_V + width2_V** |
| `c2dinfo.homedoc` | source doc ISA | **unchanged** |

No new crum is created (`createcrum` at line 260 is in the `else` branch that is skipped). The `infoptr` for the second operation — which carries the second copy's origin and width — is used only to compute the merged `cwid`, then discarded. The internal I/V boundary between the two operations is arithmetically summed away.

---

### 4. The Path That Creates the Crum in the First Place

For comparison: when no merge occurs, `insertcbcnd` creates a fresh crum at lines 260-267:

```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);
dspsub (origin, grasp, &new->cdsp, (INT)father->cenftype);   /* sets cdsp */
movewisp (width, &new->cwid);                                  /* sets cwid */
move2dinfo (infoptr, &((type2dcbc *)new)->c2dinfo);            /* sets homedoc */
```

All three fields (`cdsp`, `cwid`, `c2dinfo`) are set from the incoming operation data. When the merge path fires instead, only `cwid` is updated; the other two carry over from op1, and op2's origin/info is gone.

---

### 5. How `homedoc` Is Populated per COPY Call

The chain from `docopy` → `insertpm` → `unpacksporgl` in `sporgl.c:178-187`:

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr,
                 tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
    ...
    } else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
        movetumbler (&((typesporgl *)sporglptr)->sporglorigin, streamptr);
        movetumbler (&((typesporgl *)sporglptr)->sporglwidth, widthptr);
        movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
    }
```

`sporgladdress` is the ISA of the source document. This is the only identity datum passed down through `insertpm` → `insertnd` → `insertcbcnd` → `isanextensionnd`. **There is no field for "I-origin within source"** or any other per-operation annotation beyond `homedoc`.

---

### 6. No Secondary Record Survives

`docopy` (do1.c:53-65) also calls `insertspanf`:

```c
&& insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)
&&  insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)
```

The spanfilade records which I-spans belong to a document — the *inverse* mapping. But if the two COPY operations draw on I-adjacent spans from the same source, `putvspaninlist` in `orglinks.c:346-347` coalesces them too:

```c
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);   /* merge adjacent */
    return(0);
}
```

So the spanfilade also loses the inter-operation boundary for adjacent I-spans from the same source document.

The granfilade records raw content and has no knowledge of COPY operation identity at all.

---

### Summary

The merge performed by `isanextensionnd` + `insertcbcnd:251` is **fully and irrecoverably information-destroying**:

- The merged crum records only: (I-start of op1, V-start of op1, combined I-width, combined V-width, shared homedoc).
- The internal I/V boundary between op1 and op2 is gone.
- The fact that two distinct operations contributed is gone.
- The `type2dbottomcruminfo` structure has a single field (`homedoc`), providing no space for boundary or count metadata.
- The `dspadd` at `insertnd.c:251` is scalar addition on tumblers — not annotated, not logged, and not reversible without out-of-band knowledge of the original widths.
- No other data structure (spanfilade, granfilade) preserves per-COPY-operation provenance.

The design treats the merged span as if it were always a single contiguous copy. From the perspective of the enfilade, it is indistinguishable from having issued one COPY that covered the combined I-span in the first place.

---

## Question 15 [gregory]

> In the 2D POOM enfilade, the root displacement tracks the minimum child address via `setwispnd` — does this minimum track independently in V and I dimensions, or is there a single combined displacement that couples the two?

### Gregory's Answer

## KB Synthesis

The V and I dimensions track **independently**. The `cdsp` displacement field is a multi-dimensional structure with separate `dsas[V]` and `dsas[I]` components; `setwispnd` operates on each dimension autonomously.

**Evidence from the KB:**

[SS-POOM-BOTTOM-CRUM] (Finding 0076) shows the crum structure directly:
```
BottomCrum = {
  origin: { dsas[I]: Tumbler, dsas[V]: Tumbler },
  width:  { dsas[I]: Tumbler, dsas[V]: Tumbler }
}
```
Each dimension carries its own tumbler value with its own precision. The V and I origins and widths are stored and manipulated as separate fields.

[ST-REARRANGE] (Finding 0056) is the clearest proof: "The code modifies only `ptr->cdsp.dsas[index]` (the V-address component of the displacement). The I-address, stored separately, is never touched." A rearrange operation on `dsas[V]` leaves `dsas[I]` completely unchanged — impossible if they were coupled.

[INV-ENFILADE-RELATIVE-ADDRESSING] (Finding 0066) states `absolute_grasp(node) = absolute_grasp(parent) + node.cdsp`, where the `cdsp` addition (`dspadd`) operates on each dimension's component. The `setwispnd` algorithm at `wisp.c:196` absorbs `mindsp` into the parent and subtracts it from children — but `mindsp` is computed per-dimension: the minimum V-displacement across children is absorbed into `cdsp.dsas[V]`, and the minimum I-displacement independently into `cdsp.dsas[I]`.

[ST-INSERT] (Finding 0054) confirms the operational independence: the two-blade knife shifts `cdsp.dsas[V]` for entries within the knife range, leaving `cdsp.dsas[I]` untouched. INSERT in the V-dimension does not disturb I-dimension displacements at all.

**Summary:** The POOM root's `cdsp` is a 2D displacement vector. `setwispnd` finds the per-dimension minimum independently — the V-component minimum is absorbed into `cdsp.dsas[V]` while the I-component minimum is absorbed into `cdsp.dsas[I]`. Children's relative displacements are adjusted dimension-by-dimension. The two dimensions are structurally parallel but have no coupling in the displacement tracking mechanism.

---

## Code Exploration

I now have everything I need. Here is the full answer:

---

## POOM Displacement: Independent Per-Dimension, Not Combined

The displacement in the 2D POOM enfilade tracks **I and V independently** — there is no single combined scalar. They share a single struct, but that struct contains **two separate tumblers** that are operated on in lockstep by array iteration, never collapsed into one value.

---

### The Data Structure

Every POOM node (both upper `typecuc` and bottom crums) carries two fields [`enf.h:47-48`, `enf.h:71-72`, `enf.h:102-103`]:

```c
typewid cwid;
typedsp cdsp;
```

Both `typewid` and `typedsp` are the same struct [`wisp.h:50-55`]:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

For POOM, `dspsize` and `widsize` both return **2** [`wisp.h:26-27`, `wisp.h:60-61`]:

```c
#define DSPSIZEPM 2
#define WIDSIZEPM 2
#define dspsize(A) ((A)==GRAN?DSPSIZEGR:((A)==SPAN?DSPSIZESP:DSPSIZEPM))
```

The two slots are named by index [`wisp.h:19-20`]:

```c
#define I  0
#define V  1
```

So `cdsp.dsas[I]` is the I-stream displacement and `cdsp.dsas[V]` is the V-stream displacement. They coexist in one struct but are two independent tumbler values.

---

### How `setwispnd` Operates

`setwispnd` is the POOM/SPAN variant of the widditive recalculation, dispatched from `setwisp` when `cenftype` is `POOM` or `SPAN` [`wisp.c:126-131`]:

```c
case SPAN:
case POOM:
    return (setwispnd ((typecuc*)ptr));
```

Inside `setwispnd` [`wisp.c:171-228`], the critical operations are:

**Step 1 — Find the minimum child displacement (upper-left corner):**

```c
movewisp (&ptr->cdsp, &mindsp);                           /* line 193 — seed with first child */
for (ptr = getrightbro(ptr); ptr; ptr = getrightbro (ptr)) {
    lockmin ((tumbler*)&mindsp, (tumbler*)&ptr->cdsp,
             (tumbler*)&mindsp, (unsigned)dspsize(ptr->cenftype));  /* line 195 */
}
```

`lockmin` at [`wisp.c:281-287`] iterates over the `loxize` (= `dspsize` = **2** for POOM) tumblers independently:

```c
int lockmin(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
    while (loxize--){
        macrotumblermin (lock1, lock2, lock3);   /* per-tumbler min */
        lock1++; lock2++; lock3++;
    }
}
```

And `macrotumblermin` is a simple component-wise comparison [`common.h:144`]:

```c
#define macrotumblermin(a,b,c) \
    ((*(tumbler*)(c)) = (tumblercmp((a),(b))==LESS) ? (*(tumbler*)(a)) : (*(tumbler*)(b)))
```

This means `mindsp` ends up as **`{ min(all children's dsas[I]), min(all children's dsas[V]) }`** — the minimums are computed **per-dimension and independently**.

**Step 2 — Update father's displacement:**

```c
dspadd (&father->cdsp, &mindsp, &newdsp, (INT)father->cenftype);   /* line 200 */
```

`dspadd` [`wisp.c:15-18`] calls `lockadd` over all `dspsize` tumblers:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
    lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

Again component-wise: `newdsp.dsas[I] = father->cdsp.dsas[I] + mindsp.dsas[I]` and `newdsp.dsas[V] = father->cdsp.dsas[V] + mindsp.dsas[V]`.

**Step 3 — Compensate each child to preserve absolute positions:**

```c
dspsub(&ptr->cdsp, &mindsp, &ptr->cdsp, (INT)ptr->cenftype);   /* line 211 */
```

Same component-wise structure. Each child's I is reduced by `mindsp.dsas[I]`; each child's V is reduced by `mindsp.dsas[V]`.

**Step 4 — Find the maximum corner (width):**

```c
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid,
        (unsigned)widsize(ptr->cenftype));                         /* line 213 */
lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid,
        (unsigned)widsize(ptr->cenftype));                         /* line 214 */
```

`lockmax` mirrors `lockmin` — independent per-dimension max. Father's `cwid` becomes `{ max(cdsp[I]+cwid[I]), max(cdsp[V]+cwid[V]) }` across children.

---

### Evidence of Independent Tracking in Insertion

`insertnd.c` directly indexes the dimensions by name at points where only one axis is being adjusted. For example, at [`insertnd.c:162`]:

```c
tumbleradd(&ptr->cdsp.dsas[V], &width->dsas[V], &ptr->cdsp.dsas[V]);
```

Only `dsas[V]` is modified — `dsas[I]` is left untouched. This is only coherent if the two dimensions are tracked independently; a combined representation would require both to be updated together.

Similarly, insertion cuts are made exclusively on V [`insertnd.c:140-145`]:

```c
if (iszerotumbler (&fullcrumptr->cwid.dsas[V])
|| tumblercmp (&origin->dsas[V], &grasp.dsas[V]) == LESS
|| tumblercmp (&origin->dsas[V], &reach.dsas[V]) != LESS)
    ...
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
```

The I dimension is not consulted for this cut, confirming they live independently.

---

### Summary

| Property | Answer |
|---|---|
| **Storage** | Single `typedsp` struct, but containing `dsas[2]` — two separate tumblers |
| **Index `[I]` (dsas[0])** | I-stream displacement, independent |
| **Index `[V]` (dsas[1])** | V-stream displacement, independent |
| **`setwispnd` min** | `lockmin` iterates both slots separately — finds independent minimum per axis |
| **`setwispnd` add/sub** | `dspadd`/`dspsub` via `lockadd`/`locksubtract` — both axes shifted together by their respective per-axis minima |
| **Coupling** | None — the min for I doesn't affect V and vice versa; `lockmin` at `wisp.c:284` processes each tumbler slot in its own comparison |

The displacement is **two coupled scalars stored together, not a single combined value**. `setwispnd` computes a per-axis minimum independently across children, then adjusts the father's `cdsp` and each child's `cdsp` by that per-axis minimum. There is no cross-dimension coupling: the minimum I displacement does not influence the V adjustment, and vice versa.

---

## Question 16 [gregory]

> What is the precise boundary condition for the ONMYRIGHTBORDER case in `whereoncrum` — does it require exact equality between the query point and the crum's reach (displacement + width), and does it use `tumblereq` with full 16-digit comparison?

### Gregory's Answer

## KB Synthesis

The KB provides precise information on this, primarily from [SS-WHEREONCRUM] and [SS-INTERVAL-CMP].

## Boundary Condition for ONMYRIGHTBORDER

**Exact equality is required.** `whereoncrum()` at `retrie.c:345-372` computes:

```
left  = offset + cdsp        (grasp)
right = left + cwid           (reach)
```

Then classifies `address` against these values. ONMYRIGHTBORDER fires when `address == reach` — strict equality, not "within some epsilon."

The KB's formal statement from [SS-WHEREONCRUM]:

> `whereoncrum(crum, crum.reach) == OnRight`

And the concrete example:

```
whereoncrum(crum, v+1) → ONMYRIGHTBORDER (1)   ← NOT THRUME
```

## Does It Use `tumblereq` (Full 16-Digit Comparison)?

The KB doesn't quote the literal implementation of `whereoncrum`'s equality check. What it does specify:

- **`tumblereq`** (`tumble.c:24-36`): two tumblers are equal iff sign, exponent, and all 16 mantissa digits match — "no normalization ambiguity after `tumblerjustify`" [SS-TUMBLER Finding 0031]
- **`tumblercmp`** returning `EQUAL` (`tumble.c:72-85`): same criteria — sign then absolute value via `abscmp` which does lexicographic mantissa comparison [INV-TUMBLER-TOTAL-ORDER]

The five-way classification in [SS-INTERVAL-CMP] is built on `tumblercmp`, and `intervalcmp`/`whereoncrum` share the same structure. Both `tumblereq` and `tumblercmp == EQUAL` are functionally identical for non-degenerate tumblers — they both require sign, exponent, and all 16 mantissa digits to match.

**Practical consequence:** since `cwid > 0` is enforced by [INV-NO-ZERO-WIDTH-CRUM], the reach is always positive, avoiding the zero-tumbler special case in `tumblercmp`. The ONMYRIGHTBORDER check is therefore a full 16-digit field comparison regardless of which function is called internally.

## Why This Matters

From [ST-INSERT] / [SS-WHEREONCRUM]: when `INSERT at v+1` encounters a crum whose reach equals `v+1`, `makegappm()` exits early (no knife cut), and `isanextensionnd()` then checks `reach == new_origin` using this same equality. This is what enables coalescing (the `+0 crums` cost for sequential typing). Any representation difference between `reach` and `new_origin` — even in "trailing" mantissa digits — would break coalescing and force a split, increasing crum count unnecessarily.

**Summary:** ONMYRIGHTBORDER requires exact tumbler equality between the query point and `offset + cdsp + cwid`. The KB identifies the comparison as using the tumbler total order (effectively all 16 digits), but does not confirm whether the implementation calls `tumblereq` directly vs derives it from `tumblercmp == EQUAL`.

---

## Code Exploration

I now have everything needed to answer precisely. Here is the complete analysis:

---

## `ONMYRIGHTBORDER` in `whereoncrum`: Precise Boundary Condition

### The function — `retrie.c:345`

```c
INT whereoncrum(typecorecrum *ptr, typewid *offset, tumbler *address, INT index)
```

It classifies where `address` falls relative to the crum's interval. The interval is `[left, right)` — but the boundary cases make it half-open only at the logical level. The actual conditions are:

### SPAN/POOM path (lines 354–372)

**Right endpoint `right` is computed as:**
```c
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);  // left = offset + displacement
tumbleradd(&left, &ptr->cwid.dsas[index], &right);                 // right = left + width
```
`right` = offset displacement + crum displacement + crum width — the exclusive end of the crum's span.

**`ONMYRIGHTBORDER` is returned when** [`retrie.c:365–369`]:
```c
cmp = tumblercmp(address, &right);
if (cmp == LESS) {
    return(THRUME);
} else if (cmp == EQUAL) {
    return(ONMYRIGHTBORDER);   // ← exact equality
} else {
    return(TOMYRIGHT);
}
```

**Yes — it requires exact equality** between `address` and `right` (= displacement + width). Not `<=`, not "within epsilon" — precisely `tumblercmp(address, right) == EQUAL`.

### GRAN path (line 351–353)

```c
tumbleradd(&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
return(intervalcmp(&offset->dsas[WIDTH], &right, address));
```

`intervalcmp` at `tumble.c:144–160` applies the same two-step `tumblercmp` logic — `ONMYRIGHTBORDER` iff `tumblercmp(address, right) == EQUAL`.

---

### Does it use `tumblereq`?

**No.** `whereoncrum` calls `tumblercmp` [`retrie.c:357, 365`], not `tumblereq`. These are different functions:

| Function | Definition | What it compares |
|----------|-----------|-----------------|
| `tumblereq` | `tumble.c:24` | All fields: `xvartumbler`, `varandnotfixed`, `sign`, `exp`, all 16 mantissa digits |
| `tumblercmp` | `tumble.c:72` | Numeric value only: handles zero specially, compares `sign`, `exp`, then all `NPLACES` mantissa digits via `abscmp` |

`tumblercmp` returns `EQUAL` (defined as `0` at `common.h:80`) when `abscmp` finds: same `exp`, then all `NPLACES=16` mantissa digits equal [`tumble.c:92–110`].

So while `tumblercmp` does not compare the `xvartumbler` or `varandnotfixed` fields (those are checked only by `tumblereq`), it **does** do a full 16-digit mantissa comparison when exponents match, iterating `for (i = NPLACES; i--;)` at `tumble.c:101`.

---

### Summary

1. **Boundary condition:** `ONMYRIGHTBORDER` is returned iff `address == right` exactly, where `right = offset.dsas[index] + crum.cdsp.dsas[index] + crum.cwid.dsas[index]` — i.e., `address` equals the crum's reach (displacement + width) precisely. One digit of difference returns `TOMYRIGHT`.

2. **Comparison function used:** `tumblercmp`, not `tumblereq`. The `EQUAL` result from `tumblercmp` requires: same sign, same exponent, and all 16 mantissa places equal (`NPLACES=16`, `common.h:53`).

3. **`tumblereq` is not used here.** It additionally compares `xvartumbler` and `varandnotfixed` — structural fields for variable tumbler support — which `tumblercmp` ignores. `tumblereq` appears in `tumblersub` and `strongsub`, not in the interval comparison path.

4. **The macro equivalents** (`intervalcmppart2` at `retrie.c:343`) are commented out in the live SPAN/POOM path but show the same intent — they were the precursors to the inlined code at lines 364–372, and produce identical results.

---

## Question 17 [gregory]

> When `recombinend` merges POOM bottom crums during rebalancing, under what conditions can two adjacent crums with contiguous V-ranges but non-contiguous I-ranges be merged — or does the merge only redistribute crums between siblings without combining their V→I mappings?

### Gregory's Answer

## KB Synthesis

Rebalancing via `recombinend` operates exclusively at the **B-tree structural level** and never combines the V→I content of bottom crums. The two merge mechanisms [ST-REBALANCE-2D] both transfer crum nodes as atomic units:

- **Full merge** (`eatbrossubtreend`): transfers all children from one sibling node to another, then frees the donor. The children moved are entire subtrees — each bottom crum's `{origin.dsas[V], origin.dsas[I], width.dsas[V], width.dsas[I]}` quad remains exactly as created.
- **Nephew stealing** (`takenephewnd`): moves individual child crums between siblings via `takeovernephewsnd`. Again, each bottom crum moves as an atomic unit.

The merge guard `ishouldbother` [INV-ENFILADE-OCCUPANCY] checks only whether `dest->numberofsons + src->numberofsons <= max_children(height, type)`. It is purely a node-count predicate — it has no visibility into the V or I content of those nodes.

So two adjacent bottom crums with contiguous V-ranges but non-contiguous I-ranges can absolutely end up under the same parent after rebalancing, but they remain two separate crums. Their V→I mappings are never inspected or fused by any rebalance code path.

The only mechanism that actually combines V→I content into a single crum is `isanextensionnd` during INSERT [ST-INSERT, Finding 0062]. That check requires:

1. Same `homedoc` as the existing crum
2. New content's I-address origin equals the existing crum's I-reach (i.e., I-space contiguity)
3. The existing crum's V-reach equals the insertion point (i.e., V-space contiguity, the ONMYRIGHTBORDER case)

All three must hold simultaneously. Two crums with non-contiguous I-ranges fail condition 2 — `isanextensionnd` returns FALSE, and they are never fused regardless of how they are arranged in the B-tree by rebalancing.

The consequence [SS-POOM-BOTTOM-CRUM, INV-IADDR-PROVENANCE]: each bottom crum's I-address range reflects the provenance of the content at insertion time. Transcluded content from different source documents, or content inserted in non-contiguous I-address batches (e.g., after a CREATELINK [EC-GRAN-MB-ONE, Finding 0063 / INT-LINK-INSERT]), permanently occupies separate crums. Rebalancing can co-locate them under a common parent, but it cannot erase the I-space discontinuity between them.

---

## Code Exploration

I now have everything I need from the actual source. Here is the full answer:

---

## `recombinend`: POOM Crum Merging During Rebalancing

### Short Answer

**Two adjacent crums with contiguous V-ranges but non-contiguous I-ranges can be merged freely** — and vice versa. `recombinend` **never checks V→I range contiguity** as a precondition for merging. The only conditions that gate a merge are capacity and reservation status. What the merge operation actually does is **redistribute children (sub-crums) between siblings**, not combine the V→I mapping of two bottom crums into one.

---

### 1. Entry Point: `recombine` Dispatcher

`recombine.c:22-34` — both SPAN and POOM enfilades route through `recombinend`:

```c
case SPAN:
        recombinend (father);
        break;
case POOM:
        recombinend (father);
```

---

### 2. `recombinend` — The Rebalancing Loop

`recombine.c:104-131`:

```c
int recombinend(typecuc *father)
{
        if (father->height < 2  || !father->modified)   // [112]
                return(0);
        for (ptr = getleftson (father); ptr; ptr=(typecorecrum *)getrightbro (ptr)){
                recombinend (ptr);                       // [115] recurse down first
        }

        getorderedsons (father, sons);                   // [118] sort by diagonal
        n = father->numberofsons;
        for (i = 0; i < n-1; i++) {
                for (j = i+1; sons[i] && j < n; j++) {
                        if(i != j && sons[j] && ishouldbother(sons[i],sons[j])){  // [122]
                                takeovernephewsnd (&sons[i], &sons[j]);           // [123]
                        }
                }
        }
        if (father->isapex)
                levelpull (father);
}
```

**Key structural observation:** The function only acts on crums of `height >= 2`. Bottom crums (height 0) are never candidates for this merging loop — they are the *targets* of the children being redistributed. The comment in line 112 also gates on `modified`; an unmodified subtree is skipped entirely.

---

### 3. The Merge Gate: `ishouldbother`

`recombine.c:150-163` — this is the **complete and entire** decision function:

```c
bool ishouldbother(typecuc *dest, typecuc *src)
{
        ++noishouldbother;
        if(src->numberofsons == 0){
                if(src->sonorigin.diskblocknumber == DISKPTRNULL){
                        check(src);
                }else{
                        return(FALSE);   // [157] src is on disk only, skip
                }
        }
        if (dest->age == RESERVED || src->age == RESERVED)
                return (FALSE);          // [161] either crum is locked, skip
        return (dest->numberofsons + src->numberofsons <= (dest->height>1 ? MAXUCINLOAF : MAX2DBCINLOAF)
                && randomness(.3));      // [162]
}
```

The capacity constants (`enf.h:26-28`):
```c
#define MAXUCINLOAF      6   // max sons for interior crums
#define MAX2DBCINLOAF    4   // max sons for 2D bottom crums
```

**There is no V-range check. There is no I-range check. There is no `homedoc` check.** The sole structural condition is `numberofsons(dest) + numberofsons(src) <= capacity`.

The `randomness(.3)` call (`recombine.c:132-147`) is also permanently disabled — it unconditionally returns `TRUE`:

```c
bool randomness(float probability)
{
  static float i = 0;
  return(TRUE);    // [135] — actual logic commented out below
  /* i += probability; ... */
}
```

---

### 4. What Merging Actually Does: Children Are Redistributed, Not V→I Mappings Combined

The merge operations work at the **interior crum level**, moving child sub-crums from one parent into another. They never directly manipulate or combine the V→I mappings stored in bottom crums.

#### Full merge: `eatbrossubtreend` (`recombine.c:205-233`)

When `dest->numberofsons + src->numberofsons <= MAXUCINLOAF` (line 179), all of `bro`'s children are physically transplanted into `me`:

```c
makeroomonleftnd (me, &offset, &bro->cdsp, &grasp);  // [215] expand me's displacement envelope
fixdspsofbroschildren (me, bro);                      // [216] re-relativize bro's children's cdsp to me
getleftson(bro)->leftbroorfather = getrightmostbro(getleftson(me)); // [217] relink
getrightmostbro(getleftson(me))->rightbro = getleftson(bro);       // [218]
bro->leftson->isleftmost = FALSE;                                   // [219]

me->numberofsons += bro->numberofsons;  // [221]
...
disown (bro);
freecrum (bro);                         // [227-228] delete bro entirely
```

`fixdspsofbroschildren` (`recombine.c:259-268`) re-expresses each child's displacement relative to `me` rather than `bro`:

```c
for (nephew = getleftson (bro); nephew; nephew=(typecorecrum *)getrightbro(nephew)){
        dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, me->cenftype);  // abs = bro + rel
        dspsub (&nephew->cdsp, &me->cdsp,  &nephew->cdsp, me->cenftype);  // new_rel = abs - me
}
```

This is purely a coordinate re-expression — the V and I widths (`cwid.dsas[V]`, `cwid.dsas[I]`) of the children are unchanged. The children retain their individual V→I mappings intact.

#### Partial merge: `takeovernephewsnd` (`recombine.c:165-203`)

When combined count exceeds `MAXUCINLOAF`, children are adopted one at a time until `me` is full:

```c
getorderedsons (bro, sons);          // [184] sort bro's children diagonally
n = bro->numberofsons;
for (i = 0; i < n && roomformoresons(me); i++) {
        ptr = sons[i];
        takenephewnd (me, ptr);      // [189] move one child at a time
}
```

`takenephewnd` (`recombine.c:235-257`) moves a single nephew, re-relativizing its displacement:

```c
dspadd (&bro->cdsp, &nephew->cdsp, &nephew->cdsp, bro->cenftype); // [243] abs coords
adopt (nephew, RIGHTMOSTSON, me);                                   // [244]
prologuend (nephew, &bro->cdsp, &nephewsgrasp, NULL);              // [245]
makeroomonleftnd (me, &offset, &nephew->cdsp, &grasp);             // [247]
dspsub (&nephew->cdsp, &me->cdsp, &nephew->cdsp, me->cenftype);    // [248] me-relative
```

Again: nephew's `cwid` (its own V and I spans) is never touched. Only its `cdsp` origin is re-expressed.

---

### 5. Ordering for Merge Attempts: Diagonal Sort

`recombine.c:270-279` — `getorderedsons` sorts children by the **sum of both displacement dimensions**:

```c
tumbleradd(&v[i]->cdsp.dsas[0], &v[i]->cdsp.dsas[1], &tarray[i]);  // [298] I + V
```

This places crums in a diagonal order across the 2D space. Notably:
- This is used to **select which pairs to try merging** and **which children to adopt first** in `takeovernephewsnd`
- It is **not a contiguity test** — two crums that are diagonally close may have no contiguous range in either I or V dimension
- The commented-out `break` statements (`recombine.c:124-125`) show a former design where only the first successful merge per pass was performed; now **all pairs are tried**

---

### 6. Contrast: Where Contiguity IS Checked

The only place range contiguity is enforced is during **insertion**, in `isanextensionnd` (`insertnd.c:301-309`):

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
        if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
                return (FALSE);       // [305] homedoc must match
        prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
        return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));  // [308]
}
```

This checks **both** dimensions (`dspsize` for POOM = 2): `reach[I] == origin[I]` **and** `reach[V] == origin[V]`. Only when both dimensions are contiguous AND the `homedoc` matches will a new insertion extend an existing bottom crum rather than create a new one.

`insertnd.c:249-258` uses this: if `isanextensionnd` returns true, it widens the existing crum (`dspadd` on `cwid`); otherwise it creates a fresh crum. So **bottom crums in a POOM accumulate only strictly contiguous V×I ranges during insertion**.

---

### 7. The Critical Distinction

| Phase | V-range contiguity check | I-range contiguity check | `homedoc` check |
|---|---|---|---|
| **Insertion** (`insertnd.c:301`) | Yes — both dims via `lockeq` | Yes — both dims via `lockeq` | Yes — `tumblereq` |
| **Rebalancing** (`recombine.c:150`) | **No** | **No** | **No** |

This means:

- During insertion, each bottom crum accumulates only a strictly contiguous V×I rectangular region, with a single `homedoc` (source document identity).
- During rebalancing, `recombinend` **does not examine the ranges of bottom crums at all**. It only looks at the `numberofsons` count of interior crums when deciding whether to merge.

**The merge never combines two bottom crums into one.** It moves interior crums (which contain bottom crums as their children) between sibling interior crums. The bottom crums themselves — and their V→I mappings — remain untouched and un-merged. A bottom crum with a non-contiguous I-range relative to its neighbor will never have those ranges fused; the rebalancing is blind to that structure.

### 8. Summary

`recombinend` merges during rebalancing under exactly these conditions (`recombine.c:160-162`):

1. Neither crum is `RESERVED`
2. Their combined `numberofsons` fits within `MAXUCINLOAF` (6) or `MAX2DBCINLOAF` (4) depending on height

That is all. **V-range contiguity, I-range contiguity, and `homedoc` identity are all invisible to `recombinend`.** What it redistributes are interior crum nodes; their children (bottom crums) carry V→I mappings that were locked in at insertion time and are never re-examined or combined during rebalancing. Two bottom crums with contiguous V-ranges but non-contiguous I-ranges will never be fused — not because `recombinend` rejects the merge, but because `recombinend` never operates on bottom crums directly at all.

---

## Question 18 [gregory]

> If a bottom crum's V-displacement is stored as a relative offset from its parent, how is the absolute V-position reconstructed during retrieval — does the traversal accumulate displacements additively down the tree path, and does the same accumulation apply independently to the I-dimension?

### Gregory's Answer

## KB Synthesis

Yes to both parts. The accumulation is additive down the tree path, and it applies independently to each dimension.

## Traversal Accumulation

During retrieval, the tree traversal maintains a running `offset` parameter that accumulates ancestral displacements. At each node, `prologuend` computes the node's absolute grasp as:

```
grasp = offset + ptr->cdsp   (retrie.c:334-339)
```

That computed grasp becomes the new `offset` passed to the node's children. This is precisely the invariant captured in [INV-ENFILADE-RELATIVE-ADDRESSING]:

```
absolute_grasp(node) = absolute_grasp(parent) + node.cdsp
absolute_grasp(root) = root.cdsp
```

`setwispnd` maintains this by absorbing the minimum child displacement into the parent after each modification [SS-ENFILADE-TREE Finding 0066]:

1. Find `mindsp = min(children.cdsp)` across all children
2. `root.cdsp += mindsp` (parent absorbs the new minimum)
3. Each child: `child.cdsp -= mindsp` (children become relative to the new root)

## Both Dimensions, Independently

The POOM `cdsp` field is a multi-dimensional structure: `cdsp.dsas[V]` (SPANRANGE) and `cdsp.dsas[I]` (ORGLRANGE). The same additive accumulation occurs for each dimension in the `dsas` array independently and simultaneously [SS-POOM-BOTTOM-CRUM Finding 0076].

A POOM bottom crum stores both:
- `origin.dsas[V]` — V-address (typically 2 tumbler digits, e.g., `0.5`)
- `origin.dsas[I]` — I-address (typically 6–9 tumbler digits, e.g., `0.0.0.0.0.0.0.0.11`)

Both are relative offsets from their ancestors in their respective address spaces. Retrieval accumulates both independently along the same path.

## GRAN vs POOM Asymmetry

This relative-addressing scheme is **specific to 2D enfilades** (POOM and SPAN). The 1D GRAN enfilade uses a different scheme: root displacement is always zero, and `setwidseq` sums widths without displacement tracking [SS-ENFILADE-TREE Finding 0066]. For GRAN retrieval, no offset accumulation is needed — positions are absolute.

The `isemptyenfilade` function reflects this: for POOM/SPAN it checks both `cdsp = 0` AND `cwid = 0`; for GRAN it checks only `cwid = 0` [EC-EMPTY-DOC Finding 0066].

---

## Code Exploration

---

## How Absolute V-Position Is Reconstructed During Retrieval

### Data Layout

`wisp.h` defines both `typedsp` and `typewid` as the same struct:

```c
struct structwid {
    tumbler dsas[MAXLOXIZE];   /* MAXLOXIZE = 2 */
};
typedef struct structwid typewid;
typedef typewid typedsp;
```

For POOM (the 2D enfilade that maps V↔I), `wisp.h:18-21` defines the indices:

```c
#define I  0
#define V  1
```

And `DSPSIZEPM = 2`, `WIDSIZEPM = 2`. Every crum stores `cdsp` (displacement) and `cwid` (width) covering **both** I and V slots.

The comment block at `wisp.h:29-43` makes the storage model explicit:

```
**                    wid             dsp
**   gr:  |           WIDTH           WIDTH
**   sp:  |         ORGLRANGE         ORGLRANGE
**        |           SPANRANGE         SPANRANGE
**   pm:  |             I                     I
**        |               V                     V
```

And a critical note for GRAN: _"Note that dsp's of gr are not stored on crums themselves, but are discovered thru tree walking"_. For POOM/SPAN, dsps **are** stored on each crum.

---

### The Retrieval Entry Point

`retrie.c:33-54` — `retrieve()` initialises the accumulator to zero and dispatches:

```c
typecontext *retrieve(typecuc *fullcrumptr, tumbler *address, INT index)
{
  typedsp offset;
        clear (&offset, sizeof(typedsp));       // both dsas[I] and dsas[V] zeroed
        switch (fullcrumptr->cenftype) {
          case GRAN:
                return (findcbcseq ((typecorecrum*)fullcrumptr, &offset, address));
          case SPAN:
          case POOM:
                return (findcbcnd ((typecorecrum*)fullcrumptr, &offset, address, index));
```

---

### POOM/SPAN: Additive Accumulation via `findcbcnd` + `prologuend`

`retrie.c:208-227` — `findcbcnd()`:

```c
typecontext *findcbcnd(typecorecrum *father, typewid *offsetptr, tumbler *address, INT index)
{
        if ((cmp = whereoncrum (father, offsetptr, address, index)) < ONMYLEFTBORDER || cmp > THRUME)
                return (NULL);

        if (father->height != 0) {
                prologuend (father, offsetptr, &grasp, (typedsp*)NULL);   // accumulate
                for (ptr = findleftson ((typecuc*)father); ptr; ptr = getrightbro (ptr))
                        if (retr = findcbcnd (ptr, &grasp, address, index))   // recurse with new base
                                break;
        } else { /* FOUND IT! */
                retr = makecontextfromcbc ((typecbc*)father, offsetptr);
        }
        return (retr);
}
```

At each interior node the accumulator advances by one step via `prologuend`.

`retrie.c:334-339` — `prologuend()`:

```c
int prologuend(typecorecrum *ptr, typedsp *offset, typedsp *grasp, typedsp *reach)
{
        dspadd (offset, &ptr->cdsp, grasp, (INT)ptr->cenftype);   // grasp = offset + cdsp
        if (reach)
                dspadd (grasp, &ptr->cwid, reach, (INT)ptr->cenftype);
}
```

`wisp.c:15-18` — `dspadd()`:

```c
int dspadd(typedsp *a, typewisp *b, typedsp *c, INT enftype)
{
        lockadd (a->dsas, b->dsas, c->dsas, (unsigned)dspsize(enftype));
}
```

`wisp.c:269-273` — `lockadd()`:

```c
int lockadd(tumbler *lock1, tumbler *lock2, tumbler *lock3, unsigned loxize)
{
        while (loxize--)
                tumbleradd (lock1++, lock2++, lock3++);
}
```

For POOM, `dspsize(POOM) = DSPSIZEPM = 2` (`wisp.h:27`), so `lockadd` iterates **twice** — once for `dsas[I=0]`, once for `dsas[V=1]` — calling `tumbleradd` on each independently. Both I and V accumulators advance by exactly `crum->cdsp.dsas[I]` and `crum->cdsp.dsas[V]` at every level.

The `whereoncrum` check at `retrie.c:356-372` similarly reconstructs the absolute bound inline:

```c
case POOM:
    tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
    tumbleradd (&left, &ptr->cwid.dsas[index], &right);
```

`index` selects the dimension for the bounds test (V or I), but it is only a comparison — the underlying accumulation in `prologuend` always processes both.

---

### The Same Pattern in Area Retrieval

`retrie.c:252-265` — `findcbcinarea2d()` applies the identical accumulation for each qualifying interior node:

```c
if (crumptr->height != 0) {
        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);
} else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
```

---

### The Bottom Crum Adds Its Own `cdsp`

`context.c:151-174` — `makecontextfromcbc()` receives the *parent's* accumulated offset, then adds the leaf's own displacement:

```c
typecontext *makecontextfromcbc(typecbc *crumptr, typewid *offsetptr)
{
        ...
        movewisp(offsetptr, &context->totaloffset);          // copy parent accumulation
        movewisp(&crumptr->cwid, &context->contextwid);
        ...
        if (crumptr->cenftype != GRAN)
            dspadd(&context->totaloffset, &crumptr->cdsp,    // add leaf's own cdsp
                   &context->totaloffset, (INT)crumptr->cenftype);   // context.c:167
```

The `totaloffset` stored in the returned `typecontext` is therefore:

> **totaloffset = Σ(cdsp for every node on the root-to-leaf path)**

Both I and V slots accumulate via the same `dspadd` call — the leaf adds its own V-displacement in `dsas[V=1]` alongside its I-displacement in `dsas[I=0]`.

---

### GRAN Is Different

For granfilade (sequential text), no `cdsp` is stored on crums. `findcbcseq()` at `retrie.c:191-206` accumulates by summing sibling **widths** instead:

```c
for (; getrightbro (ptr); ptr = ptr->rightbro) {
        if (whereoncrum (ptr, offsetptr, address, WIDTH) <= THRUME)
                break;
        dspadd (offsetptr, &ptr->cwid, offsetptr, (INT)ptr->cenftype);  // add width, not cdsp
}
```

`dspsize(GRAN) = DSPSIZEGR = 1`, so only `dsas[WIDTH=0]` is touched. There is no V-dimension in GRAN.

---

### Summary

| Dimension | Mechanism | What accumulates |
|-----------|-----------|-----------------|
| POOM V (`dsas[1]`) | `prologuend → dspadd → lockadd` (loxize=2) | Each ancestor's `cdsp.dsas[V]` additively down root-to-leaf, then leaf's own `cdsp.dsas[V]` in `makecontextfromcbc` |
| POOM I (`dsas[0]`) | Same single `lockadd` call, first iteration | Each ancestor's `cdsp.dsas[I]` identically in parallel |
| GRAN WIDTH (`dsas[0]`) | `findcbcseq` sibling-width walk, loxize=1 | Sibling `cwid.dsas[WIDTH]` to the left; no stored `cdsp` |

**Both I and V are accumulated additively in lock-step by the same `lockadd` loop** — there is no separate pass for each dimension. The loop iterates `dspsize(POOM) = 2` times, hitting `dsas[0]` then `dsas[1]`, and each `tumbleradd` operates independently on its own tumbler. The final absolute V-position emerges in `context->totaloffset.dsas[V=1]` after all levels are visited.

---

## Question 19 [gregory]

> When a DELETE operation slices a bottom crum that maps a contiguous V-span to a contiguous I-span, does the surviving fragment preserve the exact I-displacement and I-width corresponding to the surviving V-range, or is there any rounding or alignment to tumbler boundaries?

### Gregory's Answer

## KB Synthesis

## DELETE Crum Slicing: I-Space Precision

The surviving fragment preserves the **exact** I-displacement and I-width with no rounding or alignment. Here is why:

**The linear 1:1 mapping within a crum**

A POOM bottom crum represents a linear V→I mapping: `poom(V_start + k) = I_start + k` for each byte offset `k` in `[0, width)`. This is guaranteed by [INV-SINGLE-CHAR-GRANULARITY] (one I-address per byte) and [SS-POOM-BOTTOM-CRUM]'s dual-origin structure.

**The slicing arithmetic**

When `slicecbcpm` is called (only when `whereoncrum == THRUME`, per [PRE-DELETE] Finding 0075), it computes:

```
localcut = tumblersub(cut, &grasp)   // V-space offset from crum start to cut
```

Because the V→I mapping is identity (offset `k` in V-space corresponds to offset `k` in I-space), `localcut` as an integer byte count simultaneously identifies the V-split and the I-split. The two resulting fragments are:

- **Left fragment**: V-span `[V_grasp, cut)`, I-span `[I_origin, I_origin + localcut)` — width = `localcut`
- **Right fragment**: V-span `[cut, V_reach)`, I-span `[I_origin + localcut, I_origin + cwid)` — width = `cwid - localcut` via `locksubtract` at `ndcuts.c:444`

**No representational ambiguity**

Both `localcut` and `cwid - localcut` are strictly positive (enforced structurally by the THRUME guard), per [INV-NO-ZERO-WIDTH-CRUM]. V-positions and I-positions in a text crum are both integer byte counts, so the arithmetic produces an exact representable integer with no fractional component.

[INV-WIDTH-VALUE-EQUIVALENCE] (Finding 0076) guarantees that V-width and I-width always encode the same numeric integer value, just at different tumbler exponents. When `slicecbcpm` re-encodes `localcut` for the I-dimension of the left fragment (using `tumblerlength(vsa)` as the precision anchor, per [SS-INSERT-VWIDTH-ENCODING]), the underlying integer is preserved exactly.

**Tumbler precision is not a constraint here**

The 16-digit mantissa limit [SS-TUMBLER] could theoretically be a concern, but byte-offset values within a single document's text span fit easily within this precision. The cut point within a crum is an integer in `[1, cwid-1]`, and these values are well within the representable range.

**Conclusion**: the cut is a clean integer partition of both the V-span and the I-span at the exact same byte offset. There is no sub-tumbler rounding.

---

## Code Exploration

I now have all the information needed. Here is the complete answer.

---

## Answer: I-Displacement and I-Width Preservation During Crum Slicing

**The surviving fragment preserves the exact I-displacement and I-width corresponding to the surviving V-range. There is no rounding or alignment to tumbler boundaries.**

Here is the full execution path and arithmetic proof.

---

### 1. Entry point: `dodeletevspan` → `deletevspanpm` → `deletend`

`dodeletevspan` [do1.c:158-167] calls `deletevspanpm` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

`deletend` [edit.c:31-76] places two knife blades at `origin` and `origin+width` on the V-axis, calls `makecutsnd` to split crums at those positions, then iterates over affected crums and either deletes them (`case 1`: fully inside the deleted span) or adjusts their V-displacement (`case 2`: survivors to the right, via `tumblersub`). Case 2 only touches `cdsp.dsas[index]` — **not** the I dimension [edit.c:63]:

```c
case 2:
    tumblersub(&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
    break;
```

The I-split happens earlier, inside `makecutsnd`.

---

### 2. Cutting: `makecutsnd` → `makecutsbackuptohere` → `slicecbcpm`

`makecutsnd` [ndcuts.c:15-31] drives `makecutsbackuptohere`, which at height == 0 (bottom crum level) does [ndcuts.c:77-91]:

```c
if (ptr->height == 0) {
    for (i = 0; i < knives->nblades; i++) {
        if (whereoncrum((typecorecrum*)ptr, offset, &knives->blades[i], knives->dimension) == THRUME) {
            new = (typecuc *)createcrum((INT)ptr->height, (INT)ptr->cenftype);
            ...
            slicecbcpm((typecorecrum*)ptr, offset, (typecorecrum*)new, &knives->blades[i], knives->dimension);
```

`THRUME` means "the knife passes through this crum's interior" — i.e., this is a crum that must be split.

---

### 3. The slice: `slicecbcpm` [ndcuts.c:373-450]

This is the key function. Walk through it step by step:

**Step A — Compute absolute V-start of the crum** [ndcuts.c:382]:
```c
prologuend(ptr, offset, &grasp, NULL);
// grasp.dsas[V] = offset->dsas[V] + ptr->cdsp.dsas[V]  (absolute V-origin)
// grasp.dsas[I] = offset->dsas[I] + ptr->cdsp.dsas[I]  (absolute I-origin)
```

**Step B — Compute `localcut`: the V-distance from the crum's left edge to the knife** [ndcuts.c:396]:
```c
tumblersub(cut, &grasp.dsas[index], &localcut);
// localcut = cut_V - crum_V_start
// = number of V-units from crum left-edge to the cut
// = V-width of the left fragment
```

**Step C — Precondition checks** [ndcuts.c:389-436]:

1. `lockis1story(ptr->cwid.dsas, widsize(enftype))` — all crum width dimensions must be 1-story (single non-zero mantissa digit). Confirmed for POOM: `WIDSIZEPM = 2` [wisp.h:27], both I and V widths checked.
2. `localcut.exp != ptr->cwid.dsas[index].exp` → fatal error. The knife falls within the crum's V-level.
3. `!is1story(&localcut)` → fatal error. The localcut is a simple single-level quantity.
4. `tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index])` → fatal error.

These guards ensure the cut arithmetic is unambiguous and exact.

**Step D — Compute left-fragment width `newwid`** [ndcuts.c:438-445]:

```c
movewisp(&ptr->cwid, &newwid);           // copy both V and I widths
for (i = 0; i < widsize(POOM)/*=2*/; i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];
    tumblerjustify(&newwid.dsas[i]);
}
```

`widsize(POOM) = WIDSIZEPM = 2` [wisp.h:27, wisp.h:60]. `I = 0`, `V = 1` [wisp.h:19-20].

After the loop:
- `newwid.dsas[V]`: `exp` = `ptr->cwid.dsas[V].exp` (preserved from `movewisp`), `mantissa[0]` = `localcut.mantissa[0]`
- `newwid.dsas[I]`: `exp` = `ptr->cwid.dsas[I].exp` (preserved from `movewisp`), `mantissa[0]` = `localcut.mantissa[0]`

`tumblerjustify` [tumble.c:289-313] is a no-op when `mantissa[0] != 0` (returns immediately at line 296). Since `localcut.mantissa[0]` is the character-count of the left fragment and is non-zero (otherwise there's no left fragment to slice), justify does nothing.

This is the line the author himself flagged: `/* I really don't understand this loop */` [ndcuts.c:439]. The loop is correct because both V and I widths of a standard POOM text crum have the **same mantissa value** (same character count), just potentially different exponents. Writing `localcut.mantissa[0]` into both dimensions — with their existing exponents preserved — is exact.

**Step E — Compute right-fragment width** [ndcuts.c:444]:

```c
locksubtract(&ptr->cwid, &newwid, &new->cwid, widsize(enftype));
```

`locksubtract` [wisp.c:275-279] calls `tumblersub` for each dimension. For the I-dimension:
```
new->cwid.dsas[I] = ptr->cwid.dsas[I] - newwid.dsas[I]
                  = total_I_width - left_I_width
                  = right_I_width (exact)
```

`tumblersub` [tumble.c:406-440] is exact subtraction. No rounding.

**Step F — Assign left-fragment width** [ndcuts.c:445]:
```c
movewisp(&newwid, &ptr->cwid);
// ptr->cwid.dsas[I] = localcut.mantissa[0] at ptr->cwid.dsas[I].exp  (exact left I-width)
// ptr->cwid.dsas[V] = localcut.mantissa[0] at ptr->cwid.dsas[V].exp  (exact left V-width)
```

**Step G — Compute right-fragment displacement** [ndcuts.c:446]:
```c
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype);
// new->cdsp.dsas[I] = ptr->cdsp.dsas[I] + ptr->cwid.dsas[I]
//                   = original_I_start + left_I_width
//                   = exact I-position of the cut (exact)
// new->cdsp.dsas[V] = original_V_start + left_V_width
//                   = cut_V (exact)
```

`dspadd` [wisp.c:15-18] calls `lockadd` [wisp.c:269-273] which calls `tumbleradd` per dimension. Exact addition, no rounding.

---

### 4. How crums are created: confirming the mantissa invariant

In `insertpm` [orglinks.c:75-133], a new POOM bottom crum is built with:

```c
movetumbler(&lstream, &crumorigin.dsas[I]);   // I-origin [line 105]
movetumbler(&lwidth,  &crumwidth.dsas[I]);    // I-width = lwidth [line 109]
movetumbler(vsaptr,   &crumorigin.dsas[V]);   // V-origin [line 113]
shift = tumblerlength(vsaptr) - 1;
inc   = tumblerintdiff(&lwidth, &zero);       // = lwidth.mantissa[0] = N chars
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);  // V-width = N at V's level [line 117]
```

So `crumwidth.dsas[I].mantissa[0] == crumwidth.dsas[V].mantissa[0] == N` (same character count), though their exponents may differ (`I.exp` is typically 0; `V.exp = -shift` where `shift = tumblerlength(vsaptr) - 1`).

The `slicecbcpm` loop propagates `localcut.mantissa[0]` (the character-count offset to the cut) into both dimensions, using each dimension's own preserved exponent. Because the exponents carry the level information separately, and the mantissa represents the count at that level, the split is exact in both V and I.

---

### 5. Summary

| Question | Answer |
|---|---|
| Does the right fragment's I-displacement equal exact original I-start + localcut? | **Yes** — `dspadd` at [ndcuts.c:446] |
| Does the right fragment's I-width equal exact original I-width − localcut? | **Yes** — `locksubtract` at [ndcuts.c:444] |
| Is there any rounding in `tumblerjustify`? | **No** — `tumblerjustify` is a no-op when `mantissa[0] != 0` [tumble.c:296] |
| Is there any alignment to tumbler boundaries? | **No** — all arithmetic (`tumblersub`, `tumbleradd`) is exact |
| Is this exact for arbitrary cut positions? | **Yes**, subject to preconditions: cut must be 1-story at the crum's V-level, and crum must be 1-story in all dimensions |

The surviving fragment — whether left or right — preserves the **exact I-displacement and I-width** corresponding to its surviving V-range. The implementation is purely exact tumbler arithmetic. The author's own confusion note (`/* I really don't understand this loop */` [ndcuts.c:439]) is the only rough edge: the loop is correct because the mantissa invariant (same character count in both dimensions) is established at insertion time and maintained by this exact split.
