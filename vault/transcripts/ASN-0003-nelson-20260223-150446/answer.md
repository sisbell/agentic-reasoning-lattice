## New Versions Share the Same Permanent Content

When a new version is created, the system does **not** create fresh copies. The new version is a new V-space arrangement that references the **same** I-space content as the original. This is fundamental to how Xanadu works.

### The I-Space/V-Space Separation

The entire architecture rests on separating permanent content (I-space) from its arrangement (V-space):

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space content is permanent and immutable. V-space is the document's current arrangement — a mapping from sequential positions to I-space addresses. A version IS a particular V-space mapping.

### CREATENEWVERSION Creates a New Mapping, Not New Content

The operation specification states:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." [LM 4/66]

"With the contents" means the new version's V-space points to the same I-space addresses. No bytes are duplicated. The new document gets a fresh V-space arrangement that initially maps identically to the original's V-space, but both map to the **same** underlying I-space content.

Nelson describes the result as prismatic — the same content refracted through different arrangements:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another. We believe our Prismatic storage can support virtually instantaneous retrieval of any portion of any version (historical or alternative)." [LM 2/19]

And crucially:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

The phrase "the same materials" confirms that versions share content, not duplicate it.

### Why This Must Be So: Correspondence Depends On It

The system's ability to compare versions structurally **requires** shared I-space addresses:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

Correspondence works because two V-space positions that map to the same I-space address are, by definition, "the same content." If CREATENEWVERSION created fresh copies with new I-addresses, the system could never determine which parts correspond — the structural basis for comparison would be destroyed.

This is also what enables refractive link following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Links point to I-space. If two versions share the same I-space addresses, a link to content in one version automatically reaches the same content in the other.

### No Copying — By Design

Nelson is explicit that the system avoids copying:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

The COPY operation in FEBE is itself transclusion — inclusion by reference, not duplication:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

This "copy" creates a V-space mapping to existing I-space content. CREATENEWVERSION does the same thing for the entire document.

### What Happens After Versioning

Once the new version exists with its shared V→I mapping:

- **Edits to the new version** (INSERT, DELETE, REARRANGE) change only the new version's V-space. The original version's V-space is untouched.
- **New content** added via INSERT gets fresh I-space addresses in the new version's address range.
- **Deleted content** is removed from the new version's V-space but remains in I-space, still visible in the original version.
- **Shared content** — anything not yet edited in the new version — continues to reference the original I-addresses.

This is the "ongoing braid" Nelson describes:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

### Summary

| Aspect | What Happens |
|--------|-------------|
| I-space content | Shared — no duplication |
| V-space arrangement | New mapping created, initially identical to original |
| Correspondence | Automatic — shared I-addresses are the mechanism |
| Links | Survive across versions via shared I-space |
| Subsequent edits | Diverge V-space; original unchanged |
| New insertions | Get fresh I-addresses in the new version's space |

The answer is unambiguous: CREATENEWVERSION shares the same permanent content. The new version is a new view over existing material, not a copy of it. This is not an optimization — it is the architectural foundation that makes correspondence, link survivability, and non-destructive editing possible.