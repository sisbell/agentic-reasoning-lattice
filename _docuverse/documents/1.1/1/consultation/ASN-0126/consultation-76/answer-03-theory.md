## Question 3 [theory]

> Did the design intend type registration to expose a queryable type name (a name-lookup / type-discovery capability the substrate reads back), or is a type's name purely an app-side label that the substrate need neither carry nor interpret?

## Answer: A type's name is an app‑side label. The substrate neither carries nor interprets it.

Nelson's design deliberately makes a link's type an **address**, not a named entry that the storage system reads, stores, or interprets. The back end's only "knowledge" of a type is its position on the tumbler line; it matches that address and looks no further. There is no substrate-level name‑lookup or type-name‑discovery capability — by design.

### The decisive evidence

The substrate matches the type's *address* and explicitly does not read what is stored there:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

And the content at a type address need not exist at all:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

This ghost‑element point is what clinches the answer. If the substrate had to expose a queryable *name* for a type, that name would have to exist somewhere for it to read back. But Nelson guarantees a type can be a pure address with **nothing stored under it**. A capability that returned a type's name could not survive a ghost type — so no such capability is part of the model. Whatever human‑readable name a type has ("citation," "comment," "counterpart") is a convention layered *above* the substrate.

Types are also defined simply by choosing an address — there is no registration handshake with the substrate:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

### Corroboration from the protocol surface

The FEBE operation set contains **no type‑registration command and no find‑type‑by‑name command**. "Type discovery" at the substrate is nothing more than address‑constrained link search — finding links whose three‑set includes a given address (via `FINDLINKSFROMTOTHREE`, constraining the three‑set; see the operations summary, 4/58–4/70). Even when you retrieve a link's type, you get an *endset* — i.e., address(es) into tumbler‑space — not a string:

> "RETRIEVEENDSETS ... returns a list of all link end-sets that are in <spec set>." (4/70)

So the value handed back is an address the front end must interpret; the substrate never hands back a name.

### The one nuance — and why it doesn't change the answer

A name *can* happen to live in the docuverse: you could store the word "citation" at a type's address, or maintain a convention document mapping type addresses to human labels. But:

1. The substrate **ignores it for type‑matching** — "does not actually look at what is stored under the 'type'" (4/44–4/45). It matches the address whether or not a name is there.
2. Any such name is retrieved and rendered by a **front end**, using the same ordinary content‑retrieval path it uses for any bytes — not via a special type‑name facility.

The implementation framing in the curated `links` notes ("the type registry lives in the bootstrap document, doc 1") is consistent with exactly this: a registry, if one exists, is *a document* — addressable, transcludable, app‑readable content — not a substrate primitive. Naming lives above the storage layer.

### Why Nelson built it this way

This is the direct consequence of his **"type by address, not content"** and **"extensibility without authority"** principles. If the substrate had to carry and interpret type *names*, then introducing a new type would require a substrate‑level registration with semantic meaning — precisely the schema change / central gatekeeper Nelson designed against. By reducing a type to an arbitrary address that the search mechanism matches blindly, anyone can mint a type with no system change, and standardization becomes a matter of *agreeing on which addresses mean what* (a convention) rather than teaching the back end any names:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." (4/52)

That standardization effort is about shared conventions over addresses, not about a queryable name service in the substrate.

---

**Bottom line:** The intended answer is the second of your two options. Type identity is purely positional (an address, matchable even as a ghost element); a type's *name* is an application‑side label the back end need neither store nor interpret. The substrate offers address‑based link search as its only form of "type discovery" — never name lookup.

(All quotes above are from the verified curated extractions of *Literary Machines*, 4/43–4/52 and 4/58–4/70. I did not need the raw page images for this; the relevant material is textual prose, not diagrammatic, and the verified quotes settle the question.)
