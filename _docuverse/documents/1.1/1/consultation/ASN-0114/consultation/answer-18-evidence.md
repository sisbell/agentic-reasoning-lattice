## Question 18 [evidence]

> Does requesting one endset by selector read or expose any I-addresses belonging to the other two endsets (the non-selected source/target/type), or is access strictly confined to the selected position?

## KB Synthesis

Access is strictly confined to the selected endset position. The KB supports this from two angles depending on which operation is used.

**FOLLOWLINK** reads the link orgl directly via `link2sporglset()` (`sporgl.c:67-95`), which calls `retrieverestricted()` with the specific position `whichend` ∈ {0.1, 0.2, 0.3} for FROM, TO, and TYPE respectively [SS-FOLLOWLINK]. The `retrieverestricted()` function performs a range-bounded I-space lookup, so a request for position 0.1 (SOURCE) only fetches I-addresses stored at that orgl subrange — the TO (0.2) and TYPE (0.3) subranges are not traversed.

**RETRIEVEENDSETS** works through the spanfilade rather than the link orgl directly, using separate ORGLRANGE prefix constants — LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3 — as dimension restrictions [SS-RETRIEVE-ENDSETS]. Each endset type is searched independently via its own `retrievesporglsetinrange()` call. The TYPE endset is explicitly noted as "conditionally retrieved (only if requested)."

In both cases the selector parameter maps to a distinct I-address subrange within the link's storage, and the range-restriction mechanism of the enfilade lookup ensures no cross-endset I-addresses are read or returned. The three endsets are structurally isolated by their orgl-dimension positions, not merely filtered post-retrieval.

---

## Code Exploration

I now have everything needed from the actual source. Here is the complete verified answer.

---

## Does requesting one endset by selector read or expose I-addresses from the other two?

**No. Access is strictly confined to the selected V-position. The other two endsets are not accessed.**

---

### The complete call chain, with verified line citations

#### 1. FEBE handler — `fns.c:114-127`

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;
  INT whichend;
  bool getfollowlink(), dofollowlink();

    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
      }else
        putrequestfailed (taskptr);
}
```

`whichend` is decoded from the wire as an integer. It is passed **without modification** to `dofollowlink`.

---

#### 2. Dispatch — `do1.c:223-232`

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
}
```

`whichend` is forwarded unchanged into `link2sporglset`. No loop. No expansion to other endsets.

---

#### 3. The selector becomes a one-slot V-span — `sporgl.c:67-95`

This is the decisive function:

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  typeorgl orgl;
  tumbler zero;
  typevspan vspan;
  typecontext *context, *c, *retrieverestricted();
  typesporgl *sporglptr;
  INT *taskalloc();
  bool findorgl();

    if (!findorgl (taskptr, granf, linkisa, &orgl, type)){
        return (FALSE);
    }
    tumblerclear (&zero);
    tumblerincrement (&zero, 0, whichend, &vspan.stream);   // line 81: V-start = whichend
    tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);      // line 82: V-width = 1
    if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
        for (c = context; c; c = c->nextcontext) {
            sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
            contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
            ...
        }
        contextfree (context);
        return (TRUE);
    } else{
        return (FALSE);
    }
}
```

Two facts established here:

- **`sporgl.c:81-82`** — `vspan.stream = whichend`, `vspan.width = 1`. The V-span is exactly one slot wide, positioned at `whichend`. Selectors 1, 2, 3 map to LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN (`xanadu.h:36-38`).

- **`sporgl.c:83`** — `retrieverestricted(orgl, &vspan, V, NULL, I, NULL)`. The first span/index pair `(&vspan, V)` constrains the V-dimension to `[whichend, whichend+1)`. The second pair `(NULL, I)` places **no** constraint on the I-dimension, so all I-addresses within that one V-slot are returned.

---

#### 4. The retrieval engine enforces the constraint — `retrie.c:56-76`

```c
typecontext *retrieverestricted(typecuc *fullcrumptr, typespan *span1ptr, INT index1,
                                 typespan *span2ptr, INT index2, typeisa *docisaptr)
{
  tumbler span1start, span1end, span2start, span2end;
  ...
    if (span1ptr) {
        movetumbler (&span1ptr->stream, &span1start);
        tumbleradd (&span1start, &span1ptr->width, &span1end);   // end = start + width
    } else {
        tumblerclear (&span1start);
        tumblerclear (&span1end);
    }
    ...
```

`span1start = whichend`, `span1end = whichend + 1`. The retrieval traversal in the 2D enfilade is bounded to that closed interval in the V-dimension. Nodes outside it are never visited.

---

#### 5. I-addresses extracted only from the matching slot — `sporgl.c:205-220`

```c
int contextintosporgl(type2dcontext *context, tumbler *linkid, typesporgl *sporglptr, INT index)
{
    sporglptr->itemid = SPORGLID;
    sporglptr->next = NULL;
    movetumbler(&context->context2dinfo.homedoc, &sporglptr->sporgladdress);
    movetumbler(&context->totaloffset.dsas[index], &sporglptr->sporglorigin);  // line 211
    ...
    movetumbler(&context->contextwid.dsas[index], &sporglptr->sporglwidth);    // line 219
}
```

Called as `contextintosporgl(..., I)` (`sporgl.c:86`), where `I=0` (`wisp.h:19`). Only the I-dimension of the context is extracted into the sporgl. The V-dimension coordinate is never read out.

---

#### 6. Dimensional constants — `wisp.h:15-20`

```c
/* wid and dsp indexes for sp */
#define ORGLRANGE 0
#define SPANRANGE 1

/* wid and dsp indexes for pm */
#define I  0
#define V  1
```

The link orgl is a 2D enfilade (pm). Dimension 0 (I) carries I-addresses; dimension 1 (V) carries endset type. These are structurally separate axes.

---

#### 7. The "all three" path is a different operation entirely

`doretrieveendsets` (`do1.c:369-374`) calls `retrieveendsetsfromspanf` (`spanf1.c:190`), which issues three separate `retrievesporglsetinrange` calls, each with a distinct one-slot V-span:

```c
fromspace.stream.mantissa[0] = LINKFROMSPAN;    // spanf1.c:210
fromspace.width.mantissa[0] = 1;
tospace.stream.mantissa[0]  = LINKTOSPAN;       // spanf1.c:213
tospace.width.mantissa[0]   = 1;
threespace.stream.mantissa[0] = LINKTHREESPAN;  // spanf1.c:216
threespace.width.mantissa[0] = 1;
```

This path is never triggered by a `followlink` request. `dofollowlink` goes through `link2sporglset` only, and `link2sporglset` builds exactly one V-span for the one requested endset.

---

### Conclusion

Access is **strictly confined** to the selected V-position. The architectural guarantee is:

1. `link2sporglset` constructs a V-span of **width=1** at position `whichend` (`sporgl.c:81-82`).
2. `retrieverestricted` bounds its enfilade traversal to that exact interval in the V-dimension (`retrie.c:56-76`).
3. No loop over all three selectors exists anywhere in the `dofollowlink` → `link2sporglset` path.
4. The I-addresses of the non-selected endsets live at different V-slots (1, 2, 3 for from/to/three per `xanadu.h:36-38`) and are never visited by that traversal.

The three endsets are physically co-resident in the same link orgl, but the enfilade's 2D structure and the one-slot-wide V-span query guarantee that requesting endset N cannot expose the content of endsets at N±k.
