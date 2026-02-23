# Consultation Answers — Tumbler Algebra

**Inquiry:** What algebraic properties must the Xanadu addressing system satisfy? What ordering, arithmetic, and structural guarantees do tumblers provide?
**Date:** 2026-02-22 21:47
**Questions:** 10 (5 nelson, 5 gregory)

---

## Question 1 [nelson]

> Must every address the system assigns be permanently ordered relative to every other address, and what does that ordering represent — creation sequence, containment, or both?

### Nelson's Answer

## Yes — and the ordering represents both containment and creation sequence, unified through a single tree structure

Every tumbler address is permanently ordered relative to every other. The tumbler line is a **total order** obtained by depth-first traversal of the docuverse's containment tree. This ordering is what makes spans work — a span is defined by two tumbler endpoints, and everything between them is determined by the tree structure:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

The ordering is permanent because addresses are permanent:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

### What the ordering represents

The tumbler line is not a number line. It is a flattened tree:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

This means the ordering encodes **containment**: server contains accounts, accounts contain documents, documents contain versions, versions contain elements. Every subtree maps to a contiguous range on the tumbler line, which is why a single span can address "all documents by this author" or "all content on this server":

> "A span may be visualized as a zone hanging down from the tumbler line—what is called in computer parlance a depth-first spanning tree." [LM 4/25]

### Creation sequence within each level

Within a containment level, siblings are numbered sequentially through the "baptism" process:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Items 2.1, 2.2, 2.3, 2.4 are "successive items being placed under 2" [LM 4/20]. So within a single level of the tree, the numeric order of siblings reflects **creation order** — the first document created under an account gets a lower number than the second.

For links this is explicit:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

For I-space content, the append-only model means native bytes within a document are stored chronologically:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Time is explicitly excluded

Despite this correlation, Nelson explicitly separates temporal from structural ordering:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." [LM 4/18]

The tumbler records WHERE something sits in the containment hierarchy, not WHEN it was created. The fact that sibling ordering correlates with creation sequence is a consequence of sequential allocation, not a temporal encoding. Two documents on different servers may be interleaved arbitrarily on the tumbler line despite being created simultaneously — their relative order reflects server containment, not creation time.

### V-space is the exception that proves the rule

V-space addresses are the one case where tumbler ordering does NOT reflect creation sequence:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-space ordering represents the document's **current arrangement** as the user sees it. This ordering changes with every INSERT, DELETE, and REARRANGE. But even here, the addresses are totally ordered at any given moment — they form a dense contiguous sequence from position 1 to the document's current length.

### Summary

The ordering is **both containment and creation sequence**, but at different structural levels:

| Level | What ordering represents |
|-------|------------------------|
| **Between branches** (servers, accounts) | Containment — depth-first tree traversal |
| **Within a branch** (sibling documents, sibling links) | Creation sequence — sequential baptism |
| **V-space** (byte positions) | Current arrangement — mutable by editing |

The architectural payoff is that a single mechanism — the span, defined by two tumbler endpoints — can express queries at every scale, from one byte to the entire docuverse, because every subtree is a contiguous range. This is what Nelson calls "a curious, bizarre, powerful, consistent, non-obvious and hard-to-visualize system. It also has a certain quirkiness and charm. Call it a hack, yes; but it is definitely a superhack." [LM 4/40]

---

## Question 2 [nelson]

> When the system computes "the next available address" for new content, what guarantees prevent two different pieces of content from ever receiving the same address?

### Nelson's Answer

# Address Uniqueness in Xanadu

Nelson's design prevents address collision through three interlocking mechanisms: **hierarchical ownership partitioning**, **sequential allocation within partitions**, and **unbounded number capacity**. Together, these make duplicate addresses structurally impossible — not merely unlikely.

## 1. Hierarchical Ownership Partitioning

The tumbler address space is a tree, and each subtree has exactly one owner. This is the primary collision-prevention mechanism:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

The four-level I-space address structure enforces this:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

At each level, exactly one entity controls allocation:
- **Server 1** allocates accounts 1.1, 1.2, 1.3...
- **Account 1.2** allocates documents 1.2.1, 1.2.2...
- **Document 1.2.3** allocates elements within its own content space

No two owners share a prefix, so they cannot produce the same address. This is structural separation, not a lock or a check — the tree topology itself prevents collision across owners.

## 2. Sequential Allocation Within Each Partition

Within any owner's subtree, new items receive the next sequential number:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

The sequence is monotonically increasing — you go from 2.1 to 2.2 to 2.3, never backward. For links specifically, Nelson confirms sequential ordering:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

This monotonic counter within each partition means: even within a single owner's subtree, two allocations cannot produce the same address because the counter always advances.

## 3. Unbounded Number Capacity

The humber (humungous number) format ensures the counter can never overflow:

> "Humber stands for 'humungous number.' Humbers are numbers we have designed for this system, a notation for positive integers." [LM 4/13]

> "They are a data structure of the class usually called Bignums, that is, a way of representing numbers that may range up to very great size; but we have tailored them also to be very small in their representation when they represent small quantities. Thus the humber is an accordion-like notation, very short when a number is small, and as large as it needs to be when the number is big." [LM 4/13]

Because each "digit" (integer component) in a tumbler has no upper limit, the address space within any subtree is inexhaustible. You will never be forced to reuse an address because the numbers ran out.

## 4. Ownership Controls Allocation — No Coordination Needed

The critical insight is that uniqueness requires **no coordination between owners**:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

Server A and Server B can both allocate simultaneously without communicating, because they occupy disjoint subtrees of the tumbler space. Account 1.2 and Account 1.3 can both create documents without consulting each other.

This is why Nelson describes the result as permanent:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## Summary of the Guarantee

