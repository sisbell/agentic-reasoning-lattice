## Question 13 [gregory]

> When `OPENDOCUMENT` is called, does it do anything beyond inserting a BERT entry — for instance, does it load or pin the document's POOM in the cache, or is POOM loading deferred until the first operation on that document?

## KB Synthesis

The KB does not contain a finding that directly answers this question. Here is what can be derived from what is recorded:

**What the KB does say:**

[SS-DOCUMENT-LIFECYCLE] (Finding 0027b) establishes that there is an explicit "open list" maintained by the backend, separate from the BERT table. `findorgl` checks whether a document orgl is in this open list — it is not just a BERT lookup. The backend log line `orgl for ... not open in findorgl temp = 0` confirms these are tracked separately.

[PRE-OPEN-DOC] (Finding 0014) describes `checkforopen` as the BERT-layer access control gate that returns access type, "needs opening", or denial. This is distinct from the open list check in `findorgl`.

[SS-CACHE-MECHANISM] (Finding 0059) describes the grim reaper cache: all crums (including POOM nodes) are in a shared in-memory circular list with age-based eviction. There is no "pinning" mechanism documented — crums are subject to eviction regardless of whether their document is open.

**What cannot be answered from the KB:**

The KB has no finding covering `doopen` (the backend handler for OPENDOCUMENT). Specifically, it does not record whether:
- OPENDOCUMENT eagerly reads the document's orgl/POOM into cache
- Or simply registers the document in the open list (BERT + orgl list), with actual POOM loading deferred to the first operation that calls `findorgl` / `retrieverestricted`

The cache architecture ([SS-CACHE-MECHANISM]) is consistent with deferred loading — crums are loaded on demand and evicted by age — but this is inference, not a finding. The question is not answerable from the KB as it stands.

---

## Code Exploration

I now have everything needed to answer definitively. Here is the full trace.

---

## `OPENDOCUMENT`: What It Does and What It Defers

### Call chain for OPEN

`bed.c:162` dispatches `(*requestfns[request])(taskptr)`. The `OPEN` opcode (35) is registered to `myopen` at `init.c:66`. That lands in:

```c
// fns.c:388–401
void myopen(typetask *taskptr)
{
  tumbler t, newt;
  int type, mode;
  bool getopen(), doopen();

    if (
        getopen(taskptr, &t, &type, &mode)
        &&  doopen(taskptr, &t, &newt, type, mode, user)) {
        putopen(taskptr, &newt);
    } else {
        putrequestfailed(taskptr);
    }
}
```

Three steps: parse the wire request, run `doopen`, send the response. The POOM is not touched in `getopen` or `putopen`; they only read/write the FEBE byte stream. The question is entirely about `doopen`.

---

### What `doopen` does — `bert.c:264–322`

```c
// bert.c:264
bool doopen(typetask *taskptr, tumbler *tp, tumbler *newtp, int type, int mode, int connection)
{
  INT openState;
  bool docreatenewversion();

   if (type == NOBERTREQUIRED) { return 1; }

   if (mode == BERTMODECOPY) {
    docreatenewversion(taskptr, tp, &taskptr->account, newtp);   // see below
    addtoopen(newtp, connection, TRUE, type);
    return 1;
   }

   openState = checkforopen(tp, type, connection);   // pure hash-table lookup

   if (openState == 0) {
    addtoopen(tp, connection, FALSE, type);
    tumblercopy(tp, newtp);
    return 1;
   }

   switch (mode) {
    case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    } else if (type != WRITEBERT && openState != WRITEBERT) {
        incrementopen(tp, connection);   // pure table increment
        tumblercopy(tp, newtp);
    } else {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);
    }
    return 1;
    case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) { return 0; }
    else if (openState == 0) {
        addtoopen(tp, connection, FALSE, type);
        tumblercopy(tp, newtp);
        return 1;
    } else {
        incrementopen(tp, connection);
        tumblercopy(tp, newtp);
        return 1;
    }
   }
}
```

