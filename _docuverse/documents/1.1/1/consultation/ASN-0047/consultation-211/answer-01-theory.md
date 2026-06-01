## Question 1 [theory]

> Does the design require that a provenance entry have a content-subspace containment witness at the moment it is recorded, or only that the content was contained at some point in the document's history?

## Short answer

In Nelson's design, **provenance does not depend on a live, point-in-time containment witness**. Origin/provenance is grounded in the *permanent* Istream address, which is timeless and survives deletion. Containment, by contrast, is a *version-relative* Vstream property — a document "contains" content in particular versions, and that relationship persists historically even after the content is removed from the current arrangement. So the design corresponds to your second option: it requires only that the content *was* contained in some version of the document's history, not that it be contained at the moment a provenance fact is recorded.

A caveat first: the terms **"provenance entry"** and **"content-subspace containment witness"** are not Nelson's vocabulary — they don't appear in the curated sources from *Literary Machines*. The reasoning below derives from Nelson's stated principles (Istream/Vstream separation, tumbler time-independence, DELETE semantics). The precise mechanism is an implementation concern that goes beyond what Nelson specifies.

## Why provenance is not a moment-witness

**1. Time is not part of the address.** Provenance in Xanadu is carried by the I-address itself (the Document field encodes the home document). That address is explicitly time-independent:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

Because origin is encoded structurally and immutably, ascertaining where content came from never requires a check against the current containment state:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

**2. Origin survives deletion from the current version.** DELETE is a Vstream operation; it does not remove content from Istream, and the provenance relationship persists:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

This is the decisive point: if a provenance fact required a *current* containment witness, deletion from the live version would invalidate it. Nelson's model explicitly says the opposite — the inclusion "may remain included in other versions," i.e., the witness is the *version* in which it was contained, which is permanently reconstructable via historical backtrack.

## Why containment is version-relative, not "at some point" loosely

Containment is not a vague historical predicate; it is precise *with respect to a version*. Each version is a distinct Vstream mapping over shared Istream content. FINDDOCSCONTAINING is phrased in present tense but resolves against arrangements:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

A document may contain the content in v1 and not in v2. The containment witness is therefore the specific Vstream arrangement (version) whose mapping touches those I-addresses — and that arrangement is permanently available because no prior version is ever destroyed.

## How this lines up with link survivability

The same logic governs links, which behave like provenance assertions over spans:

> "A Xanadu link is not between points, but between spans of data... If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." (4/42)

A link (and by analogy a recorded provenance fact) does not require its endpoints to remain in the *current* version. It survives as long as the referenced bytes exist anywhere in Istream — which they always do.

## Summary

| Property | Nature | Requires moment-of-recording witness? |
|---|---|---|
| Origin / provenance | Istream — permanent, time-independent (4/18, 2/40) | No |
| Containment | Vstream — version-relative (4/9, 4/63) | No — witnessed by the version, preserved historically |

So: **the design requires only that the content was contained in some (permanently reconstructable) version of the document's history.** A live containment witness at the instant of recording is *not* required, because (a) provenance rides on the immutable I-address, and (b) Nelson explicitly guarantees that included content "may remain included in other versions" after deletion from the current one.

NEED_RAW: 4/63 (FINDDOCSCONTAINING exact wording is from a curated FEBE-operations summary rather than a page-verified quote) — verify against page-230/231 if you need the FINDDOCSCONTAINING quote treated as fully verified.
