## Question 13 [gregory]

> When udanax-green initializes via `entexit.c`, does it bind to exactly one node address, and if so, where is that node identity stored and how is it threaded through I-address allocation in `findisatoinsertmolecule`?

## KB Synthesis

## Node Binding at Initialization

The KB does not directly document `entexit.c` binding to a specific node address. What it does say is limited to one reference:

> `entexit.c:44-45` — initialization: `granf = createenf(GRAN); spanf = createenf(SPAN)` [SS-DUAL-ENFILADE, Finding 0012]

This is the entirety of what the KB records about `entexit.c`. Whether it also initializes a node identity global is not documented.

---

## What the KB Does Reveal About Node Structure

The address convention [SS-TUMBLER, Finding 0001] uses `.0.` as a field separator with the pattern `Node.0.User.0.Doc.0.Element`. All docuverse addresses in the KB use the `1.1.0.x` prefix, implying a single node `1.1`. Permascroll I-addresses use a different prefix (`2.1.0.x...`) [SS-ADDRESS-SPACE, Finding 0033], suggesting node `2` is the permascroll namespace.

Whether `1.1` is hardcoded in source, derived from the granfilade tree at startup, or set by an initialization routine outside `entexit.c` — the KB does not say.

---

## How Document Context Is Threaded Through `findisatoinsertmolecule`

The node identity is not passed as a separate parameter. It is embedded in the document ISA, which is carried through a hint structure:

1. The caller constructs `makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint)`, which copies `docisaptr` into `hintptr->hintisa` [SS-ADDRESS-SPACE, Finding 0065]
2. `findisatoinsertmolecule` computes: `tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound)` — this sets the search boundary to `docISA.element_field.(atomtype+1)`, scoping the allocation to the document's content subspace [SS-ADDRESS-ALLOC, Finding 0065]
3. `findpreviousisagr` traverses the granfilade tree within `[docISA.element_field.0, upperbound)` to find the current maximum I-address, then increments by 1 [SS-ADDRESS-SPACE, Finding 0061]

The node prefix (`1.1` or `2.1`) is implicit in `docisaptr` — the allocation is scoped by document, not by node. Since all documents under a single node share the same node prefix, the node identity propagates automatically through the ISA hierarchy. There is no separate node argument to `findisatoinsertmolecule`.

---

**Summary:** The KB cannot answer whether `entexit.c` binds to a node address — it only shows enfilade creation there. Node identity is implicit in all tumbler addresses (hierarchical prefix) and threads through `findisatoinsertmolecule` via the document ISA hint, not as an explicit parameter.

---

## Code Exploration

Now I have everything needed for a complete answer. Here is the full analysis with all code citations:

---

## Initialization, Node Identity, and I-Address Allocation in udanax-green

### 1. What `entexit.c` Actually Does

The file named `entexit.c` contains a single function, `initmagicktricks()` [entexit.c:19-47]. Despite the filename, it performs **no node address binding**. Its sole job is to initialize the enfilade storage infrastructure:

```c
// entexit.c:19-47
int initmagicktricks(void)
{
    varcrums = TRUE;
    numbytesinloaf = NUMBYTESINLOAF;
    ...
    initgrimreaper();
    initqueues();
    clear(&ZEROTUMBLERvar, sizeof(tumbler));
    if (initenffile()) {
        initkluge((typecuc**)&granf, (typecuc**)&spanf);  // load from disk
    } else {
        granf = (typegranf) createenf(GRAN);               // fresh enfilades
        spanf = (typespanf) createenf(SPAN);
    }
}
```

`initkluge()` is defined in `corediskin.c:18-41`. It reads the granfilade and spanfilade roots from fixed disk locations (`GRANFDISKLOCATION`, `SPANFDISKLOCATION`) into the global pointers `granf` and `spanf`. No tumbler is assigned here.

---

### 2. The Single Node Address and Where It Lives

The node identity is bound **one step later**, in `be.c`, which is the backend binary actually compiled and used by the test harness. After `initmagicktricks()` returns, this single line executes:

```c
// be.c:88
movetumbler(&defaultaccount, &task.account);
```

Where `defaultaccount` is defined at [be.c:37]:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

This is a tumbler with `exp=0, sign=0, mantissa=[1,1,0,1,0,0,...]` — the address **1.1.0.1**. This is the only node address ever set at startup.

**Storage location:** The account tumbler lives in `typetask.account` [common.h:102]:

```c
typedef struct structtask {
    FILE *inp, *outp, *errp;
    typetthingheader *tempspacehead;
    typetthingheader *tempspacetail;
    tumbler account;     /* ← the node identity */
    bool charinbuff;
    char charbuff;
} typetask;
```

`be.c` has a single global `typetask task` [be.c:41] and a matching global pointer `typetask *taskptrx` [be.c:36]. `isthisusersdocument()` [be.c:171-176] reads from `taskptrx->account` to enforce ownership:

```c
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

`tumbleraccounteq()` [tumble.c:38-70] checks whether `tp`'s mantissa prefix matches the account tumbler's non-zero digits — it treats two consecutive zeros as the account terminator, allowing document addresses like `1.1.0.1.0.1` to match account `1.1.0.1`.

Note: `socketbe.c:35` declares a different `defaultaccount = {0,0,0,0, 1,1,0,14,0}` (representing `1.1.0.14`) but it is **never assigned to any task or player** in the socket path — it is dead code in that file.

In `xumain.c` (the standalone binary), `getaccount()` [task.c:28-41] simply clears the account to zero:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
    tumblerclear(accountptr);
    return (TRUE);
}
```

