## Question 16 [gregory]

> When `find_links` is called on doc2 and discovers a link originally created in doc1 through shared I-addresses, does `linksporglset2specset` resolve the link's endset I-addresses against doc2's POOM — returning V-positions within doc2 — or does it return the V-positions from doc1 where the link was originally created?

## KB Synthesis

`linksporglset2specset` resolves endset I-addresses against **whichever document's POOM is passed as the query context** — not necessarily doc1 or doc2 universally. The behavior differs by operation:

## For RETRIEVEENDSETS

[SS-RETRIEVE-ENDSETS] (Finding 0035) is explicit:

> Results are converted back to V-addresses using the querying document's docid.
> **Key: endsets are resolved in terms of the querying document's V-space, not the link's home document.**

So if RETRIEVEENDSETS is invoked from doc2's context, `linksporglset2specset` looks up the link's endset I-addresses in **doc2's POOM**. If those I-addresses exist there (because doc2 transcluded the content), it returns V-positions within doc2. If doc2 doesn't have them, they are silently dropped [INV-ITOV-FILTERING].

[INT-LINK-VERSION] (Finding 0019) confirms this empirically: "When queried from a version, endsets report the version's docid rather than the original's."

## For FOLLOWLINK

[SS-FOLLOWLINK] (Finding 0048) shows it's parametric:

> `followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }`

The caller explicitly specifies which document's POOM to resolve against. Passing doc1 returns V-positions in doc1; passing doc2 returns V-positions in doc2 (or empty if doc2's POOM has no mapping for those I-addresses).

## What `find_links` itself returns

`find_links` returns **link ISAs** (identifiers), not resolved V-positions [SS-FIND-LINKS]. The I-address intersection happens in spanfilade search [SS-SPANF-OPERATIONS] — it determines *which links* are discovered. Resolution of those links' endpoints to V-positions only happens in a subsequent RETRIEVEENDSETS or FOLLOWLINK call, where the document context determines which POOM is consulted.

## Summary

| Operation | POOM consulted |
|---|---|
| `find_links(doc2, ...)` | No POOM — returns link ISAs only |
| RETRIEVEENDSETS from doc2 | doc2's POOM |
| FOLLOWLINK(link, end, doc2) | doc2's POOM |
| FOLLOWLINK(link, end, doc1) | doc1's POOM |

A concrete consequence: if doc2 transcluded "hyperlink text" from doc1, and a link was created on doc1's "hyperlink text", then RETRIEVEENDSETS from doc2 would return V-positions within doc2 where the transcluded content lives — not doc1's original positions. If those I-addresses don't appear in doc2's POOM at all, the result is empty [EC-GHOST-LINK].

---

## Code Exploration

I have all the information needed. Let me now trace the complete execution path and produce the answer.

---

## Answer

### Short answer

`linksporglset2specset` resolves the link's endset I-addresses against **the document that owns the link's POOM** — which is **doc1** (where the link was originally created) — not doc2. This is what the `follow_link` path does. The `retrieve_endsets` path does it differently; see below.

---

### Detailed trace

#### 1. `find_links` does NOT call `linksporglset2specset`

`find_links` maps to `findlinksfromtothree` [`fns.c:189`], which calls `dofindlinksfromtothree` [`do1.c:348`], which calls `findlinksfromtothreesp` [`spanf1.c:56`]:

```c
bool findlinksfromtothreesp(typetask *taskptr, typespanf spanfptr, ...)
{
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, ...);
    ...
    intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
    return (TRUE);
}
```
[`spanf1.c:56–103`]

This function converts V-specs → sporgls → searches the spanfilade by I-address range → returns only **link ISAs** (tumblers). There is no call to `linksporglset2specset` here. The question of V-position resolution doesn't arise at the `find_links` stage.

---

#### 2. `follow_link` — the primary endset-retrieval path after `find_links`

After `find_links` returns a link ISA, the natural follow-up is `follow_link` → `dofollowlink` [`do1.c:223`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    ...
    return (
       link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress,
                             sporglset, specsetptr, NOBERTREQUIRED));
}
```
[`do1.c:228–231`]

The `homedoc` argument passed to `linksporglset2specset` is `&((typesporgl *)sporglset)->sporgladdress` — the document address packed inside the first sporgl returned by `link2sporglset`.

##### How `sporgladdress` gets set — tracing `link2sporglset`

`link2sporglset` [`sporgl.c:67`] retrieves I-addresses from the link's own POOM and builds sporgls via `contextintosporgl` [`sporgl.c:205`]:

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    /* ^^^^^ zzz foo kluge 11/23/84 ^^^^^ */
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);
}
```
[`sporgl.c:205–220`]

`sporglptr->sporgladdress` is set to `context->context2dinfo.homedoc` — the document that was recorded in the POOM crum when the link was created. This was set originally by `insertpm` [`orglinks.c:75`] via `insertnd`, which stores the `linfo.homedoc` from `unpacksporgl`:

