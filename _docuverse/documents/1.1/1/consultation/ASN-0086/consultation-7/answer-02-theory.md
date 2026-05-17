## Question 2 [theory]

> Was retraction in Nelson's design intended to nullify exactly one tuple at a time, or was subtree-broad retraction (via a deliberately broader to-span) a designed feature of the retraction primitive?

Looking at this carefully — "retraction" as a named primitive is not in the curated sources. Nelson's closest concepts are DELETE (content), link deletion, document withdrawal, and supersession links. Let me address what's actually attested.

## What Nelson Specifies

**Removal operations are span-based, not tuple-based.** Both DELETEVSPAN and link search/manipulation operate on spans, and spans are explicitly designed to scale from one byte to the entire docuverse:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." (4/38)

The same mechanism handles a single byte and a whole subtree. There is no separate "narrow" vs "broad" primitive — there is one span mechanism that naturally spans both scales.

**A span IS a subtree.** This is explicit:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." (4/24)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

So when an operation takes a span, subtree-scope is the general case; single-tuple is "a degenerate case."

**Link search criteria are span-sets.** From the link-search guarantee:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

The search architecture is designed for spans of any breadth. If retraction is conceived as a span-scoped match (as Nullify with a to-span would be), the span machinery is explicitly designed to accommodate broad to-spans without degrading.

## What's NOT Specified

Nelson does not name a "retraction" or "nullify" primitive in the curated sources. The closest attested operations are:

- **DELETEVSPAN** (4/66) — operates on Vstream spans of any size; doesn't destroy Istream
- **Link deletion** (4/9, 4/12) — owner's administrative right; granularity not discussed
- **Document withdrawal** — requires "lengthy due process" (2/43)
- **Supersession links** (4/52) — declarative obsolescence, not removal

## Inference vs. Direct Statement

The architectural answer (the system is designed for span-scoped operations where broad spans are first-class, not a corner case) is strongly supported by the span/tumbler design. But whether *retraction-as-a-primitive* was specifically intended to support broad to-spans — Nelson never names the primitive, so the answer is by extension, not direct statement.

NEED_RAW: 4/48 (one-sided links), 4/55-4/60 (link filters, junk-link problem, search architecture), 5/19-5/20 (publisher withdrawal contract terms) — these may contain more on removal/withdrawal granularity than the curated extracts surfaced.
