# Correspondence

Source: Literary Machines, 2/20-2/22, 2/26, 3/13, 4/53, 4/70

## What It Means

**Correspondence is a RELATION** - the relationship between Vstream positions that share the same Istream origin.

It is NOT:
- An operation (though SHOWRELATIONOF2VERSIONS computes it)
- A data structure (though it is derivable from structure)
- Metadata (it is inherent in the addresses themselves)

Correspondence is a semantic property that emerges from shared I-addresses. If two V-positions in different documents (or different versions of the same document) map to the same I-address, those positions CORRESPOND.

## User Guarantee

**The system can ALWAYS identify which parts of different versions correspond.**

When you compare two versions of a document, the system can:
- Show you exactly which pieces are the same
- Highlight what has changed
- Navigate from any part of one version directly to the corresponding part of another
- "Scroll through any two versions to see corresponding parts"

This is not dependent on metadata or explicit tracking - it is structural, computed from the I-addresses themselves.

## Principle Served

Correspondence serves the core goal of **intercomparison**:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail - unless it can show you, word for word, what parts of two versions are the same." (2/20)

Without correspondence, you can only place two versions side by side as disconnected wholes. With correspondence, the system can show what is same versus different, allow direct navigation between equivalent parts, and enable meaningful comparison.

## Two Forms of Correspondence

**Implicit Correspondence:** Shared Istream origin (automatic, structural)
- Automatic for any content that shares I-addresses
- Basis for version comparison

**Explicit Correspondence:** Counterpart link (user-asserted)
- For content WITHOUT shared Istream origin
- Translations, parallel passages in different authors, equivalent formulations
- User creates a link to assert "these correspond"

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link.)" (4/53)

## Version-Spanning Links

Correspondence enables "refractive" link following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

This means:
- A link made against version 1 works in version 2
- The system traces correspondence to find the same content
- You never need to know which version a link was made against

## Nelson's Words

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail - unless it can show you, word for word, what parts of two versions are the same." (2/20)

> "The user may scroll through any two versions to see corresponding parts; and much more." (2/21)

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link.)" (4/53)
