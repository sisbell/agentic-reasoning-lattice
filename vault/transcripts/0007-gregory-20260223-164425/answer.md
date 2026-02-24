## KB Synthesis

# Answer: Endset Boundaries Are Preserved

`link2sporglset` **preserves endset boundaries** — the three endsets (source, target, type) are **not** flattened into a single sporgl set. Each endset is maintained as a separate sporgl set throughout the system.

## Evidence from the Knowledge Base

### At Link Creation Time

From `[INT-SPORGL-LINK-INDEX]` Finding 0013:

> When a link is created, its endpoints (from, to, three) are converted to sporgls and indexed in the spanf enfilade. The function `insertendsetsinspanf()` receives sporglsets for **each endpoint type** and inserts them into the spanf index **tagged with the link's ISA and endpoint type** (`LINKFROMSPAN`, `LINKTOSPAN`).

**Code reference:** `do2.c:116-128` — `insertendsetsinspanf()` inserts from/to/three sporglsets **separately**.

The spanfilade maintains three distinct ORGLRANGE subspaces:
- `LINKFROMSPAN = 1` (source endset)
- `LINKTOSPAN = 2` (target endset)  
- `LINKTHREESPAN = 3` (type endset)

### At Link Retrieval Time

From `[SS-FOLLOWLINK]` Finding 0048:

> The call chain is: `link2sporglset()` extracts I-addresses from the link orgl **at the requested endset position (0.1, 0.2, or 0.3)** via `retrieverestricted()`.

The function takes a `whichend` parameter that selects **one specific endset** to extract, not all three.

**Code reference:** `sporgl.c:67-95` — `link2sporglset()` extracts I-addresses from link orgl at the **requested** endset position (selective, not flattened).

### At Query Time

From `[INT-SPORGL-LINK-INDEX]` Finding 0035:

> RETRIEVEENDSETS discovers links through the spanfilade by searching with ORGLRANGE dimension prefixes. The three link endset types are indexed as **separate ORGLRANGE subspaces**... each endset type is **searched independently** by restricting the ORGLRANGE dimension.

**Code reference:** `spanf1.c:190-235` — ORGLRANGE subspace definitions with **separate searches per endset type**.

## Conclusion

The system maintains endset boundaries at three levels:

1. **Storage layer** (link orgl): Three V-address positions (0.1, 0.2, 0.3) store the three endsets separately
2. **Index layer** (spanfilade): Three ORGLRANGE subspaces (1, 2, 3) index the three endsets with distinct type tags
3. **Retrieval layer** (`link2sporglset`): Extracts one endset at a time based on the `whichend` parameter

The design ensures that source, target, and type endpoints remain distinguishable throughout the system's operation. This separation is necessary because the three endsets serve different semantic roles and are queried independently (e.g., `find_links` by source only, or `follow_link` requesting just the target endset).

## Code Exploration

## Answer: Endset Boundaries ARE Preserved

`link2sporglset` **preserves endset boundaries**—it does NOT flatten all three endsets into a single sporgl set. Instead, it extracts **only one endset at a time**, specified by the `whichend` parameter.

---

### The Mechanism [sporgl.c:67-95]

The function signature clearly shows the selector:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, 
                    typesporglset *sporglsetptr, INT whichend, int type)
```

The extraction process [sporgl.c:77-94]:

1. **Find the link orgl** [line 77-79]:
   ```c
   if (!findorgl (taskptr, granf, linkisa, &orgl,type)){
       return (FALSE);
   }
   ```

2. **Create a vspan positioned at the specified endset** [lines 80-82]:
   ```c
   tumblerclear (&zero);
   tumblerincrement (&zero, 0, whichend, &vspan.stream);
   tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
   ```
   
   This constructs a V-span with:
   - `stream = [whichend]` (start position)
   - `width = [1]` (span width of 1)
   
   So if `whichend=1`, it retrieves position [1,2). If `whichend=2`, it retrieves [2,3). If `whichend=3`, it retrieves [3,4).

3. **Retrieve only that endset's contents** [lines 83-89]:
   ```c
   if (context = retrieverestricted((typecuc*)orgl, &vspan ,V, ...)) {
       for (c = context; c; c = c->nextcontext) {
           sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
           contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
           *sporglsetptr = (typesporglset)sporglptr;
           sporglsetptr = (typesporglset *)&sporglptr->next;
       }
   }
   ```

---

### The Endset Constants [xanadu.h:36-38]

The three endsets are explicitly defined:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

These map directly to:
- `whichend=1` → **source endset**
- `whichend=2` → **target endset**
- `whichend=3` → **type/third endset**

---

### Protocol Validation [get1.c:63-73]

The FEBE protocol requires the client to specify which endset:

```c
bool getfollowlink(typetask *taskptr, typeisa *linkisaptr, INT *whichendptr)
{
    prompt (taskptr, "enter link=> ");
    if (!getisa (taskptr, linkisaptr))
        return (FALSE);
    prompt (taskptr, "enter endset=> ");
    if (!(
       getnumber (taskptr, whichendptr)
    && (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)))
        return (FALSE);
    return (TRUE);
}
```

The client must explicitly choose 1, 2, or 3. The backend retrieves only that selected endset.

---

### Call Chain Evidence

**Following a link** [fns.c:119-123]:
```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
```

**Extracting the endset** [do1.c:223-231]:
```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, 
                  typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, 
                               sporglset, specsetptr, NOBERTREQUIRED));
}
```

The `whichend` parameter flows from protocol → dofollowlink → link2sporglset, selecting exactly one endset.

---

### Inverse Operation: Link Creation Preserves Boundaries

When creating links, the three endsets are kept separate [do1.c:214-219]:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
&& setlinkvsas (&fromvsa, &tovsa, &threevsa)
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, 
                        &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, 
                         fromsporglset, tosporglset, threesporglset)
```

Each endset is inserted separately into both the granfilade (at distinct vsa positions) and spanfilade (with distinct span type markers) [do2.c:116-128]:

```c
bool insertendsetsinspanf(..., typesporglset fromsporglset, 
                          typesporglset tosporglset, 
                          typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
      && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset, LINKTOSPAN)))
        return (FALSE);
    if (threesporglset) {
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
            return (FALSE);
    }
    return (TRUE);
}
```

---

### Conclusion

**The three endsets are architecturally separate throughout the entire system:**

1. **At rest**: Stored at distinct V-positions (1, 2, 3) in the link orgl
2. **In spanfilade**: Indexed under distinct span types (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN)
3. **During retrieval**: Extracted one at a time via the `whichend` selector
4. **In sporgl sets**: Each endset becomes a separate sporglset—never merged

The design ensures you can follow a link in a specific direction (source→target, target→source, or via type) by selecting the appropriate endset. The boundaries are never flattened.
