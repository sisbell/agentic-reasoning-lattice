## Question 3 [theory]

> What must the system guarantee about the connector or type criterion as a first-class slot, so that links can be discovered by their kind of connection and not only by what they join?

## The Type Endset as a First-Class Slot

For links to be discoverable by their *kind* of connection — not merely by what they join — the system must treat the link's type as a full **endset**, structurally identical to the from-set and to-set. Nelson calls this the "three-set" or "3-set," and the central guarantee is **symmetry**: the type criterion gets exactly the same machinery as the endpoints it categorizes.

### 1. The type must be an endset that points anywhere, symmetrically

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

Because the type is an arbitrary span-set on the same tumbler line, it can itself be multiple pointers:

> "Note that a link's type—the three-set—may be several pointers." (4/44)

### 2. The type must be matched by ADDRESS, not by stored content

This is the load-bearing guarantee that makes discovery-by-kind work. The search mechanism never inspects what is *stored* at the type address — it matches the address itself:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44–4/45)

A direct consequence is that types need no backing content at all:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So the system must guarantee that a *ghost element* — an address with nothing stored there — is a valid, searchable type. The type's meaning lives by convention among users, not in any stored value the system interprets.

### 3. The type slot must be open-ended and user-definable

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose. This is done with a mechanism which is powerful and symmetrical." (4/43)

No schema, no registry, no central authority — a user defines a new kind of connection simply by choosing an address to represent it. The guarantee is *extensibility without system change*.

### 4. The search model must let the type constrain results independently

Discovery-by-kind requires that the type participate in the satisfaction test on equal footing with from and to. A request can constrain any combination of the three endsets, and a link matches when each endset is satisfied:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58, per the curated *operations* and *links* sources)

The request explicitly carries a type criterion — the "three-set spans covering the types of link wanted" — so you can ask for "all citation links" or "all refutations" by constraining the type alone, leaving from/to open. And critically, the noise of non-matching links must not impede this:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

### 5. The mechanism must support hierarchical type structure

Because types are addresses and links can point to links, the type slot composes into supertypes/subtypes:

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." (4/51)

---

## Summary of the Guarantee

The connector/type criterion must be a **first-class endset** with these properties:

| Requirement | Guarantee |
|---|---|
| **Symmetry** | Type is an endset like from/to — an arbitrary span-set pointing anywhere (4/43–4/44) |
| **Address-matching** | Search matches the type's *address*, never its stored content (4/44–4/45) |
| **Ghost validity** | Types may point to addresses with nothing stored (4/45) |
| **Extensibility** | Any user may define types; the set is open-ended (4/43) |
| **Independent constraint** | A search satisfied per-endset, so type alone can be the criterion (4/58) |
| **Scalable filtering** | Non-matching links don't impede search on the rest (4/60) |
| **Composability** | Link-to-link lets types form sub/super-type hierarchies (4/51) |

In short: by making *what kind of connection* a structurally equal third slot — matched by address rather than content — Nelson guarantees that the docuverse is searchable along the dimension of relationship-type itself, so a link is findable not only by the bytes it binds but by the meaning of the binding.

(Operation-level confirmation: **MAKELINK** records all three endsets, and the **FINDLINKSFROMTOTHREE** family searches by constraining any of them, including the three-set — see the curated *operations* source, 4/68–4/69.)
