## Question 17 [evidence]

> Since a link's residence (its home document's link-subspace POOM entry at `2.N`) is separate from its endset I-addresses, can a link be returned even when its home orgl is no longer in any open document's POOM, as long as its endset I-spans match?

## KB Synthesis

Yes. A link is discoverable via `find_links` independent of whether its home document's POOM entry at `2.N` exists.

The key is the three-layer architecture [SS-THREE-LAYER-MODEL]:

1. **I-space (link orgl)** — permanent, append-only. The link object at its I-address cannot be deleted by any operation.
2. **Spanfilade** — write-only [INV-SPANF-WRITE-ONLY]. Endset I-spans indexed at link creation time persist forever; no operation removes them.
3. **POOM (document V-stream at 2.N)** — mutable. `DELETEVSPAN(2.x)` removes this entry.

`find_links` operates exclusively on the spanfilade [SS-SPANF-OPERATIONS]: it converts the query specset to I-addresses and searches `findlinksfromtothreesp()`. It never consults the home document's POOM, never calls `findorgl`, and does not require any document to be open [SS-DOCUMENT-LIFECYCLE].

[EC-REVERSE-ORPHAN] confirms this directly:

> After `DELETEVSPAN(2.1)`: `find_links(source_specs)` → `[link_id]` (spanfilade intact), `follow_link(link_id, LINK_SOURCE)` → works (link orgl intact), `retrieve_vspanset(doc)` → no link span (POOM entry removed).

The POOM entry at `2.N` only governs whether the link appears in `retrieve_vspanset` output. Link discoverability depends solely on whether the endset I-spans intersect the query — i.e., the spanfilade state — which is permanent [INV-LINK-PERMANENCE].

---

## Code Exploration

I have everything I need. Here is the definitive answer.

---

## Can a link be returned when its home orgl is not in any open document's POOM?

**Yes.** The link retrieval path — both `dofollowlink` and `dofindlinksfromtothree` — never consults the link's residence entry (`2.N` in the home document's POOM), and the bert open-status of the home document is bypassed entirely via `NOBERTREQUIRED`.

---

### 1. `NOBERTREQUIRED` is a hard bypass, not a soft check

`bert.c:59-61`:
```c
int checkforopen(tumbler *tp, int type, int connection)
{
  if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
  }
  ...
}
```

The constant is defined at `backend/common.h:165`:
```c
#define NOBERTREQUIRED 0
```

Anything calling `findorgl(..., NOBERTREQUIRED)` gets an unconditional pass through `checkforopen`. No hash lookup, no table walk, no ownership test.

---

### 2. `dofollowlink` passes `NOBERTREQUIRED` to every call in its chain

`do1.c:223-232`:
```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, /* ECH 6-29 READBERT */ NOBERTREQUIRED));
}
```

The comment `/* ECH 6-29 READBERT */` is a tombstone: at some point the second call required `READBERT`, meaning the home document had to be open. That requirement was removed. Both calls now carry `NOBERTREQUIRED`.

---

### 3. The link's own orgl is the source, not the home document's POOM

`link2sporglset` in `sporgl.c:67-95` retrieves the link's endset data from the **link's own orgl**, not from the home document:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr,
                    INT whichend, int type)
{
  typeorgl orgl;
  ...
    if (!findorgl (taskptr, granf, linkisa, &orgl, type)){   /* [line 77] link's own ISA */
        return (FALSE);
    }
    tumblerclear (&zero);
    tumblerincrement (&zero, 0, whichend, &vspan.stream);    /* select FROM=1, TO=2, THREE=3 */
    tumblerincrement (&zero, 0, 1, &vspan.width);
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V,
                                     (typespan*)NULL, I,
                                     (typeisa*)NULL)) {      /* [line 83] NULL = no home-doc filter */
```

`findorgl` [line 77] is called on `linkisa` — the link's own tumbler — not on any home document. The `(typeisa*)NULL` at the end of `retrieverestricted` [line 83] means no home-document restriction is applied during the retrieval from the link's own enfilade. The residence entry at `2.N` in the home document is never touched.

---

### 4. The homedoc address comes from crums inside the link's own POOM

`contextintosporgl` in `sporgl.c:205-220`:

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  /* [line 209] */
    /* ^^^^^ zzz foo kluge 11/23/84 ^^^^^ */
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```

The home document address (`sporgladdress`) is read from `context2dinfo.homedoc`, which is a field stored inside the link's own 2D POOM crums — placed there by `insertendsetsinorgl` at link-creation time. It is a tumbler that was written once and never depends on the home document being open thereafter.

---

### 5. The I→V conversion in `linksporglset2specset` also uses `NOBERTREQUIRED`

When the sporgl's `sporgladdress` is non-zero, `linksporglset2specset` [sporgl.c:97-123] calls:

```c
linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
```

which calls `sporglset2vspanset` [sporgl.c:141-176]:

```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);   /* [line 152] */
```

The `type` here is still `NOBERTREQUIRED` propagated from `dofollowlink`. So even this step — translating the endset I-spans back to V-spans using the home document's POOM — bypasses bert. The home document's open status is irrelevant.

---

### 6. `dofindlinksfromtothree` — same story

`do1.c:348-353`:
```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
  bool findlinksfromtothreesp();
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
}
```

The spanfilade search (`sporglset2linksetinrange` in `sporgl.c:239-269`) scans for links whose endset I-spans match the query sporglset. The link's `2.N` residence in any home document is not involved. The only open-ness check is again `NOBERTREQUIRED` passed to `specset2sporglset`.

---

### 7. The one hard requirement: the orgl must exist in the granf

There is a distinction between **bert-open** (session-level access control, `addtoopen`/`checkforopen`) and **granf-present** (permanent storage, `fetchorglgr`). `NOBERTREQUIRED` eliminates the bert check entirely. But at `granf1.c:39`:

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

If the ISA has no entry in the granf at all — i.e., the link (or home document) was physically deleted from permanent storage — then `findorgl` returns FALSE and the retrieval fails. That is not a bert/open question; it is a granf existence question.

---

### Summary

| Mechanism | What it checks | Required for link retrieval? |
|---|---|---|
| `checkforopen` / bert | Session-level open status (READ/WRITE) | **No** — bypassed by `NOBERTREQUIRED` |
| Home document's POOM (`2.N` link-subspace entry) | Link ownership/residence | **Never consulted** during retrieval |
| `fetchorglgr` (granf) | Whether the ISA exists in permanent storage | **Yes** — must exist |
| Endset I-spans in link's own POOM | Where the link points | **Yes** — this is what is retrieved |

A link's residence at `2.N` in its home document records ownership at creation time only (`docreatelink` → `docopy` at `do1.c:212`). It is never read back during `dofollowlink` or `dofindlinksfromtothree`. The link's endset I-spans, stored in the link's own orgl in the granf, are completely independent of the home document's bert open-status and can be retrieved and returned as long as the link's granf entry survives.
