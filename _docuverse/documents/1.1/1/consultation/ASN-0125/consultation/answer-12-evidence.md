## Question 12 [evidence]

> `findnextlinkvsa` computes max+1 over the POOM's link subspace: after DELETEVSPAN removes the highest link's `2.N` entry, does a subsequently created replacement link reuse V-position `2.N` while I-address allocation (which queries the append-only granfilade) still advances — so the same V-position can refer to two different link orgls across time?

## KB Synthesis

Yes, this can happen. Here is the reasoning from the KB:

## V-Position Reuse After DELETEVSPAN

**How `findnextlinkvsa` computes the next link position:**

[SS-LINK-SUBSPACE] documents that `findnextlinkvsa` initializes the first link at `2.1` and places subsequent links at `vspanreach` — the current end of the document's POOM extent. `vspanreach` is a live query of current POOM state, not a stored counter.

**What DELETEVSPAN does:**

[SS-THREE-LAYER-MODEL] is explicit: `DELETEVSPAN(2.x)` removes only the POOM entry. The link orgl in I-space and the spanfilade entries are untouched. [FC-GRANF-ON-DELETE] confirms the granfilade is invariant under DELETE.

**The sequence:**

1. Two links exist: V-position `2.1` → I-address I₁, V-position `2.2` → I-address I₂. `vspanreach = 2.2+`.
2. `DELETEVSPAN(2.2)` removes the POOM entry. `vspanreach` drops back to the extent of `2.1` (or whatever remains highest).
3. Next `findnextlinkvsa` call computes `vspanreach` from the current (post-deletion) POOM → yields `2.2` again.
4. I-address allocation via `findisatoinsertmolecule` queries the granfilade maximum. [INV-MONOTONIC] and [INV-NO-IADDR-REUSE] confirm the old I₂ is retained in the append-only granfilade, so the new link orgl receives I₃ > I₂.

**Result:** V-position `2.2` is now occupied by a fresh link orgl at I₃, while I₂ (the old link's orgl) remains in the granfilade — reachable directly by its ISA, still indexed in the spanfilade, but no longer mapped in the POOM.

## Consequences for the Spec

This exposes a key asymmetry:

| Layer | Under DELETEVSPAN | Under CREATELINK |
|-------|-------------------|-----------------|
| POOM (V→I mapping) | Entry removed | New entry at recomputed `vspanreach` |
| Granfilade (link orgl) | Unchanged (permanent) | New orgl appended at next I-address |
| Spanfilade | Unchanged (append-only) | New DOCISPAN/endset entries added |

**V-positions in the link subspace are not stable identifiers across time.** The same `2.N` V-position can denote different link orgls in different epochs. Only the I-address (link orgl ISA) is the stable identity for a link, as guaranteed by [INV-LINK-PERMANENCE] and [INV-NO-IADDR-REUSE].

The formal model must therefore state: `link_identity(link) ≡ link.ISA` (not `link.vposition`), and any invariant about link subspace occupancy must be scoped to a single point in time — `∀ t: poom(doc, t)` is a function at time t, but `2.N` at `t₁` and `2.N` at `t₂` may reference distinct link orgls when a DELETEVSPAN occurred between them.

This also means [EC-REVERSE-ORPHAN]'s "reverse orphan" state (link discoverable but absent from POOM) combined with subsequent CREATELINK can produce two distinct link orgls with the same V-position history — the old one discoverable via spanfilade/ISA and the new one via the current POOM — with no collision, because the I-addresses differ.

---

## Code Exploration

I have all the information needed. Let me write the complete answer.

---

## Answer: V-position Reuse After DELETEVSPAN

**Yes, the same V-position `2.N` can refer to two different link orgls across time.** Here is the complete code trace.

---

### Step 1: How `findnextlinkvsa` computes the next link V-address

`do2.c:151–166`:
```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

The function:
- Builds `firstlink = 2.1` (minimum allowed V-address for a link)
- Calls `doretrievedocvspan` to read the document's current V-span
- Computes `vspanreach = vspan.stream + vspan.width` — the V-address one past all current document content
- Returns `max(2.1, vspanreach)` as the insertion point for the next link

This is **not a high-water mark**. It reads live POOM state.

---

### Step 2: `doretrievedocvspan` reads live POOM fields

`do1.c:312–319`:
```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), retrievevspanpm();
    return
       findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)
    && retrievevspanpm (taskptr, docorgl, vspanptr);
}
```

`orglinks.c:165–172`:
```c
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root POOM node's in-memory fields: `cdsp.dsas[V]` (V-origin) and `cwid.dsas[V]` (cumulative V-width). These are mutable structural fields, updated whenever the tree changes.

---

### Step 3: DELETEVSPAN modifies exactly these POOM fields