```c
int unpacksporgl(typesporglset sporglptr, tumbler *streamptr, tumbler *widthptr, type2dbottomcruminfo *infoptr)
{
    ...
    } else if (((typeitemheader *)sporglptr)->itemid == SPORGLID) {
        movetumbler(&((typesporgl *)sporglptr)->sporglorigin, streamptr);
        movetumbler(&((typesporgl *)sporglptr)->sporglwidth, widthptr);
        movetumbler(&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
    }
}
```
[`sporgl.c:178–203`]

And in `vspanset2sporglset`, when a link is created, the sporgls store `docisa` (doc1) as `sporgladdress`:

```c
movetumbler(docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream, &sporglset->sporglorigin);
movetumbler(&ispanset->width, &sporglset->sporglwidth);
```
[`sporgl.c:53–55`]

Therefore `context->context2dinfo.homedoc` in `contextintosporgl` recovers **doc1's ISA** — the document with which the link was created. So `sporgladdress = doc1`.

---

#### 3. What `linksporglset2specset` does with that `homedoc`

`linksporglset2specset` [`sporgl.c:97`]:

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc,
                           typesporglset sporglset, typespecset *specsetptr, int type)
{
    ...
    for (; sporglset; ...) {
        if (iszerotumbler(&sporglset->sporgladdress)) {
            /* treat as a raw I-span */
            ((typeitemheader *)specset)->itemid = ISPANID;
            movetumbler(&sporglset->sporglorigin, &specset->stream);
            movetumbler(&sporglset->sporglwidth, &specset->width);
        } else {
            linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
        }
    }
}
```
[`sporgl.c:97–123`]

For a non-zero `sporgladdress` it calls `linksporglset2vspec` [`sporgl.c:127`]:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc,
                        typesporglset *sporglsetptr, typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
    specptr->vspanset = NULL;
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```
[`sporgl.c:127–137`]

**Critical observation:** `&specptr->docisa` is set to `homedoc`, not to `sporglset->sporgladdress`. The commented-out alternative `/*&sporglset->sporgladdress*/` shows the original design. In `dofollowlink` these are the same value (since `homedoc` was initialized from `sporglset->sporgladdress`), so the change is a no-op for this path.

`sporglset2vspanset` [`sporgl.c:141`]:

```c
int sporglset2vspanset(typetask *taskptr, typeisa *homedoc,
                       typesporglset *sporglsetptr, typevspanset *vspansetptr, int type)
{
    sporglptr = (typesporgl *)*sporglsetptr;
    (void) findorgl(taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
    ispan.itemid = ISPANID;
    ispan.next = NULL;
    movetumbler(&sporglptr->sporglorigin, &ispan.stream);
    movetumbler(&sporglptr->sporglwidth, &ispan.width);
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
    ...
}
```
[`sporgl.c:141–176`]

Again `homedoc` is used in the `findorgl` call. In the `follow_link` path `homedoc = doc1`, so `findorgl` loads **doc1's POOM**. The sporgl's `sporglorigin` / `sporglwidth` (the I-address range) is then mapped to V-positions using `ispan2vspanset` [`orglinks.c:389`]:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

`permute` walks doc1's POOM, intersecting the stored I-address range with the endset's I-addresses and reading out the corresponding V-coordinates from **doc1's POOM tree**.

---

#### 4. The `retrieve_endsets` path — behaves differently

`retrieve_endsets` → `doretrieveendsets` [`do1.c:369`] → `retrieveendsetsfromspanf` [`spanf1.c:190`]:

```c
linksporglset2specset(taskptr, &((typevspec *)specset)->docisa,
                      fromsporglset, fromsetptr, NOBERTREQUIRED)
```
[`spanf1.c:224`]

Here `homedoc = &((typevspec *)specset)->docisa`, where `specset` is what the **client passed** to identify the link. If the client supplies a vspec whose `docisa` is doc2, then `linksporglset2specset` will call `findorgl` for doc2's POOM and return V-positions in **doc2**. The commented-out code `/*&sporglset->sporgladdress*/` is the only thing that would have forced it back to doc1 in this path.

---

### Summary

| Path | `homedoc` passed to `linksporglset2specset` | POOM used for I→V conversion | Result |
|---|---|---|---|
| `follow_link` (`dofollowlink`) | `sporglset->sporgladdress` = doc1 (set by `contextintosporgl` from the link's POOM crum) | doc1's POOM via `findorgl` | V-positions **in doc1** |
| `retrieve_endsets` (`retrieveendsetsfromspanf`) | `specset->docisa` = whatever the client passed | `findorgl` of client's docisa | V-positions **in whichever doc the client named** |

**For the `follow_link` path** (the natural post-`find_links` call): `linksporglset2specset` resolves the link's endset I-addresses against **doc1's POOM**, returning V-positions from doc1 where the link was originally created. The fact that the link was *discovered* via doc2's shared I-addresses is irrelevant — the resolution is anchored to the document recorded in the link's POOM crums at creation time.

The two commented-out alternatives in `sporgl.c:134` (`/*&sporglset->sporgladdress*/`) and `sporgl.c:152` (`/*&sporglptr->sporgladdress*/`) are relics of a design that would have always used the sporgl's stored doc (doc1) regardless of caller. The current code parameterizes this as `homedoc`, but in `dofollowlink` the caller passes `sporglset->sporgladdress` — which is doc1 — so the behavior is identical on that path.
