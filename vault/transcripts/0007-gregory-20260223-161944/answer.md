## KB Synthesis

# Answer: FOLLOWLINK Returns Partial Results

FOLLOWLINK returns **partial VSpecs** containing only the reachable portion of the endset. Unreferenced I-addresses are silently filtered during I-to-V conversion.

## Filtering Mechanism

The I-to-V conversion path filters at the individual I-address level via `span2spanset()` [INV-ITOV-FILTERING]:

> "At `span2spanset()`, `retrieverestricted()` searches the target document's POOM for the I-address. If not found (returns NULL), **the I-address is dropped from the result without error**."

This happens per-I-address, not per-endset. When `retrieverestricted` returns NULL for an I-address, that specific I-address contributes no V-span to the output, but processing continues for remaining I-addresses in the endset.

## Three Result Cases

[EC-GHOST-LINK] explicitly documents the partial-result case:

> "Three observable cases: 
> 1. all endset I-addresses live → full result
> 2. **some unreferenced → partial result, only live addresses converted**
> 3. all unreferenced → empty result `[]`, operation still succeeds"

Case (2) is the direct answer to your question: half-reachable produces a partial VSpec covering only the reachable half.

## Per-Sporgl Independence

[EC-LINK-PARTIAL-SURVIVAL] confirms this operates at the sporgl (I-span) level:

> "Because each I-span in a link endset independently tracks its content, partial survival is possible. If document A (source of "AA") is deleted but document B (source of "BB") remains, the link endset retains the I-span for "BB" while the I-span for "AA" becomes unresolvable. **The link survives partially — it still points to the "BB" content.**"

Each I-span's content identity is evaluated independently during resolution. Surviving I-spans contribute their V-addresses to the result; unreferenced I-spans are filtered out.

## Concrete Example

From [EC-GHOST-LINK]:

```
Link L has to-endset containing I-addresses α₁, α₂, α₃
Document D has poom.D(1.5) = α₂  (only α₂ is mapped)

FOLLOWLINK(L, TO, D) → VSpec covering position 1.5 only
                        (partial result: α₂ resolved, α₁ and α₃ filtered)
```

The operation succeeds with a partial VSpec. No error is raised. The caller receives whatever portion of the endset is currently reachable through the queried document's POOM.

## System-Level Consequence

This filtering behavior is a universal property of all I-to-V conversions in the system [INV-ITOV-FILTERING]:

> "**unreferenced I-addresses are silently excluded from V-address results**. No operation that performs I-to-V conversion will ever return a V-address for an unreferenced I-address."

FOLLOWLINK, RETRIEVEENDSETS, and all other operations using `linksporglset2specset()` share this filtering path and therefore share this partial-result behavior.

## Code Exploration

---

# Answer: FOLLOWLINK Returns Partial VSpec for Partially-Reachable Endsets

When FOLLOWLINK resolves a link's source endset to V-addresses and only half the endset's I-address range is currently referenced by any POOM, **it returns the reachable half as a partial VSpec**. The unreachable portions are silently omitted from the result.

## Call Chain Analysis

### 1. FOLLOWLINK Entry Point

The FOLLOWLINK handler calls `dofollowlink` [`fns.c:122-123`]:

```c
if (
   getfollowlink (taskptr, &linkisa, &whichend)
&& dofollowlink (taskptr, &linkisa, &specset, whichend)){
    putfollowlink (taskptr, specset);
```

### 2. Extract and Convert Endset

