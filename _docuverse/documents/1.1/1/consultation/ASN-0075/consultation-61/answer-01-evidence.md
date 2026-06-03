## Question 1 [evidence]

> Does udanax-green's deletion/comparison machinery distinguish removing one of several V-occurrences of an I-address from removing the address entirely, or does it operate on set membership in a document's arrangement?

## KB Synthesis

The machinery operates on V-position crums, not on I-address membership. It has no notion of "how many V-occurrences reference this I-address."

**POOM DELETE is strictly V-range local**

`deletend` finds crums covering the specified V-range and either removes them (Case 1: fully within range — `disown + subtreefree`) or shifts them (Case 2: beyond range). Each crum is an independent V→I mapping. If I-address α appears at V-positions 1.5 (crum₁) and 1.10 (crum₂), deleting [1.5, 1.6) removes crum₁ and leaves crum₂ completely untouched. There is no reference count, no "last occurrence" check, no I-address tracking within the deletion path. [ST-DELETE, Finding 0064]

The POOM is a multimap — multiple V-positions mapping to the same I-address is a first-class state [SS-POOM-MULTIMAP] — and DELETE is designed to work within that model without collapsing it.

**DOCISPAN never tracks occurrence count**

The spanfilade DOCISPAN entry is written once at INSERT/COPY time and never removed by DELETE [INV-SPANF-WRITE-ONLY, ST-DELETE Finding 0057]. So after deleting *all* V-occurrences of α from a document, FIND_DOCUMENTS still returns that document — a stale reference with no correspondence to actual POOM state [EC-STALE-SPANF-REFERENCE]. The system has no mechanism to reconcile these layers.

**COMPARE_VERSIONS discovers via the surviving POOM**

`compare_versions` works by converting V-spans to I-spans through the current POOM, then intersecting. If any V-occurrence of α survives, the comparison finds it. If all are deleted, it won't — but the DOCISPAN still claims the document contains α. The two layers diverge permanently after deletion. [INT-DELETE-SPANF-DIVERGENCE, PRE-COMPARE-VERSIONS]

**Conclusion**

The system operates purely on set membership in the V-space arrangement (which crums cover the deleted V-range), not on I-address set membership. Removing one of N V-occurrences is structurally identical to removing the only V-occurrence from the POOM's perspective — both are crum removals in a range. The I-address "still present via another V-occurrence" vs "fully removed" distinction is only observable through subsequent queries (POOM lookup returns results vs empty), not through any tracking within the deletion operation itself.

---

## Code Exploration

Now I have all the evidence I need. Let me write the definitive answer.

---

## Answer: Deletion and Comparison in udanax-green

### The Core Architecture

A document in udanax-green is represented as a **POOM** (Permutation of Origins Matrix) enfilade. Each bottom crum in the POOM holds a 2D coordinate:

- `cdsp.dsas[V]` / `cwid.dsas[V]` — the crum's virtual (V-space) origin and width
- `cdsp.dsas[I]` / `cwid.dsas[I]` — the crum's invariant (I-space) origin and width

A single I-address can map to multiple V-positions if content is transcluded more than once; each occurrence is a separate POOM crum with the same `cdsp.dsas[I]` but a different `cdsp.dsas[V]`.

---

### Deletion is Pure V-Space Set Membership

The call chain is:

```
fns.c:deletevspan [333]
  → do1.c:dodeletevspan [158-167]
    → orglinks.c:deletevspanpm [145-152]
      → edit.c:deletend(docorgl, &vspan.stream, &vspan.width, V) [149]
```

`deletevspanpm` passes `V` as the dimension index:

```c
// orglinks.c:149
deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
```

Inside `deletend` [edit.c:31-76], the dimension is bound immediately:

```c
// edit.c:43
knives.dimension = index;  // == V
```

Every classification call is `deletecutsectionnd(ptr, &fgrasp, &knives)` [edit.c:49], which calls `whereoncrum(ptr, offset, blade, knives.dimension)`. `whereoncrum` computes position only in the named dimension [retrie.c:356-372]:

```c
// retrie.c:356-364
tumbleradd(&offset->dsas[index], &ptr->cdsp.dsas[index], &left);
// ...
tumbleradd(&left, &ptr->cwid.dsas[index], &right);
```

**The I-dimension (`cdsp.dsas[I]`, `cwid.dsas[I]`) is never read during deletion.**

After `makecutsnd` splits crums at the deletion boundaries, `deletend` iterates children [edit.c:47-73] and applies one of three outcomes:

