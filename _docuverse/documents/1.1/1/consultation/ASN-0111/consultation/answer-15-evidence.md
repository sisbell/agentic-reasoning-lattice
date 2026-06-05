## Question 15 [evidence]

> Does direct read by link ID succeed for an orphaned link whose endpoint content has been deleted from all V-streams, returning the original endset I-addresses unchanged?

## KB Synthesis

## Short Answer

**Yes, the direct read succeeds and the link orgl's stored I-addresses are unchanged — but the caller receives empty V-spans, not the I-addresses themselves.**

---

## Synthesis

### The link orgl is permanent and unmodified

Link orgls live in I-space and are governed by the permanence axiom: once created, no operation removes them [INV-LINK-PERMANENCE]. The endset I-addresses stored inside the link orgl are never touched by document edits. DELETE operates only on the POOM (V-to-I mappings) and leaves both the link orgl and the spanfilade intact [SS-THREE-LAYER-MODEL], [FC-LINK-DELETE-ISOLATION].

### FOLLOWLINK has two independent phases

`link2sporglset()` extracts I-addresses from the link orgl via `retrieverestricted()` — **no POOM check occurs here** [SS-FOLLOWLINK]. The I-addresses come back exactly as stored. This phase always succeeds if the link orgl exists [PRE-FOLLOWLINK].

`linksporglset2specset()` then converts those I-addresses to V-addresses by looking each one up in the specified document's POOM. If `retrieverestricted` returns NULL (no current V-position for that I-address), the entry is **silently dropped** [INV-ITOV-FILTERING], [SS-FOLLOWLINK:`span2spanset:446-448`].

### What the caller actually receives

When all endpoint content has been deleted from every V-stream, every I-address in the endset resolves to NULL in the POOM. Phase 2 drops all of them. The operation returns **success with empty V-spans** `[]` — not an error [EC-GHOST-LINK].

> "These are 'ghost links' — the link structure is intact in the permanent layer, but its endpoints point to content with no current V-position... operation still succeeds." [EC-GHOST-LINK]

### Reconstitution is always possible

Because I-addresses are permanent [INV-IADDR-IMMUTABILITY], copying the original content back into any document (via VCOPY from a surviving version) restores the POOM mapping and makes FOLLOWLINK return non-empty results again [EC-GHOST-LINK].

---

## Precise Answer to the Question

| Aspect | Result |
|--------|--------|
| Does the direct read by link ID succeed? | **Yes** — no error, operation completes |
| Are the endset I-addresses in the link orgl unchanged? | **Yes** — permanent, immutable [INV-LINK-PERMANENCE] |
| Does the caller receive those I-addresses? | **No** — FOLLOWLINK returns V-spans, and all are filtered empty via I→V conversion [INV-ITOV-FILTERING] |

The endset I-addresses are preserved in I-space unchanged; the FOLLOWLINK API surfaces them as empty V-address results because none map to current POOM entries.

---

## Code Exploration

Finding 0024 already has empirical confirmation of the behavior. I now have the full picture from both code analysis and existing test results. Let me write the definitive answer.

---

## Answer

**Short answer:** The call succeeds (no protocol error), but the I-addresses are **not** returned unchanged — the response is a V-spec with an empty span list.

---

### Full Trace

#### Entry point: `followlink` → `dofollowlink`

**`fns.c:114-127`**:
```c
void followlink(typetask *taskptr)
{
    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
    } else
        putrequestfailed (taskptr);
}
```

**`do1.c:223-232`**:
```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
}
```

---

#### Step 1 — `link2sporglset` reads the LINK's own PM, not the document's

**`sporgl.c:67-95`**:
```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
    if (!findorgl (taskptr, granf, linkisa, &orgl, type))   // finds the LINK's orgl
        return (FALSE);
    tumblerclear (&zero);
    tumblerincrement (&zero, 0, whichend, &vspan.stream);
    tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        for (c = context; c; c = c->nextcontext) {
            sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
            contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
            ...
        }
        return (TRUE);
    } else
        return (FALSE);
}
```

**Key point**: `findorgl` is called with `linkisa` — the **link atom's own ISA**, not the document's. The link atom has its own permutation matrix, stored in the granfilade. `dodeletevspan` operates only on the **document's** orgl:

