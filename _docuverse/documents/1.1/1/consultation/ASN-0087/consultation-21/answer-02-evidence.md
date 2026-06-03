## Question 2 [evidence]

> In udanax-green, does any operation other than the makelink path (`findnextlinkvsa`/`K.μ⁺_L`) ever create a document's first link-subspace V-position, and does fork copy any link-subspace V-positions — i.e., can a first link ever be placed at a depth other than 2?

## KB Synthesis

Two claims are firmly grounded in the KB; one gap must be acknowledged.

## Only CREATELINK places proper entries in the 2.x subspace

The sole code path that writes a well-formed link orgl reference into the document POOM is `docreatelink` via `findnextlinkvsa`, which hard-codes the first link position at `2.1` and subsequent links at `vspanreach` [SS-LINK-SUBSPACE, SS-DUAL-ENFILADE Finding 0009]. `setlinkvsas()` encodes three V-positions: `2.x` (FROM/TO) and `3.x` (TYPE) [SS-DUAL-ENFILADE Finding 0038].

Two other operations *can* land arbitrary content at 2.x, but neither creates a proper link orgl entry:

- **INSERT**: `acceptablevsa()` always returns TRUE; text can be placed at `2.1` [PRE-ENF0-PLACEMENT-GAP, SS-SUBSPACE-CONVENTION Finding 0049].
- **REARRANGE**: pivot arithmetic applies no subspace guard, so text can be displaced into 2.x [PRE-REARRANGE Finding 0051, INT-DELETE-SUBSPACE-ASYMMETRY].

These are convention violations, not makelink operations — they corrupt the link subspace rather than populate it.

## CREATENEWVERSION (fork) copies zero link-subspace V-positions

`docreatenewversion` calls `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads only the document's V-dimension displacement and width, both of which start at the text subspace (position `1`). The 2.x subspace lies structurally *outside* this vspan and is never passed to `docopyinternal` [ST-VERSION-CREATE Finding 0043, Finding 0046, FC-SUBSPACE Finding 0043].

Consequently a version always begins with an **empty link subspace**. Despite this, links are still discoverable from the version through the spanf I-address index, not the POOM [INT-LINK-VERSION Finding 0046].

## Can a document's first link land at a depth other than 2?

For *proper* link orgl entries: **no**. `findnextlinkvsa` always initialises to `2.1` for a document with no prior links, and version fork never propagates 2.x entries, so the first CREATELINK on any document — freshly created or freshly versioned — targets `2.1`.

For convention-violating placements via INSERT or REARRANGE: the first-digit digit of the resulting V-address depends entirely on the caller-supplied position or the cut geometry; it could be any digit. However, the KB does not document any test exercising what `findnextlinkvsa` returns when such contaminating content is already in the 2.x subspace. Whether it would allocate at `2.2` (treating the existing entry as a prior link) or still at `2.1` is not answerable from the KB — that code path has no finding.