| `deletecutsectionnd` | Meaning | Action |
|---|---|---|
| **0** | Crum entirely left of deleted V-range | Skip — nothing changes |
| **1** | Crum's V-range entirely inside deleted zone | `disown(ptr); subtreefree(ptr)` [edit.c:59-61] — POOM node removed |
| **2** | Crum's V-range entirely right of deleted zone | `tumblersub(&ptr->cdsp.dsas[index], width, ...)` [edit.c:63] — V-displacement adjusted to close the gap |

For case 1, the POOM crum is destroyed. Its `cdsp.dsas[I]` — the I-address it pointed to — is orphaned from this document's virtual arrangement. If another crum in the same POOM referenced the same I-address at a different V-position, it is untouched.

For case 2, only `cdsp.dsas[V]` changes. `cdsp.dsas[I]` is unchanged.

**The deletion engine never inspects I-space at all, and never counts how many V-occurrences of an I-address exist.**

---

### The Spanfilade is Not Updated on Deletion

`insertspanf` [spanf1.c:15-53] is called during `docopy` to register that document D references I-spans S in the spanfilade. The spanfilade is the index that answers "which documents contain this I-content" and drives link traversal.

`deletevspanpm` [orglinks.c:145-152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

There is no call to any spanfilade delete function anywhere in this path — no `deletespanf`, no reference count decrement. The spanfilade entry recording D→S persists after deletion. This means `finddocscontaining` [spanf1.c:151-188] and link traversal (`findlinksfromtothreesp` [spanf1.c:56-103]) will still return results for I-spans that have been removed from a document's virtual arrangement.

---

### The Consequence: One Occurrence vs. All Occurrences

Given these facts:

**If the same I-address X appears at V-position 3 (crum A) and V-position 7 (crum B), and you delete V-range [3,4]:**

- `makecutsnd` cuts at V=3 and V=4
- `deletecutsectionnd` returns 1 for crum A → `disown` + `subtreefree` — crum A gone
- `deletecutsectionnd` returns 2 for crum B → V-displacement updated from 7 to 6 — crum B intact, still maps to I-address X

**The deletion removes exactly the one V-occurrence that was in the deleted range. Other V-occurrences of the same I-address are completely unaffected.** This is correct transclusion semantics — the content at one virtual position is removed without disturbing the same content transcluded elsewhere.

However, because the spanfilade is not updated, the system's record that document D "contains" I-address X is not decremented. The distinction between "last occurrence removed" and "one of several removed" is invisible to the deletion path, and the spanfilade remains permanently inconsistent with the POOM after any deletion.

---

### Version Comparison Collapses V-Multiplicity

`doshowrelationof2versions` [do1.c:428-449] compares two versions by I-space intersection:

```c
specset2ispanset(taskptr, version1, &version1ispans, READBERT)   // V→I
&& specset2ispanset(taskptr, version2, &version2ispans, READBERT)
&& intersectspansets(taskptr, version1ispans, version2ispans, &commonispans, ISPANID)
&& ispansetandspecsets2spanpairset(taskptr, commonispans, version1, version2, relation)
```

`specset2ispanset` calls `permute` [orglinks.c:404-422] → `span2spanset` → `retrieverestricted` → `findcbcinarea2d` [retrie.c:229]. This finds all POOM bottom crums whose V-range overlaps the query V-span, and returns their I-extents. If two crums map to the same I-address (two V-occurrences of the same content), both I-extents are emitted. But `intersectspansets` operates on **I-span sets**, which merge overlapping spans into contiguous ranges.

**Version comparison has no concept of V-occurrence multiplicity.** "Common origin" is a set-theoretic property in I-space: either an I-address is present in both versions' I-span sets, or it isn't. Whether that address appeared at one or twenty V-positions does not affect the intersection result.

---

### Summary

| Question | Answer |
|---|---|
| Does deletion distinguish removing one V-occurrence vs. the last? | **No.** `deletend` [edit.c:31-76] operates on V-position intervals, never inspecting I-space. |
| What happens to other V-occurrences of the same I-address? | They are untouched — each is a separate POOM crum selected only by V-position. |
| Does the spanfilade (link/containment index) track this? | **No.** `deletevspanpm` [orglinks.c:145-152] does not call `deletespanf`. The index diverges from the POOM on deletion. |
| Does version comparison care about V-multiplicity? | **No.** It intersects I-span sets [do1.c:446], collapsing multiple V-occurrences of the same I-address to a single set-membership fact. |

The system operates on **V-space positional set membership** throughout deletion, and on **I-space set membership** during comparison. V-occurrence count is neither stored nor consulted at any point.
