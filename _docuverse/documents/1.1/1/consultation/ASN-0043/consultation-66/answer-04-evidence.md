## Question 4 [evidence]

> Does udanax-green's allocator (e.g., findisatoinsertmolecule, docreatelink) track distinct "allocation events" as first-class objects separate from the sequence of inc steps that produce addresses, or is the event/chain distinction absent at the implementation level?

## KB Synthesis

The event/chain distinction is **absent at the implementation level**. The allocator has no first-class "allocation event" objects.

## What the allocator actually is

The allocator is a **stateless query-and-increment** over the granfilade tree [SS-ADDRESS-SPACE Finding 0061]:

```
next_iaddr(granf) = findpreviousisagr(granf, upper_bound) + 1
```

There is no session-local counter, no free list, no event log, and no cached "next available" pointer. Each allocation call independently queries the current tree maximum and increments from it [SS-ADDRESS-SPACE Finding 0077]. The result is a family of independent functions partitioned by tumbler range — content addresses, document addresses, and link addresses each query different subtrees of the same granfilade.

## What a "single allocation" produces

For text INSERT, `inserttextingranf` calls `tumblerincrement(&lsa, 0, N, &lsa)` once, producing N contiguous I-addresses as a single I-span [ST-INSERT Finding 0031]. The span (start + width) is the only thing recorded — not the operation that produced it, not how many "steps" were taken. The DOCISPAN entry in the spanfilade records this I-span → document mapping at I-span granularity [SS-DOCISPAN Finding 0047], one entry per contiguous range, not one per byte and not one per "event."

For `docreatelink`, `createorglingranf` calls `findisatoinsertnonmolecule` once and gets a single address [SS-ADDRESS-ALLOC Finding 0065]. No event record is created.

## The chain concept doesn't exist

Because allocation is query-and-increment over tree state, there are no "chains" in any tracked sense. Contiguity is an emergent property: sequential inserts produce contiguous addresses only because each call finds the prior maximum and increments by 1. If a CREATELINK intervenes, it advances the maximum, so the next text INSERT's I-addresses are non-contiguous with the previous text block — this is observable via `compare_versions` returning two span pairs instead of one [INT-LINK-INSERT Finding 0063]. But neither the contiguity nor its absence is tracked as an event; it is purely arithmetic over current tree state.

**Summary**: The allocator is `max + 1`, recorded as spans. Event objects and chain tracking do not exist.

---

## Code Exploration

I have a complete picture. Here is the full answer:

---

## Does udanax-green Track "Allocation Events" as First-Class Objects?

**No. The event/chain distinction is entirely absent at the implementation level.** There are no allocation-event objects. There are no chain objects. Address generation is a pure, ephemeral computation over tumblers. The only persistent artifact is the crum inserted into the granfilade tree.

---

### The Full Allocation Call Chain

#### 1. Entry: `docreatelink` / `doinsert` build a `typehint`

```c
/* do1.c:207 */
makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);

/* do1.c:117 */
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);
```

`makehint` (`do2.c:78-84`) just fills four fields into a stack-local struct and copies a tumbler:

```c
hintptr->supertype = typeabove;
hintptr->subtype   = typebelow;
hintptr->atomtype  = typeofatom;
movetumbler (isaptr, &hintptr->hintisa);
```

`typehint` (`xanadu.h:148-153`) is:

```c
typedef struct {
    INT supertype;
    INT subtype;
    INT atomtype;
    typeisa hintisa;
} typehint;
```

It has **no identity** (no ISA address), is **not heap-allocated**, is **not stored** anywhere after address computation completes, and is **not returned** to any caller. It is a transient parameter bundle — not an allocation-event object.

---

#### 2. Address Computation: `findisatoinsertmolecule`

For ATOM types (text, links), the path is:

```
docreatelink / doinsert
  → createorglingranf / inserttextingranf   [granf1.c:50, 44]
    → createorglgr / inserttextgr           [granf2.c:111, 83]
      → findisatoinsertgr                   [granf2.c:130]
        → findisatoinsertmolecule           [granf2.c:158]
```

The entire body of `findisatoinsertmolecule` (`granf2.c:158-181`):

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength (&hintptr->hintisa) == tumblerlength (&lowerbound)) {
        tumblerincrement (&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement (isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
            tumblerincrement (&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);
        else
            tumblerincrement (&lowerbound , 0, 1, isaptr);
    }
}
```

Every operation is tumbler arithmetic:
- **`tumblerincrement`** (`tumble.c:599-623`): shifts and adds an integer into one mantissa slot of a tumbler, then justifies. No allocation, no object creation.
- **`findpreviousisagr`** (`granf2.c:255-278`): recursively walks the granfilade tree, accumulating an offset tumbler via `tumbleradd`. Returns the highest existing address below `upperbound` — but the result is just a `tumbler` placed into `lowerbound` by value.

No allocation-event object is created. No chain object is created. The function writes a single tumbler value into `*isaptr` and returns.

---

#### 3. Insertion: `insertseq` takes address + content, nothing else

After `findisatoinsertgr` returns an address, `createorglgr` calls:

```c
/* granf2.c:125 */
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

And `inserttextgr` loops:

```c
/* granf2.c:99-100 */
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
tumblerincrement (&lsa, 0, textset->length, &lsa);
```

`insertseq` (`insert.c:17`) signature:

```c
int insertseq(typecuc *fullcrumptr, tumbler *address, typegranbottomcruminfo *info)
```

It takes the granfilade root, the computed address tumbler, and the content descriptor. It inserts a new crum into the enfilade tree at that address. **No event object is passed, created, or returned.** The running address in `inserttextgr` is `lsa` — a `tumbler` local to the stack frame, incremented in-place.

---

#### 4. The "chain" in `inserttextgr` is a loop variable, not an object

When inserting multi-segment text (`granf2.c:95-101`):

```c
for (; textset; textset = textset->next) {
    locinfo.infotype = GRANTEXT;
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring,
           locinfo.granstuff.textstuff.textlength);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);
}
```

`lsa` is a stack-local `tumbler`. The "chain" of inc steps is the loop iteration itself — each `tumblerincrement` overwrites `lsa` in place. There is no accumulation into a chain object, no log of the steps, no first-class representation of the allocation sequence. After the loop, only the resulting `ispanset` (origin + width as two tumblers) is returned to the caller.

---

### Summary

| Concept | In the implementation |
|---|---|
| Allocation event object | **Does not exist.** `typehint` is a transient stack parameter, not an event record. |
| Chain object | **Does not exist.** The sequence of `tumblerincrement` calls is the computation; `lsa` is a stack variable. |
| Persistent allocation record | The crum inserted into the granfilade tree (`insertseq`), indexed by ISA tumbler. That is the only trace. |
| Address computation mechanism | Pure arithmetic: scan tree for previous address (`findpreviousisagr`), increment tumbler to find next slot. |
| `typehint` lifetime | Created by `makehint` at caller, passed through two levels of wrappers, consumed inside `findisatoinsertmolecule`/`findisatoinsertnonmolecule`, then discarded. Never stored. Never given an ISA. |

The address and the content are fused into a single `insertseq` call. The address-finding computation that precedes it leaves no object behind. The event/chain distinction is absent at the implementation level.
