## Question 2 [theory]

> What makes two spans correspond — must they share the same underlying content identity, or is textual equivalence between independently authored passages ever sufficient?

# Two senses of "correspond"

Your question exposes an overloading in the word "correspond," and the answer flips depending on which sense you mean. My design contains one mechanism that *derives* correspondence automatically and a second that lets a human *assert* it. They rest on opposite foundations — provenance in the first case, judgment in the second.

## 1. Structural correspondence requires shared content identity

The correspondence the system finds on its own — what `SHOWRELATIONOF2VERSIONS` returns, and what lets a link "reach through" from one version into another — is grounded entirely in shared Istream origin. It is never a judgment about what the text *says*; it is a fact about where the bytes *came from*.

Everything I wrote about this is framed around versions of the *same material*:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

And the protocol command itself:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

What makes those ordered pairs correspond is that the two spans map to the *same* Istream address. Content identity in Xanadu is established by **creation, not by value**. Two passages that happen to spell out exactly the same words, but were typed independently into two documents, live at *different* I-addresses. They are not the same bytes, they share no origin, and so the system does not — and by design must not — report them as corresponding. This is precisely why I distinguished native bytes from inclusions:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

So for the automatic mechanism the answer is flat: **textual equivalence between independently authored passages is never sufficient.** Identity of origin is required. Note the asymmetry — shared identity guarantees the bytes are the same, but sameness of the visible text does *not* imply shared identity. The machine traces provenance, not resemblance.

This is deliberate, and it is what makes refractive link-following trustworthy. When your link reaches through from an old version to "the same passage" in the newest one, it is following a thread of identity, not guessing at a likeness. If I let mere textual coincidence count, the system would silently conflate passages that were never meant to be the same, and the guarantee would rot from within.

## 2. The counterpart link is equivalence a human vouches for

But I did *not* make shared identity the only road to correspondence — because much genuine correspondence in real literature has no shared origin at all. A translation, a parallel passage in another author, two independent formulations of one idea: these correspond in every sense a scholar cares about, yet they share no bytes. The machine cannot see this, because there is nothing in the provenance to trace. So I provided a second, explicit mechanism — the counterpart link:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link.)" [LM 4/53]

Here a *person* declares "these correspond." The assertion lives as a link that person owns, typically carrying a comment explaining the nature of the equivalence. No shared content identity is required — that is the very case it exists to serve. (And the fact that it exists *as a separate link type* is itself the tell: if two passages already shared Istream origin, you would never need to assert their correspondence, because the system would already know it.)

Notice, too, that the counterpart link reaches *past* the dichotomy you posed. It does not even require *textual* equivalence. The cleanest example is an original and its translation — textually *different*, in different languages entirely, yet counterparts. What it captures is neither sameness of text nor sameness of origin, but *equivalence as judged by a human*: of meaning, function, or role.

## The principle underneath: identity versus equivalence

- **Identity** is mechanical and provenance-based. The system computes it because it knows where every byte was born. Shared identity is the *only* thing that earns *automatic* correspondence — and with it the right to be followed refractively, highlighted in intercomparison, and treated as "the same part" across versions.
- **Equivalence** is a human judgment that two *distinct* things mean the same. Nothing in storage records it, so the system cannot derive it. It must be asserted — and the counterpart link is the vessel for that assertion.

So, directly to your question: two spans correspond *automatically* only if they share the same underlying content identity, and textual equivalence between independently authored passages never triggers that. But correspondence as a *relation in the docuverse* is not confined to identity — a person may always assert it across independent works with a counterpart link, and may do so even where the texts differ entirely, as with a translation. The machine recognizes sameness of origin; only a human can vouch for sameness of meaning.
