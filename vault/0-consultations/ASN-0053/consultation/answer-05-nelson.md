## Question 5 [nelson]

> When one region completely contains another, must the system be able to express the remainder — the containing region with the contained region removed — as contiguous pieces?

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
