## Question 7 [theory]

> Which permanence guarantees — that content once placed is never moved or overwritten — hold purely from the nature of the operations themselves, regardless of how simultaneous actions are reconciled?

## Direct answer

The permanence guarantees that hold purely from the operations — independent of any concurrency or reconciliation policy — are exactly those that reduce to **two facts you can check on a single operation in isolation**:

1. **Istream is append-only.** No primitive in the command set can overwrite a byte already placed.
2. **Everything that looks destructive or relocating — DELETE, REARRANGE, COPY, and INSERT's position shift — acts on the Vstream mapping, never on Istream content.**

A property you can verify operation-by-operation is automatically immune to how simultaneous actions are reconciled. If no single operation has the *power* to move or overwrite placed content, then no interleaving of operations can synthesize that effect — reconciliation only chooses the order and combination of appends and remappings; it cannot manufacture a destructive result out of non-destructive parts. So the permanence of *already-placed content* never needed a locking or serialization story. The reconciliation layer governs the *combined result* (final arrangement, lineage, fresh-address allocation), not *whether existing content survives*.

## The operation-intrinsic guarantees

**1. Non-overwrite of placed content (the master guarantee).** The whole architecture is a rejection of in-place replacement:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Instead, suppose we create an append-only storage system." [LM 2/14]

There is simply no "overwrite" or "replace" verb in the protocol. The closest thing — replacing text — is INSERT plus DELETE, both of which preserve. Because the destructive primitive *does not exist*, no scheduling of writers can produce an overwrite.

**2. Survival of deleted content (DELETE is Vstream-only by definition).** DELETEVSPAN is defined narrowly:

> "This removes the given span from the given document." [LM 4/66]

— meaning it removes the span from the document's *arrangement*. The byte itself persists:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Two concurrent deletes, or a delete racing a read, cannot destroy the byte — neither operation can reach Istream in the first place.

**3. Stability of identity under rearrangement and insertion ("never moved").** What users perceive as moving content is a Vstream remapping; the byte's Istream identity is untouched:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

INSERT only shifts *virtual* positions of following content — "The v-stream addresses of any following characters in the document are increased by the length of the inserted text" [LM 4/66] — it does not relocate the bytes themselves in Istream. The crucial nuance: a byte's *V-position* may move; its *I-address* does not. The permanence guarantee is anchored at the identity level, not the position level.

**4. No duplication or relocation under COPY (transclusion shares Istream).** COPY does not copy content; it adds a reference:

> "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." [LM 4/67]

The copied span shares the source's I-addresses — "Non-native byte-spans are called inclusions or virtual copies" [LM 4/11] — so the source bytes stay exactly where they were placed. Inclusion adds a view; it never moves the original.

**5. Validity of existing addresses under insertion (forking never renumbers).** The address-space analogue of Istream immutability:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Baptism (forking) only creates sub-addresses; it never renumbers existing ones. An assigned address therefore survives any number of concurrent insertions, regardless of interleaving.

## What is *not* operation-intrinsic (these are the reconciliation questions)

- **A byte's eventual V-position / the live arrangement.** Because INSERT shifts following V-addresses by the inserted length [LM 4/66], where a byte *appears* is a function of the whole edit history — i.e., of how operations were ordered. (This is about arrangement, not survival.)
- **Which fresh I-address new content receives** when appends race. The *permanence of an address once assigned* is operational; *which* address gets assigned is an allocation/baptism matter for the owner.
- **Version/supersession lineage** — which version is "latest." That is social and reconciled, not an operational permanence property.

## Why this boundary is the right place to draw the line

Nelson never specified the concurrency layer at all — no OPEN/CLOSE, no locking protocol, no rule for two simultaneous editors of one document (the back-end "barrel-roll shared search model... on behalf of all a server's users simultaneously" is explicitly named as a *later* concern [LM 4/59]). That the permanence guarantees survive this omission is not luck: they had to be operation-intrinsic, because a guarantee asserted as absolute cannot depend on a reconciliation mechanism the design leaves open.

Two design choices keep contention from ever threatening permanence. Ownership confines who may edit — "Only the owner has a right to withdraw a document or change it" [LM 2/29] — and where edits *would* conflict, the model forks rather than overwrites: new versions are built "out of old ones indefinitely... without damaging the originals" [LM 2/45]. So the worst case of simultaneous action is *more appended content and another version*, never the relocation or destruction of what was already placed. The permanence guarantee degrades, under contention, into the very mechanism (append + fork) that defines it.
