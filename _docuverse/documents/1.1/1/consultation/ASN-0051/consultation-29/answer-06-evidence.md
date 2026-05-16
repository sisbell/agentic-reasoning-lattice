## Question 6 [evidence]

> Does udanax-green implement broader-level spans (action-points at field positions ≤ p₃), and if so, what survivability or growth behavior does the implementation exhibit when new allocations occur within such spans' reach?

## KB Synthesis

The KB does not contain information sufficient to answer this question as phrased. The concept of "broader-level spans (action-points at field positions ≤ p₃)" does not appear in any finding — that formalism is not documented in the implementation evidence extracted so far.

What the KB **does** say about span behavior at different hierarchy levels:

**Upper crum width updates**: When content is inserted within a 2D enfilade node's range, `setwispupwards` recalculates widths and displacements up the tree, so upper crums' extents grow to encompass new insertions [ST-INSERT, Finding 0066; INV-ENFILADE-RELATIVE-ADDRESSING].

**Bottom crum coalescing**: Bottom crums can extend rightward via `isanextensionnd` when new content shares `homedoc` and the origin equals the crum's reach — but this is asymmetric, rightward-only [ST-INSERT, Finding 0062; ST-CRUM-BOUND].

**No contraction**: Tree height is monotonically non-decreasing (`levelpull` is disabled), so broader spans never collapse [SS-ENFILADE-TREE, Finding 0058].

**Split on overflow**: Upper crums split when `toomanysons` is triggered, governed by `MAXUCINLOAF=6` [SS-ENFILADE-BRANCHING; SS-SPLIT].

