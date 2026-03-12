## Question 14 [gregory]

> When an orphaned link (all endpoint content deleted from every V-stream) becomes discoverable again because its endpoint I-addresses reappear via transclusion into a new document, was this "resurrection" behavior an intended design property that users/applications were expected to rely on?

## KB Synthesis

Yes. This is intended behavior — a natural consequence of the foundational design principles, not an accident.

The resurrection property follows directly from three invariants that were deliberate design choices:

**1. I-addresses are permanent and never reused.**
[INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE] Once bytes are written to the permascroll, their addresses are fixed forever. Deleting content from a document's V-stream removes the POOM mapping but leaves the I-addresses intact in the granfilade. This was the design: "bytes never die, addresses never change."

**2. Transclusion shares I-addresses, not copies them.**
[ST-VCOPY] When any document transcludes content, it acquires the *same* I-addresses the original content held. There is no new allocation. This is precisely what makes transclusion semantically meaningful — shared identity, not shared bytes.

**3. The spanfilade (link index) is write-only.**
[INV-SPANF-WRITE-ONLY] There is no `deletespanf` function anywhere in the codebase. The link index grows monotonically. When a link is created, the I-address → link mapping is permanent. When those I-addresses reappear in any document via transclusion, the spanfilade already knows about the link. `find_links` does an I-address intersection against this permanent index, so it will find the link automatically. [INT-SPORGL-LINK-INDEX]

The `find_links` operation is defined as: return all links whose endpoint I-addresses have non-empty intersection with the search specset's I-addresses. [SS-FIND-LINKS] That definition contains no clause about "only if the content was never orphaned." It just asks: do these I-addresses appear? If a transclusion puts them somewhere, the answer is yes.

[INV-LINK-GLOBAL-VISIBILITY] documents that this global discoverability property "is not a new mechanism but an emergent invariant of the content-identity-based link model." [INT-LINK-TRANSCLUSION] formalizes it explicitly: `vcopy(content, src, dst) ⟹ ∀L :: I-addresses(L.source) ∩ I-addresses(content) ≠ ∅ ⟹ findable(L, dst)`.

**The "resurrection" scenario:**
If link L was created on content with I-addresses α₁..α₅, and all documents delete that content making L orphaned [EC-ORPHANED-LINK], L's link orgl still exists at its permanent I-address [INV-LINK-PERMANENCE] and the spanfilade still maps α₁..α₅ → L. When any document subsequently transcludes content from a source that has those I-addresses — even content that was previously deleted from other documents but persists in the granfilade — L becomes discoverable again. The system makes no distinction between "original" and "resurrected" discoverability.

**The one open question:**
[EC-ORPHANED-LINK, Finding 0005] notes as an open question "whether there should be a mechanism to find orphaned links" *directly* (bypassing the content-identity search path). That's a different capability from resurrection. Resurrection via transclusion was clearly intentional. Whether to provide a direct "find all orphaned links" query was less resolved.

The whole point of building the permanence architecture was that links follow content identity through any transformation — transclusion, versioning, or reappearance after deletion. Applications could rely on this.

---

## Code Exploration

---

## Link Resurrection via Transclusion: Code Analysis

### The Behavior in Question

When all V-stream appearances of a link endpoint's I-addresses are deleted, `find_links` returns nothing for that endpoint — the link is "orphaned." If those same I-addresses later reappear in any document via transclusion (COPY), the link becomes discoverable again. This is the resurrection behavior.

The code confirms this happens. Whether it was *intended* and whether users *were expected to rely on it* requires tracing the full architecture.

---

### 1. Link Endpoints Are Stored as Permanent I-Addresses

The `typesporgl` structure in `xanadu.h:115–121` defines link endpoint storage:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid itemid;
    tumbler sporglorigin;        /* span origin in I-address space */
    tumbler sporglwidth;         /* span width in I-address space */
    typeisa sporgladdress;       /* HOME DOCUMENT I-address */
} typesporgl;
```

All three fields are tumblers representing I-addresses. V-addresses are never stored in the link record itself — they are a conversion layer only. `orglinks.c:389–422` (functions `vspanset2ispanset`, `ispan2vspanset`, `permute`) shows that V↔I conversion is a query-time operation, not a storage operation.

When a link is created, `do1.c:195–221` (`docreatelink`) calls `specset2sporglset` to convert the caller's V-specsets into I-address sporgls, then stores those I-addresses permanently via `insertendsetsinorgl` and `insertendsetsinspanf`.

---

### 2. Deletion Is V-Space Only — I-Space Is Never Touched

`do1.c:158–167` (`dodeletevspan`):

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

`orglinks.c:145–152` (`deletevspanpm`):

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletend` is called with dimension `V` [orglinks.c:149]. This removes the V→I crum from the document's POOM (in granf). The I-addresses in the granfilade are immutable — the granfilade has no delete operation. The bytes still exist. The I-addresses are just no longer mapped from any V-position in that document.

Critically: `deletevspanpm` makes **no call to remove spanfilade entries** [Finding 0057]. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. The spanfilade is structurally write-only.

---

### 3. Transclusion (COPY) Reuses Existing I-Addresses — Not Fresh Ones

