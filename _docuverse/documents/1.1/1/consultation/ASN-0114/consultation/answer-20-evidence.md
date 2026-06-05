## Question 20 [evidence]

> Does the returned spec-set carry the endset's content-identity (I-address) addressing directly, or does it embed the source document identity (sporgl) so the caller knows which document's V-space the spans originate from?

## KB Synthesis

The returned SpecSet carries **V-address specs with document identity embedded**, not raw I-addresses.

The two-phase conversion in `FOLLOWLINK` makes this clear [SS-FOLLOWLINK]:

1. `link2sporglset()` extracts endset I-addresses from the link orgl into **sporgls** — each sporgl bundles `(sporglorigin: IAddress, sporglwidth, sporgladdress: DocISA)` [SS-SPORGL]. The `sporgladdress` field is the document that contains the content at that I-address.

2. `linksporglset2specset()` then converts those sporgls to V-address specs by looking up each I-address in the specified `homedoc`'s POOM. If an I-address has no mapping in that POOM, it is silently dropped [INV-ITOV-FILTERING].

What the caller receives is a **SpecSet** of VSpecs — each VSpec is `(doc: Tumbler, start: Tumbler, width: Tumbler)` — so the document identity is fully embedded in the result [SS-SPECSET].

The implication is that the same link's endset can resolve to different document identities and V-positions depending on which `homedoc` is passed to `FOLLOWLINK`. This is observable: when queried from a version, endsets report the **version's** docid rather than the original's [INT-LINK-VERSION, Finding 0019]. The I-addresses are permanent and stable internally, but the caller-visible result is always document-relative V-coordinates.

---

## Code Exploration

I have all the evidence needed. Here is the full answer.

---

## Answer: How the Returned Spec-Set Is Addressed

The returned spec-set carries **V-space spans embedded inside a `typevspec` item, with the source document identity (`docisa`) as an explicit field.** It does not deliver raw I-addresses to the caller.

---

### The execution path from call to wire

**`followlink` → `dofollowlink` → `link2sporglset` → `linksporglset2specset` → `linksporglset2vspec` + `sporglset2vspanset`**

#### Step 1 — `dofollowlink` [do1.c:223–232]

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,
           &((typesporgl *)sporglset)->sporgladdress,   /* ← homedoc */
           sporglset, specsetptr, NOBERTREQUIRED));
}
```

The second argument to `linksporglset2specset` is `&((typesporgl *)sporglset)->sporgladdress` — the first sporgl's `sporgladdress`, which is the document ISA that owns the referenced content. This becomes the `homedoc` for all subsequent specset construction.

---

#### Step 2 — `link2sporglset` [sporgl.c:67–95]

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);    /* e.g. whichend=1 → V=1.1 */
tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);
context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, ...);
for (c = context; c; c = c->nextcontext) {
    sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
    contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
    ...
}
```

`contextintosporgl` [sporgl.c:205–220] populates a `typesporgl` with three things:

```c
movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);  /* doc ISA */
movetumbler(&context->totaloffset.dsas[I], &sporglptr->sporglorigin);     /* I-stream */
movetumbler(&context->contextwid.dsas[I],  &sporglptr->sporglwidth);      /* I-width  */
```

So at this intermediate stage the data **is** in I-space (`sporglorigin`, `sporglwidth`), plus a document identity (`sporgladdress`). The sporglset is an internal representation — it never leaves the backend.

---

#### Step 3 — `linksporglset2specset` [sporgl.c:97–123]

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset,
                           typespecset *specsetptr, int type)
{
    *specsetptr = NULL;
    for (; sporglset; sporglset = ...) {
        specset = (typespecset) taskalloc(taskptr, sizeof(typevspec));
        if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
            /* sporgladdress==0 → bare I-span (no source doc) */
            ((typeitemheader *)specset)->itemid = ISPANID;
            movetumbler(...sporglorigin..., &((typeispan *)specset)->stream);
            movetumbler(...sporglwidth...,  &((typeispan *)specset)->width);
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
        ...
    }
}
```

When `sporgladdress` is non-zero (the normal case), control goes to `linksporglset2vspec`.

---

#### Step 4 — `linksporglset2vspec` [sporgl.c:127–137] — the key site

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr,
                        typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler(homedoc /*&sporglset->sporgladdress*/, &specptr->docisa);  /* ← embeds doc identity */
    specptr->vspanset = NULL;
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

Two things happen here:

1. **`specptr->docisa` is set to `homedoc`** — the document ISA that owns the referenced content. The commented-out alternative `&sporglset->sporgladdress` (which would have used each individual sporgl's own address) was overridden in favor of the single `homedoc` passed in from `dofollowlink`. The net effect is that all returned VSPECs get the same `docisa`.

2. **`sporglset2vspanset`** [sporgl.c:141–176] converts the internal I-addresses back to V-space:

```c
findorgl(taskptr, granf, homedoc, &orgl, type);
ispan.stream = sporglptr->sporglorigin;          /* I-address */
ispan.width  = sporglptr->sporglwidth;
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);   /* I → V */
```

`ispan2vspanset` [orglinks.c:389–393] calls `permute(... I ... V ...)` to project the I-span through the document's enfilade, yielding V-space spans in `homedoc`'s coordinate system.

---

### What the FEBE client actually receives

The specset sent back by `putfollowlink` [fns.c:124] is a linked list of `typevspec` items. Each item has:

| Field | Content |
|---|---|
| `itemid` | `VSPECID` |
| `docisa` | The document ISA (tumbler) of the source document — i.e., the sporgl's document identity |
| `vspanset` | V-space spans within that document |

The client therefore receives **neither raw I-addresses nor bare V-coordinates**. It receives a **(document ISA, V-spans)** pair — a vspec — which is the backend's standard way of expressing "these V-positions inside this specific document."

The source document identity is embedded directly in the `docisa` field of each returned vspec. This is what tells the caller which document's V-space the spans originate from. Without `docisa`, the V-coordinates would be uninterpretable, since V-space is per-document.

---

### Special case: `sporgladdress == 0`

If a sporgl's `sporgladdress` is the zero tumbler, `linksporglset2specset` [sporgl.c:105–114] emits a bare `ISPANID` item with raw I-stream and I-width, bypassing V-space conversion entirely. This path exists in code but represents an abnormal case — the non-distribution build calls `gerror` if a zero-width ispan results.

---

### Summary

The returned spec-set carries **V-space spans with an embedded source-document ISA (`docisa`)** — not I-addresses. The internal sporgl (which is I-addressed) is a transient intermediate. By the time data reaches the FEBE wire, it has been projected back from I→V through the document's enfilade, and the document's tumbler address is placed into each vspec's `docisa` field so the caller knows exactly which document's V-space those coordinates belong to.
