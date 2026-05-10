## Question 7 [nelson]

> Must the system support typed links — connections that carry a declared kind or role such as "comment," "quotation," or "correction" — or are all links structurally uniform?

# Typed Links Are Structurally Required

Every Xanadu link has **three endsets**, not two. The third endset — the "three-set" or "3-set" — IS the type. It is not optional metadata bolted onto a uniform two-ended link; it is a structural component of every link in the system.

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The three endsets are:

| Endset | Purpose |
|--------|---------|
| **From-set** | The bytes the link is "from" |
| **To-set** | The bytes the link is "to" |
| **Type (three-set)** | Categorizes the link |

The MAKELINK operation requires all three:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

## The Mechanism Is Deliberately Open-Ended

The type system is not a fixed enumeration. It is extensible by any user without system changes:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

The crucial design insight: types are matched by **address**, not by content. The search mechanism never inspects what is stored at the type address — it only checks whether the address matches:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

This means type addresses need not point to anything at all:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

## Why Three and Not Two

Two endsets establish WHAT is connected. The third establishes WHAT KIND of connection it is. Without the type endset, you cannot distinguish a citation from a comment from a refutation. You cannot search for "all citations" without also retrieving every comment and footnote. You need system schema changes to add new link meanings.

The link search operation FINDLINKSFROMTOTHREE constrains on all three endsets simultaneously:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

And the system guarantees that irrelevant types do not impede search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

## Standard Types Proposed

I proposed a provisional set of standard types [LM 4/52-4/55], including connection, comment, counterpart, quote-link, citation, supersession, mail, heading, paragraph, footnote, and suggested-threading links. But I was explicit that this was provisional, not canonical:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

The type mechanism also supports **hierarchical types** through link-to-link:

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below." [LM 4/51]

## Summary

Links are **not** structurally uniform. Every link carries a type as its third endset, on equal footing with from-set and to-set. The type system is open-ended, address-matched, and user-extensible — but it is structurally present in every link. A link without a type endset is not a Xanadu link.
