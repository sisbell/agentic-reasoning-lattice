## Question 20 [evidence]

> Since INSERT and DELETE preserve subspace isolation [FC-SUBSPACE], is it invariant that the text VSpec's width returned by RETRIEVEDOCVSPANSET is independent of how many links exist — i.e., editing in `2.x` never alters the reported `1.x` extent and vice versa?

## KB Synthesis

**Yes, the invariant holds for RETRIEVEDOCVSPANSET under well-formed operations — but it is convention-enforced, not storage-enforced.**

---

**Why the `1.x` extent is independent of `2.x` edits:**

CREATELINK places link orgls at `2.x` via `findnextlinkvsa` + `insertpm`. By [FC-SUBSPACE] (Finding 0054), INSERT at `2.x` constructs a two-blade knife with `blade[1] = 3.1`, restricting all V-position shifts to `[2.x, 3.1)`. Text crums at `1.x` lie below this range and are classified as Case 0 (no shift). Deleting a link via DELETEVSPAN at `2.x` places knife blades within `[2.x, 2.x+width)`. Text crums are at lower V-addresses, so they too are Case 0 — untouched.

**Why the `2.x` extent is independent of `1.x` edits:**

INSERT at `1.x` computes `blade[1] = 2.1` via `findaddressofsecondcutforinsert`, so link crums at `2.1` (or higher) are classified as Case 2 (beyond second blade, no shift) [FC-SUBSPACE, Finding 0054]. DELETE at `1.x` produces a deletion width at `exp=-1`. Link crums have displacement `2.1` at `exp=0`. The `strongsub` exponent guard returns them unchanged since `width.exp < entry.vpos.exp` [FC-SUBSPACE, Finding 0055]. The two mechanisms are distinct: INSERT uses a deliberate structural guard; DELETE uses an incidental arithmetic one [INT-DELETE-SUBSPACE-ASYMMETRY].

**What RETRIEVEDOCVSPANSET reports:**

`retrievevspansetpm()` explicitly decomposes by subspace using `is1story()` and `maxtextwid()` — the text width and link width are computed from independent POOM regions [SS-VSPAN-VS-VSPANSET, Finding 0035]. So the reported extents directly reflect the mutually isolated subspace states.

**The critical caveat — convention, not enforcement:**

`acceptablevsa()` always returns TRUE [SS-SUBSPACE-CONVENTION, Finding 0010]. INSERT can place text at `2.x` [EC-BOUNDARY-INSERT-CLASSIFICATION / PRE-ENF0-PLACEMENT-GAP, Finding 0049] and REARRANGE can displace text across subspace boundaries [PRE-REARRANGE, Finding 0051]. Either violation causes the reported extents to entangle. The invariant holds *only under well-formed caller behavior*.

**Also: RETRIEVEDOCVSPAN does NOT satisfy this invariant.** For mixed-content documents it returns a single bounding-box span that bridges both subspaces — its width changes when either subspace changes [EC-VSPAN-MISLEADING-SIZE, Finding 0035, Bug 0011].

**Summary:** Under the subspace convention, RETRIEVEDOCVSPANSET's `1.x` width is independent of link count and link edits, and the `2.x` extent is independent of text edits — enforced structurally for INSERT by the two-blade knife and incidentally for DELETE by `strongsub`'s exponent guard. Violation of the convention (via unchecked INSERT or cross-subspace REARRANGE) breaks the invariant silently, since the backend provides no guard.

---

## Code Exploration

I now have everything needed for a complete answer. Here it is:

---

## Answer: Subspace Isolation for RETRIEVEDOCVSPANSET Width

### Short Verdict

**Partially yes.** INSERT and DELETE in `1.x` provably do not shift `2.x` (link) POOM crums, and CREATELINK in `2.x` does not shift `1.x` (text) crums. However, the *reported* text width from `RETRIEVEDOCVSPANSET` is a coarse normalized approximation (`width = "1"`) once any link exists — and the output format changes at the exact moment the first link is created. REARRANGE is a genuine exception: it crosses subspace boundaries.

---

### Part 1: INSERT in 1.x Cannot Touch 2.x Crums

**Call chain:**
`doinsert` [`do1.c:87`] → `docopy` [`do1.c:45`] → `insertpm` [`orglinks.c:75`] → `insertnd` [`insertnd.c:15`] → `makegappm` [`insertnd.c:124`]

The key is `makegappm` at `insertnd.c:144–146`:

```c
movetumbler (&origin->dsas[V], &knives.blades[0]);
findaddressofsecondcutforinsert(&origin->dsas[V], &knives.blades[1]);
knives.nblades = 2;
```

`findaddressofsecondcutforinsert` (`insertnd.c:174–183`) computes blade[1]:

```c
int findaddressofsecondcutforinsert(tumbler *position, tumbler *secondcut)
{   /*needs this to give it a place to find intersectionof for text is 2.1*/
  tumbler zero, intpart;
    tumblerclear (&zero);
    tumblerincrement (position, -1, 1, secondcut);       // 1.3 → 2.3
    beheadtumbler (position, &intpart);                  // 1.3 → 0.3
    tumblerincrement(secondcut, 0, -tumblerintdiff(&intpart, &zero), secondcut);  // 2.3 → 2.0
    tumblerincrement (secondcut, 1, 1, secondcut);       // 2.0 → 2.1
}
```

For any insert at `1.x`, blade[1] is always `2.1` — the exact start of the link subspace. The source comment confirms intent: *"needs this to give it a place to find intersectionof for text is 2.1."*

Then `insertcutsectionnd` at `edit.c:207–233`:

```c
if (knives->nblades == 2) {
    i = 1;
    cmp = whereoncrum(ptr, offset, &knives->blades[1], knives->dimension);
    if (cmp <= ONMYLEFTBORDER) {
        return (2);    // NO SHIFT — crum is at or beyond blade[1]
    }
}
```

A link crum at absolute `2.1` with blade[1] = `2.1` gets `ONMYLEFTBORDER`. Classification → case 2. The shift (`tumbleradd`) at `insertnd.c:162` is **never reached** for any `2.x` crum. This protection is **explicit and intentional**.

---

### Part 2: DELETE in 1.x Cannot Touch 2.x Crums — But for a Different Reason

**Call chain:**
`dodeletevspan` [`do1.c:158`] → `deletevspanpm` [`orglinks.c:145`] → `deletend` [`edit.c:31`]

`deletend` at `edit.c:40–41` constructs blades:

```c
movetumbler (origin, &knives.blades[0]);
tumbleradd (origin, width, &knives.blades[1]);
```

Blades are `[1.1, 1.4]` for deleting 3 bytes at 1.1. **There is no `findaddressofsecondcutforinsert` call** — no explicit subspace guard.

`deletecutsectionnd` at `edit.c:235–248`:

```c
for (i = knives->nblades-1; i >= 0; --i) {
    cmp = whereoncrum(ptr, offset, &knives->blades[i], knives->dimension);
    if (cmp <= ONMYLEFTBORDER) return (i+1);
}
```

For a link crum at `2.1` with blades `[1.1, 1.4]`:
- `i=1`: blade `1.4` is `TOMYLEFT` of crum at `2.1`. `TOMYLEFT <= ONMYLEFTBORDER` → return 2.

Case 2 reaches `edit.c:63`: `tumblersub(&ptr->cdsp.dsas[V], width, &ptr->cdsp.dsas[V])`.

This calls `tumblersub(2.1, 0.3)` → `tumbleradd(2.1, -0.3)` → `strongsub(2.1, 0.3)` at `tumble.c:534–547`:

```c
int strongsub(tumbler *aptr, tumbler *bptr, tumbler *cptr)
{
    tumblerclear(&answer);
    if (tumblereq(aptr, bptr)) { ... }
    if (bptr->exp < aptr->exp) {        // bptr->exp(-1) < aptr->exp(0) — TRUE
        movetumbler(aptr, cptr);        // Returns 2.1 UNCHANGED
        return(0);
    }
    ...
}
```

The exponent mismatch between the deletion width (`0.3`, exp=-1) and the link crum's displacement (`2.1`, exp=0) causes `strongsub` to return the minuend unchanged. The link crum is **silently left at `2.1`**.

**Critical asymmetry:** INSERT's guard is deliberate and commented; DELETE's guard is an **accidental property** of `strongsub`'s exponent check. If `strongsub` were "corrected" to handle cross-exponent subtraction, DELETE would break subspace isolation.

---

### Part 3: CREATELINK in 2.x Cannot Touch 1.x Crums

`docreatelink` [`do1.c:195`] calls `findnextlinkvsa` [`do2.c:151`]:

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);   // firstlink = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);   // firstlink = 2.1
(void) doretrievedocvspan (taskptr, docisaptr, &vspan);
tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
if (tumblercmp (&vspanreach, &firstlink) == LESS)
    movetumbler (&firstlink, vsaptr);
else
    movetumbler (&vspanreach, vsaptr);
