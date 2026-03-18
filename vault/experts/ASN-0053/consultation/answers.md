# Consultation Answers — Span Operations

**Inquiry:** What properties do contiguous regions of the tumbler space have? How do spans cover, intersect, split, and compose?
**Date:** 2026-03-18 16:28
**Questions:** 17 (8 nelson, 9 gregory)

---

## Question 1 [nelson]

> If two regions of content partially overlap, must the system always be able to identify the exact sub-region they share in common?

### Nelson's Answer

## Yes — and this is structural, not heuristic.

The system must always identify the exact shared sub-region when two content regions overlap, because overlap is defined by **shared I-space origin**, and every byte's I-address is permanently known.

### Why it works

Every byte in the docuverse has a permanent I-space address. When content appears in multiple documents (through transclusion via COPY, or through shared version ancestry via CREATENEWVERSION), those appearances share the same I-addresses. The V→I mapping (the POOM enfilade) can resolve any byte in any document to its permanent I-address. Comparing I-address sets between two regions yields the exact overlap — down to the individual byte.

Two operations make this explicit:

**SHOWRELATIONOF2VERSIONS** directly returns the shared sub-regions:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

**FINDDOCSCONTAINING** finds partial overlap across the entire docuverse:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

Note "any portion" — the system handles partial overlap, not just complete containment.

### The deeper guarantee

Nelson frames this as essential to the entire versioning system:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

The system doesn't approximate what's shared — it knows precisely, because correspondence is a structural relation derivable from I-addresses.

### The critical caveat

Overlap is defined by **provenance**, not by **value**. Two independently typed copies of identical text have different I-addresses and are NOT considered overlapping. Only content that shares I-space origin — through transclusion or version derivation — registers as shared.

This is by design. As noted in the content provenance materials: content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. This is how the system distinguishes "wrote the same words" from "quoted from the original."

So: if two regions share any I-space content at all, the system can always identify the exact sub-region they have in common — because that sub-region is simply the intersection of their I-address sets, and every byte's I-address is permanent and known.

---

## Question 2 [nelson]

> When a contiguous region is divided at a chosen point, must the two resulting pieces together account for exactly the original region with nothing lost and nothing duplicated?

### Nelson's Answer

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

---

## Question 3 [nelson]

> If two adjacent regions share a boundary, must the system guarantee they can be merged into a single contiguous region, and must that merged region be identical to one that was specified directly?

### Nelson's Answer

Yes. This follows from two properties Nelson explicitly specifies, though he never states the merge guarantee in those exact words.

## The Total Order Guarantee

The tumbler line is a total order — a depth-first linearization of the docuverse tree. A span is defined by two endpoints on this line, and its content is fully determined by those endpoints:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. **There is no choice as to what lies between; this is implicit in the choice of first and last point.**"
> — [LM 4/25]

This means a span [a, c] always designates the same content regardless of how you arrived at the endpoints a and c. The content is a function of the boundary, nothing else.

## The Normalization Guarantee

On page 4/37, Nelson explicitly addresses span-set reduction:

> "A spanset may be presented to the back end **with any degree of overlap** among the spans. This is because the system in effect performs a **boolean OR** to create a **normalized specset**, i.e. a **non-overlapping coverage of the same portion of tumbler-space**. Any overlapping specset can be reduced to a normalized specset."
> — [LM 4/37]

Two adjacent spans sharing a boundary point overlap at that single point. The boolean OR produces a single span covering the union. The normalization guarantee means the system treats {[a,b], [b,c]} and {[a,c]} as equivalent — they are the same "portion of tumbler-space."

## Why the Merge Is Identical to Direct Specification

Combining these two properties:

1. Two adjacent spans [a, b] and [b, c] share boundary b
2. Their boolean OR covers everything from a to c on the tumbler line
3. A single span [a, c] covers everything from a to c on the tumbler line
4. "There is no choice as to what lies between" — so both designate exactly the same content
5. The system normalizes them into the same non-overlapping coverage

The merged region **must** be identical to one specified directly, because spans are defined purely by their endpoints on a total order, and the content between any two endpoints is uniquely determined by the tree structure.

## A Subtlety: Future Content

Nelson notes that "a span that contains nothing today may at a later time contain a million documents" [LM 4/25]. This matters for the merge guarantee: the merged span [a, c] and the union of [a, b] ∪ [b, c] must remain identical even as new content is created between a and c. They do, because both are defined by the same endpoints on the same total order, and both include whatever the tree contains between those points at any moment.

## What Nelson Does NOT Address

Nelson does not discuss:
- Whether the **difference tumbler** representation of a merged span is always computable from the component difference tumblers (the arithmetic limitation on 4/39 — "there is no positive difference tumbler that will allow us to get BACK" — suggests some representations may require recalculation)
- Whether the normalization is performed eagerly or lazily
- The computational cost of normalization for large span-sets

The guarantee is semantic (the system treats them as equivalent) rather than a statement about representation efficiency.

---

## Question 4 [nelson]

> Can every collection of content positions be expressed as a finite set of contiguous regions, and must there be exactly one minimal such expression?

### Nelson's Answer

## Yes to both — with an important caveat about the second.

### Part 1: Every collection is expressible as a finite span-set

At any moment, the docuverse contains finitely many occupied positions on the tumbler line. Any collection of content positions is therefore a finite subset of a finite totally ordered set.

Nelson explicitly provides the mechanism:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

In the worst case (every target position separated by non-target content), each position gets its own unit span. This is always possible because:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse." [LM 4/24]

So yes — a finite span-set always suffices.

### Part 2: The minimal expression is unique

The tumbler line is a **total order** — a depth-first linearization of the docuverse tree:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line... the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

Given a target set S of content positions drawn from a finite total order, define two positions p, q in S as *contiguous in S* iff every **content** position between them on the tumbler line is also in S. Ghost elements — addressable positions with no stored content — do not break contiguity, because:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." [LM 4/23]

Ghosts carry no content, so including them in a span adds nothing and excludes nothing.

The contiguity relation partitions S into **maximal contiguous components** (runs). Each run yields exactly one span (from its minimum to its maximum element). No span can merge two distinct runs without including a non-target content position between them — which would violate "exactly, including nothing else." Therefore:

- The number of spans equals the number of runs — this is the minimum possible.
- The endpoints of each span are forced (the extremes of each run).
- **The minimal span-set is unique.**

### The caveat: minimality is moment-dependent

Nelson warns:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

Because new positions can be **forked** into existence between existing ones:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." [LM 4/20]

A span-set that minimally covers a collection **today** may cease to be minimal — or even correct — **tomorrow**, if new content appears between the endpoints of one of its spans. A single span [A, B] covering target positions A and B might need splitting into [A, A] ∪ [B, B] after a non-target position C is created between them.

The minimal span-set exists and is unique **at any given instant**, but it is not stable across mutations of the address space.

### Summary

| Question | Answer |
|----------|--------|
| Can every collection be expressed as a finite span-set? | **Yes** — unit spans always work as a fallback |
| Is the minimal expression unique? | **Yes** — forced by the total order on the tumbler line |
| Is the minimal expression stable over time? | **No** — forking can split spans |

This has a practical implication for span algebra: canonical forms must either be recomputed after mutations, or the algebra must track the ambient population of the tumbler line at the time of construction.

---

## Question 5 [nelson]

> When one region completely contains another, must the system be able to express the remainder — the containing region with the contained region removed — as contiguous pieces?

### Nelson's Answer

# Span Remainder: Containment and Contiguous Pieces

## Short Answer

Yes — and it follows directly from the geometry of the tumbler line, not from any special operation. Removing a contained span from a containing span always produces **at most two contiguous spans**, expressible as a **span-set**. Nelson provides the mechanism for this but does not discuss the subtraction operation explicitly.

## Why the Remainder Is Always Contiguous Pieces

The tumbler line is linearly ordered:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." [LM 4/22]

Spans are contiguous ranges on this line:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

Given a containing span [A₁, A₂] and a contained span [B₁, B₂] where A₁ ≤ B₁ and B₂ ≤ A₂, the remainder is:

```
[A₁ ... B₁)  ∪  (B₂ ... A₂]
    left            right
```

Each piece is itself a contiguous range on the tumbler line — a valid span. This is an inherent property of removing a contiguous sub-range from a contiguous range on any linearly ordered set. No special mechanism is needed; the linear ordering guarantees it.

## Nelson Provides the Mechanism

For expressing the two-piece remainder, Nelson specifies **span-sets**:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

And he expects front-ends to perform this kind of manipulation:

> "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." [LM 4/37]

> "Understanding spans is a key to appropriate software design for handling request-sets." [LM 4/37]

The endset mechanism confirms that non-contiguous regions are first-class:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

## What Nelson Does Not Say

Nelson does not explicitly define a "span subtraction" operation, nor does he discuss the remainder problem as such. The FEBE protocol includes no `SUBTRACT_SPANS` command. He expects the front end to handle span manipulation, but the specific algebra is left to implementors.

There is also an arithmetic limitation worth noting:

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." [LM 4/25]

This means computing the exact boundary tumblers for the remainder pieces may have constraints — you can reach addresses "after" a given point, but not arbitrary addresses through tumbler arithmetic alone. The subtraction is conceptually clean but its arithmetic realization requires care.

## Summary

| Aspect | Status |
|--------|--------|
| Can the remainder be expressed as contiguous pieces? | **Yes, always** — at most two spans (inherent in linear ordering) |
| Does the system provide a mechanism? | **Yes** — span-sets |
| Does Nelson specify span subtraction? | **No** — left to front-end implementation |
| Are there arithmetic complications? | **Yes** — tumbler arithmetic only reaches "notationally after" addresses |

The guarantee you're asking about is a **structural consequence** of the tumbler line being linearly ordered, combined with the span-set mechanism for non-contiguous selections. It doesn't need to be stated as a separate requirement — it falls out of the design.

---

## Question 6 [nelson]

> If a set of contiguous regions collectively covers a larger contiguous region without gaps, must the system guarantee that this complete-coverage property is verifiable?

### Nelson's Answer

## Complete Coverage Verifiability

The question touches on the internal correctness of the system, not on a user-facing guarantee. Let me be precise about what I designed and why.

### The V-Stream Is Always Complete

The virtual byte stream of a document is, by definition, contiguous and gap-free. V-addresses "always form a contiguous sequence starting at 1" — if you have 100 bytes, you have addresses 1 through 100. There are no holes. This is not a property that needs to be "verified" at the user level; it is what a V-stream IS.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The V-stream is composed of native spans and inclusions (transclusions). Together, these MUST cover the entire V-stream without gaps or overlaps — otherwise the V-stream would not be contiguous, which would contradict its definition.

### Coverage Is Maintained by Construction, Not by Verification

This is the implementor's problem, not the user's concern. The enfilade data structures — specifically what we called the POOM enfilade (the "eye in the pyramid") — maintain the V→I mapping such that every V-position resolves to exactly one I-position. The data structure's invariants guarantee coverage:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The FEBE editing operations (INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND) are defined to preserve V-stream contiguity. INSERT shifts following addresses. DELETE closes the gap. REARRANGE transposes regions. None of these can produce gaps, because:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

### What the User Sees

The user's guarantee is simpler and more powerful than "coverage is verifiable":

> **"THE PART YOU WANT COMES WHEN YOU ASK FOR IT."** [LM 2/16]

When you request content via RETRIEVEV, you get the material. When you request RETRIEVEDOCVSPAN, you get "a span determining the origin and extent of the V-stream" [LM 4/68]. When you request RETRIEVEDOCVSPANSET, you get "a span-set indicating both the number of characters of text and the number of links" [LM 4/68].

The system knows the total extent and composition. The user need not verify coverage — the system's job is to deliver complete, correct content.

### Where Coverage Matters Semantically

There are two places where coverage analysis becomes semantically meaningful at the user level:

**1. Version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. For this to be useful, the corresponding pairs must account for all shared content. But the operation returns the correspondence — the user receives the result, not a proof of its completeness.

**2. Royalty accounting.** When a compound document is read, "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. This requires the system to partition the V-stream into native vs. transcluded spans — a coverage decomposition. But again, this is internal bookkeeping, not a user-facing verification.

### The Direct Answer

No, the system need not expose "complete-coverage verifiability" as a user guarantee. The system must MAINTAIN coverage internally — the V-stream is always complete by construction, the enfilade invariants preserve this through edits, and the FEBE operations are defined to never produce gaps. But this is a correctness property of the implementation, not a promise the user needs to check.

The user's promise is: ask for content, receive all of it. The internals that make this work — including the span coverage invariant — are, as I put it:

> "None of these commands are to be seen by the user. The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

The coverage invariant is real and essential. But it lives in the machinery, not in the contract.

---

## Question 7 [nelson]

> Must two regions that share no positions in common be guaranteed to produce an empty result when intersected, and must this emptiness be distinguishable from a region of zero width?

### Nelson's Answer

# Intersection of Disjoint Regions and the Distinction from Zero Width

## The Short Answer

Yes to both. These are categorically different things in Xanadu's architecture, and confusing them would break the system.

## Disjoint Spans Must Produce Empty Results

The link search mechanism depends on this absolutely. When you search for links, the system checks whether a link's endset spans *overlap* with the search criteria:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

If two non-overlapping address ranges could somehow produce a non-empty intersection, the entire link search mechanism would return false matches. The guarantee that:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

...depends on overlap detection being correct. A link whose from-set is in one region of tumbler-space and whose search criterion covers a completely disjoint region must *not* satisfy the request.

The tumbler line provides the ordering that makes this deterministic:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

Two subtrees either share nodes or they don't. If they don't share nodes, their intersection is empty — no spans, no addresses, nothing.

## Emptiness Is Not Zero Width

A zero-width span (a span designating a single element) is a *valid reference to a specific thing*. An empty result is *no reference at all*. These serve entirely different purposes:

**A single-element span** addresses one specific byte, one specific link, one specific document. It has a real tumbler address. You can link to it. You can retrieve it. You can search for it.

**An empty span-set** (no spans whatsoever) is the answer to "what do these disjoint regions share?" — which is: nothing. There is no address to link to, no content to retrieve, no position to reference.

The ghost elements principle reinforces this distinction:

> "Things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements.'" [LM 4/23]

A zero-width span pointing to a ghost element is *still a valid reference* — "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them" [LM 4/23]. The address exists; it simply happens to have no stored content at the moment.