| Mechanism | What It Prevents |
|-----------|-----------------|
| **Hierarchical ownership** | Collision between different owners (structural partitioning) |
| **Sequential allocation** | Collision within the same owner's subtree (monotonic counter) |
| **Unbounded integers** | Address exhaustion forcing reuse |
| **Single owner per subtree** | Concurrent allocation races at the same level |

## What Nelson Leaves Implicit

Nelson does not address two scenarios that arise in practice:

1. **What if a server crashes mid-allocation and loses track of its counter?** The allocation counter must be durable — if it retreats, a previously-assigned address could be reassigned. Nelson's append-only storage model implies the counter never retreats, but he does not explicitly specify counter durability or crash recovery for the allocation mechanism.

2. **What prevents concurrent allocation within a single document?** If two processes simultaneously insert content into the same document, they need the same counter. Nelson's design implicitly assumes single-writer semantics per document (the owner), but the concurrency protocol is not specified.

NEED_RAW: [4/28-4/30] — The curated sources cover the key quotes about allocation, but these pages may contain additional detail about how element-level addresses (bytes within a document) are assigned during INSERT operations specifically.

---

## Question 3 [nelson]

> Must the address of a piece of content reveal which document, which version, and which user account it belongs to — and is this hierarchical containment an essential design property or merely convenient?

### Nelson's Answer

## Yes — and it is essential, not merely convenient

The tumbler address of every piece of content in Xanadu encodes a complete hierarchy: server node, user account, document (with version subdivisions), and element position. Nelson designed this deliberately, and multiple fundamental guarantees depend on it.

### What the address reveals

An I-space address has the form:

```
Node.0.User.0.Document.0.Element
```

Nelson specifies:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

The Document field further subdivides to encode version ancestry:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

And the Element field distinguishes content types by subspace (bytes in the 1.x subspace, links in the 2.x subspace).

So from any content address, you can read off: which server stores it, which account owns it, which document created it, which version it belongs to, and whether it is text or a link.

### Why hierarchical containment is essential, not convenient

The hierarchy serves at least four properties that Nelson treats as non-negotiable design requirements. Removing the hierarchy would break each of them.

**1. Structural ownership.** Ownership is not metadata attached to content — it is the User field of the address itself. Nelson's ownership guarantee ("Only the owner has a right to withdraw a document or change it" [LM 2/29]) requires no separate access control list because the address encodes the owner. If the address did not reveal the account, ownership would require a separate lookup mechanism, and that mechanism could fail, be stripped, or become inconsistent with the content.

**2. Structural attribution.** Nelson guarantees:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not a feature of a metadata system — it is a consequence of the address encoding. When content is transcluded, the system fetches it from its home location:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address IS the provenance. The Document field tells you which document created the bytes. The connection cannot be severed because the retrieval mechanism requires it.

**3. Coordination-free allocation.** Nelson's decentralization model depends on hierarchical ownership of address subspaces:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

This is how millions of independent actors create content without a central authority allocating addresses. Each owner controls their own subtree. If the address did not encode the hierarchy, address allocation would require global coordination — precisely what the tumbler system exists to avoid.

**4. Hierarchical range queries.** Nelson's span mechanism depends on the fact that the tree maps to a contiguous range on the tumbler line:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." [LM 4/38]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

A single span can express "everything by this author" or "all content on this server" precisely because the hierarchy is encoded in the address. Without it, these queries would require index lookups rather than arithmetic operations — undermining the "soft corridor" performance guarantee that Nelson considers essential for a system that must scale to the entire docuverse.

### The version encoding is slightly weaker

There is one important caveat. While the document-and-version hierarchy is encoded in the address, Nelson himself notes that the version relationship is somewhat accidental:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The CREATENEWVERSION operation does produce addresses that "indicate ancestry" [LM 4/66], but the subdocument mechanism is general — it can represent any parent-child relationship, not only version derivation. So the address reveals *that* a version is structurally subordinate to a document, but the *semantic meaning* of that subordination (actual content derivation vs. mere administrative grouping) is a convention, not an address-level guarantee.

### What the hierarchy does NOT do

Nelson is explicit that the hierarchy imposes no semantic structure on *content*:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The hierarchy organizes *where things live* (server, account, document, element), not *what things mean*. Your tumbler address says nothing about your document's subject, genre, or importance. It says everything about its provenance and ownership.

### Summary

The hierarchical encoding of server, account, document, version, and element in every address is essential to Xanadu's design. It is the mechanism by which four fundamental guarantees — ownership, attribution, decentralized allocation, and scalable range queries — are achieved structurally rather than through fragile metadata. Nelson designed the docuverse as "all really one big forking document" [LM 4/18], and the forking tree encoded in every address is what makes the system's guarantees architectural rather than administrative.

---

## Question 4 [nelson]

> If content is inserted into the middle of a document, must the addresses of all surrounding content remain unchanged, or may the system renumber positions?

### Nelson's Answer

# Address Behavior on INSERT

The answer is both: **V-space positions are renumbered; I-space addresses are unchanged.** This is not a compromise — it is the central architectural insight of Xanadu.

## V-Space: Positions Shift

Nelson is explicit that INSERT renumbers V-space positions after the insertion point:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

V-addresses are ephemeral by design. They represent "where this byte appears in the document right now," and that changes with every edit:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-addresses are always dense and contiguous — no gaps. If you have 100 bytes and insert 10 at position 50, positions 50–100 become 60–110. The system renumbers freely because V-addresses carry no permanence guarantee.

## I-Space: Addresses Never Change

The permanent identity of every byte — its I-space address — is immutable:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The newly inserted content receives fresh I-space addresses (appended to the document's I-stream). The existing content's I-addresses are untouched. INSERT changes only the V→I mapping — which bytes appear at which positions in the current view.

## Why This Works: Links Survive

The separation exists precisely so that links survive editing:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42–4/43]

