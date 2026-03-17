## Question 2 [nelson]

> Must a link distinguish a "from" endpoint and a "to" endpoint, or are the endpoints of a connection symmetric and unordered?

## Links Are Ordered but Semantically Flexible

The short answer: **links structurally distinguish a from-set and a to-set** (the endpoints are ordered), but the **meaning of that ordering is user-defined and type-dependent**, and Nelson explicitly acknowledges that directionality is not universal.

### The Key Quote

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

Three things packed into that sentence:

1. **"Typically"** — not always. Some links may not have meaningful directionality.
2. **From-set and to-set are structurally distinct** — they are separate endsets, stored and searched independently.
3. **"Depend on the specific case"** — the system provides the slot distinction; the link type gives it meaning.

### Structural Ordering

The protocol treats from and to as separate parameters. MAKELINK takes them distinctly:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>." [LM 4/68]

And search distinguishes them:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

So the system knows which endset is "first" and which is "second." This ordering is real — it's baked into the protocol.

### But Directionality Is Semantic, Not Structural

A citation link goes *from* citing text *to* source. A comment link goes *from* commentary *to* subject. A counterpart link connects equivalents — where directionality may be meaningless. The system provides the two slots; the link type defines whether the ordering carries semantic weight.

### The One-Sided Case Reveals the Design

Nelson's treatment of one-sided links is telling:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

He calls his own "from" label **inane** in this case. The label is a convention, not a deep structural commitment. The real structure is: a link has a first endset, a second endset, and a type endset — three ordered slots.

### Bidirectional Discovery Regardless

Even though from and to are distinguished structurally, **the system indexes both directions**. You can search for links *from* a span, *to* a span, or by type — from any direction. The ordering doesn't create a one-way gate.

### Summary

| Aspect | Answer |
|--------|--------|
| Are endpoints structurally distinct? | **Yes** — first endset vs. second endset, separate in protocol |
| Must they be semantically directional? | **No** — "typically directional," depends on link type |
| Who defines the meaning of from/to? | **The link type** — user-defined, open-ended |
| Can you search from either end? | **Yes** — bidirectional indexing on all three endsets |
| Are there non-directional links? | **Implied yes** — counterpart links mark equivalence; one-sided links use only one endset |

The design is: **ordered slots with user-defined semantics**. The system provides two distinguished positions; whether that distinction carries directional meaning is a property of the link type, not of the link mechanism itself.
