## Question 4 [evidence]

> When `Nullify` (or its equivalent) is called twice on the same target address in udanax-green, does the implementation produce one retraction record or two distinct records?

## KB Synthesis

This question is not answerable from the KB as provided.

Neither "Nullify" nor "retraction records" appear anywhere in these findings. The KB documents udanax-green's delete mechanism as DELETEVSPAN, which removes V-to-I mappings from the POOM [SS-THREE-LAYER-MODEL, ST-DELETE] without touching the granfilade [FC-GRANF-ON-DELETE] or spanfilade [INV-SPANF-WRITE-ONLY]. There is no concept of a "retraction record" in any of the 78 findings.

What the KB *does* say about repeated deletions is limited: the POOM is mutated in-place by `deletend` [SS-POOM-MUTABILITY], `deletevspanpm` only checks for zero-width before proceeding [PRE-DELETE, Finding 0040], and the levelpull that would clean up empty tree nodes after deletion is disabled [SS-ENFILADE-TREE, Finding 0058]. None of this addresses a "Nullify" abstraction or any record-keeping layer above the POOM.

If "Nullify" refers to a front-end concept or a design document outside this KB, the answer would require those sources.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Nullify Called Twice on the Same Target Address

The term "Nullify" does not appear in udanax-green. The closest operation is `deletevspan`, which is the FEBE command that removes content by virtual span address. There are also **no "retraction records"** in the traditional sense — `deletevspan` is a direct structural edit to the enfilade tree, not a journaled log entry.

---

### Execution Path

**1. FEBE handler** — `fns.c:333–347`

```c
void deletevspan(typetask *taskptr)
{
    typeisa docisa;
    typespan vspan;
    bool getdeletevspan(), dodeletevspan();

    (void) getdeletevspan (taskptr, &docisa, &vspan);
    putdeletevspan (taskptr);                           // ← success ACK sent BEFORE operation
    if (!dodeletevspan (taskptr, &docisa, &vspan))
        fprintf(stderr,"deletevspan failed \n");
}
```

Note `fns.c:340`: `putdeletevspan` — the success reply is sent to the client *before* the tree operation executes. Two calls therefore produce two success ACKs unconditionally.

**2. Core handler** — `do1.c:158–167`

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    typeorgl docorgl;
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
    );
}
```

Acquires the document's orgl handle (`WRITEBERT` lock), then delegates to the permutation-matrix layer.

**3. PM layer** — `orglinks.c:145–152`

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))    // only guard: zero-width check
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`orglinks.c:147` is the **only guard** — it rejects zero-width spans. There is **no check for whether the span has already been deleted**. A non-zero width always proceeds to `deletend`.

**4. Tree edit** — `edit.c:31–76`

```c
int deletend(typecuc *fullcrumptr, tumbler *origin, tumbler *width, INT index)
{
    ...
    movetumbler (origin, &knives.blades[0]);
    tumbleradd (origin, width, &knives.blades[1]);
    knives.nblades = 2;
    knives.dimension = index;
    makecutsnd (fullcrumptr, &knives);                      // cut tree at [origin, origin+width]
    newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
    ...
    for (ptr = (typecuc *) findleftson (father); ptr; ptr = next) {
        switch (deletecutsectionnd ((typecorecrum*)ptr, &fgrasp, &knives)) {
          case 1:
            disown ((typecorecrum*)ptr);    // remove from tree
            subtreefree ((typecorecrum*)ptr); // free memory
            break;
          case 2:
            tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]); // shrink
            break;
          case 0:
            break;                          // out of range — no-op
        }
    }
    setwispupwards (father, 1);
    recombine (father);
}
```

`makecutsnd` (`ndcuts.c:15–31`) also calls `logbertmodifiedforcrum` at `ndcuts.c:19` unconditionally, marking the document dirty on every invocation.

---

### What Happens on the Second Call

Given the same `docisa` and `vspan` (same origin and non-zero width):

| Step | First call | Second call |
|------|-----------|-------------|
| `putdeletevspan` `fns.c:340` | sends ACK | sends ACK |
| `iszerotumbler` `orglinks.c:147` | passes | passes (width unchanged in caller's struct) |
| `makecutsnd` `edit.c:44` | cuts tree at [origin, origin+width] | cuts tree again at same positions (already cut; cuts are idempotent structurally) |
| `deletecutsectionnd` loop `edit.c:47–73` | returns 1 or 2 for nodes in range; removes/shrinks them | returns **0** for all nodes — they were removed in call 1 |
| `disown`/`subtreefree` `edit.c:59–60` | called on content nodes | **not called** — no nodes in range |
| `logbertmodified` `orglinks.c:150` | marks document dirty | marks document dirty again (no-op, already set) |

---

### Answer

**Udanax-green produces no "retraction records" at all.** `deletevspan` is a direct in-place structural modification to the enfilade tree — content nodes are `disown`'d and `subtreefree`'d. There is no journal, log, or record of the deletion.

When called **twice** on the same target vspan:

- The **first call** genuinely modifies the tree: it inserts cut points (`makecutsnd`) and removes/adjusts all crum nodes whose addresses fall within [origin, origin+width].
- The **second call** re-enters the same code path, passes the zero-width guard at `orglinks.c:147`, calls `makecutsnd` again (which re-cuts the already-cut positions), but the subsequent loop at `edit.c:47–73` finds **no nodes** in the now-empty range — `deletecutsectionnd` returns `0` for all children, meaning the loop body is a no-op for every node.

The net result is **one structural change** to the tree (from the first call), not two. The second call is silently accepted (success ACK sent at `fns.c:340`) and then structurally inert. No duplicate record exists because no record exists at all — only the modified tree state.
