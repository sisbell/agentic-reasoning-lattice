## Question 2 [theory]

> Was version creation intended to require the version base to exist as an allocated document, or is versioning from a "ghost" tumbler (structurally valid but never instantiated) part of the design — e.g., for prismatic-document ancestry indication where the addressed ancestor need not exist?

# Version Creation and Ghost Tumblers

The addressing structure and the operational mechanics are deliberately separable. Let me distinguish them.

## The Operational Case: CREATENEWVERSION

The FEBE operation requires an existing document because it copies content (via transclusion):

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

So if you're invoking `CREATENEWVERSION`, the base must be an allocated, content-bearing document.

## The Structural Case: Address as Ancestry Indication

Here is the explicit design intent, and it surprises many readers:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

This is deliberate. A version tumbler is an *address*, not a derivation claim. The address structure may indicate ancestry without that ancestry being "true" in any derivational sense. The actual derivation is captured by *content sharing* (Istream identity through transclusion), not by the address itself.

## Ghost Elements Make This Permissible

The general principle is unambiguous:

> "the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A "ghost version" under a ghost document is structurally identical to a ghost element at any other level. The addressing scheme imposes no requirement that the ancestor be instantiated.

## Prismatic-Document Ancestry

This aligns with the Prismatic model. Versions are alternative arrangements, not strictly derivations from a "basic" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Summary of Intent

Yes — ghost-tumbler versioning is permitted by design. The address tree captures *allocation* (who baptized which sub-addresses under whose authority). The semantic relationships between versions — derivation, correspondence, equivalence — are captured separately through content sharing and counterpart links. An implementation may baptize a version tumbler under an uninstantiated parent; the addressing system was specifically built to accommodate this.

What an implementation should *not* do is conflate the two: don't treat the address as proof of derivation, and don't require allocation merely to express ancestry.
