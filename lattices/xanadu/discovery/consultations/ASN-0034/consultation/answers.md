# Consultation Answers — Tumbler Algebra

**Inquiry:** What algebraic properties must the Xanadu addressing system satisfy? What ordering, arithmetic, and structural guarantees do tumblers provide?
**Date:** 2026-03-12 23:17
**Questions:** 19 (9 nelson, 10 gregory)

---

## Question 1 [nelson]

> Must every address in the system be comparable to every other — can the system ever encounter two addresses where neither is "before" the other?

### Nelson's Answer

## Every Address Is Comparable: The Tumbler Line Is a Total Order

**Yes, every address is comparable to every other.** Nelson designed the tumbler system so that all addresses form a single linear sequence — he consistently calls it "the tumbler line" — and no two addresses can be incomparable.

### The Totality Guarantee

The tumbler system maps a hierarchical tree (servers → accounts → documents → versions → elements) onto a flat linear sequence via depth-first ordering. This traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other.

Nelson states this explicitly:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

The real line is totally ordered. Nelson's comparison is deliberate — the tumbler line shares this property, differing only in that its "population" is determined by the tree it represents rather than being fixed a priori:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

"Finite but unlimited" and "not definite" refer to the *contents* growing over time (new addresses baptized), not to any incomparability between existing addresses. The mapping is always flat — always a line.

### How Comparison Works

Tumblers are sequences of unbounded integers ("digits") separated by minor dividers (periods), with zeros serving as major field dividers. The depth-first ordering gives a concrete comparison algorithm:

1. Compare digit by digit, left to right
2. At the first difference, the smaller digit comes first
3. If one tumbler is a prefix of the other, the shorter one (the parent) comes first

The example sequence from the curated sources illustrates this:

```
1, 1.1, 1.1.2, 1.1.2.1, 1.1.2.2, 1.1.3, 1.2, 1.2.1, 1.2.65, 1.2.65.831, 1.3, ...
```

Every pair here has a definite ordering. No ambiguity, no incomparability.

The zero field-separators integrate into this naturally. A zero at position *n* is simply the digit zero, which is less than any positive digit. So all of User 1's content under Server 1 (`1.0.1.0.…`) comes before any sub-server address (`1.1.…`), because `0 < 1` at the third position.

### Why This Matters: Spans Require Totality

The total ordering is not incidental — it is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." [LM 4/25]

If two addresses were incomparable, the interval between them would be undefined, and spans would not work. The entire machinery of span-sets, request-sets, and endset-based link search depends on "between address A and address B" always having a definite meaning.

### The Arithmetic Reachability Caveat

Nelson does note one asymmetry in tumbler *arithmetic* (as opposed to tumbler *comparison*):

> "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." [LM 4/25]

This is about **computational reachability via addition of difference tumblers**, not about ordering. You can always *compare* any two addresses, but you cannot always *reach* one from the other through tumbler addition alone. The ordering is total; the arithmetic is not symmetric.

### Summary

The system **never** encounters two addresses where neither is "before" the other. The tumbler line is a total order by construction — it is a depth-first linearization of the docuverse tree. This totality is required by the span mechanism, which is in turn required by the link and search mechanisms. Nelson's repeated use of "the tumbler line" and his comparison to the real line are precise: like the real line, every two points are comparable.

---

## Question 2 [nelson]

> Between any two adjacent addresses, must there always be room to assign a new address, or can the address space between two points ever be exhausted?

### Nelson's Answer

# Between Any Two Addresses, There Is Always Room

The address space between two points can **never** be exhausted. This is fundamental to the design — indeed, it is the entire reason tumblers exist.

## The Forking Mechanism

Tumblers grow by subdivision, not by counting upward into some ceiling. Between address 2 and address 3, I can create 2.1, 2.2, 2.3, and so on indefinitely. Between 2.1 and 2.2, I can create 2.1.1, 2.1.2, 2.1.3. This nesting has no limit:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

And each of those daughters can herself have daughters, without limit.

## The Guarantee

This is stated explicitly as the core addressing invariant:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The word "continually" is doing real work there. It means the process never terminates. There is no state in which you have used up the space between two points.

## Not Like the Integers

People accustomed to conventional numbering think "between 2 and 3 there is nothing." But tumblers are not integers. The tumbler line is a flattening of a tree, and trees grow downward without bound:

> "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between. But the tumbler line is a different kind of abstraction from the real line. The real line is the same under all circumstances. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited." [LM 4/22]

**Finite but unlimited.** At any moment the tree has finitely many nodes. But it can always grow. A span that today contains nothing may tomorrow contain a million documents:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

## Why This Matters

If the space between two addresses could be exhausted, the entire system would fail. You would need to renumber, which would break every existing reference. The permanent-address guarantee — the foundation of permanent citation, permanent links, permanent literature — depends absolutely on the inexhaustibility of the address space.

This is what makes tumblers different from file paths, database keys, or URLs. Those systems can run out of names in a given namespace. Tumblers cannot. The owner of any address can always create sub-addresses beneath it, without coordinating with anyone, without risk of collision, and without disturbing any existing address.

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Each digit in the tumbler is an unbounded integer (a "humber"), and the number of digits is itself unbounded. The address space is infinite in two dimensions: each digit can grow without limit, and the depth of nesting can grow without limit.

> "This is a curious, bizarre, powerful, consistent, non-obvious and hard-to-visualize system. It also has a certain quirkiness and charm. Call it a hack, yes; but it is definitely a superhack." [LM 4/40]

---

## Question 3 [nelson]

> What distinct levels does an address contain, and what does each level uniquely identify — a user, a document, a position within content?

### Nelson's Answer

# Tumbler Address Levels

A Xanadu tumbler address contains **four major fields**, separated by three zero-digit dividers:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

---

## Level 1: Node (Server)

Identifies the **physical server or station** in the network. Always begins with digit `1`, since all servers descend from the root.

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Servers can fork sub-servers: `1.2` is a descendant of `1`. This forms the network topology.

## Level 2: User (Account)

Identifies the **owner/account** on that server. The user field is continually subdividable for sub-accounts.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

Ownership flows from this field — the User portion of an I-address permanently records who created the content.

## Level 3: Document (including Versions)

Identifies the **logical document**. This field can be further subdivided to indicate versions and sub-documents:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

So `1.0.3.0.7` is document 7 under account 3 on server 1. If that document has version 2, it becomes `1.0.3.0.7.2` — the version extends the document field, not a separate major field.

## Level 4: Element (Contents)

Identifies **individual bytes or links** within a document version. This field has two subspaces:

**Bytes** (content positions):
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

**Links** (stored connections):
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

The `0.1` prefix designates bytes; `0.2` designates links. Links are numbered sequentially by creation order and are not rearrangeable.

---

## The Hierarchy as Ownership Delegation

Each level delegates to the next through "baptism" — the owner of a number can create sub-numbers beneath it:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "So the docuverse is all really one big forking document." [LM 4/18]

---

## Summary Table

| Level | Field | Identifies | Example | Who assigns it |
|-------|-------|-----------|---------|----------------|
| 1 | Node | Server/station | `1.2` | Parent server |
| 2 | User | Owner/account | `1.2.0.5` | Server operator |
| 3 | Document | Document + version | `1.2.0.5.0.3.1` | Account owner |
| 4 | Element | Byte or link position | `1.2.0.5.0.3.1.0.1.47` (byte 47) | System (append-only) |

The three zeros act as punctuation separating the four semantic tiers. Each field is independently extensible without limit, and the entire scheme imposes no structure on content — it is purely a mapping mechanism:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]

---

## Question 4 [nelson]

> Must newly assigned addresses always be greater than all previously assigned addresses, or may the system fill in gaps retroactively?

### Nelson's Answer

## Addresses Are Inserted, Not Appended

The system explicitly inserts new addresses between existing ones. This is the defining capability of the tumbler addressing scheme — and the reason Nelson chose it.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid."
> — [LM 4/19]

The word is **inserted**, not appended. The forking mechanism creates children beneath any existing address, and those children fall between the parent and its next sibling on the tumbler line.

### How Forking Creates "Retroactive" Addresses

Suppose addresses 2.1 and 2.2 already exist. When 2.1 later acquires a child, the tumbler line becomes:

```
..., 2.1, 2.1.1, 2.2, ...
```

Address 2.1.1 is **newer** than 2.2 in creation time but **smaller** on the tumbler line. The depth-first tree ordering guarantees this:

> "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree."
> — [LM 4/25]

Every subtree maps to a contiguous range. Children always fall within their parent's range, which necessarily places them before the parent's next sibling.

### Sequential Within a Level, Not Globally

At any single level of the hierarchy, siblings are created sequentially:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2."
> — [LM 4/20]

So you create 2.1, then 2.2, then 2.3 — never skipping ahead. But each of those can later spawn children that fill in the space between them on the tumbler line. The owner of any address controls subdivision beneath it:

> "The owner of a given item controls the allocation of the numbers under it."
> — [LM 4/20]

### Spans Anticipate Future Population

Nelson makes the consequence explicit — a range that is empty today may be populated later:

> "A span that contains nothing today may at a later time contain a million documents."
> — [LM 4/25]

A span between two existing addresses is a valid, meaningful range even when empty. Content can be created within it at any future time through forking.

### The Tumbler Line Is Not Fixed

Unlike the real number line, the tumbler line is determined by what has been created so far:

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited."
> — [LM 4/22]

Every forking operation adds new points to the line, potentially between any existing points.

### Summary

| Level | Ordering rule |
|-------|--------------|
| **Siblings** (same parent) | Sequential — 2.1 before 2.2 before 2.3 |
| **Global tumbler line** | NOT monotonic by creation time — children of 2.1 are inserted before 2.2 regardless of when they're created |
| **Spans** | May be empty now, populated later |

The system does not merely permit filling gaps — **filling gaps is the fundamental growth mechanism**. The entire docuverse grows by forking, and forking always inserts rather than appends. This is why Nelson called it "a superhack" [LM 4/40] — it achieves permanent addressing in an ever-growing space precisely because new addresses slot into the existing structure rather than requiring global renumbering.

---

## Question 5 [nelson]

> Must a contiguous range of addresses be expressible as a compact pair (start, end), and must every such range denote an unbroken sequence of content units?

### Nelson's Answer

## Compact Pairs and Unbroken Sequences in Tumbler-Space

### Part 1: Compact Pair Representation — YES

Every contiguous range of tumbler addresses is expressible as a compact pair. This is the **span** mechanism, and it is fundamental to the design.

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse" [LM 4/24]

Nelson specifies two equivalent compact representations:

1. **Pair of tumblers** — start address and end address
2. **Address + difference tumbler** — start address plus a "width" tumbler

Tumbler arithmetic converts between these forms. The difference representation is more compact when the span is small relative to the addresses.

This compactness is a design requirement, not a convenience. The entire FEBE protocol operates on spans and span-sets. Link endsets are span-sets. Retrieval targets are span-sets. Search constraints are span-sets. Without compact pair representation, the protocol would be unworkable.

The "1-positions" reinforce this — a single span can express selections at any scale:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

---

### Part 2: Unbroken Sequence of Content Units — NO (at the docuverse level)

A span denotes a contiguous range of **address space**, not a contiguous sequence of **content units**. Nelson is explicit that the region a span covers may be sparse, heterogeneous, or entirely empty:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

The tumbler line is a depth-first linearization of a tree. A span cuts a contiguous region from that linearization. Within that region:

- **Ghost elements** may exist — addresses with nothing stored [LM 4/23]
- **Entire empty subtrees** may exist — accounts with no documents, servers with no content
- **Heterogeneous content** may be included — bytes, links, documents, servers all share the same line

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

Nelson visualizes this as a zone:

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." [LM 4/25]

The zone includes whatever populates it. The span's boundaries determine the region; the region's population is a separate fact about the state of the docuverse.

---

### The V-Stream Exception

Within a single document's **V-stream** (virtual byte stream), addresses ARE dense and contiguous. V-addresses form a gap-free sequence from position 1 to position N. There are no ghost elements in V-space. INSERT shifts subsequent addresses; DELETE closes gaps.

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

So a V-span within a single document version DOES denote an unbroken sequence of content units. This is by design — V-space is the user's view, and users expect sequential addressing within a document.

The distinction is:

