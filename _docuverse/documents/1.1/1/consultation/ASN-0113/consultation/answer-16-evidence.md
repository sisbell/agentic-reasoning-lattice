## Question 16 [evidence]

> After a link's POOM entry is removed via DELETEVSPAN on `2.x` (reverse-orphaned link [ST-LINK-REMOVE]), does the link subspace VSpec returned by RETRIEVEDOCVSPANSET reflect the now-absent V→I mapping, or does it still report the prior link count?

## KB Synthesis

After DELETEVSPAN on `2.x`, RETRIEVEDOCVSPANSET reflects the **now-absent mapping** — the link span disappears from the returned vspanset.

**Mechanism:** `DELETEVSPAN(2.x)` calls `deletevspanpm()` → `deletend()`, which removes the V-position `2.x` crum from the document's POOM tree [SS-THREE-LAYER-MODEL, ST-DELETE]. RETRIEVEDOCVSPANSET uses `retrievevspansetpm()`, which reconstructs spans by reading the **current POOM state** via `is1story()` checks and explicit link/text subspace traversal [SS-VSPAN-VS-VSPANSET, SS-DUAL-ENFILADE].

**Direct evidence from [SS-THREE-LAYER-MODEL] (Finding 0040):**

```
Before DELETEVSPAN(2.1):
  vspanset: [{"start": "0", "width": "0.1"}, {"start": "1", "width": "1"}]

After DELETEVSPAN(2.1):
  POOM: V-position 2.1 removed
  vspanset: [{"start": "1.1", "width": "0.11"}]   ← link span gone
  find_links(source_specs) → still finds the link  ← spanfilade intact
  follow_link(link_id, SOURCE) → still works        ← link orgl intact
```

**What persists vs. what changes:**

| Layer | After DELETEVSPAN(2.x) |
|-------|------------------------|
| I-space (link orgl) | Unchanged [INV-LINK-PERMANENCE] |
| Spanfilade (DOCISPAN/link index) | Unchanged [INV-SPANF-WRITE-ONLY] |
| POOM (V-stream) | V→I mapping removed — RETRIEVEDOCVSPANSET reflects this |

This is the "reverse orphan" state [EC-REVERSE-ORPHAN]: the link is discoverable via `find_links` and followable via `follow_link` (I-space and spanfilade intact), but the document's vspanset no longer reports it as contained. The POOM is the sole mutable layer [SS-POOM-MUTABILITY], and RETRIEVEDOCVSPANSET reads only the POOM.

---

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## Does RETRIEVEDOCVSPANSET Reflect the Now-Absent V→I Mapping After DELETEVSPAN on 2.x?

**Short answer: Yes. RETRIEVEDOCVSPANSET immediately reflects the post-deletion state. The link subspace span disappears from the returned VSpanSet; the prior link count is not reported.**

---

### 1. Call Chain for DELETEVSPAN on the Document at 2.x

```
fns.c:339        deletevspan()
                   ↓
do1.c:157-165    dodeletevspan()
                   findorgl(granf, docisaptr, &docorgl, WRITEBERT)
                   deletevspanpm(taskptr, docisaptr, docorgl, vspanptr)
                   ↓
orglinks.c:133-138  deletevspanpm()
                   deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V)
                   logbertmodified(docisaptr, user)
                   ↓
edit.c:31-76     deletend()
```

`dodeletevspan` [do1.c:163-164]:
```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
```

`deletevspanpm` [orglinks.c:133-138]:
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

No spanfilade update, no link-orgl update. Only the **document's POOM enfilade** is modified.

---

### 2. What `deletend` Does to the Enfilade

`deletend` [edit.c:31-76] performs a V-dimension cut on the document's POOM:

```c
movetumbler (origin, &knives.blades[0]);   // cut at 2.x start
tumbleradd (origin, width, &knives.blades[1]); // cut at 2.x end
knives.dimension = index; // V
makecutsnd (fullcrumptr, &knives);
newfindintersectionnd (fullcrumptr, &knives, &father, &foffset);
...
for (ptr = findleftson(father); ptr; ptr = next) {
    ...
    case 1:
        disown ((typecorecrum*)ptr);  // remove crum
        subtreefree ((typecorecrum*)ptr);
        break;
    case 2:
        tumblersub (&ptr->cdsp.dsas[index], width, &ptr->cdsp.dsas[index]);
        break;
}
setwispupwards (father, 1);  // propagate width up the tree  [edit.c:74]
recombine (father);          // rebalance                     [edit.c:75]
```

**The critical line is `setwispupwards(father, 1)` at edit.c:74.** This propagates the updated V-width from the deletion point all the way up to the root crum. After the call, the root crum's `cwid.dsas[V]` no longer includes the deleted link's V-extent.

---

### 3. Call Chain for RETRIEVEDOCVSPANSET