`orglinks.c:100–113` (`insertpm`), called by `docopy`:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   /* I-address: REUSED, not allocated */
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   /* V-address: new position */
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
```

`lstream` and `lwidth` are the **existing** I-addresses from the source. They are placed directly into the new crum without any new allocation. The V-position is new (`vsaptr`), but the identity is preserved.

This contrasts sharply with `doinsert` [do1.c:87–123], which calls `inserttextingranf` to allocate *fresh* I-addresses from the granfilade. Re-typing deleted content creates entirely new I-addresses that have no relationship to the originals [Finding 0064].

---

### 4. `find_links` Queries by I-Address

`do2.c:14–46` (`specset2ispanset`) is the gateway: it converts a caller's V-specset (document + V-span) into an I-spanset by looking up the POOM enfilade (`vspanset2ispanset`, `orglinks.c:389–422`). If the V-span currently maps to certain I-addresses, those I-addresses become the search key.

`spanf1.c:56–103` (`findlinksfromtothreesp`) uses those I-addresses to query the spanfilade. `sporgl.c:239–269` (`sporglset2linksetinrange`) calls `retrieverestricted` on the spanfilade indexed by the SPANRANGE (I-address) dimension and returns any link whose endpoint overlaps.

**The implication**: when transcluded content places I-addresses back into some document's POOM, a caller querying that document's V-span will convert to those I-addresses and find any link whose endpoint contains them. The link record has not changed — its stored I-addresses are the same ones that were "gone" and are now "back."

This is empirically confirmed by Finding 0029, test `search_after_vcopy_source_deleted`:

```
Original: "linked" → create link → vcopy to Copy
Delete "linked" from Original
find_links(Original) → []
find_links(Copy)     → [link_id]  ← Still found via shared I-addresses
```

---

### 5. No Orphan Detection, No Garbage Collection

There is no code anywhere in the backend that:
- Checks whether a link's endpoint I-addresses are currently reachable in any V-stream
- Invalidates or removes links when their endpoint content disappears
- Maintains a reference count of "how many V-streams reference this I-address"

`do2.c:110–113` (`acceptablevsa`), called during COPY to validate insertion points:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
  return (TRUE);
}
```

This is a stub. Validation at the insertion layer is intentionally absent.

`dofollowlink` [do1.c:223–232] retrieves stored I-addresses and converts them to V-addresses via `linksporglset2specset`. It does not check whether the I-addresses currently exist in any V-stream before returning. The conversion may yield an empty result if no document maps those I-addresses to V-positions, but no error is raised.

---

### 6. Was Resurrection Intentional?

The code points to a clear architectural answer, though with one important qualification.

**The architecture makes resurrection structurally inevitable and precise.** The entire I-space/V-space separation exists to give content permanent identity independent of its current visible location. Links store I-addresses by design — there was no technical obstacle to storing V-addresses instead, but that choice was never made. The spanfilade being write-only, with no `deletespanf`, means the link-to-I-address index grows monotonically and never forgets.

Most tellingly: the behavior is *precise* in a way accidental features are not. **Only transclusion (COPY) resurrects links; re-insertion (INSERT) does not** [Finding 0064]. INSERT always allocates fresh I-addresses from the granfilade. Re-typing deleted text looks identical in V-space but creates a new I-space identity that has no relationship to any existing link. The resurrection works exclusively through the identity-preserving path.

If resurrection were an accident, you would not expect this precision. The system consistently distinguishes "same content" (same I-addresses, via COPY) from "new content that happens to look the same" (new I-addresses, via INSERT). Links track content, not appearance.

**`finddocscontainingsp`** [spanf1.c:151–188] provides further evidence: this function exists to enumerate all documents that contain a given I-span — the exact capability an application would need to discover whether orphaned link endpoints have "reappeared" somewhere. Its presence implies the designers anticipated this kind of traversal query.

**The qualification**: whether users/applications were explicitly *told to rely on this* is less certain from the code alone. Several implementation details suggest the system was incomplete at the time the code was preserved:
- `acceptablevsa` is a stub (`return (TRUE)` with no validation)
- `dodeletevspan` has `/*&& TRUE*/ /* ht stuff */` — a commented-out placeholder for "ht" (hypertext?) operations that were never implemented
- Finding 0024 documents that `follow_link(type_end)` returns empty when both endpoints are deleted, which appears to be a bug (the type endpoint references the bootstrap document, which was not deleted)
- The spanfilade's lack of cleanup is structurally consistent with the permascroll philosophy but is also structurally consistent with an incomplete implementation [Finding 0057]

---

### Conclusion

**The resurrection behavior is an architecturally intentional consequence of the Xanadu identity model, not a side effect.**

Links are bound to permanent content identity (I-addresses), not to current location in any V-stream. Deletion removes the V→I mapping but leaves the I-addresses, the link record, and the spanfilade index intact. Transclusion — by sharing I-addresses rather than creating new ones — makes those addresses reachable again through new V-contexts. The link's spanfilade entries, never removed, become active again when a query V-specset resolves to those I-addresses.

The precision of the behavior (COPY resurrects; INSERT does not) cannot be accidental. The existence of `finddocscontainingsp` as a first-class query implies the designers modeled the multi-document I-address graph as navigable.

Whether the intended *user contract* was that applications would be built to exploit this — e.g., "trancslude content from a backup document to revive its link network" — is a product design question the code cannot fully answer. What the code does establish is that the designers built a system where content identity is permanent, link semantics are defined over content identity, and no mechanism was ever added to short-circuit the revival pathway. That is an affirmative architectural choice, not an oversight.

**Key code citations:**
- Link endpoint storage as I-addresses: `xanadu.h:115–121` (`typesporgl`)
- V-only deletion, no I-space effect: `orglinks.c:149` (`deletend(..., V)`)
- Transclusion reuses I-addresses: `orglinks.c:105–109` (`movetumbler(&lstream, &crumorigin.dsas[I])`)
- Spanfilade write-only, no cleanup: `spanf1.c` (no `deletespanf` exists)
- Stub validation: `do2.c:110–113` (`acceptablevsa` returns TRUE)
- Multi-document query capability: `spanf1.c:151–188` (`finddocscontainingsp`)
- INSERT creates fresh I-addresses (no resurrection): `do1.c:87–123` (`inserttextingranf`)
