## Question 5 [nelson]

> Does a link exist outside the documents it connects, as an independent object in the docuverse rather than being embedded inside one of them?

## Yes and No — Links Are Independent of What They Connect, But Not Free-Floating

The answer is both yes and no, and the distinction matters.

### Yes: A Link Is Independent of the Documents It Connects

A link does NOT live inside the documents it connects. It lives in its **home document**, which can be entirely separate from the documents at either end:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

The MAKELINK operation makes this explicit:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." (4/63)

So if Alice writes document A and Bob writes document B, Carol can create a link in her own document C that connects passages in A to passages in B. Carol's link lives at Carol's address, under Carol's ownership. Neither Alice nor Bob can delete it.

Links have their own tumbler addresses in the **2.x subspace** of their home document, their own endsets reaching out across the docuverse, and their own survival properties independent of the documents they connect.

### No: Nothing in Xanadu Is Truly Free-Floating

Every link must have a home document. There are no objects in the docuverse outside the document structure:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

A link is always *part of* a document — it just isn't part of the documents it *connects*. The home document is where it physically resides, determines who owns it, and provides its tumbler address.

### The Design Intent

This separation of link residence from link targets is one of my most important architectural decisions. It solves the **marginalia problem**: how do you annotate someone else's work without modifying it?

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." (2/31)

Your links are YOUR property at YOUR address. They reach into other people's documents without touching them. The target author cannot delete your links — they can only delete content that the links point to. And even that won't necessarily kill the link, because links attach to spans of bytes and survive as long as any bytes remain at each end (4/42).

This is why I insisted that published documents cannot be withdrawn — other people's links depend on their continued existence. Those links are other people's property, stored at other people's addresses.

### Summary

A Xanadu link is **structurally independent** of the documents it connects — it lives in a separate home document, has its own address, and is owned by its creator. But it is not **ontologically independent** — it must always belong to some document. The docuverse contains documents and nothing else; links are elements within documents that happen to reach across the entire address space.
