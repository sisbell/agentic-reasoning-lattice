# Revision Consultation — ASN-0063

**Review:** review-11.md
**Date:** 2026-03-21 21:41

## Summary

2 REVISE items analyzed: 1 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 2: K.μ⁺ amendment impact on J4 (ForkComposite) not acknowledged

**Category:** NELSON
**Reason:** Whether a forked document should inherit its source's link-subspace mappings is a design intent question. The code-level mechanics are clear, but Nelson's intent for link behavior under forking — whether links belong to a document identity or a document version — determines whether the current behavior is correct.

**Nelson question:** When a document is forked (copied to create a new version or variant), should the new document inherit the source document's out-links, or does each document version build its own link set independently?

**Nelson's Answer:**

## Answer: Link Inheritance on CREATENEWVERSION

The new document inherits the source's **byte content** (through transclusion) but gets its own **empty link subspace**. Out-links are not copied. However, because byte content shares I-addresses across versions, links from the original remain **discoverable** through the shared content.

### Evidence for Separation of Content and Links

Nelson grammatically separates "contents" from "out-links" in his description of documents:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents." [LM 2/29]

CREATENEWVERSION operates on "contents":

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

And each document owns only its home links:

> "A document includes only the links of which it is the home document." [LM 4/31]

Since the new version is a new document with its own tumbler address, its link subspace (the 2.x range) starts empty. The links from the source live in the source's address space and remain owned by the source document.

### Why This Doesn't Matter: Refractive Following

The key insight is that **links don't need to be inherited because they're content-addressed**. The FINDLINKSFROMTOTHREE operation searches by I-address (content identity), not by which document a link lives in. Since the new version transcludes the same I-stream content, links pointing to that content are discoverable from either version.

Nelson makes this explicit:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Here is how it works in practice:

1. **Version 1** has a citation link L from paragraph P to external document X. Link L lives in version 1's link subspace (home = version 1).
2. **CREATENEWVERSION** creates version 2. Version 2's Vstream transcludes paragraph P (same I-addresses). Version 2's link subspace is empty.
3. A reader views version 2. The front end queries FINDLINKSFROMTOTHREE for the I-addresses of paragraph P.
4. Link L is returned — it touches those I-addresses even though it lives in version 1.
5. The reader sees the citation despite L not being "in" version 2.

### Each Version Builds Its Own Link Set

The new version's owner creates new links that live in the new document's link subspace:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]

So version 2 might accumulate its own links over time — new annotations, new citations — while version 1's links remain attached to the shared content and discoverable from both versions.

### The In-Link / Out-Link Asymmetry

This design creates an intentional asymmetry:

| Aspect | Inherited? | Why |
|--------|------------|-----|
| **Byte content** | Yes (transcluded) | Shared I-addresses |
| **Out-links** (owned by source) | No (separate subspace) | Link home determines ownership |
| **In-links** (from other documents) | Reachable via I-addresses | Content-addressed discovery |
| **Source's out-links** | Reachable via I-addresses | Same mechanism as in-links |

From the new version's perspective, the source's out-links are indistinguishable from in-links — they're links in another document that happen to touch shared content. The link search mechanism finds them regardless.

### Architectural Elegance

This is why Nelson emphasizes that links attach to **bytes, not positions**:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" binds to I-address content. When that content is transcluded into a new version, the strap reaches through. No copying of links is needed because the content they're strapped to is shared.

### One Caveat

NEED_RAW: [4/65-4/67] — The curated summary of CREATENEWVERSION is terse. The raw page 233 confirms the description matches what's curated, but if there were additional commentary on link handling in surrounding paragraphs, it would be on pages 4/65 through 4/67. The architectural argument above is strong but the explicit statement "links are not copied on version creation" does not appear verbatim in Nelson's text. The conclusion follows from the separation of "contents" and "out-links" at 2/29, the "home document only" rule at 4/31, and the refractive following mechanism at 2/26.