An empty intersection result has *no address at all*. It is not pointing to a ghost element — it is pointing to nothing.

## Why This Matters: The Span-That-Contains-Nothing

I was very deliberate about this distinction:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

A span over an unpopulated region of tumbler-space is *not empty* — it is a valid address range that happens to have no stored elements yet. It designates a zone of the docuverse. Content can appear there later.

This gives us three distinct states, not two:

| State | Meaning | Can you link to it? |
|-------|---------|-------------------|
| **Non-empty span** | Contains stored elements | Yes |
| **Span over unpopulated space** | Valid address range, no stored elements (yet) | Yes — ghost elements |
| **Empty result (no spans)** | No address range at all | No — nothing to reference |

Collapsing the last two would mean you could not distinguish "these regions don't overlap at all" from "these regions overlap at an unpopulated address." That distinction is essential for the link search mechanism and for the ghost element principle.

## The Design Principle

The spans are address ranges on the tumbler line. The tumbler line is a flat mapping of the docuverse tree:

> "The tumbler line is an abstract representation of a particular tree... finite but unlimited." [LM 4/22]

Intersection on this line is well-defined by the ordering of tumblers. Two ranges either share positions or they do not. If they share a single position, the intersection is a zero-width span at that position. If they share no positions, the result is the empty set — categorically different from any span, however narrow.

This is not a detail I left to implementors. It falls out necessarily from the nature of tumbler-space as an ordered line where spans designate contiguous ranges. The system would not work if these were conflated.

---

NEED_RAW: [4/32-4/39] — The curated sources cover the key quotes from these pages about request sets and span manipulation, but there may be additional detail about span operations and their algebra that would further illuminate the intersection question.

---

## Question 8 [nelson]

> When multiple overlapping regions are combined, must the result be independent of the order in which they are combined — that is, must region combination be associative and commutative?

### Nelson's Answer

## Region Combination: Associativity and Commutativity

Nelson does not explicitly state algebraic properties like associativity or commutativity for combining spans or span-sets. However, the design strongly implies both, because spans and span-sets are set-theoretic constructs over a totally ordered space.

### What Nelson Specifies

Spans designate **sets of bytes** on the tumbler line — a totally ordered sequence:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

Span-sets are collections of spans used for non-contiguous selections:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

Endsets are span-sets, and the link search model treats them as unordered disjunctions:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This "AND of the ORs" model is inherently order-independent — which span satisfies the request doesn't depend on how the spans are listed.

### Why the Design Implies Both Properties

1. **Spans are intervals on a total order.** The tumbler line is totally ordered (depth-first tree traversal). Combining intervals on a total order is set union, which is commutative (A ∪ B = B ∪ A) and associative ((A ∪ B) ∪ C = A ∪ (B ∪ C)).

2. **Span-sets designate byte collections.** The semantics are purely extensional — a span-set designates a set of bytes. Two span-sets that cover the same bytes are equivalent regardless of how they decompose into individual spans.

3. **Request sets are manipulated as sets.** Nelson says "The manipulation of request sets is an important aspect of what front-end functions do" [LM 4/37] and "Understanding spans is a key to appropriate software design for handling request-sets" [LM 4/37]. The operations are set operations on byte collections.

4. **No ordering semantics for span combination.** Nelson never distinguishes "A combined with B" from "B combined with A." Spans within an endset have no specified ordering that affects semantics.

### The One Caveat

Nelson describes span-sets as "a series of spans" [LM 4/25], which could suggest ordered representation. But the *semantics* are set-theoretic — what matters is which bytes are designated, not the order of the series. The representation may be ordered (for efficiency in the tumbler line), but the denotation is a set.

### My Assessment

**Yes, region combination must be order-independent** — both associative and commutative. This is not because Nelson states it explicitly, but because it follows necessarily from the set-theoretic semantics of spans over a totally ordered address space. Any implementation where the order of combination affected the result would violate the fundamental guarantee that span-sets designate byte collections.

Nelson's silence on this point is telling: he likely considered it obvious from the mathematical structure. Spans are ranges on a line; combining ranges is set union; set union has these properties by definition.

NEED_RAW: 4/32-4/39 (pages 199-206) — these cover span manipulation in detail and may contain explicit statements about algebraic properties of span operations that the curated summaries omit.

---

## Question 9 [gregory]

> When two spans are adjacent in tumbler space (the end of one equals the start of the next), under what conditions can they be merged into a single span, and when does the exponent difference between their width tumblers prevent merging?

### Gregory's Answer

## KB Synthesis

## Span Merging: Conditions and Exponent Constraints

### When Spans Can Be Merged

The POOM uses `isanextensionnd` as the merging gate [ST-INSERT, Finding 0062]. Two adjacent spans coalesce into one crum when **both** conditions hold:

1. **Same provenance** — the `homedoc` field on both sides matches (I-address origin document is identical)
2. **Exact boundary equality** — `reach(span1) == origin(span2)` as raw tumblers in both V and I dimensions, where `reach = tumbleradd(start, width)`

Sequential insertions within a single subspace naturally satisfy this. Each new character's origin equals the previous crum's reach, so typing "ABCDE" one character at a time still produces a single consolidated crum after the first-insert split [INV-VSPAN-CONSOLIDATION]. The `ONMYRIGHTBORDER` classification from `whereoncrum` [SS-WHEREONCRUM] bypasses knife-cutting entirely when the insertion point equals a crum's reach, routing directly to the extension check.

### When Exponent Difference Prevents Merging

**The fundamental constraint** comes from `strongsub` [SS-TUMBLER, Finding 0055]:

```
strongsub(a, b) : b.exp < a.exp  ==>  returns a unchanged
```

This is not just a DELETE artefact — it defines which tumbler pairs can participate in arithmetic. Specifically:

**Cross-subspace adjacency is arithmetically impossible.** Text-subspace V-addresses (1.x, exp = −1 per [SS-INSERT-VWIDTH-ENCODING]) produce widths at exp = −1. Link-subspace V-addresses (2.x, exp = 0) occupy a different exponent domain. When `tumbleradd(1.x_address, width_exp=-1)` is computed, the result stays within the exp = −1 domain — it can never produce a tumbler that `tumblereq`-equals `2.1` (exp = 0). The boundary at `2.1` is unreachable by addition from below using fractional widths.

This asymmetry is confirmed in two places:
- **INSERT isolation** [SS-TWO-BLADE-KNIFE, FC-SUBSPACE Finding 0054]: `findaddressofsecondcutforinsert` places `blade[1]` at `(N+1).1` — a deliberate structural guard ensuring shifts stay within the `N.x` subspace
- **DELETE isolation** [FC-SUBSPACE Finding 0055]: `strongsub(2.1, width_exp=-1)` returns `2.1` unchanged — an *incidental* arithmetic guard, not intentional design

**The practical consequence for merging:** A span ending at the top of the text subspace (reach approaching `2.0` in exp = −1 representation) and a span starting at `2.1` (exp = 0) can never satisfy `tumblereq(reach, origin)` — even if their numeric values were adjacent — because the exponent mismatch makes them distinct tumblers. The same applies to the 2.x/3.x boundary.

**Within a single subspace**, exponent consistency is maintained by [SS-INSERT-VWIDTH-ENCODING]: V-width exponent is computed as `-(tumblerlength(vsaptr) - 1)`, so all V-addresses of the same digit length get same-exponent widths. Sequential insertions at 1.x (all 2-digit V-addresses, exp = −1) produce widths all at exp = −1, making `tumbleradd(start, width)` produce reaches in the same exponent domain as subsequent origins — enabling exact tumbler equality and successful merging.

### Summary Table

| Scenario | Merge possible? | Reason |
|---|---|---|
| Sequential text insertions at 1.x | Yes | Same exponent domain; reach equals next origin exactly [ST-INSERT] |
| Sequential link insertions at 2.x | Yes | Same exponent domain [SS-LINK-SUBSPACE] |
| Text span (1.x) adjacent to link span (2.x) | No | Exponent gap; `strongsub` guard prevents cross-domain arithmetic [FC-SUBSPACE] |
| Different `homedoc` (e.g., two transclusions) | No | `isanextensionnd` homedoc check fails [ST-INSERT] |
| CREATELINK between two text insertions | No | Link orgl allocation advances I-address counter, breaking I-space contiguity [ST-CRUM-BOUND, Finding 0063] |

---

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Span Merging in Tumbler Space: When Exponent Differences Block the Merge

### The Two Merge Sites

There are exactly two active code paths that test whether two adjacent spans can be merged:

**1. `isanextensionnd` — merge at the enfilade level** (`insertnd.c:301–309`)

Called from `insertcbcnd` (`insertnd.c:242–275`) before creating a new bottom crum. If an existing crum's *reach* exactly equals the new insertion *origin*, the new span's width is simply added to the existing crum rather than creating a new crum:

```c
bool isanextensionnd(typecbc *ptr, typedsp *offsetptr, typedsp *originptr, type2dbottomcruminfo *infoptr)
{
    typedsp grasp, reach;
    if (!tumblereq (&infoptr->homedoc, &((type2dcbc *)ptr)->c2dinfo.homedoc))
        return (FALSE);
    prologuend ((typecorecrum*)ptr, offsetptr, &grasp, &reach);
    return (lockeq (reach.dsas, originptr->dsas, (unsigned)dspsize(ptr->cenftype)));
}
```

`lockeq` (`wisp.c:261–267`) calls `tumblereq` per dimension. `tumblereq` (`tumble.c:24–36`) requires **field-for-field exact match**: same `xvartumbler`, `varandnotfixed`, `sign`, `exp`, and all 16 mantissa bytes.

**2. `putvspaninlist` — merge at the vspan-list level** (`orglinks.c:329–387`)

Called when assembling the output list of V-spans from retrieved contexts. It tests adjacency using `tumblercmp`:

```c
tumbleradd (&spanptr->stream, &spanptr->width, &newspanend);  // line 343
tumbleradd (&ptr->stream, &ptr->width, &oldspanend);          // line 344
spancmp = tumblercmp (&spanptr->stream, &oldspanend);         // line 345
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);   // merge
    return(0);
}
// ... and symmetrically:
spancmp = tumblercmp (&ptr->stream, &newspanend);             // line 351
if (!spancmp) {
    movetumbler (&spanptr->stream, &ptr->stream);
    tumbleradd (&spanptr->width, &ptr->width, &ptr->width);   // merge
    return(0);
}
```

There is also `cleanupvspanlist` (`orglinks.c:297–312`) using `tumblereq`, but it is inside `#ifdef UnDEFined` and is dead code.

---

### The Gate: `abscmp` Refuses Equality Across Different Exponents

`tumblercmp` (`tumble.c:72–85`) dispatches to `abscmp` for positive tumblers. The first thing `abscmp` does:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)   // tumble.c:87
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);      // tumble.c:93
        } else {
            return(GREATER);   // tumble.c:96
        }
    }
    // only if exps match: compare mantissa digit by digit
    ...
    return (EQUAL);
}
```

**If two tumblers have different `exp` fields, `abscmp` returns LESS or GREATER — never EQUAL — regardless of what the mantissa digits are.** This is the gating condition. Two spans are adjacent but unmergeable the moment their boundary tumblers carry different `exp` values.

---

### How `absadd` Determines the Endpoint's Exponent

The endpoint of a span is computed by `tumbleradd` → `functiontumbleradd` → `absadd` (`tumble.c:444–484`):

```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;                    // exps match: trivial
    ansmant[0] = amant[0] + bmant[0];
    i = j = 1;
} else if (aptr->exp > bptr->exp) {           // stream coarser than width
    answer.exp = aptr->exp;                    // endpoint takes stream's exp
    temp = aptr->exp - bptr->exp;
    while (i < temp) { ansmant[j++] = amant[i++]; }
    ansmant[j++] = amant[i++] + bmant[0];
    i = 1;
} else {                                       // width coarser than stream
    answer.exp = bptr->exp;                    // endpoint takes WIDTH's exp
    temp = bptr->exp - aptr->exp;
    while (i <= temp) { ansmant[j++] = bmant[i++]; }
}
while (j <= NPLACES - 1) { ansmant[j++] = bmant[i++]; }
```

The rule is simple: **`endpoint.exp = max(stream.exp, width.exp)`** (less negative wins, since `exp ≤ 0` always — enforced by `tumblercheck` at `tumble.c:174`).

Note also the asymmetry in case 3 (`b.exp > a.exp`): when the *width* is coarser than the *stream*, `absadd` copies only from `bptr` (the width), completely ignoring `aptr` (the stream). The endpoint equals the width itself. This is the lossy case and is rarely reached in normal document operations.

---

### How Width Exponents Are Created in `insertpm`

The V-dimension width for a POOM insertion is set in `orglinks.c:115–117`:

```c
shift = tumblerlength (vsaptr) - 1;
inc   = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```

`tumblerlength` (`tumble.c:259–262`) = `nstories - exp`. For a simple integer vsaptr (exp=0, nstories=1): `shift = 0`, so `width.exp = 0`. For a two-story vsaptr like `1.2` (exp=0, nstories=2): `shift = 1`, so `width.exp = -1`.

Because vsaptr.exp = 0 and width.exp = -shift ≤ 0, we always have `stream.exp ≥ width.exp`, landing in case 1 or case 2 of `absadd`. The resulting endpoint has `endpoint.exp = stream.exp`. Sequential insertions through `insertpm` are self-consistent: each endpoint becomes the next stream, with the same exp.

---

### When the Exponent Difference Actually Blocks Merging

The dangerous case arises from **cutting operations**. `findaddressofsecondcutforinsert` (`insertnd.c:174–183`) creates a sub-address one level finer than the insertion position:

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{
    tumblerclear (&zero);
    tumblerincrement (position, -1, 1, secondcut);     // rightshift = -1 !
    beheadtumbler (position, &intpart);
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart,&zero), secondcut);
    tumblerincrement (secondcut, 1, 1, secondcut);
}
```

The `tumblerincrement` with `rightshift = -1` produces `secondcut.exp = position.exp + 1` — a finer exponent. Called from `makegappm` (`insertnd.c:124–172`) every time the POOM must be split to make room for a new insertion. After a cut, crums within the split subtree carry cdsp/cwid tumblers at this finer resolution.

Scenario where two logically adjacent spans cannot merge:

