## Question 10 [theory]

> Must the resolved result preserve the identity of the original content, so that the user can tell which underlying material each visible region came from?

# Yes — Origin Identity Must Be Preserved

This is a fundamental, non-negotiable guarantee of Xanadu. When a compound document resolves — combining native content with windowed (transcluded) material from elsewhere — the system must let the user ascertain the home document of any specific character.

This is **structural**, not metadata. It cannot be stripped, falsified, or lost in resolution. Every byte carries its Istream address, and the Document field of that address IS the proof of origin. When a document includes content from elsewhere, the resolved view fetches those bytes from their home location — the fetching mechanism itself enforces the connection.

## Nelson's Words

The core guarantee, stated plainly:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The mechanism that enforces this:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The address structure that carries origin:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

## Why This Matters

I designed transclusion specifically to solve what copying destroys. The whole point of windowing over copying is that **the connection survives**. Compare what happens when someone takes a paper copy out of the system:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy." [LM 2/48]

Within the docuverse, that loss is impossible. A resolved compound document is not a flattened blob — it is a layered structure where each visible region traces back through its I-address to the document that owns it. This is what enables:

1. **Attribution** — readers can always see who wrote what
2. **Royalty flow** — the system knows whom to pay for each byte delivered
3. **"Show me the original"** — readers can always step through a window to the source
4. **Compound authorship** — when a modified document is read, "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]

None of this works if the resolved view loses track of which bytes came from where. The identity of the underlying material is preserved not as an optional feature but as a **conservation law** of the system.
