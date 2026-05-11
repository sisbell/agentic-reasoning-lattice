## Question 1 [evidence]

> At system genesis, does udanax-green initialize the address space with seed addresses already present, or does it start from an empty registry and baptize the root via the normal mechanism?

## KB Synthesis

The KB does not contain a finding that directly documents the genesis sequence for udanax-green's address space. Here is what can be synthesized from what is present:

**What the KB does tell us:**

- At initialization, both enfilades are created empty: `granf = createenf(GRAN)` and `spanf = createenf(SPAN)`, each producing a minimal height-1 tree with a zero-width bottom node [SS-DUAL-ENFILADE, Finding 0012; SS-ENFILADE-TREE, Finding 0058].

- A **bootstrap document** at address `1.0.2.x` demonstrably exists at runtime and contains the link type registry (JUMP at `1.0.2.2`, QUOTE at `1.0.2.3`, FOOTNOTE at `1.0.2.6`, MARGIN at `1.0.2.6.2`). Link creation depends on this registry being present [SS-LINK-ENDPOINT, Finding 0024].

- The disk file `enf.enf` has **fixed locations** for the granfilade and spanfilade roots (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`), suggesting some pre-allocated structure in the on-disk layout [SS-UNIFIED-STORAGE, Finding 0059].

- Address allocation is stateless query-and-increment with a first-child convention (`parent.0.1`) when no children exist yet [SS-ADDRESS-ALLOC, Finding 0021].

**What the KB cannot answer:**

Whether the bootstrap document's type content is seeded by a one-time initialization routine (hardcoded inserts at first run), pre-baked into the `enf.enf` file distributed with the system, or created lazily on first link creation — none of the 78 findings cover this initialization path explicitly. The KB has no finding examining `entexit.c` initialization logic beyond the `createenf()` calls.

You would need a Finding targeting the startup path in `entexit.c` or `init.c` that traces whether the type registry addresses are written programmatically or assumed present.

---

## Code Exploration

I now have everything needed to give a complete and precise answer.

---

## Genesis Initialization in udanax-green: Empty Registry, No Baptism

The short answer: **udanax-green starts from a completely empty registry.** The session account is not "baptized" through the normal mechanism — it is simply hardcoded to the all-zeros tumbler and never inserted into the granfilade at all.

---

### The Startup Sequence (`xumain.c:30-64`)

```c
int main(void)
{
    typetask task;
    processrcfile();          // [xumain.c:39] — read .backendrc runtime config
    init(0);                  // [xumain.c:40] — wire FEBE dispatch table
    inittask(&task);          // [xumain.c:41] — attach stdio to task
    initmagicktricks();       // [xumain.c:47] — THE GENESIS FUNCTION
    getaccount(&task, &task.account);  // [xumain.c:49] — set account tumbler
    for (;;) { xanadu(&task); ... }   // event loop
}
```

---

### `initmagicktricks()` — The Fork (`entexit.c:19-47`)

```c
int initmagicktricks(void)
{
    initgrimreaper();
    initqueues();
    clear(&ZEROTUMBLERvar, sizeof(tumbler));    // [entexit.c:40]
    if (initenffile()) {
        initkluge((typecuc**)&granf, (typecuc**)&spanf);  // PATH A: restore
    } else {
        granf = (typegranf) createenf(GRAN);              // PATH B: fresh start
        spanf = (typespanf) createenf(SPAN);
    }
}
```

#### Path A — Restore from disk (`corediskin.c:18-41`)

If `enf.enf` already exists, `initkluge()` reads the GRAN and SPAN root enfilades from fixed disk locations (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`) via `inorgl()`, reconstructing whatever was previously saved. No seeds are added; prior state is restored wholesale.

#### Path B — Fresh start (`disk.c:340-383`, `credel.c:492-516`)

`initenffile()` returns `FALSE` when:
- Test mode is active (memory blocks all `NULL`), or
- `enf.enf` does not yet exist (it is `creat()`-ed fresh)

```c
// disk.c:340-383
bool initenffile(void) {
    if (test_mode) { initheader(); return FALSE; }  // FALSE = empty
    fd = open("enf.enf", 2, 0);
    if (fd == -1) {
        creat("enf.enf", 0666);
        initheader();
        return FALSE;  // [disk.c:373] fresh — no prior state
    }
    readallocinfo(fd);
    return TRUE;  // existing file
}
```

