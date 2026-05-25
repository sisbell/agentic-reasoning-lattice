## Question 19 [evidence]

> When the type endset references a type registered at `1.0.2.x` in the global type namespace, is that I-address resolved to a V-position in the type document's POOM, or returned as a raw I-address since the type namespace has no document context?

## KB Synthesis

Based on the KB, the type endset goes through the same I-to-V conversion path as source and target endsets — it is **not** returned as a raw I-address.

## Resolution Mechanism

From [SS-FOLLOWLINK]:
> `link2sporglset()` extracts I-addresses from the link orgl at the requested endset position (0.1, 0.2, or **0.3**) via `retrieverestricted()`. Then `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM. If `retrieverestricted` returns NULL, the I-address is **silently dropped**.

The type endset (position 0.3) is handled identically to source (0.1) and target (0.2) — no special-casing.

## What the Type Endset Contains

From [SS-LINK-ENDPOINT] Finding 0024: type addresses like `1.0.2.2` (JUMP) are permascroll I-addresses of content in the bootstrap document. They were recorded as V-spans (`link.type : VSpec` where `VSpec.docid = bootstrap_doc`) when the link was created.

## Resolution Depends on `homedoc` POOM

From [INV-ITOV-FILTERING]: both FOLLOWLINK and RETRIEVEENDSETS share the same I-to-V filter — unreferenced I-addresses are silently excluded. The type I-addresses only resolve to V-positions if the queried `homedoc`'s POOM maps them.

The anomalous behavior in [EC-ORPHANED-LINK] Finding 0024 — where type returns **empty** when both endpoints are deleted — is consistent with this: the implementation apparently uses the link's home document as `homedoc` for all three endsets. When that document's POOM no longer contains the relevant I-address mappings (or some resolution precondition fails), the type endset returns empty despite the bootstrap document being intact.

## What the KB Cannot Resolve

The KB does not document **which** `homedoc` `dofollowlink` passes for the type endset specifically. The normal-operation case (type resolving to `QUOTE`, `JUMP`, etc.) implies the bootstrap document's POOM is accessible, but the mechanism is not explicitly traced.

---

## Code Exploration

I now have all the evidence needed. Here is the full answer:

---

## Type Endset I-Address Resolution

**Short answer:** The I-address is **resolved to a V-position** using `ispan2vspanset` → `permute`, with the type document's own POOM as conversion context. There is no bypass for the `1.0.2.x` type namespace. Raw I-addresses are only returned in a different, narrower case.

---

### The Call Chain

**`dofollowlink`** — `do1.c:223–231`

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
    && linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

`link2sporglset` extracts I-addresses from the link's endset into a `typesporglset`. `linksporglset2specset` then converts those sporgls into the client-facing specset. The `homedoc` parameter passed in is `sporglset->sporgladdress` — the document address stored in the first sporgl.

---

### How sporgls are built — `contextintosporgl`

**`sporgl.c:205–220`**

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    /* ^^^^^ zzz foo kluge 11/23/84 ^^^^^ */
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler (&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```

`sporgladdress` is set to `context->context2dinfo.homedoc` — the document that the I-address lives in. For a type endset referencing a type at `1.0.2.x`, `sporgladdress` = `1.0.2.x`. The "kluge" comment (11/23/84) marks that `linkid` was the original intended value, later overridden.

---

### The fork in `linksporglset2specset`

**`sporgl.c:97–123`**

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc, typesporglset sporglset, typespecset *specsetptr, int type)
{
    ...
    if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {
        /* BRANCH A — raw I-address returned */
        ((typeitemheader *)specset)->itemid = ISPANID;
        movetumbler(&((typesporgl *)sporglset)->sporglorigin, &((typeispan *)specset)->stream);
        movetumbler(&((typesporgl *)sporglset)->sporglwidth,  &((typeispan *)specset)->width);
    } else {
        /* BRANCH B — I→V conversion */
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
```

**Branch A** (zero `sporgladdress`): raw `ISPANID` returned, no conversion.  
**Branch B** (non-zero `sporgladdress`): conversion is triggered. A type endset with `sporgladdress = 1.0.2.x` is non-zero, so **Branch B always fires**.

---

### I→V conversion — `linksporglset2vspec` and `sporglset2vspanset`

**`sporgl.c:127–137`**

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr, typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);  // docisa = 1.0.2.x
    specptr->vspanset = NULL;
    sporglset2vspanset (taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

The commented-out `/*&sporglset->sporgladdress*/` reveals the historical intent: use the sporgl's own document address. The current code uses `homedoc` instead — but since `dofollowlink` passes `&sporglset->sporgladdress` as `homedoc`, the value is the same for the first (and in practice only) sporgl processed.

**`sporgl.c:141–176`**

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    ...
    (void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
    ispan.itemid = ISPANID;
    movetumbler (&sporglptr->sporglorigin, &ispan.stream);
    movetumbler (&sporglptr->sporglwidth,  &ispan.width);
    vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
    ...
}
```

`findorgl` looks up `1.0.2.x` in the granfilade to get its POOM. The return value is cast `(void)` — a failure is silently ignored. `ispan2vspanset` then calls:

**`orglinks.c:389–394`**

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    typespanset *permute();
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` walks the POOM for `1.0.2.x` and maps the I-address to one or more V-positions within that document.

---

### What the client receives

The result in `specsetptr` is a `typevspec` with:
- `itemid = VSPECID`
- `docisa = 1.0.2.x` (the type document's tumbler address)
- `vspanset` = V-positions within the type document's POOM

This is **identical in form** to following a link endset into any other document. There is no special code path for the type namespace.

---

### The one edge case: zero `sporgladdress`

Raw `ISPANID` is returned only when `sporgladdress` is zero — which would indicate an I-address that was stored without an associated document context. A properly registered type at `1.0.2.x` yields a non-zero `sporgladdress`, so this path does not apply.

---

### Summary

The I-address in a type endset referencing `1.0.2.x` **is resolved to V-positions** via `findorgl(1.0.2.x)` → `ispan2vspanset` → `permute`. The type namespace has no special bypass. The `docisa` in the returned `typevspec` is `1.0.2.x`, and the `vspanset` contains positions within that type document's content ordering. If `findorgl` fails to locate a POOM for `1.0.2.x` (e.g., the type document has never been initialized in the granfilade), the failure is swallowed (`(void)` cast at `sporgl.c:152`) and `ispan2vspanset` is called with a garbage `orgl` — a latent crash risk in that corner case.