`checkforopen` and `addtoopen`/`incrementopen` only manipulate the **in-memory `berttable`** — a hash table of `bertentry` structs keyed by tumbler. Those structs hold `{connection, documentid, created, modified, count, type}`. Nothing else. No enfilade traversal, no disk I/O.

---

### `addtoopen` — `bert.c:128–151`

```c
int addtoopen(tumbler *tp, int connection, int created, int type)
{
  bertentry *ptr = eallocwithtag(sizeof(bertentry), BERTTAG);
  tumblercopy(tp, &ptr->documentid);
  ptr->connection = connection;
  ptr->count = 1;
  ptr->created = created;
  ptr->modified = FALSE;
  ptr->type = type;
  // insert ptr into berttable[hash]
}
```

Allocates a small `bertentry`, populates it, chains it into the hash bucket. **No POOM, no disk.**

---

### Where POOM loading actually happens

Every document operation (insert, delete, rearrange, retrieve) reaches the POOM through `findorgl` in `granf1.c:17–41`:

```c
// granf1.c:17
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        ...return FALSE;  // access check
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);   // <-- POOM fetch
    return (*orglptr ? TRUE : FALSE);
}
```

`fetchorglgr` (in `granf2.c:22–81`) navigates the granfilade to find the crum for the given ISA. **If the POOM is not yet in memory** (`!orglincore`), it calls `inorgl` to load it from disk:

```c
// granf2.c:51–61
if (context->corecrum->cinfo.infotype == GRANORGL) {
    if (!context->corecrum->cinfo.granstuff.orglstuff.orglincore) {
        // disk block number must be valid
        inorgl (context->corecrum);   // <-- LAZY LOAD FROM DISK
    }
    ret = context->corecrum->cinfo.granstuff.orglstuff.orglptr;
}
```

`inorgl` is defined in `corediskin.c:171` and reads the enfilade tree for that document from the disk file. After loading, `orglincore` is set so subsequent calls skip the disk read.

`findorgl` is **never called** from `myopen`, `doopen`, or `addtoopen`. It is only called by the operational do-functions: `dorearrange` [do1.c:40], `docopy` [do1.c:55], `dodeletevspan` [do1.c:164], `doretrievedocvspan` [do1.c:318], `doretrievedocvspanset` [do1.c:327], `doretrievedocvspanfoo` [do1.c:307], and others in `do2.c`.

---

### Special case: `BERTMODECOPY` / write-conflict in `BERTMODECOPYIF`

When `OPENDOCUMENT` is called with mode `BERTMODECOPY` (or `BERTMODECOPYIF` against a write-locked document), `doopen` calls `docreatenewversion` [do1.c:260–299]. This function **does** touch the POOM of the **source** document: it calls `doretrievedocvspanfoo` → `findorgl` → `fetchorglgr` to get the source's V-span, then runs `docopyinternal` to copy content into the freshly-created empty POOM. However, this is the copy-on-open operation itself — the result is a brand-new document whose POOM is already in memory (`orglincore = TRUE`, `diskorglptr = DISKPTRNULL` [granf2.c:123–124]).

---

### Summary

| Mode | BERT table updated | POOM loaded |
|---|---|---|
| `BERTMODEONLY` (plain open) | Yes — `addtoopen` or `incrementopen` | **No — deferred to first operation** |
| `BERTMODECOPYIF` (no conflict) | Yes — `incrementopen` | **No — deferred** |
| `BERTMODECOPYIF` or `BERTMODECOPY` (write conflict / explicit copy) | Yes — `addtoopen` on new version | Yes — source POOM loaded to copy content into new version |

**For a standard open (`BERTMODEONLY` or `BERTMODECOPYIF` against an unlocked document), `OPENDOCUMENT` does exactly one thing beyond the wire protocol: it inserts a `bertentry` into the in-memory `berttable` hash table.** The document's POOM is not loaded, not pinned, not touched. POOM loading is deferred until the first actual document operation, which calls `findorgl` → `fetchorglgr`, which calls `inorgl` only if `orglincore` is false.
