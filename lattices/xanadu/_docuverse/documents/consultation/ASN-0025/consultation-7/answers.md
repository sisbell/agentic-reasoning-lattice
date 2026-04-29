# Revision Consultation — ASN-0025

**Review:** review-7.md
**Date:** 2026-03-07 12:03

## Summary

4 REVISE items analyzed: 3 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 4: P6 status ambiguous between constraint and theorem

**Category:** NELSON
**Reason:** Whether P6 is a universal constraint (documents are irremovable by design) or merely a theorem about the current seven operations depends on whether Nelson intended document permanence as a system guarantee alongside content permanence.

**Nelson question:** Did you intend document permanence — that a document, once created, can never be removed from the system — as a design requirement on par with content permanence, or is it merely a consequence of the operations you defined?

**Nelson's Answer:**

# Document Permanence: Intentional Design Requirement

Document permanence for published documents is an explicit, deliberate design requirement — not an accidental consequence. I stated it directly and gave my reasons. But the full picture has important nuances that distinguish it from content permanence.

## The Explicit Requirement

For published documents, permanence is a first-order design decision:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not sentimental. Other users will have made links to your published work — links that they own, at their addresses. Withdrawing your document would destroy their property:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## The Asymmetry: Published vs. Private

Document permanence is not universal. It applies to **published** documents, not all documents:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Private documents can be withdrawn by their owner. Publication is what creates the permanence obligation — because publication creates dependencies.

I even designed an explicit escape hatch for those who want broad access without permanence:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution."

The very existence of "privashing" proves that published-document permanence is intentional. If permanence were merely a side effect, there would be no need for an alternative that avoids it.

## Two Kinds of Permanence, Two Enforcement Mechanisms

**Content permanence** (I-space) is enforced *architecturally*. The append-only storage model means content cannot be removed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**Document permanence** (published documents) is enforced *contractually*. The publication contract binds the author:

> "Because the conceptual structure expects participants to behave in certain ways, these are embraced in the contract offered to users. These provisions are necessary for the orderly and confident use of published material by many people." [LM 4/4]

Both are design requirements. But content permanence is a technical impossibility to violate, while document permanence is a social/legal obligation that could theoretically be overridden through "lengthy due process."

## The Operations Confirm the Intent

Look at the seventeen FEBE commands. There is no DELETEDOCUMENT. There is no WITHDRAWDOCUMENT. DELETEVSPAN removes content from V-space arrangement, but the document itself — as an addressable entity in the docuverse — persists. CREATENEWDOCUMENT and CREATENEWVERSION create; nothing destroys.

This is not an oversight. I defined the system by its operations:

> "What the Xanadu storage and hypertext system does—and thus is—is defined by the commands to which it responds." [LM 4/61]

A system that lacks a document-removal command is a system where documents are not removed. The operations reinforce the contractual requirement.

## The Deeper Principle

Document permanence serves the same conservation law as content permanence: **the interconnected structure of literature must be preserved**. Content permanence preserves the atoms (bytes). Document permanence preserves the molecules (the addressable, linkable units that other users depend on). Removing either would damage the web.

The answer to your question: document permanence for published documents is on par with content permanence as a design requirement. Both are intentional. They differ only in enforcement mechanism — one architectural, one contractual — because they operate at different levels of the system. But neither is accidental, and both serve the same fundamental guarantee: what is published will survive.
