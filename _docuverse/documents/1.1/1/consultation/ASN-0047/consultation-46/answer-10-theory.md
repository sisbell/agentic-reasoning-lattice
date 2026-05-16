## Question 10 [theory]

> Did the design conceive of a document's content and link sub-allocators as siblings under a single element-field allocator (parent), or as independent address-producing mechanisms each operating directly on the document's tumbler prefix?

I need to look at the raw pages on tumbler address structure to answer this precisely. The curated sources mention the Element field but with some inconsistency (one mentions "3" for links, another shows "0.2").

[Reading page 195 (4/28) and surrounding pages to verify the Element field structure]
[Reading page 196 (4/29) - document/version subdivision]
[Reading page 197 (4/30) - element addressing]

NEED_RAW: 4/28-4/32 (pages 195-199)

Let me examine what the curated sources establish and what requires verification.

## What the curated sources establish

From the curated **i-space-addresses** memory:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." (4/28)

So the structure is: `Node.0.User.0.Document.0.Element` — three zero-dividers, four fields.

From the curated **links** memory:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

And the parsing offered there:
> "`0.2` = delimiter + link subspace (vs `0.1` for bytes)"

## Reading what this implies architecturally

The pattern `N.0.U.0.D.V.0.X.N` (with X ∈ {1 for bytes, 2 for links}) demonstrates a **single element-field allocator with sibling sub-allocators**, not two independent mechanisms.

Evidence for the "siblings under one parent" reading:

1. **The third `0` divider sits between Document and Element.** Nelson explicitly says "A tumbler address may have at most three zero digits... interpreted as the major dividers" (4/28). After this third divider, you are in the Element field — a single named field in the four-field schema.

2. **The `1` vs `2` discriminator lives inside the Element field, not above it.** The byte/link distinction is expressed by the *first digit after the third zero-divider*. That digit is hierarchically subordinate to the Element field, not a peer of it. Bytes live in subspace `1`; links live in subspace `2` — both addressed *under* the same Element-field root.

3. **Nelson's own taxonomy reads top-down as a forking tree.** From the curated **forking** memory:

   > "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." (4/19)
   > "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on." (4/19)

   The element-field discriminator (`1`/`2`) is the same baptism-by-forking pattern applied one level deeper: the document owner forks the Element field into a byte subspace and a link subspace.

4. **The i-space-addresses memory names exactly this structure:**

   > "**Element field structure:**
   > - Bytes: sequential positions in the content stream
   > - Links: 'The digit after the "3" is a link-address designating the link's serial position'"

   Both bytes and links are described as substructures *of* the Element field — they are co-allocated under it, not allocated independently from the document prefix.

## The "3" vs "2" discrepancy

The curated **i-space-addresses** memory references "the digit after the '3'" for links, while the curated **links** memory shows `0.2` as the link subspace. These are not necessarily contradictory:

- `0.2` reads as: minor divider `0`, then link subspace `2`.
- "After the '3'" may refer to a different schema reading where the third zero-divider is what's meant, or a typo/transcription variance.

The architectural point is unaffected: in both readings, **a discriminator digit lives between the document prefix and the actual byte/link instance number**, and it identifies which sub-allocator inside the Element field is being addressed.

NEED_RAW: 4/30-4/32 (pages 197-199) to resolve the `2` vs `3` discriminator value and confirm the exact wording Nelson uses for the byte/link subdivision within the Element field.

## Answer

The design conceives bytes and links as **siblings under a single element-field allocator (parent)**, not as independent address-producing mechanisms.

The Element field (the fourth and final field after the three major zero-dividers) is itself subdivided by a type discriminator: one subspace for bytes (sequential positions in the content stream), another for links (sequential by creation order). Both share the same document/version prefix and are reached through the same Element-field root — the discriminator just selects which sub-allocator within that field you are addressing.

This is also consistent with Nelson's general baptism-by-forking principle (4/19-4/20): every level of the tumbler tree is allocated by forking under the owner of the level above. The document owner forks the Element field into byte and link subspaces in exactly the same way a server forks itself into accounts.