| Space | Dense? | Span = unbroken sequence? |
|-------|--------|--------------------------|
| **V-space** (within one document version) | Yes — contiguous positions 1..N | Yes |
| **I-space** (within one document's native bytes) | Yes — append-only, sequential | Yes |
| **Tumbler-space** (across the docuverse) | No — ghost elements, empty subtrees | No |

---

### Why This Matters

For non-contiguous selections, Nelson specifies **span-sets** (collections of spans):

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." [LM 4/25]

This is how link endsets work — each endset is an arbitrary span-set, potentially discontiguous, potentially spanning multiple documents. The compact pair representation applies to each individual span within the set, but the set as a whole can cover arbitrary scattered regions.

---

### Summary

A contiguous range of tumbler addresses is always expressible as a compact pair — this is architecturally required. But such a range does NOT necessarily denote an unbroken sequence of content units at the docuverse level. It denotes a region of address space whose population is determined by the current state of the tree. Within a single document's V-stream, however, spans do denote unbroken sequences, because V-space is dense by construction.

---

## Question 6 [nelson]

> What is the finest granularity an address can identify — a single character, a byte, or some other atomic unit of content?

### Nelson's Answer

## The Byte Is the Atomic Unit

The finest granularity a tumbler address can identify is **a single byte**. Nelson is consistent and explicit about this throughout the technical specification.

### Direct Evidence

The stored entities are bytes and links — nothing smaller:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links."
> — [LM 4/23]

V-space addresses resolve to individual byte positions:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."
> — [LM 4/30]

Spans explicitly bottom out at one byte:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network."
> — [LM 4/24]

Links attach to bytes, not to any finer unit:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes."
> — [LM 4/42]

### Byte, Not Character

Nelson occasionally uses "characters" informally — for example, "spans of characters" [LM 4/24] — but the technical specification always says **bytes**. This matters because the system is media-agnostic. The same addressing works for text, images, audio, and any other digital content. A "byte" is the universal atomic unit; a "character" is one possible front-end interpretation of bytes.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control."
> — [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document."
> — [LM 4/11]

### Summary

A tumbler address identifies a single byte. Spans address contiguous ranges of bytes. Span-sets address arbitrary (possibly discontiguous) collections of bytes. Every operation in FEBE works in terms of bytes and spans of bytes. There is no sub-byte addressing, and "character" is used only as informal shorthand — the architectural atom is the byte.

---

## Question 7 [nelson]

> When two addresses share a common prefix, what relationship must hold between the things they identify — must they belong to the same containing scope?

### Nelson's Answer

## Yes — shared prefix means shared containing scope

The tumbler system is explicitly a **tree flattened onto a line**. A common prefix means the two addresses descend from the same node in that tree — they belong to the same containing scope.

Nelson states this directly:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

The tumbler line is not an arbitrary number line — it is a specific tree's depth-first linearization:

> "The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "The contents of the tumbler line are determined by the population of entities and relations on the tree it represents." [LM 4/22]

### What "same scope" means concretely

The four major fields define the containment hierarchy:

```
Node.0.User.0.Document.0.Element
```

If two addresses share prefix `1.2.0.3`, they are under the same user account (`3`) on the same server (`1.2`). If they share `1.2.0.3.0.7`, they are in the same document (`7`). The containment is structural — forking creates daughter items, and ownership flows downward:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

This is why spans work as subtree selectors — a span covering a prefix captures everything beneath it:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

And why ghost elements work — linking to an account address implicitly references all documents under it:

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

### The important caveat: scope, not semantics

Shared prefix means shared **administrative scope** (same server, same account, same document), but NOT shared subject matter or semantic relationship:

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17–4/18]

Two documents under the same account are owned by the same user. That is the only relationship the prefix guarantees. Nelson is explicit that tumblers are about *where things live* in the ownership tree, not *what they mean*.

### Summary

Shared prefix → same containing scope in the ownership/containment tree. This is not a convention but a structural invariant: the prefix IS the path from the root of the tree to the common ancestor. The relationship is containment and ownership, never semantic categorization.

---

## Question 8 [nelson]

> Must the difference between two addresses within the same level be arithmetically meaningful — for instance, must it tell you how many content units lie between them?

### Nelson's Answer

## No. The difference between two tumbler addresses is not a count of anything.

Nelson is explicit and emphatic on this point:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything."
> — [LM 4/24]

The difference between two addresses specifies **boundaries**, not **cardinality**. What lies between those boundaries depends on the actual population of the tree — which is dynamic and unpredictable:

> "A span that contains nothing today may at a later time contain a million documents."
> — [LM 4/25]

### Why the arithmetic doesn't yield a count

The tumbler line is not the real number line. It is a depth-first flattening of a tree whose population changes as content is created:

> "The tumbler line is an abstract representation of a particular tree... The contents of the tumbler line are determined by the population of entities and relations on the tree it represents. Thus the tumbler line is not definite in the same way as the real line; the tumbler line is a flat mapping of a particular tree, finite but unlimited."
> — [LM 4/22]

Between any two sibling addresses (say document 3 and document 7 under the same account), the "distance" of 4 tells you nothing about how many items exist there, because:

1. **Forking creates subtrees.** Document 5 might have subdivisions 5.1, 5.2, 5.3... each with further descendants. The span from 3 to 7 encompasses all of them — their count is unknowable from the addresses alone. [LM 4/20]

2. **Ghost elements may occupy positions.** Addresses can be referenced even when nothing is stored there. A span sweeps over occupied and ghost positions alike. [LM 4/23]

3. **The content is implicit in the boundaries, not computable from them:**

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point."
> — [LM 4/25]

### The one exception: V-space byte positions

Within a single document version, V-space byte addresses **are** dense sequential integers (1, 2, 3, ... N) with no gaps — by definition, INSERT shifts subsequent addresses and DELETE closes gaps [LM 4/66]. So in V-space, the difference between position 10 and position 20 does correspond to 10 byte positions. But this is a property of V-space's contiguous virtual stream, not of tumbler arithmetic in general. Nelson explicitly notes that V-addresses are ephemeral and "may be continually altered by editorial operations" [LM 4/30].

### What tumbler arithmetic *is* for

Tumbler arithmetic supports **span manipulation** — computing whether one address falls within a span, combining spans, computing difference tumblers for compact representation. It is an addressing calculus, not a counting calculus:

> "In one big flash of insight, Mark Miller saw that everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system."
> — [LM 4/16]

The arithmetic makes addresses **manipulable** (you can compute offsets, test containment, define ranges). It does not make them **cardinal** (you cannot derive population from distance).

---

## Question 9 [nelson]

> If a user creates content across multiple sessions, must the addresses assigned in each session form a contiguous block, or may they be interleaved with other users' addresses?

### Nelson's Answer

## Addresses Are Never Interleaved Between Users

The tumbler hierarchy structurally prevents interleaving. Each user's content lives in its own subtree of the address space, completely isolated from every other user's subtree.

### Why: The Ownership Principle

Tumbler addresses encode a strict hierarchy: `Node.0.User.0.Document.0.Element`. The key mechanism is **baptism** — whoever owns a number controls all sub-numbers beneath it:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

If Alice is account `1.0.2` and Bob is account `1.0.3`, then:
- Alice's documents are `1.0.2.0.1`, `1.0.2.0.2`, `1.0.2.0.3`...
- Bob's documents are `1.0.3.0.1`, `1.0.3.0.2`, `1.0.3.0.3`...

Bob cannot create anything at an address under `1.0.2` — he doesn't own it. Alice cannot create anything under `1.0.3`. Their address spaces are disjoint by construction.

### Contiguity on the Tumbler Line

Tumblers map to a linear sequence via depth-first tree ordering. All of Alice's content occupies a contiguous range on this line, and all of Bob's content occupies a separate contiguous range:

> "The tumbler line is an abstract representation of a particular tree." [LM 4/22]

Within Alice's subtree, her documents are numbered sequentially. If she creates document 1 in session 1 and document 2 in session 5, they are `Alice.0.1` and `Alice.0.2` — contiguous in her subtree regardless of how many sessions elapsed or what other users did in between.

Within a single document, element addresses are also sequential:

> "The digit after the one indicates the byte position in the current ordering of bytes." [LM 4/30]

### Physical Storage Is a Separate Concern

There is a distinction between **logical addresses** (tumblers) and **physical storage** (the append-only store). Nelson describes content being "filed, as it were, chronologically" [LM 2/14] in the physical store. So physically, bytes from different users' sessions may be interleaved in the append-only stream. But the **I-space addresses** are tree-structured, not chronological. The enfilades bridge this gap — mapping from logical tumbler addresses to physical locations:

> "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely." [LM 1/36]

### Summary

| Level | Interleaved? | Why |
|-------|-------------|-----|
| Between users | Never | Different subtrees; ownership prevents cross-allocation |
| Between documents (same user) | Never | Documents numbered sequentially under user's account |
| Within a document (across sessions) | Never | Elements numbered sequentially within document |
| Physical storage bytes | May be | Append-only; chronological; but this is invisible to addressing |

The answer is unambiguous: **addresses need not and cannot be interleaved between users.** The tumbler tree structure guarantees that each user's addresses form a contiguous subtree, and the ownership/baptism mechanism makes it impossible for one user to allocate addresses within another user's subtree.

---

## Question 10 [gregory]

> Is `tumblersub(a, b)` intended to be a true group subtraction (always yielding a valid distance), or are there tumbler pairs where the negative result is a representation artifact that should never appear in practice?

### Gregory's Answer

## KB Synthesis

The KB evidence points to **representation artifact** — negative results from `tumblersub` are not intended valid distances.

## The case for "always valid group subtraction"

The type system was clearly built with negative tumblers in mind. `tumblersub` negates the subtrahend's sign and calls `tumbleradd` [SS-TUMBLER, Finding 0053], `tumblercmp` correctly sorts negative tumblers before all positives [INV-TUMBLER-TOTAL-ORDER], and the sign-magnitude encoding is structurally consistent. The capability exists.

## Why it's actually a representation artifact

**Intended use context is always non-negative.** The primary consumer of `tumblersub` is span width computation: `width = tumblersub(end, start)` in `granf2.c:106` [SS-SPAN]. This is only called when `end >= start` by construction — a negative width has no meaningful interpretation in a content span.

**Negative V-positions from DELETE are explicitly described as a missing precondition violation.** [PRE-DELETE, Finding 0053] states directly that a *complete* precondition for DELETE should include `∀ entry : entry.vpos > delete_end ⟹ entry.vpos - delete_width ≥ 0`. The fact that this is labeled a *missing precondition* rather than a design choice confirms negative results are unintended. [INV-POOM-BIJECTIVITY] further confirms: entries with negative V-positions "exist in the POOM tree but maps to no valid V-address" — leaked dead state, not valid negative distances.

**The `strongsub` exponent guard is incidental protection, not intentional design.** [SS-TUMBLER, Finding 0055] shows that cross-exponent subtraction returns the minuend unchanged — but this was not designed as a guard against underflow. It's an arithmetic side effect that happens to prevent cross-subspace corruption. [INT-DELETE-SUBSPACE-ASYMMETRY] explicitly flags this as a fragile, unintentional invariant.

**No operation consumes negative tumblers.** The system has `iszerotumbler()` to detect zero, but no `isnegativetumbler()` used in any meaningful data structure path. Negative results have nowhere to go — they become invisible entries that cannot even be targeted by a subsequent DELETE (their V-position is unreachable by any positive-valued span argument).

## Summary

`tumblersub` was built as a general signed arithmetic operation — a complete implementation — but the **intended domain is non-negative results**. The sign-magnitude representation is an implementation convenience (subtraction-as-negation-plus-addition), not a design feature for negative distances. When the precondition `a >= b` is violated, the result is not a valid distance in any address space; it's undefined behavior that manifests as invisible leaked POOM entries [EC-DEEPLY-ORPHANED-LINK].

---

## Code Exploration

I now have a complete picture. Here is my full analysis:

---

## `tumblersub`: True Group Subtraction, with Intentional Negative Intermediates

### The Implementation

`tumblersub(a, b, c)` [tumble.c:406–440] is implemented as full signed arithmetic: it negates `b->sign` and delegates to `tumbleradd` [tumble.c:426–428]. `tumbleradd` dispatches to `absadd`, `strongsub`, or `weaksub` depending on signs and relative magnitude [tumble.c:374–396]. The `sign` field in the tumbler struct is a genuine signed-magnitude bit [common.h:62]:

```c
char sign  BIT ;  /* 1 if negative, otherwise 0 */
```

The tumbler representation explicitly supports negative values. `tumblercheck` [tumble.c:169–227] validates a negative tumbler as legal — it only rejects `sign=1` when `mantissa[0] == 0` (negative zero), not when `sign=1` in general [tumble.c:180–183]:

```c
if (ptr->sign && ptr->mantissa[0] == 0){
    fprintf(stderr," negative zero ");
    wrong = TRUE;
}
```

So **negative tumblers are a valid state** in the representation, not an artifact.

---

### The Commented-Out Debug Sentinels

The most revealing evidence is the two diagnostic blocks commented out inside `tumblersub` [tumble.c:409–417, 432–438]:

```c
/*
    if(aptr->sign || bptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEG IN \n");
        ...
    }
*/
...
/*
    if (cptr->sign) {
        fprintf(stderr,"TUMBLERSUB NEGATIVE OUTPUT\n");
        ...
    }
*/
```

These were *observability* probes, not *defensive guards*. They were added to monitor how often the function received signed inputs or produced signed outputs, then commented out once the developers understood the call sites. They do not reject negative results — they were watching for them. Their existence confirms the authors knew negative outputs could occur.

---

### Call Sites: Two Distinct Usage Modes

**Mode 1 — Width/span arithmetic (majority of sites):** The caller guarantees `a ≥ b`, so negative output indicates a logic error. Examples:

- `edit.c:63`: `tumblersub(&ptr->cdsp.dsas[index], width, ...)` — reducing a crum's displacement by `width`, where `width ≤ displacement` by construction.
- `correspond.c:319,327`: `tumblersub(&span2->width, &span1->width, ...)` — used only inside a switch branch that has already compared the widths.
- `orglinks.c:377,381`: width calculations for new spans inside `vspanset2ispanset`, called only when `spanptr->stream ≤ oldspanend` is known.
- `makeroom.c:31`: `tumblersub(&grasp->dsas[i], &origin->dsas[i], &base)` — entered only inside `if (tumblercmp(&origin->dsas[i], &grasp->dsas[i]) == LESS)` [makeroom.c:26], so `base > 0` is guaranteed.

In all these sites a negative result would mean a tree invariant had been violated upstream.

**Mode 2 — Geometric offset arithmetic (edit.c):** The caller deliberately computes a signed displacement. This is the clearest proof of intentional negative use.

`edit.c:178–180`:
```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
tumblersub (&knives->blades[1], &knives->blades[0], &diff[2]); /* should be negative */
diff[2].sign = !diff[2].sign;
```

The comment `/* should be negative */` is explicit. The sign is then flipped on the next line to convert the result to a positive absolute value for use as an offset. Crucially, the *same computation* could have been written as `tumblersub(blades[0], blades[1], diff[2])`, but the developer chose to express the geometric semantics as a negative and then flip.

`edit.c:174–176`:
```c
/*  tumblersub (&knives->blades[0], &knives->blades[2], &(diff[3]));*/  /* should be <0 */
movetumbler (&diff[1], &diff[3]);
diff[3].sign = !diff[1].sign;
```

The `/* should be <0 */` call was commented out and replaced with a manual sign-flip of `diff[1]` — but the intent is the same: produce a negated distance. The replacement avoids an unnecessary `tumblersub` call when the value is already computed.

---

### `strongsub` and `weaksub` Are Internal, Not Asymmetric

These two helpers [tumble.c:534–589] implement magnitude subtraction where `|a| ≥ |b|` is a precondition. They are only invoked from inside `tumbleradd` [tumble.c:384–393], after `abscmp` has already established which operand is larger. They are not exposed as the general subtraction interface — `tumblersub` is. The use of `strongsub`/`weaksub` internally does not mean the outer operation is restricted to non-negative results.

---

### Conclusion

`tumblersub(a, b)` **is a true signed group subtraction**. It always yields a valid tumbler value — including negative ones. Negative results are not representation artifacts; they are legitimate values that the type supports and that callers sometimes deliberately produce (as signed geometric offsets in `edit.c`).

The design intent has two tiers:

1. **Span/width arithmetic**: callers establish `a ≥ b` as a precondition and expect a positive result. A negative result here would indicate an upstream invariant violation, which the (now-commented-out) `"TUMBLERSUB NEGATIVE OUTPUT"` probe was designed to catch during development.

2. **Rearrangement offset arithmetic** (`edit.c:makeoffsetsfor3or4cuts`): negative results are *intended*, explicitly noted with comments like `/* should be negative */`, and consumed by immediately flipping the sign to form a positive displacement in the opposite direction.

The function is general; the non-negativity assumption is a *caller responsibility*, not a function contract. Nothing in `tumblersub` prevents or rejects negative output.

---

## Question 11 [gregory]

> The `strongsub` exponent guard (line 544 of `tumble.c`) returns `a` unchanged when `b.exp < a.exp` — was this an intentional algebraic design choice to make subtraction a no-op across exponent classes, or a defensive guard against a specific bug?

### Gregory's Answer

## KB Synthesis

The KB evidence points toward an algebraic property of the implementation rather than a deliberate defensive guard — but cannot fully resolve the intent question.

**What the KB establishes:**

[SS-TUMBLER] Finding 0055 characterizes it explicitly: *"This is not a deliberate subspace guard — it is a property of how `strongsub` handles cross-exponent arithmetic."* The guard at `tumble.c:544` reads: `if (bptr->exp < aptr->exp) { movetumbler(aptr, cptr); return(0); }` — when the subtrahend has a smaller exponent than the minuend, return the minuend unchanged.

**The algebraic reading:**

Tumblers use a sign-magnitude representation where the exponent encodes hierarchical scale. `2.1` (exp=0) and `0.3` (exp=-1) operate at fundamentally different scales — one is an address like a street address, the other is an offset like a room number. Under this interpretation, `strongsub` is saying: *I don't know how to subtract a sub-scale quantity from a whole-scale quantity, so I return the whole unchanged*. That's a coherent algebraic position, not obviously wrong.

**The fragility evidence:**

[INT-DELETE-SUBSPACE-ASYMMETRY] is unambiguous: INSERT's subspace isolation was *deliberately designed* — `findaddressofsecondcutforinsert()` has explanatory source comments about its purpose. DELETE's subspace isolation through `strongsub` has no such comments. This asymmetry is described as a "fragility risk" — if someone "corrected" `strongsub` to handle cross-exponent subtraction, DELETE would break subspace isolation while INSERT would remain unaffected [FC-SUBSPACE, Finding 0055].

**My read:**

The `strongsub` behavior looks like a pragmatic algebraic decision — cross-exponent subtraction was either undefined or unneeded for the use cases at hand, so the implementation returns the minuend unchanged rather than attempting mixed-scale arithmetic. Whether that was a conscious design choice or the path of least resistance is unknowable from the code alone.

What I'm confident about: it was *not* inserted as a subspace protection mechanism. That's a consequence the original authors appear not to have noticed or documented. The KB has no citation showing anyone wrote "this guard protects subspace isolation in DELETE" — that connection was only reconstructed by analysis [Finding 0055].

---

## Code Exploration

Now I have everything I need. Let me write the full analysis.

---

## The `strongsub` Exponent Guard at `tumble.c:544`

### What the guard does

```c
// tumble.c:534-565
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
  tumbler answer;
  register INT i, j;

    tumblerclear(&answer);
    if (tumblereq (aptr, bptr)) {           // line 540 — equal case: return zero
        movetumbler (&answer, cptr);
        return(0);
    }
    if (bptr->exp < aptr->exp) {            // line 544 — THE GUARD
        movetumbler(aptr,cptr);
        return(0);
    }
    answer.exp = aptr->exp;
    for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {   // line 549
        --answer.exp;
        ...
    }
    answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];  // line 556
```

When `bptr->exp < aptr->exp`, the guard fires and returns `aptr` unchanged into `cptr`.

---

### What `exp` means

From `common.h:59-65`, the tumbler struct:

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;
    short exp;               // exponent of most-significant digit; always <= 0
    tdigit mantissa[NPLACES]; // NPLACES = 16
} tumbler;
```

`tumblercheckptr` (`tumble.c:174`) treats `exp > 0` as a hard error (`"bad exp"`). So `exp` is always `<= 0`. The mantissa digit at `mantissa[i]` is at hierarchical scale `i` levels below `exp`. Larger `exp` (less negative) means larger magnitude — confirmed by `abscmp` at `tumble.c:92-97`:

```c
if (aptr->exp != bptr->exp) {
    if (aptr->exp < bptr->exp) {
        return(LESS);
    } else {
        return(GREATER);
    }
}
```

A tumbler with `exp=0, mantissa=[3]` is address `3`. With `exp=-1, mantissa=[3,2]` it is address `3.2` — a sub-address one level deeper. Comment in `common.h:53`: NPLACES was *"increased from 11 to support deeper version chains"* — confirming that `exp` depth is the version/sub-version hierarchy.

---

### When `strongsub` is called

`functiontumbleradd` at `tumble.c:384-395`:

```c
} else if (abscmp (aptr, bptr) == GREATER) {
    strongsub (aptr, bptr, cptr);          // |a| > |b|
    cptr->sign = aptr->sign;
    ...
} else {
    weaksub (bptr, aptr, cptr);            // |b| >= |a|
    cptr->sign = bptr->sign;
    ...
}
```

`strongsub` is called exactly when `|a| > |b|`. Since `abscmp` ranks purely by `exp` when exponents differ (`tumble.c:92-97`), `|a| > |b|` is satisfied in two cases:

1. **Same exponent** (`a.exp == b.exp`) but `a.mantissa > b.mantissa`
2. **Different exponents** (`a.exp > b.exp`) — regardless of mantissa

The guard at line 544 fires exclusively in case 2.

---

### Why the algorithm below the guard would fail without it

The core loop at `tumble.c:549-556`:

```c
answer.exp = aptr->exp;
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
```

This compares `a.mantissa[i]` to `b.mantissa[i]` positionally, assuming both start at the same scale. It works correctly when `a.exp == b.exp`.

When `a.exp > b.exp` — say `a.exp = 0` and `b.exp = -1` — `a.mantissa[0]` is at level 0, but `b.mantissa[0]` is at level −1 (one hierarchy deeper). Comparing them positionally is category confusion: the algorithm would compute `a[0] − b[0]` as if they're at the same scale, producing a value that has no correct interpretation in either address space. There is no conditional, shift, or alignment step in `strongsub` for this cross-exponent case.

**Contrast with `weaksub`** (`tumble.c:567-589`), which IS called with cross-exponent tumblers (when `|b| >= |a|`, `b.exp >= a.exp`). It handles the mismatch correctly:

```c
answer.exp = aptr->exp;          // aptr here is the LARGER arg (b in the outer call)
expdiff = aptr->exp - bptr->exp; // >= 0
for (i = 0; i < expdiff; ++i) {
    answer.mantissa[i] = aptr->mantissa[i]; // copy high-order digits of a not reached by b
}
answer.mantissa[i] = aptr->mantissa[i] - bptr->mantissa[0]; // subtract at the overlap point
```

`weaksub` explicitly computes `expdiff` and copies the non-overlapping high-order digits of the larger argument first. `strongsub` has no such mechanism. The asymmetry is the key tell: whoever wrote `weaksub` knew how to handle cross-exponent subtraction, yet `strongsub` lacks it.

---

### Is returning `a` mathematically correct?

Only in a truncation sense. If `a = 5` (exp=0) and `b = 0.32` (exp=−1), then `a − b = 4.68`, not `5`. The guard returns `5`, which is wrong in exact arithmetic.

However, there is a plausible precision rationale: when `b.exp < a.exp`, `b`'s most-significant digit is at a finer hierarchical level than `a`'s least-significant digit. If `b` falls entirely below `a`'s resolution, the truncated result would be `a`. The guard fires on *any* exponent mismatch, not just the truly-negligible case — so it over-applies this truncation. It does not check whether `|b|` is actually below the least-significant digit of `a`.

---

### Was there a specific bug this prevented?

There is no comment on the guard, no named bug reference, and no disabled test pointing to a crash here. What the code record does show is:

- The guard was written inline, without any diagnostic `fprintf` or `gerror` branch (unlike the many other guards in `tumblercheckptr` and elsewhere that do emit diagnostics for truly invalid states). This implies it was not written as a hard-error catch.
- The body `movetumbler(aptr,cptr); return(0)` is identical in structure to the `tumblereq` equality guard two lines above — both are silent no-ops. The pair reads as two "bail out early if this case won't work" guards, not as one assertion and one design choice.
- `weaksub` correctly handles the analogous cross-exponent case via `expdiff`, but `strongsub` never got that treatment. The most parsimonious explanation is that `strongsub`'s algorithm was written only for the same-exponent case, and the guard was added to prevent the broken path from executing when real data occasionally triggered the cross-exponent branch.

---

### Verdict

The guard at `tumble.c:544` is **a defensive measure against a broken algorithm path, not an intentional algebraic design choice.**

The algorithm below it (`tumble.c:549-556`) is only correct when `a.exp == b.exp`. It has no mechanism to align digits from different exponent levels. Without the guard, it would silently produce garbage when `a.exp > b.exp`. The guard was added to make `strongsub` safe for that input rather than to define a principled "subtraction across exponent classes is a no-op" semantics.

The result of returning `a` unchanged is a coincidental approximation — defensible only when `b` happens to be negligibly small relative to `a`'s precision, which the guard does not verify. The absence of any explanatory comment, the absence of an error branch, and the contrast with `weaksub`'s explicit `expdiff` handling all point to a quick protective fix rather than a deliberate algebraic invariant.

---

## Question 12 [gregory]

> Is the tumbler number line dense — can you always construct a tumbler strictly between any two distinct tumblers — or does the fixed 16-digit mantissa impose a minimum gap where no intermediate value can be represented?

### Gregory's Answer

## KB Synthesis

The tumbler number line is **not dense** at its finest representable scale, though the exponent mechanism provides a practical approximation of density for hierarchical address construction.

## What the KB tells us

**The representation is finite-precision by construction.** [SS-TUMBLER] Finding 0031 establishes that a tumbler is stored as a sign bit, a short exponent (`exp`), and a fixed-length mantissa of exactly `NPLACES = 16` digit positions. The exponent shifts the mantissa: `exp = 0` places the first digit at the most significant position; negative exponents represent sub-unit fractional positions.

**Adjacent values can exist at the digit level.** [SS-TUMBLER] Finding 0031 documents the increment primitive: `tumblerincrement(&lsa, rightshift, count, &result)` advances a tumbler by `count` units at the digit position indexed by `rightshift`. At `rightshift = 0` (the least significant occupied digit), incrementing by 1 produces the immediate successor — the next representable tumbler at that exponent level. [SS-ADDRESS-SPACE] Finding 0033 confirms this: sequential inserts receive tumblers exactly 1 apart (`tumblerincrement(&lowerbound, 0, 1, isaptr)`), and these are treated as adjacent with no intermediate address in the allocation scheme.

**The exponent is bounded.** The exponent is described as "a short exponent" in [SS-TUMBLER] Finding 0031, corresponding to a `SINT` (short integer in C, typically 16-bit, range −32768 to 32767). This places a floor on representable precision.

## The density conclusion

Between two tumblers A and B that differ only in the last mantissa digit by exactly 1 (same exponent, finest granularity), the exponent mechanism *could* in principle provide an intermediate by using `exp - 1` to represent a finer subdivision. But:

1. If the exponent is already at its minimum value, no more negative exponent is available, and the pair `{A, A+1}` at that scale has **no representable intermediate**.

2. [INV-MONOTONIC] treats the sequence as discrete: allocation always takes `max_existing + 1` with no interpolation step, confirming the implementation treats the I-address space as a sequence of discrete points, not a dense continuum.

3. [SS-ADDRESS-ALLOC] Finding 0021 shows the address allocation algorithm explicitly: find the highest existing address, truncate, and increment by 1 — the same integer-step model.

**Therefore: the tumbler number line is not mathematically dense.** It has the structure of a high-precision but finitely-quantized number system. At any given exponent level, adjacent integers (differing by 1 in the last digit) are truly adjacent — no tumbler with the same exponent fits between them. Finer precision requires a more negative exponent, but the 16-bit exponent bound means there is a finest granularity below which no further subdivision is representable.

The `.0.` hierarchical convention in address construction (depth parameters in [SS-ADDRESS-SPACE] Finding 0021, [SS-ADDRESS-ALLOC]) does allow inserting child addresses between any parent and its successor — but this is structural containment (appending `.0.N`), not numerical interpolation between two arbitrary adjacent values.

---

## Code Exploration

The finding has been prepared. Here is the full answer based on the source code:

---

## The Tumbler Number Line Is Not Dense

**The fixed 16-digit mantissa imposes a minimum gap. There exist pairs of adjacent tumblers with no representable value between them.**

---

### The Representation

From `common.h:53`:
```c
#define NPLACES 16  /* increased from 11 to support deeper version chains */
```

From `common.h:57–65` and `defs.h:12`:
```c
typedef UINT tdigit;   /* uint32_t */

