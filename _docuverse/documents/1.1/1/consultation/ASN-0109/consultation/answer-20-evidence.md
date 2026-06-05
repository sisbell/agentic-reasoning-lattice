## Question 20 [evidence]

> Are the I-address spans returned by a read endset guaranteed immutable for the life of the link, such that two reads of the same link's endsets at different times always return identical I-spans even after DELETE on the referenced content?

## KB Synthesis

**Yes — the I-address spans stored in a link's endsets are immutable for the life of the link. Two reads of the same link's raw endset I-addresses at any time will return identical I-spans.**

The guarantee comes from three independent KB facts:

1. **Link endsets are stored in I-space (the granfilade), which is append-only.** [SS-THREE-LAYER-MODEL] Finding 0040 states: "I-space (link orgl): The link object at a permanent I-address. Contains the link's endset references (FROM, TO, TYPE). Cannot be deleted (permanence axiom P0)." [INV-IADDR-IMMUTABILITY] further confirms: no operation modifies granfilade content — only the POOM is mutable.

2. **No operation removes the link orgl from I-space.** [INV-LINK-PERMANENCE] (Findings 0024, 0029, 0040): the link orgl persists unconditionally. DELETE, REARRANGE, and VCOPY are all granfilade-preserving. [FC-GRANF-ON-DELETE] (Findings 0061, 0063) confirms DELETE only modifies the POOM.

3. **`link2sporglset()` reads I-addresses directly from the link orgl, before any POOM check.** [SS-FOLLOWLINK] Finding 0048: "extracts I-addresses from the link orgl at the requested endset position via `retrieverestricted()` — no POOM check occurs at this stage."

---

**The critical distinction is between raw endset I-spans and what FOLLOWLINK outputs to the caller:**

- **I-spans in the link orgl** → immutable, identical across all reads
- **V-spans returned by FOLLOWLINK** → variable; after DELETE removes content from the POOM, `linksporglset2specset()` silently drops I-addresses with no current POOM mapping [INV-ITOV-FILTERING], producing empty or partial V-span results

This is exactly the "ghost link" state described in [EC-GHOST-LINK]: FOLLOWLINK succeeds, the link orgl is intact with its original I-spans, but the I→V conversion yields `[]` because the I-addresses are no longer mapped in any document's POOM. The I-spans themselves are unchanged; only their resolvability varies.

---

## Code Exploration

Now I have the complete picture. Let me write the definitive answer.

---

## Answer: Immutability of I-Spans Returned by Link Endset Reads

### Short answer

**The I-spans stored in the link's own enfilade are immutable with respect to DELETE.** However, the `followlink` FEBE handler does not return raw I-spans to the client for V-spec-created links — it converts them back to V-spans using the document's *current* orgl. After DELETE, that round-trip yields different results. Whether the returned endsets are stable therefore depends on which path is being examined.

---

### How link endsets are stored at creation

`docreatelink()` [do1.c:195-221] calls:

1. `createorglingranf()` [do1.c:209] — allocates a **separate private orgl** for the link, distinct from any document orgl.
2. `specset2sporglset()` [do1.c:214-216, sporgl.c:14-33] — converts V-specs to sporgls. For V-spec inputs it calls `vspanset2sporglset()` [sporgl.c:35-65] which:
   - calls `vspanset2ispanset()` [orglinks.c:397-402] → `permute()` → `retrieverestricted()` on the **document's** orgl to convert V-positions to I-spans (permascroll addresses)
   - packs the result into a `typesporgl` with `sporgladdress = docisa`, `sporglorigin = I-stream`, `sporglwidth = I-width`
3. `insertendsetsinorgl()` [do1.c:218] → `insertpm()` [orglinks.c:75-134] inserts a 2D crum into the **link's** orgl:
   - [orglinks.c:105]: `movetumbler(&lstream, &crumorigin.dsas[I])` — I-span stream into the crum's I-dimension
   - [orglinks.c:109]: `movetumbler(&lwidth, &crumwidth.dsas[I])` — I-span width into the crum's I-dimension
   - [orglinks.c:113]: `movetumbler(vsaptr, &crumorigin.dsas[V])` — endset selector (0=from, 1=to, 2=three) into the crum's V-dimension
   - [orglinks.c:130]: `insertnd(taskptr, (typecuc*)orgl, ...)` — written into the link's own enfilade

**At creation time, the permascroll I-addresses are captured and written into the link's private enfilade. This is the permanent record.**

---

### What DELETE does (and does not touch)

