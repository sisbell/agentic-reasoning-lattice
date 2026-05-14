## Question 1 [evidence]

> Does udanax-green's POOM hold mapping blocks for non-text subspaces (e.g., the link subspace), or is each POOM restricted to a single subspace of one document?

## KB Synthesis

A single POOM per document holds mapping blocks for **all subspaces**. The POOM is a unified 2D enfilade whose V-dimension spans the full address space of a document, with subspace membership encoded by convention in the leading tumbler digit rather than by structural partitioning.

**Direct evidence:**

[SS-TWO-BLADE-KNIFE] is the clearest proof. `findaddressofsecondcutforinsert()` computes `blade[1] = (N+1).1` for any insertion at `N.x`. The knife explicitly guards against shifting *sibling subspace entries residing in the same tree* — a guard only necessary because 1.x text crums and 2.x link crums coexist in one POOM.

[SS-THREE-LAYER-MODEL] / [ST-DELETE] (Finding 0040) confirms: `DELETEVSPAN(2.x)` calls `deletend()` on the **document's orgl enfilade** — the same POOM that holds 1.x entries — and removes the link crum from it.

[ST-CREATE-LINK] (Finding 0052): CREATELINK calls `docopy` → `insertpm` → `insertnd` → `makegappm`. This is the same insertion path used for text. The 2.x entry goes into the document's existing POOM alongside 1.x entries.

[FC-SUBSPACE] (Finding 0055): DELETE at 1.x classifies 2.x crums as case 2 (shift), then `strongsub`'s exponent guard prevents the shift from actually executing. Both crum types are traversed by the same `deletend` loop — confirming they live in one tree.

[SS-VSPAN-VS-VSPANSET] (Findings 0017, 0035): `retrievevspansetpm()` extracts both subspace spans from one root node by testing `is1story()` — a single root covers the full multi-subspace extent.

**The three-subspace layout** ([SS-SUBSPACE-CONVENTION], Finding 0038): V-positions 1.x (text), 2.x (link orgls), and 3.x (type endpoints) all live in the same document POOM. `setlinkvsas()` hardcodes digits 1, 2, and 3 for the three endpoint types, all inserted via the same `insertpm` into the same tree.

**Summary:** Each document has exactly one POOM. That POOM is subspace-agnostic at the storage level — it holds whatever V→I mappings callers insert. The caller-enforced convention assigns 1.x to text, 2.x to link orgls, and 3.x to type endpoints, but the POOM tree structure knows nothing of these partitions. Subspace isolation (INSERT at 1.x not shifting 2.x) is enforced by the knife mechanism and `strongsub` arithmetic, not by separate trees.

---

## Code Exploration

Now I have everything I need. Let me compose the final, fully cited answer.

---

## Does the POOM Hold Mapping Blocks for Non-Text Subspaces?

**Yes — a single POOM instance spans multiple subspaces.** Each POOM belongs to one owner (a document or a link), but within that owner's V-dimension the tree holds crums for both text content and link-related data. There is no separate POOM per subspace.

---

### 1. The POOM Data Structure Has No Subspace Field

`enf.h:54-81` defines `typecuc` (core upper crum), which is the POOM fullcrum:

```c
struct structcuc {
    bool isapex BIT;
    SINT height;
    SINT cenftype;           /* GRAN, SPAN, or POOM */
    bool modified BIT;
    bool isleftmost BIT;
    typecorecrum *nextcrum, *prevcrum;
    unsigned char age;
    typecorecrum *leftbroorfather;
    typecorecrum *rightbro;
    typewid cwid;            /* 2D: cwid.dsas[I] and cwid.dsas[V] */
    typedsp cdsp;            /* 2D: cdsp.dsas[I] and cdsp.dsas[V] */
    typediskloafptr sonorigin;
    typecorecrum *leftson;
    INT numberofsons;
};
```

There is no `subspace`, `linkspace`, or `textspace` field. The POOM is a **two-dimensional enfilade** (I × V). Document identity is passed as an external parameter (`typeisa *docisaptr`) to every operation, never stored in the tree node itself.

---

### 2. Two Distinct Kinds of POOM Owner

#### Document POOM

Every document gets one POOM via `findorgl(taskptr, granf, docisaptr, &docorgl, ...)` (`do1.c:55`). Its V-dimension is partitioned by value:

