## Question 2 [nelson]

> When a contiguous region is divided at a chosen point, must the two resulting pieces together account for exactly the original region with nothing lost and nothing duplicated?

## Yes — exact partition is a necessary consequence of the design

Nelson does not state this as an explicit axiom, but it follows inescapably from three structural properties he does specify.

### 1. Every element occupies exactly one position on the tumbler line

The tumbler line is a total order — a "flat mapping of a particular tree" where every element has a unique, determinate position:

> "The tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

No element occupies two positions. No position holds two elements.

### 2. Span content is fully determined by its boundaries

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. **There is no choice as to what lies between; this is implicit in the choice of first and last point.**" [LM 4/25]

A span includes *everything* between its endpoints. Nothing can hide between two points and fail to be covered. This rules out loss.

### 3. V-space is dense and gap-free

From the V-space specification, the virtual byte stream is always a contiguous sequence with no holes. INSERT shifts addresses; DELETE closes the gap:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

There are no empty positions in V-space. If a document has N bytes, every V-address from 1 through N is occupied.

### The REARRANGE operation confirms this structurally

Nelson's REARRANGE operation assumes exact partition at shared cut points:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3." [LM 4/67]

With three cuts, cut 2 is simultaneously the boundary of both regions — the first region ends where the second begins. There is no gap between them (nothing lost) and no overlap (nothing duplicated). Together they exhaust the range from cut 1 to cut 3.

The four-cut variant reinforces this by contrast: "With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." Here the region between cut 2 and cut 3 is explicitly *not* part of either transposed region — it stays in place. The fact that Nelson needs four cuts to leave a middle section undisturbed confirms that three cuts leave nothing undisturbed; the partition is exhaustive.

### Why duplication is impossible

Duplication would require a single element to appear in both resulting pieces. Since each element occupies exactly one position on the tumbler line, and a dividing point assigns each position to one side or the other, no element can appear on both sides. Nelson reinforces this with the span-set mechanism:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

A single span covers a contiguous region completely. Two adjacent spans sharing a boundary cover the union completely. The need for span-*sets* to handle non-contiguous selections confirms that individual spans are always contiguous and non-overlapping when used to partition.

### Summary

The partition property — dividing a contiguous region at a point yields two pieces that together account for exactly the original, with nothing lost and nothing duplicated — is not stated as a named axiom in Literary Machines. But it is a necessary consequence of: (a) unique positions on the tumbler line, (b) spans including everything between their endpoints with no discretion, and (c) dense, gap-free V-space addressing. The REARRANGE operation's three-cut semantics depend on this property being true.
