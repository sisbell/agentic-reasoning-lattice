## Question 4 [theory]

> What must the system record about the relationship between an old link and its modified successor so users can trace the editing history?

# Link Editing History: What Nelson Specifies (and Doesn't)

Nelson does **not** explicitly specify a mechanism for tracking the relationship between an old link and its modified successor. In Xanadu's non-destructive model, "modifying" a link effectively means creating a new one—the system records each link's facts independently, not their successor relationships.

## What the system DOES record for every link

1. **Permanent home address by creation order.** Links keep their position permanently: "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

2. **Endsets and type.** From-set, to-set, and three-set are recorded permanently.

3. **Deletion state for historical backtrack.** Nelson explicitly includes "DELETED LINKS" as a valid state: "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." [LM 4/9]

## What's implicit (not an explicit relationship record)

- **Temporal ordering** is encoded in the addresses themselves. Link `2.755` was created before `2.756`. There is no separate "successor pointer."
- **Deletion is recoverable** but Nelson doesn't specify automatic linking from a deletion to its replacement.

## What users could do (not system-mandated)

Because Xanadu treats links as first-class addressable objects, users can construct supersession relationships themselves via **link-to-link**: "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link" [LM 4/49]. A user could apply the **Document Supersession Link** pattern—"This link indicates that one document or version supersedes another" [LM 4/52]—to relate old and new links.

But Nelson specifies supersession as a **metalink for documents**, not as a system-tracked property of links themselves.

NEED_RAW: 4/31 and 4/52 to confirm whether Nelson discusses link versioning beyond the hint at "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]
