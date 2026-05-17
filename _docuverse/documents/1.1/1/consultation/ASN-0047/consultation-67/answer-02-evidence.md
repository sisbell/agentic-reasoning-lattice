## Question 2 [evidence]

> When a document is created in udanax-green, does the implementation track the content and link sub-allocators as a single structure with two frontier states, or as two separately-managed allocator records?

## KB Synthesis

There is neither a single two-frontier structure nor two separately-managed allocator records. The implementation has **no allocator state at all** — both content (text) and link I-addresses are allocated via stateless query-and-increment on a single shared granfilade tree.

The mechanism [SS-ADDRESS-ALLOC] / [SS-ADDRESS-SPACE] (Finding 0077):

- Text I-addresses live under `docISA.3.x` in the granfilade tree; `findisatoinsertmolecule` bounds its search to that range.
- Link I-addresses live under `docISA.2.x`; the same function with a different upper-bound (`docISA.2.3`) handles link allocation [SS-ADDRESS-ALLOC] Finding 0065.
- Both paths call the same `findpreviousisagr` tree traversal, then `tumblerincrement(..., 0, 1, ...)` to derive the next address.

The key finding [SS-ADDRESS-SPACE] Finding 0077 states explicitly: "There is no single global `Σ.next` counter. Allocation is a family of independent functions partitioned by tumbler range…both query the same granfilade tree but search different subtrees."

The consequence is observable: `CREATELINK` advances the granfilade maximum into the `2.x` range, making subsequent text `INSERT` addresses non-contiguous with prior text — demonstrating they compete in the same tree with no isolation [EC-GRAN-BOTTOM-SINGLETON / Finding 0063].

**Summary**: One granfilade tree, no frontier pointers, two query bounds.

---

## Code Exploration

I now have enough from direct source reading to answer definitively.

---

## Answer: Two Separately-Managed Allocator Records

When a document is created in udanax-green, the content and link sub-allocators are **two independently-managed allocator records** — different struct types, initialized separately, stored separately, with entirely different internal layouts.

---

### The Two Global Allocators

Both are declared as opaque `INT *` pointers in `backend/xanadu.h:13-16`:

```c
#define typegranf INT *   /* temp -- INT for alignment */
extern typegranf granf;
#define typespanf INT *   /* temp -- INT for alignment */
extern typespanf spanf;
```

They are created independently at startup in `backend/entexit.c:44-45`:

```c
granf = (typegranf) createenf (GRAN);
spanf = (typespanf) createenf (SPAN);
```

Each is a separately heap-allocated enfilade — `GRAN` and `SPAN` are different enfilade type codes, producing distinct runtime structures with no shared state.

---

### Different Leaf Struct Types

Their bottom-of-tree leaf payloads are **completely different C structs**, defined in `backend/wisp.h`:

**Content allocator leaf** (`typegranorgl`, wisp.h:88-92):
```c
typedef struct structgranorgl {
    struct structcuc *orglptr;       /* pointer into a POOM (content tree) */
    typediskloafptr diskorglptr;     /* disk location */
    bool orglincore;                 /* in-core vs. on-disk flag */
} typegranorgl;
```

**Link/span allocator leaf** (`type2dbottomcruminfo`, wisp.h:107-109):
```c
typedef struct struct2dbottomcruminfo {
    tumbler homedoc;                 /* tumbler address of home document */
} type2dbottomcruminfo;
```

These two leaf types are unified into a discriminated union at `wisp.h:112-116`:

```c
typedef union unionbottomcruminfo {
    typegranbottomcruminfo granbottomcruminfo;   /* wraps typegranorgl */
    type2dbottomcruminfo   x2dbottomcruminfo;
} typebottomcruminfo;
```

The union exists for generic enfilade traversal — not because the two allocators share state. They occupy different branches of the union depending on which enfilade you're in.

---

### Document Creation Touches Only `granf`

`docreatenewdocument` in `backend/do1.c:234-241`:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    bool createorglingranf();
    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

Only `granf` is touched. `createorglingranf` allocates a new ORGL node (an empty POOM tree) into the granfilade, keyed by the document's ISA (tumbler address). At this moment `spanf` is not involved at all.

`docreatenewversion` (do1.c:260-292) follows the same pattern — `createorglingranf(taskptr, granf, &hint, newisaptr)` [do1.c:277] — again touching only the granfilade.

---

### The Spanfilade Is Invoked Later, Per-Operation

`spanf` enters the picture when content or link endpoints are actually inserted:

- **Content insert** (`docopyinternal`, do1.c:55-65): after copying content via `insertpm`, calls `insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)` [do1.c:62]
- **Link creation** (`domakelink`, do1.c:169-219): calls `createorglingranf(granf, ...)` [do1.c:182] for the link's ORGL, then `insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, NULL)` [do1.c:191] to register link endpoints in the spanfilade

The span types in `xanadu.h:36-39` distinguish content from link records within `spanf`:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4   /* document content */
```

---

### Summary

| Property | `granf` (content) | `spanf` (links/spans) |
|---|---|---|
| Declared | `xanadu.h:13-14` | `xanadu.h:15-16` |
| Initialized | `entexit.c:44` | `entexit.c:45` |
| Leaf struct | `typegranorgl` (wisp.h:88) | `type2dbottomcruminfo` (wisp.h:107) |
| Key field | `orglptr` → POOM tree | `homedoc` → tumbler address |
| Used at doc creation | Yes (`docreatenewdocument`, do1.c:240) | No |
| Used at content insert | Yes (findorgl, do1.c:55) | Yes (insertspanf, do1.c:62) |
| Used at link creation | Yes (createorglingranf, do1.c:182) | Yes (insertendsetsinspanf, do1.c:191) |

The implementation uses **two separately-managed allocator records** — different types, different enfilade instances, different frontier mechanics, initialized independently. There is no parent struct pairing them with dual frontier states; they are coupled only by the shared `tumbler` address space used to key lookups in both.
