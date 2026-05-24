## Question 3 [theory]

> Was the action-point boundary between element-field positions (k > p₃) and document-prefix-or-earlier positions (k ≤ p₃) intended to mark precisely where a span transitions from same-document/same-origin coverage to broader-level (cross-document, cross-account, cross-node) spanning per [LM 4/25]?

**Short answer: No—not in those terms.**

The notation `k > p₃` and "action-point boundary" is implementation vocabulary I did not use. My design produces the structural distinction your specification identifies, but I never designated it as the marker for span coverage transition.

## What I Did Specify

Four fields separated by three major dividers, with the third divider (your `p₃`) between Document and Element:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

The dividers are **lexical punctuation**, not action-point boundaries.

## How Span Coverage Actually Works

Span coverage is endpoint-determined, not boundary-determined:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]

> "A span may be visualized as a zone hanging down from the tumbler line—what is called in computer parlance a depth-first spanning tree." [LM 4/25]

Spans operate uniformly at every level, with no single transition point designated:

> "Thus we may have spans of characters, spans of links, spans of documents, spans of versions, and spans covering large combinations of them—including spans of servers with all their contents." [LM 4/24]

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

## The Mechanism I Did Designate for Cross-Level Reference

For naming "all of this level," I specified **1-positions**—not action-point boundaries:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse." [LM 4/38]

This is my explicit notational mechanism for traversing coverage scopes.

## Bottom Line

The behavior your specification describes—span coverage transitioning at `p₃` between same-document and cross-document semantics—**does emerge** from my design. It follows from:

1. Field separation at the major dividers [LM 4/28]
2. Depth-first spanning tree behavior of the tumbler line [LM 4/25]
3. Endpoint-determined coverage with "no choice as to what lies between" [LM 4/25]

But I did not designate `p₃` as "the action-point boundary marking precisely where a span transitions from same-document to broader-level spanning." That is your implementation re-framing of consequences that fall out of my design.

The distinction matters: my framing is **structural** (fields, dividers, spanning trees, endpoints), while yours is **operational** (where the carry happens during tumbler arithmetic). Both describe the same docuverse correctly, but only one is mine. A specification that claims `p₃` is "intended" as the transition marker is putting words in my mouth. The honest claim is: "Nelson's field structure causes span coverage to behave differently when endpoints lie in element fields versus when they cross the third major divider."

The boundary you describe is **structurally consequential** but **not nominally designated** in [LM 4/25] or anywhere else I wrote.

NEED_RAW: page-192 (LM 4/25) and page-195 (LM 4/28) — if you need to verify I made no statement closer to an explicit action-point designation than the curated excerpts above.