typedef struct structtumbler {
    humber xvartumbler;
    char   varandnotfixed;
    char   sign  BIT;   /* 1 if negative */
    short  exp;         /* must be <= 0 */
    tdigit mantissa[NPLACES];
} tumbler;
```

A tumbler encodes a dotted address like `3.1.4` as `exp=0, mantissa=[3, 1, 4, 0, …]`. Leading zeros are not stored — the parser (`get2.c:81–83`) decrements `exp` and discards them, so `0.3.1` becomes `exp=-1, mantissa=[3, 1, 0, …]`.

**Validity constraint:** `tumblercheck` at `tumble.c:174–178` enforces `exp <= 0`. `exp > 0` is a hard error.

---

### The Ordering

`abscmp` (`tumble.c:87–111`):

1. Compare `exp` first: **larger `exp` → greater value** (so exp=0 > exp=−1)
2. If equal `exp`: **lexicographic mantissa** comparison slot-by-slot

---

### Two Families of Hard Gaps

#### Gap 1 — Between exp levels

Let:
- **A** = exp=−1, mantissa=`[UINT_MAX, UINT_MAX, …, UINT_MAX]` — the address `0.MAX.MAX…` at depth 16
- **B** = exp=0, mantissa=`[1, 0, …, 0]` — the address `1`

Any candidate M strictly between A and B must have:

| M's `exp` | Consequence |
|-----------|-------------|
| `exp < −1` | M < A — wrong direction |
| `exp = −1` | M ≤ A at best — can't exceed `[MAX,MAX,…]` |
| `exp = 0`, `mantissa[0] = 0` | **Invalid** — `tumble.c:186–190` rejects non-normalized: `exp ≠ 0` with `mantissa[0] = 0` is a hard error |
| `exp = 0`, `mantissa[0] ≥ 1` | M ≥ B |

**No representable tumbler exists between A and B.** This gap exists at every exp-level boundary.

#### Gap 2 — At full depth within the same exp

Given:
- **A** = exp=0, mantissa=`[k, UINT_MAX, UINT_MAX, …, UINT_MAX]` (all 16 slots filled)
- **B** = exp=0, mantissa=`[k+1, 0, 0, …, 0]`

Any M with A < M < B at exp=0 needs `mantissa[0] = k` and `mantissa[1..15] > [UINT_MAX, …, UINT_MAX]` — impossible — or `mantissa[0] = k+1`, giving M ≥ B.

**Minimum representable gap:** 1 unit at `mantissa[15]`, with the same `exp` and same `mantissa[0..14]`. Nothing finer exists.

---

### Code Evidence the Gaps Are Known and Intentional

**`strongsub` discards sub-scale differences.** `tumble.c:544–547`:
```c
if (bptr->exp < aptr->exp) {
    movetumbler(aptr, cptr);
    return(0);
}
```
When B's exp is smaller than A's (B is at finer scale), `A − B` returns `A`. The difference is below representable precision — the tumbler analogue of floating-point underflow. **Explicit and deliberate.**

**`tumblerincrement` has a hard overflow guard.** `tumble.c:611–619`:
```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
if (idx + rightshift >= NPLACES) {
    gerror("tumblerincrement overflow\n");
}
```
No way to push a depth-16 tumbler further right.

**The protocol parser rejects depth > 16.** `get2.c:88–90`:
```c
if (eatchar(taskptr, '.')) {
    fprintf(taskptr->errp, "tumbler overflow\n");
    return(FALSE);
}
```

**`absadd` has no carry propagation.** `tumble.c:462`:
```c
ansmant[0] = amant[0] + bmant[0];  /* no carry */
```
Each digit slot is independent. An overflow at `mantissa[15]` wraps silently (C unsigned arithmetic) rather than carrying into `mantissa[14]`. There is no arithmetic path to bridge a depth-16 gap.

**The NPLACES comment records the history.** `common.h:53`:
```c
#define NPLACES 16  /* increased from 11 to support deeper version chains */
```
The depth limit was a real bottleneck at 11 and was raised to 16 pragmatically. The ceiling is architectural, not accidental.

---

### Conclusion

The tumbler space is a **finite lattice**, not a continuum.

- **At shallow depths** (fewer than 16 components): effectively dense — you can always insert a sub-address by appending a new dot-component. No gap.
- **At full depth (16 components)**: discrete. The minimum step is 1 unit at `mantissa[15]`. Nothing smaller is representable.
- **At every exp boundary**: the maximally-deep tumbler at exp=n−1 and the minimal tumbler at exp=n are strictly adjacent — no value fits between them.

The density property holds in the practical range for Xanadu document addresses (which are typically a few levels deep). It fails precisely when you exhaust the 16-slot mantissa or hit an exp-level boundary. The `strongsub` underflow behavior and `tumblerincrement` overflow guard are the two places in the code where this fundamental limitation surfaces explicitly.

---

## Question 13 [gregory]

> Are `tumbleradd` and `tumblersub` inverses of each other for all representable tumblers, i.e., does `tumbleradd(tumblersub(a, b), b)` always recover `a` exactly, or are there precision-loss cases from the fixed mantissa?

### Gregory's Answer

## KB Synthesis

## `tumbleradd`/`tumblersub` as Inverses

**Short answer: No, they are not inverses in general.** The KB documents at least one case where the round-trip `tumbleradd(tumblersub(a, b), b) ≠ a`, and the fixed 16-digit mantissa creates a second potential failure mode.

---

### Case 1: The `strongsub` Exponent Guard (documented)

[SS-TUMBLER] Finding 0055 documents a definitive counterexample. `strongsub` — the implementation backing `tumblersub` — has an exponent guard:

> when the subtrahend's exponent is strictly less than the minuend's exponent, `strongsub` returns the minuend unchanged

So when `b.exp < a.exp`:

```
tumblersub(a, b) = strongsub(a, b) = a   (no-op, not a - b)
tumbleradd(a, b) = a + b  ≠  a
```

The round-trip `tumbleradd(tumblersub(a, b), b)` yields `a + b`, not `a`. Finding 0055 gives a concrete example:

```
strongsub(a={exp=0, mant=[2,1]}, b={exp=-1, mant=[3]}):
  b.exp (-1) < a.exp (0) → TRUE
  Returns a unchanged: {exp=0, mant=[2,1]} = tumbler 2.1