On a fresh start, `createenf(GRAN)` and `createenf(SPAN)` are called:

```c
// credel.c:492-516
typecuc *createenf(INT enftype)
{
    fullcrumptr = (typecuc *) createcrum(1, enftype);
    fullcrumptr->isapex = TRUE;
    fullcrumptr->isleftmost = TRUE;
    adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);
    if (enftype == GRAN) {
        ((typecbc *)ptr)->cinfo.infotype = GRANNULL;  // [credel.c:503] empty sentinel
    }
    ivemodified(ptr);
    return (fullcrumptr);
}
```

This creates:
- A height=1 apex node (the enfilade root, `isapex=TRUE`)
- A single height=0 child leaf marked **`GRANNULL`** — a structural empty sentinel, **not a real address entry**

**No tumbler addresses exist in the granfilade at this point.** The registry is truly empty.

---

### Account Initialization — Not a Registration (`task.c:28-41`)

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
    tumblerclear(accountptr);  // [task.c:31]
    return(TRUE);
}
```

`tumblerclear` is the macro `clear((tumblerptr), sizeof(tumbler))` (`common.h:71`). The `ZEROTUMBLER` is defined as `{0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}` (`common.h:67`).

The result: **`task.account` is the all-zeros tumbler.** This is assigned by a `memset`-equivalent. The account is never passed through `createorglingranf`, `insertseq`, or any granfilade insertion path. It has no presence in the registry.

There is no "baptism" call. The commented-out code nearby (`task.c:24` — `/*tumblerclear(&taskptr->account);*/` and `task.c:35-40` — a commented-out interactive `gettumbler` prompt) shows the code was refactored toward this minimal form, discarding any attempt at account lookup or registration.

---

### First Real Address Entry — On the First FEBE Operation

The very first address inserted into the granfilade is not a seed; it is the result of the first `CREATENEWDOCUMENT` request:

```c
// do1.c:234-241
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);  // hintisa = 0-tumbler
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

`makehint` (`do2.c:78-83`) sets `supertype=ACCOUNT`, `subtype=DOCUMENT`, `hintisa = {zero tumbler}`.

`createorglingranf` → `createorglgr` → `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203-242`):

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    depth = (hintptr->supertype == hintptr->subtype) ? 1 : 2;  // = 2 (ACCOUNT≠DOCUMENT)
    hintlength = tumblerlength(&hintptr->hintisa);               // = 1 for zero-tumbler

    tumblerincrement(&hintptr->hintisa, depth-1, 1, &upperbound);  // upperbound = 0.1
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    // Granfilade is empty: lowerbound stays zero
    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // isaptr = 0.0.1
    }
    ...
}
```

From `tumblerincrement` (`tumble.c:599-623`): when `aptr` is the zero tumbler:
```c
if (iszerotumbler(aptr)) {
    tumblerclear(cptr);
    cptr->exp = -rightshift;     // = -2
    cptr->mantissa[0] = bint;    // = 1
}
```

The result, `exp=-2, mantissa[0]=1`, represents the tumbler address `0.0.1` — the first document, nested two levels under the implicit zero account.

---

### Summary

| Question | Answer | Source |
|---|---|---|
| Are seed addresses pre-inserted at genesis? | **No** | `credel.c:503` — only a `GRANNULL` sentinel |
| Is the root "baptized" via the normal mechanism? | **No** | `task.c:31` — zero tumbler set by `memset`, never passed to `createorglingranf` |
| What is the session account at genesis? | All-zeros tumbler (never in the registry) | `task.c:31`, `common.h:67,71` |
| When does the first actual address appear in the registry? | On the first `CREATENEWDOCUMENT` FEBE call | `do1.c:239-240`, `granf2.c:235-237` |
| What is the first document address on a blank system? | `0.0.1` | `granf2.c:237`, `tumble.c:603-606` |
| Two-path genesis: fresh vs. restore? | Fresh: `createenf()` builds empty enfilades; Restore: `initkluge()` loads from fixed disk positions | `entexit.c:41-46`, `corediskin.c:18-41` |

The address space at genesis is structurally present (the enfilade tree exists with its root crum) but semantically empty. The zero tumbler is the implicit root of all addresses in the session, but it is a convention embedded in the task struct alone — not a registry entry. The first FEBE operation is what places the first atom of meaning into the granfilade.
