## Question 3 [evidence]

> When CREATELINK adds the first link to a document with an empty link subspace, what exact V-position (tumbler depth and components, e.g. under `docISA.0.2`) does udanax-green assign it, and is that depth fixed or derived from anything?

## KB Synthesis

## First Link V-Position and I-Address

There are two distinct addresses involved in the first CREATELINK, and the KB is explicit about both.

---

### V-Position in the Document POOM: `2.1`

This is **fixed**, not derived from the document's ISA structure.

`findnextlinkvsa` in `do2.c:151-167` computes the first link's V-position by performing two tumbler increments on a zero tumbler: first to `2.0`, then to `2.1`. It does not consult the document's address depth or ISA to derive this position — the value `2.1` is hardcoded arithmetic. [SS-LINK-SUBSPACE], [SS-DUAL-ENFILADE]

Subsequent links are placed at `vspanreach` (end of current document extent), so they get `2.2`, `2.3`, etc. [SS-LINK-SUBSPACE]

The leading `2` in the V-position is the subspace identifier — mantissa[0] = 2 designates the link subspace, as opposed to mantissa[0] = 1 for text. This is the three-subspace convention (`1.x` = text, `2.x` = links, `3.x` = type endpoints). [SS-SUBSPACE-CONVENTION] (Finding 0038)

---

### I-Address of the Link Orgl: `docISA.0.2.1`

The link orgl itself receives an I-address allocated under the document's address namespace via `findisatoinsertmolecule`. The structure is:

```
account.0.document.0.element_field.element_number
                        ↑             ↑
                        2 = links     1 = first link
```

For document `1.1.0.1.0.1`, the first link orgl gets I-address `1.1.0.1.0.1.0.2.1`. [SS-ADDRESS-SPACE] (Finding 0065), [SS-LINK-HOME-DOCUMENT]

The `.0.` separator is a T4 tumbler field separator; the `2` is the element_field constant for `LINKATOM` (distinct from `3` for text atoms). The element_number `1` is allocated by the same `findpreviousisagr` + `tumblerincrement` query-and-increment mechanism as text. [SS-ADDRESS-ALLOC]

The allocation bound is set to `docISA.2.3` (upper), constraining the search to the document's link subspace. When no links yet exist (`lowerbound < docISA.2.2`), the first allocation lands at `docISA.2.2.1`. [SS-ADDRESS-SPACE] (Finding 0065)

---

### Depth is Fixed, Not Derived

The V-position depth (`2.1`) is fixed by the hardcoded increment sequence in `findnextlinkvsa`. The I-address depth is fixed by `makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint)` which encodes document-scoped element allocation — the element field `2` for `LINKATOM` is a compile-time constant, not derived from the document's own address depth. [SS-ADDRESS-SPACE] (Finding 0065), [ST-CREATE-LINK]

---

## Code Exploration

I now have everything I need. Let me compile the full answer from the code trace.

---

## Answer: V-Position Assigned by CREATELINK for the First Link

### Call Chain

```
fns.c:100  createlink()
  └─ do1.c:195  docreatelink()
       ├─ do2.c:48   tumbler2spanset()   — wraps link ISA as a 1-wide ispan
       ├─ do2.c:151  findnextlinkvsa()   ← determines the V-position
       └─ do1.c:212  docopy()            — places link ISA at that V-position
```

---

### `findnextlinkvsa()` — the V-position oracle

`do2.c:151-167`:
```c
bool findnextlinkvsa(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr)
{
  tumbler vspanreach, firstlink;
  typevspan vspan;
  bool doretrievedocvspan();
    tumblerclear (&firstlink);
    tumblerincrement (&firstlink, 0, 2, &firstlink);  // step 1
    tumblerincrement (&firstlink, 1, 1, &firstlink);  // step 2

    (void) doretrievedocvspan (taskptr, docisaptr, &vspan);
    tumbleradd (&vspan.stream, &vspan.width, &vspanreach);
    if (tumblercmp (&vspanreach, &firstlink) == LESS)
        movetumbler (&firstlink, vsaptr);   // ← empty doc takes this branch
    else
        movetumbler (&vspanreach, vsaptr);
    return (TRUE);
}
```

---

### Decoding the `firstlink` tumbler

The tumbler struct is `{exp, mantissa[NPLACES]}` (`common.h:59-65`, `NPLACES=16` per `common.h:53`).

