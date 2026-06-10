## Question 7 [evidence]

> Does udanax-green's persistent state record wall-clock timestamps anywhere (e.g., at document, version, or link creation), or is all ordering purely structural (chain indices, tumbler order)?

## KB Synthesis

Based on a thorough search of the KB, **udanax-green records no wall-clock timestamps anywhere in its persistent state**. All ordering is purely structural.

## Evidence

**Disk block headers have no timestamp field.** The `typediskloafhedr` structure is [SS-UNIFIED-STORAGE]:
```c
typedef struct structdiskloafhedr {
    INT sizeofthisloaf;
    SINT isapex;
    SINT height;
    SINT denftype;
    SINT numberofcrums;
    SINT refcount;
    SINT allignmentdummy;
} typediskloafhedr;
```
No creation time, no modification time.

**Content atoms have no timestamp.** `typegrantext` [SS-CONTENT-IDENTITY, Finding 0034] is just `{ char textstring[950], unsigned textlength }`.

**BERT entries have no timestamp.** [SS-BERT]: `{ connection, document, type: {READ|WRITE}, count }`.

**The `age` field is not a wall-clock value.** [SS-CACHE-MECHANISM] describes `age` as an in-memory counter used by the grim reaper for cache eviction policy — it is not persisted to disk and carries no calendar meaning.

## Ordering is Entirely Structural

The KB documents three purely structural ordering mechanisms:

1. **I-address order reflects insertion chronology** [INV-MONOTONIC, SS-ADDRESS-SPACE]: `findpreviousisagr` finds the highest existing I-address and increments by 1. Later inserts always get higher I-addresses. This is a monotonic structural counter derived from the current granfilade tree state — "The allocation is purely derived from current tree state — there is no cached 'next available' pointer" [Finding 0061].

2. **Version lineage is encoded in address structure** [SS-VERSION-ADDRESS]: `1.1.0.1.0.1.1` is structurally a child of `1.1.0.1.0.1`. Version ordering is readable from address containment alone, with no timestamp needed.

3. **Sequential allocation order within a namespace** [SS-ADDRESS-ALLOC]: Documents under an account get `.0.1`, `.0.2`, `.0.3`, etc. by query-and-increment. The allocation sequence implies creation order, but only ordinally — not with any calendar anchor.

## Conclusion

There is no way to recover an absolute creation time for any document, version, link, or content atom from the persistent state. The system is entirely structural: what you can know is *which came first* (lower I-address, lower tumbler suffix) but not *when*.

---

## Code Exploration

I now have everything I need for a complete answer.

---

## Answer: No Wall-Clock Timestamps Anywhere in Persistent State

All ordering in udanax-green is purely structural. Here is the full evidence.

---

### The Three `time()` Calls — All Ephemeral

**`init.c:37-41`**
```c
long start_time;
struct tm *tm;

start_time = time((long *) 0);
tm = gmtime(&start_time);
```
`tm` is computed and never used — the result is discarded. This is dead code. The function continues at `init.c:42` setting up `requestfns[]` without touching `tm`.

**`be.c:61-63`**
```c
clock = time (0);
local = localtime (&clock);
sprintf(buf,"ln%d.%d.%d:%d",local->tm_mon+1,local->tm_mday,local->tm_hour,local->tm_min);
```
Used only to generate a log filename. The result is never written to any persistent data structure.

**`bed.c:79-84`**
```c
clock = time(0);
local = localtime(&clock);
sprintf (buf, "ln%d.%d.%d:%d", local->tm_mon+1, local->tm_mday, local->tm_hour, local->tm_min);
interfaceinput=fopen(buf, "w");
```
Same pattern: log filename construction only.

---

### No Timestamp Fields in Any Struct

I read every data structure header. None contain a wall-clock field:

**`common.h:59-65`** — `tumbler` struct: `humber xvartumbler`, `char varandnotfixed`, `char sign`, `short exp`, `tdigit mantissa[NPLACES]`. No timestamps.

**`xanadu.h:52-121`** — All protocol-layer types (`typetext`, `typespan`/`typevspan`/`typeispan`, `typevspec`, `typeaddress`/`typelink`, `typesporgl`) contain only tumblers (`stream`, `width`, `address`) and data payloads. No timestamps.

