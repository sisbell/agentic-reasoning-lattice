## Question 20 [evidence]

> Does direct read of the link orgl require the home document to be open under BERT (PRE-DOCUMENT-OPEN), or is the granfilade-resident orgl readable by ISA without a document-open precondition?

## KB Synthesis

## Direct Link Orgl Read: No Document-Open Precondition Required

The KB gives a clear answer across several entries.

**FOLLOWLINK reads the link orgl by ISA, not via document handle.** [SS-FOLLOWLINK] (Finding 0048) describes the call chain: `link2sporglset()` calls `retrieverestricted()` on the granfilade directly by the link's ISA — "no POOM check occurs at this stage." The check that can fail is `findorgl()` returning FALSE if the link orgl does not exist at all, not a BERT/open-document check.

**The document-open precondition is POOM-specific, not granfilade-wide.** [SS-DOCUMENT-LIFECYCLE] (Finding 0027) draws the line explicitly: "Operations that work through I-address lookup (e.g., `find_links` via span-f) do not require the referenced document to be open. Operations that resolve V→I mappings within a specific document orgl (e.g., `retrieve_contents` via `findorgl`) do require it to be open. `follow_link` returns SpecSets containing document references **without requiring those documents to be open**."

**[PRE-FOLLOWLINK]** (Finding 0048) confirms: "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

**The split is architectural:** [SS-BERT] states BERT gates document content operations through `findorgl(..., READBERT/WRITEBERT)`. Link orgl reads use `retrieverestricted()` against the granfilade by ISA — the same I-address-lookup path used by span-f queries, which [SS-DOCUMENT-LIFECYCLE] explicitly exempts from the open-document requirement. [SS-BERT] also notes `NOBERTREQUIRED (0)` bypasses the table for internal operations.

**Summary:** The link orgl is readable by ISA without opening the home document under BERT. The document-open precondition applies only to POOM-level operations (V→I mapping resolution). FOLLOWLINK's second phase — converting endset I-addresses to V-spans — does require a document to be open, but that is the *queried* document passed as `homedoc`, not the link's home document [EC-GHOST-LINK].

---

## Code Exploration

I now have the complete picture. Here is the full answer with all code citations.

---

## Answer: The Link Orgl Is Readable WITHOUT a Document-Open Precondition

The call chain from `dofollowlink` down to `checkforopen` passes `NOBERTREQUIRED` at every step, completely bypassing BERT enforcement. Here is the complete trace.

---

### 1. FEBE Entry — `fns.c:114-127`

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;
  INT whichend;
  bool getfollowlink(), dofollowlink();

    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
      }else
        putrequestfailed (taskptr);
}
```

No BERT check here. Control passes directly to `dofollowlink`.

---

### 2. `dofollowlink` — `do1.c:223-231`

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,
                              /* ECH 6-29 READBERT */ NOBERTREQUIRED));
}
```

Both calls carry `NOBERTREQUIRED`. The comment `/* ECH 6-29 READBERT */` is a tombstone: `READBERT` was once used at the second call site, then deliberately changed to `NOBERTREQUIRED`.

---

### 3. `link2sporglset` — `sporgl.c:67-95`

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  typeorgl orgl;
  ...
  bool findorgl();

    if (!findorgl (taskptr, granf, linkisa, &orgl, type)){  /* type == NOBERTREQUIRED */
        return (FALSE);
    }
    ...
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        ...
        return (TRUE);
    } else {
        return (FALSE);
    }
}
```

`link2sporglset` calls `findorgl` with whatever `type` it received — `NOBERTREQUIRED`. The orgl is fetched from the granfilade to answer: "what does end `whichend` of this link point to?" — with no BERT gate.

---

### 4. `findorgl` — `granf1.c:17-41` — The Gate

```c
bool
findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)/*BERT*/
{
  typeorgl fetchorglgr();
  int temp;

    if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
#ifndef DISTRIBUTION
        if (!isxumain) {
            fprintf(stderr,"orgl for ");
            dumptumbler(isaptr);
            fprintf(stderr," not open in findorgl temp = %d\n",temp);
            return FALSE;
        }
#else
        if (!isxumain) {
            *orglptr = NULL;
            return FALSE;
        }
#endif
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

This is the only BERT enforcement point in the path. It calls `checkforopen(isaptr, type, user)`. When `type == NOBERTREQUIRED`, see what happens next.

---

### 5. `checkforopen` — `bert.c:52-61` — The Bypass

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  ...
  if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
  }
  ...
}
```

`NOBERTREQUIRED == 0` (`common.h:165`). When this is the `type`, `checkforopen` returns `1` immediately — no BERT table lookup occurs.

Back in `findorgl`, `temp = 1`, so `temp <= 0` is `FALSE`. The BERT enforcement block is skipped entirely. `fetchorglgr` is called and the link's orgl is returned.

---

### 6. Corroborating Evidence: `docreatelink` Changed from `WRITEBERT` to `NOBERTREQUIRED`

`do1.c:213`:
```c
  && findorgl (taskptr, granf, linkisaptr, &link, /*WRITEBERT ECH 7-1*/ NOBERTREQUIRED)
```

During link creation, opening the link's own orgl was changed from `WRITEBERT` to `NOBERTREQUIRED`. The comment records the original value and date. This is not an oversight — it is the same architectural decision applied consistently to link orgl access.

---

### 7. What Would Require BERT

For contrast: reading ordinary document content uses `READBERT` all the way down:

- `doretrievev` → `specset2ispanset(READBERT)` → `findorgl(READBERT)` — `do1.c:338-345`
- `doretrievedocvspan` → `findorgl(READBERT)` — `do1.c:312-319`
- `doretrievedocvspanset` → `findorgl(READBERT)` — `do1.c:322-335`

These are the document-content paths. They enforce BERT open state. The link orgl path does not.

---

## Conclusion

**Direct read of the link orgl does NOT require the home document to be open under BERT.** The granfilade-resident link orgl is readable by ISA address alone, with no PRE-DOCUMENT-OPEN precondition.

The mechanism: `dofollowlink` passes `NOBERTREQUIRED` to `link2sporglset`, which passes it to `findorgl`, which passes it to `checkforopen`. `checkforopen` treats `NOBERTREQUIRED` as an unconditional pass, returning `1` without consulting the BERT table. `fetchorglgr` is then called directly.

This is a deliberate architectural property of udanax-green: **links are globally addressable objects**, followable by any caller who holds the link's ISA tumbler. The home document's open/closed state under BERT is irrelevant to link traversal.