`dodeletevspan` (do1.c:158–166) calls `deletevspanpm` (orglinks.c:145–152):

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

`deletend` (`edit.c:31–76`) removes the matching crums from the POOM tree and then calls:

```c
setwispupwards (father, 1);   // edit.c:74
recombine (father);            // edit.c:75
```

`setwispupwards` (`wisp.c:83`) walks from the affected node upward, calling `setwisp` at each level. For POOM nodes, `setwisp` calls `setwispnd` (`wisp.c:171`), which recomputes the parent's bounding box:

```c
// wisp.c:207–214
clear (&newwid, sizeof(newwid));
for (ptr = findleftson (father); ptr; ptr = getrightbro (ptr)) {
    lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, ...);
    lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, ...);
}
```

The result is propagated all the way to the POOM root. After `deletend` of the highest-address link content at `[2.N, 2.N+w)`, the root's `cwid.dsas[V]` **shrinks from `stream + (2.N+w)` to `stream + 2.N`**.

**Critical:** `deletevspanpm` does NOT touch the granfilade. It calls `deletend` only on `docorgl` (the document's POOM), never on the granfilade tree.

---

### Step 4: I-address allocation queries the granfilade, which is never pruned

When `docreatelink` or `domakelink` is called, the first step is I-address allocation:

```c
// do1.c:182 / do1.c:209
createorglingranf (taskptr, granf, &hint, linkisaptr)
```

This calls through `createorglingranf` → `createorglgr` (granf2.c:111) → `findisatoinsertgr` (granf2.c:130) → `findisatoinsertmolecule` (granf2.c:158) for LINKATOM:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typeisa upperbound, lowerbound;

    tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
    // upperbound = docisa.2.3 (just above link subspace)

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    // lowerbound = highest ISA currently in granfilade below docisa.2.3

    } else if (hintptr->atomtype == LINKATOM) {
        tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);  // docisa.2.2 = min link ISA
        if (tumblercmp (&lowerbound, isaptr) == LESS)
            tumblerincrement (isaptr, 1, 1, isaptr);          // no links yet
        else
            tumblerincrement (&lowerbound, 0, 1, isaptr);    // lowerbound + 0.1
    }
}
```

`findpreviousisagr` (granf2.c:255–278) traverses the granfilade sequential enfilade looking for the rightmost entry below `upperbound`:

```c
int findpreviousisagr(typecorecrum *crumptr, typeisa *upperbound, typeisa *offset)
{
    if (crumptr->height == 0) {
        findlastisaincbcgr ((typecbc*)crumptr, offset);
        return(0);
    }
    for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
        if ( (tmp = whereoncrum(ptr, offset, upperbound, WIDTH)) == THRUME
          || tmp == ONMYRIGHTBORDER
          || !ptr->rightbro) {
            findpreviousisagr (ptr, upperbound, offset);   // recurse into this child
            return(0);
        } else {
            tumbleradd(offset, &ptr->cwid.dsas[WIDTH], offset);  // accumulate offset
        }
    }
}
```

Because DELETEVSPAN never modifies the granfilade (only the POOM), the deleted link's I-address entry at `docisa.2.K.0.1` (or wherever) persists. `findpreviousisagr` finds it, and the new link gets ISA `docisa.2.K.0.2` — strictly beyond the old link's I-address. **The I-address counter is monotonically increasing.**

---

### The Collision

Given:
1. **Link L1 created**: I-addr = `D.2.K.0.1`, V-addr = `2.N` (link copy inserted into POOM at `[2.N, 2.N+w)`)
2. **DELETEVSPAN on `[2.N, 2.N+w)`**: POOM shrinks — `cwid.dsas[V]` updated to `2.N`; granfilade unchanged — L1's entry `D.2.K.0.1` remains
3. **Link L2 created**:
   - `findnextlinkvsa` reads POOM: `vspanreach = 2.N` → returns `2.N` ← **V-position reused**
   - `findisatoinsertmolecule` reads granfilade: finds `D.2.K.0.1`, returns `D.2.K.0.2` ← **new I-address**
   - `docopy` inserts L2's ispan at V-address `2.N` in the POOM

**Result:** V-position `2.N` in the document now maps to L2 (I-addr `D.2.K.0.2`). L1 (I-addr `D.2.K.0.1`) has been orphaned in the granfilade. Any client-side reference that recorded V-position `2.N` expecting L1 silently resolves to L2. The V-to-I bijection — the invariant that each V-position names exactly one link over the system's lifetime — is broken.

The structural mismatch is that `findnextlinkvsa` looks backward through live POOM state (mutable after deletion), while `findisatoinsertmolecule` looks backward through granfilade state (append-only, never pruned by DELETEVSPAN). The two address spaces advance independently, and deleting from one while the other holds fixed creates the reuse hole.
