## Question 2 [theory]

> At the byte level within a document, was the "strap between bytes" intended to be closed against future same-origin allocations (including child-depth), or is span coverage open by design at all levels?

# Span Coverage: Open by Design at All Levels

**Answer: Open by design at all levels, including byte-level within a document.** The "strap between bytes" attaches to a tumbler range, and the span mechanism is fractally consistent — what holds for servers and documents holds for bytes.

## Direct Evidence

Nelson is explicit that a span is a **subtree**, not an enumeration:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree). Thus we may have spans of characters, spans of links, spans of documents, spans of versions, and spans covering large combinations of them--including spans of servers with all their contents." (4/24)

The contents of a span are **implicit, not enumerated**:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

The decisive quote — span membership is **prospectively open**:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

This explicitly addresses the question of future allocations. If a span's content were closed at creation time against future same-origin or child-depth allocations, this statement would be false.

## Closure Is Available — But Only Via Span-Sets

Nelson provides closure as an opt-in via span-sets:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

The fact that Nelson introduces span-sets specifically for "exactly, including nothing else" confirms by contrast that single spans are **not** closed by default. If single spans were closed, span-sets would be redundant for exactness.

## Fractal Consistency Across Levels

Nelson treats the span mechanism as uniform across the entire addressing hierarchy:

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

And the 1-position notation works identically at every level:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." (4/38)

There is no separate byte-level rule. The same depth-first spanning tree semantics apply whether you're naming "all documents on this server" or "this paragraph in this version."

## Implication for the "Strap Between Bytes"

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." (4/42)

Combined with the subtree semantics: the strap attaches to a **range**, and any byte that comes to occupy a position within that range — including via child-depth forking under a covered position — is gathered by the span. This is consistent with the survivability principle (4/43): links care about whether *anything is left at each end*, not about preserving a fixed enumeration.

## Caveat on Practice vs. Design

In the canonical byte arrangement, byte I-addresses are described as "sequential positions in the content stream" (i-space-addresses.md citing 4/30), so child-depth byte allocation is not the typical pattern. But the **architectural intent** — what the span mechanism *means* — is open by design. If child-depth byte allocations occur within a covered range, the span includes them. Closure is the opt-in (span-set), not the default.

NEED_RAW: 4/24-4/25, 4/30, 4/42-4/43 — to verify whether Nelson anywhere discusses child-depth byte allocation explicitly, or whether the byte-level case is left implicit under the general subtree rule. My reading of the curated sources is that he treats it implicitly under the uniform fractal rule, but the original pages may have diagrams clarifying byte-level structure.
