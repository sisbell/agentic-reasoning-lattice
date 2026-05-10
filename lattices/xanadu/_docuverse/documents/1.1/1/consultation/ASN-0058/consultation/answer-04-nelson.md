## Question 4 [nelson]

> Under what conditions may two adjacent mapping units in a document be recognized as a single larger unit, and what must be true about their original content positions for this to be valid?

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
