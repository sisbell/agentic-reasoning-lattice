## Question 9 [theory]

> Must the deleted content returned be actionable for further operations such as restoration into a new document arrangement?

Yes. Deleted content must remain actionable for restoration and re-use. This follows directly from my design intent.

**The architectural basis:**

Deleted bytes are explicitly characterized as "not currently addressable, **awaiting historical backtrack functions**, may remain included in other versions." [LM 4/9] The phrase "awaiting historical backtrack functions" is the key — deletion is a *pending* state, not a terminal one.

**What restoration requires:**

1. **The bytes remain in Istream.** "Native bytes of a document are those actually stored under its control... all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11] Deletion changes Vstream arrangement only; Istream content persists at its permanent I-address.

2. **Previous versions remain accessible.** "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/14-2/15]

3. **The bytes can be reincorporated.** "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11] This works because I-addresses are stable references usable by COPY (transclusion) into new arrangements.

**The user guarantee:**

A user must be able to reach back, retrieve previously-deleted content via historical backtrack, and bring it forward into a new arrangement — through COPY/transclusion from the prior version, or directly via the permanent I-address. If deleted content were inert — addressable for reading but not reusable — historical backtrack would be a museum exhibit rather than the working capability I specified.

This is the entire point of distinguishing Vstream from Istream: "Safety and backtrack are not separate problems." [LM 2/13, paraphrased in the curated source] Deletion that prevented restoration would collapse this distinction and reduce Xanadu to the "destructive replacement" model I built the system to abolish. [LM 2/14]

**What this does NOT require:**

The deleted content need not be addressable in the *current* Vstream — that's precisely what "not currently addressable" means. Restoration is an explicit act (via historical backtrack, COPY, or version retrieval), not an automatic reappearance.
