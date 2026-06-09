## Question 1 [theory]

> Is an unattributed retraction (no attributing source) intended as a semantically distinct operation, or is attribution always conceptually present and the `F = ∅` form merely a notational default?

## Design intent: attribution is always conceptually present

Attribution is **always conceptually present**. The `F = ∅` form is a notational default — it records that the *from-set / derivation slot* is empty, not that the operation has no responsible party. An "unattributed retraction" in the strong sense (an operation with genuinely no attributing source) is not a coherent object in my architecture, and it was never intended as a semantically distinct operation.

The reason is a distinction I drew deliberately and which the formal notation must not collapse: **who is responsible for a link is carried on a different channel than what the link points from.**

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

A retraction — whether you formalize it as a supersession-style metalink or a deletion declaration — is a link, and:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

So ownership/attribution is *structural*: it rides on the home document, the address at which the link lives. The from-set can be emptied without touching it. That is exactly why the empty form is admissible at all — I designed for one-sided links:

> "An important variation where a link has only one side - something pointing to material, but not from other material. The paragraph designator is an example... since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

The lesson from the one-sided link is the lesson for `F = ∅`: an empty endset is a statement about *what is reached*, never about *who reached*. The endset and the home/ownership are orthogonal.

## Why this matters: claims are always *someone's* claims

The same principle governs supersession and authorship, which is the family retraction belongs to. Even a claim made from *outside* a document is still an owned, attributed claim:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52)

A retraction is a *claim that something is withdrawn or replaced*, and in my system every claim has a home address, hence a responsible party. The claim/authority distinction matters socially — a third party's retraction of someone else's work is a claim to be weighed, not an authoritative act — but at no point is it *unattributed*. The home address tells you who said it.

## The one apparent exception, and why it isn't one

The closest thing to "no attributing source" in Xanadu is John Doe publication — anonymous, walk-in content. But anonymity there is *real-world identity hidden*, not *structural attribution absent*. The content still occupies an owning address; that is precisely what lets an affected party act against it:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." (2/60)

So even the anonymous case is *attributed-but-pseudonymous*, not unattributed. It does not give you an operation that floats free of all ownership.

## Bottom line for the formalization

Treat `F = ∅` as a notational default within an operation whose attribution is supplied on a separate, always-present channel (the equivalent of the link's home/ownership). Do **not** introduce a distinct "unattributed retraction" operator. If you did, you would be modeling an object my design forbids — a link with no home — and you would be conflating two axes (the from-set and the responsible party) that I kept deliberately independent (4/12, 4/48).

---

*Scope note:* the `F`/`G` notation and the term "retraction" are your formalism's, not language from Literary Machines; I have answered the underlying design-intent question by mapping retraction onto Nelson's owned-link / supersession / deletion machinery. If you want the formal spec's own treatment of the attribution slot pinned to a specific operation signature, that lives in the project's substrate docs rather than in Literary Machines.