`dodeletevspan()` [do1.c:158-167]:

```c
return (
   findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // line 164
&& deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)        // line 165
```

`deletevspanpm()` [orglinks.c:145-152]:

```c
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

`deletend()` [edit.c:31-76] operates on `docorgl` — the **document's** enfilade — removing V-space crums and adjusting the tree via `disown()`, `subtreefree()`, and `recombine()`.

**DELETE never touches the link's own orgl.** The link ISA and its enfilade are separate objects in the granfilade. No code path in `dodeletevspan()` or `deletevspanpm()` opens or writes to the link's orgl.

---

### What the `followlink` FEBE handler returns

`followlink()` [fns.c:114-127] calls `dofollowlink()` [do1.c:223-232]:

```c
return (
   link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)  // line 229
&& linksporglset2specset(taskptr, &((typesporgl*)sporglset)->sporgladdress,
                         sporglset, specsetptr, NOBERTREQUIRED));              // line 230
```

**Step 1 — `link2sporglset()`** [sporgl.c:67-95]:

```c
if (!findorgl(taskptr, granf, linkisa, &orgl, type)) return FALSE;  // line 77
// build V-span for whichend (0, 1, or 2)
tumblerincrement(&zero, 0, whichend, &vspan.stream);  // line 81
tumblerincrement(&zero, 0, 1, &vspan.width);          // line 82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL)) {  // line 83
    contextintosporgl((type2dcontext*)c, NULL, sporglptr, I);  // line 86
```

This queries the **link's own orgl** by restricting on V (which endset) and extracting I (permascroll addresses). `contextintosporgl()` [sporgl.c:205-220] stores into `sporglptr`:
- `sporgladdress` ← `context->context2dinfo.homedoc` (the home document ISA stored at crum creation)
- `sporglorigin` ← `context->totaloffset.dsas[I]` (I-span stream — permascroll address)
- `sporglwidth` ← `context->contextwid.dsas[I]` (I-span width)

**These I-spans are read from the link's own enfilade, which DELETE never modifies. They are always identical across reads.**

**Step 2 — `linksporglset2specset()`** [sporgl.c:97-123]:

```c
if (iszerotumbler(&sporgladdress)) {          // line 105
    ((typeitemheader*)specset)->itemid = ISPANID;   // → return raw I-span
} else {
    linksporglset2vspec(..., specptr, type);   // → convert to V-span
}
```

- If the link was created with **raw I-span specsets** (ISPANID): `sporgladdress` is zero [sporgl.c:14-22], so `linksporglset2specset()` emits a raw ISPANID. The client receives the permascroll I-span directly. **This is immutable.**
- If the link was created with **V-spec specsets** (VSPECID — the typical case): `sporgladdress` is the document ISA (non-zero). `linksporglset2vspec()` → `sporglset2vspanset()` [sporgl.c:141-176] → `ispan2vspanset()` [orglinks.c:389-393] → `permute(..., I, ..., V)` [orglinks.c:404-422] → `retrieverestricted()` on the **document's current orgl**. After DELETE has modified the document's enfilade, this I→V conversion yields different V-spans (or none if the content is absent). **The returned V-spans are not immutable.**

---

### The "trying to kluge links followable thru versions" comment

At `sporgl.c:251`, in `sporglset2linksetinrange()`:

```c
if (FALSE/*trying to kluge links followable thru versions */ && ...)
```

This dead branch was an abandoned attempt to make link following version-aware. Its presence confirms the developers recognized that link endsets do **not** automatically track through version changes — they are frozen at creation time in I-space, and the back-conversion to V-space is done against whatever the current document state happens to be.

---

### Summary

| Layer | Immutable after DELETE? | Evidence |
|---|---|---|
| I-spans in the link's private orgl | **YES** | DELETE calls `deletend(docorgl, ...)` [do1.c:165], never the link's orgl |
| Raw I-span returned when endset is an ISPANID | **YES** | `linksporglset2specset()` emits ISPANID directly [sporgl.c:112-114] |
| V-spans returned when endset is a VSPECID | **NO** | `ispan2vspanset()` re-queries the document's current orgl [orglinks.c:389-393]; DELETE changes that orgl |

**The permascroll I-addresses stored in the link's endsets are permanent.** The link owns its own enfilade and DELETE never writes to it. But the FEBE `followlink` response for V-spec-created links is a V-span computed against the document's current state — which means two reads of the same link, bracketing a DELETE on the referenced content, can return different (or empty) endsets to the client.
