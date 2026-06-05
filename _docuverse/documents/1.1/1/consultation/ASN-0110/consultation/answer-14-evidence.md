## Question 14 [evidence]

> Does the region-to-endset query distinguish among the three endset roles (source, target, type), or does it return any endset of any role whose I-span touches the region?

## KB Synthesis

RETRIEVEENDSETS distinguishes the three roles separately.

From [SS-RETRIEVE-ENDSETS] and [INT-SPORGL-LINK-INDEX] (both citing Finding 0035): the operation converts the input specset to I-addresses (sporglset) and then **searches each endset type independently** using distinct ORGLRANGE subspace prefixes:

- LINKFROMSPAN = 1 (source)
- LINKTOSPAN = 2 (target)
- LINKTHREESPAN = 3 (type)

Each role gets its own call to `retrievesporglsetinrange()` with the appropriate ORGLRANGE restriction. The operation returns **three separate specsets simultaneously** — one per role — rather than a single undifferentiated union.

So a region that touches only a source endset will produce a non-empty from-specset and empty to/three-specsets. The roles do not bleed into each other.

---

## Code Exploration

I now have everything I need. Here is the full answer.

---

## `retrieve_endsets`: Role Distinction is Structural and Strict

The region-to-endset query (`retrieve_endsets`, command 28) **always distinguishes among the three roles**. It does not return a flat union of all endsets touching the region; it returns three role-separated sets. The separation is enforced by the spanfilade's two-dimensional index, not by post-query filtering.

---

### The Spanfilade's Two Dimensions

The spanfilade (`spanf`) is a 2D structure with two axes:

- **SPANRANGE**: the I-address (permascroll address) of the linked content
- **ORGLRANGE**: the link identity with the role encoded as a prefix

At link creation, `insertendsetsinspanf` in `do2.c:116-128` calls `insertspanf` once per role:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset,  LINKFROMSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,    LINKTOSPAN)
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN)
```

Inside `insertspanf` at `spanf1.c:22`, the role constant is prepended to the ORGLRANGE key:

```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3` (defined in `xanadu.h:36-38`). This means the spanfilade stores three structurally separate entries for each link endpoint — one per role — distinguished by the leading digit of their ORGLRANGE coordinate.

---

### How `retrieveendsetsfromspanf` Queries by Role

`doretrieveendsets` in `do1.c:369-373` immediately delegates to `retrieveendsetsfromspanf` in `spanf1.c:190-235`. That function:

**Step 1** — converts the input specset to a sporglset (I-address set):

```c
specset2sporglset(taskptr, specset, &sporglset, NOBERTREQUIRED)  // spanf1.c:222
```

**Step 2** — builds three role-specific window spans over ORGLRANGE:

```c
fromspace.stream.mantissa[0]  = LINKFROMSPAN;   // = 1, width = 1  [spanf1.c:210-211]
tospace.stream.mantissa[0]    = LINKTOSPAN;     // = 2, width = 1  [spanf1.c:213-214]
threespace.stream.mantissa[0] = LINKTHREESPAN;  // = 3, width = 1  [spanf1.c:216-217]
```

Each window covers exactly one role value — the spans are non-overlapping by construction.

**Step 3** — calls `retrievesporglsetinrange` three times, passing a different window each time:

```c
retrievesporglsetinrange(taskptr, sporglset, &fromspace,  &fromsporglset)  // [line 223]
retrievesporglsetinrange(taskptr, sporglset, &tospace,    &tosporglset)    // [line 225]
retrievesporglsetinrange(taskptr, sporglset, &threespace, &threesporglset) // [line 230]
```

Inside `retrievesporglsetinrange` at `spanf1.c:245`, the core call is:

```c
context = retrieverestricted((typecuc*)spanf,
    (typespan*)sporglptr, SPANRANGE,     // restrict by I-address in SPANRANGE
    whichspace,          ORGLRANGE,      // restrict by role in ORGLRANGE
    (typeisa*)NULL);
```

This is a 2D range query: "return entries where the I-address overlaps the queried region **and** the ORGLRANGE key falls within `whichspace`." Because `fromspace`/`tospace`/`threespace` cover non-overlapping ORGLRANGE intervals, each of the three calls returns only the endsets of one role.

---

### How `find_links` Also Enforces Role (`findlinksfromtothreesp`, `spanf1.c:56-103`)

The `find_links` operation (command 30) works the same way from the other direction. It takes three separate role-assigned input specsets, and each is queried against only its designated spanfilade layer:

```c
sporglset2linkset(taskptr, spanfptr, fromsporglset,  &fromlinkset, orglrange, LINKFROMSPAN)  // [line 77]
sporglset2linkset(taskptr, spanfptr, tosporglset,    &tolinkset,   orglrange, LINKTOSPAN)    // [line 85]
sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset,orglrange, LINKTHREESPAN) // [line 93]
```

Inside `sporglset2linksetinrange` at `sporgl.c:257-259`, the role constant is again prepended to the ORGLRANGE restriction:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

---

### Summary

**The region-to-endset query strictly distinguishes all three roles.** Role separation is a structural property of the spanfilade, not a filter applied after retrieval:

- At **insertion** (`insertspanf`, `spanf1.c:22`): each endset is stored with its role (1/2/3) as the leading digit of its ORGLRANGE coordinate.
- At **retrieval** (`retrievesporglsetinrange`, `spanf1.c:245`): the spanfilade is queried three times with role-specific ORGLRANGE windows (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`), each covering exactly one role.

An I-span touching the queried region will appear in `fromsetptr` if and only if it was recorded as a source endset, in `tosetptr` if and only if it was a target endset, and in `threesetptr` if and only if it was a type endset. There is no cross-role contamination.