1. Span A was inserted via `insertpm` at vsaptr `S` (exp=0) with width W (exp=0). Its endpoint in the POOM crum is at exp=0, mantissa=`[S[0]+W[0], ...]`.
2. An earlier deletion triggered `makegappm` / `findaddressofsecondcutforinsert`, creating a cut at a sub-address with `exp = -1`.
3. Span B's origin crum was placed at that sub-address, giving its stream `exp = -1`.
4. Endpoint of A has exp=0; stream of B has exp=−1. `abscmp` at `tumble.c:92–97` sees `0 ≠ -1` and returns GREATER — never EQUAL. Merge is blocked.

The same failure occurs in `isanextensionnd`'s `lockeq`/`tumblereq` check: the `exp` fields don't match, so the bit-level comparison fails at `tumble.c:31` (`if (a->exp != b->exp) return FALSE`), and no extension is granted.

---

### Summary

| Condition | Merge result |
|-----------|-------------|
| `stream1.exp == width1.exp == stream2.exp` | Merge succeeds (exps match, mantissas checked) |
| `stream1.exp > width1.exp` (normal POOM case) | `endpoint.exp = stream1.exp`; merge succeeds if `stream2.exp` matches |
| `width1.exp > stream1.exp` (rare) | `endpoint.exp = width1.exp`; stream is *ignored* by `absadd`; merge succeeds only if `stream2 == width1` |
| `endpoint.exp ≠ stream2.exp` (from cuts/splits) | **`abscmp` returns LESS or GREATER — never EQUAL — at `tumble.c:92–97`. Merge is unconditionally blocked.** |

The structural invariant is this: `abscmp` treats the `exp` field as the *magnitude class* of a tumbler. A tumbler with `exp = -1` lives in a strictly finer hierarchical stratum than one with `exp = 0`, and the two strata can never be equal by definition. This is semantically correct for Xanadu's hierarchical address space, but it means any operation that introduces crum addresses at a finer exp — principally the cut machinery in `findaddressofsecondcutforinsert` — creates span boundaries that are opaque to the adjacency test, preventing merging even when the spans are numerically contiguous.

---

## Question 10 [gregory]

> Is the intersection of two overlapping tumbler spans always representable as a single span, or can hierarchical boundary crossings produce a result that requires multiple spans?

### Gregory's Answer

## KB Synthesis

The intersection of two overlapping tumbler spans is **always representable as a single span** in the mathematical sense, but **hierarchical boundary crossings can make that single span semantically degenerate**, requiring callers to split it for correct content access.

## Why the Intersection Is Always a Single Span

Tumblers form a total order per [INV-TUMBLER-TOTAL-ORDER]: `tumblercmp` is total, antisymmetric, and transitive, with lexicographic digit comparison after exponent alignment. Because the ordering is total and dense, any two overlapping half-open intervals `[a, b)` and `[c, d)` have intersection `[max(a,c), min(b,d))` — a single contiguous interval with no gaps.

The five-way `intervalcmp` predicate ([SS-INTERVAL-CMP]) treats the interval as a simple convex set in this total order: TOMYLEFT, ONMYLEFTBORDER, THRUME, ONMYRIGHTBORDER, TOMYRIGHT. There is no concept of internal discontinuity at the level of the ordering relation itself.

Crucially, the `.0.` separators in docuverse addresses are **semantic convention, not structural enforcement** ([SS-TUMBLER] Finding 0001): "The zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." The address `1.1.0.2.0.5` and the address `1.1.0.3.0.1` are just two tumblers with a well-defined ordering relationship. Nothing in `tumblercmp` skips over `.0.` boundaries.

## Where Hierarchical Crossings Cause Practical Problems

While the intersection is mathematically one span, crossing a `.0.` boundary produces a span that is **semantically non-contiguous**. The critical case is the subspace boundary between `1.x` (text) and `2.x` (links):

- `RETRIEVEDOCVSPAN` returns a single bounding span like `1.1 for 1.2` for a document with both text and links — this span is mathematically valid but semantically degenerate, spanning two distinct content types with a semantic gap between them ([EC-VSPAN-MISLEADING-SIZE], [SS-VSPAN-VS-VSPANSET])
- When `compare_versions` receives a specset that includes the link subspace, the V-to-I conversion produces link orgl ISAs and permascroll addresses — address types in different spaces that will never intersect, causing the correspond.c loop to crash ([EC-COMPARE-VERSIONS-LINK-CRASH], [PRE-COMPARE-VERSIONS])
- `RETRIEVEDOCVSPANSET` exists precisely because a single bounding span is insufficient — it returns separate spans per subspace ([SS-VSPAN-VS-VSPANSET] Finding 0035)

The subspace isolation mechanism for INSERT ([SS-TWO-BLADE-KNIFE]) tells the same story from the other direction: `findaddressofsecondcutforinsert()` deliberately places the second knife blade at `(N+1).1` to keep shifts within one subspace. If the intersection of a shift region with the occupied space could naturally span subspaces, this explicit boundary would be unnecessary.

## Summary

| Property | Value |
|----------|-------|
| Mathematical intersection | Always a single span (total order, no gaps) |
| Span width computation | `tumblersub(min_end, max_start)` — well-defined |
| Hierarchical boundary crossings | Produce a single span that may be *semantically* degenerate |
| Caller responsibility | Must split at subspace boundaries before content access (per [SS-VSPAN-VS-VSPANSET], [PRE-COMPARE-VERSIONS]) |

The system's design acknowledges this by providing `RETRIEVEDOCVSPANSET` (returns multiple spans, one per subspace) alongside `RETRIEVEDOCVSPAN` (returns the raw bounding span), and by requiring that operations like `compare_versions` and `retrieve_contents` receive text-subspace-only specsets as a precondition.

---

## Code Exploration

Now I have all the source evidence I need. Let me compile the answer.

---

## Answer

**The intersection of two overlapping tumbler spans is always representable as a single span.** Hierarchical boundary crossings cannot fragment it into multiple spans. Here is the complete code-traced reasoning.

---

### 1. What a tumbler span is

A span is defined in `xanadu.h:65-71`:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid      itemid;
    tumbler stream;   /* start address */
    tumbler width;    /* extent */
} typespan;
```

A span represents the closed-half-open interval `[stream, stream+width)` in the **total order** on tumblers. The total order is defined by `tumblercmp` (`tumble.c:72-85`), which delegates to `abscmp` (`tumble.c:87-111`): lexicographic comparison of the `exp` field, then each mantissa digit in order. This is a strict total order over all tumblers regardless of how many "stories" they have.

---

### 2. The intersection function

The only function that computes the intersection of two individual spans is `spanintersection` in `correspond.c:210-265`:

```c
bool spanintersection(typespan *aptr, typespan *bptr, typespan *cptr)
{
  tumbler aend, bend;

    tumblerclear (&cptr->stream);
    tumblerclear (&cptr->width);
    tumbleradd (&bptr->stream, &bptr->width, &bend);
    if (tumblercmp (&aptr->stream, &bend) >= EQUAL)
        return (FALSE);                             /* A starts at or after B ends → no overlap */
    tumbleradd (&aptr->stream, &aptr->width, &aend);
    if (tumblercmp (&bptr->stream, &aend) >= EQUAL)
        return (FALSE);                             /* B starts at or after A ends → no overlap */
    switch (tumblercmp (&aptr->stream, &bptr->stream)) {
      case EQUAL:
        movetumbler (&aptr->stream, &cptr->stream);
        /* width = min(aend, bend) - stream */
        ...
      case GREATER:  /* astart > bstart */
        movetumbler (&aptr->stream, &cptr->stream);  /* intersection starts at A */
        /* width = min(aend, bend) - astart */
        ...
      case LESS:     /* astart < bstart */
        movetumbler (&bptr->stream, &cptr->stream);  /* intersection starts at B */
        /* width = min(aend, bend) - bstart */
        ...
    }
    return (TRUE);                                  /* always exactly ONE output span */
}
```

This function always writes into a **single** `cptr` and returns exactly `TRUE` (overlap) or `FALSE` (empty). There is no code path that creates a list or produces two disjoint spans. This is `correspond.c:210-265`.

---

### 3. Why the mathematics guarantees this

Two intervals `[A_start, A_end)` and `[B_start, B_end)` in any total order intersect as:

```
∅                          if A_end ≤ B_start or B_end ≤ A_start
[max(A_start, B_start),    otherwise
 min(A_end,   B_end))
```

This is a topological fact. Two contiguous intervals cannot intersect as a disconnected set in a total order. `spanintersection` implements exactly this formula:

- `cptr->stream = max(astart, bstart)` (the `switch` on `tumblercmp`)
- `cptr->width  = min(aend, bend) - max(astart, bstart)` (the inner `switch` on `tumblercmp(&aend, &bend)`)

---

### 4. The role of hierarchical structure

Tumblers are hierarchical: `1.2.3` has three levels, and in tumbler ordering `1.2 < 1.2.1 < 1.3` (because each level is compared lexicographically by `abscmp`, `tumble.c:99-108`). A span `[1.2, 1.3)` therefore contains `1.2.1`, `1.2.99`, `1.2.1.1`, etc. — the full sub-tree between those two addresses.

But this structure does **not** make the interval non-contiguous. The total order is still linear. Sub-addresses are simply between their parent addresses in the order. Crossing a "hierarchical boundary" (e.g., from within `1.*` to `2.*`) is just crossing one point in the total order: `2.0` itself. There is no gap or disconnection.

---

### 5. Where multiple spans actually arise

Multiple spans **do** arise, but not from the intersection of two individual spans. They arise from:

**V→I or I→V coordinate mapping.**  `permute` → `span2spanset` in `orglinks.c:404-453` calls `retrieverestricted` (`retrie.c:56-85`) to walk the POOM enfilade and collect all crums that overlap the query span. Each crum produces one context, and `context2span` (`context.c:176-212`) clips it to the query restriction. The results from all crums are collected into a `targspanset` list — potentially many spans.

```c
typespanset *permute(typetask *taskptr, typeorgl orgl, typespanset restrictionspanset, ...)
{
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(...);    /* may grow the list */
    }
}
```

`span2spanset` (`orglinks.c:425-454`) appends one span per context:

```c
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *) onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

So a single vspan query can return many non-contiguous ispans if the document content is fragmented across multiple POOM crums (i.e., has been cut, copied, or rearranged).

**Spanset intersection.** `intersectspansets` in `correspond.c:145-188` does produce multiple output spans, by iterating over all pairs:

```c
for (; set1; set1 = set1->next) {
    for (p = set2; p; p = p->next) {
        if (comparespans (taskptr, set1, p, set3, spantype))
            set3 = &(*set3)->next;        /* appends one span per overlapping pair */
    }
}
```

If set1 has M spans and set2 has N spans, the output can have up to M×N spans. But this is the intersection of two **spansets**, not two individual spans.

---

### 6. A subtle limitation in coordinate-space clipping

`context2span` (`context.c:194`) uses `tumblerintdiff` to compute offsets:

```c
tumblerincrement (&grasp.dsas[idx2], 0,
    (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
    &grasp.dsas[idx2]);
```

`tumblerintdiff` (`tumble.c:591-597`) returns only `c.mantissa[0]` — the first digit of the tumbler subtraction. If the clipping offset is a multi-story tumbler (e.g., the restriction span starts deep within a sub-address that is many levels removed from the crum origin), only the top digit is used. This is a precision limitation of the coordinate mapping, not of span intersection itself, and it affects V→I/I→V fidelity rather than the pure geometric intersection.

---

### Summary

| Question | Answer | Evidence |
|---|---|---|
| Is intersection of two single tumbler spans always one span? | **Yes** | `spanintersection`, `correspond.c:210-265` — always at most one output span |
| Can hierarchical boundaries fragment a span intersection? | **No** | `tumblercmp` defines a total order; two intervals in any total order intersect as 0 or 1 intervals |
| Where do multiple spans arise? | V→I/I→V mapping across POOM crums | `permute`, `orglinks.c:404-453`; `intersectspansets`, `correspond.c:145-188` |
| Are there known imprecisions in span computations? | Yes, in clipping | `context2span` uses `tumblerintdiff` returning only `mantissa[0]`, `context.c:194` |

The intersection of two overlapping tumbler spans is always exactly one span. The multi-span results that appear in practice arise from the POOM permutation mapping that converts between V-space and I-space, where content fragmentation across crum boundaries produces a set of non-contiguous output spans — but that is coordinate mapping, not geometric span intersection.

---

## Question 11 [gregory]

> Given that tumblers use `.0.` as a hierarchical separator by convention but not enforcement, does a span starting at `1.1` with width `0.5` cover position `1.3.0.1` — i.e., do spans enumerate all tumblers within the range regardless of hierarchical depth?

### Gregory's Answer

## KB Synthesis

## Spans Are Flat Numeric Intervals

**Yes, `1.3.0.1` falls within a span starting at `1.1` with width `0.5`** (reaching `1.6`). Span containment uses the tumbler total order, which is purely lexicographic — the `.0.` hierarchical separator convention has no effect on containment arithmetic.

### The Total Order

From [INV-TUMBLER-TOTAL-ORDER] and [SS-TUMBLER, Finding 0031]: `tumblercmp` compares tumblers by expanding to their fixed-precision mantissa representations. `1.1.0.2 < 1.1.0.2.0.1` because the shorter tumbler compares as having trailing zeros — which are less than the non-zero continuation. The comparison is purely positional on the digit sequence.

For the specific case:
- `1.1` → mantissa `[1, 1, 0, 0, ..., 0]`
- `1.3.0.1` → mantissa `[1, 3, 0, 1, 0, ..., 0]`
- `1.6` → mantissa `[1, 6, 0, 0, ..., 0]`

Digit-by-digit: position 1 differs. `1 < 3 < 6`, so `1.1 < 1.3.0.1 < 1.6`. The address falls strictly interior to the span (`THRUME` in [SS-INTERVAL-CMP] and [SS-WHEREONCRUM] terminology).

### The Mechanism

From [SS-INTERVAL-CMP]: `intervalcmp(left, right, address)` classifies membership using `tumblercmp` directly. No special handling exists for `.0.` boundaries — the function is unaware of address hierarchy. The half-open interval `[1.1, 1.6)` includes every tumbler `t` where `tumblercmp(1.1, t) != GREATER && tumblercmp(t, 1.6) == LESS`, regardless of how many `.0.` separators `t` contains.

