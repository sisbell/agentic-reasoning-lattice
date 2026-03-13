## Question 11 [gregory]

> When a fresh backend instance starts for the first time, what initialization steps create the node's identity — is there a node address written into the granfilade or spanfilade root, or is the node address purely a configuration parameter external to the enfilade state?

## KB Synthesis

The KB does not contain sufficient detail to answer this definitively. Here is what the KB does and does not tell us:

**What the KB says about initialization:**

[SS-DUAL-ENFILADE, Finding 0012] — `entexit.c:44-45` shows the initialization sequence:
```c
granf = createenf(GRAN);
spanf = createenf(SPAN);
```

[SS-ENFILADE-TREE, Finding 0058] — `createenf(POOM)` produces a minimal height-1 tree with one zero-width bottom node (`infotype=GRANNULL` for GRAN). The fresh enfilade has no content.

[SS-UNIFIED-STORAGE, Finding 0059] — All persistent state lives in `enf.enf`. Fixed locations on disk: granf root at `GRANFDISKLOCATION`, spanf root at `SPANFDISKLOCATION`. On startup, `disk.c:364-382` opens or creates this file.

[EC-NO-STARTUP-VALIDATION, Finding 0059] — `initenffile()` opens the file and reads the block allocation table via `readallocinfo()`. No tree traversal or consistency check occurs. The KB doesn't describe what is written into a *newly created* `enf.enf` on first run.

**What the KB implies but does not confirm:**

The bootstrap document at `1.0.2.x` must exist for link type creation to work — [SS-LINK-ENDPOINT, Finding 0024] references JUMP (`1.0.2.2`), QUOTE (`1.0.2.3`), FOOTNOTE (`1.0.2.6`) as pre-existing entries. This implies some initial granfilade content is either pre-seeded at first run or shipped as a pre-built `enf.enf`.

All document addresses embed the node prefix (e.g., `1.1.0.1.0.1`) [SS-ADDRESS-SPACE, Finding 0021], and `makehint` uses `hintisa` as the parent for allocation — but where that initial hint address originates (config file, command-line argument, or a seeded granfilade entry) is not covered in the KB.

**The gap:** The KB does not trace the `xumain.c` startup path beyond the `strlen()` reference at line 143, does not describe `init.c`'s role in node address setup, and does not explain whether `1.1` (or the local node address) is stored as state inside the granfilade or supplied externally at daemon launch. The bootstrap document existence is asserted but its creation mechanism is not documented.

To answer your question, the KB evidence would need to include what `initenffile()` writes on first creation vs. re-open, and how `makehint`'s root `hintisa` gets populated on a clean node.

---

## Code Exploration

I now have everything needed for a definitive, fully-cited answer.

---

## Node Identity Initialization in udanax-green

### Short Answer

The node address is a **hardcoded compile-time constant** embedded in `be.c`. It is **not written into the granfilade or spanfilade root nodes**, and it is **not a configurable parameter** in any runtime config file. The enfilade roots are pure structural containers; identity lives only in a runtime task variable.

---

### The `main()` Entry Points

There are two entry points, and they handle node identity differently:

**`be.c` (FEBE server mode — the primary path used by the test harness):**

```c
// be.c:37
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */

// be.c:83–88
init (1);
inittask (&task);
initmagicktricks ();
movetumbler(&defaultaccount,&task.account);
```

The node address `1.1.0.1` is a C static aggregate initializer baked into the binary. `movetumbler` is a macro [`common.h:73`] that does a raw struct copy: `*B = *A`. The address lands in `task.account`, a runtime-only variable on the stack.

**`xumain.c` (standalone mode):**

```c
// xumain.c:49
getaccount(&task,&task.account);
```

`getaccount` in `task.c:28–41` simply calls `tumblerclear(accountptr)`, zeroing the entire tumbler struct. The standalone mode runs with address `0.0.0.0`.

---

### Tumbler Structure

```c
// common.h:53–65
#define NPLACES 16
typedef UINT tdigit;
typedef struct structtumbler {
    humber xvartumbler;       // unused ptr field
    char varandnotfixed;
    char sign;                // 1 = negative
    short exp;
    tdigit mantissa[NPLACES]; // hierarchical address digits
} tumbler;

#define ZEROTUMBLER  {0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
```

`defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}` maps to: `xvartumbler=0, varandnotfixed=0, sign=0, exp=0, mantissa={1,1,0,1,0,...}` — which the comment confirms decodes to tumbler address `1.1.0.1`.

---

### Enfilade Initialization: Fresh vs. Resume

`initmagicktricks()` in `entexit.c:19–47` dispatches:

```c
// entexit.c:41–46
if (initenffile()) {
    initkluge ((typecuc**)&granf, (typecuc**)&spanf);
} else {
    granf = (typegranf) createenf (GRAN);
    spanf = (typespanf) createenf (SPAN);
}
```

**`initenffile()` in `disk.c:340–383`** resolves which path to take:

```c
// disk.c:364–376
fd = open ("enf.enf", 2 /*rw*/,0);
if (fd == -1) {                       // No file → fresh start
    fd = creat ("enf.enf", 0666);
    initheader ();
    enffileread = FALSE;
    ret = FALSE;                       // returns FALSE → create empty enfilades
} else {
    ret = readallocinfo (fd);          // Existing file → resume path
    enffileread = TRUE;                // returns TRUE → initkluge reads from disk
}
```

In test mode (`--test-mode`), `initenffile()` unconditionally returns `FALSE` [`disk.c:360`], always creating a fresh empty state.

**Fresh start path:** `createenf(GRAN)` and `createenf(SPAN)` allocate empty root nodes with no content and no embedded address.

**Resume path:** `initkluge()` in `corediskin.c:18–41` reads the enfilade roots from fixed disk locations:

```c
// corediskin.c:25–26
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
// ...
// corediskin.c:33
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
```

These constants are:
```c
// coredisk.h:119–120
#define GRANFDISKLOCATION (NUMDISKLOAFSINHEADER+1)
#define SPANFDISKLOCATION (NUMDISKLOAFSINHEADER+2)
```

The enfilade roots at these locations are **structural nodes** — they contain enfilade topology (height, son counts, disk pointers) but **no node address or identity field**.

---

### What `.backendrc` Configures

`rcfile.c:18–93` shows `processrcfile()` parses these keys: `port`, `host`, `backenddir`, `backend`, `accountfile`, `frontend`, `backglue`, `frontglue`, `allocsize`, `incrementalallocsize`. There is **no `account`, `node`, or `address` key** — the rc file cannot configure node identity.

---

### Summary

| Question | Answer | Citation |
|---|---|---|
| Is there a node address in the granfilade root? | No — enfilade roots contain only structural topology | `corediskin.c:18–41` |
| Is there a node address in the spanfilade root? | No — same reason | `corediskin.c:33–38` |
| Where does node identity live? | `task.account` — a runtime stack variable | `be.c:88` |
| What is the address? | `1.1.0.1` (server mode) or `0.0.0.0` (standalone mode) | `be.c:37`, `task.c:31` |
| Is it configurable at runtime? | No — hardcoded in source; `.backendrc` has no account key | `rcfile.c:18–93` |
| Does fresh start write an address anywhere? | No — `createenf(GRAN/SPAN)` creates empty structural roots | `entexit.c:44–45` |

**The node address is purely a configuration parameter external to the enfilade state.** In FEBE server mode, it is a compile-time constant (`1.1.0.1`) copied into `task.account` after enfilade initialization. The granfilade and spanfilade roots store enfilade structure — they carry no node identity whatsoever.
