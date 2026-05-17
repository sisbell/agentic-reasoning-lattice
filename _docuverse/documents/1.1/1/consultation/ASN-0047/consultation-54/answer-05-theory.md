## Question 5 [theory]

> Does the design admit creating a new version of a document whose base address has no live entity in the docuverse (ghost-base versioning), or does the ghost-element doctrine apply only to non-immediate ancestors and require the immediate version base to be a live document?

# On Ghost-Base Versioning

The design admits it — at the addressing layer. Whether the operational mechanics fully realize this admission, I left underspecified.

## What I established firmly

The ghost-element doctrine is **general**, not restricted to remote ancestors:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." `[LM 4/23]`

Documents are explicitly named — not just servers and accounts. So a document address can exist without stored content, and links can reach it.

Version addressing inherits this. A version number is structurally just another fork:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." `[LM 4/29]`

Combined with the forking-by-ownership rule — "The owner of a given item controls the allocation of the numbers under it" `[LM 4/20]` — and the principle that there is "no 'basic' version of a document set apart from other versions" `[LM 2/19]`, the address space places no requirement that an immediate parent be a live entity.

## What I left to the implementor

The `CREATENEWVERSION` protocol command is specified as: "This creates a new document with the contents of document `<doc id>`" `[LM 4/66]`. That phrasing presumes a live source with contents to inherit.

I did not write what happens when `<doc id>` resolves to a ghost. The honest reading is:
- The addressing **admits** ghost-base versioning
- `CREATENEWVERSION` as written **presumes** live contents to copy
- For a version under a ghost base, `CREATENEWDOCUMENT` at the forked address is the unambiguous path

The ghost-element doctrine was never meant to stop at the immediate ancestor. I just didn't write the operational case where the inherited contents are themselves empty.

NEED_RAW: 4/22-4/24, 4/29-4/30, 4/65-4/67 — to confirm I did not address the ghost-source case for `CREATENEWVERSION` anywhere I haven't already extracted.