Links point to I-space content, not V-space positions. When V-space renumbers after an INSERT, every link remains valid because the I-addresses it references have not moved.

## Summary

| Address Type | On INSERT | Guarantee |
|---|---|---|
| **V-space** (position) | Shifts — positions after insertion point increase by insertion length | None. "May be constantly changing." |
| **I-space** (identity) | Unchanged — existing content keeps its permanent address; new content gets fresh addresses | Permanent. "Any address... may be specified by a permanent tumbler address." |

The system *must* renumber V-space positions — that is what editing means. It *must not* change I-space addresses — that is what permanence means. The document is the mapping between them, and INSERT modifies only that mapping.

---

## Question 5 [nelson]

> Must it always be decidable from two addresses alone — without consulting any index — whether they refer to the same document, the same version, or entirely separate accounts?

### Nelson's Answer

## Yes, With One Important Qualification

The tumbler address system is designed so that field-level relationships are **syntactically decidable from the addresses alone**, with no index consultation required. But the *derivation history* between versions within a document family is not fully encoded.

### Why It Works: Self-Describing Structure

Tumbler addresses have **at most three zero digits** that serve as unambiguous field separators:

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

This parsing is purely syntactic. Given any address, you find the zeros and extract four fields:

```
Node . 0 . User . 0 . Document . 0 . Element
```

Given two addresses, comparing these fields tells you:

| Question | Method | Index needed? |
|----------|--------|---------------|
| Same account? | Compare Node and User fields | No |
| Same document family? | Compare Document field prefixes | No |
| Same version? | Exact match through Document field | No |
| Entirely separate accounts? | Node+User fields differ | No |

### The Version Subtlety

Within the Document field, versions are created by forking — appending sub-digits:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

So document `5` may have versions `5.1`, `5.2`, `5.3`, and `5.1` may have sub-versions `5.1.1`, `5.1.2`. From addresses alone, you can determine:

- `5.3` is **under** `5` (prefix match)
- `5.1.1` is **under** `5.1`, which is **under** `5` (prefix chain)
- `5.3` and `5.7` are **siblings under** `5`

This is decidable by simple prefix comparison — no index required.

### What Is NOT Decidable: Derivation

Here is the qualification. Nelson explicitly warns:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The address `5.3` tells you it was *created under* document `5` — the owner of `5` allocated it. But it does not tell you:

- Whether `5.3` was produced by `CREATENEWVERSION(5)` or `CREATENEWVERSION(5.2)`
- Whether `5.3` has any content relationship to `5` at all (it could be a blank sub-document)
- Which version was the *source* for any given fork

The FEBE spec says `CREATENEWVERSION` will produce an address that "will indicate its ancestry" [LM 4/66], but Nelson's qualification at 4/29 limits how much you may infer from that indication. The address encodes *ownership hierarchy* (who allocated it), not *content derivation* (what it was forked from).

### The Element Subspace Is Also Decidable

Within the Element field (after the third zero separator), the subspace indicator distinguishes content types:

- Byte subspace: `...0.1.N` (text positions)
- Link subspace: `...0.2.N` (link instances)

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

So you can also determine from two addresses alone whether they refer to bytes or links within the same document — again, no index needed.

### Summary

The tumbler system is deliberately designed so that the **structural relationships** between addresses — same account, same document family, same version, same subspace — are decidable from the addresses alone through syntactic parsing and prefix comparison. The one thing that escapes purely address-based reasoning is the **derivation graph**: which version was actually the source for which. That requires consulting the system's version history, not just the tumbler strings.

---

## Question 6 [gregory]

> When `tumbleradd(a, b)` is used to shift V-positions during INSERT, is the addition associative — does `tumbleradd(tumbleradd(a, b), c)` always equal `tumbleradd(a, tumbleradd(b, c))` — and does it preserve the total order, so that `a < b` implies `tumbleradd(a, c) < tumbleradd(b, c)` for all positive `c`?

### Gregory's Answer

## KB Synthesis

The knowledge base does **not explicitly document** whether `tumbleradd` is associative or order-preserving. However, I can synthesize relevant structural properties that bear on this question:

## Tumbler Arithmetic Structure

From **[SS-TUMBLER]** (Findings 0001, 0031, 0053, 0055):

