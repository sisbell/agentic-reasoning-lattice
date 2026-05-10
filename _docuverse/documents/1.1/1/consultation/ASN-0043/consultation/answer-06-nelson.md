## Question 6 [nelson]

> Is a link itself a piece of content — something that can be addressed, quoted, and linked to in turn — or is it a separate category of object outside the content space?

## Links Are First-Class Objects in the Same Address Space as Content

The answer is **both**: a link is a stored, addressable object in tumbler-space — fully capable of being linked to in turn — but it is architecturally **distinct** from content bytes. Nelson designs links as a separate category of element that nonetheless shares the universal address space.

### Links Live in Tumbler-Space Alongside Bytes

The two types of entity actually stored in the docuverse are bytes and links, and nothing else:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

Links have their own tumbler addresses within each document, occupying the `2.x` subspace:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

While content bytes occupy the `1.x` subspace. This subspace distinction is structural — links and bytes are different *kinds* of element sharing one address space, not different spaces entirely.

### Links Can Be Linked To

Because links have addresses on the tumbler line, they can be targets of other links. Nelson is explicit that this requires no special mechanism:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

This is not a special "meta-link" feature. It falls out of the uniform addressing: if you can point at an address, and links have addresses, then you can point at links. From this primitive, Nelson derives compound structures:

> "Complex relational structures, such as the faceted link, may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

### But Links Are Not Ordinary Content

Nelson calls links "meta-virtual structures" — they are *about* content rather than *being* content in the way bytes are:

> "The Xanadu link is a meta-virtual structure connecting parts of documents (which are themselves virtual structures)." [LM 4/41]

Key differences from content bytes:

1. **Separate subspace.** Bytes are in `1.x`, links in `2.x`. The system distinguishes them structurally.

2. **Permanent order of arrival.** Unlike bytes (which can be rearranged in V-space), links keep their creation-order addresses permanently: "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

3. **Three-part internal structure.** Bytes are raw content. Links have structured internals: from-set, to-set, and type — each an arbitrary span-set pointing into the docuverse.

4. **Owned independently of what they connect.** "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

### The Architecture's Answer

Nelson's design resolves the question by refusing the dichotomy. Links are not "content" in the sense of being undifferentiated bytes in the permascroll. But they are not "outside the content space" either — they are fully within tumbler-space, fully addressable, fully linkable-to. The system has exactly two kinds of stored element (bytes and links), both first-class, both permanent, both addressable through the same tumbler mechanism.

The docuverse is built from these two primitives and nothing else:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

So: a link is an addressable, ownable, linkable-to object that shares the universal address space with content — but is structurally and semantically distinct from content bytes. It is a **peer** of content in the address space, not a subordinate of it, and not external to it.