If your question is drawing on enfilade theory from the Xanadu literature (e.g., Theodor Nelson's formalism), the KB does not bridge that theory to the implementation. You would need findings specifically probing that mapping.

---

## Code Exploration

I now have sufficient evidence from the source code to give a complete answer.

---

## Does udanax-green implement broader-level spans?

**No.** The implementation contains no broader-level span mechanism. Every claim below is traced to a specific line.

---

### 1. The tumbler has 16 places — but only two are ever indexed

`common.h:53`:
```c
#define NPLACES 16
```

`common.h:64`:
```c
tdigit mantissa[NPLACES];
```

The 16-place mantissa is allocated, but a search of every `.c` file for `mantissa[2]`, `mantissa[3]`, and `mantissa[4]` returns **zero matches**. Field positions p₃ and beyond are declared but dead — no span logic ever reads or writes them.

The only direct mantissa-index accesses in the entire codebase are:

| File | Line | Access | Purpose |
|------|------|--------|---------|
| `spanf1.c` | 39 | `lwidth.mantissa[1] = textset->length` | Character count → span width |
| `do1.c` | 105, 108, 111, 113 | `mantissa[1]` | Commented-out debug probe |
| `sporgl.c` | 230 | `nullhomeset.width.mantissa[0] = 100` | Sentinel width for null home |
| `tumble.c` | 180, 186, 192 | `mantissa[0]` | Zero-tumbler checks |
| `iszerotumbler` macro | `common.h:72` | `mantissa[0]` | "Is this tumbler zero?" predicate |

p₂ (`mantissa[1]`) carries character offset; p₁ (`mantissa[0]`) carries document/link identity. p₃ and deeper are structurally present but semantically inert.

---

### 2. Span struct carries no level or action-point field

`xanadu.h:65–76`:
```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid      itemid;
    tumbler stream;
    tumbler width;
} typespan;
typedef typespan typevspan;
typedef typespan typeispan;
```

A span is exactly two tumblers: `stream` (start address) and `width` (extent). There is no `level`, no `actionpoint`, no `fieldpos`, and no flag distinguishing broader from narrower spans. `typevspan` and `typeispan` are the same struct; the distinction is purely by naming convention at call sites, not by any structural difference.

---

### 3. Insertions write span endpoints verbatim — no growth

`spanf1.c:25–51` (`insertspanf`):
```c
for (; sporglset; ...) {
    if (... ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);  // line 27
        movetumbler (&((typeispan *)sporglset)->width,  &lwidth);   // line 28
    }
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  // line 49
    movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);   // line 50
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // line 51
}
```

`movetumbler` is a struct-copy macro (`common.h:73`): `#define movetumbler(A,B) (*((tumbler*)(B)) = *((tumbler*)(A)))`. The source coordinates are written directly into the enfilade. No arithmetic adjusts them; no existing node is widened.

The same pattern appears in `insertpm` (`orglinks.c:75–160`), which stores span endpoints into the POOM (permutation matrix) enfilade. Both paths use `movetumbler` + `insertnd` with the coordinates taken literally from the caller.

---

### 4. V↔I conversion is computed fresh, not stored with growing endpoints

The path that converts between V-space (version) and I-space (internal) spans is:

```
ispan2vspanset / vspanset2ispanset   [orglinks.c:389-402]
  └─ permute()                        [orglinks.c:404-422]
       └─ span2spanset()              [orglinks.c:425-454]
            └─ retrieverestricted()   [retrie.c:56-80]
            └─ context2span()         [context.c:176-212]
```

`context2span` [context.c:176–212] clips the context's `grasp`/`reach` interval against the restriction span using `tumblercmp` and `tumblerincrement`. The computation is read-only: it produces a new `foundspan` that represents the intersection of the query and what the enfilade knows, then returns it. No stored endpoint is modified.

```c
// context.c:191-207
if (tumblercmp (&grasp.dsas[idx1], &lowerbound) == LESS)
    tumblerincrement (&grasp.dsas[idx2], 0, (INT)tumblerintdiff(...), &grasp.dsas[idx2]);
if (tumblercmp (&reach.dsas[idx1], &upperbound) == GREATER)
    tumblerincrement (&reach.dsas[idx2], 0, -tumblerintdiff(...), &reach.dsas[idx2]);
movetumbler (&grasp.dsas[idx2], &foundspanptr->stream);
tumblersub(&reach.dsas[idx2], &grasp.dsas[idx2], &foundspanptr->width);
```

This is clipping, not growth. The freshly computed `foundspan` exists only in local scope; it is copied to an output list by `onitemlist` [orglinks.c:444] and then `contextfree` releases the context.

---

### 5. Link creation stores endpoints at creation time, frozen thereafter

`do1.c:195–221` (`docreatelink`):
```c
&& specset2sporglset(taskptr, fromspecset, &fromsporglset, ...)
&& specset2sporglset(taskptr, tospecset,   &tosporglset,   ...)
&& insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
&& insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
```

`specset2sporglset` converts the caller's V-space specsets to I-space sporglsets at the moment of link creation [do2.c:14–46]. Those i-spans are then written into both the link's own orgl and the spanfilade via `insertspanf`. Once written, there is no code path that revisits a stored link endpoint and grows it in response to later insertions elsewhere.

---

### 6. No concept matching "action-point" or field-position gating

A full-text search of all `.c` files for `level`, `p3`, `action.point`, `broader`, `narrower`, `field.pos` finds no matches in span-related logic. The word "level" appears only in `spanf2.c:10`'s comment `/* lower-level spanfilade calls */` — an English word for "abstraction tier," not a Xanadu span concept.

---

## Answer

Udanax-green does **not** implement broader-level spans. The implementation is a flat, static-endpoint model:

- **Span structure**: two tumblers (`stream`, `width`) with no level or action-point field [`xanadu.h:65–70`].
- **Storage**: span endpoints are copied verbatim into the enfilade at creation time via `movetumbler` + `insertnd` [`spanf1.c:49–51`]. No subsequent insertion modifies them.
- **Retrieval**: V↔I conversion clips intervals against a query restriction [`context.c:191–207`]; it never widens stored endpoints.
- **Tumbler depth**: the 16-place mantissa is allocated but only `mantissa[0]` (identity/type) and `mantissa[1]` (character offset) are ever used [`common.h:53`, `spanf1.c:39`]. Field position p₃ (`mantissa[2]`) and deeper are structurally present and semantically dead.

When new content is inserted into a document (via `doinsert` → `inserttextgr` → `inserttextgr` in `granf2.c:83–120`), the granfilade sequence is extended and new crum nodes are created. Existing link endpoints stored in the spanfilade are untouched. A link created to span characters 5–10 of a document will still describe characters 5–10 after one thousand subsequent insertions. There is no survivability or growth behavior — udanax-green implements the narrow, fixed-reference model of Xanadu links only.
