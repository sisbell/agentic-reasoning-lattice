## Question 6 [theory]

> If a document once contained the specified content but no longer does, must the system still report it, and under what identity?

# Answer

**Yes. The system must report it, under the identity of the specific version where the content remains.**

This follows directly from three principles I've established:

## Nothing is ever destroyed

DELETE is a Vstream operation, not an Istream operation. When you "delete" content from a document, you remove it from the current arrangement, but it persists everywhere it has ever been. As the diagram on 4/9 makes explicit:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And further:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## Versions are themselves addressable as documents

A version is not metadata about a document — it IS a document, accessed by an extended tumbler address:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

There is no privileged "current" identity:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## FINDDOCSCONTAINING must return all containing arrangements

The operation is defined to return *every* document holding the specified material:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

## What this means concretely

If document D at version V1 contained span X, and at version V2 the owner deleted X from the current arrangement:
- V1's tumbler still resolves and still contains X
- V2's tumbler resolves but no longer contains X in its Vstream
- FINDDOCSCONTAINING(X) must return V1 (and any other versions/documents that include X)
- The reported identity is the full tumbler **down to the version** — not the unversioned document family

To return less would be to lie about history. The whole point of Prismatic storage is that you can ask for "a certain part of a certain version at a certain point in time" [LM 2/15] — which is meaningless if past arrangements become invisible to discovery once superseded.

## The deeper guarantee

This is the historical backtrack guarantee made operational. A user who searches for content must be able to find every arrangement that ever contained it, with sufficient address precision to retrieve that exact arrangement. Otherwise the "permanent archive" promise [LM 3/25] is hollow — searches would silently rewrite history each time an owner edited.