```

This is not a bug in the finding's framing — it's a **deliberate architectural property** that prevents cross-subspace POOM shifts during DELETE ([FC-SUBSPACE], Finding 0055, Finding 0067). But it means subtraction is a partial function, not an invertible one.

---

### Case 2: Fixed-Precision Mantissa Overflow (structural)

[SS-TUMBLER] Finding 0031 establishes:

> A tumbler is stored as a sign bit, a short exponent, and a fixed-length mantissa of `NPLACES` (16) digits.

With only 16 mantissa digits, `tumbleradd` on two tumblers whose sum would require 17+ significant digits must truncate or overflow. The KB doesn't document the exact carry-overflow behavior, but the fixed-width representation makes precision loss structurally possible for sufficiently large or fine-grained tumblers. Since `tumblersub` reduces the magnitude and `tumbleradd` restores it, any truncation introduced during subtraction would propagate — if `c = a - b` loses low-order digits, `c + b` recovers something in the right range but not necessarily `a` exactly.

---

### When the Round-Trip Does Hold

For same-exponent subtraction without mantissa overflow — i.e., when both operands are positive, share the same exponent, and the result fits in 16 digits — the sign-magnitude arithmetic should recover exactly. [SS-TUMBLER] Finding 0053 confirms subtraction is implemented as sign negation plus addition, so same-exponent cases with `a ≥ b ≥ 0` should satisfy `(a - b) + b = a` within precision bounds.

---

### Spec Implications

This matters for [PRE-DELETE] and [FC-SUBSPACE]: the `strongsub` no-op is the mechanism that prevents DELETE from shifting link crums into negative territory across subspace boundaries ([INT-DELETE-SUBSPACE-ASYMMETRY]). It is an **intentional non-inverse** that the spec must capture as a conditional postcondition: `tumblersub(a, b) = a - b` only when `b.exp ≥ a.exp`; otherwise `tumblersub(a, b) = a`.

---

## Code Exploration

I now have everything needed. Here is the full analysis:

---

## Are `tumbleradd` and `tumblersub` inverses?

**No. `tumbleradd(tumblersub(a, b), b)` does not in general recover `a`.** There are multiple distinct failure modes, each traceable to specific code paths in `tumble.c`. None of them involve carry/borrow — because the arithmetic has no carry at all.

---

### The Representation

`tdigit = UINT` (32-bit unsigned), `NPLACES = 16` [`common.h:53,57`].

```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;   /* 1 if negative */
    short exp;       /* always ≤ 0 for valid tumblers */
    tdigit mantissa[NPLACES];
} tumbler;
```
[`common.h:59–65`]

`tumblercheckptr` enforces `exp > 0` as invalid [`tumble.c:174–179`]. After `tumblerjustify`, the first non-zero digit is always at `mantissa[0]`, and `exp` counts how many leading zeros were shifted away (hence always ≤ 0). An address like `0.0.5.3` becomes `{exp=-2, mantissa=[5,3,0,...]}`.

There is **no carry between levels**. Each `mantissa[k]` is an independent integer representing one level of the Xanadu address hierarchy. Zeros in the mantissa are semantically significant separators.

---

### `tumblersub` dispatch

```c
int tumblersub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    if (iszerotumbler(bptr))        movetumbler(aptr, cptr);
    else if (tumblereq(aptr, bptr)) tumblerclear(cptr);
    else if (iszerotumbler(aptr))   { movetumbler(bptr, cptr); cptr->sign = !cptr->sign; }
    else {
        movetumbler(bptr, &temp);
        temp.sign = !temp.sign;
        tumbleradd(aptr, &temp, cptr);   /* a + (-b) */
    }
    tumblerjustify(cptr);
}
```
[`tumble.c:406–440`]

In the general case it negates b and calls `tumbleradd(a, -b, c)`. Since the signs differ, `functiontumbleradd` dispatches based on `abscmp`:

- `|a| > |b|` → `strongsub(a, b, c)`, sign = a's sign  
- `|b| ≥ |a|` → `weaksub(b, a, c)`, sign = b's sign

[`tumble.c:384–396`]

---

### Failure Mode 1 — `strongsub` early return, then `absadd` corrupts the result

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr) {
    tumblerclear(&answer);
    if (tumblereq(aptr, bptr)) { movetumbler(&answer, cptr); return 0; }
    if (bptr->exp < aptr->exp) {            /* ← EARLY RETURN */
        movetumbler(aptr, cptr);
        return 0;
    }
    /* ... skip equal prefix, subtract at first differing digit ... */
}
```
[`tumble.c:534–565`]

When `b.exp < a.exp` (b is deeper in the hierarchy than a), `strongsub` immediately returns `a` unchanged. So `d = tumblersub(a, b) = a`.

Now `tumbleradd(d, b) = tumbleradd(a, b)` where both are positive and `a.exp > b.exp`. This hits the `aptr->exp > bptr->exp` branch of `absadd`:

```c
} else if (aptr->exp > bptr->exp) {
    answer.exp = aptr->exp;
    temp = aptr->exp - bptr->exp;          /* positive */
    while (i < temp) {
        ansmant[j++] = amant[i++];         /* copy a's prefix */
    }
    ansmant[j++] = amant[i++] + bmant[0]; /* add b's first digit into a */
    i = 1;
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];            /* fill from b's suffix */
}
```
[`tumble.c:464–484`]

**Concrete counterexample:**

- `a = {exp=0, mantissa=[1,2,3,0,...]}` — address `1.2.3`
- `b = {exp=-2, mantissa=[5,0,...]}` — address `0.0.5` (two levels deep)

`tumblersub(a, b)`: `abscmp` sees `a.exp(0) > b.exp(-2)` → GREATER → `strongsub` → `b.exp(-2) < a.exp(0)` → returns `a` unchanged. `d = {exp=0, [1,2,3,0,...]}`.

`tumbleradd(d, b)`: same sign, `absadd(d, b)` with `d.exp(0) > b.exp(-2)`, `temp=2`:  
- copies `d[0]=1, d[1]=2` into `answer[0,1]`  
- `answer[2] = d[2] + b[0] = 3 + 5 = 8`  
- fills from `b[1], b[2], ...` (all zero)

**Result: `{exp=0, [1,2,8,0,...]}` — address `1.2.8`, not `1.2.3`.**

---

### Failure Mode 2 — `absadd` else branch silently discards the first operand

The `else` branch of `absadd` (when `bptr->exp > aptr->exp`):

```c
} else {
    answer.exp = bptr->exp;
    temp = bptr->exp - aptr->exp;
    while (i <= temp) {
        ansmant[j++] = bmant[i++];         /* copy b's prefix */
    }
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];             /* copy b's suffix */
}
```
[`tumble.c:473–484`]

`aptr` is **never read**. The result is just `b`'s digits.

This fires whenever the first argument to `tumbleradd` has a more negative `exp` than the second — exactly what happens when `d = tumblersub(a, b)` strips a common prefix.

**Concrete counterexample** (standard same-level addresses):

- `a = {exp=0, [3,5,7,9,0,...]}`, `b = {exp=0, [3,2,1,0,...]}`

`strongsub(a, b)`:
- Skip equal position 0 (both 3): `answer.exp = -1`
- At position 1: `a[1]=5 > b[1]=2`, so `answer.mantissa[0] = 5-2 = 3`
- Copy `a[2]=7 → answer.mantissa[1]=7`, `a[3]=9 → answer.mantissa[2]=9`
- `d = {exp=-1, mantissa=[3,7,9,0,...]}`

`tumbleradd(d, b)`: same sign, `absadd(d, b)` with `b.exp(0) > d.exp(-1)` → **else branch**:
- `temp = 0 - (-1) = 1`  
- copies `b[0]=3, b[1]=2` (inner while: `i <= 1`)  
- outer while: copies `b[2]=1, b[3]=0, ...`

**Result: `{exp=0, [3,2,1,0,...]} = b`, not `a`.**

---

### Failure Mode 3 — `absadd` same-exp branch drops all but the first digit of the smaller operand

When both operands have the same `exp`:

```c
if (aptr->exp == bptr->exp) {
    answer.exp = aptr->exp;
    ansmant[0] = amant[0] + bmant[0];   /* only first digit pair used */
    i = j = 1;
}
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];           /* rest filled from b only */
}
```
[`tumble.c:460–484`]

