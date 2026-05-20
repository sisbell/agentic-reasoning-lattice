## Question 1 [evidence]

> Does the udanax-green retraction operation accept or record any attribution metadata about the retracting party, or does it only carry the address of the tuple being nullified?

## KB Synthesis

The KB does not contain any entry describing a retraction or nullification operation in udanax-green. The operations documented in the FEBE protocol include DELETEVSPAN, CREATENEWVERSION, INSERT, COPY/VCOPY, REARRANGE, FINDLINKSFROMTOTHREE, RETRIEVEENDSETS, FOLLOWLINK, and related queries — none of which are described as a "retraction."

The closest operations are DELETEVSPAN [ST-DELETE], which removes V-to-I mappings from a document's POOM without touching I-space or the spanfilade, and link-subspace deletion [SS-THREE-LAYER-MODEL], which severs a document's POOM reference to a link orgl while leaving the link in I-space and the spanfilade intact. Neither carries attribution metadata; both operate only on address/span arguments with no party identification.

The only reference to "Nullify" in the broader project context appears in memory about ASN-0086 (Typed Relations on Address Sets), which is spec-level work, not an implemented udanax-green operation documented in the KB.

This question is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything I need for a complete answer.

---

## Retraction (deletevspan): Attribution Analysis

**Short answer:** The retraction operation carries only the document address and the vspan (the span being nullified). No attribution metadata about the retracting party is accepted on the wire, stored in the data structure, or written to any audit log.

---

### 1. What the wire protocol accepts

`getdeletevspan` in both `get1.c:162` and `get1fe.c:138` reads exactly two values from the wire:

```c
// get1.c:162-170
bool getdeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    prompt(taskptr, "document=> ");
    if(!getisa (taskptr,docisaptr))
        return(FALSE);
    prompt(taskptr, "delete this part\n");
    if(!getspan (taskptr,vspanptr,VSPANID/*zzz*/))
        return(FALSE);
    return(TRUE);
}
```

A document ISA (tumbler) and a vspan. Nothing else. The protocol opcode `DELETEVSPAN` is written out by the frontend (`get1fe.c:142`), but only these two data fields follow it.

---

### 2. The do-layer: dodeletevspan

`do1.c:158`:

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

Two calls: `findorgl` (access check) and `deletevspanpm` (the structural edit). No attribution argument exists anywhere in this chain.

---

### 3. Access control: connection-based, not identity-based

`findorgl` in `granf1.c:17` calls `checkforopen(isaptr, type, user)`, where `user` is a **global integer connection index** (`bed.c:28`: `int user = 0;`).

`checkforopen` in `bert.c:52` consults the in-memory `berttable`. The `bertentry` struct (`bert.c:13–19`) is:

```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
```

The gate checks whether the issuing connection (`user`) has the document open for write (`WRITEBERT`). It also calls `isthisusersdocument(tp)` (`be.c:171`) which checks whether the document's tumbler prefix matches `taskptrx->account`. But these are **gatekeeping checks only** — no identity is recorded as a result of the delete.

---

### 4. The actual structural edit: deletevspanpm

`orglinks.c:145`:

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

After `deletend` cuts the node from the enfilade, `logbertmodified(docisaptr, user)` is called. That function (`bert.c:97`) does only this:

```c
int logbertmodified(tumbler *tp, int connection)
{
  // ...
  if (bert->connection == connection && tumblereq(tp, &bert->documentid)) {
      bert->modified = TRUE;
      return(0);
  }
}
```

It sets the `modified` flag on the bert table entry for the current connection. It records **no identity**. The account tumbler from `taskptr->account` is not passed here.

---

### 5. The account tumbler: present but not used in this path

`typetask` (`common.h:98–105`) carries a `tumbler account` field:

```c
typedef struct structtask {
    FILE *inp, *outp, *errp;
    typetthingheader *tempspacehead;
    typetthingheader *tempspacetail;
    tumbler account;
    bool charinbuff;
    char charbuff;
} typetask;
```

This account tumbler is used in two places unrelated to deletion:
- **Version creation**: `bert.c:274, 290, 296` pass `&taskptr->account` to `docreatenewversion`
- **Ownership gating**: `be.c:173` checks `tumbleraccounteq(tp, &taskptrx->account)` inside `isthisusersdocument`

It is **never passed to, stored by, or consulted within** `deletevspanpm`, `deletend`, or `logbertmodified`.

---

### Summary

The retraction operation accepts only two things from the caller: the address of the target document (ISA tumbler) and the virtual span to nullify. The only "identity" in play is the integer connection index (`user`), which serves as an access gate (must have WRITEBERT on the document) and is used to mark the bert entry as `modified = TRUE` — a dirty flag, not an audit record. No account tumbler, no retracting-party identifier, and no attribution metadata of any kind is accepted on the wire, threaded through the do-layer, or written to persistent storage as a result of the retraction.