From [SS-TUMBLER, Finding 0001]: "The document/element decomposition is a predicate over tumblers, not a structural subtype." The `.0.` hierarchy is a convention enforced by callers, not by the comparison machinery [PRE-SUBSPACE-CONVENTION].

### Practical Implications

In POOM queries ([SS-POOM-MULTIMAP]), `findcbcinarea2d` traverses the B-tree using this same total order. Any entry with a V-address in `[1.1, 1.6)` is returned — if `1.3.0.1` were stored as a V-address, it would be found.

In practice, text V-addresses within a document are allocated as `1.1, 1.2, 1.3, ...` (flat byte offsets via `tumblerincrement` with `rightshift=0`) [SS-ADDRESS-SPACE, Finding 0033], so hierarchically deep V-addresses don't typically arise in the text subspace. But for I-address spans (permascroll queries), this matters: a span `[2.1.0.5.0.100, width=10)` would capture `2.1.0.5.0.100.3.1` if such an address existed, because it falls numerically within the range.

The subspace boundary between text (`1.x`) and links (`2.x`) is also enforced through this total order: the two-blade knife in INSERT sets `blade[1] = 2.1` to exclude the link subspace from shift operations [SS-TWO-BLADE-KNIFE, FC-SUBSPACE] — which only works correctly because the total order places all `1.x` addresses below `2.1` and all `1.3.0.1`-style addresses in between.

---

## Code Exploration

Now I have everything I need. Let me trace through the full arithmetic.

---

## Answer

**Yes, the span `[start=1.1, width=0.5)` covers position `1.3.0.1`.** The backend uses flat mantissa comparison with no hierarchical semantics baked into the comparison logic. Here is the complete proof from the source.

---

### 1. The C Tumbler Structure

From `backend/common.h:53-65`:

```c
#define NPLACES 16
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

A tumbler is an exponent plus a 16-place array of non-negative digits. The `.` in `1.3.0.1` is **not stored** — only the integer digits are, laid out in `mantissa[0..3]`.

---

### 2. Protocol Parsing: How `1.3.0.1` Enters the C Backend

The Python client encodes `Tumbler(1,3,0,1)` on the wire as `0.1.3.0.1~` — the leading `0` is the count of leading zeros (the exponent), followed by each digit separated by `.` [`client.py:166-174`].

The FE parser `gettumbler` in `backend/get2fe.c:69-88`:

```c
bool gettumbler(typetask *taskptr, tumbler *tumblerptr)
{
    INT i, num, value;
    tumblerclear(tumblerptr);
    getnum(taskptr, &num);       // reads leading number: "0"
    tumblerptr->exp = -num;      // exp = 0
    for (i = 0; gettdigit(taskptr, &value); i++) {
        tumblerptr->mantissa[i] = value;
    }
    ...
}
```

`gettdigit` [`get2fe.c:90-99`] simply consumes a `.` then reads the next integer. For `0.1.3.0.1~`:

| mantissa slot | value |
|---|---|
| mantissa[0] | 1 |
| mantissa[1] | 3 |
| mantissa[2] | 0 |
| mantissa[3] | 1 |
| mantissa[4..15] | 0 |

Result: **`exp=0, mantissa=[1,3,0,1,0,…]`**

The `0` in position 2 is just a zero digit. It has no structural role in the comparison engine.

---

### 3. Computing the Span End: `1.1 + 0.5`

The start `1.1` (wire `0.1.1~`): `exp=0, mantissa=[1,1,0,…]`  
The width `0.5` (wire `1.5~`): `exp=-1, mantissa=[5,0,…]`

`functiontumbleradd` dispatches to `absadd` in `backend/tumble.c:444-484`:

```c
} else if (aptr->exp > bptr->exp) {   // 0 > -1: true
    answer.exp = aptr->exp;            // exp = 0
    temp = aptr->exp - bptr->exp;      // temp = 1
    while (i < temp) {
        ansmant[j++] = amant[i++];     // ansmant[0] = 1  (copies a's leading digit)
    }
    ansmant[j++] = amant[i++] + bmant[0];  // ansmant[1] = 1 + 5 = 6
    i = 1;
}
while (j <= NPLACES-1) {
    ansmant[j++] = bmant[i++];         // rest are zeros
}
```

Span end = **`exp=0, mantissa=[1,6,0,…]`** = `1.6`.

---

### 4. The Comparison: Does `1.3.0.1` fall in `[1.1, 1.6)`?

Span membership is determined by `intervalcmp` in `backend/tumble.c:144-160`:

```c
INT intervalcmp(tumbler *left, tumbler *right, tumbler *address)
{
    cmp = tumblercmp(address, left);
    if (cmp == LESS) return TOMYLEFT;
    else if (cmp == EQUAL) return ONMYLEFTBORDER;
    cmp = tumblercmp(address, right);
    if (cmp == LESS) return THRUME;        // inside
    else if (cmp == EQUAL) return ONMYRIGHTBORDER;
    else return TOMYRIGHT;
}
```

`tumblercmp` dispatches to `abscmp` for two positive tumblers [`tumble.c:87-111`]:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) { ... }
    else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {
            if (!(cmp = *a++ - *b++)) {}
            else if (cmp < 0) return LESS;
            else return GREATER;
        }
    }
    return EQUAL;
}
```

**Check 1: `address (1.3.0.1)` vs `left (1.1)`**

Both have `exp=0`. Compare mantissa left-to-right:
- `mantissa[0]`: `1 − 1 = 0` → equal, continue
- `mantissa[1]`: `3 − 1 = +2` → **GREATER**

`tumblercmp(address, left) = GREATER` → address is not to the left.

**Check 2: `address (1.3.0.1)` vs `right (1.6)`**

Both have `exp=0`. Compare mantissa:
- `mantissa[0]`: `1 − 1 = 0` → continue
- `mantissa[1]`: `3 − 6 = −3` → **LESS**

`tumblercmp(address, right) = LESS` → `intervalcmp` returns **`THRUME`** (inside the interval).

---

### 5. The Zero at `mantissa[2]` Is Irrelevant to Span Membership

The comparison terminates at position 1 — the `0` at `mantissa[2]` and `1` at `mantissa[3]` are never reached. They were already dominated by the `3 < 6` difference at position 1. Even if the comparison had reached `mantissa[2] = 0`, it would merely continue to the next slot. **There is no code path in `abscmp`, `intervalcmp`, or `whereoncrum` that treats a zero digit as a hierarchical fence.**

The comment in `common.h:53` confirms this is just convention:

```c
/* places in mantissa of tumbler - increased from 11 to support deeper version chains */
```

The only place `.0.` has semantic weight is in `tumbleraccounteq` [`tumble.c:38-70`], which is used for **account ownership testing**, not span membership.

---

### Verdict

**A span starting at `1.1` with width `0.5` covers `1.3.0.1`.** Spans enumerate all tumblers in the numeric half-open interval `[start, start+width)` using flat, left-to-right mantissa comparison. Hierarchical depth — the number of `.`-separated components — plays no role. Position `1.3.0.1` falls squarely in `[1.1, 1.6)` because `1.3 < 1.6` at the second mantissa slot, regardless of how many sub-components follow.

---

## Question 12 [gregory]

> When `strongsub` returns its input unchanged due to the exponent guard, what does that imply about the algebraic closure of span difference — can subtracting one span's width from another's start position fail to produce a meaningful displacement?

### Gregory's Answer

## KB Synthesis

The exponent guard in `strongsub` means span difference is **not algebraically closed** — the operation silently degenerates to identity rather than producing a displacement when operand exponents don't match.

Here's what the code actually does:

```c
// strongsub(a, b, c): computes c = a - b
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);  // c = a, unchanged
    return(0);
}
// otherwise, proceed with actual subtraction
```

So `strongsub(a, b)` returns `a` — not `a - b`, not zero, not an error — whenever `b.exp < a.exp`. [SS-TUMBLER Finding 0055]

**The algebraic consequence:** Span displacement is only meaningful within an exponent class. When you compute "shifted position = old_position - deletion_width", the subtraction is a genuine displacement only when `deletion_width.exp >= old_position.exp`. When the width lives at a lower exponent (finer granularity) than the position, the result is the original position, as if no deletion occurred.

This is exactly what happens with subspace isolation in DELETE [FC-SUBSPACE Finding 0055]:

- Text content at V-displacement `0.4` (exp=-1)
- Link content at V-displacement `2.1` (exp=0)  
- Deletion width `0.3` (exp=-1)

For text: `strongsub(0.4, 0.3)` — exponents match, subtraction proceeds, yields `0.1`. Meaningful displacement.

For links: `strongsub(2.1, 0.3)` — `0.3.exp(-1) < 2.1.exp(0)`, guard fires, returns `2.1`. Not a displacement — identity.

**The deeper problem:** This makes span algebra contextually valid only within a single exponent level. If you have a span at position `1.x` (exp=-1) and try to subtract a width computed in a different exponent class, the arithmetic silently does nothing rather than flagging a type mismatch. The system doesn't distinguish between "these operands are incompatible" and "the subtraction produced the original value." [INT-DELETE-SUBSPACE-ASYMMETRY]

Compare this to INSERT's approach [SS-TWO-BLADE-KNIFE Finding 0054]: INSERT explicitly computes a second knife blade at the subspace boundary `(N+1).1`, using structural geometry to exclude cross-subspace entries from the shift region before any arithmetic occurs. DELETE has no such guard — it relies on the arithmetic failing silently at the exponent boundary.

The practical implication for the spec: you cannot reason about `tumblersub(start, width)` producing a "displacement" without also knowing that `start.exp >= width.exp`. When this condition fails, the operation is a no-op that looks like success. Any formal model of DELETE's postcondition must be qualified: `entry.vpos' = entry.vpos - width` holds only when `entry.vpos.exp = width.exp`; otherwise `entry.vpos' = entry.vpos` [ST-DELETE Finding 0055].

The closure property you'd expect — that subtracting any valid width from any valid position yields the position minus that width — does not hold across the tumbler type. Span difference is a partial function whose domain is restricted to same-exponent operands.

---

## Code Exploration

Now I have everything I need. Here is the full analysis.

---

## `strongsub` Exponent Guard and Algebraic Closure of Span Difference

### The Exponent Guard — Exact Code

`strongsub` is defined at `backend/tumble.c:534`:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;
  register INT i, j;

    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {
        movetumbler (&answer, cptr);   // return zero
        return(0);
    }
    if (bptr->exp < aptr->exp) {        // <<< THE EXPONENT GUARD
        movetumbler(aptr,cptr);         // return aptr UNCHANGED
        return(0);
    }
    ...
