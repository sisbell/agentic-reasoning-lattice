## Question 13 [evidence]

> When a matching endset only partially overlaps the queried region, does the operation return the endset's full I-span or only the sub-span that intersects the region?

## KB Synthesis

The KB gives a clear answer for **FOLLOWLINK** but is ambiguous for **RETRIEVEENDSETS**.

## FOLLOWLINK: Always returns the full endset

[SS-FOLLOW-LINK] is explicit: `follow_link` returns the **complete, original SpecSet** regardless of how the link was discovered. Even if found via a 4-character partial overlap with a 14-character source, `follow_link` returns the full 14-character endpoint. This is a direct consequence of reading from the link orgl, not the spanfilade.

## RETRIEVEENDSETS: Architecture implies intersection only

[SS-RETRIEVE-ENDSETS] describes a fundamentally different mechanism: it searches the spanfilade using a **SPANRANGE restriction** derived from the query's I-addresses. The spanfilade stores sporgls (contiguous I-address runs) indexed by I-address. The search finds sporgls whose I-addresses fall within the query range — implying only the **matching sub-span** is returned, not the full endset.

This is reinforced by the comparison table in [SS-RETRIEVE-ENDSETS]: FOLLOWLINK returns endsets from "the link's perspective"; RETRIEVEENDSETS returns them from "the querying document's perspective."

## What the KB doesn't answer

No finding directly tests RETRIEVEENDSETS with a partial-overlap case and shows which sub-span is returned. The architectural inference (intersection only) is reasonable but not empirically confirmed in the KB. If you need certainty here, a targeted scenario test is warranted.

---

## Code Exploration

Now I have everything I need. Let me compile the complete, code-cited answer.

---

## Answer: Full I-span is returned for endsets; clipping occurs only in the POOM V→I layer

There are two distinct retrieval paths. They behave differently with respect to partial overlap.

---

### Path A: Spanfilade endset retrieval — returns the **full I-span**

The endset retrieval path is:

```
doretrieveendsets (do1.c:369)
  → retrieveendsetsfromspanf (spanf1.c:190)
    → retrievesporglsetinrange (spanf1.c:237)
      → retrieverestricted (retrie.c:56)
        → retrieveinarea → findcbcinarea2d (retrie.c:229)
          → crumqualifies2d (retrie.c:270)        [overlap test]
          → makecontextfromcbc (context.c:151)    [full crum into context]
      → contextintosporgl (sporgl.c:205)          [context → sporgl, no clip]
```

**`crumqualifies2d` accepts partial overlap** (`retrie.c:270-305`). It returns `TRUE` whenever the crum's extent overlaps the query range in both dimensions — there is no requirement for full containment:

```c
// retrie.c:282-290
endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
if ( endcmp <=/*=*/ ONMYLEFTBORDER){
    return(FALSE);
}
startcmp = whereoncrum (crumptr, offset, span1start, index1);
 if( (startcmp > THRUME /*&& endcmp > THRUME*/)){
    return (FALSE);
 }
```

A crum is **rejected** only if the query end is at or left of the crum's left border, or if the query start is right of the crum's right border. Any partial overlap qualifies.

Once a crum qualifies, **`makecontextfromcbc`** builds the context from the crum's full extent (`context.c:160-161`):

```c
movewisp(offsetptr, &context->totaloffset);
movewisp(&crumptr->cwid, &context->contextwid);  // full crum width, unclipped
```

Then **`contextintosporgl`** copies the full width directly (`sporgl.c:205-220`):

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);  // full crum start
    ...
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);    // full crum width
}
```

**No clipping.** The sporgl gets `contextwid.dsas[SPANRANGE]` — the whole crum's I-span — regardless of how much of it overlaps the query.

This same unclipped behavior appears in `link2sporglset` (`sporgl.c:83-88`) and `sporglset2linksetinrange` (`sporgl.c:263-264`), which also extract the full context and do not intersect it with the query bounds.

---

### Path B: POOM V→I conversion — returns the **clipped sub-I-span**

The V-to-I translation path is:

```
vspanset2ispanset (orglinks.c:397)
  → permute (orglinks.c:404)
    → span2spanset (orglinks.c:425)
      → retrieverestricted → findcbcinarea2d → crumqualifies2d  [same overlap test]
      → context2span (context.c:176)                             [clips output]
```

**`context2span`** explicitly clips the target-dimension span to the intersection (`context.c:176-212`):

```c
// context.c:191-207
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
    // crum start precedes query start: advance the I-start by the overhang
    tumblerincrement (&grasp.dsas[idx2], 0,
        (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]),
        &grasp.dsas[idx2]);
}
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER) {
    // crum end exceeds query end: retreat the I-end by the overhang
    tumblerincrement (&reach.dsas[idx2], 0,
        -tumblerintdiff(&reach.dsas[idx1], &upperbound),
        &reach.dsas[idx2]);
}
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

The logic: if the POOM crum overhangs the query's V-start by Δ characters, the returned I-start is pushed forward by Δ; if it overhangs the V-end, the returned I-end is pulled back by the same amount. This assumes a unit-ratio bijection within each POOM crum. The result is a **sub-I-span** corresponding exactly to the queried V-sub-span.

---

### Summary

| Operation | Partial overlap detected by | Output when partially overlapping |
|---|---|---|
| Spanfilade endset retrieval (`retrievesporglsetinrange`, `contextintosporgl`) | `crumqualifies2d` (retrie.c:270) | **Full I-span** of the matching crum (sporgl.c:211,219) |
| POOM V→I conversion (`span2spanset`, `context2span`) | `crumqualifies2d` (retrie.c:270) | **Clipped sub-I-span** proportional to V-overlap (context.c:191-207) |

The endset I-span returned by the spanfilade path is **always the full stored crum extent**. Clipping is a property of the POOM permutation layer (`context2span`), not of the spanfilade endset layer (`contextintosporgl`). A spanfilade endset crum is atomic — it is returned whole or not at all.