`a[1], a[2], ...` are completely ignored. Only `a[0]` contributes.

---

### Failure Mode 4 — NPLACES truncation

In `absadd` with `aptr->exp > bptr->exp`:

```c
temp = aptr->exp - bptr->exp;
while (i < temp) {
    ansmant[j++] = amant[i++];
}
ansmant[j++] = amant[i++] + bmant[0];
i = 1;
while (j <= NPLACES - 1) {
    ansmant[j++] = bmant[i++];
}
```
[`tumble.c:466–484`]

If `temp` is large, `b`'s low-order digits are truncated when `j` reaches `NPLACES-1`. Any digit in `b` (or in the result of `tumblersub`) beyond position 15 is silently dropped. Similarly, in `tumblerincrement`:

```c
if (idx + rightshift >= NPLACES) {
    gerror("tumblerincrement overflow\n");
}
```
[`tumble.c:612–619`]

The system treats overflow as a fatal error rather than silently wrapping, but the `absadd` path has no such guard.

---

### Why the code works at all — operand order matters

In actual use, `tumbleradd` is always called as **`tumbleradd(high_level, low_level)`** — the higher-`exp` (shallower) address first:

```c
/* granf2.c:296 */
tumbleradd(&lowerbound, &ispanptr->width, &upperbound);
/* stream first, width second — stream.exp ≥ width.exp */
```

```c
/* orglinks.c:131 */
tumbleradd(vsaptr, &crumwidth.dsas[V], vsaptr);
/* accumulated offset (higher level) + increment (lower level) */
```

In this order, `absadd` uses the `aptr->exp > bptr->exp` branch, which correctly places the high-level prefix and adds the low-level increment at the right position. The **reverse** call `tumbleradd(low, high)` hits the else branch and returns `high` unchanged — it is not an error from the code's perspective, but it does not produce `low + high`.

The identity that holds in practice is:

```
tumbleradd(start, tumblersub(end, start)) == end
```

— **start first**, difference second — because `start.exp ≥ width.exp` after prefix cancellation.

The question's formulation `tumbleradd(tumblersub(a, b), b)` puts the **difference first**, which reverses the expected operand order and triggers the else branch.

---

### Summary table

| Condition | `d = tumblersub(a, b)` | `tumbleradd(d, b)` | Recovers `a`? |
|-----------|------------------------|---------------------|---------------|
| `b == 0` | `d = a` | `a + 0 = a` | ✓ |
| `a == b` | `d = 0` | `0 + b = b = a` | ✓ |
| `a == 0` | `d = -b` | `-b + b = 0 = a` | ✓ |
| `b.exp < a.exp` | `d = a` (strongsub early return [`tumble.c:544`]) | `absadd(a,b)` blends b into a | ✗ |
| Same-level, common prefix | `d.exp` more negative than `b.exp` | `absadd` else branch returns `b` [`tumble.c:473`] | ✗ |
| Same `exp` | `d.exp` more negative after prefix strip | `absadd` same-exp branch drops `a[1..]` [`tumble.c:462`] | ✗ |
| `temp ≥ NPLACES` | Bits overflow | Low-order truncation [`tumble.c:480`] | ✗ |

---

### Conclusion

`tumbleradd` and `tumblersub` are **not inverses** in the general case. The `absadd` implementation is explicitly **asymmetric**: the first argument supplies the high-level prefix; the second supplies the low-level suffix/increment. When `d = tumblersub(a, b)` is computed, the result has a more negative `exp` than `b` (because common prefix digits were cancelled), so `tumbleradd(d, b)` treats `b` as the dominant prefix and discards `d`'s information — returning `b`, not `a`.

Precision loss from the fixed 16-place mantissa is a secondary concern: the **operand-order asymmetry** causes total information loss even before any digit overflow can occur. The arithmetic is correct only in the direction the code actually uses it: `tumbleradd(higher_level_address, lower_level_offset)`.

---

## Question 14 [gregory]

> What was the design rationale for sign-magnitude representation instead of two's complement — was it to make the total order (negative < zero < positive) straightforward in `tumblercmp`, or was there a deeper reason related to hierarchical addressing?

### Gregory's Answer

## KB Synthesis

The KB does not contain the design rationale — no finding records why sign-magnitude was chosen over two's complement. I can offer what the KB makes inferable, but cannot claim this reflects actual design intent.

**What the KB says about the representation:**

From [SS-TUMBLER] Finding 0031: tumblers store a sign bit, exponent, and 16-digit mantissa, with zero digits acting as hierarchical separators (e.g., `1.1.0.2.0.5` encodes a three-level hierarchy). From [SS-TUMBLER] Finding 0053: `tumblercmp` simply orders all negatives before zero before all positives, with absolute magnitude comparison within sign classes.

**What can be inferred:**

The hierarchical separator convention — zeros *within* the mantissa as field delimiters — is likely the deeper reason. In two's complement, the bit pattern for negative numbers would be opaque as a digit sequence; the `1.1.0.2.0.5` style addressing would lose its legibility. Sign-magnitude preserves the digit sequence intact with only a separate sign flag, so the hierarchical structure remains inspectable and the same comparison logic (`abscmp`: exponent first, then lexicographic mantissa) works uniformly across the magnitude.

The `tumblercmp` ordering being "straightforward" is a consequence of sign-magnitude, not a primary motivation — any representation can implement a total order. But sign-magnitude makes the order *obvious*: negative sign flips an otherwise identical comparison, with no wraparound arithmetic to reason about.

Supporting evidence: [SS-TUMBLER] Finding 0055 notes that `strongsub` uses an explicit exponent guard (`b.exp < a.exp → return a unchanged`), which operates directly on the tumbler's structural fields. This kind of direct exponent reasoning would be harder with two's complement encoding.

**Bottom line:** The KB supports inferring that hierarchical digit-sequence legibility drove the representation choice, with the clean total order as a secondary benefit. But this is inference — no KB entry states the rationale explicitly.

---

## Code Exploration

Now I have everything I need. Let me compile the full analysis.

---

## Sign-Magnitude in Tumbler Arithmetic: A Code-Grounded Analysis

The answer is that sign-magnitude was chosen primarily because of **hierarchical addressing semantics** — the digit values must be intrinsically non-negative — and secondarily because the subtraction identity it provides is cleaner. The simple total order in `tumblercmp` is a consequence, not the cause.

---

### 1. The Fundamental Constraint: `tdigit` Is Unsigned

`common.h:57`:
```c
typedef UINT tdigit;
```

And the full struct, `common.h:59-65`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign  BIT ;  /* 1 if negative, otherwise 0 */
    short exp;
    tdigit mantissa[NPLACES];
} tumbler;
```

The mantissa digits are typed as unsigned integers. Sign is a completely *separate* field — a single bit isolated from the digits. This is the defining structural choice.

The validator enforces it explicitly. `tumble.c:202-209`:
```c
for (i = 0; i < NPLACES; ++i){
    if ((INT)(ptr->mantissa[i]) < 0){
        fprintf(stderr,"negative digit");
        wrong = TRUE;
    }
}
```

And negative zero is independently invalid — `tumble.c:180-184`:
```c
if (ptr->sign && ptr->mantissa[0] == 0){
    fprintf(stderr," negative zero ");
    wrong = TRUE;
}
```
Two's complement doesn't have negative zero; that check only makes sense for sign-magnitude.

---

### 2. The Deep Reason: Hierarchical Addresses Have No Negative Digits

A tumbler like `3.7.2` is not an integer — it's a *hierarchical path*. The digits name positions in a containment hierarchy (document → section → subsection). It is semantically meaningless for a digit to be negative. You cannot be at the "−3rd" subsection of something.

The `exp` field encodes depth in the hierarchy (it is validated to be non-positive, `tumble.c:174-178`):
```c
if (ptr->exp > 0){
    fprintf(stderr,"bad exp ");
    wrong = TRUE;
}
```

The `exp` says how many levels deep the implicit decimal point sits. All digits above that point are non-negative path components.

If two's complement were used, negative numbers would corrupt bit `31` of mantissa digits. The hierarchical semantic of "count at level i" would break. `absadd` (`tumble.c:444-485`) operates directly on unsigned digit arrays with no sign involvement — that would be impossible with two's complement encoding in the digits.

---

### 3. The Sign Bit Is Solely for Signed Displacement Arithmetic

Negative tumblers appear only as transient computational intermediates. They **cannot be serialized**. `tumbleari.c:77-78`:
```c
if(ptr->sign)
    gerror("negative tumbler in tumblerfixedtoptr\n");
```

The constant `TUMBLERMINUS = 129` (`common.h:56`) is defined as if for a wire encoding, but `tumblerfixedtoptr` refuses to produce it. Negative tumblers only live in memory, during arithmetic.

The canonical use of sign is in subtraction. `tumble.c:425-428`:
```c
movetumbler (bptr, &temp);
temp.sign = !temp.sign;
tumbleradd (aptr, &temp, cptr);
```

`tumblersub(a, b, c)` negates `b` by flipping its sign bit, then calls `tumbleradd`. This is the sign-magnitude identity `a − b = a + (−b)`. With two's complement you'd need one's complement inversion + increment, which corrupts the digit values and breaks the unsigned-digit invariant.

---

### 4. The Wire Format Depends on Non-Negative Digits

The `humber` encoding scheme (`tumbleari.c`) is a self-delimiting unsigned variable-length integer encoding. Each mantissa digit of a tumbler is encoded separately as a humber (`tumbleari.c:53-62`):
```c
for (i = 0; i < NPLACES && mantissadigitptr < humberEnd; i++) {
    if(mantissadigitptr[0] <=127){
        tptr->mantissa[i] = mantissadigitptr[0];
    }else{
        tptr->mantissa[i] = functionintof(mantissadigitptr);
    }
}
```

Humbers are unsigned: `humberput` (`tumbleari.c:137`) rejects negative values:
```c
if((int)i <0){
    gerror("humberput of negative number\n");
}
```

Two's complement would require a completely different serialization per digit. Sign-magnitude lets each digit be independently encoded as a non-negative humber.

---

### 5. `strongsub` and `weaksub` Are Hierarchical Operations, Not Integer Arithmetic

There are two subtraction operations distinct from `tumblersub` that only make sense with unsigned digits.

`strongsub` (`tumble.c:534-565`) strips a common hierarchical prefix, returning the suffix offset:
```c
for (i = 0; aptr->mantissa[i] == bptr->mantissa[i]; ++i) {
    --answer.exp;
    ...
}
answer.mantissa[0] = aptr->mantissa[i] - bptr->mantissa[i];
```

This finds where two addresses diverge in their hierarchy and returns "how far apart" they are at that level. It is not integer subtraction — it is prefix-stripping. Two's complement digits would break the digit-by-digit prefix comparison.

`weaksub` (`tumble.c:567-589`) subtracts the first digit of `b` from the corresponding position in `a` — a "partial suffix" operation:
```c
answer.mantissa[i] = aptr->mantissa[i] - bptr->mantissa[0];
```

Again, this makes sense only when digits are non-negative path components.

---

### 6. The `tumblercmp` Simplicity Is Real but Derivative

`tumblercmp` (`tumble.c:72-85`):
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

The logic is: same sign → compare absolute values (negatives in reversed order because larger magnitude = more negative); different signs → negative is always less. This is the total order negative < zero < positive, clean and readable.

But this simplicity is a *consequence* of the design, not the reason for it. The deeper reason is that `abscmp` (`tumble.c:87-111`) does unsigned lexicographic comparison of digit arrays:
```c
a = (INT *) aptr->mantissa;
b = (INT *) bptr->mantissa;
for (i = NPLACES; i--;) {
    if(!(cmp = *a++ - *b++)){
    } else if (cmp < 0) {
        return (LESS);
    } else {
        return (GREATER);
    }
}
```

This direct pointer arithmetic over the digit arrays works because digits are unsigned and the address ordering is lexicographic. With two's complement digits the subtraction `*a++ - *b++` would produce wrong results for large values (signed overflow). The comparison function works correctly *because* the digits are unsigned non-negative hierarchical components.

---

### Summary

The sign-magnitude choice is layered in three tiers, from deepest to shallowest:

1. **Deepest — hierarchical semantics**: Tumbler digits are non-negative path components naming levels in a containment hierarchy. They are typed `UINT` (`common.h:57`). This is a semantic constraint, not a numerical one. Two's complement would corrupt the digit semantics.

2. **Middle — wire format and `abscmp`**: The `humber` variable-length encoding is purely unsigned (`tumbleari.c:137`). `abscmp` does unsigned digit-array comparison (`tumble.c:99-108`). Both require that digit values be non-negative. Negative tumblers are therefore never serialized (`tumbleari.c:77-78`).

3. **Shallowest — the subtraction identity**: Sign-magnitude allows `tumblersub` to be implemented as `tumbleradd(a, flip_sign(b))` (`tumble.c:425-428`), a clean algebraic identity. Two's complement would require inversion + increment, touching the digit values themselves.

The total order in `tumblercmp` (negative < zero < positive) falls out naturally from all of this, but it would have been achievable with two's complement too. The real reason is that tumblers are hierarchical addresses, and hierarchical addresses are made of non-negative path components — so the sign of the *address* must live in a dedicated bit separate from those components.

---

## Question 15 [gregory]

> Does `tumblerincrement` always produce the immediate successor in the total order, or does it increment only the least-significant nonzero digit — and if the latter, what is the formal successor relation between tumblers?

### Gregory's Answer

## KB Synthesis

`tumblerincrement` does **not** in general produce the immediate successor in the tumbler total order. It computes `t + n × 10^(-rightshift)` — that is, it adds `n` at a specific digit position determined by `rightshift`.

## What the function does

The signature is `tumblerincrement(source, rightshift, amount, dest)`:

- `rightshift=0, amount=1`: adds 1 at the units position → `t + 1`
- `rightshift=1, amount=n`: adds at the tenths position → `t + n × 0.1`

The zero-tumbler special case [SS-INSERT-VWIDTH-ENCODING] confirms this: `tumblerincrement(&zero, 1, 11, &result)` produces `exp = -1, mantissa[0] = 11`, representing `0.11`.

For I-address allocation [ST-INSERT], Finding 0031: `tumblerincrement(&lsa, 0, textset->length, &lsa)` with `rightshift=0` advances the address by the text length in integer units. For single-character allocation [SS-ADDRESS-SPACE], Finding 0033: `tumblerincrement(&lowerbound, 0, 1, isaptr)` steps by exactly 1.

## Why this is NOT the immediate total-order successor in general

The tumbler total order [INV-TUMBLER-TOTAL-ORDER] is lexicographic: compare signs, then exponents, then mantissa digits left-to-right. This means:

```
1.1.0.2.0.1  <  1.1.0.2.0.1.1  <  1.1.0.2.0.2
```

`tumblerincrement(1.1.0.2.0.1, 0, 1)` yields `1.1.0.2.0.2` — the **next sibling** — skipping over all descendants (`1.1.0.2.0.1.1`, `1.1.0.2.0.1.2`, ...). The KB makes this explicit [SS-ADDRESS-ALLOC], Finding 0021: `upperbound = tumblerincrement(hintisa, depth-1, 1)` is described as "the next sibling of the parent."

The function is deliberately used this way to compute **upper bounds** that fence off subtrees during allocation searches (via `findpreviousisagr`), not to enumerate all tumblers in order.

## When it does produce the total-order successor

For **permascroll atom I-addresses** (e.g., `2.1.0.5.0.100`), `tumblerincrement(t, 0, 1)` yields `2.1.0.5.0.101`, which is the immediate successor. This holds because permascroll I-addresses have no descendants by construction — the allocation scheme never creates sub-tumblers below a content atom address [SS-ADDRESS-SPACE], Finding 0033. So for flat I-address ranges, integer-step increment equals total-order increment.

## The formal successor relation

`tumblerincrement(t, k, n)` computes `t + n × 10^(-k)` in the tumbler numeric representation. The total-order immediate successor of `t` would require knowing the global state: if any tumbler `t'` exists with `t < t' < t + 10^(-k)` (i.e., any descendant of `t`), then `t + 10^(-k)` is not the immediate successor. The function makes no such promise — it is a pure arithmetic operation, not a search over existing addresses.

---

## Code Exploration

Now I have everything needed for a complete answer. Let me synthesize from the source code.

---

## Answer: `tumblerincrement` and the Tumbler Successor Relation

### 1. What `tumblerincrement` actually computes

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
// tumble.c:599
```