1. **Fixed-precision representation**: Tumblers have exactly 16 mantissa digits (`NPLACES = 16`), with an exponent that shifts the decimal point position
2. **Sign-magnitude encoding**: Sign bit separate from magnitude (not two's complement)
3. **Exponent-based scaling**: Similar to floating-point — `exp=0` means first digit is most significant, negative exponents represent sub-positions
4. **Total order**: `tumblercmp` provides a well-defined total order (exponent comparison, then lexicographic mantissa comparison)

## Properties Likely NOT Universal

Given this structure, **associativity likely does not hold** in all cases:

- **Precision limits**: With fixed 16-digit precision, `(a + b) + c` may lose precision differently than `a + (b + c)` when numbers have widely different exponents
- **Similar to floating-point**: The exponent-mantissa structure mirrors floating-point, which is notoriously non-associative due to rounding

From **[SS-TUMBLER]** Finding 0055, there's evidence of special-case handling: `strongsub` has an exponent guard that makes subtraction a no-op when exponents differ (`b.exp < a.exp`). This suggests the arithmetic is not standard mathematical addition but has implementation-specific behaviors.

## Order Preservation Appears to Hold in Practice

From **[INV-MONOTONIC]** (Findings 0033, 0061, 0063): I-address allocation is strictly monotonically increasing, relying on `tumblerincrement(&lowerbound, 0, 1, isaptr)`. This suggests that for the **specific operations the system performs** (small positive increments), order is preserved.

From **[ST-INSERT]** (Finding 0054): The two-blade knife mechanism depends on position arithmetic working correctly — entries are classified by comparing `tumbleradd(vpos, width)` results. The system's correct operation suggests order preservation holds for **same-exponent, in-range operations**.

## Critical Limitations

From **[EC-VWIDTH-ZERO-ADDRESS]** Finding 0076: The developer's 1985 comment `/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/` regarding exponent computation suggests **edge cases were not fully analyzed**.

From **[SS-TUMBLER]** Finding 0053: Sign-magnitude representation means there are **two representations of zero** (positive and negative), which complicates arithmetic identity properties.

## Conclusion

**The KB does not establish these properties formally.** For formal verification:

1. **Associativity**: Likely fails for operations across different exponent ranges or near precision boundaries
2. **Order preservation**: Likely holds for `a, b, c` within the same exponent range and no overflow, but **not proven** for the general case

The system's correct operation for **[ST-INSERT]**, **[INV-MONOTONIC]**, and other mechanisms suggests these properties hold **for the specific tumbler ranges and operations the system actually uses** (same-exponent shifts, small increments), but the KB provides **no proof for arbitrary tumblers**.

If these properties are critical for a formal specification, they should be **explicitly verified** against the `tumbleradd` implementation or added as axioms with stated preconditions (e.g., "for positive tumblers with matching exponents").

---

## Question 7 [gregory]

> What happens when tumbler arithmetic produces a result that exceeds the 16-digit mantissa (`NPLACES`): does `tumbleradd` or `tumblerincrement` silently truncate, wrap around, or is the 16-digit limit simply assumed never to be reached in practice?

### Gregory's Answer

## KB Synthesis

# Tumbler Arithmetic Overflow Behavior

**The KB does not explicitly document what happens when tumbler arithmetic exceeds the 16-digit mantissa limit.**

## What the KB Does Document

### Structural Constraints

From [SS-TUMBLER], Finding 0031:
- A tumbler is stored as "a sign bit, a short exponent, and a fixed-length mantissa of `NPLACES` (16) digits"
- The mantissa is a fixed-size array: `short mantissa[NPLACES]` where `NPLACES = 16`
- The exponent shifts the mantissa: `exp = 0` means the first mantissa digit is the most-significant

### Arithmetic Operations

The KB documents several tumbler arithmetic functions but does not describe their overflow behavior:

From [ST-INSERT], Finding 0031:
- `tumblerincrement(&lsa, 0, textset->length, &lsa)` is used during I-address allocation
- The `rightshift=0` parameter means "the increment is applied at the last significant digit"

From [SS-INSERT-VWIDTH-ENCODING], Finding 0076:
- `tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V])` is used to create V-width tumblers
- Special case for zero tumblers: sets `exp = -rightshift`, `mantissa[0] = inc`

From [SS-TUMBLER], Finding 0031:
- `tumblerjustify` is mentioned as a normalization function
- "The exponent/mantissa encoding means two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match (no normalization ambiguity after `tumblerjustify`)"

### Code References

The KB cites `tumble.c:599-623` for `tumblerincrement` implementation, but does not describe its overflow handling.

## What Can Be Inferred

The existence of both an exponent field and a `tumblerjustify` normalization function suggests the system likely handles overflow by:
1. Adjusting the exponent when digits would exceed position 16
2. Renormalizing the mantissa to canonical form

However, **this is inference, not documented behavior.**

## Implications for the Spec

This is a **gap in the knowledge base**. The formal specification would need to address:
1. What `tumblerincrement(t, 0, n)` does when `n` is large enough that the result exceeds 16 digits
2. Whether there's a maximum representable value
3. Whether overflow is impossible by design (e.g., address space partitioning prevents it)
4. What error handling, if any, exists for overflow conditions

The KB provides no evidence of overflow checks, error returns, or bounds on tumbler values beyond the 16-digit mantissa constraint itself.

## Code Exploration

Based on my analysis of the C source code, I can now answer your question comprehensively:

## Answer: Tumbler Arithmetic Overflow Behavior

### `tumblerincrement`: Hard Error on Overflow

**`tumblerincrement` explicitly detects overflow and terminates with an error.**

**[backend/tumble.c:612-619]**
```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
if (idx + rightshift >= NPLACES) {
#ifndef DISTRIBUTION
	dumptumbler (aptr);
	fprintf(stderr," idx = %d  rightshift = %d\n", idx, rightshift);
	gerror ("tumblerincrement overflow\n");
#else
	gerror("");
#endif
}
```

The check `if (idx + rightshift >= NPLACES)` detects when incrementing would write beyond the 16-digit mantissa array. When this occurs, `gerror()` is called, which terminates the program. This makes overflow a **fatal error**.

This matters most for **version chains**: each time you create a new version, the version address becomes deeper by one level (e.g., `1.1` → `1.1.1` → `1.1.1.1`). With NPLACES=16, you can create at most 16 levels of versions before `tumblerincrement` crashes.

---

### `tumbleradd`: Silent Truncation

**`tumbleradd` (via `absadd`) silently truncates results exceeding 16 digits. There is no overflow detection.**

**[backend/tumble.c:480-482]** (in `absadd`)
```c
while ( j <= NPLACES -1 ) {    
	ansmant[j++] = bmant[i++];
}
```

The write loop is bounded by the condition `j <= NPLACES - 1`, which limits writes to array indices 0-15. If the mathematical result would require more than 16 digits, the loop simply **stops writing after position 15**, discarding higher-order digits.

**Critical observation**: The read index `i` is **not** bounds-checked. If the loop runs beyond NPLACES, `bmant[i++]` reads past the end of the mantissa array. This is a memory safety bug that could read garbage data or crash, but in practice it's masked by the write bounds.

The result: **digits beyond position 15 are silently dropped**. No error, no warning.

---

### Practical Impact

The 16-digit limit appears to be a **design assumption**, not a runtime-enforced constraint:

1. **Version chains**: Limited to 16 levels by `tumblerincrement`'s overflow check
2. **Address arithmetic**: Can overflow silently when adding deeply nested addresses
3. **Mixed behavior**: `tumblerincrement` crashes, but `tumbleradd` truncates

### Evidence from Usage

Looking at actual call sites in [backend/granf2.c:162-175], [backend/orglinks.c:37-43], and [backend/insertnd.c:179-182], I see that:
- `tumblerincrement` is called with small rightshift values (0-2) and small increments
- The code structure suggests the authors expected shallow address hierarchies
- The NPLACES definition comment **[backend/common.h:53]** says: "increased from 11 to 16 to support deeper version chains" — this was clearly a known constraint that was later expanded

### Conclusion

The 16-digit limit is **assumed never to be reached in normal operation**, but the behaviors differ:

- **`tumblerincrement`**: Fatal error (explicit guard)
- **`tumbleradd`**: Silent truncation (implicit assumption)

This is inconsistent design. The increment operation protects against overflow (presumably because version chains are a known depth risk), but addition assumes you'll never add tumblers deep enough to overflow.

---

## Question 8 [gregory]

> Does `tumblerincrement` always advance the least significant non-zero digit by one, or does its behavior depend on the tumbler's exponent — specifically, does incrementing `1.1.0.2` (a document-level address) produce `1.1.0.3` (next document) rather than `1.1.0.2.0.0.0.0.0.0.0.0.0.0.0.1` (next sub-position)?

### Gregory's Answer

## KB Synthesis

Looking at the knowledge base entries on `tumblerincrement`, I can provide a definitive answer.

**Yes, `tumblerincrement` behavior depends on its `rightshift` parameter, and it produces hierarchically appropriate siblings, not deeply nested sub-positions.**

## Key Evidence

### For `rightshift=0` (text/content allocation)

From [ST-INSERT] (Finding 0033):
```
`tumblerincrement(&lowerbound, 0, 1, isaptr)` to compute the next I-address 
by incrementing the previous highest by 1.

This produces `2.1.0.1.0.1.3.1` → `2.1.0.1.0.1.3.2` → `2.1.0.1.0.1.3.3`
```

From [SS-VERSION-ADDRESS] (Finding 0068):
```
Second version of `1.1.0.1.0.1`:
  upperbound = tumblerincrement(source_doc, depth-1=0, 1)
  Result: `1.1.0.1.0.2` (the next sibling)
```

Both use `rightshift=0` and increment the **last significant digit**, not a deeply nested position.

### For `rightshift=depth-1` (document/address allocation)

From [SS-ADDRESS-SPACE] (Finding 0021):
```
Compute upper bound from the parent (hint) address: 
`upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent

For ACCOUNT → DOCUMENT (depth=2): rightshift = 1
```

This means `tumblerincrement(1.1.0.1, 1, 1)` produces `1.1.0.2` (next account), **crossing the `.0.` boundary** to the appropriate hierarchical level.

### Zero-tumbler special case

From [SS-INSERT-VWIDTH-ENCODING] (Finding 0076):
```
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]) 
creates V-width tumbler with `exp = -shift`, `mantissa[0] = inc`

