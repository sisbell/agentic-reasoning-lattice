## Question 3 [theory]

> Was the retraction operation intended to record each retraction call as a distinguishable audit event (multiset semantics, with duplicates preserved for event reconstruction), or as a state-level flag setting `a ∈ nullified` (set semantics, with duplicates collapsing)?

The curated sources do not contain an operation called "retraction" specifically. Nelson's specification names DELETE (vstream removal) and withdrawal (the "lengthy due process" for published documents), plus peremptory challenge for anonymous defamatory content, but does not formalize a "retraction" operation with semantics that distinguish multiset/set behavior.

What the curated sources DO establish that bears on the question:

**1. The append-only principle strongly favors event semantics over flag semantics.**

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes; integrating them all by means of an indexing method that allows any previous instant to be reconstructed." (2/15)

This is Nelson's most foundational storage principle: changes are events, filed chronologically, with previous states reconstructable. A flag-setting model (`a ∈ nullified`) where duplicate calls collapse would lose the chronological record of *when* and *how often* something was retracted - which is exactly the kind of information Nelson's "space-time vortex" is designed to preserve.

**2. DELETE preserves the deletion event as a recoverable state.**

From `delete-semantics.md`:
> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The annotation "awaiting historical backtrack functions" implies the deletion is recorded as an event that can be traversed back through, not collapsed into a single flag bit.

**3. Operations are events the back end responds to.**

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61)

Each FEBE command is treated as a discrete event. The system is defined by its response to a *stream* of commands, not by an end-state flag set.

**4. However, Nelson does not formalize repeated/idempotent retraction.**

Nelson never addresses the question "what happens if the same retraction is invoked twice?" His specification operates at the semantic level (ownership, access, history), leaving concurrency and idempotency to the implementor — as noted in `session-model.md`:
> "Nelson designs at the semantic level: who owns what, who may see what, what happens on denial. He leaves the concurrency mechanics (locking, session state, token management) to the implementor."

---

**NEED_RAW: 2/43, 2/59-2/60, 4/9, 4/52-4/53** — to verify whether withdrawal/supersession/peremptory-challenge passages contain language clarifying whether retraction-class operations are recorded as events or as state flags. The supersession-link mechanism in particular (4/52-4/53) may inform whether nullification creates a discrete link-event or sets a property.

**Recommendation based on what IS in the sources:** Nelson's append-only philosophy and historical-backtrack guarantee point toward **multiset/audit-event semantics**. A retraction is a *change* (a command issued at a time by an owner), and Nelson's storage model is built around preserving each change as a distinguishable event. Collapsing duplicates into a flag would violate the principle that "any previous instant [must be reconstructable]" (2/15). But this is an inference from Nelson's principles, not a directly cited specification.
