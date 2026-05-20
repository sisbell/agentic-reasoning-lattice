## Question 1 [theory]

> Was Attribute (parent → sidecar) intended to carry at-most-one sidecar per parent document as part of its design semantics, distinct from the slot-pair distinctness Sh4 enforces?

# Answer

The terminology in your question — "Attribute," "sidecar," "parent document," and "Sh4 slot-pair distinctness" — is not language I used in *Literary Machines*. These appear to be specification-level constructs developed by implementors, not concepts I introduced. I cannot tell you what *was intended* for them without knowing the spec.

What I can tell you is what I actually wrote about cardinality and link structure:

**I did not specify cardinality constraints on link types.** When I introduced metalinks like Title, Author, and Document Supersession Link [LM 4/52], I described their semantics but never said "at most one per document." Quite the opposite — the Author link is explicitly multi-valued by design:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52]

Multiple Author claims can coexist. The system surfaces all of them; users judge.

**My general posture on link types was permissive, not restrictive:**

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

> "What the 'type' designation points to is completely arbitrary." [LM 4/44]

**Where I did discuss "uniqueness," it was about address uniqueness, not relationship cardinality.** Tumbler addresses are unique [LM 4/19]; link instance addresses are sequential and permanent [LM 4/31]. But I never built cardinality constraints into the type system.

**On the specific question of parent→sidecar uniqueness:** If your spec wants "at most one sidecar per parent," that is a design decision *you* are making — not one I dictated. My architecture would accommodate it (you'd enforce it at link-creation time), but it's not implied by anything I wrote. The closest natural analog might be Document Supersession Link [LM 4/52-4/53] which is described as "the canonical way to find out whether you are reading the latest version" — but even there I did not say a document can have only one supersession link pointing into it.

**Recommendation on intent:** Distinguish carefully between:
- *Slot-pair distinctness* (a structural constraint on link instances — no duplicate (from, to) pairs of a given type)
- *Cardinality constraints on a relation* (at most one sidecar per parent)

Those are different invariants. I specified neither. If your spec needs both, they should be motivated by the user-facing guarantee you're trying to deliver, not by appeal to *Literary Machines*.

NEED_RAW: none — the curated sources are sufficient to establish that I did not specify these constraints. The gap is in your spec's design intent, not in my source text.