This produces a tumbler representing `inc * 10^(-shift)`
```

The `rightshift` parameter controls the **exponent/magnitude** of the result.

## Conclusion

`tumblerincrement(1.1.0.2, 0, 1)` produces **`1.1.0.3`** (next document), not `1.1.0.2.0.0.0.0.0.0.0.0.0.0.0.1`.

The function is designed to **respect hierarchical boundaries**. When `rightshift=0`, it increments at the current level (last significant digit). When `rightshift > 0`, it increments at hierarchically higher levels, producing proper sibling addresses within the tumbler hierarchy.

This behavior is critical for [ST-ADDRESS-ALLOC] - the allocation mechanism uses `depth-1` as `rightshift` specifically to produce addresses at the correct hierarchical level, whether allocating sibling documents under an account or child versions under a document.

## Code Exploration

Based on my analysis of the source code, I can definitively answer your question:

## Answer

**`tumblerincrement` behavior depends on the `rightshift` parameter, NOT on the tumbler's exponent.** The function always finds the least significant non-zero digit, then adds at position `idx + rightshift`.

## Source Code Analysis

### Core Logic `[tumble.c:599-623]`

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
  register INT idx;
  
  if (iszerotumbler (aptr)) {
    tumblerclear (cptr);
    cptr->exp = -rightshift;
    cptr->mantissa[0] = bint;
    return(0);
  }
  if (aptr != cptr)
    movetumbler(aptr,cptr);
  for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
  if (idx + rightshift >= NPLACES) {
    /* overflow error */
  }
  cptr->mantissa[idx + rightshift] += bint;
  tumblerjustify (cptr);
}
```

**Key line `[tumble.c:611]`:**
```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
```
This finds the **rightmost (least significant) non-zero digit** by decrementing from `NPLACES` until hitting a non-zero value.

**Key line `[tumble.c:621]`:**
```c
cptr->mantissa[idx + rightshift] += bint;
```
The increment happens at position **`idx + rightshift`**, where:
- `idx` = position of least significant non-zero digit
- `rightshift` = parameter controlling whether to increment laterally (0) or extend deeper (>0)
- `bint` = value to add (typically 1)

### For Your Example: `1.1.0.2`

Given tumbler `1.1.0.2`:
- `mantissa[0] = 1`
- `mantissa[1] = 1`
- `mantissa[2] = 0`
- `mantissa[3] = 2`

The loop finds `idx = 3` (position of the "2").

**With `rightshift = 0, bint = 1`:**
- `mantissa[3 + 0] += 1` → `mantissa[3] = 3`
- Result: **`1.1.0.3`** (next document)