```

The guard fires when `bptr->exp < aptr->exp` — i.e., when `b` is expressed at a **finer hierarchical depth level** than `a`. The result is that `cptr` receives `aptr`'s value unchanged. No error is raised. The subtraction silently does nothing.

---

### What `exp` Means

The tumbler struct is declared in `backend/common.h:59–65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT;
    short exp;
    tdigit mantissa[NPLACES];  // NPLACES == 16
} tumbler;
```

`tumblercheckptr` at `backend/tumble.c:174` treats `exp > 0` as invalid — so `exp` is always ≤ 0. `tumblerjustify` at `tumble.c:289–313` normalizes a tumbler by left-shifting leading zeros and decrementing `exp` accordingly. The effect: a more-negative `exp` means the first mantissa digit occupies a finer (deeper) hierarchical position in the address tree.

`tumblerlength` at `tumble.c:259–262` confirms this:

```c
INT tumblerlength(tumbler *tumblerptr) {
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

Since `exp ≤ 0`, length grows with more-negative `exp`.

---

### How the Guard Is Reached: `abscmp` Drives `strongsub`

`strongsub` is called only from `functiontumbleradd` at `tumble.c:384–386`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
```

`abscmp` at `tumble.c:87–111` checks `exp` **first**:

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);
        } else {
            return(GREATER);   // aptr->exp > bptr->exp => aptr is COARSER
        }
    } else {
        // compare mantissas digit by digit
    }
    return (EQUAL);
}
```

Because exp ≤ 0, "`aptr->exp > bptr->exp`" means `aptr` is at a **coarser** hierarchical level (less-negative exp). When `abscmp` returns `GREATER` based solely on the exponent comparison, it means `a` is defined at a coarser level than `b`. This is exactly when `strongsub` is called — and then at `tumble.c:544`, `bptr->exp < aptr->exp` is true, so the guard fires immediately.

**The exponent guard is the direct consequence of `abscmp`'s exponent-first ordering.** They are two halves of the same implicit assumption: when `a` is coarser-grained than `b`, the system considers `a > b` in magnitude, calls `strongsub`, and `strongsub` immediately bails out by returning `a`.

---

### What `strongsub` Actually Computes (When the Guard Doesn't Fire)

When `aptr->exp == bptr->exp`, the guard does not fire and `strongsub` proceeds at `tumble.c:548–564`:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    if (i >= NPLACES) {
        movetumbler (&answer, cptr);
        return(0);
    }
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
if (++i >= NPLACES) { ... }
for (j = 1; j < NPLACES && i < NPLACES;)
    answer.mantissa[j++] = aptr->mantissa[i++];
```

This is **not arithmetic subtraction**. It is a hierarchical displacement computation: skip the common prefix (counting down `exp` for each matching level), then subtract the first diverging digit, then copy the remaining tail of `a`. It produces the address of `a` relative to `b` within their shared sub-tree. This operation is meaningful only when both tumblers are at the same hierarchical depth (same `exp`).

---

### `tumblersub` and the Span Difference Path

`tumblersub` at `tumble.c:406–440` is the entry point for span differences:

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    if (iszerotumbler (bptr))
        movetumbler (aptr, cptr);
    else if (tumblereq (aptr, bptr))
        tumblerclear (cptr);
    else if (iszerotumbler (aptr)) {
        movetumbler (bptr, cptr);
        cptr->sign = !cptr->sign;
    } else {
        movetumbler (bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd (aptr, &temp, cptr);   // dispatches to strongsub or weaksub
    }
    tumblerjustify (cptr);
}
```

For span operations, `orglinks.c:377` and `orglinks.c:381` call `tumblersub` to compute widths from end-points:

```c
// orglinks.c:377
tumblersub(&oldspanend, &spanptr->stream, &ptr->width);
// orglinks.c:381
tumblersub(&newspanend, &ptr->stream, &ptr->width);
```

These compute `end - start = width`. If `end` and `start` are at the same depth, `exp` values match, `abscmp` compares mantissas, and when `end > start`, `strongsub` correctly computes the displacement.

---

### When Span Difference Fails to Produce a Meaningful Displacement

Consider subtracting **a span's width** from **another span's start position** — the conceptual operation of "position B.width units before A.start":

```
result = tumblersub(A.start, B.width, result)
```

This flows into `tumbleradd(A.start, -B.width, result)`. The dispatch in `functiontumbleradd` calls `abscmp`:

- If `A.start.exp > B.width.exp` (A.start is at a coarser hierarchical level than B.width) → `abscmp` returns `GREATER` → `strongsub(A.start, B.width, result)` is called → **exponent guard fires** → result = A.start unchanged.

The width had no effect. The displacement was not computed.

**This is a silent failure.** The function returns `0` (success), `cptr` contains `aptr`'s value, and no error path is taken.

---

### The Algebraic Implication

The exponent guard reveals that **tumbler subtraction is not closed over the set of all valid tumblers at different hierarchical depths**. Specifically:

1. **No additive inverse at cross-depth.** For tumblers `a` (coarser) and `b` (finer), `a - b` does not yield a value `d` such that `b + d = a`. Instead it yields `a`, breaking the expected displacement relationship.

2. **The "subtraction" is really a same-level operation only.** `strongsub` is a relative-position function, not an arithmetic difference. It only produces a meaningful result when `a.exp == b.exp` — the two tumblers are at the same hierarchical depth, `a > b` in magnitude. This corresponds to the case where `a` and `b` share a common prefix in the address tree and `a` diverges from `b` to the right.

3. **Width and position must be at the same depth for span arithmetic to be valid.** In `insertpm` at `orglinks.c:115–117`, widths are explicitly constructed at the same depth level as the position:
   ```c
   shift = tumblerlength (vsaptr) - 1;
   inc = tumblerintdiff (&lwidth, &zero);
   tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
   ```
   The `shift` aligns the width digit to the VSA's depth level. This is the **required precondition** — violated, span difference degrades silently.

4. **`abscmp`'s exponent-first ordering creates an incoherent magnitude relationship for cross-depth tumblers.** It declares the coarser-grained tumbler "greater" even if in a numeric sense the finer-grained quantity could be larger. `strongsub` inherits this incoherence and papers over it with the guard.

---

### Concrete Example of the Failure

Suppose:
- `A.start` = `1.2` (exp=0, mantissa=`[1, 2, 0, ...]`) — a two-level address
- `B.width` = `0.0.5` → normalized to (exp=-2, mantissa=`[5, 0, ...]`) — a sub-sub-address quantity

`abscmp(A.start, B.width)`:  
→ `A.start.exp (0) != B.width.exp (-2)`, `A.start.exp > B.width.exp` → returns `GREATER`

`strongsub(A.start, B.width, result)`:  
→ `B.width.exp (-2) < A.start.exp (0)` → guard fires → `result = A.start = 1.2`

`1.2 - 0.0.5 = 1.2`. The fractional width `0.0.5` was entirely swallowed. No displacement occurred.

---

### Summary

When `strongsub` returns its input unchanged due to the exponent guard at `tumble.c:544–547`, it means the subtrahend (`b`) lives at a finer hierarchical depth than the minuend (`a`). The tumbler system has no mechanism to "carry" a fine-grained displacement upward into a coarser-grained address. The exponent guard is an admission of this: rather than produce a wrong answer, it returns `a` unchanged.

For span difference, this means: **subtracting one span's width from another's start position can fail to produce a meaningful displacement whenever the width is expressed at a finer hierarchical depth than the start position.** The operation is defined and closed only within a single depth level. Across depth levels, the result is the coarser operand itself — the width disappears without trace or error. The tumbler algebra is not a group under subtraction; it is a partial operation whose domain of meaningful closure is the set of same-`exp` tumbler pairs.

---

## Question 13 [gregory]

> Is there a canonical representation for a given region of tumbler space, or can the same set of positions be described by spans with different (start, width) pairs using different exponent encodings?

### Gregory's Answer

## KB Synthesis

There is no single canonical representation. The same region of tumbler space can be described by spans with different exponent encodings, and these representations are **not equal** as tumblers.

## Start Positions: Canonical After Justification

For start positions alone, `tumblerjustify` normalizes the tumbler, and after that step, `tumblereq` (equality) is unambiguous — two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match [SS-TUMBLER, Finding 0031]. So a given start point has a canonical form once justified.

## Widths: Not Canonical

Width is where non-uniqueness enters. The same integer "width" can be encoded at different tumbler precisions, producing unequal tumbler values.

This is directly evidenced by [SS-INSERT-VWIDTH-ENCODING, Finding 0076] and [INV-WIDTH-VALUE-EQUIVALENCE]:

> `value(crum.width.dsas[V]) == value(crum.width.dsas[I])` but `crum.width.dsas[V] != crum.width.dsas[I]` as tumbler representations

Concretely: a 11-character span yields
- I-width: `0.0.0.0.0.0.0.0.11` (9-digit precision, exp = −8)
- V-width: `0.11` (2-digit precision, exp = −1)

Both decode to integer 11, but `tumblercmp` treats them as distinct values — different exponents mean different positions in the total order [INV-TUMBLER-TOTAL-ORDER].

## Arithmetic Consequences

This non-canonicality is not merely representational — it affects computation. The `strongsub` exponent guard [SS-TUMBLER, Finding 0055] returns the minuend **unchanged** when the subtrahend's exponent is strictly less than the minuend's. Two widths encoding the same integer but at different precisions will behave differently in subtraction:

```
strongsub(a={exp=0}, b={exp=-1}):
  b.exp (-1) < a.exp (0) → no-op, returns a unchanged
```

This is why [FC-SUBSPACE, Finding 0055] notes that DELETE's subspace isolation is an **accidental** property of exponent mismatch — link displacements at `exp=0` are immune to deletion widths at `exp=-1`, even when they represent overlapping numeric ranges.

## Summary

| Aspect | Canonical? |
|--------|-----------|
| Start position (after `tumblerjustify`) | Yes |
| Width value (as tumbler) | No — same integer encodable at multiple precisions |
| Region equality via `tumblereq` | Requires matching exponent + mantissa, not just numeric value |

The POOM exploits this intentionally [SS-POOM-BOTTOM-CRUM]: V-widths are re-encoded at V-address precision, I-widths copied directly. The same region's extent is stored twice in different tumbler encodings, and they compare unequal. Any spec reasoning about "equivalent spans" must use value extraction (`tumblerintdiff`) rather than tumbler equality.

---

## Code Exploration

Now I have a complete picture. Here is the full answer.

---

## Canonical Representation in Tumbler Space

### The Tumbler Data Structure

A tumbler is defined in `backend/common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;     // 1 if negative, 0 otherwise
    short exp;         // always <= 0 in normalized form
    tdigit mantissa[NPLACES]; // 16 × uint32_t
} tumbler;
```

`tdigit` is `uint32_t` (`common.h:57`). `NPLACES` is `16` (`common.h:53`). The `exp` field is a signed short.

---

### The Canonical Form Is Unique — and Enforced by Code

#### The normalization invariant

`tumblercheckptr` [tumble.c:169-227] rejects three kinds of malformed tumblers:

1. **`exp > 0`** — [tumble.c:174-179]: only negative or zero exponents are valid.

2. **`exp != 0` AND `mantissa[0] == 0`** — [tumble.c:186-191]: flagged as `"fucked up non-normalized"`. The mantissa must be left-justified; the first slot cannot be zero unless the exponent is also zero.

3. **`mantissa[0] == 0` with any non-zero digit elsewhere** — [tumble.c:192-200]: flagged as `"nonzerozerotumbler"`.

The consequence: **`exp` encodes exactly how many leading-zero "stories" precede the first non-zero mantissa digit, and that mapping is injective.** A tumbler with `exp = -2, mantissa = [3, 5, 0, ...]` represents `0.0.3.5`; there is no other valid encoding of that address.

#### The human-readable serialization confirms this

`puttumbler` in `put.c:26-46` renders the exponent as literal leading `0.` groups:

```c
for(i = tumblerptr->exp; i < 0; ++i)
    fprintf(outfile, "0.");
// then prints mantissa[0..last_nonzero]
```

So `exp = -2, mantissa = [3, 5, ...]` serializes as `0.0.3.5`.

The FEBE wire format (`putfe.c:104-117`) sends `-exp` as an explicit integer prefix:

```c
putnum (outfile, - tumblerptr->exp);   // e.g. sends "2"
// then sends TUMDELIM-separated mantissa digits
```

The FEBE parser (`get2fe.c:69-88`) reads them back:

```c
getnum (taskptr, &num);
tumblerptr->exp = -num;
for (i = 0; gettdigit(taskptr, &value); i++) {
    tumblerptr->mantissa[i] = value;
}
```

There is no normalization step on FEBE input. The backend takes the `exp` and mantissa exactly as supplied. An input like `2.0.0.3.5~` would produce `exp = -2, mantissa = [0, 0, 3, 5, ...]` — but that would fail `tumblercheckptr` (rule 2: exp≠0 and mantissa[0]=0). **The protocol accepts whatever the client sends, but only internally-normalized tumblers are valid.**

#### `tumblerjustify` enforces normalization after arithmetic

Any arithmetic operation that might leave leading zeros calls `tumblerjustify` [tumble.c:289-313]:

```c
for (shift = 0; mantissaptr[shift] == 0; ++shift) { … }
for (i = 0, j = shift; j < NPLACES;)
    mantissaptr[i++] = mantissaptr[j++];
tumblerptr->exp -= shift;
```

It strips leading zeros and compensates by decrementing `exp`. After justification, `mantissa[0]` is again the first non-zero digit. `tumblersub` always calls `tumblerjustify` at [tumble.c:430]. The addition path (`absadd`) leaves the result left-justified by construction [tumble.c:444-485].

---

### Comparison Is Structural, Not Semantic

`abscmp` [tumble.c:87-111] compares by `exp` first:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp)
        return(LESS);
    else
        return(GREATER);
}
```

Two tumblers with **different `exp` values can never compare as `EQUAL`**, regardless of their mantissa contents. This means the ordering and equality relations treat the canonical structural encoding as the identity of the value.

`tumblereq` [tumble.c:24-36] does field-by-field comparison including `exp` and every mantissa slot. Again: different `exp` ⟹ not equal.

---

### Spans: (start, width) Is Also Uniquely Determined

`typespan` (= `typevspan`, `typeispan`) is defined in `xanadu.h:65-71`:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid itemid;
    tumbler stream;   // start
    tumbler width;
} typespan;
```

There is **no additional span-level normalization** beyond the individual tumbler normalizations. Both `stream` and `width` are canonical tumblers. Because each canonical tumbler has a unique encoding, a given pair (start, width) has exactly one binary representation, and that representation uniquely identifies the half-open interval `[start, start+width)`.

The span merger in `putvspaninlist` [orglinks.c:329-387] checks for adjacency via `tumblercmp` returning `EQUAL` on endpoints — which only occurs when the tumblers are structurally identical. This would break if two differently-encoded tumblers could represent the same address; the fact that it is not guarded against reflects the assumption that canonical form is unique.

---

### The One Real Hazard: `strongsub` Truncates Across Scales

`strongsub` [tumble.c:534-565] has a surprising early-exit:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

If `b` is at a finer scale (more negative `exp`) than `a`, the function returns `a` unchanged rather than computing `a − b`. The rationale: at the scale of `a`, `b` contributes nothing to the upper stories, so the result is considered equal to `a`. This is **lossy** — span endpoints computed via such subtraction can silently drop fine-grained contributions.

This does not create two encodings for one value. It means that certain span widths, when computed through subtraction, will be rounded up to the coarser granularity. The result is still canonical; it just does not represent the mathematically exact difference.

---

### Summary

| Property | Verdict | Key evidence |
|---|---|---|
| Each tumbler value has exactly one normalized encoding | **Yes** | `tumblercheckptr` [tumble.c:186-191], `tumblerjustify` [tumble.c:289-313] |
| Two tumblers with different `exp` can be equal | **No** | `abscmp` [tumble.c:92-96] returns LESS/GREATER before checking mantissa |
| A span (start, width) uniquely identifies a region | **Yes**, given canonical components | No span-level normalization beyond tumbler normalization |
| Non-canonical tumblers can be injected via FEBE | **Yes** (silently) | `get2fe.c:69-88` does not call `tumblercheckptr` on input |
| Scale-crossing subtraction is exact | **No** | `strongsub` [tumble.c:544-547] rounds coarser when `b->exp < a->exp` |

**The canonical form is unique.** Given the normalization invariant (`exp` = count of leading-zero stories, `mantissa[0]` = first non-zero digit), the same set of tumbler-space positions cannot be described by two different valid (start, width) pairs with different exponent encodings. The `exp` field is not a floating-point scale factor that can be freely shifted; it is an address-component index that is structurally bound to the mantissa content.

---

## Question 14 [gregory]

> How does `tumblerlength` (significant digits: `nstories(t) - t.exp`) interact with span width — does a width tumbler with more significant digits subdivide positions more finely than one with fewer, and what happens when a span's width has a different `tumblerlength` than its start?

### Gregory's Answer

## KB Synthesis

## `tumblerlength`, Width Precision, and Span Arithmetic

### `tumblerlength` encodes address-space depth, not content granularity

From [SS-TUMBLER] Finding 0031: `tumblerlength(t) = nstories(t) - t.exp` — the count of significant digits. For a V-address like `1.1`, tumblerlength=2. For an I-address like `0.0.0.0.0.0.0.0.11`, tumblerlength=9. Both can represent the integer 11 as a width, but at different exponent levels.

A width tumbler with more significant digits does NOT inherently subdivide positions more finely in the content sense. The digit count reflects how deep in the address hierarchy the value lives. From [SS-POOM-BOTTOM-CRUM] Finding 0076:

```
V-width for 11 chars: 0.11      (exp=-1, 2 digits)
I-width for 11 chars: 0.0.0.0.0.0.0.0.11  (exp=-8 or so, 9 digits)
```

Both encode the integer 11. [INV-WIDTH-VALUE-EQUIVALENCE] states this explicitly: `tumblerintdiff(crum.width.dsas[V], zero) == tumblerintdiff(crum.width.dsas[I], zero)` — same value, different precision.

### How V-width is derived from I-width

