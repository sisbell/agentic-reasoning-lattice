## Question 2 [theory]

> Must the original link remain forever readable at its original address after it has been superseded, exactly as it was before the edit?

## Short answer

No — not as an unconditional guarantee, and the question quietly conflates two things Nelson keeps separate. The strong *"once it exists, it stays forever, exactly, at its address"* promise is what Nelson makes for **published documents**, not for **links**. A link is its maker's property, and the maker may delete it. So a superseded link is not obligated to remain *live-readable* at its original address. What survives is weaker but real: by the non-destruction principle the old link is never truly *destroyed* — it is recoverable through historical backtrack and may stay live in other versions that included it — and because links are not edited in place, whatever is preserved is preserved exactly.

## Whose permanence is guaranteed

Nelson's "cannot withdraw" rule is stated for documents:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

And the reason a superseded *document* must stay is precisely that links were made *to* it:

> "for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

This is the crux: the permanence obligation runs to the **target** (the linked-to version must remain so the link doesn't break), not to the **link** itself. Asserting "the original link must remain forever readable at its address" inverts that obligation.

## Links are deletable; "superseded" really means delete-and-remake

There is no link-supersession primitive — the Document Supersession Link applies to whole documents/versions, not links. There is also no edit-link operation (the link operations are `MAKELINK` plus the find/retrieve calls; you cannot mutate an existing link's endsets). So "superseding" a link means the owner deletes the old one and makes a new one — and only the owner can do this:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

> "Only the owner has a right to withdraw a document or change it." (2/29)

A deleted link does **not** stay live-readable at its address. It enters the same "not currently addressable" state Nelson defines for deleted content:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

So in the *current/live* view, the answer to "must it remain readable at its original address" is no.

## What *is* preserved — and it is exact

The same quote tells you nothing is destroyed: the deleted link "awaits historical backtrack functions" and "may remain included in other versions." Two things follow:

1. **Recoverable, never reused.** Link addresses are permanent creation-order slots — "The links designated by a tumbler address are in their permanent order of arrival." (4/31) Deleting link `2.5` does not renumber the others or reassign `2.5` to a new link, so the original is always backtrack-addressable at its own slot.
2. **Exact.** Because links are not mutated in place, there is no partial edit that could leave a "drifted" version. Whatever is preserved is the original link verbatim.

So on "exactly as it was before the edit": yes, for whatever is preserved — the preservation is faithful, not approximate.

## Putting it together

| Sense of "readable at its original address" | Holds for a superseded link? |
|---|---|
| Directly accessible in the **live/current** docuverse | **No** — the owner can delete it; it becomes "not currently addressable" (4/9) |
| **Recoverable via historical backtrack**, address never reused, exact | **Yes** — non-destruction; "may remain included in other versions" (4/9) |
| Carries the same "cannot withdraw" guarantee as a **published document** | **No** — that guarantee is for documents, and protects the *linked-to* target, not the link (2/43) |

The precise correction to the premise: don't borrow the document-permanence guarantee for links. A link survives *editing of the content it points to* automatically ("Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." — 4/43), but a link is not itself immune to its owner's deletion. It is *non-destructibly recoverable*, not *forever live at its address*.

(One caveat on terminology: Nelson never defines "supersession" for links, so I'm reading "superseded link" as "a link its owner replaced," which routes to the deletion semantics at 4/9. If you instead meant a link pointing *at* a superseded document, then the relevant guarantee is the one in 2/43 — the old target version must remain so the link still resolves.)
