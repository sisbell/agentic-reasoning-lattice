## Question 1 [theory]

> When a new version is created from a prior version (CREATENEWVERSION on an already-edited version), is the new version intended to inherit the prior version's edited content, or to re-fork the original base document's content?

## Answer

**The new version inherits the prior (edited) version's content.** CREATENEWVERSION copies the current contents of whatever document you invoke it on — it does not re-fork the original base document.

### The operation's definition

The FEBE specification is explicit that the operation takes the source document by ID and copies *its* contents:

> "CREATENEWVERSION: This creates a new document with the contents of document `<doc id>`. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

The phrase "the contents of document `<doc id>`" is the key. If `<doc id>` refers to an already-edited version, then the new version starts with *that version's* current contents (its current Vstream arrangement) — including all edits applied to it. There is no mechanism in the operation that reaches past the immediate source back to the original base.

### Why this is consistent with the model

This follows directly from how versions work in the Istream/Vstream model. Each version is a Vstream arrangement over shared Istream content, and CREATENEWVERSION is effectively transclusion of the entire source document:

- The new version transcludes all content from its source by reference (same Istream addresses), not by re-deriving from the base.
- Whatever the source version's *current arrangement* is becomes the starting arrangement of the child.

This is why Nelson frames versioning as an "ongoing braid" — each version builds on the immediately prior state, not on a reset to origin:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

### A caveat on "ancestry"

The new version's tumbler ID records ancestry, but Nelson is careful to note that this naming is not a strict derivation guarantee:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

So the *content* inheritance is determined by which document you pass to CREATENEWVERSION (the edited version, whose contents are copied), while the *address* merely reflects where it sits in the forking tree.

### Summary

When you call CREATENEWVERSION on an already-edited version, the child inherits that version's edited content — not a fresh fork of the original base. To re-fork the base instead, you would invoke CREATENEWVERSION on the base document directly.
