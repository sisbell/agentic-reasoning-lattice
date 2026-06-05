## Question 9 [theory]

> What must the design guarantee about a reader's ability to interpret a link's type without consulting its endpoints?

## What the design must guarantee

A link's type must be interpretable **purely from the address of its type endset (the "three-set"), never from whatever content might be stored at that address.** The type is matched by address, not by dereferencing it — so a reader (or the search mechanism) can classify and filter a link without ever fetching or consulting what lies at the type's endpoint.

This is what makes **ghost-element types** possible: the address can point to a location where nothing is stored at all, and type interpretation still works.

### Nelson's words

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44–4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

### Why this matters to the design

Two guarantees follow from address-based (not content-based) type interpretation:

1. **Ghost types are valid.** Because nothing need be stored at the type address, a reader cannot be required to consult the endpoint to know the type — the meaning lives by convention on the address itself.

2. **Search efficiency / scale.** Filtering by type never forces content retrieval. This connects to the broader link-search guarantee: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

In short: the design must guarantee that **type is determinable from the type endset's address alone** — symmetry of the three endsets gives the type the same arbitrary-address form as from/to, but the searchability convention ("considers the type's address," not its contents) is what lets a reader interpret type without consulting the endpoint.

(Drawn from the curated `endsets`, `links`, and `link-type-system` sources; all quotes verified at 4/44–4/45 and 4/60.)