```
fns.c:129-141    retrievedocvspanset()
                   doretrievedocvspanset(taskptr, &docisa, &vspanset)
                   ↓
do1.c:317-331    doretrievedocvspanset()
                   findorgl(granf, docisaptr, &docorgl, READBERT)
                   if (isemptyorgl(docorgl)) → return NULL vspanset
                   retrievevspansetpm(taskptr, docorgl, vspansetptr)
                   ↓
orglinks.c:158-199  retrievevspansetpm()
```

`doretrievedocvspanset` [do1.c:317-331]:
```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
    typeorgl docorgl;
    if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
        return FALSE;
    if (isemptyorgl (docorgl)) {
        *vspansetptr = NULL;
        return TRUE;
    }
    return retrievevspansetpm (taskptr, docorgl, vspansetptr);
}
```

---

### 4. How `retrievevspansetpm` Reads the Root Crum

`retrievevspansetpm` [orglinks.c:158-199]:
```c
ccptr = (typecorecrum *) orgl;          // root crum of document's POOM
tumblerclear (&voffset);
*vspansetptr = NULL;
if (is1story (&ccptr->cwid.dsas[V])) { // [orglinks.c:167]
    // text-only case
    vspan.itemid = VSPANID;
    movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
    vspan.next = NULL;
    putvspaninlist (taskptr, &vspan, vspansetptr);
    return TRUE;
} else {
    // text + links case: compute both spans from root width
    linkvspan.itemid = VSPANID;
    movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream); // [orglinks.c:176]
    linkvspan.stream.mantissa[1] = 0;
    tumblerjustify(&linkvspan.stream);
    movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);  // [orglinks.c:180]
    linkvspan.width.mantissa[1] = 0;
    tumblerjustify(&linkvspan.width);
    ...
}
```

The gate is `is1story(&ccptr->cwid.dsas[V])` [tumble.c:237-246]:
```c
bool is1story(tumbler *tumblerptr)
{
    INT i;
    for (i = 1; i < NPLACES; i++)
        if (tumblerptr->mantissa[i] != 0)
            return (FALSE);
    return (TRUE);
}
```

`is1story` returns TRUE when **all mantissa positions ≥ 1 are zero** — meaning the V-dimension covers only a single "level" (text content at mantissa[0] = 1, with no link overflow into mantissa[1]).

After `deletend` + `setwispupwards` removes the link crum and propagates the change, the root's `cwid.dsas[V]` reflects text-only extent → `is1story` returns TRUE → **no link span is computed or emitted**.

---

### 5. Empirical Confirmation (Finding 0040)

Finding 0040 records the actual test results (`links/delete_link_subspace.json`):

**Before DELETEVSPAN(2.1):**
```json
"spans": [
  {"start": "0", "width": "0.1"},   // link subspace (normalized from 2.x)
  {"start": "1", "width": "1"}      // text subspace
]
```

**After DELETEVSPAN(2.1):**
```json
"spans": [
  {"start": "1.1", "width": "0.11"}  // only text remains
]
```

The link span is **gone**. No stale link count. The POOM deletion propagates through the enfilade to the root, and `retrievevspansetpm`'s `is1story` branch switch immediately reflects it.

---

### 6. Normalization Note (Finding 0038)

`retrievevspansetpm` does not report raw V-positions. When text and links coexist, links are **normalized to "0"** in output (by zeroing mantissa[1] of the root V-width and justifying). The internal representation is always 2.x. After deletion of the sole link, no normalization artifact remains — the "0" entry disappears entirely because `is1story` gates the `else` branch that produces it.

---

### 7. What Does NOT Get Updated

`dodeletevspan` [do1.c:157-165] touches only the **document's POOM**. It does not call any spanfilade update. After the deletion:

- **Link orgl in I-space** (granfilade): intact, permanently at the link's I-address
- **DOCISPAN entries in spanfilade**: intact, so `FINDLINKSFROMTOTHREE` still returns the link
- **Link's own POOM** (from/to/three endpoints): intact, so `FOLLOWLINK` still works

The document no longer "contains" the link in its V-stream view (RETRIEVEDOCVSPANSET reports it absent), but the link is still discoverable and followable via the other two layers.

---

### Summary

| Query after DELETEVSPAN(2.x) | Result |
|------------------------------|--------|
| **RETRIEVEDOCVSPANSET** | Link span absent — reflects actual post-deletion POOM state |
| **FINDLINKSFROMTOTHREE** | Link still found — spanfilade unchanged |
| **FOLLOWLINK(link_id)** | Still works — link orgl in I-space unchanged |

The mechanism: `deletend` [edit.c:31] removes the link crum from the document's POOM and calls `setwispupwards` [edit.c:74] to propagate the updated V-width up to the root. `retrievevspansetpm` [orglinks.c:164] reads the root crum directly — no cache layer — so the next RETRIEVEDOCVSPANSET call sees the post-deletion state, not the prior link count.