- **Text content** — crums with `mantissa[1] == 0` and a 1-digit (single-level) V-width, identified by `istextcrum` at `orglinks.c:246-253`
- **Link-ISA references** — crums where `cdsp.dsas[V].mantissa[0] == 1 AND mantissa[1] != 0` (i.e. V-displacement is a two-level tumbler like 1.n), identified by `islinkcrum` at `orglinks.c:255-261`:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0){
        /* if the whole crum is displaced into link space it is a link crum
           this is true if the tumbler is a 1.n tumbler where n != 0 */
        return TRUE;
    }
    return FALSE;
}
```

`findvsatoappend` (`orglinks.c:29-49`) uses `linkspacevstart` (V = 2.0, built by incrementing position 0 by 2) as the boundary guard when appending text — if the document's grasp has already passed 2.0 into link territory, it back-fills text at the first available text slot instead of stomping on link data. That boundary check only makes sense if text and link crums coexist in the same tree.

#### Link POOM

`docreatelink` (`do1.c:195-221`) creates a separate orgl for each link via `createorglingranf(taskptr, granf, &hint, linkisaptr)` at `do1.c:209`. Then `insertendsetsinorgl` (`do2.c:130-148`) calls `insertpm` three times on that single link orgl:

```c
bool insertendsetsinorgl(... tumbler *fromvsa, typesporglset fromsporglset,
                             tumbler *tovsa,   typesporglset tosporglset,
                             tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset))) {
        return (FALSE);
    }
    if (threevsa && threesporglset) {
        insertpm(taskptr, linkisaptr, link, threevsa, threesporglset);
    }
    ...
}
```

`setlinkvsas` (`do2.c:169-183`) sets the three V-addresses:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   /* 1.1 */
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);
    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       /* 2.1 */
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);
    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  /* 3.1 */
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);
    }
    return (TRUE);
}
```

Three distinct V-positions (1.1, 2.1, 3.1) inside **one link POOM** — the "from endpoint" subspace, the "to endpoint" subspace, and the optional "three endpoint" subspace all coexist in the same tree.

---

### 3. `retrievevspansetpm` Confirms the Unified Structure

`orglinks.c:173-221` explicitly handles both portions of a single POOM in one read:

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
    ...
    if (is1story (&ccptr->cwid.dsas[V])) {
        /* just text — return one span */
        putvspaninlist (taskptr, &vspan, vspansetptr);
        return TRUE;
    } else {
        /* both text and link portions present */
        /* link part: grab last digit off the width */
        movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
        linkvspan.stream.mantissa[1] = 0;

        /* text part: use maxtextwid to find the text ceiling */
        maxtextwid(taskptr, ccptr, &voffset, &maxwid);

        putvspaninlist (taskptr, &vspan, vspansetptr);
        putvspaninlist (taskptr, &linkvspan, vspansetptr);  /* both returned */
        return (TRUE);
    }
}
```

`maxtextwid` (`orglinks.c:224-245`) recurses over the tree and explicitly skips link crums:

```c
for(ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)){
    if(ptr && !islinkcrum(ptr)){  /* only look for text or overlapping stuff */
        maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
    }
}
```

This can only work if text crums and link crums are **siblings in the same subtree**.

---

### 4. How Link ISA References Enter the Document POOM

In `docreatelink` (`do1.c:195-221`), after creating the link orgl, the link's ISA is copied into the document's own POOM at the next available link V-position:

```c
&& findnextlinkvsa (taskptr, docisaptr, &linkvsa)     /* find next V slot */
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)    /* write into doc POOM */
```

`findnextlinkvsa` (`do2.c:151-167`) computes the insertion point: it uses V = 2.1 as a floor and places the link ISA reference right after the document's existing V-span, whichever is further out. `docopy` in turn calls `insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)` (`do1.c:60`) — the same `insertpm` used for text insertion, on the same document POOM.

---

### Summary

| Owner | What the POOM holds | V subspaces in the tree |
|---|---|---|
| Document | Text content atoms + link ISA references | Text crums (single-level V, `mantissa[1]=0`) and link crums (two-level V, `mantissa[1]≠0`) |
| Link | From/to/three endpoint span sets | Three V-positions: 1.1 (from), 2.1 (to), 3.1 (three) |

**Each POOM belongs to exactly one owner (one document or one link), but that single POOM tree holds mapping blocks for all of that owner's V-subspaces.** There is no separate POOM per subspace. Subspace identity is encoded entirely in the tumbler value of the V-dimension, not in any structural field of the crum or enfilade. The functions `istextcrum` and `islinkcrum` (`orglinks.c:246-261`) classify crums by inspecting their V-displacement tumblers at runtime rather than reading a stored tag.
