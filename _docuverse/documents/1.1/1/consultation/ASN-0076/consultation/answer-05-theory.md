## Question 5 [theory]

> If a link's endsets are modified, must the original endsets remain permanently retrievable as content in their own right?

# Link Endset Modification and Permanence

## Direct Answer

Nelson does **not specify a "modify endsets" operation**. The 17 FEBE commands in XU.87.1 include `MAKELINK`, `RETRIEVEENDSETS`, and various link-finding operations, but no `MODIFYLINKENDSETS`. Links are created with their endsets and identified by permanent creation-order addresses:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

So in Nelson's specification, the practical answer is: you don't modify a link's endsets — you create a new link.

## If Modification Were Performed

If a system did implement endset modification, Nelson's fundamental principles require that the originals remain retrievable:

**Non-destruction is foundational.** The system is append-only at the storage layer:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**Historical backtrack must always work.** Even explicit deletion does not destroy:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This is the same regime as deleted bytes — the content (or in this case, the link state) becomes "not currently addressable" but remains recoverable.

**Time-navigability is guaranteed.** Nelson promises retrieval of any prior state:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/14-2/15]

## The Architectural Logic

Endsets are first-class content. A link is itself an addressable element in tumbler-space (the `2.N` subspace within a document), and its endsets *are* its content. By the same logic that protects byte content from destructive editing, the original endset configurations would persist in the historical record.

Note also that endsets are **span-sets pointing to spans of bytes** [LM 4/42], not standalone objects. The bytes they point to remain in Istream regardless of what happens to any particular link's endset configuration:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/42]

## Caveat

NEED_RAW: [4/55-4/60] — The curated sources cover link creation, search, deletion, and types thoroughly, but I cannot find Nelson explicitly addressing the modification of an existing link's endsets as a distinct operation. The pages at the end of the links section may discuss this, or it may be genuinely unspecified because the architectural answer is "create a new link instead."

## Summary

Nelson's specification doesn't include endset modification as an operation. If it were added, the principles of non-destruction, append-only storage, and historical backtrack would require the original endsets to remain retrievable — most naturally as a prior state of the link itself, parallel to how deleted bytes "remain included in other versions" [LM 4/9].
