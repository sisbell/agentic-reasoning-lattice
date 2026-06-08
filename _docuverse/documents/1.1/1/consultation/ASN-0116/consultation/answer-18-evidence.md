## Question 18 [evidence]

> After an INSERT shifts content rightward, do existing links remain discoverable unchanged because their endsets reference I-addresses, with only the resolved V-positions reflecting the new layout?

## KB Synthesis

Yes, exactly correct. The KB confirms this in several complementary entries.

**Links stay discoverable because discovery is I-address-based**

[INT-LINK-INSERT] (Finding 0030) states this directly: a link targeting "CDE" (I-addresses I.3–I.5) remains valid after inserting "XY" at position 1.3. The link's I-address endpoints are unchanged. `find_links` still works. The V-address interpretation shifts (linked content moves from 1.3–1.5 to 1.5–1.7), but the link itself references I-addresses and needs no update.

This is mechanically enforced by [FC-INSERT-IADDR] (Finding 0030): INSERT never modifies any pre-existing I-address, in the target document or any other. All existing V→I mappings for content outside the insertion point retain their I-addresses; only their V-addresses shift.

**The spanfilade index is untouched**

[FC-CONTENT-SPANF-ISOLATION] (Finding 0012/0036) confirms that INSERT writes to the DOCISPAN portion of the spanfilade but never touches the link index portion. Link endset entries (I-address → link ISA mappings) are read-only after creation.

**Resolved V-positions dynamically reflect the new layout**

[SS-LINK-ENDPOINT] (Finding 0019) notes endsets are *dynamic* — they report current V-positions after edits. [SS-FOLLOWLINK] (Finding 0048) explains the mechanism: FOLLOWLINK retrieves I-addresses from the link orgl, then converts them to V-addresses via the queried document's current POOM. Since the POOM reflects the post-insert shift, the returned V-spans show the new positions.

[INV-LINK-CONTENT-TRACKING] (Finding 0004) captures this as a system invariant: insert before a linked span shifts the reported endset V-addresses; the link itself is unchanged.

---

## Code Exploration

I now have all the evidence needed for a complete, line-cited answer.

---

## After INSERT: Do Link Endsets Remain Discoverable via I-Addresses?

**Yes. The claim is correct and verifiable at every step.** Here is the full code trace.

---

### 1. What address type is stored in a link endset at creation time

`createlink` [fns.c:100–112] calls `docreatelink` [do1.c:195–221].