From [SS-INSERT-VWIDTH-ENCODING] Finding 0076, `insertpm` encodes V-width as:

```
shift = tumblerlength(vsaptr) - 1
inc   = tumblerintdiff(&lwidth, &zero)       // extract integer from I-width
tumblerincrement(&zero, shift, inc, &V-width) // encode at V-space precision
```

The V-width exponent is `-shift = -(tumblerlength(vsaptr) - 1)`, determined by the V-address length, not the I-width. So for V-address `1.1` (tumblerlength=2), V-width gets exp=-1; mantissa[0] holds the byte count. The I-width is copied directly. This is a lossy-on-representation-but-value-preserving transformation.

### When widths have different `tumblerlength` than their start: the `strongsub` gate

This mismatch is operationally significant. From [SS-TUMBLER] Finding 0055, `strongsub(a, b)` has an **exponent guard**: if `b.exp < a.exp`, it returns `a` unchanged — no subtraction occurs.

This is precisely why DELETE at V-position `1.x` does not shift link entries at `2.x` ([FC-SUBSPACE], [ST-DELETE] Finding 0055):

```
Deletion width: 0.3  (exp = -1)  
Link displacement: 2.1 (exp = 0)
strongsub(2.1, 0.3): b.exp(-1) < a.exp(0) → NO-OP, returns 2.1
```

The link crum's displacement has exp=0 (integer level); the deletion width is at exp=-1 (fractional/sub-unit level). The exponent mismatch prevents the shift from occurring. This is the **accidental subspace isolation** mechanism for DELETE — in contrast to INSERT's deliberate two-blade knife ([SS-TWO-BLADE-KNIFE], [INT-DELETE-SUBSPACE-ASYMMETRY]).

More generally, if you have a span whose start and width are at the same exponent level, arithmetic behaves as expected. If the width's exponent is lower than the start's exponent, `strongsub`-based shifting is a no-op. `tumbleradd` does not have this guard — it always adds — so computing `reach = start + width` always works regardless of exponent mismatch, but subtracting (shifting) only works when exponents match.

### Practical consequence for the spec

- For text content, span widths are always flat integer byte counts. The tumblerlength asymmetry between V-space (`0.11`) and I-space (`0.0.0.0.0.0.0.0.11`) is an encoding artifact, not a semantic difference ([INV-SINGLE-CHAR-GRANULARITY]).
- The `strongsub` exponent guard is the mechanism behind DELETE's frame condition on the link subspace ([FC-SUBSPACE] Finding 0055). Any Dafny proof of DELETE's subspace isolation must reason about tumbler exponent relationships, not just subspace digit values.
- V-width exponent is a function of V-address depth, so inserting at deeper V-addresses (more digits) produces V-widths with more negative exponents — still encoding the same byte count but at a different precision level.

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## `tumblerlength`, Span Width, and Hierarchical Subdivision

### What `tumblerlength` actually measures

```c
// tumble.c:249-262
INT nstories(tumbler *tumblerptr)
{
    for (i = NPLACES; i > 0 && tumblerptr->mantissa[--i] == 0;);
    return (i + 1);
}

INT tumblerlength(tumbler *tumblerptr)
{
    return (nstories (tumblerptr) - tumblerptr->exp);
}
```

`nstories` returns the index of the last non-zero mantissa digit + 1: the number of mantissa positions actually used.

`tumblerlength` = `nstories + |exp|`, since `exp` is always ≤ 0 [`tumblercheckptr` at `tumble.c:174` enforces this].

`exp` is decremented each time `tumblerjustify` removes leading zeros from the mantissa (`tumble.c:310`: `tumblerptr->exp -= shift`). So `|exp|` records how many hierarchical levels were collapsed. `tumblerlength` is therefore the **total hierarchical depth**: the number of significant levels, including both the stored digits and the removed leading zeros.

Concretely:
- Address `1.2` (mantissa `[1,2,0,…]`, exp=0): nstories=2, tumblerlength=**2**
- Address `1.2.3` (mantissa `[1,2,3,0,…]`, exp=0): nstories=3, tumblerlength=**3**
- A width of "5 at depth 5" (mantissa `[5,0,…]`, exp=−5): nstories=1, tumblerlength=**6**

---

### How span widths are constructed

In `tumbler2spanset` [`do2.c:57–58`]:
```c
tumblerclear (&spanptr->width);
tumblerincrement (&spanptr->width, tumblerlength (tumblerptr)-1/*zzzzz*/, 1, &spanptr->width);
```
Starting from zero, `tumblerincrement` with `rightshift = tumblerlength(stream) - 1` produces:
```c
// tumble.c:603-607
if (iszerotumbler (aptr)) {
    tumblerclear (cptr);
    cptr->exp = -rightshift;   // → exp = -(tumblerlength-1)
    cptr->mantissa[0] = bint;  // → mantissa[0] = 1
}
```
So `tumblerlength(width) = nstories(1) - (-(tumblerlength(stream)-1)) = 1 + (tumblerlength(stream)-1) = tumblerlength(stream)`. **Width is explicitly constructed to have the same tumblerlength as the stream.**

The same pattern appears in `insertpm` [`orglinks.c:115–117`]:
```c
shift = tumblerlength (vsaptr) - 1;
inc = tumblerintdiff (&lwidth, &zero);
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```
The V-dimension crum width again gets `tumblerlength = shift + 1 = tumblerlength(vsaptr)`.

And in `inserttextgr` [`granf2.c:106`]:
```c
tumblersub (&lsa, &spanorigin, &ispanptr->width);
```
`lsa` and `spanorigin` are at the same hierarchical depth (same document/atom level), so `strongsub` produces a width whose depth matches the stream.

---

### Does more significant digits = finer subdivision? Yes.

The span end is `stream + width`, computed via `absadd` [`tumble.c:460–484`], which aligns tumblers by their `exp` before adding. Work through three cases with the same stream `1.2` (mantissa `[1,2,0,…]`, exp=0):

**Width = `[1]` at exp=0 (tumblerlength=1) — coarsest:**
```
absadd: exps equal (0 == 0)
answer.mantissa[0] = 1 + 1 = 2
```
Span end = `2`. The span `[1.2, 2)` covers all of chapter 1's content after section 2, including 1.3, 1.4, … up to (not including) 2.

**Width = `[1]` at exp=−1 (tumblerlength=2) — matching:**
```
absadd: aptr->exp (0) > bptr->exp (-1), temp=1
answer.mantissa[0] = a[0] = 1
answer.mantissa[1] = a[1] + b[0] = 2 + 1 = 3
```
Span end = `1.3`. The span `[1.2, 1.3)` covers exactly section 2, including all sub-addresses 1.2.anything.

**Width = `[1]` at exp=−2 (tumblerlength=3) — finest:**
```
absadd: aptr->exp (0) > bptr->exp (-2), temp=2
answer.mantissa[0..2) = a[0..2) = [1, 2]
answer.mantissa[2] = a[2] + b[0] = 0 + 1 = 1
```
Span end = `1.2.1`. The span `[1.2, 1.2.1)` contains only addresses of the form `1.2.k` where k < 1, i.e., only the address `1.2` itself — a span that resolves to a single atomic position.

So yes: **a width tumbler with more significant digits (larger tumblerlength) produces a finer-grained span boundary.** Each additional level of depth narrows the span by one hierarchical tier.

---

### What happens when span width has a different `tumblerlength` than its start?

The system treats this as a **fatal invariant violation**. `ndcuts.c:431`:
```c
if (tumblerlength (cut) != tumblerlength (&ptr->cwid.dsas[index]))
#ifndef DISTRIBUTION
    gerror ("level mismatch\n");
```
(Identical check at `ndcuts.c:504` in the old-code block.)

This check fires during crum splitting: when the enfilade tries to insert a cut point through a node whose width is at a different depth than the cut address, the arithmetic fails. `strongsub` at `tumble.c:548–562` computes the local offset by skipping matching leading digits—if the cut is at depth 3 but the crum width is at depth 5, the subtraction produces a result at the wrong depth, the surviving crum width becomes inconsistent, and the enfilade invariants break.

The reason the depths must match: `tumblerincrement` at `tumble.c:621` places the incremented value at position `idx + rightshift`. If the existing crum has a width at depth 5 and the cut is at depth 3, the result of `locksubtract` at `ndcuts.c:444` will distribute the subtraction across incompatible digit positions, producing a nonsensical new width.

`granf2.c:240` shows how the system defends against this during address allocation:
```c
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
```
The increment depth is chosen conditionally based on whether the found `isaptr` is already at the expected depth (`hintlength`). If not, `depth` is zeroed out — a safety path to avoid placing an address at the wrong level.

---

### Summary

| Property | Effect |
|---|---|
| `tumblerlength(width) < tumblerlength(start)` | Width crosses to a coarser tier; span covers many sub-addresses of adjacent parent nodes |
| `tumblerlength(width) == tumblerlength(start)` | Width is at the same tier as the address; span covers a natural "unit" at that depth |
| `tumblerlength(width) > tumblerlength(start)` | Width crosses to a finer tier; span covers a sub-range of the address's own level |
| Mismatched in a POOM/SPAN crum | `gerror("level mismatch")` — fatal, since `strongsub`/`tumblerincrement` produce garbage at the wrong depth |

The invariant `tumblerlength(width) == tumblerlength(stream)` is enforced by construction at every insertion site (`do2.c:58`, `orglinks.c:115–117`, `granf2.c:106`) and checked defensively at split time (`ndcuts.c:431`, `ndcuts.c:504`). It is a first-class structural constraint of the enfilade: a span lives at a specific hierarchical depth, and both its start and width must agree on what that depth is.

---

## Question 15 [gregory]

> When splitting a span at an interior point, does the split always produce exactly two non-empty sub-spans whose widths sum to the original width, or can tumbler arithmetic rounding cause the parts to not reconstruct the whole?

### Gregory's Answer

## KB Synthesis

The KB gives a clear answer, though it comes from an implementation detail rather than an explicit arithmetic theorem.

## Split Reconstruction Is Exact by Construction

When `slicecbcpm` splits a crum at an interior cut point, the two resulting widths are computed as:

1. **Part 1:** `localcut = tumblersub(cut, grasp)` — the distance from the crum's left edge to the cut
2. **Part 2:** `cwid - localcut` via `locksubtract` — the *remainder*

This is the critical design choice. Part 2 is **not** computed independently as `tumblersub(reach, cut)`. It is computed as `original_width - part_1_width`. Mathematically:

```
part1 + part2 = localcut + (cwid - localcut) = cwid
```

This is exact and tautological — no tumbler arithmetic rounding can affect the sum because part2 is defined as the remainder from subtracting part1 from the original. [INV-NO-ZERO-WIDTH-CRUM]

## The Exponent Guard Is Not a Problem Here

The `strongsub` exponent guard (Finding 0055 in [SS-TUMBLER]) — which returns `a` unchanged when `b.exp < a.exp` — does not affect same-subspace splits. The precondition for `slicecbcpm` is `whereoncrum() == THRUME`, meaning `grasp < cut < reach` strictly. Interior points within a subspace (e.g., both at `1.x`) share the same exponent level, so the guard does not trigger. [PRE-DELETE], [SS-WHEREONCRUM]

## Strictly Positive Guarantee

The THRUME precondition also guarantees:
- `localcut = cut - grasp > 0` (cut is strictly above grasp)
- `cwid - localcut = reach - cut > 0` (cut is strictly below reach)

The assertions at `ndcuts.c:398` and `ndcuts.c:410` would catch any zero-width result. [INV-NO-ZERO-WIDTH-CRUM]

## Fixed Precision Caveat

Tumblers use a 16-digit mantissa (NPLACES=16). [SS-TUMBLER] Finding 0031. For very deep tumbler hierarchies with many significant digits, the 16-digit limit could theoretically cause truncation in `localcut`. The KB does not document any cases where this actually occurs for normal V-addresses (which use only 2–3 significant digits at text subspace positions like `1.3`). This remains an unverified edge case for pathologically long tumblers.

**Bottom line:** The split is designed to guarantee exact reconstruction by computing the second width as a remainder (`cwid - localcut`), not independently. Rounding cannot cause the parts to fail to sum to the original width — but only because the implementation avoids independent re-computation of the second part.

---

## Code Exploration

---

## Answer

The split **always produces exactly two non-empty sub-spans whose widths sum to the original** — but only because hard precondition checks in `slicecbcpm` abort the process if the preconditions for exact arithmetic are not met. There is no rounding. There is, however, a real truncation bug in `absadd` that exists for multi-story tumblers — it simply cannot be triggered by a legal span split.

---

### Where the Split Happens

The interior-point split of a bottom-level crum (height == 0) is performed by `slicecbcpm` [`ndcuts.c:373–450`], invoked from `makecutsbackuptohere` [`ndcuts.c:77–91`] when `whereoncrum` returns `THRUME` (address passes through this crum).

---

### The Tumbler Structure

From `common.h:59–65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;     /* 1 if negative, else 0 */
    short exp;         /* always <= 0; negative means leading zeros compressed */
    tdigit mantissa[NPLACES];  /* NPLACES = 16 unsigned ints */
} tumbler;
```

`iszerotumbler` is `!tumblerptr->mantissa[0]` [`common.h:72`]. A "1-story" tumbler has exactly one non-zero mantissa digit: `is1story` returns true iff `mantissa[1..15]` are all zero [`tumble.c:237–247`].

---

### What `slicecbcpm` Does

Starting at [`ndcuts.c:373`]:

**Step 1 — Validate and compute local cut position:**
```c
tumblersub(cut, &grasp.dsas[index], &localcut);  // [ndcuts.c:396]
```
`localcut` is the cut point expressed relative to the start of this crum.

**Step 2 — Hard preconditions (both abort with `gerror` if violated):**

```c
if (localcut.exp != ptr->cwid.dsas[index].exp)
    gerror("Oh well, I thought I understood this1\n");  // [ndcuts.c:403–408]

if (!is1story(&localcut))
    gerror("Oh well, I thought I understood this2\n");  // [ndcuts.c:410–430]

if (tumblerlength(cut) != tumblerlength(&ptr->cwid.dsas[index]))
    gerror("level mismatch\n");                          // [ndcuts.c:431–436]
```

Additionally, the crum's own width must be 1-story — checked just before `slicecbcpm` is called:
```c
if (!lockis1story(ptr->cwid.dsas, (unsigned)widsize(enftype)))
    gerror("Not one story in POOM wid\n");  // [ndcuts.c:389–394]
```

