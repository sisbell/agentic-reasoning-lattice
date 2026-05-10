## Question 3 [nelson]

> Can a single link connect more than two spans of content, or is every link strictly a pair of endpoints?

# A Single Link Connects Three Sets, Each Containing Arbitrary Spans

A Xanadu link is emphatically **not** a pair of endpoints. Every link has **three endsets** — from-set, to-set, and type — and each endset can itself be an **arbitrary collection of multiple discontiguous spans** scattered anywhere in the docuverse.

## Three Endsets, Not Two

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The type (the "three-set") is not metadata bolted onto a binary connection — it is a full endset with the same power and structure as from and to.

## Each Endset Is a Set of Spans

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

Even the type endset can be multi-valued:

> "Note that a link's type--the three-set--may be several pointers." [LM 4/44]

## Concrete Example

A single critique link might have:

- **From-set**: three non-adjacent passages in the critic's essay (the arguments)
- **To-set**: two passages in different documents being criticized
- **Type**: a span pointing to the "critique" type address

That is one link connecting **five** separate spans of content across multiple documents, plus a type designation — all in a single connective unit.

## Beyond Three: Compound Links

For structures requiring even more complexity, Nelson describes **compound links** built from link-to-link chains:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

Just as LISP builds arbitrarily complex structures from pairs, Xanadu builds arbitrarily complex relational structures from three-endset links pointing to other links.

## Summary

Every link is a **three-way** connection (from, to, type), and each of those three ways can touch **multiple discontiguous spans** across the entire docuverse. The common mental model of a link as "a line between two points" is a severe understatement of what I designed. A Xanadu link is a typed strap binding arbitrary collections of bytes — a far more powerful primitive than the point-to-point links the web settled for.
