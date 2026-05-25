## Question 15 [evidence]

> When the home document parameter to `find_links` is specified but `sporglset2linkset` overrides it via `TRUE||!homeset` [EC-FIND-LINKS-GLOBAL], does the endset resolution step also ignore the home document, or is the home document used to scope which POOM is consulted for I→V conversion?

## KB Synthesis

Two separate concerns are at play here, and the KB is clear on how they split.

## The `find_links` home document parameter affects only the search phase

`find_links` (FINDLINKSFROMTOTHREE) returns **link ISAs** — it does not perform I→V conversion. The `homedocids` parameter was designed to restrict the orgl-dimension search in the spanfilade, scoping which link orgls are returned. Per [EC-FIND-LINKS-GLOBAL] / [PRE-FIND-LINKS F0069], the `TRUE||!homeset` guard in `sporglset2linkset()` overrides that parameter unconditionally, replacing it with a hardcoded width-100 range from zero. The home document is therefore ignored in the search phase entirely.

## I→V conversion is a separate operation with a separate homedoc

Endset resolution (I-address → V-address conversion) does not happen within `find_links` at all. It happens in two places:

**FOLLOWLINK** [SS-FOLLOWLINK F0048]: Takes `(link_isa, whichend, homedoc)` as distinct parameters. `linksporglset2specset()` looks up the endset I-addresses against the specified `homedoc`'s POOM. If the I-address has no POOM mapping in that homedoc, it is silently dropped [INV-ITOV-FILTERING]. The homedoc here is the caller's choice of which document's POOM to resolve through — completely independent of the `find_links` call that discovered the link ISA.

**RETRIEVEENDSETS** [SS-RETRIEVE-ENDSETS F0035]: Converts the input specset to I-addresses (via the querying document's POOM), searches the spanfilade, then converts results back to V-specs using the querying document's docid. The endset V-addresses are always relative to the querying document's context [INT-LINK-VERSION F0019].

## Summary

The `homedocids` parameter to `find_links` was intended to scope which link orgls are searched — it has no role in I→V conversion. Due to [EC-FIND-LINKS-GLOBAL], it has no effect on the search either. Endset resolution consults a wholly separate `homedoc` parameter supplied to FOLLOWLINK or RETRIEVEENDSETS, and that consultation is correct and functional.

---

## Code Exploration

I now have all the code I need. Let me trace the complete answer from entry point to I→V conversion.

---

## Answer: Home Document in `find_links` vs. Endset Resolution

### Stage 1 — `find_links` home document is discarded before `sporglset2linkset`

The `find_links` home document parameter is killed at the **very first call** in `fns.c`, before it ever reaches `sporglset2linkset`:

```c
// fns.c:197-199
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                            (typeispan*)NULL/*homeset*/, &linkset)
```

The `homeset` is parsed off the wire but immediately replaced with `(typeispan*)NULL` [fns.c:198]. It is passed as `orglrangeptr=NULL` through `dofindlinksfromtothree` [do1.c:352] into `findlinksfromtothreesp` [spanf1.c:77], and then into `sporglset2linkset` as `orglrange=NULL`.

Inside `sporglset2linkset` [sporgl.c:222-237], the `TRUE||!homeset` guard is unconditional — it fires regardless of whether `orglrange` was NULL or carried a real home document:

```c
// sporgl.c:227-233
if (TRUE||!homeset) {
    tumblerclear (&nullhomeset.stream);
    tumblerclear (&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
```

This substitutes a synthetic range of `[0, 100)` in the ORGLRANGE dimension and passes it to `sporglset2linksetinrange` [sporgl.c:257-259]:

```c
// sporgl.c:257-259
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

The ORGL range restriction is `[0, 100)` — effectively global. The home document plays no role in link discovery.

---

### Stage 2 — Endset resolution uses the link's docisa, not the find_links home document

Endset resolution is a **separate operation** (`retrieve_endsets`). The `find_links` home document parameter does not flow into it at all.

`doretrieveendsets` [do1.c:369-374] delegates to `retrieveendsetsfromspanf` [spanf1.c:190-235]. The critical call chain is:

```c
// spanf1.c:222-226
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

The `homedoc` argument to `linksporglset2specset` is `&((typevspec *)specset)->docisa` — **the link's own document ISA**, not the user's `find_links` home document.

`linksporglset2specset` [sporgl.c:116] calls `linksporglset2vspec` for every sporgl with a non-zero `sporgladdress`:

```c
// sporgl.c:127-137
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc,
                        typesporglset *sporglsetptr, typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);  // KLUGE
    specptr->vspanset = NULL;
    sporglset2vspanset (taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

The commented-out `/*&sporglset->sporgladdress*/` reveals the original intent: use the sporgl's own `sporgladdress` (the **content document**). The kluge substitutes `homedoc` (the **link document**) in both `linksporglset2vspec:134` and `sporglset2vspanset:152`.

`sporglset2vspanset` then performs the I→V lookup:

```c
// sporgl.c:150-157
sporglptr = (typesporgl *)*sporglsetptr;
(void) findorgl (taskptr, granf, homedoc/*&sporglptr->sporgladdress*/, &orgl, type);
ispan.itemid = ISPANID;
ispan.next = NULL;
movetumbler (&sporglptr->sporglorigin, &ispan.stream);
movetumbler (&sporglptr->sporglwidth, &ispan.width);
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

`findorgl` uses `homedoc` (= the link's docisa) to look up the POOM in the granfilade. `ispan2vspanset` [orglinks.c:389-393] calls `permute(taskptr, orgl, ispanptr, I, vspansetptr, V)` [orglinks.c:404], which calls `span2spanset` [orglinks.c:425-453] with a `retrieverestricted((typecuc*)orgl, ...)` — querying **that specific POOM** (the link document's POOM) for the I→V translation.

---

### Comparison: `dofollowlink`

`follow_link` handles this differently. In `dofollowlink` [do1.c:228-231]:

```c
link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
&& linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                          sporglset, specsetptr, NOBERTREQUIRED));
```

Here `homedoc` is `sporglset->sporgladdress` — the address that was set in `contextintosporgl` [sporgl.c:209]:

```c
// sporgl.c:209 — another acknowledged kluge ("11/23/84")
movetumbler(/*linkid*/&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
```

In `follow_link`, `sporgladdress` carries `context2dinfo.homedoc` from the link document's POOM lookup — in practice the content document's address. The `homedoc`/`sporgladdress` substitution is therefore a no-op for `follow_link`: both point to the same content document.

---

### Conclusion

**The `find_links` home document parameter has no effect on which POOM is consulted for I→V conversion in endset resolution.** There are two independent reasons:

1. **Dead parameter**: The home document is discarded at `fns.c:198` (`(typeispan*)NULL/*homeset*/`) before `dofindlinksfromtothree` is ever called. Even if it weren't discarded, `sporglset2linkset`'s hardcoded `TRUE||` [sporgl.c:227] would override it unconditionally.

2. **Separate code path**: Endset resolution (`retrieve_endsets`) does not receive or consult the `find_links` home document at all. The POOM for I→V conversion is selected by `findorgl(taskptr, granf, homedoc, &orgl, type)` [sporgl.c:152], where `homedoc` = the **queried link's own docisa** [spanf1.c:224]. This is a property of the link being queried, not of the original `find_links` call.

The kluged substitution of `homedoc` for `sporglptr->sporgladdress` in `linksporglset2vspec:134` and `sporglset2vspanset:152` means the I→V conversion in `retrieve_endsets` always uses the link document's POOM — regardless of which document the endset content actually lives in. This is semantically correct only when the link's endsets point to content held in the same document that owns the link.