`tumblerincrement()` semantics (`tumble.c:599-623`):

> When `aptr` is zero: set `exp = -rightshift`, `mantissa[0] = bint`.  
> Otherwise: find the last non-zero mantissa index `idx`, write `bint` at `mantissa[idx + rightshift]`.

**Step 1** — `tumblerincrement(&firstlink, 0, 2, &firstlink)`, input is zero:
- `exp = -0 = 0`, `mantissa[0] = 2`
- Result: `{exp=0, mantissa=[2, 0, 0, ...]}`  → tumbler **"2"**

**Step 2** — `tumblerincrement(&firstlink, 1, 1, &firstlink)`, input is `{exp=0, mantissa=[2,0,...]}`:
- Last non-zero index: `idx = 0` (mantissa[0]=2)
- Write at `mantissa[0 + 1] = mantissa[1]`: `mantissa[1] += 1`
- Result: `{exp=0, mantissa=[2, 1, 0, 0, ...]}`  → tumbler **"2.1"**

Depth check via `tumblerlength()` (`tumble.c:259-261`):
- `nstories({mantissa=[2,1,0,...]}) = 2` (last non-zero is at index 1)
- `tumblerlength = nstories - exp = 2 - 0 = **2**`

**`firstlink = 2.1`, depth 2.**

---

### Why the empty-document branch always reaches `2.1`

For a new document with no prior links and no text, `doretrievedocvspan` → `retrievevspanpm` (`orglinks.c:165-172`) reads the root crum's fields directly:

```c
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
```

A freshly-allocated orgl has both fields zeroed. So `vspan.stream = 0`, `vspan.width = 0`, `vspanreach = 0`.

`tumblercmp(0, "2.1") == LESS` → `firstlink` is used.

`acceptablevsa()` (`do2.c:110-113`) is a no-op — it always returns `TRUE` — so `2.1` passes validation unconditionally.

**The first link in any empty link subspace always lands at V = `2.1`.**

---

### Is the depth fixed or derived?

The sentinel `firstlink = 2.1` is **hardcoded** — two `tumblerincrement` calls with literal constants `(0, 2)` then `(1, 1)`. It is not computed from the document ISA, from the document's content, or from any runtime state. The depth-2 shape is a compile-time invariant.

The *position* becomes dynamic only if the document's V-span already extends past `2.1` (i.e., a second or later link; or a text insertion that somehow reaches into link territory — which the subspace convention prevents). For the *first* link in an empty document, `2.1` is always the result.

---

### The `0` vs `2.1` display confusion

Finding 0038 (and the recent `fix(findings)` commits) document this: `retrievedocvspanset` post-processes the output via `retrievevspansetpm` (`orglinks.c:173-221`). When the document contains both text and links, it reports the link span with `mantissa[1]` zeroed and justified, which makes the leading component appear as `0` in external notation. That `0` is a **display normalization**, not the internal V-address. The internal V-address is always `2.1` for the first link.

When only links exist (no text), `retrievevspansetpm` takes the `is1story` branch and returns the real stored position — `{"start": "2.1", "width": "0.1"}` — consistent with the internal representation.

---

### Summary

| Property | Value | Source |
|---|---|---|
| Internal V-position, first link | **`2.1`** | `do2.c:156-158` |
| Tumbler depth | **2** | `tumble.c:259-261`, `nstories=2`, `exp=0` |
| `mantissa[0]` | **2** (link subspace) | `do2.c:157` |
| `mantissa[1]` | **1** (first element) | `do2.c:158` |
| Fixed or derived? | **Fixed** — hardcoded sentinel | `do2.c:156-158` |
| Link subspace boundary | **`2`** (one-component) | `orglinks.c:37` (`findvsatoappend`, same constant) |
| External display (with text present) | `"0"` or `"0.1"` | `orglinks.c:196-203` (`retrievevspansetpm` normalization) |
| `acceptablevsa` check | No-op — always `TRUE` | `do2.c:110-113` |

The V-position `2.1` sits under the document's link subspace boundary `2`, which is the same constant used in `findvsatoappend` (`orglinks.c:37`). The notation `docISA.0.2.1` that appears in I-addresses (e.g., `1.1.0.1.0.1.0.2.1`) contains the `2.1` as its element field after a field-separator `0` — but that is the link's **ISA** (its identity in I-space), not its **V-position**. The V-position is simply the two-component tumbler `2.1`, relative to the hosting document's internal V-space.
