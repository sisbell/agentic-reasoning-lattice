## Question 5 [nelson]

> Can a document within one node contain content that originates from a different node, or is each document confined to material held locally?

## Yes — absolutely. Cross-node inclusion is fundamental to the architecture.

A document's virtual byte stream can include bytes from **any** document in the docuverse, regardless of which node stores them. This is not a special case; it is the normal mode of operation.

### The mechanism

Nelson distinguishes two kinds of bytes in a document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The I-space address itself encodes the originating node — `Node.0.User.0.Document.0.Element` — so the system always knows where to fetch non-native bytes. When your document on node 3 transcludes a passage from a document on node 7, the back end requests those bytes from node 7's storage. The user sees a seamless document.

### BEBE makes it invisible

The entire purpose of the inter-server protocol (BEBE) is to make node boundaries disappear:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

Requests fan out from the user's local server to whichever servers hold the needed content, and replies funnel back:

> "First, by the forwarding of requests as they fan out from users to servers able to supply..." [LM 4/70]

Each server maintains a "microcosm" — a cached subset of the whole docuverse that grows and shrinks with demand:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

Popular remote content migrates closer to users who request it. The contents "slosh back and forth dynamically" [LM 4/72].

### The user experience

From the user's perspective, there is one docuverse, not a collection of servers:

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." [LM 2/36]

The user never specifies which server to contact. They work with tumbler addresses; the network resolves them.

### Why this matters

If documents were confined to local material, transclusion would be limited to content on the same server — which would fragment the docuverse into isolated silos. The entire vision of a unified, interconnected literature depends on cross-node inclusion working transparently. The vendor interoperation contract makes this a legal obligation, not just a technical capability:

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [LM 5/14]

In short: a document is a V-space arrangement over I-space content. V-space is local to the document; I-space is global to the docuverse. The document reaches anywhere it needs to.
