## Question 6 [evidence]

> Does udanax-green implement any form of link withdrawal or retraction, and if so does it remove entries from the link store or mark them in place?

## KB Synthesis

Udanax-green has **no link withdrawal or retraction mechanism**. The evidence is unambiguous across several KB entries:

**No DELETELINK operation exists.** [INV-LINK-PERMANENCE] explicitly states there is no DELETELINK opcode in the FEBE protocol. Once created, a link is permanent at the I-space and spanfilade layers.

**The link store is structurally write-only.** [INV-SPANF-WRITE-ONLY] documents that inspection of `spanf1.c` and `spanf2.c` reveals only insertion and query functions — no `deletespanf`, `removespanf`, or any removal mechanism exists. The set of spanfilade entries is monotonically non-decreasing.

**The three-layer model shows what IS and IS NOT mutable.** [SS-THREE-LAYER-MODEL] establishes:
- **I-space (link orgl):** Cannot be deleted — permanence axiom P0
- **Spanfilade (DOCISPAN entries):** Append-only — monotonicity P0′
- **POOM (document V-stream):** Mutable via `DELETEVSPAN`

The only operation that touches a link's presence is `DELETEVSPAN` on the 2.x subspace, which removes the link's POOM entry from one document. [EC-REVERSE-ORPHAN] characterizes the result: the link orgl persists at its I-address, the spanfilade entries remain intact, `find_links` still discovers the link, and `follow_link` still works. This is not retraction — it is merely severing one document's V-stream reference while leaving the link fully intact in the permanent layers.

In summary: **no retraction exists at any layer**. The nearest approximation (POOM removal via DELETEVSPAN) does not touch the link store at all.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer:

---

## Link Withdrawal in udanax-green: Does Not Exist at the Protocol Level; Partial POOM Removal Only

### Short Answer

udanax-green implements **no link withdrawal or retraction operation**. There is no `DELETELINK` protocol command, and no mechanism exists to delete or mark a link in the link store (spanfilade). The link's I-space record is permanent and append-only. The closest thing to "withdrawal" is a side-effect of calling `DELETEVSPAN` on the link's V-position in its home document's POOM — but that only removes one of three storage layers and leaves the link fully accessible.

---

### Evidence: No Protocol Operation for Link Deletion

`backend/requests.h` is the canonical list of all FEBE protocol operations:

```c
#define INSERT                     0
#define RETRIEVEDOCVSPANSET        1
#define COPY                       2
#define REARRANGE                  3
#define RETRIEVEV                  5
#define CREATENEWDOCUMENT         11
#define DELETEVSPAN               12
#define CREATENEWVERSION          13
#define CREATELINK                27
#define FOLLOWLINK                18
#define FINDLINKSFROMTOTHREE      30
#define FINDNUMOFLINKSFROMTOTHREE 29
#define FINDNEXTNLINKSFROMTOTHREE 31
#define RETRIEVEENDSETS           28
// ...
```
[`requests.h:21-46`]

There is no `DELETELINK`, `WITHDRAWLINK`, `RETRACTLINK`, or any equivalent. The dispatch table in `init.c` confirms the complete registered operation set — `createlink` is registered at line 60, but no link removal operation is registered anywhere [`init.c:45-69`].

A broad grep over all `.c` and `.h` files for `deletelink`, `withdrawlink`, `retractlink`, `removelink`, and `link.*delete` returns **zero matches**.

---

### How Links Are Created and Stored: Three Independent Layers

