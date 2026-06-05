## Question 3 [theory]

> Does the ghost-element principle ("things may be addressed even though nothing is there") extend to a document address that is unallocated — i.e., is reading by position on a non-existent document a legitimate empty-answer question rather than an error?

## Short answer

Yes — the ghost-element principle does extend this way, and the weight of Nelson's design points toward treating a positional read on an unallocated document as a *legitimate empty-answer question*, not an error. But this conclusion is strongest for **linking and search** (which Nelson addresses directly) and is an **inference** for `RETRIEVEV`-style positional reads (which he does not explicitly cover). I'll separate the two.

## What Nelson directly supports

**1. Documents themselves are ghost elements.** The address of a document is a *conceptual position*, not a stored object. Only content bytes and links are actually stored:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." (4/23)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

So an *unallocated* document address is not a special pathological case — every document address is, in essence, a ghost position that may or may not have content stored beneath it. There is no categorical difference between "document not yet allocated" and "document allocated but empty"; both are positions with nothing stored.

**2. Addressing/searching an empty position is explicitly legitimate.** Nelson states this for the link and search path:

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

A search of a position that happens to have nothing under it simply *finds nothing* — it is not an error. This is the answer-by-emptiness model.

**3. Span semantics make emptiness a first-class, temporary state.** This is the clearest philosophical statement that an empty result is legitimate and not exceptional:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

A span over an unallocated document is just a span whose contents are currently empty. The address is well-formed; the answer is "nothing here (yet)."

**4. Search is designed to not treat absence as failure.** The link-search guarantee reinforces that non-satisfaction is normal operation:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

## Where this becomes an inference

The question specifically asks about **reading by position** (the `RETRIEVEV` family), which is different from linking or searching. The curated operations material gives only:

> **RETRIEVEV**: "This returns the material (text and links) determined by `<spec set>`." (4/67)

Nelson specifies no error condition here. By the ghost-element and span logic above, the consistent reading is: a positional read whose spec-set lands in an unallocated (or empty) document returns the empty result — the material "determined by" the spec-set is simply nothing. Treating it as an error would contradict (a) documents being ghost elements, (b) "a span that contains nothing today," and (c) the search-doesn't-fail-on-absence principle.

There is, however, one genuine subtlety the sources do not resolve. A V-position presupposes a Vstream arrangement, and an unallocated document has *no* Vstream mapping at all. So "position 5 of a never-created document" is arguably a slightly different question from "an empty span over a known document." Nelson's text treats the docuverse as a uniform coordinate space where addressing precedes storage, which favors empty-answer; but he never explicitly adjudicates a positional read against a document address that was never baptized.

## Bottom line

Conceptually, Xanadu's address space is "an abstraction, since things may be addressed even though nothing is there to represent them in storage" (4/23). That principle, combined with span emptiness (4/25) and non-failing search (4/60), means an unallocated document address is a *coordinate*, and querying it is a meaningful question whose honest answer is "nothing." Returning an error would treat the address space as object-presence-gated, which is exactly the model Nelson rejects.

NEED_RAW: 4/61-4/70 — to confirm whether the FEBE operation definitions (especially RETRIEVEV, RETRIEVEDOCVSPAN, and any return/error conventions) explicitly distinguish an unallocated document address from an empty-but-allocated one, since the curated text gives the command semantics but no error model.