```c
// do1.c:214–215
specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14–33] dispatches on `VSPECID` to `vspanset2sporglset` [sporgl.c:25]:

```c
// sporgl.c:47–55
vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);   // V → I conversion
...
movetumbler (docisa,              &sporglset->sporgladdress);  // document ISA
movetumbler (&ispanset->stream,   &sporglset->sporglorigin);   // I-coordinate
movetumbler (&ispanset->width,    &sporglset->sporglwidth);    // I-width
```

`vspanset2ispanset` [orglinks.c:397–401] is a one-liner:

```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);   // orglinks.c:401
```

The sporgl is then written to the spanfilade via `insertendsetsinspanf` [do1.c:219] → `insertspanf` [do2.c:119–120] → `insertnd`. The spanfilade entry is `(document-ISA, I-origin, I-width)`. **No V-coordinate is retained.**

Also written to the link's own orgl via `insertendsetsinorgl` → `insertpm` [orglinks.c:75–134], which calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

Here the `V`-index is the link's *own* virtual address (link-space, ≥ 2.0) used to file the crum positionally in the link's POOM — not the content text address. The content I-coordinates remain in the `I` dimension of that same crum.

---

### 2. Does `doinsert` modify any link endset?

`doinsert` [do1.c:87–123]:

```c
// do1.c:118–121
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
/* no ht stuff here, 'cause it's taken care of in */
/*   docopy */ );
```

Two structures are touched:

- `granf` (the global granfilade) — receives the new text atom via `inserttextingranf`
- The document's permutation matrix orgl — `docopy` calls `insertpm` on it, inserting a new (V, I) crum that maps the insertion V-address to the new text's I-address

The **spanfilade** (`spanf`) is never referenced by `doinsert` or `docopy`. It holds no pointer into the path that INSERT traverses. **Link endsets stored in the spanfilade are untouched.**

---

### 3. What the INSERT actually shifts

`docopy` calls `insertpm` on the *document's* orgl. `insertpm` [orglinks.c:75–134] calls:

```c
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);  // orglinks.c:130
```

This splices a new crum into the POOM, changing how V-positions map to I-addresses for all subsequent V-positions. That is the "shift rightward": content that was at V=5 may now appear at V=6 from the perspective of the POOM walk. But the I-addresses of existing content atoms are stable — they were assigned by the permascroll allocator and never renumbered.

---

### 4. How link discovery resolves I-addresses back to V-positions

**`followlink`** [fns.c:114–127] → `dofollowlink` [do1.c:223–232]:

```c
link2sporglset     (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)   // do1.c:229
linksporglset2specset (taskptr, &sporglset->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED)  // do1.c:230
```

`link2sporglset` [sporgl.c:67–95]:

```c
// sporgl.c:83
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
// sporgl.c:86
contextintosporgl ((type2dcontext*)c, NULL, sporglptr, I);
```

The `I` index passed to `contextintosporgl` [sporgl.c:205–220] selects the I-dimension:

```c
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);  // sporgl.c:211
movetumbler(&context->contextwid.dsas[I],  &sporglptr->sporglwidth);   // sporgl.c:219
```

`linksporglset2specset` [sporgl.c:97–123] → `linksporglset2vspec` [sporgl.c:127–137] → `sporglset2vspanset` [sporgl.c:141–176]:

```c
// sporgl.c:155–157
movetumbler (&sporglptr->sporglorigin, &ispan.stream);  // I-origin
movetumbler (&sporglptr->sporglwidth,  &ispan.width);   // I-width
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // I → V
```

`ispan2vspanset` [orglinks.c:389–393]:

```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

This walks the document's current POOM, which now includes the INSERT's new crums, and returns the V-positions that correspond to the stored I-addresses — **the positions as they appear in the post-insert layout**.

**`findlinksfromtothree`** [fns.c:189–202] → `findlinksfromtothreesp` [spanf1.c:56–102]:

```c
// spanf1.c:71–77
specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);  // caller's V → I
sporglset2linkset (taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

The caller supplies V-addresses; `specset2sporglset` converts them to I-addresses via the same `vspanset2ispanset` path. Then `sporglset2linkset` [sporgl.c:222–269] queries the spanfilade using those I-addresses, matching them against the I-addresses stored in link endsets. **The match occurs entirely in I-space**, unaffected by any V-shift.

---

### Conclusion

The architecture confirms every part of the claim:

| Property | Evidence |
|---|---|
| Endsets store I-addresses | `vspanset2ispanset` called in `vspanset2sporglset` [sporgl.c:48]; sporgl fields are I-origin/I-width [sporgl.c:54–55] |
| INSERT never modifies endsets | `doinsert` [do1.c:87–123] only calls `inserttextingranf` + `docopy`; spanfilade untouched |
| V-shift is local to document POOM | `docopy` → `insertpm` on document's orgl [orglinks.c:130]; no other structure modified |
| Follow resolves I→V on demand | `ispan2vspanset` → `permute(..., I, vspansetptr, V)` [orglinks.c:393] walks current POOM |
| Find converts V→I before querying | `specset2sporglset` in `findlinksfromtothreesp` [spanf1.c:71–73]; match is in I-space |

Existing links are discoverable unchanged after INSERT precisely because their endsets are I-addresses, which are invariant. The POOM walk resolves those I-addresses to whatever V-positions the current document layout assigns them — incorporating the shift transparently at query time.
