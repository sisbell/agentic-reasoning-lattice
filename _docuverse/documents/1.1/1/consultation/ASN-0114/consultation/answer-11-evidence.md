## Question 11 [evidence]

> When the link's ISA (`docISA.0.2.N`) and an end selector are supplied, does the operation return the endset's raw I-address spans from the granfilade link orgl, or are they first converted to V-positions before being returned?

## KB Synthesis

FOLLOWLINK returns **V-address spans**, not raw I-addresses. The operation has two distinct phases.

**Phase 1 — I-address extraction:** `link2sporglset()` reads the link orgl from the granfilade at the requested endset position (0.1, 0.2, or 0.3) via `retrieverestricted()`. This produces a sporglset of raw I-addresses. No POOM check occurs here. [SS-FOLLOWLINK]

**Phase 2 — I-to-V conversion:** `linksporglset2specset()` takes the I-addresses and looks each one up in the specified `homedoc`'s POOM via `span2spanset()`. Any I-address that has no current V-position mapping in that POOM is silently dropped — no error, no partial result. [SS-FOLLOWLINK], [INV-ITOV-FILTERING]

The final result is a SpecSet of V-spans relative to the queried document, not the raw I-spans from the link orgl. This is why FOLLOWLINK can return an empty result for a valid link: all endset I-addresses may be unresolvable in the queried document even though the link orgl is intact. [EC-GHOST-LINK]

This also means the same link can produce different V-span results depending on which `homedoc` is queried — a document that transcludes the endpoint content will see V-spans; a document with no mapping for those I-addresses returns empty. [SS-FOLLOWLINK]

---

## Code Exploration

I have everything I need. Here is the complete answer:

---

## Answer: V-Positions, Not Raw I-Addresses

When `dofollow` (implemented as `dofollowlink`) is given a link ISA and an end selector, it **converts the raw I-address spans to V-positions** before returning them. Here is the exact call chain with citations.

---

### Call Chain

**1. FEBE entry — `fns.c:114–127` — `followlink`**

```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
```

The result type is `typespecset`, which contains vspecs. `putfollowlink` sends those vspecs (V-position specs) to the client.

---

**2. Core function — `do1.c:223–232` — `dofollowlink`**

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

Two steps: (a) retrieve the endset from the link's orgl as sporgls, (b) convert those sporgls back to a specset.

---

**3. Endset retrieval — `sporgl.c:67–95` — `link2sporglset`**

```c
if (!findorgl (taskptr, granf, linkisa, &orgl, type))        // line 77
    return (FALSE);
tumblerincrement (&zero, 0, whichend, &vspan.stream);         // line 81 — build V-address for end selector
tumblerincrement (&zero, 0, 1, &vspan.width);                 // line 82
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {  // line 83
    for (c = context; c; c = c->nextcontext) {
        sporglptr = ...
        contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);  // line 86
```

The retrieval is `V → I`: the V-axis index selects the end (from/to/3), and the I-axis index returns the raw I-address coordinates stored in the link's orgl. Those I-coordinates are packed into the sporgl by `contextintosporgl`.

**`sporgl.c:205–219` — `contextintosporgl`** (called with `index = I`):

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress); // line 209 — referenced doc's ISA
movetumbler(&context->totaloffset.dsas[I],   &sporglptr->sporglorigin);  // line 211 — raw I-origin
movetumbler(&context->contextwid.dsas[I],    &sporglptr->sporglwidth);   // line 219 — raw I-width
```

`sporgladdress` = the ISA of the document being linked to (non-zero for normal vspec endsets). `sporglorigin` / `sporglwidth` = raw I-space coordinates within that document's orgl.

---

**4. Sporgl → specset conversion — `sporgl.c:97–123` — `linksporglset2specset`**

```c
for (; sporglset; ...) {
    if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {  // line 105
        ((typeitemheader *)specset)->itemid = ISPANID;   // raw I-span — only when sporgladdress == 0
        ...
    } else {
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);  // line 116
    }
```

The branch at line 105 is the key decision point:

- **`sporgladdress == 0`**: returns a raw `ISPANID` (I-span) without conversion. This is the case for pure I-span endsets — unusual in practice.  
- **`sporgladdress != 0`** (normal case with vspec endsets): calls `linksporglset2vspec`, which triggers the I→V conversion.

Since normal links are created via `docreatelink` → `specset2sporglset` (which sets `sporgladdress` from the document ISA at `sporgl.c:53`), the sporgladdress is non-zero and the else branch is always taken for normal links.

---

**5. Conversion path — `sporgl.c:127–176` → `orglinks.c:389–422`**

`linksporglset2vspec` (`sporgl.c:132–136`) sets `docisa = homedoc` and calls `sporglset2vspanset`.

`sporglset2vspanset` (`sporgl.c:141–176`):
```c
(void) findorgl (taskptr, granf, homedoc, &orgl, type);  // line 152 — get the *target document's* orgl
ispan.stream = sporglptr->sporglorigin;                   // line 155 — raw I-address
ispan.width  = sporglptr->sporglwidth;                    // line 156 — raw I-width
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // line 157 — I→V
```

`ispan2vspanset` (`orglinks.c:389–393`):
```c
return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
```

`permute` (`orglinks.c:404–422`) iterates the restriction span set and calls `span2spanset` with `restrictionindex=I, targindex=V`, using `retrieverestricted` on the target document's orgl to perform the coordinate transformation.

---

### Summary

| Step | Function | File | What happens |
|------|----------|------|--------------|
| 1 | `followlink` | `fns.c:114` | FEBE dispatch |
| 2 | `dofollowlink` | `do1.c:223` | Calls retrieve, then convert |
| 3 | `link2sporglset` | `sporgl.c:67` | Gets link orgl, retrieves endset via `V→I` retrieval |
| 4 | `contextintosporgl` | `sporgl.c:209` | Packs I-coords + referenced doc ISA into sporgl |
| 5 | `linksporglset2specset` | `sporgl.c:105` | Branches: non-zero address → vspec conversion |
| 6 | `sporglset2vspanset` | `sporgl.c:157` | Calls `ispan2vspanset` with target doc's orgl |
| 7 | `ispan2vspanset` | `orglinks.c:393` | `permute(I → V)` |

**The operation returns V-position spans in the referenced document — not raw I-address spans from the link orgl.** The raw I-addresses are an intermediate form (the sporgl), visible only inside `link2sporglset`. By the time `linksporglset2specset` finishes, those I-addresses have been walked through the target document's orgl via `ispan2vspanset` → `permute(I, V)` and returned as `typevspec` items carrying V-space spans.

The one exception: if a link was created with pure I-span endsets (no document ISA), `linksporglset2specset:105` detects zero `sporgladdress` and returns raw `ISPANID` spans without conversion. This branch exists but is not the normal operational case.
