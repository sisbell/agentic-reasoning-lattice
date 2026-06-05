## Question 8 [theory]

> What permanence guarantee must hold across the combined result, so that every fragment refers to the same version of the document?

## The permanence guarantee: version-pinned Istream immutability

When a document is reconstructed from scattered fragments — Nelson's "part-pounce," where the part "materializes... while you are, as it were, in midair" (2/16) — coherence requires that **every fragment resolve through the same version's Vstream mapping to immutable Istream content**. Two layers must hold:

**1. The version is fixed by its tumbler address.** A version is not a separate copy but a particular arrangement, identified by the version subfield of the document tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (4/29)

Because tumbler addresses are permanent, the version reference itself never drifts:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

**2. Istream content is immutable.** Each fragment — whether native or transcluded from elsewhere — is addressed in Istream, and content at an Istream address never changes. This is what lets the assembled result be self-consistent even when fragments come from many home locations:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

## Why this guarantees same-version coherence

A version pins a Vstream arrangement; the Vstream maps to permanent Istream addresses; Istream content never changes. So when you request "a given part of a given version at a given time," the system reconstructs **one** arrangement, and every fragment in the combined result is drawn through that single version's mapping:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

The retrieval operation that does this assembly is **RETRIEVEV**, which "returns the material (text and links) determined by `<spec set>`" (4/67) — the spec-set addresses being version-qualified tumblers.

## The crucial consequence

Because deletion is Vstream-only and Istream is never destroyed, a version reconstructed today returns identical bytes when reconstructed later — no fragment silently shifts to a newer revision:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

This is exactly the separation that makes the guarantee hold: **arrangement is flexible (Vstream), content is permanent (Istream), and the version tumbler is the permanent key that binds every fragment of the combined result to one consistent arrangement.**

A caveat worth flagging: a *location-fixed* (floating-in-time) transclusion window deliberately tracks the current version of its source and so updates automatically, whereas a *time-fixed* window pins a specific version (2/37). If a combined result must have every fragment refer to the *same* version, the constituent windows must be time-fixed, not location-fixed.
