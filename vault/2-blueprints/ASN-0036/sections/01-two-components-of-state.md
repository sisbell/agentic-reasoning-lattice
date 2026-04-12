## Two components of state

The observation that motivates the entire design is that content EXISTS independently of how it is ARRANGED. A paragraph does not cease to exist when removed from a document — it merely ceases to appear there. Nelson states this plainly:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This observation forces the state into two components:

**Σ.C (ContentStore).** The *content store*: a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

Σ.C is a definition, not a derived property. We justify the modelling choice. Nelson's architecture requires a mechanism that associates content values with permanent addresses — the Istream. The natural mathematical object is a partial function `C : T ⇀ Val`. It is partial because not every tumbler carries content: only those addresses at which content has been stored belong to `dom(C)`. It maps to `Val` rather than to a specific type because the content store is indifferent to what it stores — text, links, media — at this level of abstraction. The domain `dom(Σ.C)` names the set of addresses at which content exists; all subsequent properties (S0 through S9) constrain how this domain and these values evolve under state transitions. The content store is the first of two state components; the second is the arrangement family Σ.M(d). Together they constitute the complete system state `Σ = (C, M)`. ∎

*Formal Contract:*
- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

**Σ.M(d) (Arrangement).** The *arrangement* of document `d`: a partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.

Σ.M(d) is a definition, not a derived property. We justify the modelling choice. A document in Nelson's architecture is not a contiguous block of stored content but a structure that *selects from* the content store — specifying which content appears, in what order. The natural mathematical object for this selection is a partial function `M(d) : T ⇀ T`. It maps from V-positions (tumblers addressing locations within the document's virtual stream) to I-addresses (tumblers addressing locations in the content store). It is partial because not every tumbler is an active V-position: only those positions at which `d` currently presents content belong to `dom(M(d))`. The codomain is `T` rather than `Val` because an arrangement does not contain content values directly — it refers to I-addresses where content resides. The content itself is retrieved via `Σ.C`. This indirection is the structural mechanism by which Nelson's two requirements — immutable content and mutable presentation — coexist: editing a document changes which I-addresses its V-positions reference (modifying `M(d)`) without altering what any I-address stores (preserving `Σ.C`). The arrangement is the second of two state components; together with the content store Σ.C, they constitute the complete system state `Σ = (C, M)`. ∎

*Formal Contract:*
- *Axiom:* `Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.
