## Question 1 [theory]

> Did the design intend the substrate's `Σ_init` to have an empty link store globally (across all type indices, including unregistered ones), or only at registered types?

# Design Intent: Globally Empty Link Store

The design intent is that `Σ_init` should have an empty link store **globally** — across all type indices, with no distinction between "registered" and "unregistered" types. The very concept of "registered types" is foreign to my design.

## Why Globally Empty

My system treats all type addresses uniformly. There is no privileged set of type indices that get special treatment at initialization.

**Three principles establish this:**

1. **Types are open-ended.** Any user may define new types by choosing addresses — no registration, no schema, no committee:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

2. **Types are matched by address, not by stored content.** The search mechanism is uniform across all addresses:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

3. **Type addresses can be ghost elements.** A type address needs no stored representation to function:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

## The Conceptual Gap

The notation `Σ_init` and the registered/unregistered distinction come from formalization work, not from my specification. I do mention a "working set of link types" as a standardization priority [LM 4/52], but those are **conventions for interoperability**, not a technical class of "registered" types with special status in the substrate.

If a formalization introduces a "registered types" category and treats unregistered indices differently at `Σ_init`, that distinction is an implementation artifact — it would create asymmetry where my design demands symmetry. The whole point of the ghost-element principle is that the substrate should not need to know in advance which addresses will be used as types.

## Operational Consequence

At initialization, no links exist anywhere. A search for links of *any* type — whether one of Nelson's tentative standard types (Citation, Comment, Counterpart) or some entirely novel address a user invents tomorrow — returns the empty set by the same mechanism. The substrate cannot distinguish "an empty bucket for a registered type" from "an empty bucket for an unregistered type" because there are no buckets — only the universal address space and the indexing of whatever links happen to point into it.

NEED_RAW: none — the curated extracts from 4/43-4/45 are sufficient to answer this. If the formalization being clarified is in `docs/design-notes/`, I would need to see that document to confirm whether its `Σ_init` definition is consistent with my intent.