**These checks establish the invariant: both the original width and the split point are 1-story tumblers at the same `exp` level.**

**Step 3 — Construct left width:**
```c
movewisp(&ptr->cwid, &newwid);                     // [ndcuts.c:438] copy original width
for (i = 0; i < widsize(enftype); i++) {
    newwid.dsas[i].mantissa[0] = localcut.mantissa[0];  // [ndcuts.c:440]
    tumblerjustify(&newwid.dsas[i]);               // [ndcuts.c:441] no-op if [0] != 0
}
```
After this, `newwid` is 1-story with `mantissa[0] = localcut.mantissa[0]` and same `exp` as the original width (copied from `ptr->cwid`).

**Step 4 — Compute right width:**
```c
locksubtract((tumbler*)&ptr->cwid, (tumbler*)&newwid, (tumbler*)&new->cwid, widsize(enftype));
// [ndcuts.c:444]
```
`locksubtract` calls `tumblersub` per dimension [`wisp.c:275–279`]. So `new->cwid = original_cwid - newwid`.

**Step 5 — Install the split:**
```c
movewisp(&newwid, &ptr->cwid);                     // [ndcuts.c:445] left part gets newwid
dspadd(&ptr->cdsp, &ptr->cwid, &new->cdsp, enftype); // [ndcuts.c:446] right starts at cut
adopt(new, RIGHTBRO, ptr);                         // [ndcuts.c:448]
```

---

### Why the Arithmetic Is Exact for 1-Story Tumblers

**`tumblersub` for 1-story tumblers at equal `exp`:**

`tumblersub` [`tumble.c:406–440`] dispatches to `strongsub` via `tumbleradd(a, -b)` when neither argument is zero and they're unequal. In `strongsub` [`tumble.c:534–565`]:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) { --answer.exp; }
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // [tumble.c:556]
if (++i >= NPLACES) { movetumbler(&answer, cptr); return(0); }
for (j = 1; j < NPLACES && i < NPLACES;)
    answer.mantissa[j++] = aptr->mantissa[i++];               // [tumble.c:561–562]
```

For two 1-story tumblers at equal `exp`:
- `mantissa[0]` differs (since they're not equal), so `i = 0`, no decrement of `answer.exp`
- `answer.mantissa[0] = a.mantissa[0] - b.mantissa[0]` — exact integer difference
- `i` becomes 1, and `aptr->mantissa[1..N] = 0` (1-story), so the copy loop writes zeros

Result: `strongsub(a, b) = a.mantissa[0] - b.mantissa[0]` at the same `exp`. **Exact.**

**Reconstruction check:**

```
newwid.mantissa[0]     = localcut.mantissa[0]
new_cwid.mantissa[0]   = original.mantissa[0] - localcut.mantissa[0]
sum.mantissa[0]        = localcut.mantissa[0] + (original.mantissa[0] - localcut.mantissa[0])
                       = original.mantissa[0]  ✓
```

Both parts are 1-story at the same `exp` as the original. Their widths sum exactly to the original width.

---

### The Latent `absadd` Truncation (Does Not Apply to Span Splits)

`absadd` [`tumble.c:444–485`] is used by `tumbleradd`. In every branch, the final loop reads exclusively from `bmant`:

```c
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];   // [tumble.c:480–482]
}
```

In the equal-`exp` branch, after `ansmant[0] = amant[0] + bmant[0]`, the remaining digits `amant[1..N-1]` are **discarded** — only `bmant[1..N-1]` fills the tail. For a multi-story `a`, any sub-digits below the first level are silently lost.

This is a genuine truncation for multi-story tumblers: `absadd([2, 5, 3], [1, 0, 0]) = [3, 0, 0]`, not `[3, 5, 3]`.

However, `slicecbcpm` prevents this path via the `is1story` and `lockis1story` preconditions. All span widths entering `slicecbcpm` have `mantissa[1..N] = 0`. With only a single non-zero digit, `absadd` has nothing to truncate. The truncation bug is unreachable for any legal span split.

---

### The `strongsub` Early Return (Does Not Apply Either)

`strongsub` has a special case [`tumble.c:544–547`]:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);
    return(0);
}
```

This returns `a` unchanged (as if `b = 0`) when `b` is at a coarser hierarchical level than `a`. For span splits, both widths are at the **same** `exp` level (validated at [`ndcuts.c:398–408`]), so `bptr->exp == aptr->exp` and this early return is never taken.

---

### Summary

| Claim | Verdict | Evidence |
|-------|---------|----------|
| Split always produces exactly 2 non-empty sub-spans | **True, within preconditions** | Enforced by `slicecbcpm` structure |
| Sub-span widths sum to original | **Yes, exactly** | Integer arithmetic on 1-story tumblers |
| Tumbler arithmetic causes rounding | **No** | No fractional/floating arithmetic; only integer digit ops |
| `absadd` can truncate sub-digits | **Yes, but only for multi-story tumblers** | `ndcuts.c:480–482` drops `amant` tail |
| Multi-story tumblers can enter `slicecbcpm` | **No** | `gerror` aborts at `ndcuts.c:389–394` and `ndcuts.c:410–430` |

**The split is exact precisely because the code aborts rather than proceeding when the arithmetic would be approximate.** The preconditions (`is1story`, matching `exp`, matching `tumblerlength`) are not defensive programming — they are load-bearing constraints on a number system that does not support general multi-story subtraction. If a cut point cannot be expressed as a 1-story tumbler at the same level as the span width, the backend crashes rather than producing a split that does not reconstruct.

---

## Question 16 [gregory]

> In SpecSet composition, what ordering invariant do the component VSpecs maintain — must they be non-overlapping, sorted by start position, or can a SpecSet contain redundant or overlapping spans?

### Gregory's Answer

## KB Synthesis

## SpecSet Ordering and Overlap Invariants

The KB establishes the following, though the overlap question is only partially answered.

### Established: Order Is Significant, No Sort Required

[SS-SPECSET] defines `SpecSet = seq<VSpec>` — a **sequence**, not a set. The ordering is operationally significant: `retrieve` concatenates content in VSpec order, `vcopy` places content in VSpec order. [INV-SPECSET-ORDER] confirms all SpecSet-consuming operations preserve this sequence order as an invariant.

Crucially, no sorted-by-start-position requirement is stated anywhere. The system respects the caller-specified order; the backend is not documented to sort or reorder VSpecs before processing.

### Established: No Non-Overlap Requirement at the Backend

[PRE-SPECSET] specifies that backend validation checks only document existence — it does NOT validate element-level structure or structural relationships between VSpecs. The implementation does not enforce non-overlap between component spans.

[PRE-COPY] (Finding 0046) states explicitly that COPY **performs no duplicate checking** before inserting V→I mappings. The same I-address can intentionally appear at multiple V-positions via repeated COPY. [SS-POOM-MULTIMAP] confirms the POOM is a multimap: a single I-address can map to multiple V-positions.

### Inferred: Redundant/Overlapping Spans Are Accepted and Processed Redundantly

From [INV-IDENTITY-OVERLAP], overlapping transclusion regions are valid — overlapping characters in the destination share I-position identity with the source. [EC-SELF-TRANSCLUSION] confirms a document can transclude content from itself, producing duplicate I-address references.

Given no overlap check at any layer, a SpecSet with overlapping VSpecs would be accepted. On `retrieve`, the overlapping byte range would appear twice in the output (once per VSpec, in sequence order). On `vcopy`, the overlapping I-addresses would be placed at multiple V-positions in the destination.

### Summary

| Constraint | Status |
|------------|--------|
| Sequence order preserved | **Enforced** — all operations respect VSpec order [INV-SPECSET-ORDER] |
| VSpecs must be sorted by start position | **Not required** — no such precondition exists |
| VSpecs must be non-overlapping | **Not enforced** — backend validates only document existence [PRE-SPECSET] |
| Redundant spans cause errors | **Not documented** — POOM multimap and no-duplicate-check [PRE-COPY] imply they are processed as given |

The KB does not contain a direct test of overlapping-VSpec behavior in a single SpecSet, so the redundant-processing behavior above is inferred from the multimap structure and absence of any overlap guard, rather than directly observed.

---

## Code Exploration

Now I have everything I need. Here is the complete answer.

---

## SpecSet Composition: VSpec Ordering Invariants

### Data Structure

The relevant types are defined in `backend/xanadu.h`:

```c
// xanadu.h:73-74
typedef typespan typevspan;
typedef typevspan * typevspanset;

// xanadu.h:78-83
typedef struct structtypevspec{
        struct structtypevspec *next;
        typeitemid      itemid;
        typeisa docisa;          // which document
        typevspanset vspanset;   // linked list of VSpans within that doc
} typevspec;

// xanadu.h:85-89
typedef union {
        typevspec xxxvspec;
        typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

A **SpecSet** is a singly-linked list of `typespec` items, each of which is either a VSpec (virtual specification: a document ISA + a set of V-space spans) or a raw ISpan. The two levels of structure — the SpecSet itself and the `vspanset` inside each VSpec — have completely different invariants.

---

### Level 1: Within a VSpec's `vspanset` — Strict Invariants Enforced

The only function that inserts a VSpan into a vspanset is `putvspaninlist` [`orglinks.c:329-387`]. It is the gatekeeper, and it enforces three invariants aggressively:

**1. Sorted by start position (`stream`)**

The function walks the list comparing the new span's start against each existing span's end:

```c
// orglinks.c:342
for (; ptr; last = ptr, ptr = ptr->next) {
    tumbleradd (&spanptr->stream, &spanptr->width, &newspanend);
    tumbleradd (&ptr->stream, &ptr->width, &oldspanend);
    spancmp = tumblercmp (&spanptr->stream, &oldspanend);
    ...
    } else if (spancmp == GREATER)
        continue;   // skip past spans that end before new one starts
```

It inserts at the correct position once it finds where the new span fits in the ordering [`orglinks.c:356-361`]:

```c
} else if (spancmp == GREATER) {
    if (ptr != *spansetptr)
        last->next = makevspan (taskptr, spanptr, ptr);
    else
        *spansetptr = makevspan (taskptr, spanptr, ptr);
    return(0);
}
```

**2. Non-overlapping — overlapping spans are merged, not stored separately**

When the new span overlaps an existing one, `putvspaninlist` mutates the existing node to subsume both spans rather than inserting a duplicate. The `startcmp`/`endcmp` switch at lines 363–384 covers all overlap cases:

- New span is **fully contained** in existing → early return, nothing added [`orglinks.c:365-366`]:
  ```c
  if (startcmp > LESS && endcmp < GREATER)
      return(0);
  ```
- Same start, new is longer → widen existing width [`orglinks.c:368-370`]
- New starts earlier, new ends earlier (partial left overlap) → extend start leftward and recompute width [`orglinks.c:372-377`]
- New starts later, new ends later (partial right overlap) → extend width rightward [`orglinks.c:379-382`]

**3. Adjacent (touching) spans are merged**

When the new span starts exactly where an existing span ends (`tumblercmp` returns 0), the widths are summed:

```c
// orglinks.c:346-348
spancmp = tumblercmp (&spanptr->stream, &oldspanend);
if (!spancmp) {
    tumbleradd (&ptr->width, &spanptr->width, &ptr->width);
    return(0);
```

Similarly, when an existing span starts exactly where the new span ends [`orglinks.c:352-355`]:
```c
spancmp = tumblercmp (&ptr->stream, &newspanend);
if (!spancmp) {
    movetumbler (&spanptr->stream, &ptr->stream);
    tumbleradd (&spanptr->width, &ptr->width, &ptr->width);
    return(0);
```

**Summary for `vspanset`:** VSpans within a single VSpec are always non-overlapping, non-adjacent, and sorted ascending by `stream`. This is not a convention — `putvspaninlist` actively enforces it by merging any new span that would violate these conditions.

---

### Level 2: Across VSpecs in a SpecSet — No Invariants

`specset2ispanset` [`do2.c:14-46`] is the primary consumer of a SpecSet. It iterates each element sequentially:

```c
// do2.c:23-39
for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *ispansetptr = (typeispanset)specset;
        ispansetptr = (typeispanset *)&((typeitemheader *)specset)->next;
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        ...
        ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr)
    }
}
```

There is no ordering check, no overlap check, and no deduplication between VSpecs. Each VSpec is processed independently. The SpecSet is consumed as a plain linked list in whatever order items were inserted.

`onitemlist` [`orglinks.c:464-537`], which appends items to a SpecSet, simply walks to the tail and links the new item — no sorting, no deduplication:

```c
// orglinks.c:521-534
for (temp = *itemsetptr;
     temp && ((typeitemheader *)temp)->next;
     temp = (typeitem *)((typeitemheader *)temp)->next)
    ;
((typeitemheader *)temp)->next = (typeitemheader *)newitem;
```

Multiple VSpecs in a SpecSet can therefore:
- Reference the same document (`docisa`) with overlapping or redundant V-spans
- Reference different documents in any order
- Contain ISpans interleaved with VSpecs in any sequence

---

### The Commented-Out Consolidation Evidence

The absence of cross-VSpec consolidation is not an accident. `orglinks.c` contains two traces of work that was explicitly abandoned:

**1. `consolidatespans` call disabled in `permute`** [`orglinks.c:412-413`]:
```c
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset);    */
```

**2. `cleanupvspanlist` function and the entire alternative `retrievevspansetpm` implementation** are wrapped in `#ifdef UnDEFined` [`orglinks.c:263-313`]. The disabled `cleanupvspanlist` would have merged only *adjacent* vspans (using `tumblereq` equality at line 307), not overlapping ones — which tells us the active `putvspaninlist` is the more correct and complete approach.

**3. A `consolidatespanset` stub** (commented, never completed) appears at [`orglinks.c:455-462`]:
```c
/*
consolidatespanset(spanset);
  typespan *spanset;
{
    for(;spanset->next;spanset = spanset->next){
        if(
    }
}*/
```

This confirms cross-SpecSet consolidation was considered and deliberately left unimplemented.

---

### Summary Table