**With `rightshift = 1, bint = 1`:**
- `mantissa[3 + 1] += 1` → `mantissa[4] = 1`
- Result: **`1.1.0.2.1`** (sub-address, first child)

## Call Site Evidence

The codebase uses both patterns:

**Lateral increment `[do1.c:395]`:**
```c
tumblerincrement(&text_subspace_start, 0, 1, &text_subspace_start);
```
Creates `1` from zero tumbler (document-level address).

**Depth extension `[granf2.c:237]`:**
```c
tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
```
Creates first child under a hint by using `depth` (1 or 2) as rightshift.

**Conditional logic `[granf2.c:240]`:**
```c
tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
```
Uses `depth` if creating a new level, `0` if incrementing at the same level.

## Conclusion

**The tumbler's exponent is NOT consulted.** The function:
1. Finds the least significant non-zero digit position (`idx`)
2. Adds the value at `idx + rightshift`
3. The caller controls whether increment is lateral (rightshift=0) or extends deeper (rightshift>0)

Therefore, incrementing `1.1.0.2` produces:
- **`1.1.0.3`** when called with `rightshift=0` (next document)
- **`1.1.0.2.1`** when called with `rightshift=1` (first sub-position)

It will **never** produce `1.1.0.2.0.0.0.0.0.0.0.0.0.0.0.1` because that would require `rightshift=12` (to skip 11 zero positions), which no caller uses.

---

## Question 9 [gregory]

> Does `tumbleradd` have an exponent guard analogous to `strongsub`'s — where adding a width with a lower exponent than the target is a no-op — or is the exponent guard unique to subtraction, making INSERT's subspace isolation depend on the two-blade mechanism rather than on arithmetic properties?

### Gregory's Answer

## KB Synthesis

# Answer: No exponent guard in `tumbleradd` — INSERT uses structural protection, DELETE uses arithmetic protection

**`tumbleradd` does NOT have an exponent guard analogous to `strongsub`**. The two operations achieve subspace isolation through fundamentally different mechanisms:

## DELETE: Arithmetic Protection (Incidental)

[SS-TUMBLER Finding 0055] documents that `strongsub` at `tumble.c:534-547` contains an exponent guard at line 544:

```c
if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }
```

When DELETE attempts `tumblersub(2.1, 0.3)` (link position minus text width):
- Link displacement `2.1` has exponent `0`
- Deletion width `0.3` has exponent `-1`
- Guard condition: `-1 < 0` → TRUE
- Result: returns `2.1` unchanged

This protection is **arithmetic** — the operation is attempted but made into a no-op by the exponent guard.

## INSERT: Structural Protection (Deliberate)

[SS-TWO-BLADE-KNIFE Finding 0054] documents that INSERT uses a two-blade knife where the second blade is explicitly computed at the next subspace boundary via `findaddressofsecondcutforinsert()`:

```
INSERT at 1.x → blades [1.x, 2.1)
```

The classification in `insertcutsectionnd` (edit.c:207-233) checks entries against `blade[1]` BEFORE any arithmetic:

```c
cmp = whereoncrum(blade[1], grasp, &reach, &totaloffset, &fullcrumptr->cwid);
if (cmp <= ONMYLEFTBORDER) { // case 2: at/beyond blade[1]
    return(2);  // NO SHIFT
}
```

Link entries at `2.1` are classified as case 2 because `2.1 >= blade[1]` (ONMYLEFTBORDER). Case 2 entries **never reach the shift code**. The `tumbleradd` at edit.c:162 is only called for case 1 entries.

This protection is **structural** — cross-subspace entries are filtered out before the arithmetic operation is attempted.

## The Asymmetry

[INT-DELETE-SUBSPACE-ASYMMETRY Finding 0067] explicitly documents this difference:

> "INSERT's protection is robust — it was designed intentionally (the source contains explanatory comments). DELETE's protection is accidental — there is no comment suggesting awareness of the exponent guard as a subspace protection mechanism. If `strongsub` were modified to handle cross-exponent subtraction correctly, DELETE would break subspace isolation while INSERT would remain safe."

**Implication**: If you somehow forced an INSERT operation to call `tumbleradd(2.1, 0.3)` directly (bypassing the knife classification), it would produce `2.4` — there is no arithmetic guard to prevent cross-subspace addition. The entire safety mechanism is the two-blade knife preventing such calls.

**Citations**: [SS-TUMBLER], [SS-TWO-BLADE-KNIFE], [FC-SUBSPACE], [INT-DELETE-SUBSPACE-ASYMMETRY]

## Code Exploration

Perfect! I have all the information needed to answer your question. Let me provide a comprehensive answer with code citations.

---

## Answer

**`tumbleradd` does NOT have an exponent guard analogous to `strongsub`'s.** The exponent guard is unique to subtraction, making INSERT's subspace isolation depend entirely on the two-blade mechanism, while DELETE's protection is an accidental byproduct of arithmetic properties.

## Code Evidence

### strongsub Has an Exponent Guard

