## Question 5 [theory]

> Does the Xanadu design admit links of arity 2 with no type endset, or must every link carry a type endset (with arity-2 being merely an internal storage form)?

# Every link carries a type endset

My Xanadu design makes the link a three-endset structure. From-set, to-set, and type (the "three-set") are symmetrical:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. **We adopt the same convention for link types**." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. **This is symmetrical with the other endsets**." [LM 4/44]

The type endset is part of the link's identity, not optional ornament. The protocol bears this out — `MAKELINK` takes three sets:

> "This creates a link in document <doc id> from <from set> to <to set> **connected to <three set>**." [LM 4/68]

And search operates on the three together (`FINDLINKSFROMTOTHREE`, [LM 4/69]).

## What the type endset is permitted to be

- "Several pointers" rather than a single span [LM 4/44]
- A "ghost element" — pointing to an address with nothing stored there [LM 4/45]:
  > "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements."

So the *content* at the type address can be absent, but the type endset itself is structural.

## Arity-2 as storage form

An arity-2 representation (omitting the three-set entirely) is not part of the design I published. If an implementation stores untyped links compactly — implicitly defaulted, conventionally "vanilla jump-link" [LM 4/54], or pointing at a fixed ghost — that is a back-end compression of the same three-endset object, not a separate kind of link.

The one variation I explicitly admit on arity is **one-sidedness in the from/to dimension** — the paragraph designator "has only one side" and uses the first endset alone [LM 4/48]. Even there, nothing in my text drops the type endset.

## Caveat

NEED_RAW: 4/41-4/48 to verify that I never explicitly sanction a type-less ("arity-2") link form in surrounding prose I haven't quoted. The curated extracts establish the three-endset structure unambiguously but do not record me saying "arity-2 is disallowed" in those words.
