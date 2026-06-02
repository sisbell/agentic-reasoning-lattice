## Question 1 [theory]

> Was the retraction/nullification mechanism intended to apply only to standard-triple links, or should retraction-typed links of any arity (N≥3) carry the same to-set nullifying semantics?

## Short answer

Nelson never specified a "retraction/nullification mechanism" at all, and he never assigned *behavioral* semantics — like "nullifying a to-set" — to any link type. So the premise of the question (that there is a retraction mechanism whose to-set nullifying semantics might or might not extend to higher-arity links) is an **implementation construct, not part of Nelson's design intent**. From Nelson's framework, the question of "which arity carries the nullifying semantics" cannot be answered by appeal to his stated intent, because he gave links no enforced semantics of that kind.

## What Nelson actually says about link types and semantics

Three points from the verified sources are decisive:

**1. Link types are arbitrary addresses; the system attaches no behavior to them.** The back end matches a type by its *address*, not by anything it "means" or does:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

A "retraction" or "nullify" type would, in Nelson's design, just be another arbitrary type address. The back end would not act on it — *interpretation is a front-end responsibility*. There is no system-level rule that a to-set gets "nullified."

**2. Types are open-ended and user-defined — there is no privileged set with special powers.**

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

Nothing in this scheme privileges one arity over another, nor grants any type the power to cancel content at its to-set.

**3. Arity is not fixed at three.** The canonical link has three endsets (from/to/type), but Nelson explicitly allows the type endset to be multiple pointers, and allows compound/higher structures via link-to-link:

> "Note that a link's type—the three-set—may be several pointers." (4/44)

> "Complex relational structures, such as the faceted link... may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

So Nelson's own model already contemplates links "of any arity (N≥3)" as compositions of the basic three-endset structure. He does *not* attach distinct semantics to "the triple" versus "higher arity."

## The closest Nelson comes to "retraction"

The only retraction-adjacent concepts Nelson defines are about **whole-document status**, handled by metalinks and by due process — not by any to-set nullification:

- **Supersession link** — "indicates that one document or version supersedes another... the canonical way to find out whether you are reading the latest version" (4/52-4/53). This *points to* a successor; it does not nullify anything.
- **Withdrawal** is deliberately hard and is a social/contractual process, not a link semantic: "its author may not withdraw it except by lengthy due process" (2/43).

Both are declarative claims to be evaluated by readers/front-ends, consistent with the principle that "social dynamics become visible in the link structure" rather than being enforced by the back end.

## Design-intent guidance for the implementation question

Given the above, the consistent reading of Nelson's intent is:

- A "retraction-typed" link is just a type address. Whether N=3 or N>3, **the back end should treat it identically** — match by address, store, index, deliver. No arity should be specially privileged.
- Any "to-set nullifying" behavior is a **front-end rendering convention**, and if you adopt it, the *type* (the address) is what signals it — not the arity. Restricting the semantics to "standard triples only" would contradict Nelson's symmetry principle, under which all endsets follow the same convention and the type-set may itself be several pointers (4/44).

So if your implementation chooses to honor a nullify convention, it should key off the **type endset's address**, and it should apply uniformly regardless of arity — because Nelson's model gives no basis for binding the behavior to triple-arity specifically.

---

NEED_RAW: 4/52-4/55 — to confirm whether Nelson's "tentative listing" of link types includes anything beyond the supersession/author/title metalinks that could be read as a retraction type with defined semantics. The curated sources strongly indicate it does not, but the full type listing on these pages should be checked directly before treating this as exhaustive.
