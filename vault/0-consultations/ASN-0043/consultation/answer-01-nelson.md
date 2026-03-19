## Question 1 [nelson]

> What is the minimum structure of a link — what components must every connection between arbitrary spans of content contain?

# The Minimum Structure of a Link

Every Xanadu link contains exactly **four** structural components: a **home**, and **three endsets**.

## The Home

A link must reside somewhere. Its **home document** gives it a tumbler address and determines who owns it:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

The home is not optional. Without it, the link has no address, no owner, and no place in the docuverse.

## The Three Endsets

Every link has three endsets, treated symmetrically:

| Endset | Also Called | Role |
|--------|------------|------|
| **From-set** | first endset | The bytes the link is "from" |
| **To-set** | second endset, 2-set | The bytes the link is "to" |
| **Type** | three-set, 3-set | Categorizes the connection |

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The MAKELINK operation confirms this is the complete set:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

Four parameters: home document, from-set, to-set, type. Nothing else.

## What Each Endset IS

Each endset is an **arbitrary span-set** — not a single point, not a single span, but potentially multiple discontiguous regions of bytes scattered across the entire docuverse:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

This generality is fundamental. A link does not connect "page A to page B" or even "passage A to passage B." It connects an arbitrary collection of byte-spans to another arbitrary collection of byte-spans, categorized by a third arbitrary collection of byte-spans.

## Why the Type Endset Is Not Optional

The type is structurally identical to from and to — it is an endset pointing anywhere. But its role is semantic classification, and it has a crucial property: **search matches on address, not content**.

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

A link with no type would be unsearchable by kind — you could not ask "find all citations" or "find all comments." The type endset may point to a ghost address where nothing is stored, but it must point somewhere.

## The Degenerate Case: One-Sided Links

There is one acknowledged variation — the **one-sided link**, where only one content endset is populated:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

Paragraph designators and heading links are examples. But even these still have a home and a type — they are structurally three-endset links where one content endset happens to be empty.

## Summary

The minimum link structure is:

1. **Home** — a tumbler address in a document (establishes ownership and identity)
2. **From-set** — an arbitrary span-set (the source side of the connection)
3. **To-set** — an arbitrary span-set (the target side of the connection)
4. **Type** — an arbitrary span-set (the semantic classification, matched by address)

Nothing less is a link. Nothing more is required. The entire link mechanism — the universal system of retrieval "quite unlike any other in the world" [LM 4/41] — is built from this single four-part primitive.