The function has two paths:

**Zero-tumbler path** [tumble.c:603–608]: Constructs a new tumbler from scratch — `exp = -rightshift`, `mantissa[0] = bint`. Used when `aptr` is the origin.

**Non-zero path** [tumble.c:609–622]:
```c
for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
// ...
cptr->mantissa[idx + rightshift] += bint;
tumblerjustify (cptr);
```

The loop scans backward from `mantissa[NPLACES-1]` and stops at the **last (highest-index, least-significant) non-zero digit** — call this position `idx`. It then adds `bint` to `mantissa[idx + rightshift]` and normalizes.

So with the canonical call `tumblerincrement(T, 0, 1, T)`:
- `idx` = position of the last nonzero mantissa digit
- `mantissa[idx]` += 1
- All digits after `idx` remain zero (trailing zeros were already there)

### 2. The tumbler data model and total order

From `common.h:59–65` and `defs.h`:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;          // 1 = negative
    short exp;          // always <= 0  [tumblercheckptr, tumble.c:174]
    tdigit mantissa[NPLACES];  // NPLACES=16, each digit is unsigned int
} tumbler;
```

`iszerotumbler` [common.h:72] = `!mantissa[0]`. A normalized non-zero tumbler always has `mantissa[0] != 0`.

The **total order** is defined by `abscmp` [tumble.c:87–111]:
1. Compare `exp` fields: smaller exp (more negative) → LESS.
2. If equal exp, compare `mantissa[0..NPLACES-1]` **lexicographically** from index 0 to 15.

So the order is the strict lexicographic order on the tuple `(exp, mantissa[0], mantissa[1], ..., mantissa[15])`.

### 3. Does `tumblerincrement` produce the immediate successor?

**No.** There are infinitely many tumblers between `T` and `tumblerincrement(T, 0, 1, T')` in the total order.

Consider `T = [A, B]` (exp=0, `mantissa[0]=A, mantissa[1]=B, rest zero`). Then:

```
tumblerincrement(T, 0, 1) → [A, B+1]
```
(`idx=1`, adds 1 to `mantissa[1]`)

But the tumbler `[A, B, 1, 0, ...]` (exp=0) has:
- Same `mantissa[0]=A`, same `mantissa[1]=B`, then `mantissa[2]=1`
- Lexicographically: `[A, B, 1, ...] > [A, B, 0, ...]` = T  ✓
- Lexicographically: `[A, B, 1, ...] < [A, B+1, 0, ...]` = T' ✓

So `T < [A, B, 1] < T'`. The gap between T and its "next sibling" is an entire sub-tree of deeper addresses.

### 4. The formal successor relation

In the tumbler address space, tumblers form a tree:
- `[A]` is an ancestor of `[A, B]` for any B ≥ 1
- `[A, B]` is an ancestor of `[A, B, C]` for any C ≥ 1
- The tree order respects the total order: all descendants of T sort between T and T's next peer

The true **immediate successor** of T (with last nonzero at position `idx`) in the total order is `tumblerincrement(T, 1, 1)`, which adds a new digit 1 one level deeper:

```
immediate_successor([A, B]) = [A, B, 1]   (tumblerincrement with rightshift=1)
```

Because the mantissa digits are non-negative integers (`tdigit = UINT`), there is no value between `B` and `B+1` at the same position — the only things between `[A, B]` and `[A, B+1]` in the total order are sub-addresses of `[A, B]`.

### 5. What `rightshift` actually controls

`rightshift` shifts the write target relative to `idx`:

| rightshift | Write position | Semantic |
|---|---|---|
| `0` | `mantissa[idx]` | Increment last digit — **next peer** at current depth |
| `+1` | `mantissa[idx+1]` | Write to next-deeper level — **first child** = immediate successor |
| `+N` | `mantissa[idx+N]` | Write N levels deeper — Nth-generation child |
| `-1` | `mantissa[idx-1]` | Increment parent digit — **next peer at shallower depth** |

The call in `findaddressofsecondcutforinsert` [insertnd.c:179] uses `rightshift=-1` precisely to step up one level before finding an insertion boundary:
```c
tumblerincrement (position, -1, 1, secondcut);  // [A, B] → [A+1, B] (idx=1, writes to idx-1=0)
```

And in `setlinkvsas` [do2.c:172–176], a two-call sequence builds a two-digit tumbler:
```c
tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);  // zero → [1], exp=0
tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);  // [1] → [1, 1] (idx=0, writes to idx+1=1)
```

The `credel.c:511` usage `tumblerincrement(..., 2, 1, ...)` writes 2 positions deeper than the last nonzero digit.

### 6. Summary

**`tumblerincrement` increments the least-significant nonzero digit (at `idx`), offset by `rightshift`.** With the canonical `(rightshift=0, bint=1)` call:

- It does **not** produce the immediate successor in the total order.
- It produces the **next peer** at the same hierarchical depth — the smallest tumbler at that depth strictly greater than T.
- The formal gap `(T, tumblerincrement(T, 0, 1))` in the total order contains exactly the sub-tree of T: all tumblers of the form `[T.mantissa[0..idx], k, ...]` for k ≥ 1 and any deeper extensions.

The **true immediate successor** in the total order is `tumblerincrement(T, 1, 1)` — which appends a digit 1 one level deeper and is the first member of T's subtree `[tumble.c:599–622]`.

---

## Question 16 [gregory]

> The `.0.` digit acting as a hierarchical separator is described as convention, not enforcement — were there ever plans to make the algebra aware of hierarchy (e.g., parent-child ordering guarantees), or is hierarchy purely an interpretation layer above flat digit sequences?

### Gregory's Answer

## KB Synthesis

The KB is clear on this: hierarchy is and was always an interpretation layer, not an algebraic property. The evidence points consistently one direction.

**What the algebra knows about hierarchy: nothing.**

The tumbler operations — compare, add, subtract, increment — operate on flat digit sequences. [SS-TUMBLER] Finding 0031 states explicitly: "The zero-separator convention is semantic, not structural — the data type itself does not enforce hierarchy boundaries." `tumblercmp` is a pure lexicographic total order with exponent alignment [INV-TUMBLER-TOTAL-ORDER]. There is no "parent of" or "child of" primitive in the arithmetic layer.

**Hierarchy is imposed from outside the algebra, at two levels:**

1. **Allocator bounds**: `findisatoinsertnonmolecule` enforces containment by computing an upper bound (`tumblerincrement(hintisa, depth-1, 1)`) and bounding its search to the parent's address range [SS-ADDRESS-ALLOC]. The `makehint` function packages a depth integer to pass this information to the allocator [SS-ADDRESS-SPACE]. Hierarchy is injected as a search constraint, not as a type constraint.

2. **Containment predicate**: `tumblertruncate` + `tumblereq` implements "is A under B?" as a derived utility — truncate A to B's length, compare [SS-TUMBLER-CONTAINMENT]. This is a predicate built on top of the algebra, not part of it.

**Was enforcement ever planned?**

There are fragments suggesting it was. `acceptablevsa()` in `do2.c:110-113` always returns `TRUE` — Finding 0049 calls this "a stub that was presumably intended for validation." That's the clearest signal: a validation hook was designed into the architecture but never implemented. Bug 0013 shows that the allocator originally didn't even enforce account containment, requiring a post-hoc fix to add the truncation/comparison check [PRE-ADDRESS-ALLOC].

The two-blade knife in INSERT [SS-TWO-BLADE-KNIFE] is the one place where something like hierarchy-awareness appears in an operation: the second blade is computed as `(N+1).1`, isolating shifts to within a subspace. But this is using the digit-value structure of the address space, not `.0.` boundaries — it's subspace isolation, not hierarchy enforcement.

**Bottom line:** The `.0.` separators were always a docuverse convention layered over flat arithmetic. The algebra was designed to be hierarchy-oblivious — fast, simple, composable. Hierarchy enforcement was supposed to live in the allocation machinery and input validation (`acceptablevsa`), not in the arithmetic itself. The allocator got its enforcement (with the Bug 0013 fix). The input validation never did.

---

## Code Exploration

Zero matches for `isparent`, `isancestor`, `ischild`, or hierarchy predicates of any kind — only the license boilerplate's "contains" phrase.

---

## Full Answer

The question asks whether the `.0.` digit's role as a hierarchical separator was ever planned to be enforced by the algebra itself, or whether it has always been purely an interpretation layer.

The truth is a three-way split, visible in the code:

---

### 1. Core Arithmetic Is Completely Flat (By Design)

`tumblercmp`, `abscmp`, `tumbleradd` (`functiontumbleradd`), `strongsub`, `weaksub`, and `tumblerincrement` — all in `tumble.c` — treat every mantissa slot identically. `abscmp` at `tumble.c:99-108` is the canonical example: it walks the mantissa array left-to-right with `*a++ - *b++`, no zero-special logic anywhere. Comparison, addition, and subtraction are all positional arithmetic over a flat unsigned-integer sequence.

The struct definition (`common.h:59-65`) has no field for depth, level, parent, or hierarchy. The macro `iszerotumbler` (`common.h:72`) only tests `mantissa[0]` — the zero tumbler test, not a "is this a hierarchical separator" test. No constant, macro, enum, or comment in `common.h` or `tumble.c` distinguishes "structural zeros" from "content digits."

---

### 2. The Zero Digit HAS Algebraic Meaning in One Place

`tumbleraccounteq` (`tumble.c:38-70`) is the exception. Its own comment is explicit:

> *"Key insight: When account has a zero, it marks the boundary of the account's address space. The document can have any value there (continuing to sub-addresses). We only check for exact match on non-zero account positions."*

A zero digit in the *account* (right-hand) tumbler is a wildcard: it matches any document digit at that position. Two consecutive zeros terminate the match and return `TRUE`. This is hierarchy-awareness baked into the algebra: account address `1.1.0` will match document address `1.1.0.1`, `1.1.0.1.0.3`, etc.

This function is load-bearing in `do1.c:270` for `docreatenewversion`: whether the new version goes under your own account (DOCUMENT→DOCUMENT, depth=1) or under another's account (ACCOUNT→DOCUMENT, depth=2) depends on `tumbleraccounteq` returning the right answer.

---

### 3. Hierarchy Is Constructed by Address Generation via `depth`

The `.0.` gap itself is produced in `granf2.c:209` (`findisatoinsertnonmolecule`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

When the object being created is a *different type* than its container (e.g., an ACCOUNT creating a DOCUMENT, or a DOCUMENT creating an ATOM), `depth=2`. This means `tumblerincrement` writes at `last_occupied_slot + 2`, leaving slot `last_occupied_slot + 1` as zero. That gap IS the `.0.` separator.

When creating a same-type object (DOCUMENT creating DOCUMENT = versioning), `depth=1` — no gap, a flat increment.

The convention comment at `granf2.c:219-227` is explicit about this being convention-by-construction:

> *"BUG FIX #1: If nothing exists under the hint (lowerbound is zero after findpreviousisagr), create the first child address as hintisa.0.1. The original code would produce just '1' due to truncate/increment on a zero tumbler, causing the first document to get the wrong address."*

The bug being fixed was that the first document under an account was *not* getting the `.0.` separator — the fix explicitly enforces the convention. But this enforcement lives in `granf2.c` (address generation), not in `tumble.c` (arithmetic).

---

### 4. Hierarchy-Manipulation Primitives Exist but Are Not Used Broadly

`prefixtumbler` (`tumble.c:641-651`) prepends a digit, wrapping an address into a sub-namespace. `beheadtumbler` (`tumble.c:673-683`) removes the first digit, stepping up. `docidandvstream2tumbler` (`tumble.c:685-699`) explicitly concatenates a document ISA with a V-stream address by appending after the last non-zero digit (creating the `docid.0.vstream` structure).

These functions exist in the arithmetic layer, not the address-generation layer. They are hierarchy-aware primitives. But they are narrow in scope: `prefixtumbler` appears to be unused in the live call graph, `beheadtumbler` is used only in the (ifdef'd-out) old `abscmp` branch. `docidandvstream2tumbler` is present but I found no callers in the current codebase. They read like primitives that were built in anticipation of operations that were never fully wired up.

---

### 5. Domain Subspace Interpretation Is Pure Convention

`istextcrum` and `islinkcrum` in `orglinks.c:246-261` read specific mantissa slots to classify crums:

```c
bool istextcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(...)) { return TRUE; }
```

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(...mantissa[0] == 1 && ...mantissa[1] != 0){  /* if the tumbler is a 1.n tumbler where n!= 0 */
```

The inline comment says it directly: this is "if the tumbler is a 1.n tumbler where n!= 0." The algebra never established that `mantissa[1]` means "this is in link space" — this is the application layer reading positional conventions back out. The arithmetic has no concept of "link space" vs. "text space."

Similarly, `findvsatoappend` in `orglinks.c:37` creates `linkspacevstart` as tumbler `2.0` (literally `tumblerincrement(..., 0, 2, ...)`) and uses `tumblercmp` against it to decide whether to append in text or link territory. This is a numeric boundary comparison that happens to correspond to the `.0.` convention — the algebra doesn't "know" it's a domain boundary.

---

### The Naming Tells You the Intended Mental Model

`nstories` and `is1story` (`tumble.c:249-247`) are the most revealing function names in the codebase. "Stories" = floors of a building. The designers were explicitly thinking in spatial/hierarchical terms. `nstories` counts occupied mantissa positions; a "1-story" tumbler has only one significant digit. But this naming maps hierarchical intuition onto a count of flat array positions — the hierarchy is a metaphor for the digit depth, not an enforced structural property.

---

### Summary: The Architecture as Built

| Layer | Hierarchy Awareness | Evidence |
|---|---|---|
| Core arithmetic (`tumblercmp`, `tumbleradd`, etc.) | None | `abscmp` walks mantissa uniformly, `tumble.c:99-108` |
| Account matching (`tumbleraccounteq`) | Partial — zero is a wildcard | `tumble.c:47-62` comment; zero-termination protocol |
| Hierarchy-manipulation primitives (`prefixtumbler`, `beheadtumbler`) | Yes — explicit | `tumble.c:641-683`; but narrow scope, limited callers |
| Address generation (`findisatoinsertnonmolecule`) | Yes — `depth` encodes level | `granf2.c:209`; `depth=2` produces the `.0.` gap |
| Domain interpretation (`istextcrum`, `islinkcrum`) | Pure convention | `orglinks.c:246-261`; reads `mantissa[1]` by position |

**The design is deliberate, not accidental.** The arithmetic layer is kept flat so that span arithmetic, retrieval, and comparison are O(NPLACES) simple operations with no parsing of semantic structure. Hierarchy is "enforced" through two mechanisms: (a) `tumbleraccounteq`'s zero-wildcard semantics for ownership, and (b) the `depth` parameter in address generation which produces the `.0.` pattern by construction. There are no parent-child ordering guarantees from comparison, no hierarchy predicates, and no structural enforcement that a zero at any given position is "the separator" rather than an ordinary digit.

The question of whether hierarchy was ever planned to be more deeply embedded in the algebra probably has this answer: the primitives (`prefixtumbler`, `beheadtumbler`, `docidandvstream2tumbler`) were built to support it, but the usage never materialized. The real work is done by `tumbleraccounteq` (zero-as-boundary) and the address-generation layer. Everything else is convention that the algebra happens to respect by the accident of lexicographic ordering — `1.0.2 < 1.1 < 1.1.0.1` by pure arithmetic, which also happens to be the correct hierarchical ordering.

---

## Question 17 [gregory]

> When two tumblers have different exponents, `tumblercmp` compares them — is the ordering purely lexicographic on the (exponent, mantissa) pair, or does the exponent shift the mantissa digits before comparison so that `2.1` (exp=0) and `0.21` (exp=-1) compare as equal?

### Gregory's Answer

## KB Synthesis

The comparison is **not** value-normalizing. `2.1` (exp=0) and `0.21` (exp=-1) compare as strictly ordered, not equal.

From [SS-TUMBLER] Finding 0031 and [INV-TUMBLER-TOTAL-ORDER]:

`abscmp` uses a two-phase comparison:
1. **Exponent first** — a larger exponent means a larger absolute value, full stop.
2. **Mantissa second** — lexicographic left-to-right, only when exponents are equal.

For your example:
- `2.1`: `exp=0`, `mantissa=[2,1,0,...,0]`
- `0.21`: `exp=-1`, `mantissa=[2,1,0,...,0]`

`abscmp` sees `exp=0 > exp=-1` and returns GREATER immediately — the mantissa is never consulted. So `2.1 > 0.21`.

**Equality is exact match**: two tumblers are equal iff sign, exponent, and all 16 mantissa digits match. [SS-TUMBLER] Finding 0031 states explicitly: "no normalization ambiguity after `tumblerjustify`." `tumblerjustify` canonicalizes the representation, and then `tumblereq` is a bitwise comparison of the three fields.

This design is what makes [SS-TUMBLER] Finding 0055's `strongsub` exponent guard meaningful: when `b.exp < a.exp`, `strongsub` returns `a` unchanged rather than attempting cross-exponent arithmetic — because the exponent comparison alone encodes a magnitude relationship that prevents the subtraction from being meaningful at the same scale.

---

## Code Exploration

The answer is clear from two functions in `backend/tumble.c`. Let me walk through them precisely.

---

## `tumblercmp` [tumble.c:72–85]

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

Zero-tumbler edge cases aside, for two positive tumblers it delegates directly to `abscmp(aptr, bptr)`.

---

## `abscmp` [tumble.c:87–111] (active branch — `#ifndef ExPeriMental`)

```c
static INT abscmp(tumbler *aptr, tumbler *bptr)
{
    if (aptr->exp != bptr->exp) {
        if (aptr->exp < bptr->exp) {
            return(LESS);
        } else {
            return(GREATER);
        }
    } else {
        a = (INT *) aptr->mantissa;
        b = (INT *) bptr->mantissa;
        for (i = NPLACES; i--;) {
            if(!(cmp = *a++ - *b++)){
            } else if (cmp < 0) {
                return (LESS);
            } else {
                return (GREATER);
            }
        }
    }
    return (EQUAL);
}
```

The logic is a strict two-level lexicographic comparison:

1. **Primary key: exponent** [tumble.c:92–97]. If `aptr->exp != bptr->exp`, the result is decided **entirely by the exponent** — the mantissa is never examined.
2. **Secondary key: mantissa, slot by slot** [tumble.c:99–108]. Only reached when exponents are equal; compares `mantissa[0]`, `mantissa[1]`, … left-to-right.

There is **no digit shifting**. The mantissa slots of `a` and `b` are compared directly at the same array indices. The exponent is treated as an independent key, not as an alignment offset.

---

## Answering the specific example

For `2.1` (exp=0, mantissa=[2,1,…]) vs `0.21` (exp=-1, mantissa=[2,1,…]):

- The exponents differ: 0 ≠ -1.
- `abscmp` enters the `if (aptr->exp != bptr->exp)` branch [tumble.c:92].
- `exp=0 > exp=-1`, so `2.1` returns **GREATER**.
- The mantissa arrays `[2,1,…]` are **never consulted**.

They do **not** compare as equal. The encoding `0.21` with exp=-1 is a completely different address from `2.1` with exp=0 — the exponent is treated as a distinct numeric field, not as a decimal-shifting mechanism.

---

## Normalization constraint confirms this

`tumblercheckptr` [tumble.c:186–191] enforces:
```c
if (ptr->exp && ptr->mantissa[0] == 0){
    wrong = TRUE;
}
```

A valid non-zero tumbler with `exp != 0` must have `mantissa[0] != 0` (no leading zeros). `tumblerjustify` [tumble.c:289–313] normalizes by shifting leading zeros out and **decrementing** `exp` by the shift count. This means the representation is canonical: there is only one valid encoding for any given abstract address. Two tumblers that "look the same after alignment" would have already been collapsed into the same canonical form before comparison — so there is no need for `abscmp` to perform alignment. It simply never does.

---

## Conclusion

**The ordering is purely lexicographic on the `(exp, mantissa)` pair.** The exponent is not used to align or shift digits before comparison. `2.1` (exp=0) and `0.21` (exp=-1) compare as **GREATER/LESS** — not equal — because their exponents differ, and `abscmp` returns immediately on that difference without ever looking at the mantissa.

---

## Question 18 [gregory]

> What happens when `tumbleradd` or `tumblerincrement` would produce a result requiring more than 16 mantissa digits — is there silent truncation, wraparound, or an error condition, and has this limit ever been hit in practice?

### Gregory's Answer

## KB Synthesis

This question is not answerable from the KB.

The KB establishes the relevant structural facts: tumblers have a fixed-precision representation with exactly `NPLACES` (16) mantissa digits and a short exponent [SS-TUMBLER Finding 0031], and operations like `tumblerincrement` and `tumbleradd` are used throughout the codebase for I-address allocation and V-position arithmetic [SS-ADDRESS-SPACE, ST-INSERT, ST-REARRANGE].

However, no finding documents what happens when arithmetic would overflow the 16-digit mantissa — whether the implementation silently truncates, wraps, errors via `qerror`/abort, or whether `tumblerjustify` handles this. The KB also contains no evidence that this limit has been hit in practice (e.g., no golden test failure or finding referencing a mantissa-overflow bug).

This would require direct code inspection of `tumble.c`'s `tumbleradd` and `tumblerincrement` implementations, particularly their carry-propagation and overflow paths.

---

## Code Exploration

I have everything I need. Here is the full analysis:

---

## Tumbler Overflow Behavior: `tumbleradd`, `tumblerincrement`, and the 16-digit limit

---

### The Data Structure

From `common.h:53-65`:

```c
#define NPLACES 16  /* places in mantissa of tumbler - increased from 11 to support deeper version chains */

typedef UINT tdigit;   // uint32_t — common.h:57, defs.h:12

typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign BIT;
    short exp;
    tdigit mantissa[NPLACES];   // 16 slots of uint32_t
} tumbler;
```

The mantissa is a 16-element array of **unsigned 32-bit integers**. Each element is one "place" or "story" in the Xanadu hierarchical address (e.g., `1.1.0.2.0.5` uses 6 places). Zeros within the mantissa are semantic level separators, not padding. Tumblers are always normalized so that `mantissa[0] != 0` for non-zero tumblers [tumble.c:186-190].

---

### `tumblerincrement` — Two Distinct Failure Modes

`tumblerincrement(aptr, rightshift, bint, cptr)` at `tumble.c:599` adds `bint` at the position `rightshift` places to the right of the last non-zero digit.

```c
for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);  // find last nonzero [tumble.c:611]

if (idx + rightshift >= NPLACES) {   // [tumble.c:612]
#ifndef DISTRIBUTION
    dumptumbler(aptr);
    fprintf(stderr, " idx = %d  rightshift = %d\n", idx, rightshift);
    gerror("tumblerincrement overflow\n");   // [tumble.c:616]
#else
    gerror("");                              // [tumble.c:618]
#endif
}
cptr->mantissa[idx + rightshift] += bint;  // [tumble.c:621]
```

`gerror` is defined as `#define gerror(s) qerror(s)` [common.h:119], and `qerror` at `genf.c:546-551`:

```c
INT qerror(char *message)
{
    fprintf(stderr, "Error: %s\n", message);
    abort();          // process terminates
    return(1);
}
```

**Failure Mode 1: Structural overflow** (`idx + rightshift >= NPLACES`)

The result would require a mantissa position at index ≥ 16. This is **detected explicitly**. In both DISTRIBUTION and non-DISTRIBUTION builds the code calls `gerror` → `qerror` → `abort()`. The process dies; there is no silent truncation, no wraparound. In non-DISTRIBUTION builds a diagnostic is printed first.

**Failure Mode 2: Digit-value overflow** (`mantissa[pos] + bint > UINT32_MAX`)

Line 621: `cptr->mantissa[idx + rightshift] += bint` performs unsigned 32-bit arithmetic with no overflow check. If the sum exceeds `2^32 − 1`, C's unsigned wraparound applies **silently** — no error, no diagnostic, wrong answer stored. This is undocumented and unguarded.

In practice this would require a single digit value to exceed ~4 billion. Given how the allocator works (allocating documents as 1, 2, 3, … under each account [granf2.c:162-175]), individual digits stay small. But a text span of more than 4 billion characters in a single leaf crum would trigger it.

---

### `absadd` (called by `tumbleradd`) — No Overflow Check at All

`absadd` at `tumble.c:444` is the active addition implementation (the `OlDVeRsIon` variant at line 488 is dead code). It performs a **single-point addition**, not a full multi-precision carry chain.

**Equal-exponent case** [tumble.c:460-464]:

```c
answer.exp = aptr->exp;
ansmant[0] = amant[0] + bmant[0];  // one uint32_t add, no carry check [tumble.c:462]
i = j = 1;
```

Then the loop [tumble.c:480-482] copies `bmant[1..15]` verbatim; `amant[1..15]` is entirely discarded. If `amant[0] + bmant[0]` overflows `uint32_t`, the result **wraps silently** with no error or diagnostic of any kind.

**Unequal-exponent case** [tumble.c:464-482]:

When `aptr->exp > bptr->exp`: the prefix of `amant` is copied, then one digit of `amant[i] + bmant[0]` is added at the crossover point (line 470), then the remainder of `bmant` is copied. Again, only one addition site, no carry, no overflow check.

When `bptr->exp > aptr->exp`: `bmant` is copied entirely and `amant` is discarded. The subtraction-via-negation path in `tumblersub` [tumble.c:426-429] routes through `tumbleradd`, subject to the same constraints.

**There is no structural overflow guard in `absadd`.** If the combination of exponent difference and mantissa depth would require writing past `NPLACES`, the loop `while (j <= NPLACES-1)` simply copies `bmant[i++]` until `j` reaches `NPLACES-1`. However, the tumblercheck invariant `exp <= 0` [tumble.c:174] limits how many leading positions are possible, and in practice the two operands are always within the same address subspace.

---

### Has This Limit Ever Been Hit?

**Yes — definitively, in practice, with `NPLACES=11`.**

From `bugs/0012-deep-version-chain-crash.md`:

> The backend crashes when creating or accessing version chains deeper than 3–4 levels. The root cause was tumbler overflow — document addresses for deep versions exceed the tumbler mantissa capacity. The tumbler struct had `NPLACES=11` mantissa digits. Deep version chains exceed this, causing overflow in `tumblerincrement`.

Version addresses grow one digit per generation: `1.1.0.1.0.1` → `1.1.0.1.0.1.1` → `1.1.0.1.0.1.1.1` etc. With NPLACES=11, a version chain of depth ~4 hit the structural check at `tumble.c:612`, `gerror` fired, and the process `abort()`ed.

The fix was increasing NPLACES from 11 to 16, recorded in `common.h:53` with the comment *"increased from 11 to support deeper version chains."* Verified working to depth 5 after the fix. Bug 0012 notes that some of those crashes may also have been triggered by the separate `recombine` stack buffer overflow (Bug 0020), since both produce `SIGABRT` with no `gerror` message in the DISTRIBUTION build.

---

### Summary Table

| Operation | Condition | Behavior |
|---|---|---|
| `tumblerincrement` | `idx + rightshift >= NPLACES` (position overflow) | `gerror` → `abort()` — detected, fatal, never silent |
| `tumblerincrement` | `mantissa[pos] += bint` overflows `uint32_t` (digit overflow) | Silent unsigned wraparound — **undetected** |
| `absadd` / `tumbleradd` | `amant[0] + bmant[0]` overflows `uint32_t` | Silent unsigned wraparound — **undetected** |
| `absadd` | Result would need > NPLACES positions | No guard — copies beyond intended range (UB if it occurs) |
| **NPLACES=11 hit** | Deep version chains (depth ≥ 4–5) | Confirmed in Bug 0012; fixed by raising to NPLACES=16 |

The short answer: structural position overflow in `tumblerincrement` causes `abort()`, not silent truncation. Digit-value (`uint32_t`) overflow in both `tumblerincrement` and `absadd` wraps silently with no error. The NPLACES limit was concretely hit in practice with the original value of 11, forcing it to be raised to 16 — the code still carries that comment today at `common.h:53`.

---

## Question 19 [gregory]

> `tumblerjustify` normalizes a tumbler before equality comparison — what invariant does it restore (leading-zero removal, trailing-zero trimming, exponent normalization), and can two tumblers that are `tumblercmp`-ordered but not `tumblerjustify`-normalized produce an inconsistent ordering?

### Gregory's Answer

## KB Synthesis

## `tumblerjustify` and Normalization

**What the KB tells us about the representation**

From [SS-TUMBLER] Finding 0031: a tumbler is stored as `(sign, exp, mantissa[NPLACES=16])`. The exponent shifts the mantissa — `exp=0` places the first mantissa digit as most-significant; negative exp represents fractional positions. `tumblerlength()` returns `nstories(t) - t.exp` (significant digit count).

**What `tumblerjustify` normalizes**

The KB doesn't describe `tumblerjustify`'s implementation directly, but Finding 0031 gives the critical constraint:

> "Two tumblers are equal iff their sign, exponent, and all 16 mantissa digits match (**no normalization ambiguity after `tumblerjustify`**)"

The phrase "no normalization ambiguity after `tumblerjustify`" implies that without it, the same logical value can be represented multiple ways. Given the exponent/mantissa structure, the ambiguity is **leading-zero equivalence**: the value `0.11` can be represented as either:
- `exp=-1, mantissa=[1,1,0,...,0]` (normalized: first digit non-zero)
- `exp=0, mantissa=[0,1,1,0,...,0]` (unnormalized: leading zero shifts value by one position)

`tumblerjustify` restores the **canonical form** where the leading mantissa digit is non-zero (or the tumbler is zero), adjusting `exp` accordingly — analogous to floating-point normalization.

**Can unnormalized tumblers produce inconsistent ordering?**

Yes. From [INV-TUMBLER-TOTAL-ORDER] Finding 0031, `abscmp` compares exponents first: "a larger exponent means a larger absolute value." If two tumblers represent the same value but one has a leading zero (requiring a higher `exp` to "reach" the significant digits), `abscmp` would classify the larger-exponent variant as strictly greater — returning an incorrect non-zero comparison for logically equal values.

Concretely:
```
A = exp=0,  mantissa=[0,1,1,0,...,0]  → logically "0.11"
B = exp=-1, mantissa=[1,1,0,...,0]    → logically "0.11"

abscmp: compares exp first: 0 > -1 → returns GREATER
        But A and B are equal values → INCONSISTENT
```

This would break any ordering predicate that relies on the total-order invariant, including interval classification ([SS-INTERVAL-CMP]), POOM traversal ([SS-WHEREONCRUM]), and enfilade search ([SS-ENFILADE-TREE]).

**Conclusion**

`tumblerjustify` restores canonical form by eliminating leading zeros from the mantissa (adjusting exp accordingly), ensuring the representation is unique per value. Without this normalization, `tumblercmp`'s exponent-first comparison produces incorrect ordering for logically equal but differently-encoded tumblers. The KB directly confirms this: equality comparison is only unambiguous after `tumblerjustify`, and since ordering subsumes equality, unnormalized tumblers can corrupt the total order that all downstream operations depend on.

---

## Code Exploration

---

## `tumblerjustify`: Invariant and Ordering Safety Analysis

### The Tumbler Representation

The `tumbler` struct [`common.h:59-65`]:
```c
typedef struct structtumbler {
    humber xvartumbler;
    char varandnotfixed;
    char sign;          /* 1 if negative, otherwise 0 */
    short exp;          /* always <= 0 for valid tumblers */
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

`NPLACES = 16` [`common.h:53`]. `mantissa[0]` is the most-significant digit (MSD). `exp` is always `<= 0` (positive `exp` is a validity error at [`tumble.c:174-178`]). The value is conceptually:

```
mantissa[0] at story-level exp
mantissa[1] at story-level exp-1
mantissa[2] at story-level exp-2
...
```

The zero tumbler is identified by the macro [`common.h:72`]:
```c
#define iszerotumbler(tumblerptr) (!((tumblerptr)->mantissa[0]))
```
It checks **only `mantissa[0]`**.

---

### What `tumblerjustify` Does

```c
int tumblerjustify(tumbler *tumblerptr)          /* tumble.c:289 */
{
    mantissaptr = tumblerptr->mantissa;
    if (mantissaptr[0] != 0) {                   /* line 296 */
        return(0);    /* already normalized */
    }
    for (shift = 0; mantissaptr[shift] == 0; ++shift) {
        if (shift == NPLACES - 1) {              /* line 302 */
            tumblerptr->exp = 0;
            tumblerptr->sign = 0;
            return(0);    /* all-zeros: canonical zero */
        }
    }
    /* left-shift mantissa by `shift` positions */
    for (i = 0, j = shift; j < NPLACES;)
        mantissaptr[i++] = mantissaptr[j++];    /* line 307 */
    while (i < NPLACES)
        mantissaptr[i++] = 0;
    tumblerptr->exp -= shift;                   /* line 310 */
}
```

Three paths:

1. **`mantissa[0] != 0` → return immediately** [`tumble.c:296-298`]. The tumbler is already in canonical form. No work to do.

2. **All `NPLACES` digits are zero → canonicalize to zero** [`tumble.c:299-305`]. Sets `exp = 0` and `sign = 0`. This ensures there is exactly one bit pattern for zero, eliminating "negative zero" (`sign=1, mantissa=all-zeros`, which `tumblercheck` explicitly rejects at [`tumble.c:180-183`]).

3. **Leading zeros with a non-zero tail → left-shift and adjust `exp`** [`tumble.c:306-313`]. Counts leading zero digits (`shift`), slides the mantissa array left by `shift` positions, zeros the vacated tail, and subtracts `shift` from `exp` to preserve value: `mantissa[0]_before` was at story-level `exp`; the first non-zero digit at position `shift` was at story-level `exp - shift`; after the shift, that digit is at `mantissa[0]` and the new `exp` equals `exp - shift`.

---

### The Invariant Restored

`tumblerjustify` restores **leading-digit normalization**:

> **For any non-zero tumbler, `mantissa[0]` must be non-zero.**

This is neither trailing-zero trimming (trailing zeros in the mantissa are left intact — `nstories` at [`tumble.c:255`] and `lastdigitintumbler` at [`tumble.c:282`] both work over trailing zeros without removing them) nor IEEE-style exponent bias normalization. It is strictly a requirement that the **first story slot be occupied by the most significant digit**.

`tumblercheck` gives the invariant explicitly in two diagnostics:

- **`"fucked up non-normalized"`** [`tumble.c:186-190`]: fires when `ptr->exp != 0 && ptr->mantissa[0] == 0` — the exponent says there are significant digits above story-0 but the top slot is empty.
- **`"nonzerozerotumbler"`** [`tumble.c:192-200`]: fires when `mantissa[0] == 0` but any later mantissa entry is non-zero — the digit is buried under leading zeros.

The secondary invariant also restored: **no negative zero** — the zero value always has `sign == 0` [`tumble.c:180-183`].

---

### Can Un-Normalized Tumblers Produce Inconsistent `tumblercmp` Ordering?

**Yes. The inconsistency is structural, not hypothetical.**

The root cause: `tumblercmp` [`tumble.c:72-85`] begins with zero-checks using `iszerotumbler`, which is defined as `!((tumblerptr)->mantissa[0])` [`common.h:72`]. Any un-normalized tumbler with `mantissa[0] == 0` and a non-zero digit somewhere in positions `1..15` is **misclassified as zero** by this macro. The actual non-zero value buried in the tail is invisible to `tumblercmp`.

**Concrete example of inconsistency:**

Let T be un-normalized: `mantissa = [0, 0, 5, 0, ...]`, `exp = 0`, `sign = 0`.  
T_norm (after `tumblerjustify`): `mantissa = [5, 0, ...]`, `exp = -2`, `sign = 0`.  
Let B be normalized: `mantissa = [3, 0, ...]`, `exp = -1`, `sign = 0`.

Actual ordering: T_norm at story-level `-2` vs B at story-level `-1`. In `abscmp`, `exp(-2) < exp(-1)`, so T_norm < B. Correct.

Now call `tumblercmp(T, B)` with un-normalized T:
- `iszerotumbler(T)` → `!mantissa[0]` → `!0` → **TRUE** (wrong — T is not zero)
- Fall into `return (bptr->sign ? GREATER : LESS)` [`tumble.c:78`]
- B has `sign = 0`, so returns **LESS**: T < B ← accidentally correct here

But call `tumblercmp(T, ZERO)` where ZERO is the genuine zero tumbler (all mantissa zero, exp=0):
- `iszerotumbler(T)` → TRUE (T misidentified as zero)
- `iszerotumbler(ZERO)` → TRUE (genuinely zero)
- Returns **EQUAL** [`tumble.c:76`]

So `tumblercmp` says T == 0 AND T < B AND 0 < B — which is self-consistent in this case. But now consider T2, an un-normalized tumbler with `mantissa = [0, 7, 0, ...]`, `exp = -3`, `sign = 0` (actual value 7 at story-level `-4`):

- `tumblercmp(T, T2)`: both have `mantissa[0] == 0`, so both are misclassified as zero → returns **EQUAL**
- `tumblercmp(T_norm, T2_norm)`: T_norm has `exp = -2` (story `-2`, value 5); T2_norm has `exp = -4` (story `-4`, value 7). In `abscmp`: `exp(-2) > exp(-4)`, so returns **GREATER**: T_norm > T2_norm

Result: `tumblercmp(T, T2) = EQUAL` but `tumblercmp(T_norm, T2_norm) = GREATER`. The un-normalized comparison and the normalized comparison give **opposite verdicts** for the same pair of values. Transitivity is broken: T == T2 and T == 0 and T2 == 0, but T_norm > T2_norm > 0.

**The mechanism is clear**: `abscmp` is only called when both operands pass the `!iszerotumbler()` gate. Un-normalized tumblers with leading zeros never reach `abscmp` at all — they are short-circuited at the zero-detection branches. Those branches do not look at `exp` or any mantissa position beyond `[0]`, so all structural information in positions `1..15` is discarded.

---

### Summary

| Question | Answer |
|---|---|
| What invariant does `tumblerjustify` restore? | `mantissa[0] != 0` for any non-zero tumbler (leading-zero removal). Also: the zero value is canonical — `sign = 0`, all mantissa zeros. |
| Which of leading-zero removal / trailing-zero trimming / exponent normalization? | **Leading-zero removal only.** Trailing zeros are preserved. `exp` is adjusted arithmetically as a consequence, not normalized by a separate rule. |
| Can un-normalized tumblers produce inconsistent `tumblercmp` ordering? | **Yes.** `iszerotumbler` checks only `mantissa[0]`. Any un-normalized tumbler (leading zeros, non-zero tail) is misclassified as zero and never reaches `abscmp`. Two such tumblers representing different positive values compare EQUAL to each other and to the actual zero tumbler, producing ordering contradictions. |

The defense in the codebase: `tumblersub` always calls `tumblerjustify` on its output [`tumble.c:430`]; `functiontumbleradd` and `tumblerincrement` call `partialtumblerjustify` (a slightly more efficient variant that skips the early-exit check [`tumble.c:315-340`]) whenever a leading zero can occur. `partialtumblerjustify` is identical in logic; callers guard it with `if(cptr->mantissa[0] == 0)` [`tumble.c:387, 392`]. These call sites collectively enforce that public outputs of arithmetic operations are always normalized before being handed to comparison functions.
