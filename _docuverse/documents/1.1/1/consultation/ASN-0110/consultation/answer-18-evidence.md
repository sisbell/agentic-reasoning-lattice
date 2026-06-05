## Question 18 [evidence]

> Given that `find_links` ignores the orgl range parameter (`TRUE||!homeset`), does the region-to-endset query likewise search the spanfilade globally rather than scoping to the queried document?

## KB Synthesis

Yes — based on the KB, RETRIEVEENDSETS also searches the spanfilade globally, though for a structurally different reason than the `TRUE||!homeset` bug.

## How RETRIEVEENDSETS searches the spanfilade

From [SS-RETRIEVE-ENDSETS] and [INT-SPORGL-LINK-INDEX] (Finding 0035), the call chain is:

```
retrieveendsetsfromspanf() 
  → V-to-I conversion (sporglset)
  → retrievesporglsetinrange() with:
      SPANRANGE = I-addresses from input specset
      ORGLRANGE = endset-type prefix (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3)
```

The ORGLRANGE restriction in RETRIEVEENDSETS is used to partition the three endset types, **not** to scope results to a specific document. There is no document-address bound applied during the spanfilade search itself.

## Difference from `find_links`'s bug

The `TRUE||!homeset` bug ([EC-FIND-LINKS-GLOBAL]) is specific to `sporglset2linkset()`, which `findlinksfromtothreesp()` calls. RETRIEVEENDSETS uses a separate function `retrievesporglsetinrange()`. However, that function's ORGLRANGE is fixed to endset-type constants — it was never designed to carry a document-scope bound.

## Implication

Document scoping in RETRIEVEENDSETS is applied only at the *result-conversion stage*: `linksporglset2specset()` resolves I-addresses back to V-positions using the querying document's POOM. This is why [INT-LINK-VERSION] Finding 0019 observes that endsets "report the version's docid rather than the original's" — the filtering is POOM-based (I→V conversion), not spanfilade-based.

The spanfilade search itself is global across all documents in both operations. The practical effect matches [INT-LINK-TRANSCLUSION] and [INV-LINK-GLOBAL-VISIBILITY]: any document sharing I-addresses (via transclusion or versioning) will have its links surface in RETRIEVEENDSETS results, regardless of which document initiated the query.

The KB does not confirm whether `retrievesporglsetinrange()` has its own analogous bug, but structurally it was not designed to carry document-scope bounds — those were only ever present as a parameter in the `find_links` path.

---

## Code Exploration

I now have all the code I need. Let me compile the answer.

---

## Answer

### Short answer

Yes. The region-to-endset query (`retrieve_endsets`) also searches the spanfilade globally — it is not scoped to the queried document — but for a structurally different reason than `find_links`.

---

### The `find_links` global bypass (known context)

`fns.c:198` discards the client-supplied `homeset` before it ever reaches the spanfilade:

```c
// fns.c:198
dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                        (typeispan*)NULL/*homeset*/,   // ← homeset silently dropped
                        &linkset)
```

The NULL propagates through `do1.c:348–353` → `spanf1.c:77,85,93` into `sporglset2linkset`, where the orglrange parameter is unconditionally overridden:

```c
// sporgl.c:222–237
int sporglset2linkset(... typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;
    *linksetptr = NULL;
    if (TRUE||!homeset) {           // ← always true; homeset ignored
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;  // synthetic range [0, 100)
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next)
        sporglset2linksetinrange(..., homeset, spantype);
}
```

`sporglset2linksetinrange` [sporgl.c:257–259] then builds a spanfilade query with ORGLRANGE = `prefixtumbler(0, spantype)` to `+prefixtumbler(100, 0)` — a sweep across effectively all document ISAs at the given endpoint type.

---

### The `retrieve_endsets` path

Entry: `fns.c:350–362` → `do1.c:369–374` → `spanf1.c:190–235`.

`retrieveendsetsfromspanf` [spanf1.c:206–217] builds fixed endpoint-type spans:

```c
// spanf1.c:210–217
fromspace.stream.mantissa[0] = LINKFROMSPAN;   // 1  (xanadu.h:36)
fromspace.width.mantissa[0]  = 1;

tospace.stream.mantissa[0]   = LINKTOSPAN;     // 2  (xanadu.h:37)
tospace.width.mantissa[0]    = 1;

threespace.stream.mantissa[0] = LINKTHREESPAN; // 3  (xanadu.h:38)
threespace.width.mantissa[0]  = 1;
```

These are passed to `retrievesporglsetinrange` [spanf1.c:237–267], which calls `retrieverestricted` for each sporgl in the set:

```c
// spanf1.c:245
context = retrieverestricted(
    (typecuc*)spanf,
    (typespan*)sporglptr,   // SPANRANGE — queried permascroll range
    SPANRANGE,
    whichspace,             // ORGLRANGE — endpoint type only
    ORGLRANGE,
    (typeisa*)NULL          // ← no homedoc restriction
    /*kluge to make links show thru to version &sporglptr->sporgladdress*/
);
```

The `NULL` as `docisaptr` flows into `retrieverestricted` [retrie.c:56–85]:

```c
// retrie.c:77–82
if (docisaptr) {
    movetumbler(docisaptr, &info.homedoc);
    infoptr = &info;
} else {
    infoptr = NULL;         // ← taken; no bottom-crum homedoc filter
}
```

`infoptr = NULL` means `findcbcinarea2d` [retrie.c:229–268] skips the homedoc equality check entirely:

```c
// retrie.c:274
if ((crumptr->height == 0) && infoptr &&
    !tumblereq(&infoptr->homedoc, &(((type2dcbc *)crumptr)->c2dinfo.homedoc)))
        return (FALSE);    // ← never reached when infoptr == NULL
```

The ORGLRANGE window is `[LINKFROMSPAN, LINKFROMSPAN+1)` = `[1.0, 2.0)`, which spans **all** link ISAs of the from type. There is no restriction to the queried document's own ISA.

---

### Comparison

| | `find_links` | `retrieve_endsets` |
|---|---|---|
| SPANRANGE scope | queried content's permascroll addresses | queried content's permascroll addresses |
| ORGLRANGE scope | `[spantype.0, spantype.100)` via `nullhomeset` | `[spantype.0, (spantype+1).0)` via `whichspace` width=1 |
| Homedoc filter | None (`infoptr=NULL` in `sporglset2linksetinrange`) | None (`infoptr=NULL` in `retrievesporglsetinrange`) |
| Why global | `TRUE||!homeset` dead bypass [sporgl.c:227] | Intentional: comment says "kluge to make links show thru to version" [spanf1.c:245] |

**Both paths are global in the same sense**: they find any link in the spanfilade — from *any* document — whose endpoint overlaps the queried permascroll range. Neither restricts to links owned by the queried document.

The architectural difference is intent: `find_links`'s global behaviour is an unreachable-code artifact (the `orglrange` parameter was designed to scope by document but is hardcoded to NULL at `fns.c:198` and then immediately overwritten by `TRUE||...` at `sporgl.c:227`). `retrieve_endsets`'s global behaviour is deliberate — the comment at `spanf1.c:245` names it a "kluge to make links show thru to version", meaning cross-version link visibility was an explicit design goal that required dropping the homedoc restriction.