**`enf.h:31-50`** — `typecorecrumhedr` (the in-memory enfilade node):
```c
struct structcorecrumhedr {
    bool isapex BIT;
    SINT height;
    SINT cenftype;
    bool modified BIT;
    bool isleftmost BIT;
    struct structcorecrumhedr *nextcrum, *prevcrum;
    unsigned char age;        // cache eviction byte, NOT a timestamp
    struct structcorecrumhedr *leftbroorfather;
    struct structcorecrumhedr *rightbro;
    typewid cwid;
    typedsp cdsp;
};
```
The `age` field (`enf.h:41`) looks suspicious but is defined in `reap.h:11-14` as a 3-value cache management byte: `RESERVED=0xff`, `NEW=0`, `OLD=1`. The macros in `common.h:126-128` confirm: `rejuvinate(x)` resets it to `NEW`, `RESERVED` pins a crum against eviction. No wall-clock semantics.

**`coredisk.h:12-115`** — The on-disk serialization format: `typediskloafhedr` has `sizeofthisloaf`, `isapex`, `height`, `denftype`, `numberofcrums`, `refcount`. `typeduc` has `dwid`, `ddsp`, `sonloafptr`. `typedbc` has `dbcwid`, `dbcdsp`, `dinfo`. The `diskheader` global has `filesize`, `bitmap`, `hasenftops`. No timestamps anywhere in the disk format.

**`wisp.h:75-116`** — `typegrantext` has `textstring[GRANTEXTLENGTH]` and `textlength`. `typegranbottomcruminfo` has `granstuff` and `infotype`. `type2dbottomcruminfo` has only `homedoc` (a tumbler). No timestamps.

---

### The `bert.c` `created`/`modified` Fields Are Booleans, Not Timestamps

**`bert.c:13-19`**:
```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;   // char, not time_t
    int type;
    int count;
} bertentry;
```

**`bert.c:128-144`** — `addtoopen()`:
```c
int addtoopen(tumbler *tp, int connection, int created, int type)
{
    ...
    ptr->created = created;   // bert.c:143 — caller passes TRUE or FALSE
    ptr->modified = FALSE;    // bert.c:144
```

**`bert.c:105`** — `logbertmodified()`: `bert->modified = TRUE;`

**`bert.c:173`** — `removefromopen()`: `status = bert->created && !bert->modified;`

`created` means "was this version created during this session" (i.e., it is newly created and should be cleaned up if closed unmodified). `modified` means "has it been written". Both are boolean flags (`char` set to `TRUE`/`FALSE`). Furthermore, `bertentry` exists only in the runtime hash table `berttable[NUMBEROFBERTTABLE]` (`bert.c:29`) — it is not written to disk and is torn down on connection close (`bert.c:195-231`).

---

### How Ordering Actually Works

All ordering is structural, via tumblers:

- **Document and version identity**: a `tumbler` address in the granfilade. A new version (via `docreatenewversion` in `do1.c`, `bert.c:274,290,296`) gets an incremented tumbler — determined by `tumblerincrement` in `tumble.c`, not by wall clock.
- **Link identity**: a tumbler stored as a `typeaddress.address` in the spanfilade.
- **Content ordering**: I-space (ispan) tumblers encode character position order within a version's content stream (`orglinks.c` converts V↔I).
- **Version chain structure**: parent-child relationships are encoded as tumbler sub-addresses (e.g., `1.2.1` is a child of `1.2`), not as timestamps.

---

### Summary

**There are no wall-clock timestamps in udanax-green's persistent state.** `time()` is called in three places (`init.c:40`, `be.c:61`, `bed.c:79`) and in all three cases the result is used only for naming log files. No struct written to disk or tracked in persistent enfilades contains a `time_t`, `struct tm`, or any integer field representing elapsed seconds. The `age` byte in `typecorecrumhedr` is a cache-eviction signal. The `created`/`modified` chars in `bertentry` are session-scoped booleans, never persisted. All ordering — of versions, content, links — is purely structural, encoded in the tumbler address space.
