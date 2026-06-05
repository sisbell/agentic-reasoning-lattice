## Question 11 [evidence]

> When RETRIEVEDOCVSPANSET reads a multi-span specset, does it return the text subspace (1.x) and link subspace (internal 2.x, normalized 0.x) as separate VSpecs, or interleaved within one ordered result?

## KB Synthesis

RETRIEVEDOCVSPANSET returns them as **separate VSpecs**, one per occupied subspace — not interleaved.

The implementation in `retrievevspansetpm()` (`orglinks.c:173-221`) uses an `is1story` check to detect whether the document spans multiple subspaces, then explicitly constructs distinct spans for each. [SS-DUAL-ENFILADE Finding 0038, Finding 0043]

For a document with both text and links, the output is two VSpecs in fixed order:

```json
[{"start": "0", "width": "0.1"}, {"start": "1", "width": "1"}]
```

The link span comes first (normalized from internal `2.x` to `"0"` when text is also present), followed by the text span (at `"1"`). [SS-DUAL-ENFILADE Finding 0038]

If only links exist (no text), the link span is reported at its actual internal position `"2.1"` instead of `"0"`. [SS-VSPAN-VS-VSPANSET Finding 0017, Finding 0035]

This contrasts with RETRIEVEDOCVSPAN (opcode 14), which reads the raw root displacement/width and returns a single bounding span bridging both subspaces — a meaningless value for mixed-content documents. [SS-VSPAN-VS-VSPANSET Finding 0035]

---

## Code Exploration

I have all I need. Here is my complete answer.

---

## RETRIEVEDOCVSPANSET: Text vs. Link Subspace in Multi-Span Results

**Short answer:** Both subspaces are returned **interleaved within a single ordered vspanset** — not as two separate VSpec lists. The result is one linked list sorted by V-space stream address.

---

### Execution Chain

**1. FEBE handler — `fns.c:129-141`**

```c
void retrievedocvspanset(typetask *taskptr)
{
  typeisa docisa;
  typevspanset vspanset;
  bool getretrievedocvspanset(), doretrievedocvspanset();

    if (
       getretrievedocvspanset (taskptr, &docisa)
    && doretrievedocvspanset (taskptr, &docisa, &vspanset))
        putretrievedocvspanset (taskptr, &vspanset);
      else
        putrequestfailed (taskptr);
}
```

There is **one** `vspanset` variable. It is populated by `doretrievedocvspanset` and serialized by `putretrievedocvspanset` as a unit.

---

**2. Document lookup — `do1.c:322-336`**

```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
  typeorgl docorgl;
  bool findorgl(), isemptyorgl(), retrievevspansetpm();

    if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
        return FALSE;

    if (isemptyorgl (docorgl)) {
        *vspansetptr = NULL;
        return TRUE;
    }

    return retrievevspansetpm (taskptr, docorgl, vspansetptr);
}
```

`findorgl` locates the root crum via the granfilade. An empty document returns `NULL`. Otherwise the single `vspansetptr` is filled by `retrievevspansetpm`.

---

**3. The span-building function — `orglinks.c:173-221`**

This is the key function. There are **two definitions** of `retrievevspansetpm` in the file. The second (lines 266-275) is wrapped in `#ifdef UnDEFined` and is **dead code**. Only the first is compiled.

```c
bool retrievevspansetpm(typetask *taskptr, typeorgl orgl, typevspanset *vspansetptr)
{
  tumbler voffset, maxwid;
  typevspan vspan, linkvspan;
  typecorecrum *ccptr;
    ccptr = (typecorecrum *) orgl;
    tumblerclear (&voffset);
    *vspansetptr = NULL;

    if (is1story (&ccptr->cwid.dsas[V])) {   /* pure text: single-story width */
        vspan.itemid = VSPANID;
        movetumbler (&ccptr->cdsp.dsas[V], &vspan.stream);
        movetumbler (&ccptr->cwid.dsas[V], &vspan.width);
        vspan.next = NULL;
        putvspaninlist (taskptr, &vspan, vspansetptr);   // ONE span
        return TRUE;
    } else {
        /* multi-span: both text and link content exist */

        /* link span: grab cwid, zero the sub-axis digit */
        linkvspan.itemid = VSPANID;
        movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream); // (cdsp line is commented out)
        linkvspan.stream.mantissa[1] = 0;
        tumblerjustify(&linkvspan.stream);
        movetumbler (&ccptr->cwid.dsas[V], &linkvspan.width);
        linkvspan.width.mantissa[1] = 0;
        tumblerjustify(&linkvspan.width);
        linkvspan.next = NULL;

        /* text span: walk crums for max V-width, zero the major-axis digit */
        maxtextwid(taskptr, ccptr, &voffset, &maxwid);
        vspan.itemid = VSPANID;
        tumblerclear (&vspan.stream);
        movetumbler (&maxwid, &vspan.width);
        vspan.width.mantissa[0] = 0;
        vspan.next = NULL;

        putvspaninlist (taskptr, &vspan, vspansetptr);      // line 216
        putvspaninlist (taskptr, &linkvspan, vspansetptr);  // line 217
        return (TRUE);
    }
}
```