**`orglinks.c:145-152`**:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    ...
}
```

The link atom's PM is **never touched** by `dodeletevspan`. Therefore `link2sporglset` succeeds for any valid orphaned link, returning the I-span data stored at link creation time.

---

#### Step 2 — `contextintosporgl` sets `sporgladdress` to the endpoint's home document

**`sporgl.c:205-220`**:
```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler (&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```

For a link created with V-spec endpoints (the normal FEBE path), the PM crum's `homedoc` is the endpoint document's ISA (non-zero). This was stored by `insertpm` via `unpacksporgl` at link creation:

**`sporgl.c:184-188`**:
```c
} else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
    movetumbler (&((typesporgl *)sporglptr)->sporglorigin, streamptr);
    movetumbler (&((typesporgl *)sporglptr)->sporglwidth, widthptr);
    movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc /* should be sourcedoc */);
}
```

So `sporgladdress != 0` for all V-spec links.

---

#### Step 3 — `linksporglset2specset` takes the V-conversion branch

**`sporgl.c:97-123`**:
```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset, typespecset *specsetptr, int type)
{
    for (; sporglset; ...) {
        specset = (typespecset) taskalloc (taskptr, sizeof (typevspec));
        if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
            // ISPANID branch — returns raw I-address directly
            ((typeitemheader *)specset)->itemid = ISPANID;
            movetumbler(&((typesporgl *)sporglset)->sporglorigin, &((typeispan *)specset)->stream);
            movetumbler(&((typesporgl *)sporglset)->sporglwidth, &((typeispan *)specset)->width);
        } else {
            // V-conversion branch — taken for all V-spec links
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
    }
    return (TRUE);   // always succeeds
}
```

Since `sporgladdress != 0`, the **ISPANID** branch is never taken. The original I-addresses are not returned directly.

Instead, `linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` is called:

**`orglinks.c:389-394`**:
```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` → `span2spanset` → **`retrieverestricted` on the document's orgl**:

**`orglinks.c:425-453`**:
```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                  (typespan*)NULL, targindex, (typeisa*)NULL);
    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    if (!context) {
        return(targspansetptr);  // returns unchanged (empty) if no contexts found
    }
    ...
}
```

When all V-content has been deleted via `deletend`, the document's PM has no I→V mappings for those I-addresses. `retrieverestricted` returns NULL. `span2spanset` returns the target spanset unchanged — which is `NULL`. The V-span is empty.

The final specset item assembled by `linksporglset2vspec`:
```c
specptr->itemid = VSPECID;
movetumbler (homedoc, &specptr->docisa);       // endpoint doc's ISA — preserved
specptr->vspanset = NULL;                       // ispan2vspanset found nothing
sporglset2vspanset(..., &specptr->vspanset, type);  // remains NULL
```

---

#### Step 4 — Wire format sent to client

**`putfe.c:339-343`**:
```c
int putfollowlink(typetask *taskptr, typespecset specset)
{
    putnumber (taskptr->outp, FOLLOWLINK);
    putitemset (taskptr, (typeitemset)specset);
}
```

Since `dofollowlink` returned TRUE, the backend sends `FOLLOWLINK`, not `FAILFLAG`. The itemset contains 1 item of type `VSPECID`:

**`putfe.c:157-162`**:
```c
case VSPECID:
    xuputc (VSPECFLAG, outfile);          // 'v'
    xuputc (WORDELIM, outfile);           // '~'
    puttumbler (outfile, &((typevspec*)itemptr)->docisa);  // endpoint doc ISA
    putitemset (taskptr, (typeitemset)((typevspec*)itemptr)->vspanset);  // NULL → "0~"
    break;
```

Wire bytes: `<FOLLOWLINK>~ 1~ v~ <endpoint_docisa>~ 0~`

The client reads this without raising `XuError` (no `FAILFLAG`), and returns:
```python
SpecSet([VSpec(endpoint_doc_isa, [])])   # non-error, but empty spans
```

---

### Final Answer

**1. Does the call succeed?**  
**Yes.** `dofollowlink` [do1.c:223] returns TRUE for an orphaned link. `link2sporglset` reads from the link atom's own permutation matrix, which `dodeletevspan` never touches [orglinks.c:145]. `linksporglset2specset` always returns TRUE [sporgl.c:122]. The backend sends `FOLLOWLINK` opcode, not `FAILFLAG`. The client does not raise `XuError`.

**2. Does it return the original endset I-addresses unchanged?**  
**No.** The ISPANID return path in `linksporglset2specset` [sporgl.c:112] is only taken when `sporgladdress == 0`. For all links created with V-spec endpoints, `sporgladdress` holds the endpoint document's ISA (non-zero), so the V-conversion branch is taken. `ispan2vspanset` [orglinks.c:389] then looks up the document's PM — which has the deleted content removed — and returns an empty vspanset.

**What is returned:** A `SpecSet` containing one `VSpec` item with the correct **endpoint document ISA** (preserved through `sporgladdress` / `homedoc`) but **zero spans** (the I→V conversion returns nothing for deleted content).

The original I-addresses ARE preserved inside the link atom's own PM (untouched by deletion), but they are never exposed as raw I-spans in the FOLLOWLINK response for V-spec links. They are effectively **read but not returned** — they go into the I→V lookup and emerge as empty.

This is confirmed by existing empirical tests in Finding 0024, which show `source endpoint | Empty` and `target endpoint | Empty` (not error) for both-endpoints-deleted cases.