```

The link is always placed at the **end of the current document V-extent**, which is `>= 2.1`. When `insertpm` is called with `vsaptr = 2.1`, `findaddressofsecondcutforinsert(2.1, blade1)` yields blade[1] = `3.1` (the next subspace boundary). All `1.x` text crums are classified as case 0 or 2 — they **do not shift**.

---

### Part 4: What RETRIEVEDOCVSPANSET Actually Reports

`doretrievedocvspanset` [`do1.c:322`] → `retrievevspansetpm` [`orglinks.c:173`]:

```c
if (is1story (&ccptr->cwid.dsas[V])) {   // Only text, no links
    vspan.stream = ccptr->cdsp.dsas[V];  // Precise start (e.g., 1.1)
    vspan.width  = ccptr->cwid.dsas[V];  // Precise width (e.g., 0.10)
    return TRUE;
} else {                                  // Text + links exist
    // "link part" (stored in linkvspan):
    linkvspan.stream = cwid; linkvspan.stream.mantissa[1] = 0; justify();  // = 1
    linkvspan.width  = cwid; linkvspan.width.mantissa[1] = 0;  justify();  // = 1

    // "text part" (stored in vspan, via maxtextwid):
    maxtextwid(taskptr, ccptr, &voffset=0, &maxwid);  // max absolute position of text crums
    vspan.stream = 0;  // tumblerclear
    vspan.width  = maxwid; vspan.width.mantissa[0] = 0;  // = 0.k
}
```

`maxtextwid` at `orglinks.c:224` recursively walks the POOM, visiting only non-`islinkcrum` nodes. `islinkcrum` at `orglinks.c:255`:

```c
bool islinkcrum(typecorecrum *crumptr)
{
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

A link crum at absolute `2.1` has relative displacement `1.1` from the document root (via `strongsub(2.1, 1.1) = {mant=[1,1]}`). `mantissa[0]==1 && mantissa[1]!=0` → `islinkcrum = TRUE` → **skipped by `maxtextwid`**.

#### The Two Output Spans

| Variable | Stream | Width | Client labels as | Tracks |
|---|---|---|---|---|
| `vspan` | 0 | `0.k` | **link span** (digits[0]==0) | Last text crum's absolute V-position, second digit |
| `linkvspan` | 1 | 1 (always) | **text span** (digits[0]==1) | First digit of root V-width (always "1" while text+links coexist) |

The variable names in the source are reversed relative to the client API convention. The span at `start=1, width=1` is what clients call "text" — it is **always "1"** whenever both text and links exist, regardless of text byte count or link count.

---

### Part 5: Is the Width Invariant?

**The 1.x span (client "text") width = "1":**
- Derived from `ccptr->cwid.dsas[V].mantissa[0]` (first digit of total V-width)
- While text lives in `1.x` and links in `2.x`, the root cwid first digit is always `1`
- **Invariant to:** text INSERT/DELETE (text stays in `1.x`, first digit unchanged), CREATELINK (link goes to `2.x`, first digit unchanged)
- But this "1" is a **coarse normalization** — it tells you "text exists somewhere in 1.x" but not how many bytes

**The 0.x span (client "link") width = "0.k":**
- Derived from `maxtextwid` — the absolute V-position of the highest text crum, with `mantissa[0]` zeroed
- **Changes** when text is inserted or deleted (crums shift, max position changes)
- **Invariant to** CREATELINK (link crums skipped by `maxtextwid`)

**The critical discontinuity:**
When the **first link** is created, the output format switches:
- Before first link: `[{start:"1.1", width:"0.n"}]` — precise byte-level text extent
- After first link: `[{start:"0", width:"0.k"}, {start:"1", width:"1"}]` — normalized approximation

The precise byte-level text width (`0.n`) becomes unrecoverable from `RETRIEVEDOCVSPANSET` after any link is added.

---

### Part 6: REARRANGE Breaks the Invariant

Finding 0051 / golden test `pivot_cross_subspace_boundary.json` confirms: `rearrangend` [`edit.c:78`] uses `makeoffsetsfor3or4cuts` [`edit.c:164`] which computes offsets from raw tumbler differences:

```c
tumblersub (&knives->blades[2], &knives->blades[1], &diff[1]);
```

There is **no subspace guard**. A pivot with cuts at `[1.1, 1.4, 2.5]` moves content from `1.x` to `2.x`. Text bytes end up at link-subspace V-positions. `RETRIEVEDOCVSPANSET` then returns a single span covering both subspaces.

---

### Summary

| Operation | Preserves 1.x/2.x isolation? | Mechanism |
|---|---|---|
| INSERT at 1.x | **Yes** — 2.x crums not shifted | `findaddressofsecondcutforinsert` sets blade[1]=2.1; case 2 = no shift [`insertnd.c:174`, `edit.c:218`] |
| DELETE at 1.x | **Yes** — 2.x crums survive | `strongsub` exponent guard: bptr->exp(-1) < aptr->exp(0) → returns minuend unchanged [`tumble.c:544`] |
| CREATELINK (insert at 2.x) | **Yes** — 1.x crums not shifted | Placed at vspanreach ≥ 2.1; second blade = 3.1; no 1.x crum beyond 3.1 [`do2.c:151`, `insertnd.c:179`] |
| REARRANGE with cross-subspace cuts | **No** | No subspace check in `makeoffsetsfor3or4cuts` [`edit.c:164`] |

**For the specific invariant asked:** the reported `1.x` span width is "1" and unchanging once links exist — INSERT, DELETE, and CREATELINK all leave it at "1". But this "1" is a normalization artifact, not the byte-level text extent. The precise text width is only available when the document has **no links at all**, via the `is1story` fast path in `retrievevspansetpm` [`orglinks.c:184`].
