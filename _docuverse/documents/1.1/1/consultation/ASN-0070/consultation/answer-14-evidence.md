## Question 14 [evidence]

> For a link whose endset references I-addresses that exist in the granfilade but appear in NO open document's POOM, does endset resolution return an empty VSpecSet, a partial result containing only the source-document positions, or raise an error?

## KB Synthesis

## Endset Resolution With No POOM-Mapped I-Addresses

The operation returns an **empty VSpecSet and succeeds without error**. There is no partial-result-from-source-document behavior — the resolution is filtered purely by what the queried document's POOM currently maps.

### Mechanism

[SS-FOLLOWLINK] describes the two-phase call chain: `link2sporglset()` extracts I-addresses from the link orgl (no POOM check at this stage), then `linksporglset2specset()` converts each I-address to a V-address by calling `retrieverestricted()` against the specified `homedoc`'s POOM. When `retrieverestricted()` returns NULL — meaning that I-address has no POOM mapping — the address is **silently dropped**. No V-span is appended. The operation continues and returns whatever (possibly empty) accumulation remains.

### Universal Invariant

[INV-ITOV-FILTERING] states this is system-wide, not FOLLOWLINK-specific: every operation that performs I-to-V conversion silently excludes unreferenced I-addresses. No such operation returns a V-address for an I-address with no current POOM mapping. The same filtering path (`linksporglset2specset()` → `span2spanset()`) is shared by RETRIEVEENDSETS as well [SS-RETRIEVE-ENDSETS].

### Three Observable Cases

[EC-GHOST-LINK] gives the complete taxonomy for endsets referencing unreferenced I-addresses:

| Case | Condition | Result |
|------|-----------|--------|
| 1 | All I-addresses have POOM mappings | Full VSpecSet |
| 2 | Some I-addresses mapped | Partial VSpecSet (only live ones) |
| **3** | **None mapped (the question's case)** | **`[]`, success** |

[PRE-FOLLOWLINK] is explicit: "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

### One Prerequisite

The homedoc parameter itself must be open. [SS-DOCUMENT-LIFECYCLE] / [PRE-RETRIEVE-CONTENTS] note that `findorgl()` fails if the document is not in the open list, which would cause the operation to fail. But given the homedoc is open and its POOM simply has no entries for these I-addresses — empty VSpecSet, no error.

The granfilade's permanence of those I-addresses [INV-IADDR-IMMUTABILITY] is irrelevant to resolution: granfilade existence enables reconstitution (COPY the I-addresses into a new document), but the current query result depends solely on the live POOM state.

---

## Code Exploration

I now have the complete picture from the source code. Here is the full answer.

---

## Endset Resolution When I-Addresses Are Absent from All Document POOMs

### The Short Answer

**Neither empty VSpecSet nor error.** The backend returns a degenerate partial result: a VSpecSet containing one vspec entry per endset sporgl, where each vspec has the homedoc document ISA set but an empty (zero-span) inner vspanset. No `FAILFLAG` is sent.

---

### Execution Trace

#### Entry point: `followlink` [fns.c:114–127]

```c
if (getfollowlink(taskptr, &linkisa, &whichend)
 && dofollowlink(taskptr, &linkisa, &specset, whichend)){
    putfollowlink(taskptr, specset);
} else
    putrequestfailed(taskptr);
```

#### Step 1 — `dofollowlink` [do1.c:223–232]

```c
return (
   link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                         sporglset, specsetptr, NOBERTREQUIRED));
```

#### Step 2 — `link2sporglset` [sporgl.c:67–95]

This reads the **link's own POOM** (via `findorgl` + `retrieverestricted` on the link's granfilade node at `V=whichend`) to get the stored I-addresses. With `NOBERTREQUIRED`, `checkforopen` returns 1 immediately [bert.c:59–61], so access is unconditional. If the link was created with endsets, this call succeeds and returns the sporgls.

The sporgls carry: `sporgladdress` = homedoc ISA, `sporglorigin` + `sporglwidth` = the I-address range.

#### Step 3 — `linksporglset2specset` [sporgl.c:97–123]