`docreatelink` in `do1.c:195-221` creates entries in **three separate storage layers**:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)   // Layer 1: I-space
      && tumbler2spanset (taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
      && docopy (taskptr, docisaptr, &linkvsa, ispanset)          // Layer 3: POOM
      && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset (...)
      && setlinkvsas (...)
      && insertendsetsinorgl (...)                                  // Layer 1: I-space endpoint data
      && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)    // Layer 2: Spanfilade
    );
}
```
[`do1.c:195-221`]

#### Layer 1: I-space (link orgl, in granf)

`createorglingranf` allocates a permanent orgl for the link at a new I-address. The link's FROM/TO/THREE endsets are written into this orgl via `insertendsetsinorgl`. **No deletion function for orgl entries exists.** The granf enfilade supports `insertnd` (insertion) and `deletend` (removal from POOM dimension), but `deletend` operates on V→I mappings in a document's POOM, not on the global I-space allocation. Link orgl nodes are permanent once allocated.

#### Layer 2: Spanfilade (spanf)

`insertendsetsinspanf` calls `insertspanf` three times — once each for `LINKFROMSPAN`, `LINKTOSPAN`, and `LINKTHREESPAN` [`do2.c:116-128`]:

```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr,
    typeisa *linkisaptr, typesporglset fromsporglset,
    typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
      && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
            return (FALSE);
    if (threesporglset) {
        if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
            return (FALSE);
        }
    }
    return(TRUE);
}
```
[`do2.c:116-128`]

Examination of the complete `spanf1.c` and `spanf2.c` sources reveals the following functions exist:

- `insertspanf` — adds spanfilade entries ✓
- `findlinksfromtothreesp` — searches for links ✓
- `retrieveendsetsfromspanf` — retrieves endsets ✓
- `finddocscontainingsp` — finds documents containing I-addresses ✓
- `findnumoflinksfromtothreesp` — counts links ✓

And these **do not exist anywhere in the codebase**:
- `deletespanf` ✗
- `removespanf` ✗
- `withdrawspanf` ✗

The spanfilade is **write-only with respect to link entries**. [`spanf1.c` and `spanf2.c` in full]

#### Layer 3: POOM (document V-stream, in granf)

`docopy` (called during link creation) inserts a V→I mapping for the link's I-address into the home document's POOM at a V-position in the link subspace (2.x). This is the only mutable layer. The `DELETEVSPAN` operation can target this layer.

---

### The Only Partial Mechanism: DELETEVSPAN on the Link Subspace

`dodeletevspan` in `do1.c:158-167` calls `deletevspanpm` from `orglinks.c`:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```
[`do1.c:158-167`]

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr,
                   typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```
[`orglinks.c:145-152`, per Finding 0057]

`deletend` removes crums from the document's POOM in the V-dimension. If you call `DELETEVSPAN` targeting V-position 2.1 (the link's slot in the home document), it removes the POOM entry for that link. **It makes no call to remove anything from the spanfilade or from I-space.** The link orgl at its I-address is untouched.

After such a deletion (confirmed by Finding 0040):
- `retrieve_vspanset` on the home document no longer shows the link's 2.x slot
- `find_links()` **still finds the link** (spanfilade entries persist)
- `follow_link(link_id)` **still works** (link orgl in I-space persists)

---

### Summary of What Exists vs. What Is Missing

| Operation | Layer 1: I-space (link orgl) | Layer 2: Spanfilade | Layer 3: POOM |
|---|---|---|---|
| `CREATELINK` | Created permanently | Entries inserted | V-slot inserted at 2.x |
| `DELETEVSPAN(2.x)` | No effect | No effect | V-slot removed |
| Any retraction/withdrawal | **Not implemented** | **Not implemented** | Via DELETEVSPAN only |
| Mark-in-place mechanism | **Does not exist** | **Does not exist** | N/A |

### Conclusion

udanax-green implements **no link withdrawal or retraction** as a first-class operation. The FEBE protocol has no `DELETELINK` command (`requests.h`), `fns.c` dispatches no such handler, `init.c` registers none, and no `deletespanf`/`deletespanf`-equivalent function exists anywhere in `spanf1.c` or `spanf2.c`. The spanfilade — the structure that indexes link endpoints for `find_links` queries — is strictly append-only.

Links are not marked in place as "deleted" or "withdrawn" either: there is no status flag in the link orgl or spanfilade entry structure (`xanadu.h`) for this purpose.

The only mechanism that partially resembles withdrawal is using `DELETEVSPAN` to remove the link's V-position (2.x) from its home document's POOM. This hides the link from `retrieve_vspanset` but leaves the link orgl and all spanfilade entries intact, so the link remains discoverable via `find_links` and followable via `follow_link`. The three-layer architecture (I-space permanent / spanfilade append-only / POOM mutable) means even this partial removal does not constitute true retraction.
