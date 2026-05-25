## Question 2 [theory]

> Must the result include every document that has ever contained that content, or only those that currently contain it?

# FINDDOCSCONTAINING: Currently Contains vs Ever Contained

## My Answer

The result includes documents that **currently contain** the material—where "currently contain" means the bytes are presently addressable in that document's Vstream. But because of Xanadu's permanence model, this is effectively equivalent to "every version-document that has ever contained the material."

## What Nelson Says

The operation definition is precise about tense:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

Note: "**containing**" (present participle), not "have ever contained" or "did contain." The query asks about present state, not history.

## Why "Currently" Effectively Equals "Ever"

The diagram on LM 4/9 distinguishes two states for bytes in a document version:

> "Living bytes (currently addressable)"
> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

In Xanadu, each version is itself a permanent, addressable document:

> "In a sense the version, or subdocument number is only an accidental extension of the document number." [LM 4/29]

So when document D has bytes deleted in version 2:
- **D version 2** does NOT currently contain those bytes (deleted from Vstream)
- **D version 1** STILL currently contains those bytes (its Vstream is frozen)
- **D version 1 is itself a document** with its own tumbler address

Therefore version 1 appears in the FINDDOCSCONTAINING result. The deletion in version 2 doesn't erase history—it just produces a new version-document that doesn't contain the bytes, while the prior version-document persists permanently.

## The Precise Semantic

Document D appears in the result if and only if D's Vstream **currently maps to** any byte in the specified span-set. This excludes:

- Versions where the bytes were deleted (those specific version-documents drop out)
- Documents that never contained the bytes

This includes:

- All current document versions that have the bytes living in their Vstream
- All historical version-documents whose frozen Vstreams contain the bytes
- All documents that transclude the bytes (since transclusions are part of the Vstream)

## The Distinction That Matters

If you delete bytes in version 5 of your document and ask FINDDOCSCONTAINING, you will get back versions 1-4 of your document (which still contain them) but NOT version 5. Each version is asked the same question: "does your current Vstream contain this?" Versions 1-4 answer yes; version 5 answers no.

This is consistent with the deletion semantics: nothing is destroyed, but the current arrangement of version 5 has elected to omit those bytes. Other versions (which are other documents) made different choices.

## Caveat on "Has Ever Contained"

A truly historical query—"what documents EVER had these bytes in their Vstream at any point in time, even if those bytes have since been deleted from a single non-versioned document"—is **not** what FINDDOCSCONTAINING returns. But because Xanadu makes new versions rather than destructively editing, this distinction rarely matters: every edit that removes content produces a new version, and the prior version (containing the content) persists as its own document. The historical record is captured in the version structure itself.
