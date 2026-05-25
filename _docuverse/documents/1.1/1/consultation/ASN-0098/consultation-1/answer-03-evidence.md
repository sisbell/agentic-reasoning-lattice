## Question 3 [evidence]

> Does udanax-green implement projection as a uniform function, or are there separate code paths for endset-level vs. span-level vs. address-level projection?

## KB Synthesis

Projection in udanax-green has a **uniform core but differentiated wrapper paths** depending on the abstraction level.

## Uniform Core

`permute()` (`orglinks.c:389-422`) is the single primitive that handles V↔I conversion in both directions. It is explicitly type-agnostic — it does not distinguish permascroll I-addresses from link orgl ISAs, and operates identically regardless of which subspace the V-address falls in [SS-DUAL-ENFILADE Finding 0011, SS-LINK-ENDPOINT Finding 0009]. `retrieverestricted()` is the leaf-level lookup function shared across all paths [SS-FOLLOWLINK Finding 0048].

## Separate Wrapper Paths

**Span-level (document content):**
- V→I: `vspanset2ispanset()` → `permute()` → `span2spanset()` → `retrieverestricted()` [SS-VSPAN-TO-SPORGL Finding 0013]
- I→V: `ispan2vspanset()` → `permute()` with same chain; returns a *set* because the POOM is a multimap [SS-POOM-MULTIMAP Finding 0039]

**Endset-level via FOLLOWLINK:**
Two-phase: `link2sporglset()` calls `retrieverestricted()` directly against the link orgl in I-space (no POOM check), then `linksporglset2specset()` calls `span2spanset()` → `retrieverestricted()` against the home document's POOM for I→V. Unreferenced I-addresses are silently dropped at the second `span2spanset()` call [SS-FOLLOWLINK Finding 0048, INV-ITOV-FILTERING Finding 0048].

**Endset-level via RETRIEVEENDSETS:**
Searches the spanfilade rather than reading a known link orgl: `specset2sporglset()` converts V→I (same `permute()` path), then `retrievesporglsetinrange()` searches the spanf with dual ORGLRANGE/SPANRANGE restrictions, then `linksporglset2specset()` resolves I→V via the *querying document's* docid — not the link's home document [SS-RETRIEVE-ENDSETS Finding 0035, INT-SPORGL-LINK-INDEX Finding 0035].

## Key Structural Observation

The sporgl layer ([SS-SPORGL Finding 0013]) is the differentiator: endset paths add provenance tracking (`sporgladdress` = source document ISA) on top of the same `permute()` core. Span-level projection uses bare I-spans (no provenance). Address-level arithmetic (tumbler operations) is orthogonal — it's not projection but coordinate manipulation used *before* projection [SS-TWO-BLADE-KNIFE Finding 0054].

The type-agnosticism of `permute()` is what makes the subspace invariant a caller-enforced convention rather than a storage guarantee [INV-SUBSPACE-CONVENTION, PRE-COMPARE-VERSIONS Finding 0015].

---

## Code Exploration

---

## Projection in udanax-green: A Single Uniform Algorithm

**The answer is: projection is implemented as a single, dimension-parametric algorithm. There are no separate code paths for endset-level, span-level, or address-level projection.**

---

### The Core: `permute()`

`backend/orglinks.c:404` is the universal projection dispatcher:

```c
typespanset *permute(typetask *taskptr, typeorgl orgl,
                     typespanset restrictionspanset, INT restrictionindex,
                     typespanset *targspansetptr, INT targindex)
```

It takes the source dimension as `restrictionindex` (I or V) and the target dimension as `targindex` (V or I). Its entire body is a loop over input spans with no branching on object type:

```c
// orglinks.c:414-416
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
```

### The Two Public Wrappers

Both V→I and I→V projection are trivial one-liners that differ only in which argument they pass as `I` vs `V`:

```c
// orglinks.c:389-394
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}

// orglinks.c:397-402
typeispanset *vspanset2ispanset(...) {
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

There is no `project_endset()`, no `project_address()`, no type-level switch anywhere in this path.

### Per-Span Worker: `span2spanset()`

`backend/orglinks.c:425` handles a single span from the input set:

1. **Query the orgl** via `retrieverestricted()` — finds all contexts that overlap the restriction span along `restrictionindex` (`orglinks.c:435`)
2. **Loop over returned contexts** — for each one, call `context2span()` to compute the projected span (`orglinks.c:439-444`)

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
}
```

Again: no branching on span granularity.

### The Math: `context2span()`

`backend/context.c:176` performs the actual coordinate transformation:

```c
int context2span(typecontext *context, typespan *restrictionspanptr,
                 INT idx1, typespan *foundspanptr, INT idx2)
```

The algorithm (`context.c:186-209`):
1. Extract lower/upper bounds from the restriction span (`context.c:186-187`)
2. Get the context's grasp and reach in both dimensions via `prologuecontextnd()` (`context.c:188`)
3. Clamp grasp upward if it falls below the restriction lower bound (`context.c:191-195`)
4. Clamp reach downward if it extends past the restriction upper bound (`context.c:197-201`)
5. Write clamped `grasp[idx2]` → `foundspan.stream` and `reach[idx2]-grasp[idx2]` → `foundspan.width` (`context.c:206-207`)
6. Assign `itemid` dynamically via `index2itemid(idx2, context)` (`context.c:209`)

The only type-conditional logic in the entire chain lives here, in `index2itemid()` at `context.c:223`:

```c
INT index2itemid(INT index, typecontext *context) {
    switch (context->contexttype) {
      case POOM: return (index == I ? ISPANID : VSPANID);
      case SPAN: return (ISPANID);
      default:   gerror("index2itemid bad enftype");
    }
}
```

This assigns the correct span type tag (`ISPANID` vs `VSPANID`) based on the enfilade type (POOM = 2D orgl with both I and V dimensions; SPAN = 1D). It does **not** distinguish endset-level from address-level — those distinctions don't exist at this layer. All spans, regardless of their semantic granularity, are geometrically identical `typespan` structs with a `stream` (start tumbler) and `width`.

### The Retrieval Engine: `retrieverestricted()`

`backend/retrie.c:56` accepts two dimension parameters (`index1`, `index2`) and passes them straight through to the 2D rectangle walk in the enfilade tree. No level-specific paths exist there either.

---

### Call Chain Summary

```
vspanset2ispanset()     orglinks.c:397  — public API, passes (V → I)
ispan2vspanset()        orglinks.c:389  — public API, passes (I → V)
  └─ permute()          orglinks.c:404  — loops over input spans
       └─ span2spanset() orglinks.c:425  — projects one span
            ├─ retrieverestricted()  retrie.c:56   — 2D enfilade query
            └─ context2span()        context.c:176 — coordinate clamp + assignment
                 └─ index2itemid()   context.c:223 — only type branch (POOM/SPAN)
```

---

### Conclusion

Projection in udanax-green is **one uniform algorithm parametric on dimension index**. The design insight is that a span in I-space and a span in V-space are the same data structure — a tumbler start and a tumbler width — so the projection is pure arithmetic clamping (`context2span`) with the dimension slot selected by an integer index. Endset-level, span-level, and address-level distinctions are semantic layers above this; the enfilade doesn't know about them, and neither does the projection code.