The commented-out code below [task.c:35-40] shows the original intent to read the account from user input, but it was disabled. The test harness uses `be.c`, not `xumain.c`.

---

### 3. How the Node Address Threads Through I-Address Allocation

The account tumbler `1.1.0.1` is the root of the I-address hierarchy. It propagates as follows:

#### Step 1 — Document creation (`docreatenewdocument`, do1.c:234)

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

`makehint()` [do2.c:78-84] copies `taskptr->account` into `hint.hintisa`, with `supertype=ACCOUNT`, `subtype=DOCUMENT`. This hint then travels:

```
createorglingranf → createorglgr [granf2.c:111] → findisatoinsertgr [granf2.c:130]
```

#### Step 2 — Routing at `findisatoinsertgr` [granf2.c:130-156]

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    if (hintptr->subtype == ATOM) {
        findisatoinsertmolecule(fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule(fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

For **document creation** (`subtype=DOCUMENT ≠ ATOM`), `findisatoinsertnonmolecule` is called, **not** `findisatoinsertmolecule`. With `hintisa=1.1.0.1` and `depth=2` (supertype≠subtype), it allocates the first document as `1.1.0.1.0.1`.

#### Step 3 — When `findisatoinsertmolecule` is actually called

`findisatoinsertmolecule` [granf2.c:158-181] is called only for **ATOM subtypes** — text content (`TEXTATOM=1`) and link content (`LINKATOM=2`). The call chains are:

**Text insertion** (`doinsert`, do1.c:87):
```c
makehint(DOCUMENT, ATOM, TEXTATOM, docisaptr, &hint);  // hintisa = docisa (e.g. 1.1.0.1.0.1)
inserttextingranf → inserttextgr → findisatoinsertgr → findisatoinsertmolecule
```

**Link creation** (`docreatelink`, do1.c:195):
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);  // hintisa = docisa
createorglingranf → createorglgr → findisatoinsertgr → findisatoinsertmolecule
```

At this point, `hintisa` is the **document address** (e.g. `1.1.0.1.0.1`) — the account prefix `1.1.0.1` is already embedded in it. `findisatoinsertmolecule` does not see the raw account tumbler; it only uses the document ISA as its base.

#### Step 4 — Inside `findisatoinsertmolecule` [granf2.c:158-181]

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound;

    tumblerincrement(&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    clear(&lowerbound, sizeof(lowerbound));
    findpreviousisagr((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    if (tumblerlength(&hintptr->hintisa) == tumblerlength(&lowerbound)) {
        tumblerincrement(&lowerbound, 2, hintptr->atomtype, isaptr);
        tumblerincrement(isaptr, 1, 1, isaptr);
    } else if (hintptr->atomtype == TEXTATOM) {
        tumblerincrement(&lowerbound, 0, 1, isaptr);
    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement(&hintptr->hintisa, 2, 2, isaptr);
        if (tumblercmp(&lowerbound, isaptr) == LESS)
            tumblerincrement(isaptr, 1, 1, isaptr);
        else
            tumblerincrement(&lowerbound, 0, 1, isaptr);
    }
}
```

With `hintisa = docisa` (e.g. `1.1.0.1.0.1`):

- **TEXTATOM:** `upperbound = docisa + {2}` (i.e., `docisa.0.2`). Searches backward for the previous ISA under that bound. The new text address is placed after whatever was found.
- **LINKATOM:** `upperbound = docisa + {3}` (i.e., `docisa.0.3`). The first link address is `docisa.0.2`, then incremented past any existing links.

The account/node prefix `1.1.0.1` is baked into `docisa` and flows through the arithmetic invisibly.

---

### 4. The Complete Address Hierarchy

The single node address `1.1.0.1` set at [be.c:88] anchors the entire I-address tree:

| Level | Address | Allocated by |
|-------|---------|-------------|
| Node | `1` | Hardcoded in `defaultaccount` |
| Account | `1.1` | Hardcoded in `defaultaccount` |
| Sub-node | `1.1.0` | Hardcoded in `defaultaccount` |
| Account ISA | **`1.1.0.1`** | `defaultaccount` → `task.account` [be.c:88] |
| First document | `1.1.0.1.0.1` | `findisatoinsertnonmolecule` via `docreatenewdocument` |
| Text in doc | `1.1.0.1.0.1.0.N` | `findisatoinsertmolecule` (TEXTATOM) |
| Links in doc | `1.1.0.1.0.1.0.2`, `.0.3`, … | `findisatoinsertmolecule` (LINKATOM) |

### Summary

1. **`entexit.c` / `initmagicktricks()`** does **not** bind any node address. It only initializes enfilade disk infrastructure.

2. The single node address **`1.1.0.1`** is bound at [be.c:88] via `movetumbler(&defaultaccount, &task.account)`, immediately after `initmagicktricks()` returns.

3. The node identity lives in **`typetask.account`** [common.h:102], with the live global pointer at `taskptrx` [be.c:36].

4. `findisatoinsertmolecule` [granf2.c:158-181] is **only called for ATOM subtypes** (text and links). It never receives the raw account tumbler; by the time it is called, the account prefix is already embedded in the document's ISA via the `hint.hintisa` field. The account's `1.1.0.1` flows through: `task.account` → `hint.hintisa` (via `makehint` in `do1.c:117` or `207`) → document address → `hintisa` argument to `findisatoinsertmolecule` — where it appears as the prefix of the document address from which atom sub-addresses are derived.