**Both spans go into the same `*vspansetptr`.**

The branching logic:
- `is1story` (`tumble.c:237-247`) returns TRUE when all `mantissa[i]` for i≥1 are zero — meaning the document's cwid is a single-component tumbler. This is the pure-text case.
- When the cwid is multi-story (mantissa[1] ≠ 0), the document spans both subspaces and the `else` branch fires.

Crum classification used by `maxtextwid` (`orglinks.c:224-244`, `246-260`):
- **Text crum** (`istextcrum`, line 246): `cdsp.dsas[V].mantissa[1] == 0` AND `is1story(cwid)` — displaced only in the major V-axis.
- **Link crum** (`islinkcrum`, line 255): `cdsp.dsas[V].mantissa[0] == 1` AND `mantissa[1] != 0` — displaced into the nested `1.n` sub-axis where n ≠ 0.

`maxtextwid` recurses through child crums, skipping any `islinkcrum` node (`orglinks.c:240`), accumulating the maximum V-extent of text crums only.

---

**4. Ordering — `putvspaninlist` at `orglinks.c:329-387`**

```c
int putvspaninlist(typetask *taskptr, typevspan *spanptr, typevspanset *spansetptr)
{
  typevspan *ptr, *last, *makevspan();
  tumbler newspanend, oldspanend;
  INT startcmp, endcmp, spancmp;
    ptr = *spansetptr;
    last = NULL;
    if (!ptr) {
        *spansetptr = makevspan (taskptr, spanptr, (typevspan*)NULL);
        return(0);
    }
    for (; ptr; last = ptr, ptr = ptr->next) {
        tumbleradd (&spanptr->stream, &spanptr->width, &newspanend);
        tumbleradd (&ptr->stream, &ptr->width, &oldspanend);
        spancmp = tumblercmp (&spanptr->stream, &oldspanend);
        if (!spancmp) {
            tumbleradd (&ptr->width, &spanptr->width, &ptr->width); // merge
            return(0);
        } else if (spancmp == GREATER)
            continue;   // new span starts after this existing span; keep scanning
        // ... insert at correct sorted position
    }
    last->next = makevspan (taskptr, spanptr, (typevspan*)NULL);
}
```

The function maintains a **sorted linked list ordered by stream position**. Adjacent or overlapping spans are merged. There is no grouping by subspace type — spans from text and link subspace are simply placed wherever their stream address falls.

---

**5. Serialization — `putfe.c:248-251` / `put.c:60-71`**

```c
int putretrievedocvspanset(typetask *taskptr, typespanset *spansetptr)
{
    putnumber (taskptr->outp, RETRIEVEDOCVSPANSET);
    putitemset (taskptr, (typeitemset)*spansetptr);
}
```

```c
int putitemset(typetask *taskptr, typeitemset itemset)
{
    if (itemset == NULL){ ... return(0); }
    for (; itemset; itemset = (typeitemset)((typeitemheader *)itemset)->next) {
        putitem (taskptr, itemset);
        ...
    }
}
```

`putitemset` walks a **single `->next` chain**. There is no outer loop over subspaces.

---

### Dead Alternate Implementation

The `#ifdef UnDEFined` block (`orglinks.c:263-313`) contains `walkorglonvpm`, which would recursively walk every leaf crum, accumulate one vspan per leaf, and then merge adjacent spans via `cleanupvspanlist`. This would produce a richer, fully decomposed result — but it is **never compiled**. The active implementation at line 173 uses a coarser two-span approximation.

---

### Summary

For a **pure-text document** (single-story cwid): RETRIEVEDOCVSPANSET returns **one VSpan** covering the entire text content. No link span appears.

For a **multi-span document** (multi-story cwid, containing both text and link content): RETRIEVEDOCVSPANSET returns **two VSpans in one ordered vspanset**:
- A text span: stream=0, width = max text V-extent with the major-axis component zeroed (`mantissa[0]=0`)
- A link span: stream and width both derived from the root cwid with the sub-axis component zeroed (`mantissa[1]=0`)

Both are inserted into the **same** vspanset by `putvspaninlist` (orglinks.c:216-217), sorted by stream address, and serialized as a single flat linked list. There is no structural separation by subspace — they are interleaved in V-space address order within one result.

One note: the link span's stream is assigned from the root's **cwid** (not cdsp), and the `movetumbler(&ccptr->cdsp.dsas[V], &linkvspan.stream)` line is commented out at orglinks.c:196. This means the link span's start address reflects total document width rather than a displacement — a construction oddity that may reflect an incomplete or intentionally simplified encoding of link-space extent.
