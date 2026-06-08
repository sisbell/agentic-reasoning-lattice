## Question 1 [evidence]

> Can a link be allocated with `origin(ℓ) = d` and never appear in `d`'s link-subspace arrangement, or does the back end couple link creation to arrangement so that every home link of `d` is necessarily present in `M(d)`?

## KB Synthesis

## Answer

The back end **fully couples** link address allocation to arrangement insertion at creation time, but **does not guarantee** that coupling persists afterward.

### At Creation: Tight Coupling

`docreatelink` is a compound, sequenced operation [ST-CREATE-LINK, Finding 0012]:

1. `createorglingranf()` — allocates the link ISA under `d`'s address space, establishing `origin(ℓ) = d`
2. `findnextlinkvsa()` — computes the next available `2.x` V-position in `d`'s POOM
3. `docopy()` → `insertpm()` — inserts the ISA into M(d) at that position

There is no code path through `docreatelink` where step 1 executes without steps 2–3. Every newly created link with `origin(ℓ) = d` is necessarily in M(d) immediately after creation [SS-LINK-SUBSPACE, SS-THREE-LAYER-MODEL].

### Post-Creation: Coupling Can Be Severed

`DELETEVSPAN(2.x)` on the home document removes ℓ from M(d) while leaving the link orgl fully intact in I-space and the spanfilade [PRE-DELETE, Finding 0040]:

> `DELETEVSPAN` accepts link subspace addresses as valid targets. The only precondition enforced is non-zero width. No operation removes from I-space or spanfilade.

This produces the **reverse-orphan** state [EC-REVERSE-ORPHAN]: `origin(ℓ) = d` but `ℓ ∉ M(d)`. The link remains discoverable via `find_links` (spanfilade intact) and followable via its ISA directly, but `retrieve_vspanset(d)` shows no link span.

### Summary

| Moment | `origin(ℓ) = d` | `ℓ ∈ M(d)` |
|--------|----------------|------------|
| After `CREATELINK` | Yes | Yes (coupled by construction) |
| After `DELETEVSPAN(2.x)` on `d` | Yes | No (reverse orphan) |

So: a link cannot be **created** with `origin(ℓ) = d` without appearing in M(d), but it can **subsequently** be removed from M(d) while retaining its home document address. The coupling holds at allocation time but not as a persistent invariant.

---

## Code Exploration

I now have all the source verified. Here is the complete answer.

---

## Can a link with origin(ℓ) = d escape d's link-subspace arrangement?

**Short answer: The backend design couples them tightly, but two implementation gaps can decouple allocation from spanfilade presence.**

---

### The Coupling Path

`createlink` in `backend/fns.c:100–112` is the entry point. It calls `docreatelink` and only fires `putcreatelink` (the success response) if `docreatelink` returns `TRUE`:

```c
// fns.c:106–111
if (
   getcreatelink (taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
&& docreatelink (taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa)){
    putcreatelink (taskptr, &linkisa);
}else
    putrequestfailed (taskptr);
```

`docreatelink` is a single `&&`-chained return across seven steps (`do1.c:208–220`):

```c
// do1.c:208–220
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)           // (1) allocate link ISA in granfilade
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)                // (2) make I-span from link ISA
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)                  // (3) find d's next link VSA
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)                 // (4) insert link into d's V-space
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)    // (5) fetch link's orgl
  && specset2sporglset (...)                                         // (6a,6b,6c) convert endpoint specsets
  && setlinkvsas (...)
  && insertendsetsinorgl (...)                                       // (6) record endpoints in granfilade
  && insertendsetsinspanf (taskptr, spanf, linkisaptr,               // (7) insert into spanfilade
                           fromsporglset, tosporglset, threesporglset)
);
```

The hint uses `docisaptr` as the home document: `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` at `do1.c:207`. This means the link's ISA is allocated under d's address namespace — its tumbler is a child of d's tumbler.

**Step 4 (`docopy`)** inserts the link's I-span into d's content enfilade. This is the canonical "the link exists in d" step. **Step 7 (`insertendsetsinspanf`)** inserts the link's endpoint coordinates into the global spanfilade, which is the arrangement that makes the link discoverable by endpoint content range. Both steps must return `TRUE` before the client receives the link ISA.

---

### Two Gaps That Can Decouple Allocation from Arrangement

#### Gap 1 — `insertspanf` returns `TRUE` unconditionally

`insertspanf` in `backend/spanf1.c:15–54` calls `insertnd` to write each spanfilade crum but ignores the result:

```c
// spanf1.c:49–53
        movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
        movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
     insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
}
return (TRUE);    // ← unconditional; insertnd failure is invisible
```

If `insertnd` fails without aborting (e.g., allocation exhaustion), `insertspanf` still returns `TRUE`, the && chain still succeeds, and `putcreatelink` fires. The link has a live ISA and is in d's V-space (step 4 already completed), but has **zero spanfilade entries**. It cannot be located by endpoint-based queries.

#### Gap 2 — Empty sporglset silently writes nothing

`insertspanf` loops over the sporglset input (`spanf1.c:25`):

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    // write crum
}
return (TRUE);
```

If `fromsporglset` or `tosporglset` is `NULL` (possible if `specset2sporglset` returns an empty set for an empty endpoint specset), the loop body never runs. `insertspanf` returns `TRUE`, `insertendsetsinspanf` (`do2.c:116–128`) sees no failure and returns `TRUE`, and `docreatelink` completes successfully. The link lives in d's V-space but has no spanfilade entries for the empty endpoint.

---

### What Structures Constitute M(d)?

The arrangement spans two structures:

| Structure | What it holds | When written | Escape possible? |
|-----------|---------------|--------------|-----------------|
| Content enfilade (d's V-space) | Link's I-span as virtual content of d | Step 4: `docopy` | No — step 4 is before step 7 in the && chain; if step 7 fails the transaction aborts but step 4 is already done. However, the client gets `putrequestfailed`, so it never learns the ISA |
| Spanfilade (global endpoint index) | Link ISA keyed by endpoint content ranges | Step 7: `insertendsetsinspanf` | Yes — via the two gaps above |

The spanfilade entry stores the link ISA in the ORGLRANGE dimension with key `prefixtumbler(linkisaptr, spantype, ...)` (`spanf1.c:22`). The home document field `linfo.homedoc` is set to `isaptr` (the link's ISA) for `ISPANID` and `TEXTID` sporgl items (`spanf1.c:29, 42`), but to `sporgl->sporgladdress` for `SPORGLID` items (`spanf1.c:33`). This means `homedoc` is not uniformly the home document d — it is endpoint-specific provenance.

---

### Conclusion

The backend **intends tight coupling**: from the client's perspective, successful `createlink` implies the link is present in both d's V-space (via `docopy`, step 4) and the spanfilade (via `insertendsetsinspanf`, step 7), because the entire transaction is one atomic `&&` chain. If any step fails, the client sees `putrequestfailed` and never learns a link ISA.

However, two implementation gaps in `insertspanf` (`spanf1.c:51–53`) — the unconditional `return(TRUE)` after `insertnd`, and the loop-skip on null sporglsets — mean a link could in principle carry a live ISA under d while having **no spanfilade presence**. In that state it would be allocated with origin(ℓ) = d, accessible in d's V-space content enfilade, but invisible to the endpoint-indexed arrangement that constitutes the link-subspace search structure.

Under normal operating conditions (non-null endpoints, non-failing `insertnd`), every home link of d is necessarily present in M(d). The two escape routes are latent bugs, not intentional design.
