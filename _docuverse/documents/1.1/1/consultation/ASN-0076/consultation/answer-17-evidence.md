## Question 17 [evidence]

> When `link2sporglset` extracts I-addresses from a link, does it traverse a fixed three-endset structure, or could it handle a fourth endset slot representing a "supersedes" relationship to a prior link's ISA?

## KB Synthesis

The KB describes a **fixed three-endset structure** with no evidence of a fourth slot.

**What `link2sporglset` actually traverses:**

`link2sporglset()` calls `retrieverestricted()` with a caller-specified endset position — values `0.1`, `0.2`, or `0.3` — corresponding to FROM, TO, and THREE respectively [SS-FOLLOWLINK, Finding 0048]. The function has no branching logic for additional slots.

**Why three is the fixed limit:**

The structure is anchored in three independent places:

1. `setlinkvsas()` hardcodes mantissa[0] values 1, 2, and 3 for the three endpoints when creating link V-space entries [SS-SUBSPACE-CONVENTION, Finding 0038]
2. `retrieveendsetsfromspanf()` defines exactly three ORGLRANGE prefix constants: `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [SS-RETRIEVE-ENDSETS, Finding 0035]
3. `RETRIEVEENDSETS` (opcode 28) returns exactly three specsets simultaneously: from, to, and three-endset [SS-RETRIEVE-ENDSETS]

**On a "supersedes" fourth slot:**

The KB contains no evidence of a fourth endset position in any code path, data structure, or protocol opcode. The "three" (third) endpoint is the link **type** endpoint — a VSpec into the bootstrap document's type registry at `1.0.2.x` [SS-LINK-ENDPOINT, Finding 0024]. There is no "supersedes" slot and no mechanism in `link2sporglset` to reach one.

If such a relationship existed it would require changes to `setlinkvsas()`, new ORGLRANGE constants, and a new opcode — none of which appear in the KB.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## `link2sporglset`: Fixed Three-Endset Structure

### What the function actually does

`link2sporglset` [sporgl.c:67–95] is **mechanically generic** — it knows nothing about endset semantics. Its core is:

```c
tumblerclear (&zero);
tumblerincrement (&zero, 0, whichend, &vspan.stream);   // [sporgl.c:81]
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);      // [sporgl.c:82]
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
```

It constructs a V-span at position `whichend` with width 1, calls `retrieverestricted` to fetch I-addresses at that slot in the link's granfilade enfilade, and chains the results as sporgl items. The function itself imposes no upper bound on `whichend`.

---

### The physical endset layout is hardwired at link creation

The only code that ever **writes** endset data into a link enfilade is `setlinkvsas` [do2.c:169–183]:

```c
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);   // slot 1 = from
tumblerincrement(tovsaptr,   0, 2, tovsaptr);     // slot 2 = to
tumblerincrement(threevsaptr, 0, 3, threevsaptr); // slot 3 = three (if non-NULL)
```

This is invoked by both link creation paths:
- `domakelink` [do1.c:189]: `setlinkvsas(&fromvsa, &tovsa, NULL)` — two endsets only
- `docreatelink` [do1.c:217]: `setlinkvsas(&fromvsa, &tovsa, &threevsa)` — three endsets

Both paths call `insertendsetsinorgl` [do2.c:130–149] and `insertendsetsinspanf` [do2.c:116–128] using the same three constants defined in `xanadu.h`:

```c
#define LINKFROMSPAN    1   // [xanadu.h:36]
#define LINKTOSPAN      2   // [xanadu.h:37]
#define LINKTHREESPAN   3   // [xanadu.h:38]
#define DOCISPAN        4   // [xanadu.h:39] — NOT a link endset
```

`DOCISPAN = 4` is used in the spanfilade to represent a document's own I-span range — entirely separate from link endsets, a different span type in a different logical context.

---

### The input gate enforces {1, 2, 3} explicitly

The interactive path in `getfollowlink` [get1.c:63–73]:

```c
getnumber (taskptr, whichendptr)
&& (*whichendptr == 1 || *whichendptr == 2 || *whichendptr == 3)  // [get1.c:70–71]
```

Any value outside {1, 2, 3} returns `FALSE` immediately, before ever reaching `link2sporglset`.

The FEBE path in `get1fe.c` [174–180] has **no such validation** — it reads the number blindly:

```c
return (
   getnumber (taskptr, whichendptr)
&& gettumbler (taskptr, linkisaptr));
```

So the FEBE protocol could in principle send `whichend=4`, and it would reach `link2sporglset`. But `retrieverestricted` would find nothing at that V-position (since nothing was ever written there), and the function would return `FALSE` [sporgl.c:92–94].

---

### The parallel `retrieveendsets` path confirms the ceiling

`retrieveendsetsfromspanf` [spanf1.c:190–235] — the separate `RETRIEVEENDSETS` request handler — also retrieves exactly three endsets and no more:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // [spanf1.c:210]
tospace.stream.mantissa[0]   = LINKTOSPAN;      // [spanf1.c:213]
threespace.stream.mantissa[0]= LINKTHREESPAN;   // [spanf1.c:216]
```

Its signature `(fromsetptr, tosetptr, threesetptr)` [spanf1.c:190] has no fourth output parameter, and its `putretrieveendsets` serializer [putfe.c:356–360] transmits exactly three item sets.

---

### Conclusion

`link2sporglset` traverses a **fixed three-endset structure**. It is not a static three-slot loop — it is a generic single-slot lookup parameterized by `whichend` — but the system only ever writes data into slots 1, 2, and 3 (via `setlinkvsas`), and the interactive input gate [get1.c:70–71] enforces that only those values are requested.

There is **no fourth endset slot** representing a "supersedes" relationship anywhere in this codebase. No such constant is defined (the nearest candidate, `DOCISPAN = 4`, is a document span type, not a link endset), no writer populates slot 4 during link creation, and no retrieval path requests it. If slot 4 were requested via the unguarded FEBE path, `link2sporglset` would mechanically attempt the lookup and return `FALSE` when nothing was found.
