## Question 11 [evidence]

> When a link orgl is read by its own I-address (docISA.0.2.N), are all three endsets returned as raw I-address spans, or are they converted to V-addresses during the read?

## KB Synthesis

When a link orgl is read by its I-address, the endsets are returned as **raw I-address spans** — no V-address conversion occurs during the orgl read itself.

The process is explicitly two-phase, as documented in [SS-FOLLOWLINK] (Finding 0048):

**Phase 1 — Raw I-space read:**  
`link2sporglset()` extracts the endsets at position 0.1, 0.2, or 0.3 via `retrieverestricted()` against the link orgl. At this stage, no POOM check occurs. The result is a sporglset: each entry carries an I-address origin, a width, and a source-doc ISA, but no V-addresses.

**Phase 2 — Optional V-address conversion:**  
`linksporglset2specset()` then maps those I-addresses to V-addresses by looking them up in a caller-specified `homedoc`'s POOM. If an I-address has no current POOM mapping in that document, it is silently dropped ([INV-ITOV-FILTERING]).

This means FOLLOWLINK's postcondition `follow_link(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }` is document-relative — the same link orgl can yield different V-address results (or empty results) depending on which `homedoc` POOM is used for resolution.

All three endsets (FROM at 0.1, TO at 0.2, THREE at 0.3) follow this same pattern. The link orgl itself holds permanent I-address data; V-addresses are an ephemeral view derived from whichever document's POOM the caller provides.

---

## Code Exploration

I now have all the evidence. Let me compile the complete answer.

---

## When a Link Orgl Is Read by Its I-Address: Are Endsets Returned as I-Spans or V-Addresses?

**Short answer:** The endsets go through a **conditional conversion** in `sporgl.c:105`. In the normal case (content in a real document), they are **converted to V-addresses**. There is a fallback path that returns raw I-address spans only when the internal `sporgladdress` field is zero.

---

### Call Chain

**1. Entry point — `fns.c:350`**

```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  if (
     getretrieveendsets (taskptr, &specset)
  && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)){
      putretrieveendsets (taskptr, fromset, toset, threeset);
  } else
      putrequestfailed (taskptr);
}
```

`doretrieveendsets` delegates directly to `retrieveendsetsfromspanf`.

---

**2. `retrieveendsetsfromspanf` — `spanf1.c:190`**

This is where all three endsets are assembled. The link's V-address specset is first converted to a sporglset (the internal spanfilade representation), then each endset is extracted:

```c
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)          // line 222
&& retrievesporglsetinrange(taskptr,sporglset,&fromspace,&fromsporglset)   // line 223
&& linksporglset2specset (taskptr,&((typevspec *)specset)->docisa,
                          fromsporglset, fromsetptr, NOBERTREQUIRED)       // line 224
&& retrievesporglsetinrange (taskptr, sporglset, &tospace, &tosporglset)   // line 225
&& linksporglset2specset (taskptr, &((typevspec*)specset)->docisa,
                          tosporglset, tosetptr, NOBERTREQUIRED)           // line 226
```

And for the typeset (threeset) at lines 230–231, the same pattern. The `fromspace`, `tospace`, `threespace` spans are fixed-ordinal I-coordinate regions (`LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` offsets at lines 210–217) inside the link's own I-space.

---

**3. THE BRANCH — `linksporglset2specset`, `sporgl.c:97`**

This is the critical decision point:

```c
bool linksporglset2specset(typetask *taskptr, typeisa *homedoc,
                            typesporglset sporglset, typespecset *specsetptr, int type)
{
  for (; sporglset; ...) {
    specset = (typespecset) taskalloc (taskptr, sizeof (typevspec));

    if (iszerotumbler (&((typesporgl *)sporglset)->sporgladdress)) {    // line 105
        // sporgladdress == 0: return raw I-span
        ((typeitemheader *)specset)->itemid = ISPANID;                   // line 112
        movetumbler(&sporglptr->sporglorigin, &((typeispan *)specset)->stream);
        movetumbler(&sporglptr->sporglwidth,  &((typeispan *)specset)->width);
    } else {
        // sporgladdress != 0: convert to V-address
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type); // line 116
    }
  }
}
```

`sporgladdress` is the ISA address of the document whose granfilade orgl maps the I-span to V-spans. For real link endsets pointing to actual document content, `sporgladdress` is non-zero, so the `else` branch fires and V-conversion proceeds.

---

**4. V-address conversion chain (non-zero `sporgladdress` path)**

**`linksporglset2vspec` — `sporgl.c:127`**

```c
specptr->itemid = VSPECID;                              // line 132 — marks output as V-spec
movetumbler (homedoc, &specptr->docisa);                // line 134
sporglset2vspanset (taskptr, homedoc, sporglsetptr,
                    &specptr->vspanset, type);           // line 136
```

**`sporglset2vspanset` — `sporgl.c:141`**

```c
findorgl (taskptr, granf, homedoc, &orgl, type);        // line 152 — find the orgl for this doc
ispan.itemid = ISPANID;
movetumbler (&sporglptr->sporglorigin, &ispan.stream);  // line 155
movetumbler (&sporglptr->sporglwidth,  &ispan.width);   // line 156
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);  // line 157
```

**`ispan2vspanset` — `orglinks.c:389`**

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl,
                              typeispan *ispanptr, typevspanset *vspansetptr)
{
  return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);  // line 393
}
```

`permute` is called with `I` as the restriction dimension and `V` as the target. Contrast with `vspanset2ispanset` at `orglinks.c:397–401`, which calls `permute(..., V, ..., I)` — the mirror function.

**`permute` — `orglinks.c:404`**

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);  // line 415
}
```

**`span2spanset` — `orglinks.c:425`**

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                             restrictionindex, (typespan*)NULL,
                             targindex, (typeisa*)NULL);    // line 435
for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex,
                  &foundspan, targindex);                   // line 443
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                      (typeitemset*)targspansetptr);  // line 444
}
```

The orgl is queried with the I-span as the restriction (`restrictionindex = I`) and the V-dimension as output (`targindex = V`).

**`context2span` — `context.c:176`**

```c
prologuecontextnd (context, &grasp, &reach);               // line 188
// clips grasp/reach to the restriction in dimension idx1 (I)
// then extracts idx2 (V) coordinates:
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);    // line 206
tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);  // line 207
foundspanptr->itemid = index2itemid (idx2, context);        // line 209
```

**`index2itemid` — `context.c:223`**

```c
case POOM :
    return (index == I ? ISPANID : VSPANID);   // line 227
```

When `idx2 = V`, this returns `VSPANID`. The output span is a V-address span.

---

### Summary

| Condition | `sporgladdress` | Result type | Where decided |
|-----------|-----------------|-------------|---------------|
| Normal: endset points to real document content | non-zero (doc ISA) | `VSPECID` containing `VSPANID` list — **V-addresses** | `sporgl.c:116` → `sporgl.c:132` |
| Abnormal/degenerate: no doc reference | zero | `ISPANID` — **raw I-address span** | `sporgl.c:112` |

For the normal case — a link whose endsets reference content in a document with a valid ISA address — the three endsets (`fromset`, `toset`, `typeset`) are **converted to V-addresses** during the read. The conversion goes through `ispan2vspanset` → `permute(I → V)` → `span2spanset` → `context2span`, extracting the V-dimension coordinates from the orgl contexts and returning `VSPECID` items with `VSPANID` vspansets.

The raw `ISPANID` path at `sporgl.c:112` fires only when `sporgladdress` is zero, which would indicate a degenerate or internally inconsistent link endset with no granfilade document reference.