`[tumble.c:544-547]`:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr,cptr);
    return(0);
}
```

**When the subtrahend has a lower (more negative) exponent than the minuend, `strongsub` returns the minuend unchanged.** This is the guard. For example, `strongsub(2.1, 0.3)` where `2.1` has exp=0 and `0.3` has exp=-1 returns `2.1` unmodified.

### absadd Has NO Exponent Guard

`[tumble.c:460-478]`:
```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;
    ansmant[0] = amant[0] + bmant[0];
    i = j = 1;
} else if (aptr->exp > bptr->exp) {
    answer.exp = aptr->exp;
    temp = aptr->exp-bptr->exp;
    while ( i < temp ) {
        ansmant[j++] = amant[i++];
    }
    ansmant[j++] = amant[i++] + bmant[0];
    i = 1;
} else {
    answer.exp = bptr->exp;
    temp = bptr->exp - aptr->exp;
    while (i <= temp) {
        ansmant[j++] = bmant[i++];
    }
}
```

**There is no early return when exponents differ.** Instead, `absadd` aligns the mantissas by padding with the higher-exponent operand's leading digits, then performs addition across all levels. Addition with mismatched exponents proceeds normally: `absadd(2.1, 0.2)` produces `2.3`.

### tumbleradd Delegates to absadd

`[tumble.c:374-383]`:
```c
} else if (aptr->sign == bptr->sign) {
    absadd (aptr, bptr, cptr);
    cptr->sign = aptr->sign;
    /*absadd returns justified result so no need to justify*/
```

For positive operands (the INSERT case), `tumbleradd` calls `absadd`, inheriting its lack of exponent guard.

## Implications for Subspace Isolation

### INSERT: Two-Blade Mechanism (Deliberate Design)

`[insertnd.c:143-146]`:
```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V],&knives.blades[1]);
knives.nblades = /*1*/2;
knives.dimension = V;
```

INSERT explicitly computes a second blade at the next subspace boundary using `findaddressofsecondcutforinsert` `[insertnd.c:173-182]`. For an insert at `1.x`, this produces blade[1] at `2.1`, causing `insertcutsectionnd` to classify link crums at `2.1` as case 2 (no shift). **`tumbleradd` is never even called for them.**

### DELETE: Exponent Guard (Accidental Protection)

`[edit.c:39-40]`:
```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

DELETE constructs blades as `[origin, origin + width]`, e.g., `[1.1, 1.4]`. There is **no call to `findaddressofsecondcutforinsert` or equivalent.** For a link crum at `2.1`:

1. `deletecutsectionnd` classifies it as case 2 (shift) `[edit.c:235-248]`
2. `tumblersub(2.1, 0.3)` is called `[edit.c:62]`
3. This routes through `tumbleradd(2.1, -0.3)` → `strongsub(2.1, 0.3)` `[tumble.c:428, 385]`
4. The exponent guard triggers: `-1 < 0` returns `2.1` unchanged

**The link is not shifted, but only because `strongsub`'s exponent check acts as an implicit guard.**

## Summary Table

| Operation | Arithmetic Function | Exponent Guard? | Subspace Protection |
|-----------|-------------------|----------------|---------------------|
| **INSERT** | `tumbleradd` → `absadd` | **NO** | Two-blade mechanism (deliberate) |
| **DELETE** | `tumblersub` → `strongsub` | **YES** (line 544) | Exponent guard (accidental) |

## Why This Matters

As documented in **Finding 0055** `[findings/0055-delete-does-not-shift-link-subspace.md:149-160]`:

> INSERT needs an explicit second blade because the shift operation (`tumbleradd`) CAN cross hierarchy levels. Adding `0.2` to `2.1` would produce `2.3` -- the exponents align during addition. So without the second blade, INSERT WOULD shift link crums.
>
> DELETE does not need an explicit second blade because the shift operation (`tumblersub`) has an implicit guard in `strongsub`: subtraction with mismatched exponents returns the minuend unchanged. This is an accidental property of the implementation, not a deliberate design choice (there is no comment explaining it as a subspace guard).

**The asymmetry is a fragility risk**: if `strongsub` were "fixed" to handle cross-exponent subtraction, DELETE would break subspace isolation.

---

## Question 10 [gregory]

> Can two distinct tumbler representations (different exponent/mantissa combinations) compare as equal under `tumblercmp` but unequal under `tumblereq`, or does `tumblerjustify` guarantee a canonical form so that order-equivalence and equality always agree?

### Gregory's Answer

## KB Synthesis

Looking at the relevant KB entries, I can answer this question precisely.

From [SS-TUMBLER] Finding 0031 and [INV-TUMBLER-TOTAL-ORDER]:

**The answer is NO** — `tumblercmp` and `tumblereq` cannot disagree on equality. Both compare the **representation**, not the mathematical value.

## How the comparison functions work

**`tumblereq`** (from [SS-TUMBLER] Finding 0031):
- Compares sign, exponent, and all 16 mantissa digits
- Returns TRUE only if all fields match exactly

**`tumblercmp`** (from [INV-TUMBLER-TOTAL-ORDER] Finding 0031):
- First checks for zero tumblers
- Then compares signs  
- Then uses `abscmp` which:
  - First compares exponents (larger exponent → larger value)
  - Then compares mantissa digits lexicographically left-to-right
- Returns EQUAL only if sign, exponent, and all mantissa digits match

Since both functions compare the same fields (sign, exponent, mantissa), they **agree on equality**:
- If `tumblercmp(a,b) = EQUAL`, then `tumblereq(a,b) = TRUE`
- If `tumblereq(a,b) = TRUE`, then `tumblercmp(a,b) = EQUAL`

## The role of `tumblerjustify`

From [SS-TUMBLER] Finding 0031: *"two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match (no normalization ambiguity after `tumblerjustify`)"*

This statement reveals the subtle issue: **multiple representations CAN exist for the same value** before normalization.

For example, 0.123 could be represented as:
- `exp=-1, mantissa=[1,2,3,0,0,...]` (normalized form)
- `exp=0, mantissa=[0,1,2,3,0,...]` (unnormalized with leading zero)

Both represent the same mathematical value. However:
- `tumblercmp` would return **LESS** (comparing exp: -1 < 0)
- `tumblereq` would return **FALSE** (different exponent)

Both functions compare **representation**, not **value**. They agree that these are unequal representations, even though the mathematical values are the same.

## Conclusion

