## KB Synthesis

**YES**, the version WILL discover the after-the-fact link through shared I-addresses.

## Mechanism

The link discovery mechanism operates purely on content identity (I-addresses), not on temporal ordering or document membership:

1. **Version shares I-addresses with original** — `[ST-VERSION-CREATE]` (Finding 0032) establishes that `references(version) = references(source)` at creation time. The version's text content maps to the same I-addresses as the original's.

2. **Link endpoints indexed by I-address** — `[ST-LINK-CREATE]` (Finding 0012): When the link is created on the original, `insertendsetsinspanf()` indexes the link's endpoints by their I-addresses in the spanfilade. These are the SAME I-addresses the version already references.

3. **find_links operates on I-address intersection** — `[SS-FIND-LINKS]` (Finding 0028): "find_links(search_specset) discovers links by I-address intersection, not by document or V-address matching." When `find_links` is called from the version:
   - The version's V-addresses are converted to I-addresses
   - The spanfilade is searched for links whose endpoints intersect these I-addresses
   - The newly created link matches because its endpoints reference the shared I-addresses

4. **Bidirectional discovery is explicit** — `[INT-LINK-VERSION]` (Finding 0008): "Links added to a version are discoverable from the original document, and vice versa... This is bidirectional — links created on either document are discoverable from both." The "vice versa" explicitly covers the scenario where the link is created on the original after versioning.

5. **Global visibility through content identity** — `[INV-LINK-GLOBAL-VISIBILITY]` (Finding 0008): "Links in udanax-green are globally visible through content identity. A link created in any document is discoverable from every document in the system that shares the linked content's identity."

## Why Timing Doesn't Matter

The spanfilade is a permanent index (`[INV-SPANF-WRITE-ONLY]`). When the link is created:
- The spanfilade gains an entry: `I-addresses_of_endpoints → link_id`
- Any future `find_links` call that queries those I-addresses will return this link
- The version already holds those I-addresses (from the earlier VERSION operation)
- Therefore the version will discover the link

The independence works because `[FC-CONTENT-SPANF-ISOLATION]` establishes that link discovery (spanfilade queries) and document content (granfilade state) are separate subsystems. The version's I-address references exist independently of when links pointing to those I-addresses are created.

## Code Exploration

## Answer

**YES**, the version should discover the after-the-fact link through shared I-addresses. Here's the detailed reasoning based on the source code:

### How It Works

**1. CREATENEWVERSION shares I-addresses** [`do1.c:260-299`]

When `docreatenewversion` creates a new version, it:
- Retrieves the original's entire V-span via `doretrievedocvspanfoo` [`do1.c:281`]
- Copies the content to the new version via `docopyinternal` [`do1.c:293`]
- This calls `insertpm` which inserts the **same I-addresses** at the corresponding V-positions

The original and version share content identity — same I-addresses, different V-addresses in different documents.

**2. CREATELINK stores by I-address** [`do1.c:195-221`, `spanf1.c:15-54`]

When a link is created on the original:
- The source specset (V-spans) is converted to I-spans via `vspanset2ispanset` [`orglinks.c:397-402`]
- The link endpoints are stored in spanf indexed by **I-address**, not V-address
- The link is stored at `insertspanf(spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)` [`spanf1.c:119`]

**3. FIND_LINKS queries by I-address without document filtering** [`spanf1.c:56-103`, `sporgl.c:239-269`]

When `find_links` is called on the version:
- The version's V-spans are converted to I-spans via `specset2sporglset` [`sporgl.c:14-33`]
- For each I-span, `sporglset2linksetinrange` queries spanf [`sporgl.c:239-269`]
- **Critical line [`sporgl.c:255`]:** `infoptr = NULL` — no document filtering
- The query at [`sporgl.c:259`] retrieves ALL links matching the I-span, regardless of which document they were created on:
  ```c
  context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
  ```

**The commented-out code at [`sporgl.c:251-254`]:**
```c
if (FALSE/*trying to kluge links followable thru versions */&&((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
  } else
    infoptr = NULL;
```

This comment explicitly mentions "links followable thru versions" with `FALSE`, meaning the feature is **enabled** (the condition is false, so it falls through to `infoptr = NULL`, which allows cross-document link discovery).

### Execution Flow

```
1. ORIGINAL doc at I-address 123 (V-position 1.7)
2. CREATENEWVERSION creates VERSION with same content at I-address 123 (V-position 1.7)
3. CREATELINK on ORIGINAL from V-span 1.7→1.12
   → Converts to I-span 123→width
   → Stores in spanf: {I-span: 123→width, link_id: XYZ}
4. FIND_LINKS on VERSION from V-span 1.7→1.12
   → Converts to I-span 123→width
   → Queries spanf for links at I-span 123
   → Finds link XYZ (no document filtering)
   → Returns link XYZ
```

### Verification

The existing test `scenario_version_copies_what` tests whether links created BEFORE versioning are visible. I can write a complementary test for links created AFTER versioning if you'd like empirical verification.

**Conclusion:** The version WILL discover the link because link discovery operates on shared I-addresses, not document-specific V-addresses, and the query explicitly uses `infoptr = NULL` to avoid document filtering.