| Level | Invariant | Enforced? | Where |
|---|---|---|---|
| Within a VSpec's `vspanset` | Sorted ascending by `stream` | **Yes, enforced** | `putvspaninlist` `orglinks.c:342-361` |
| Within a VSpec's `vspanset` | Non-overlapping (merged) | **Yes, enforced** | `putvspaninlist` `orglinks.c:363-384` |
| Within a VSpec's `vspanset` | Non-adjacent (touching merged) | **Yes, enforced** | `putvspaninlist` `orglinks.c:346-355` |
| Between VSpecs in a SpecSet | Sorted by any criterion | **No** | `onitemlist` appends to tail `orglinks.c:521-534` |
| Between VSpecs in a SpecSet | Non-overlapping across docs | **No** | `specset2ispanset` iterates blindly `do2.c:23-39` |
| Between VSpecs in a SpecSet | No redundant entries | **No** | Consolidation code commented out `orglinks.c:412-413` |

**The invariants are strictly local**: a SpecSet can contain redundant or overlapping entries across its component VSpecs, but within each VSpec the vspanset is always a canonicalized, sorted, merged, non-overlapping sequence of V-space spans.

---

## Question 17 [gregory]

> Does the tumbler total order guarantee that all positions within a span `[start, start+width)` form a contiguous interval under `tumblercmp`, or can the hierarchical digit structure create positions that compare as "inside" the range but are not logically part of the span?

### Gregory's Answer

## KB Synthesis

## Tumbler Span Contiguity and Hierarchical Addresses

The answer is **no** — the tumbler total order does not guarantee that `[start, start+width)` contains only "logically equivalent" positions. The hierarchical digit structure does create phantom elements that compare as interior to a span.

### The Core Issue

From [SS-TUMBLER] (Findings 0001, 0031): tumblers use `.0.` boundaries to encode hierarchy — `1.1.0.2.0.1` (a document address) and `1.1.0.2.0.1.1` (its child) are distinct tumblers. The total order on tumblers is lexicographic after exponent alignment.

From [INV-TUMBLER-TOTAL-ORDER]: comparison proceeds by exponent first, then mantissa digits left-to-right. This gives the ordering:

```
1.1.0.2 < 1.1.0.2.0.1 < 1.1.0.3
```

So a span `[1.1.0.2, 1.1.0.3)` — with width computed via `tumblersub` — classifies `1.1.0.2.0.1` as `THRUME` ([SS-INTERVAL-CMP]), even though `1.1.0.2.0.1` is a document address at a deeper hierarchy level, not a position within the span's intended range.

Similarly, within V-space: a span `[1.3, 1.4)` would admit any tumbler `t` satisfying `1.3 < t < 1.4` — including `1.3.0.5` or `1.35` (fractional addresses at different precision) — all classifying as THRUME under `intervalcmp` per [SS-WHEREONCRUM].

### Why This Does Not Break the System in Practice

The system avoids phantom-element problems through two mechanisms:

**1. Allocation at uniform precision.** From [SS-ADDRESS-SPACE] (Finding 0033): sequential text inserts get contiguous I-addresses at the same precision level (`2.1.0.1.0.1.3.1`, `2.1.0.1.0.1.3.2`, etc.). From [SS-POOM-BOTTOM-CRUM] (Finding 0076): V-positions are allocated as flat 2-digit tumblers (`1.1`, `1.2`, ..., `1.10`). No V-stream content is ever placed at mixed-precision addresses like `1.3.0.5` within a subspace. This is a **convention**, not a structural enforcement.

**2. Subspace isolation via knife bounds.** From [SS-TWO-BLADE-KNIFE] (Finding 0054): INSERT at `N.x` uses second blade `(N+1).1`. The shift region `[N.x, (N+1).1)` is bounded by a whole-number subspace boundary. Any address at `(N+ε)` for fractional ε would fall inside, but since no content exists at such addresses, no POOM crums are affected. The two-blade knife exploits the hierarchical ordering without being harmed by the phantom-element property.

**3. The containment property is intentionally used.** From [SS-TUMBLER-CONTAINMENT]: the system uses prefix-truncation + equality checks (not interval comparison) for the allocation algorithm's hierarchical containment predicate. The interval classifier is used only for POOM traversal over V-positions allocated at uniform precision.

### Formal Implication for the Spec

The spec cannot state "the set of tumblers in `[start, start+width)` is exactly the intended content positions" as a consequence of the total order alone. It requires an additional **well-formedness invariant**: all V-positions within a document's POOM are allocated at a fixed precision level within their subspace. From [INV-SUBSPACE-CONVENTION]: this is a caller-enforced convention, not a storage-layer structural guarantee.

The `intervalcmp` / `whereoncrum` machinery is sound precisely because the POOM never contains entries at fractional or hierarchically deeper V-addresses within a subspace — but that soundness depends on [SS-SUBSPACE-CONVENTION] holding, not on the total order itself.

---

## Code Exploration

Now I have the complete picture. Here is the full analysis.

---

## Tumbler Total Order and Span Contiguity

### 1. The Total Order: What `tumblercmp` Actually Does

`tumblercmp` [tumble.c:72-85] delegates to `abscmp` [tumble.c:87-111] for positive tumblers. `abscmp` is a **flat lexicographic comparison** on the `(exp, mantissa[0..15])` tuple:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp) return(LESS);
    else return(GREATER);
}
// exps equal: compare mantissa[0], mantissa[1], ... left to right
for (i = NPLACES; i--;) {
    if(!(cmp = *a++ - *b++)) {}
    else if (cmp < 0) return(LESS);
    else return(GREATER);
}
return(EQUAL);
```
[tumble.c:92-110]

This is a genuine strict total order. Smaller `exp` (more negative) is LESS; among equal exps, mantissa is compared element by element. Zeros are **not treated specially** — `abscmp` compares all 16 mantissa digits without any zero-termination logic. This distinguishes `abscmp` sharply from `tumbleraccounteq` [tumble.c:38-70], which *does* treat consecutive zeros as a level terminator. These two functions have inconsistent models of what a tumbler means.

---

### 2. Sub-Addresses Are Dense But Legitimate

The hierarchical digit structure means there are infinitely many tumblers that sort strictly between any two adjacent top-level positions. For example, between `[exp=0, mantissa=[2,0,...]]` (= 2) and `[exp=0, mantissa=[3,0,...]]` (= 3):

```
2 < 2.1 < 2.5 < 2.5.3 < 2.9 < 3      (under abscmp, same exp=0)
```

Any `p = [exp=0, mantissa=[2, X, Y, ...]]` with any non-zero `X` or later digits satisfies `2 ≤ p < 3`. These positions compare as "inside" the span `[2, 3)`.

Are they **logically phantom**? No. In Xanadu's model, sub-addresses like 2.5 are legitimate positions within position 2's subtree. The enfilade correctly places them inside any span covering position 2. This is *by design*, not an anomaly.

---

### 3. `absadd` Is Not Standard Addition

The critical mechanism for computing `end = start + width` is `absadd` [tumble.c:444-485]. It is **not numeric addition with carries**. When `aptr->exp == bptr->exp`:

```c
ansmant[0] = amant[0] + bmant[0];   // add only first aligned digit
i = j = 1;
// ... then fill from bmant[1..NPLACES-1], DISCARDING amant[1..]
while ( j <= NPLACES -1 ) {
    ansmant[j++] = bmant[i++];   // b's suffix, not a's
}
```
[tumble.c:460-483]

**A's sub-digits after the alignment point are silently discarded.** Only the first aligned digit of `b` is added to the first aligned digit of `a`. The result's suffix comes from `b`, not `a`.

When `aptr->exp > bptr->exp` (a is "shallower"):
```c
temp = aptr->exp - bptr->exp;
while (i < temp) { ansmant[j++] = amant[i++]; }   // copy a's prefix
ansmant[j++] = amant[i++] + bmant[0];               // add at alignment point
i = 1;
// then fill from bmant[1..], discarding amant[temp+1..]
```
[tumble.c:464-471, 480-483]

Again, `a`'s tail digits beyond the addition point are lost.

---

### 4. The Level-Invariant That Keeps Spans Consistent

In `insertpm` [orglinks.c:74-134], the V-width stored in each POOM crum is computed at exactly the same hierarchical level as the V-address:

```c
shift = tumblerlength (vsaptr) - 1;              // depth of vsaptr
inc = tumblerintdiff (&lwidth, &zero);           // integer value of ispan width
tumblerincrement (&zero, shift, inc, &crumwidth.dsas[V]);
```
[orglinks.c:115-117]

`tumblerincrement(&zero, shift, inc)` places `inc` at position `shift` in a zero tumbler, yielding `[exp=-shift, mantissa=[inc, 0,...]]`. So if `vsaptr` has level-1 address (e.g., `1.3`, exp=0, mantissa=[1,3,...]), `shift=1`, and the V-width gets `exp=-1`. Then:

```
absadd([exp=0, mantissa=[1,3,...]], [exp=-1, mantissa=[inc,0,...]])
   → aptr->exp(0) > bptr->exp(-1), temp=1
   → copy amant[0]=1, then add amant[1]+bmant[0] = 3+inc
   → result: [exp=0, mantissa=[1, 3+inc, 0,...]]
```

So the span covers `[1.3, 1.(3+inc))` — exactly `inc` sub-positions at level 1. **When the level-invariant holds, span endpoints are computed correctly and the round-trip via `strongsub` works:**

`strongsub([1, 3+inc,...], [1, 3,...])` [tumble.c:548-564]:
- Both exps equal (=0); iterate prefix: mantissa[0] = 1 == 1 → --answer.exp = -1; mantissa[1] = 3+inc ≠ 3
- answer.mantissa[0] = (3+inc) - 3 = inc; suffix: zeros
- Result: `[exp=-1, mantissa=[inc,...]]` = original width ✓

---

### 5. The Pathological Case: Level-Mismatched Span Endpoints

Now, the concrete failure mode. If `start` has sub-digits but `width` is expressed at the top level — mixed levels:

**Example:** `start = 2.5` (`[exp=0, mantissa=[2,5,...]]`), `width = 3` (`[exp=0, mantissa=[3,...]]`):

```
absadd(2.5, 3):
  exps equal (both 0)
  ansmant[0] = 2 + 3 = 5       ← sub-digit .5 discarded
  rest: bmant[1...] = [0, 0,...]
  result: [exp=0, mantissa=[5, 0,...]] = 5
```

Span `[2.5, 5)` under `tumblercmp` now contains:
- `2.5` and all sub-addresses of `2.5` ✓
- `2.6, 2.7, ...` (other sub-positions of 2, after 2.5) ✓
- `3, 3.1, 3.2, ...` — **all of position 3 and its subtree**
- `4, 4.1, 4.2, ...` — **all of position 4 and its subtree**

But if the system intended "3 items starting at sub-position 2.5," the correct width should have been `[exp=-1, mantissa=[3,...]]`, giving end `2.8` and span `[2.5, 2.8)` — covering only 3 sub-positions within 2.x.

With the mismatched width, positions 3 and 4 compare as "inside" [2.5, 5) but were not intended to be part of this span. This is the "inside the range but logically outside" scenario the question asks about.

A further asymmetry: `strongsub(5, 2.5)` [tumble.c:534-565]:
- `bptr->exp(0)` is not less than `aptr->exp(0)`, so normal path
- mantissa[0]: 5 ≠ 2 → immediately: `answer.mantissa[0] = 5 - 2 = 3`
- Result: `[exp=0, mantissa=[3,...]]` = 3 ≠ original width (which might have been `[exp=-1, 3]`)

The round-trip breaks: `absadd(2.5, 3_level0) = 5`, then `strongsub(5, 2.5) = 3_level0`, which appears to reconstruct the width — but now the width is at level 0, making the span 3 top-level units, not 3 sub-units. The information about the original level is permanently lost.

The comment in `insertpm` at orglinks.c:114 — `"I'm suspicious of this shift"` — reflects genuine uncertainty from the author about whether this level-matching mechanism is always invoked correctly.

---

### 6. `strongsub`'s Silent Truncation

`strongsub` [tumble.c:544-546] has a silent failure mode when `bptr->exp < aptr->exp`:

```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);   // ← just return a unchanged; b is ignored
    return(0);
}
```

If you try to subtract a deep-level tumbler from a shallower one — `strongsub(5, [exp=-1, 3])` — the result is `5`, not `4` or `4+2/3`. Subtraction ignores `b` entirely if it's at a deeper level than `a`. This means level-mismatched arithmetic is silently incorrect in both directions (add and subtract).

---

### 7. Granfilade Guards Against Phantom Hits

The granfilade lookup in `fetchorglgr` [granf2.c:22-81] explicitly rejects addresses that fall inside a crum's range but don't match exactly:

```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```
[granf2.c:37-40]

This means if a query address like `1.3.5` happens to fall within a granfilade crum's range, but the crum was stored at exactly `1.3`, the lookup returns NULL. The "inside the range" property of `tumblercmp` does **not** cause false positive hits in granfilade lookups because an exact-match guard explicitly screens them out.

For text retrieval via `ispan2vstuffset` [granf2.c:286-318], range queries are intentional:
```c
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```
[granf2.c:296-297]

But I-addresses for text are always level-0 (assigned by `tumblerincrement(..., 0, length, ...)` in `inserttextgr` [granf2.c:100]), so the level-invariant holds there, and the `absadd` is safe.

---

### Summary

**The total order is genuine.** `tumblercmp` induces a strict total order on all tumblers, and for any span `[start, end)`, the set `{p : start ≤ p < end}` is a well-defined contiguous interval under this order.

**The hierarchical structure does NOT by itself create phantom inside-positions.** Sub-addresses like `2.5` or `2.5.3` that compare as inside a span containing position `2` ARE logically part of that position's sub-tree. Their presence in the interval is correct and intended.

**But `absadd` is not standard addition**, and this creates a genuine span-boundary problem when its operands are at different hierarchical levels. When `start` has sub-digits and `width` is expressed at a higher (coarser) level, `absadd` discards `start`'s sub-digits [tumble.c:460-483] and computes an `end` that is **too far forward** — extending the span to include entire top-level positions that should not be part of the span. Under `tumblercmp`, these extra positions compare as "inside" `[start, end)`, but they are not logically part of the intended span content.

The system guards against this with the `shift` calculation in `insertpm` [orglinks.c:115-117], which enforces the level-invariant for all POOM crums. When this invariant holds, every position comparing as "inside" a stored span is genuinely logically inside it. When it breaks — either via corrupted spans or user-provided spans with mismatched levels passed into `retrieverestricted` [retrie.c:56-85] — the span [start, end) will contain positions that are logically extraneous, and `tumblercmp` will classify them as inside with no error.
