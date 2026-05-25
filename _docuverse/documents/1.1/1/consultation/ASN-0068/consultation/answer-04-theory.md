## Question 4 [theory]

> Must the determination of shared content be exact, or may it tolerate approximate or near-matching content?

# Determination of Shared Content: Exact, by Identity

The determination of shared content is **exact**. It operates on Istream address identity, not on textual similarity. Two pieces of content are "shared" only when they trace to the same Istream bytes — meaning one was transcluded (windowed) from the other, or both descend from a common source through inclusion. **Coincidental textual identity does not constitute shared content.**

This is not a limitation; it is the entire point of the Istream/Vstream separation.

## Why Exactness Is Essential

Consider two authors who independently type "It was the best of times." In Xanadu, these are *different content* with *different I-addresses*. They are not shared. One did not quote the other; they merely produced coincidentally identical strings. The system distinguishes:

- **Wrote the same words** (independent creation, different I-addresses, not shared)
- **Quoted from the original** (transclusion, same I-address, shared)

This distinction is the foundation of attribution, royalty, and the entire literary economy I propose. If "near-matching" counted as shared, then:

- Attribution would be ambiguous (who originated the words?)
- Royalties would be impossible to assign
- "Find all documents containing this material" would return false positives based on coincidence

From 4/11: *"Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."*

From 4/11: *"Non-native byte-spans are called inclusions or virtual copies."*

The native/non-native distinction is structural — bytes are either at their home location or they are inclusions of bytes at their home location. There is no "almost the same" category.

## How Operations Implement Exact Matching

**SHOWRELATIONOF2VERSIONS** (4/70): *"This returns a list of ordered pairs of the spans of the two spec-sets that correspond."* Correspondence here means shared I-address — exact identity.

**FINDDOCSCONTAINING** (4/63): *"This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located."* The match is on I-address, not on text content.

Intercomparison shows "word for word, what parts of two versions are the same" (2/20) — but "the same" here means *the same bytes by identity*, not the same text by coincidence.

## The Mechanism for Near-Matching: Counterpart Links

I am not blind to the need for asserting semantic correspondence between content that does *not* share Istream origin. Translations, parallel passages in different authors, equivalent formulations in different languages — these are real and important relationships. But they cannot be inferred from byte comparison.

The mechanism is the **counterpart link**, from 4/53:

> *"The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link. Note that a counterpart link will typically have a comment attached to it."*

This is a **user assertion**, not a system inference. The user declares "these two passages correspond" by creating an explicit link. The system does not guess. The system does not run fuzzy matching algorithms. The user — who alone can judge whether two passages are translations, paraphrases, or counterparts — makes the claim and stands behind it.

## Design Principle

The architecture refuses to conflate *identity* with *similarity*. Identity is structural and exact (shared I-address). Similarity is semantic and asserted (counterpart link with comment). The two are kept rigorously separate because conflating them would destroy attribution.

If you want the system to know two passages correspond, **link them**. Do not expect the system to discover it through inspection of bytes.