`dofollowlink` extracts the I-address endset from the link and converts it to V-addresses [`do1.c:223-232`]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

	return (
	   link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
	&& linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,/* ECH 6-29 READBERT */NOBERTREQUIRED));
}
```

### 3. Convert I→V via POOM

`linksporglset2specset` calls `linksporglset2vspec` for each sporgl [`sporgl.c:115-116`]:

```c
} else {
       linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
```

`linksporglset2vspec` initializes an empty vspanset and calls `sporglset2vspanset` [`sporgl.c:132-136`]:

```c
specptr->itemid = VSPECID;
specptr->next = NULL;
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
specptr->vspanset = NULL;
sporglset2vspanset (taskptr,homedoc, sporglsetptr, &specptr->vspanset,type);
```

### 4. The Critical Conversion: `span2spanset`

`sporglset2vspanset` calls `ispan2vspanset` which calls `permute`, which loops through each I-span and calls `span2spanset` [`orglinks.c:415`]. This is where partial resolution happens.

`span2spanset` calls `retrieverestricted` to find **all crums that intersect** the I-address range [`orglinks.c:425-454`]:

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr, INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  typespan foundspan;
  typespan *nextptr;
  typeitem *onitemlist();

	context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);

	for (c = context; c; c = c->nextcontext) {
		context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
		nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
	}
	if(!context){
		return(targspansetptr);
	}
		contextfree (context);
	return (&nextptr->next);
}
```

**Key observation at lines 446-448**: If `context` is NULL (no matches found), it returns `targspansetptr` unchanged. Since `vspanset` was initialized to NULL [`sporgl.c:135`], an empty result is returned.

**Key observation at lines 439-444**: If `context` is non-NULL, it loops through **each context** (representing each matching crum) and converts it to a V-span.

### 5. Partial Matching: `findcbcinarea2d`

`retrieverestricted` calls `retrieveinarea` which initializes `context = NULL` [`retrie.c:93`] and calls `findcbcinarea2d` [`retrie.c:97`].

`findcbcinarea2d` accumulates **only the portions that exist** [`retrie.c:229-268`]:

```c
int findcbcinarea2d(typecorecrum *crumptr, typedsp *offsetptr, tumbler *span1start, tumbler *span1end, INT index1, tumbler *span2start, tumbler *span2end, INT index2, typecontext **headptr, typebottomcruminfo *infoptr)
{
  typedsp localoffset;
  typecontext *context, *makecontextfromcbc();
  bool crumintersectsarea2d ();
  bool crumqualifies2d();

        for (; crumptr; crumptr = getrightbro (crumptr)) {
                if (!crumqualifies2d (crumptr, offsetptr, span1start, span1end, index1, span2start, span2end, index2, (type2dbottomcruminfo*)infoptr)){
                        continue;
                }
                if (crumptr->height != 0) {
                        dspadd (offsetptr, &crumptr->cdsp, &localoffset, (INT)crumptr->cenftype);
                        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, span1start, span1end, index1, span2start, span2end, index2, headptr, infoptr);
                } else {
                        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
                        incontextlistnd (headptr, context, index1);
                }
        }
}
```

**Line 252**: Iterates through ALL crums at this level.  
**Line 253-254**: If `crumqualifies2d` returns FALSE (crum doesn't intersect the search range), **skip it** with `continue`.  
**Line 262-263**: If the crum IS a leaf and qualifies, **add it to the context list**.

### 6. Intersection Test: `crumqualifies2d`

`crumqualifies2d` returns TRUE for **any crum that intersects the requested I-address range**, even if only partially [`retrie.c:270-305`]:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset, tumbler *span1start, tumbler *span1end, INT index1, tumbler *span2start, tumbler *span2end, INT index2, type2dbottomcruminfo *infoptr)
{
  INT startcmp, endcmp;

        endcmp = iszerotumbler (span1end) ? TOMYRIGHT : whereoncrum (crumptr, offset, span1end, index1);
	if ( endcmp <=/*=*/ ONMYLEFTBORDER){
		return(FALSE);
	}
        startcmp = whereoncrum (crumptr, offset, span1start, index1);
         if( (startcmp > THRUME /*&& endcmp > THRUME*/)){
                return (FALSE);
	 }
        // ... (similar checks for index2) ...
        return (TRUE);
}
```

**Lines 283-284**: If the requested range ends before the crum starts → FALSE.  
**Lines 287-289**: If the requested range starts after the crum ends → FALSE.  
**Line 304**: Otherwise → TRUE (crum intersects the range).

### 7. Clipping to Range: `context2span`

Each matching context is clipped to the restriction range and converted to V-address [`context.c:176-212`]:

```c
int context2span(typecontext *context, typespan *restrictionspanptr, INT idx1, typespan *foundspanptr, INT idx2)
{
  tumbler upperbound, lowerbound;
  typedsp grasp, reach;

	movetumbler (&restrictionspanptr->stream, &lowerbound);
	tumbleradd (&lowerbound, &restrictionspanptr->width, &upperbound);
	prologuecontextnd (context, &grasp, &reach);

	if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS) {
		tumblerincrement (&grasp.dsas[idx2], 0, (INT) tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
	}
	if (tumblercmp (&reach.dsas[idx1], &upperbound)  == GREATER) {
		tumblerincrement (&reach.dsas[idx2], 0,/*i=*/ - tumblerintdiff (&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);       
	}
	movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
	tumblersub(&reach.dsas[idx2],&grasp.dsas[idx2],&foundspanptr->width);
```

**Lines 191-196**: If the crum starts before the restriction, **clip the start** by adjusting the V-coordinate.  
**Lines 197-203**: If the crum extends beyond the restriction, **clip the end** by adjusting the V-coordinate.  
**Lines 206-207**: Extract the clipped V-span.

## Conclusion

When FOLLOWLINK encounters an endset where only part of the I-address range exists in the target document's POOM:

1. `findcbcinarea2d` iterates through ALL crums and collects **only those that intersect** the requested I-range
2. Each matching crum becomes a context
3. `context2span` clips each context to the restriction and extracts the corresponding V-span
4. **Result**: A VSpec containing only the reachable portions

**The unreachable portions are silently omitted.** There is no error, no indication to the client that the endset was partial. The result is simply a smaller vspanset than the original I-address endset would imply.

This is a **silent partial resolution** — FOLLOWLINK returns whatever it can find and ignores the rest.
