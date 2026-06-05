## Question 5 [theory]

> What does reading the endsets directly reveal about the relationship that traversing to one endpoint would never expose?

## What reading endsets reveals that traversal cannot

Traversal answers "where does this link take me?" — it lands you at a single destination. Reading the endset directly answers "what is the full shape of this connection?" Three things become visible only by inspection, never by following:

### 1. The set is discontiguous — traversal hides the scattering

A Xanadu endset is not a single point but "an arbitrary set of bytes" that "may be anywhere in the docuverse" (endsets.md, 4/42). Following a link delivers you to *a* place; reading the endset shows you that the connection actually touches multiple non-adjacent spans, possibly across several documents at once:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

A critique that binds three separate passages reads as one endset of three spans — but traversal would only ever drop you into one of them, exposing none of the others as siblings of the same connection.

### 2. The type endset has no destination to traverse to

The third endset — the "three-set" — categorizes the link by *address*, and that address often points at nothing stored:

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

You cannot meaningfully *traverse* to a ghost element — there is nothing there to arrive at. The link's *kind* (citation, refutation, counterpart, comment) is legible only by reading the type endset's address, never by following it.

### 3. The link is a unit with a home, not just a one-way path

Reading the endsets exposes the link as a concrete object whose home sits on one side and whose three endsets map outward symmetrically:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

This is the "Tumbler Square" view (4/46–4/47): the link as a thing with ownership and three reaching arms, discoverable from any of the four sides. Traversal collapses that whole structure into a single arrow you happened to follow.

### Why it matters

This is exactly why FEBE separates `RETRIEVEENDSETS` from any follow operation: the former "returns the from-set and to-set of specified links" (endsets.md) as data to inspect. The principle is symmetry and generalization — all three parts are arbitrary span-sets, so the system "needs only one mechanism for all three" (endsets.md). Traversal consumes that symmetry by privileging one direction to one point; reading the endsets preserves it, revealing the set membership, the type, and the link's identity as an owned object — none of which a single traversal would ever surface.