For each sporgl with a non-zero `sporgladdress`:
```c
linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
```

A fresh `typevspec` is always allocated and appended to `*specsetptr`, regardless of what happens next. `linksporglset2specset` **always returns TRUE** [sporgl.c:122].

#### Step 4 — `sporglset2vspanset` [sporgl.c:141–176]

```c
(void) findorgl(taskptr, granf, homedoc, &orgl, type);  // ignored return
ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
```

`findorgl` with `NOBERTREQUIRED` bypasses BERT — the homedoc's granfilade node is fetched regardless of whether it is "open." But what matters here is that the homedoc's **POOM has no entries for these I-addresses** (they were deleted or never mapped).

#### Step 5 — `ispan2vspanset` → `permute` → `span2spanset` [orglinks.c:389–454]

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, I,
                              (typespan*)NULL, V, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) { ... }
if (!context) {
    return(targspansetptr);   // <-- returns unchanged, vspanset stays NULL
}
```

`retrieverestricted` [retrie.c:56–85] calls `retrieveinarea` which calls `findcbcinarea2d`. If the I-addresses are not present in the POOM, the traversal produces no context nodes. `context == NULL`. **`span2spanset` returns its `targspansetptr` argument unchanged**, meaning `specptr->vspanset` remains `NULL`.

#### Step 6 — The vspec is built anyway [sporgl.c:132–137]

```c
specptr->itemid = VSPECID;
specptr->next = NULL;
movetumbler(homedoc, &specptr->docisa);   // document address IS set
specptr->vspanset = NULL;                 // remains NULL
sporglset2vspanset(...);                  // finds nothing, changes nothing
```

The vspec has `docisa` set to the homedoc's ISA and `vspanset = NULL`.

#### Step 7 — Wire format [putfe.c:157–162, 124–141]

```c
case VSPECID:
    xuputc(VSPECFLAG, outfile);           // 'v'
    xuputc(WORDELIM, outfile);            // '~'
    puttumbler(outfile, &specptr->docisa); // the document address
    putitemset(taskptr, specptr->vspanset); // vspanset=NULL → count=0
    break;
```

`putitemset(NULL)` outputs count 0 (the `i = 0` loop body never fires [putfe.c:129–132]). The binary protocol sends:

```
FOLLOWLINK~  N~  v~ <homedoc_ISA>~  0~  [repeated N times]
```

Not a `?` (FAILFLAG). Not an empty specset (`N` ≥ 1). Each vspec advertises the document address but carries zero span entries.

---

### The `retrieveendsets` Path

`doretrieveendsets` [do1.c:369–374] → `retrieveendsetsfromspanf` [spanf1.c:190–235] queries the **spanfilade** for the from/to/three I-address ranges, then calls `linksporglset2specset` [sporgl.c:97] for each set. The same logic applies: sporgls are extracted, V-positions are sought in the homedoc's POOM, and if none are found, vspecs with empty vspansets are produced. `retrieveendsetsfromspanf` returns `FALSE` only if `specset2sporglset` fails — which in turn fails only if `findorgl` fails for the *input* link specset's document, not the endset homedoc.

---

### Definitive Answer

| Outcome | Observed? | Why |
|---------|-----------|-----|
| Empty VSpecSet (0 items) | **No** | `linksporglset2specset` always adds one vspec per sporgl |
| Error / FAILFLAG | **No** | `linksporglset2specset` always returns `TRUE`; `link2sporglset` succeeds when link exists |
| Partial result | **Yes** | N vspecs returned, each with `docisa` set to homedoc's ISA, `vspanset = NULL` (0 inner spans) |

The result is a **degenerate partial VSpecSet**: the homedoc document addresses are preserved from the link's stored sporgls [sporgl.c:134], but the V-positions within those documents are absent because `retrieverestricted` on the homedoc's POOM finds no mapping for those I-addresses [orglinks.c:435, 446–448]. The backend silently swallows the lookup failure — the `(void)` cast on `findorgl` [sporgl.c:152] and the `if(!context) return(targspansetptr)` guard [orglinks.c:447] both suppress any signal to the caller.
