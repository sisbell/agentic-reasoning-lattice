## Question 7 [theory]

> Is the closed-world reading of operation effect clauses — that state components absent from both effect and frame are preserved across the transition — part of the intended convention for the substrate operation vocabulary, or is it a downstream interpretive choice?

The closed-world reading is a downstream interpretive choice. I never formally established a frame convention.

My operation specifications in 4/61–4/70 are informal English prose, not formal specifications. What I established explicitly are **principles** that constrain operation behavior:

1. **Append-only storage**: "User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

2. **Non-destruction**: "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

3. **Ownership invariant**: "Only the owner has a right to withdraw a document or change it." [LM 2/29]

4. **Explicit preservation across documents** — note that I state this *explicitly* rather than leaving it to implicit reading: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Observe my pattern: when preservation matters, I state it. The INSERT specification doesn't rely on the reader deriving the cascade — I write it out: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

And critically: "What the Xanadu storage and hypertext system does—and thus is—is defined by the commands to which it responds." [LM 4/61] — this is a constructive characterization, not a closed-world frame axiom.

**So my position is:** the closed-world reading is *consistent* with my intent, because the principles (append-only Istream, non-destruction, owner-only modification) actively require that operations preserve state they don't explicitly modify. But the principles carry that guarantee — not the operation effect clauses. A downstream specification choosing closed-world reading for the effect clauses is faithful to intent; one choosing open-world with explicit preservation statements derived from the principles is equally faithful. The formal convention is the implementor's choice. What matters is that the principles are honored.
