## Question 12 [gregory]

> How is a node's tumbler address assigned — is there a global allocation authority, a bootstrap configuration file, or does the first backend instance self-assign from a convention?

## KB Synthesis

Not fully answerable from the KB.

The KB extensively documents how addresses are allocated *within* an existing hierarchy: documents under accounts via `findisatoinsertnonmolecule` [SS-ADDRESS-ALLOC], links under documents via `findisatoinsertmolecule` [SS-ADDRESS-SPACE, Finding 0065], versions under documents [SS-VERSION-ADDRESS, Finding 0068]. The pattern is always the same: query the granfilade for the highest existing address below an upper bound, then increment.

But the KB stops at the account level. We know from the address structure that a docuverse address like `1.1.0.1.0.2` encodes `Node.0.User.0.Doc`, making `1.1` the node prefix [SS-TUMBLER, Finding 0001]. We know `enf.enf` is the single persistent file that stores all state [SS-UNIFIED-STORAGE, Finding 0059], and that initialization calls `createenf(GRAN)` and `createenf(SPAN)` [SS-DUAL-ENFILADE, Finding 0012]. We also know type registry entries live at bootstrap document `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024], implying some initial state exists.

What the KB does not contain is any finding about:
- How the node's own tumbler (`1.1`, `1.2`, etc.) is chosen at startup
- Whether there is a configuration file that sets the node address
- Whether the backend self-assigns from a convention (e.g., always `1.1` for a single-node deployment)
- Whether a global authority allocates node addresses before a backend can join

The exploration work captured findings about operation-level allocation mechanics but did not probe the bootstrap question — how the initial granfilade state with a node address comes to exist in the first place.

---

## Code Exploration

I now have a complete picture of the entire address-assignment machinery. Here is the answer.

---

## How a Node's Tumbler Address is Assigned in udanax-green

**Short answer: self-assignment from a hardcoded compile-time constant. There is no global allocation authority and no configuration file for this.**

---

### 1. The backend's identity address is a static literal

The backend's own tumbler address — its "account" — is declared as an initialized global variable in `be.c:37`:

```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

The `tumbler` struct (`common.h:59-65`) is:

```c
typedef struct structtumbler {
    humber xvartumbler;   /* = 0 */
    char varandnotfixed;  /* = 0 */
    char sign;            /* = 0  (positive) */
    short exp;            /* = 0  (normalized) */
    tdigit mantissa[16];  /* {1, 1, 0, 1, 0, 0, ...} */
} tumbler;
```

So `defaultaccount` decodes to tumbler `1.1.0.1`. This is a literal constant in source code, not read from anywhere at runtime.

It is installed into the active task context immediately after startup at `be.c:88`:

```c
movetumbler(&defaultaccount, &task.account);
```

Every subsequent request handler reads the account from `taskptr->account`, which now permanently equals `1.1.0.1`.

---

### 2. The `.backendrc` configuration file is irrelevant to tumbler addresses

`rcfile.c` defines every key the `.backendrc` file recognizes (`rcfile.c:19-29`):

```c
#define PORTMETANAME                 "port"
#define HOSTMETANAME                 "host"
#define BACKENDDIRECTORYMETANAME     "backenddir"
#define BACKENDFILEMETANAME          "backend"
#define ACCOUNTFILEMETANAME          "accountfile"
#define FRONTENDFILEMETANAME         "frontend"
#define BACKENDGLUEFILEMETANAME      "backglue"
#define FRONTENDGLUEFILEMETANAME     "frontglue"
#define ALLOCSIZENAME                "allocsize"
#define INCREMENTALALLOCSIZENAME     "incrementalallocsize"
```

There is no tumbler-address key. `processrcfile()` is called at `be.c:73` (and `xumain.c:39`) before `initmagicktricks`, but it cannot affect the node's identity — there is no field for it.

---

### 3. The interactive standalone build uses the zero address instead

The standalone `xumain.c` build calls `getaccount` at `xumain.c:49`:

```c
getaccount(&task, &task.account);
```

But `task.c:28-33` shows `getaccount` simply zeroes the tumbler:

```c
bool getaccount(typetask *taskptr, typeisa *accountptr)
{
  bool validaccount();
  tumblerclear(accountptr);
  return (TRUE);
```

The interactive-terminal version of the backend has account `0` (the zero tumbler). Only the FEBE backend (`be.c`) has the `1.1.0.1` default. There is no prompt, no file, no network query — `getaccount` was scaffolding that was commented out before shipping (`task.c:34-41`).

---

### 4. Child document addresses are allocated sequentially within the account's namespace

When `docreatenewdocument` is called (`do1.c:239`):

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

The call chain is:
- `createorglingranf` → `createorglgr` (`granf2.c:111-128`)
- `createorglgr` → `findisatoinsertgr` (`granf2.c:130-156`)
- `findisatoinsertgr` → `findisatoinsertnonmolecule` (`granf2.c:203-242`)

Inside `findisatoinsertnonmolecule`, because `supertype=ACCOUNT ≠ subtype=DOCUMENT`, the depth is 2 (`granf2.c:209`):

```c
depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
```

And the algorithm (`granf2.c:235-241`):

```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    /* Nothing under this hint - create first child as hintisa.0.1 */
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
} else {
    tumblertruncate(&lowerbound, hintlength + depth, isaptr);
    tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength?depth:0, 1, isaptr);
}
```

So under account `1.1.0.1`:
- First document: `1.1.0.1.0.1` (hintisa incremented at depth 2 → two zeros appended then increment)
- Second document: `1.1.0.1.0.2`
- etc.

This is purely local sequential allocation within the enfilade tree. No coordination with any external authority occurs.

---

### 5. NODE-level address creation

The `docreatenode_or_account` function (`do1.c:243-258`) uses `makehint(NODE, NODE, ...)`, which gives `depth=1` (same supertype and subtype). The caller passes a hint ISA, and the function finds the next sequential address one level below that hint. But this is for creating *entries* in the enfilade representing node or account objects — it does not change the backend's own identity, which is still the hardcoded `1.1.0.1`.

The hierarchy from `xanadu.h:140-143` is:

```c
#define NODE     1
#define ACCOUNT  2
#define DOCUMENT 3
#define ATOM     4
```

`1.1.0.1` sits at the ACCOUNT level of the hierarchy. An enclosing NODE would be at a shorter address like `1.1`.

---

### Summary

| Mechanism | What it does |
|-----------|-------------|
| `be.c:37` — `tumbler defaultaccount = {...} /* 1.1.0.1 */` | Hardcodes the backend's own identity as a compile-time constant |
| `be.c:88` — `movetumbler(&defaultaccount, &task.account)` | Installs it into every request's task context |
| `rcfile.c` / `.backendrc` | Configures ports, filenames, alloc sizes only — no address fields |
| `task.c:31` — `tumblerclear(accountptr)` | The standalone `xumain` build gets account `0` instead |
| `granf2.c:203-242` — `findisatoinsertnonmolecule` | Allocates sequential child addresses under the account prefix |

**The answer is: self-assignment from a hardcoded convention.** The FEBE backend unconditionally claims address `1.1.0.1` every time it starts. There is no allocation authority, no bootstrap file, no discovery protocol. The reference implementation implicitly assumes a single-backend deployment where address conflict cannot arise.
