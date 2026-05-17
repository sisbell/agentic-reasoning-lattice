## Question 8 [evidence]

> Does udanax-green have any state representation (granfilade record, ISA reservation, or similar) for tumblers that are structurally valid but have never been instantiated by `docreatenewdocument`, `docreatenewversion`, or related procedures?

## KB Synthesis

No. Udanax-green has no state representation for structurally valid but uninstantiated tumblers.

The granfilade is strictly **populated on creation, never pre-allocated**. The allocation mechanism is purely reactive: `findisatoinsertnonmolecule` and `findisatoinsertmolecule` query the granfilade tree via `findpreviousisagr` to find the current maximum address in the target range, then derive the next address by incrementing [SS-ADDRESS-SPACE Finding 0021, Finding 0061]. There is no cached counter, no reservation record, no "claimed-but-pending" ISA entry.

Concretely:
- A tumbler like `1.1.0.1.0.5` is only present in the granfilade if `docreatenewdocument` (or equivalent) was actually called and produced that address [SS-ADDRESS-SPACE Finding 0077].
- The address space below the current maximum is an empty range in the tree — absent, not represented as "reserved" or "available" [INV-NO-IADDR-REUSE].
- `findpreviousisagr` traverses the actual tree; if a subtree is empty it returns nothing and the allocator falls back to the first-child convention (`parent.0.1`) [SS-ADDRESS-ALLOC Finding 0021].

The corollary: every tumbler in the granfilade corresponds to an entity that was explicitly instantiated. The gap between existing addresses and the theoretical upper bound of the tumbler space is simply absent from all enfilade state.

---

## Code Exploration

---

## Does udanax-green track structurally valid but uninstantiated tumblers?

**No.** The system operates under a strict instantiation model: a tumbler exists in state if and only if an actual ORGL (organizational link) record has been written into the granfilade for it. There is no reservation mechanism, no high-water mark, no "allocated but empty" address space tracking anywhere in the codebase.

Here is the full evidence, file by file.

---

### 1. The granfilade record structure carries only content

The `bertentry` struct in `bert.c:13-19`:

```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
```

The fields are: connection ID, document tumbler, boolean `created`, boolean `modified`, access type (`READBERT`/`WRITEBERT`), and reference count. There is **no `reserved` field, no `allocated` field, no "valid but empty" flag**. The BERT table is populated only when `addtoopen()` is called, which happens only when an actual ORGL exists.

---

### 2. ISA allocation is on-demand and leaves no gap

`findisatoinsertnonmolecule()` in `granf2.c:203-242` is the ISA allocator for DOCUMENT, ACCOUNT, and NODE types. It works by:

1. Computing an upper bound from the hint (`granf2.c:213`)
2. Walking the granfilade tree backwards to find the **last actually-instantiated tumbler** under the hint — `findpreviousisagr()` at `granf2.c:217`
3. Incrementing that by 1 to get the next address (`granf2.c:237-240`)

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);  // first child
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

No range is pre-reserved. The allocator finds the high-water mark from the tree itself at call time — there is no persistent counter. Tumblers are assigned the moment content is written.

`findpreviousisagr()` (`granf2.c:255-278`) confirms this: it walks the enfilade tree to find the **last crum with actual content**, not a stored "last allocated" counter. There is no global next-ISA state anywhere.

---

### 3. `docreatenewdocument` and `docreatenewversion` instantiate immediately; no pre-reservation

`docreatenewdocument()` at `do1.c:234-241`:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

One call: `createorglingranf()`. This writes an actual ORGL node into the granfilade. Nothing else. No reservation of a range of child tumblers or future versions.

`docreatenewversion()` at `do1.c:260-299`:

```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) return FALSE;
// ...
addtoopen(newisaptr, user, TRUE, WRITEBERT);   // do1.c:292
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);   // do1.c:293
logbertmodified(newisaptr, user);   // do1.c:295
doclose(taskptr, newisaptr, user);  // do1.c:296
```

Same pattern: ORGL is created, content is immediately copied in, and the version is marked modified and closed. No version slots are pre-allocated.

---

### 4. `isaexistsgr` confirms existence means content in the tree

`isaexistsgr()` at `granf2.c:244-253`:

```c
bool isaexistsgr(typecuc *crumptr, typeisa *isaptr)
{
  typecontext *context, *retrieve();
  bool ret;
    context = retrieve(crumptr, isaptr, WIDTH);
    ret = tumblereq((tumbler*)&context->totaloffset, isaptr);
    contextfree(context);
    return (ret);
}
```

This retrieves the context at that ISA address in the tree and checks whether the tree's accumulated offset **exactly matches** the requested ISA. If no crum was ever inserted there, the tree returns a neighboring offset and the comparison fails. There is no way for this to return true for an uninstantiated tumbler.

---

### 5. `acceptablevsa` accepts all tumblers unconditionally — no address-space validation

`do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

This is the VSA validity check called during copy operations. It accepts every tumbler as an acceptable virtual stream address regardless of whether it has ever been instantiated. This is not a reservation mechanism — it is the absence of any validation at all. There is no address-space model against which tumblers are validated.

---

### 6. Unmodified newly-created versions are immediately deleted on close

`removefromopen()` at `bert.c:154-193`:

```c
status = bert->created && !bert->modified;   // bert.c:173
if (status) {
    deleteversion(tp);   // bert.c:175
}
```

Even the act of creating a document via `docreatenewversion()` does not permanently instantiate a tumbler: if no content is written (`!bert->modified`), `removefromopen()` calls `deleteversion()` and removes the ORGL from the granfilade. The tumbler reverts to being entirely absent from system state. The `logbertmodified()` call in `docreatenewversion()` (`do1.c:295`) exists precisely to prevent this deletion for legitimate new versions.

---

### 7. `checkforopen` treats unknown tumblers as "needs open" or "not yours"

`checkforopen()` at `bert.c:52-87`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;  // open required
} else {
    return -1; // new version should be made (or denied)
}
```

For a tumbler with no BERT entry: returns `0` (open required, document exists but not currently open) if it's the user's document, `-1` otherwise. The check for ownership (`isthisusersdocument()`) consults the granfilade — not any reservation table. A tumbler that has never been instantiated in the granfilade is indistinguishable here from one that simply isn't open; the caller's subsequent `findorgl()` call will fail and the operation will be rejected.

---

### Summary

| Question | Answer | Evidence |
|----------|--------|----------|
| Does the granfilade record "reserved but empty" slots? | No | `bertentry` struct has no such field (`bert.c:13-19`) |
| Does ISA allocation pre-reserve ranges? | No | `findisatoinsertnonmolecule` finds last actual crum, increments by 1 (`granf2.c:235-241`) |
| Is there a global "next available ISA" counter? | No | High-water mark is derived from tree walk at call time (`granf2.c:255-278`) |
| Does `docreatenewversion` pre-allocate version slots? | No | It creates one ORGL and immediately copies content in (`do1.c:277-296`) |
| Is there any "valid but uninstantiated" address space concept? | No | `isaexistsgr` requires exact tree match (`granf2.c:250`); `acceptablevsa` accepts everything without validation (`do2.c:112`) |
| Can a tumbler survive creation without content? | No | Created-but-unmodified versions are deleted on close (`bert.c:173-175`) |

**A tumbler in udanax-green is an address without a receptacle until the moment `createorglingranf()` writes an ORGL for it into the granfilade tree.** Before that moment, no system structure acknowledges its potential existence.
