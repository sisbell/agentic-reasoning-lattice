## Question 2 [theory]

> Does the design intend the retraction (deletion) type to be a reserved system type seated outside the content space, so that retraction-type endsets are structurally guaranteed disjoint from content addresses?

**Short answer: No.** My design does not seat a "retraction" or "deletion" type outside the content space, and it provides no structural guarantee that a type endset is disjoint from content addresses. The premise cuts against the link design in three distinct ways.

## 1. There is no retraction/deletion *type* in the design

Deletion in Xanadu is an *operation*, not a link type. Removing content is a Vstream operation (DELETEVSPAN) that leaves the bytes permanently in Istream; removing a link is an ownership action. Neither is expressed as a typed link carrying a "type endset." The closest typed relative is the Document Supersession Link — and it declares *replacement*, not removal:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52-4/53]

Genuine retraction of *published* material is also deliberately heavy in my design, not a lightweight reserved primitive: "its author may not withdraw it except by lengthy due process." [LM 2/43]

## 2. The type system is open-ended, not "reserved"

The point of the three-set is extensibility without a privileged system registry:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

Even the standard list is explicitly provisional — "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended..." [LM 4/52] — and "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]. Standardization is a *convention* for interoperability, never a structural reservation.

## 3. Type endsets are *symmetrical* with content endsets — so disjointness is not guaranteed (the crux)

The type endset is the same kind of object as the from-set and to-set; all three point anywhere:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

"Anywhere in the docuverse" includes addresses where content lives. The search machinery never inspects what sits at a type address — it matches the *address itself*:

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

The "ghost element" provision says a type *may* land on an empty address — not that it *must*:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

So a type endset is *permitted* to occupy a ghost address outside any content, but nothing structurally *forbids* it from coinciding with a content address. Disjointness is allowed, not enforced.

## What this means for your specification

If you want a retraction type pinned to a reserved address (a ghost element in some well-known region) with type endsets *provably* disjoint from content addresses, that is a **constraint you are imposing** — a defensible engineering refinement, but not something my design grants you. Label it as your invariant, not a Xanadu structural guarantee, because it actually *narrows* the symmetry I built in, where the three-set is just another endset that can point anywhere. My design gives you the freedom to *seat* a type at a disjoint address; it does not *guarantee* that every retraction-type endset is disjoint from content.

(For completeness: even the storage model treats deletion as a *state* — "DELETED LINKS… not currently addressable, awaiting historical backtrack functions" [LM 4/9] — rather than as a reserved typed object, which is one more reason the "retraction type seated outside content space" framing has no anchor in the original design.)
