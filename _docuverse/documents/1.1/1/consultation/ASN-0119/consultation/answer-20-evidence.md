## Question 20 [evidence]

> When the rearranged content shares I-addresses with another document via transclusion, does [FC-DOC-ISOLATION] guarantee that document's POOM V-positions are wholly unaffected, since REARRANGE operates on a single `fullcrumptr`?

## KB Synthesis

Yes, the guarantee holds, and the KB gives several convergent reasons why.

**REARRANGE only mutates the target document's POOM**

[ST-REARRANGE] (Finding 0056) is explicit: `rearrangend()` calls `tumbleradd(&ptr->cdsp.dsas[index], &diff[i], &ptr->cdsp.dsas[index])` — it rewrites V-displacement values in-place on crums reached by traversing the target document's enfilade. No other document's tree is traversed or touched.

**Per-document POOM trees are separate structures**

[SS-POOM-MUTABILITY] (Finding 0072) establishes the three-layer model: the granfilade (I-space) is shared and append-only; each document has its own POOM. Since REARRANGE modifies only V-address displacements within one POOM tree, and another document's POOM is a disjoint data structure, there is no path for mutation to cross.

**The shared layer (granfilade) is untouched**

[FC-GRANF-ON-DELETE] (Finding 0061) categorises REARRANGE alongside DELETE as granfilade-preserving: neither calls any granfilade write function. [INV-REARRANGE-IDENTITY] (Findings 0016, 0018, 0056) confirms I-addresses are invariant under REARRANGE. The only shared mutable resource between documents is the granfilade, and REARRANGE leaves it unchanged.

**The pattern generalises from DELETE**

[FC-DELETE-CROSS-DOC] (Finding 0064) proves the same property for DELETE: "`deletend` operates on a single document's POOM tree only. Other documents' trees are separate data structures and are not touched." REARRANGE (`rearrangend`) follows the same code architecture — it receives a single document orgl and iterates only over crums within that tree.

**Conclusion**

A document T that transcludes I-addresses from the rearranged document D will have its POOM V-positions left wholly unchanged. The V-position shifts from REARRANGE are local to D's POOM; T's POOM independently maps those same I-addresses to T's own V-positions, which are untouched.

---

## Code Exploration

All citations verified. Here is the full answer.

---

## Does [FC-DOC-ISOLATION] Guarantee POOM V-Position Immunity Under Transclusion?

**Short answer: Yes, completely — and by structural necessity, not policy.**

The guarantee is not a contract someone wrote. It is a consequence of how the enfilade trees are wired in memory. Every piece of evidence below is read directly from source.

---

### 1. The Call Chain Accepts Exactly One Document

`rearrange` in `fns.c:159` decodes one `docisa`, passes it to `dorearrange` at `do1.c:34`:

```c
bool dorearrange(typetask *taskptr, typeisa *docisaptr, typecutseq *cutseqptr)
{
  typeorgl docorgl;
  bool findorgl(), rearrangepm();
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)   /* one doc */
    && rearrangepm (taskptr, docisaptr, docorgl, cutseqptr)
    );
}
```
`findorgl` returns a single `typeorgl` — one document's POOM root. That is passed to `rearrangepm` at `orglinks.c:137`:

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   /* one fullcrumptr */
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

One FEBE request → one `findorgl` call → one `fullcrumptr`. No second document pointer is ever loaded.

---

### 2. The Fullcrum Is a Hard Tree Boundary

The `isapex` bit in `enf.h:56` is defined on every crum type:

```c
struct structcuc {
    bool isapex BIT; /* TRUE if this is the fullcrum */
    ...
    typecorecrum *leftbroorfather;
                /* if it is NULL then this is fullcrum */
```

`isfullcrum` is a macro at `enf.h:176`:

```c
#define isfullcrum(x) ((bool)((typecorecrum *)(x))->isapex)
```

And `weakfindfather` at `common.h:195` reads:

```c
#define weakfindfather(x) ((typecuc *)(((!(((typecuc*)(x))->isapex)) && (((typecuc*)(x))->isleftmost)) \
    ? ((typecuc*)((typecuc*)(x))->leftbroorfather) \
    : (typecuc*)functionweakfindfather((typecuc*)(x))))
```

When `isapex == TRUE`, `leftbroorfather` is NULL. Every upward navigation function terminates here. There is no pointer that crosses from one document's apex into another document's tree.

---

### 3. `rearrangend` Only Touches Descendants of the Passed Root

The full kernel at `edit.c:78`:

```c
int rearrangend(typecuc *fullcrumptr, typecutseq *cutseqptr, INT index)
{
  ...
  makecutsnd (fullcrumptr, &knives);                          /* line 110 */
  newfindintersectionnd (fullcrumptr, &knives, &father, &foffset); /* line 111 */
  prologuend ((typecorecrum*)father, &foffset, &fgrasp, (typedsp*)NULL);
  for (ptr = (typecuc*)findleftson(father); ptr;              /* line 113 */
       ptr = (typecuc *)findrightbro((typecorecrum*)ptr)) {
      i = rearrangecutsectionnd((typecorecrum*)ptr, &fgrasp, &knives);
      switch (i) {
        case 1: case 2: case 3:
          tumbleradd (&ptr->cdsp.dsas[index], &diff[i],       /* line 125 */
                      &ptr->cdsp.dsas[index]);
          ivemodified((typecorecrum*)ptr);
          break;
      }
  }
  setwispupwards (father,1);                                  /* line 137 */
  recombine (fullcrumptr);                                    /* line 139 */
  (void)splitcrumupwards(fullcrumptr);                        /* line 141 */
}
```

Every operation — `makecutsnd`, `newfindintersectionnd`, the `findleftson`/`findrightbro` loop, `setwispupwards`, `recombine`, `splitcrumupwards` — receives only `fullcrumptr` or a node descended from it. No function takes a second document pointer. The V-offset mutation at line 125 writes to `ptr->cdsp.dsas[index]`, where `ptr` is a crum descended from the passed root.

---

### 4. `disown` Enforces the Fullcrum Wall With a Hard Error

At `genf.c:349`:

```c
int disown(typecorecrum *crumptr)
{
    if (isfullcrum(crumptr)){
        gerror("can't disownnomodify fullcrum\n");   /* genf.c:356 */
    }
    ...
    disownnomodify(crumptr);
    ivemodified((typecorecrum*)father);
}
```

`disown` is the only mechanism for detaching a crum from its parent. It is unconditionally fatal to call it on a fullcrum. This means no rebalancing operation (`recombine`, `takenephewnd`, etc.) can extract the root of one document's tree and graft it into another.

---

### 5. I-Addresses (Transclusion) Are Content Metadata, Not Tree Pointers

Transclusion works by storing an I-address — the `homedoc` tumbler in the `type2dbottomcruminfo` structure — inside the *leaf* (bottom crum) of the receiving document's POOM tree. This is the source document's I-space location, recorded as data. It is not a pointer to the source document's `fullcrumptr`.

When `rearrangend` walks the target document's tree at `edit.c:113`, it reads and modifies `ptr->cdsp.dsas[V]` — V-space offsets belonging to the *target* tree. The `homedoc` value sitting inside a bottom crum is not touched, not followed as a pointer, and does not cause any code to load the source document's POOM tree.

`ispan2vspanset` / `vspanset2ispanset` in `orglinks.c` perform I↔V coordinate conversion, but each call takes a single `typeorgl` (one document's root) and permutes spans within that document only. They do not look up a second document when they encounter a `homedoc` value.

---

### 6. `setwispupwards` Is Self-Limiting

After cuts and offset adjustments, `setwispupwards(father, 1)` at `edit.c:137` propagates V-width corrections upward through the tree. The propagation loop walks up through `findfather()` / `weakfindfather()` calls. When a node's `isapex == TRUE`, `leftbroorfather` is NULL, `weakfindfather` returns NULL, and the loop exits. The V-width update never escapes the document boundary.

---

### Conclusion

The question correctly identifies that REARRANGE operates on a single `fullcrumptr`. The corollary is that the second document's POOM tree is never accessed. No pointer to it is loaded, no crum within it is modified, and no V-offset within it is touched.

[FC-DOC-ISOLATION] holds because:

1. **One-document dispatch**: `dorearrange` calls `findorgl` for exactly one `docisaptr` [`do1.c:40`].
2. **Apex = dead end**: The `isapex` bit with `leftbroorfather == NULL` terminates all upward navigation at the document root [`enf.h:43, 67`].
3. **Disown guard**: The fullcrum cannot be detached, so no tree merge across documents is possible [`genf.c:353–360`].
4. **Metadata ≠ pointer**: Shared I-addresses live as scalar `homedoc` tumblers in leaf crums; they do not function as cross-tree pointers and are not dereferenced during REARRANGE [`insertnd.c`, `orglinks.c`].
5. **setwispupwards terminates at apex**: V-width propagation stops at the document root [`edit.c:137`].

The second document's V-positions are not "protected" by any explicit guard — they are simply structurally unreachable from a single-document REARRANGE call.
