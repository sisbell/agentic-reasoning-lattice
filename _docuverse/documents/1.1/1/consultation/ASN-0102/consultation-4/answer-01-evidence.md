## Question 1 [evidence]

> Does `docopy` (via `specset2ispanset` / `insertspanf`) accept source spans drawn from the link subspace, or does it restrict resolved source spans to content?

## KB Synthesis

`docopy` accepts source spans from either subspace — it performs **no restriction** on the source I-address types.

The evidence is direct [PRE-VCOPY]:

> `docopy` (`do1.c:45-65`) copies I-spans from a source specset without validating that the source I-address types match the destination subspace. `acceptablevsa` is a no-op (always returns TRUE). Text I-addresses can be copied into the link subspace and link ISAs into the text subspace.

The call chain `specset2ispanset` → `permute` → `retrieverestricted` is fully type-agnostic [SS-DUAL-ENFILADE Finding 0011]:

> The unified enfilade storage treats all V→I mappings identically. Both permascroll addresses and link orgl ISAs are untyped tumblers; no code in the storage path distinguishes them.

`insertspanf` similarly records whatever I-spans are passed in [FC-CONTENT-SPANF-ISOLATION Finding 0036] — it does not inspect whether they came from the text or link subspace.

The practical consequence: if a caller builds a specset from the full output of `retrieve_vspanset` (which includes both subspaces), `docopy` will silently copy link orgl ISAs into the destination's text subspace. `retrieve_contents` on those positions then dereferences a link ISA in the permascroll, returning garbage [EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES]. Filtering to the text subspace before constructing the source specset is a **caller obligation**, not an enforcement [PRE-SUBSPACE-CONVENTION].

---

## Code Exploration

I have all the source I need. Let me compose the complete answer now.

---

## Answer: `docopy` Does Not Filter by Subspace

The full call chain — `docopy` → `specset2ispanset` → `vspanset2ispanset` → `permute` → `insertspanf` — contains **zero subspace checks**. Source spans drawn from the link subspace (V ≥ 2.x) pass through entirely unfiltered.

---

### The `docopy` Entry Point — `do1.c:45–65`

```c
bool docopy(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
  ...
    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // [54]
    && findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)         // [55]
    && acceptablevsa (vsaptr, docorgl)                                   // [56]
    && asserttreeisok(docorgl)                                           // [57]
    && insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)          // [60]
    && insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)       // [62]
    && asserttreeisok(docorgl));                                         // [63]
}
```

No subspace conditional exists here. The specset is passed directly to `specset2ispanset` regardless of what subspace its V-spans occupy.

---

### `acceptablevsa` Is a Stub — `do2.c:110–113`

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

The one gate that could reject the destination VSA is unconditionally open. Nothing here and nothing in any caller restricts which V-addresses may be targets.

---

### `specset2ispanset` — `do2.c:14–46`

For a `VSPECID` specset, the function calls:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```
[do2.c:35–36]

No span value is inspected before this call. The raw vspanset — whatever subspace its tumblers fall in — is handed to `vspanset2ispanset`.

---

### `vspanset2ispanset` → `permute` — `orglinks.c:397–422`

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);   // [401]
}
```

`permute` simply walks the restriction spanset and dispatches each span to `span2spanset`:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {     // [414]
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset, ...);      // [415]
}
```

Neither function tests `restrictionspanset->stream.mantissa[0]` or any other tumbler component for subspace membership. V-spans from the link subspace (mantissa[0] == 1 for a link crum, or reaching into V ≥ 2.0) are processed identically to content spans.

---

### `insertspanf` — `spanf1.c:15–54`

```c
for (; sporglset; sporglset = ...) {
    if      (itemid == ISPANID)  { unpack stream/width from ispan ...   }  // [26–29]
    else if (itemid == SPORGLID) { unpack stream/width from sporgl ...  }  // [30–33]
    else if (itemid == TEXTID)   { build stream/width from text ...     }  // [34–42]
    else gerror("insertspanf - bad itemid");

    insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // [51]
}
```

The switch dispatches on item type, not on tumbler subspace. An ispan whose stream lands in the link V-region is inserted into the spanfilade with no objection.

---

### Where Subspace Structure Is Defined

The code _does_ define and use link-vs-content subspace in other contexts:

**`findvsatoappend` — `orglinks.c:31–49`** sets the link subspace start:
```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);   // [37] — linkspacevstart = 2.0
```
New text is appended below V = 2.0; links are placed at V ≥ 2.0. This is a write-time placement convention, not a read-time restriction on `docopy`.

**`findnextlinkvsa` — `do2.c:151–167`** places link references starting at V = 2.1:
```c
tumblerincrement (&firstlink, 0, 2, &firstlink);   // [157] — 2.0
tumblerincrement (&firstlink, 1, 1, &firstlink);   // [158] — 2.1
```
And `domakelink` [do1.c:184] calls `docopy(taskptr, docisaptr, &linkvsa, ispanset)` with that VSA — proving that `docopy` is intentionally used _to insert link-subspace entries_. The `ispanset` there is an I-span (from `tumbler2spanset`) not a V-span, so no V→I conversion is needed, but the pattern confirms the design.

**`islinkcrum` — `orglinks.c:255–261`**:
```c
if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
    return TRUE;
```
Link crums are identified by mantissa shape, but this function is used only in `maxtextwid` [orglinks.c:240] (called from `retrievevspansetpm`) to _skip_ link crums during text-width computation — not to gate `docopy`.

---

### The Only Subspace Filter — and Where It Is Not Used

`filter_vspanset_to_text_subspace` [do1.c:386–411] is the codebase's sole filter that drops spans with V < 1.0. It is called exclusively by `doshowrelationof2versions` [do1.c:440–441], added as an explicit semantic fix (comment: "Bug 009 SEMANTIC FIX"). It is **not called by `docopy`**, `specset2ispanset`, `vspanset2ispanset`, or `insertspanf`.

---

### Conclusion

`docopy` (and the entire `specset2ispanset` / `insertspanf` pipeline) **accepts source spans from any subspace**, including the link subspace. There is no guard at the specset input, no check inside `vspanset2ispanset` or `permute`, and `acceptablevsa` is an unconditional stub. The subspace separation (content below V = 2.0, links at V ≥ 2.0) is a placement convention enforced only at _write time_ by `findvsatoappend` and `findnextlinkvsa`, and at _compare time_ by the `filter_vspanset_to_text_subspace` fix in `doshowrelationof2versions`. `docopy` itself has no such restriction.