The comparison functions **never disagree** with each other. They can both report inequality for mathematically equal values if the tumblers are unnormalized. The phrase "no normalization ambiguity after `tumblerjustify`" means normalization produces a **canonical form** where representation uniquely determines value — but the KB doesn't confirm that this normalization is enforced everywhere in the system as an invariant.

## Code Exploration

I have read the relevant source code and can now answer your question based on direct code analysis.

## Answer: Order-Equivalence vs Equality in Tumbler Comparisons

**No, different exponent/mantissa combinations cannot compare as equal under `tumblercmp`.** However, **`tumblerjustify` does NOT guarantee that order-equivalence and equality always agree** due to metadata fields that are ignored by ordering comparisons.

### Part 1: Different Exp/Mantissa Cannot Compare Equal

The `tumblercmp` function delegates to `abscmp` for comparing absolute values:

**[tumble.c:72-85]** - `tumblercmp`:
```c
INT tumblercmp(tumbler *aptr, tumbler *bptr)
{
    if (iszerotumbler(aptr)){
        if (iszerotumbler(bptr))
            return (EQUAL);
        else
            return (bptr->sign ? GREATER : LESS);
    }
    if (iszerotumbler(bptr))
        return (aptr->sign ? LESS : GREATER);
    if (aptr->sign == bptr->sign)
        return (aptr->sign ? abscmp(bptr,aptr) : abscmp(aptr,bptr));
    return (aptr->sign ? LESS : GREATER);
}
```

**[tumble.c:92-97]** - `abscmp` exponent comparison:
```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp) {
        return(LESS);
    } else {
        return(GREATER);
    }
}
```

The `abscmp` function **immediately returns LESS or GREATER if exponents differ**. It only proceeds to compare mantissa digits if `aptr->exp == bptr->exp` (line 98). Then it requires all mantissa digits to match exactly (lines 99-110).

Therefore, for `tumblercmp` to return `EQUAL`, tumblers must have:
- Identical sign
- Identical exp
- Identical mantissa digits

**Conclusion:** Different exp/mantissa combinations representing the "same" mathematical value cannot compare as equal. `tumblerjustify` removes leading zeros to create a canonical (sign, exp, mantissa) representation.

### Part 2: The Metadata Field Problem

However, the tumbler struct has **five** fields, not just three:

**[common.h:59-65]** - Tumbler structure:
```c
typedef struct structtumbler {
    humber xvartumbler;        // Variable-length representation pointer
    char varandnotfixed;       // Variable vs fixed flag
    char sign  BIT ;           // 1 if negative, 0 otherwise
    short exp;                 // Exponent
    tdigit mantissa[NPLACES];  // Mantissa digits (NPLACES=16)
} tumbler;
```

**[tumble.c:24-36]** - `tumblereq` checks ALL fields:
```c
bool tumblereq(tumbler *a, tumbler *b)
{
    register INT i;
    /* Use field-by-field comparison to avoid issues with struct padding */
    if (a->xvartumbler != b->xvartumbler) return FALSE;      // ← Checked
    if (a->varandnotfixed != b->varandnotfixed) return FALSE; // ← Checked
    if (a->sign != b->sign) return FALSE;
    if (a->exp != b->exp) return FALSE;
    for (i = 0; i < NPLACES; i++) {
        if (a->mantissa[i] != b->mantissa[i]) return FALSE;
    }
    return TRUE;
}
```

**[tumble.c:289-313]** - `tumblerjustify` only normalizes three fields:
```c
int tumblerjustify(tumbler *tumblerptr)
{
    register INT i, j;
    INT shift;
    tdigit *mantissaptr;
    
    mantissaptr = tumblerptr->mantissa;
    if (mantissaptr[0] != 0) {
        return(0);
    }
    for (shift = 0; mantissaptr[shift] == 0; ++shift) {
        if (shift == NPLACES - 1) {
            tumblerptr->exp = 0;         // ← Modifies exp
            tumblerptr->sign = 0;        // ← Modifies sign
            return(0);
        }
    }
    for (i = 0, j = shift; j < NPLACES;)
        mantissaptr[i++] = mantissaptr[j++];  // ← Shifts mantissa
    while (i < NPLACES)
        mantissaptr[i++] = 0;
    tumblerptr->exp -= shift;            // ← Adjusts exp
    // NOTE: xvartumbler and varandnotfixed are NEVER touched
}
```

### The Discrepancy

`tumblerjustify` creates canonical forms for **(sign, exp, mantissa)** but leaves **(xvartumbler, varandnotfixed)** untouched.

Since:
- `tumblercmp` only examines **(sign, exp, mantissa)** via `abscmp`
- `tumblereq` examines **all five fields**
- `tumblerjustify` only normalizes **three fields**

**Therefore:** Two tumblers with:
- Identical (sign, exp, mantissa)
- Different (xvartumbler, varandnotfixed)

Would be:
- **Order-equivalent**: `tumblercmp(a, b) == EQUAL`
- **Not equal**: `tumblereq(a, b) == FALSE`

### Evidence from Usage

**[tumble.c:456-457]** - `absadd` clears metadata fields:
```c
answer.xvartumbler = 0;
answer.varandnotfixed = 0;
```

This suggests that arithmetic operations may not preserve these metadata fields, potentially creating tumblers with identical mathematical values but different metadata.

## Final Answer

**`tumblerjustify` does NOT guarantee that order-equivalence and equality always agree.**

While it prevents different exp/mantissa combinations from comparing as equal (by enforcing a canonical representation with no leading zeros), it does not canonicalize the `xvartumbler` and `varandnotfixed` metadata fields. These fields are:
- Ignored by `tumblercmp` [tumble.c:72-85]
- Checked by `tumblereq` [tumble.c:28-29]
- Left unmodified by `tumblerjustify` [tumble.c:289-313]

Therefore, tumblers can be order-equivalent without being truly equal.
