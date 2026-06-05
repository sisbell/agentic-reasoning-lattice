## Question 11 [evidence]

> When RETRIEVEDOCVSPAN reports the root width of a document containing both text (1.x) and link (2.x) subspaces, does the returned span's width tumbler bridge across the inter-subspace gap, and what start position does it report?

## KB Synthesis

Yes — RETRIEVEDOCVSPAN bridges the inter-subspace gap, and the result is a semantically meaningless bounding box.

**Start position**: The root node's V-dimension displacement (`cdsp.dsas[V]`) points to the start of the text subspace at position `1`. So the returned start is the first occupied text position, e.g., `1.1`. [SS-DUAL-ENFILADE, Finding 0043]

**Width tumbler**: The root's `cwid.dsas[V]` is the raw structural width — the maximum V-extent minus the minimum. Because link orgls occupy `2.x` internally and text occupies `1.x`, the root width spans both, yielding a tumbler like `1.2`. This means the span runs `1.1` to `1.1 + 1.2 = 2.3`, bridging straight across the gap between subspaces. [SS-VSPAN-VS-VSPANSET Finding 0035, EC-VSPAN-MISLEADING-SIZE]

**Concrete reported result**: `1.1 for 1.2` (Bug 0011). [SS-VSPAN-VS-VSPANSET Finding 0017]

The mechanism: `retrievevspanpm()` is a raw root-copy — no subspace awareness, no gap detection. [SS-VSPAN-VS-VSPANSET Finding 0035, `orglinks.c:165-172`]

Callers must use RETRIEVEDOCVSPANSET instead, which uses `retrievevspansetpm()` with the `is1story()` check to decompose into per-subspace spans correctly. [SS-VSPAN-VS-VSPANSET, PRE-CONTENT-ITERATION]

---

## Code Exploration

I now have all the evidence I need from the source code and golden tests. Let me compile the complete answer.

---

## RETRIEVEDOCVSPAN with Mixed Text (1.x) and Link (2.x) Subspaces

### Call Path

**`fns.c:303–315`** — `retrievedocvspan()` calls `doretrievedocvspan()`.

**`do1.c:312–320`** — `doretrievedocvspan()`:
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

**`orglinks.c:165–172`** — `retrievevspanpm()`:
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

This is a **direct raw copy** of the root crum's V-dimension displacement and width. No subspace decomposition happens here.

---

### How Root Width Is Computed

**`wisp.c:171–228`** — `setwispnd()` computes the root crum's `cdsp` and `cwid` from its children each time the tree is modified:

```c
// Step 1: find minimum displacement across children → becomes new root cdsp
movewisp (&ptr->cdsp, &mindsp);
for (ptr = getrightbro(ptr); ptr; ...)
    lockmin (&mindsp, &ptr->cdsp, &mindsp, dspsize);
...
// Step 2: children's cdsp adjusted by - mindsp (leftmost child → relative dsp=0)
// Step 3: root cwid = max over all children of (adjusted_cdsp + cwid)
lockadd((tumbler*)&ptr->cdsp, (tumbler*)&ptr->cwid, (tumbler*)&tempwid, widsize);
lockmax((tumbler*)&newwid, (tumbler*)&tempwid, (tumbler*)&newwid, widsize);
```

The root's `cwid.dsas[V]` is the **bounding-box reach** — the maximum V-endpoint across every child crum, computed without any subspace awareness.

---

### What `is1story` Reveals

**`tumble.c:237–247`** — `is1story` returns TRUE only if `mantissa[1]` through `mantissa[NPLACES-1]` are all zero:
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

**`orglinks.c:184`** in `retrievevspansetpm()`:
```c
if (is1story (&ccptr->cwid.dsas[V])) { /* if it is  just text return that */
```

When text crums (V ≈ 1.x) and link crums (V ≈ 2.x) both exist, `setwispnd`'s max-reach computes a width like `1.2` — a **2-story tumbler** (mantissa[0]=1, mantissa[1]=2). `is1story` returns FALSE for this value. This is the branching condition that `retrievevspansetpm` uses to know the document is mixed — but `retrievevspanpm` (used by RETRIEVEDOCVSPAN) ignores this entirely and just returns the raw value.

---

### Confirmed by Golden Tests

**`golden/documents/retrieve_vspan.json`** — text-only ("Hello World", 11 chars):
- `retrieve_vspan` → `at 1.1 for 0.11`
- `retrieve_vspanset` → single span `{start: "1.1", width: "0.11"}`
- Width `0.11` is a 1-story tumbler (exp=−1, mantissa[0]=11): `is1story` returns TRUE.

**`golden/documents/retrieve_vspan_with_links.json`** — "Click here" (10 chars) + one link:
- `retrieve_vspan` → `at 1.1 for 1.2`
- `retrieve_vspanset` → two spans: `{start:"0", width:"0.1"}` (text) and `{start:"1", width:"1"}` (link)
- Width `1.2` is a 2-story tumbler (mantissa[0]=1, mantissa[1]=2): `is1story` returns FALSE.

---

### Does the Width Bridge the Inter-Subspace Gap?

**Yes — numerically, as a bounding-box artifact.** `retrievevspanpm` returns a single `typevspan` with:

| Field | Value | Meaning |
|-------|-------|---------|
| `stream` | `1.1` | Root `cdsp.dsas[V]`: absolute V-address of leftmost content (first text insertion) |
| `width` | `1.2` | Root `cwid.dsas[V]`: 2-story bounding-box tumbler spanning both subspaces |

The `stream + width` in tumbler arithmetic crosses the subspace boundary into the 2.x range. Digit 0 of the width (`1`) encodes the inter-subspace gap distance; digit 1 (`2`) encodes the link's position within link space. The returned single vspan nominally covers the entire V-range from `1.1` to the end of the link, including the empty void between subspaces.

**This is not semantically meaningful as content.** The empty gap between 1.x and 2.x contains no insertions. `RETRIEVEDOCVSPANSET` (`orglinks.c:173–221`) correctly decomposes this into two spans using `is1story` + `maxtextwid`, but `RETRIEVEDOCVSPAN` bypasses that logic entirely by calling `retrievevspanpm` instead of `retrievevspansetpm`.

### Start Position

The start is always the root's `cdsp.dsas[V]`, which after `setwispnd` normalization equals the absolute V-address of the document's **leftmost V-content**. For a document where text is inserted first, this is the text insertion address — `1.1` in both golden tests above [`do1.c:318–319`, `orglinks.c:169`].

### Summary

RETRIEVEDOCVSPAN returns one span: `start = 1.1` (text subspace start), `width = 1.2` (a 2-story tumbler that bridges across the subspace gap). The bridging is real arithmetic — `stream + width` lands in the 2.x link range — but the span is a raw bounding box, not a semantic content range. Use RETRIEVEDOCVSPANSET to get properly decomposed per-subspace spans.
