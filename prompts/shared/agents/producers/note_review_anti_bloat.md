## Forward-reference accretion (additional patterns to flag)

This note carries the `review-mode.anti-bloat` classifier, signalling that prior cycles have accumulated meta-prose around forward references. Surface these patterns in addition to the standard review checks above.

Prose that does not advance reasoning is noise the precise reader must work around. Defensive justifications, exhaustiveness claims, use-site inventories, and essay content in structural slots degrade the argument. When you have to skip past meta-prose to follow a claim, that is a finding. Concrete examples, analogies, and statements of what an operation does or does not do are not meta-prose even when they sit in the wrong slot — flag their placement, not their existence.

Reviser drift is a specific form of noise worth naming. Flag when:

- a paragraph imagines a case the claim's carrier or precondition already excludes;
- a paragraph looks like a prior finding's content relocated rather than removed;
- new prose around an axiom explains why the axiom is needed rather than what it says (sub-paragraphs labeled "Scope," "Object-level content," "Protocol rationale," "Why the axiom is needed," etc.);
- multiple paragraphs in different sections defer to the same downstream location ("see X below," "deferred to Y," "the full account is in Z");
- prose justifies document ordering ("placed here to avoid circular dependency on X," "the forward pointer is non-circular by Y argument");
- a definition's introduction enumerates downstream consumers ("this is consumed by X, Y, Z") rather than advancing the definition's meaning;
- two paragraphs in the same document say the same thing in different words.

These patterns compound across cycles if not flagged at source.
