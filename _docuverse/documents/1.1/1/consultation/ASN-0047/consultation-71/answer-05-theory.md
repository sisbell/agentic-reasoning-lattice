## Question 5 [theory]

> When a document is forked, does the new document inherit the source's V-position structure (so V-positions correspond exactly to the source's at fork time), or only the I-address set with V-positions chosen freely by the fork operation?

When a document is forked via `CREATENEWVERSION`, the new document inherits **both** the I-address set **and** the V-position arrangement of the source exactly at the moment of fork. The V-positions begin in correspondence and only diverge as subsequent edits are applied to either version.

## Evidence

**The operation creates content, not just identity:**

> "CREATENEWVERSION: This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

"With the contents of" — not "with references to the I-addresses of" — implies the new document is a Vstream snapshot, preserving arrangement.

**The Prismatic refraction model presupposes corresponding positions:**

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." (2/19)

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

For a "given part" to refract across versions, that part must occupy correspondent positions in each — initially identical, then progressively rearranged by edits.

**Refractive link-following requires correspondence at fork time:**

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

A link made against version 1 must immediately work against a freshly-forked version 2. This guarantee only holds if the fork preserves the V-arrangement so correspondence is non-trivially defined from the start.

**Correspondence is structural, derived from shared I-addresses:**

> "Correspondence is a semantic property that emerges from shared I-addresses. If two V-positions in different documents (or different versions of the same document) map to the same I-address, those positions CORRESPOND."

At fork time, every V-position in the new version maps to the same I-address as the corresponding V-position in the source — and (importantly) at the same V-coordinate, since no editing has yet occurred.

## Important Caveat on Address Semantics

The fork's *address* (version subfield) does not by itself constrain content:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

This refers to the **address-tree relationship**, not the content relationship. The version number is a designator; the V-arrangement inheritance is a property of the `CREATENEWVERSION` operation, not the addressing scheme.

## What Nelson Does Not Explicitly State

Nelson does not write a sentence of the form "V-position N in the forked version corresponds to V-position N in the source at fork time." The conclusion is the natural reading of:
1. `CREATENEWVERSION` inheriting "contents"
2. Prismatic refraction
3. Refractive link-following guarantees
4. The Vstream-over-Istream view model

NEED_RAW: 4/66 for the full `CREATENEWVERSION` paragraph context, and 4/70 (`SHOWRELATIONOF2VERSIONS`) for any commentary on initial-fork correspondence behavior — to confirm whether Nelson directly addresses fork-time V-coordinate identity rather than leaving it implicit.
