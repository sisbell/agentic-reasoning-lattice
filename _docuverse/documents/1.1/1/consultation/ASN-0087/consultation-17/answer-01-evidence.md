## Question 1 [evidence]

> When udanax-green places the first link in a document's link subspace, does it fix the V-position to a particular depth, and if so, what depth and is it constant across documents?

## KB Synthesis

Yes. The first link in any document is fixed at V-position **`2.1`** — a constant depth of 2 tumbler digits — and this is uniform across all documents.

The mechanism is in `findnextlinkvsa()` (`do2.c:151-167`), which initializes by incrementing tumbler coordinates first to `2.0`, then to `2.1`. There is no per-document variation: the function hardcodes the two-step increment to reach `2.1` as the starting position [SS-LINK-SUBSPACE].

[SS-DUAL-ENFILADE] (Finding 0009) confirms the same: "`findnextlinkvsa()` constructs first link position at `2.1`."

Subsequent links are placed at `vspanreach` (current document end in V-space), so they get `2.2`, `2.3`, etc. [ST-CREATE-LINK] (Finding 0052) notes the append-at-end behavior means no shifting occurs in practice.

The subspace isolation machinery in [SS-TWO-BLADE-KNIFE] depends on this fixed starting point: `findaddressofsecondcutforinsert()` computes `(N+1).1` as the second knife blade boundary, which for text insertions at `1.x` yields `2.1` — exactly the first link position — ensuring text shifts never reach link entries.

---

## Code Exploration

I have all the information needed. Here is my complete answer.

---

## How udanax-green Fixes the V-Position of the First Link

### Short Answer

Yes. The first link in a document's link subspace is placed at V-position **2.1** (depth-2 tumbler, `mantissa[0]=2, mantissa[1]=1`), subject to a floor. This is hardcoded and constant across all documents, with one qualifier: if the document's text V-span extends past `2.1`, the link is placed immediately after the text — still at depth 2.

---

### The Tumbler Representation

The tumbler struct [common.h:59-64]:
```c
typedef struct structtumbler {
    ...
    tdigit mantissa[NPLACES];   /* NPLACES = 16 */
} tumbler;
```

A depth-2 tumbler like `2.1` has `mantissa[0]=2, mantissa[1]=1`, all higher positions zero. "Depth" here means the number of non-zero mantissa components.

---

### Entry Point: `findnextlinkvsa` [do2.c:151–167]

Both link creation functions — `domakelink` [do1.c:184] and `docreatelink` [do1.c:211] — call `findnextlinkvsa` to compute the absolute V-position for the new link atom in the document's V-space:

```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
    tumbler vspanreach, firstlink;
    typevspan vspan;
    bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);   // [do2.c:157] mantissa[0] = 2
    tumblerincrement (&firstlink, 1, 1, &firstlink);   // [do2.c:158] mantissa[1] = 1

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)   // [do2.c:162]
        movetumbler (&firstlink, vsaptr);               // use 2.1
    else
        movetumbler (&vspanreach, vsaptr);              // use text_end
    return (TRUE);
}
```

**Tracing `tumblerincrement` [tumble.c:599–623]:**

1. First call: `aptr` is zero → enters the zero-branch [tumble.c:603–607]:
   ```c
   cptr->exp = -rightshift;  // exp = 0
   cptr->mantissa[0] = bint; // mantissa[0] = 2
   ```
   Result: `firstlink = [2, 0, 0, ...]`

2. Second call: `aptr` is non-zero → scans backward to last non-zero (`idx=0`), then:
   ```c
   cptr->mantissa[idx + rightshift] += bint;  // mantissa[0+1] += 1
   ```
   Result: `firstlink = [2, 1, 0, ...]`

So `firstlink` is the depth-2 tumbler **2.1**, assembled from literal integers `2` and `1`.

---

### The Floor Logic

The placement rule at [do2.c:162–165] is:

```
linkvsa = max(2.1, text_vspan_end)
```

- **If the text subspace is empty or ends before 2.1**: link goes at exactly **2.1**.
- **If text extends past 2.1**: link goes immediately after the last text position.

In the normal case — text occupying V-space at mantissa[0]=1 (the text subspace) — `vspanreach` stays below 2.0, so the floor `2.1` is always the operative value. The depth is 2 in both branches.

---

### Fixed Internal V-Addresses: `setlinkvsas` [do2.c:169–183]

After placing the link node at `linkvsa`, the link's internal endpoint structure (FROM/TO/THREE) uses fixed relative V-addresses, also built from integer literals:

```c
bool setlinkvsas(tumbler *fromvsaptr, tumbler *tovsaptr, tumbler *threevsaptr)
{
    tumblerclear (fromvsaptr);
    tumblerincrement (fromvsaptr, 0, 1, fromvsaptr);   // [do2.c:172] fromvsa = 1.x
    tumblerincrement (fromvsaptr, 1, 1, fromvsaptr);   // [do2.c:173] fromvsa = 1.1

    tumblerclear (tovsaptr);
    tumblerincrement (tovsaptr, 0, 2, tovsaptr);       // [do2.c:175] tovsa = 2.x
    tumblerincrement (tovsaptr, 1, 1, tovsaptr);       // [do2.c:176] tovsa = 2.1

    if (threevsaptr) {
        tumblerclear (threevsaptr);
        tumblerincrement (threevsaptr, 0, 3, threevsaptr);  // [do2.c:179] threevsa = 3.x
        tumblerincrement (threevsaptr, 1, 1, threevsaptr);  // [do2.c:180] threevsa = 3.1
    }
    return (TRUE);
}
```

Every link, in every document, has:
| Endpoint | V-address (relative) | Depth |
|----------|----------------------|-------|
| FROM     | `1.1`                | 2     |
| TO       | `2.1`                | 2     |
| THREE    | `3.1`                | 2     |

These are confirmed as meaningful by `islinkcrum` [orglinks.c:255–261], which identifies link crums by the condition `mantissa[0]==1 && mantissa[1]!=0` — matching the FROM endpoint pattern exactly.

The spanfilade uses the named constants `LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3` [xanadu.h:36–38], set directly into `mantissa[0]` [spanf1.c:210–217], consistent with the same depth-2 scheme.

---

### Is It Constant Across Documents?

**Yes, unconditionally.** The depth-2 structure is embedded as bare integer literals (`0`, `1`, `2`, `3`) in the `tumblerincrement` calls. There is no per-document calculation, no parameter, no configuration. The function `findnextlinkvsa` takes the document ISA only to read the text span for the floor comparison; the floor value itself (`2.1`) is reconstructed identically every call.

---

### Summary

| Property | Value | Source |
|----------|-------|--------|
| Link subspace boundary | V = 2.0 (mantissa[0]=2) | [do2.c:157] |
| First link V-position (floor) | **2.1** (depth-2: mantissa=[2,1,...]) | [do2.c:157–158] |
| Actual position if text precedes it | `max(2.1, text_vspan_end)` | [do2.c:162–165] |
| FROM endpoint V-address within link | 1.1 (depth-2) | [do2.c:172–173] |
| TO endpoint V-address within link | 2.1 (depth-2) | [do2.c:175–176] |
| THREE endpoint V-address within link | 3.1 (depth-2) | [do2.c:179–180] |
| Varies by document? | **No** — hardcoded integer literals | [do2.c:151–183] |

The depth is fixed at **2** (two mantissa components), the link subspace floor is always **2.1**, and this is invariant across all documents.
