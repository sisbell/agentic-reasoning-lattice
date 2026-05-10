## Question 11 [gregory]

> When `deletend` removes a POOM entry entirely within the deleted span, does `subtreefree` reclaim only the enfilade tree nodes (crums), or does it also touch the granfilade content those crums pointed to via I-address?

## KB Synthesis

`subtreefree` reclaims only the POOM enfilade tree nodes (in-memory crum structs). It does not touch the granfilade content those crums referenced via I-address.

The KB is explicit on this at multiple levels:

**POOM nodes are freed; granfilade is untouched**

[ST-DELETE] Finding 0064 states directly:

> DELETE operates exclusively on the POOM enfilade — it removes V-to-I mappings by pruning bottom crums (height-0 nodes) via `disown` + `subtreefree`. The I-addresses themselves continue to exist in the granfilade (which is append-only) and in the spanfilade (which has no delete operation).

The code reference confirms: `backend/credel.c:413-436` — `subtreefree`: recursive memory deallocation. This is deallocation of the in-memory `typecorecrum` structs managed by the grim reaper cache [SS-CACHE-MECHANISM], not any granfilade operation.

**The granfilade is append-only; DELETE cannot modify it**

[FC-GRANF-ON-DELETE] Finding 0061 establishes the frame condition:

> DELETE and REARRANGE are frame-condition-preserving with respect to the granfilade. These operations modify only the spanfilade (V-to-I mappings) and leave the granfilade (I-space content storage) completely unchanged.

[INV-IADDR-IMMUTABILITY] reinforces this:

> DELETE frees the POOM bottom crums that *reference* I-addresses, but the I-addresses themselves persist in the granfilade unconditionally.

**What `deletend` Case 1 actually does**

[ST-DELETE] Finding 0072 describes the mechanism: nodes within the deletion range are `disown`ed (removed from parent/sibling pointer chains) and then `subtreefree`d (recursively freed from the in-memory cache). This is purely structural surgery on the POOM tree topology. The I-addresses stored in those crums are just tumbler values — freeing the crum struct that held them has no effect on the granfilade entries at those addresses.

**Consequence: permanent I-space residue**

The granfilade content remains at its I-addresses after DELETE. This is what makes [INV-NO-IADDR-REUSE] hold — the next allocation via `findpreviousisagr` will find those I-addresses still present and allocate above them, never reusing them. It is also why [EC-STALE-SPANF-REFERENCE] occurs: the spanfilade's DOCISPAN entries (pointing to a document that no longer maps those I-addresses in its POOM) persist because neither `subtreefree` nor `deletend` touches the spanfilade.

---

## Code Exploration

Now I have the complete picture. Here is the full answer.

---

## Answer

**`subtreefree` reclaims only enfilade tree nodes (crums). It does not touch granfilade content via I-address.** The POOM crum's I-address information is simply dropped with the crum — no granfilade content is accessed, evicted, or freed.

---

### Execution Path

#### 1. `deletend` — the entry point [`edit.c:31`]

```c
case 1:
    disown ((typecorecrum*)ptr);      /* edit.c:59 */
    subtreefree ((typecorecrum*)ptr); /* edit.c:60 */
    break;
```

`deletecutsectionnd` returns `1` when the crum lies entirely within the deleted span [`edit.c:235–248`]. `disown` unlinks it from its parent in the tree. Then `subtreefree` is called on the orphaned root of that sub-tree.

---

#### 2. `subtreefree` — the definition [`credel.c:413`]

```c
/* assumes crum is disowned */
void subtreefree(typecorecrum *ptr)
{
    if (ptr->height > 0) {
        for (p = ((typecuc *)ptr)->leftson; p; p = right) {
            right = p->rightbro;
            disown (p);
            subtreefree (p);           /* credel.c:427 — recurse */
        }
    } else if (ptr->cenftype == GRAN
            && ((typecbc *)ptr)->cinfo.infotype == GRANORGL
            && ((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglincore)
        orglfree (((typecbc *)ptr)->cinfo.granstuff.orglstuff.orglptr); /* credel.c:430 */
    freecrum (ptr);                    /* credel.c:431 */
}
```

The logic has two branches:

- **Interior node** (`height > 0`): recurse into all children, then free this node. No content access.
- **Leaf node** (`height == 0`): check for the special GRAN/GRANORGL case, then always call `freecrum`.

---

#### 3. Why the GRAN/GRANORGL branch never fires for POOM crums

The guard at `credel.c:429` requires:

```c
ptr->cenftype == GRAN    /* enf.h:12: GRAN=1, POOM=2 */
```

A POOM crum has `cenftype == POOM` (2), not `GRAN` (1) [`enf.h:12–13`]. The condition is always false for any node in a POOM enfilade. The granfilade access branch is dead code from `deletend`'s perspective.

---

#### 4. What `orglfree` does (for completeness, for GRAN crums)

Even when `orglfree` is reached (only for GRAN leaf crums, not POOM), it does not delete granfilade content:

```c
void orglfree(typecuc *ptr)          /* credel.c:470 */
{
    /* assert: diskorglptr was written to disk */
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
    subtreefree ((typecorecrum*)ptr); /* credel.c:489 */
}
```

It asserts the on-disk copy exists (guarded by the `DISKPTRNULL` check at `credel.c:481`), then simply **clears the in-core pointer** — it evicts the cache, but leaves the disk-resident granfilade block untouched. The disk content is intentionally preserved.

---

#### 5. Corroborating comment in `corediskout.c`

```c
/*subtreefree(ptr);*/ /*12/04/86*/   /* corediskout.c:410 */
```

In the disk-write path, `subtreefree` was explicitly commented out as of December 1986. This is consistent with a design where granfilade content outlives the in-memory crum tree that references it.

---

### Summary

| What gets freed | What does not get freed |
|-----------------|------------------------|
| POOM crum tree nodes (all heights), via `freecrum` → `efree` | Granfilade content (disk blocks) |
| In-core GRAN orgl pointer (if `GRANORGL` leaf) | I-address slots referenced by deleted POOM crums |
| The crum's own heap allocation | On-disk granfilade blocks pointed to by I-addresses |

The I-address fields in the POOM crum's dimension span (`cdsp`) are carried along and dropped when the crum struct is freed by `efree` [`credel.c:452`]. Nothing traverses those I-addresses to notify the granfilade. The granfilade has no reference count decremented. The content it holds survives the deletion intact.
