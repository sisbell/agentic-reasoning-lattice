## Question 5 [nelson]

> Can a document's arrangement ever reference content that does not exist in permanent storage, or must every position in a document correspond to something already stored?

## Every V-Space Position Must Correspond to Stored I-Space Content

A document's V-stream (its current arrangement) is strictly a mapping to content that exists in I-space. Every position in the virtual byte stream resolves to actual stored bytes. There is no mechanism for a V-space position to reference "nothing."

### The Evidence

Nelson defines the V-stream as composed of two kinds of bytes, both of which must exist in storage:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [4/11]

Every byte is either natively stored or fetched from its home. There is no third category of "not yet existing." Non-native bytes participate fully:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [4/11]

The operations confirm this. INSERT creates new I-space content and places it in V-space simultaneously. COPY creates a V-space reference to *existing* I-space content from another document. APPEND adds new stored content. None of these operations allow referencing unstored content.

### The Ghost Element Distinction

Ghost elements might seem like a counterexample, but they operate at a different level entirely. Ghost elements are structural positions in the address hierarchy—servers, accounts, documents—not content bytes:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [4/23]

Ghost elements are containers with no stored representative object. They are *not* content that a document's V-stream can include. You can link *to* a ghost element (a link's endset can point to an empty address), but you cannot include a ghost element in a document's byte stream.

### Link Endsets vs. Document Content

Link endsets and spans *can* reference addresses where nothing is stored:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [4/45]

> "A span that contains nothing today may at a later time contain a million documents." [4/25]

But these are references in the link/span addressing layer, not positions in a document's V-stream. A link's type endset can point to an empty address by design (type matching is by address, not content). A span can designate an empty range. Neither of these constitutes a document "containing" unstored content.

### Summary

The architecture has two layers with different rules:

| Layer | Can reference empty addresses? |
|-------|-------------------------------|
| **V-stream** (document content) | **No** — every position maps to stored I-space bytes |
| **Link endsets** (connections) | **Yes** — can point to ghost elements, empty ranges |
| **Spans** (address ranges) | **Yes** — can designate ranges with no current content |

A document's arrangement is always a concrete view over real, stored content. The addressing and linking layers are more permissive, allowing forward references and structural pointers into empty space. This separation is consistent with Nelson's design: content is permanent and real; connections and addressing are abstract and anticipatory.
