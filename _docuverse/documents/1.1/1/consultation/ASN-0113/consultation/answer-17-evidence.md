## Question 17 [evidence]

> The KB says RETRIEVEDOCVSPAN is "broken for documents with links — returns a bounding span covering both subspaces" — does RETRIEVEDOCVSPANSET's per-subspace separation come from a distinct traversal that classifies entries by `first_digit(v)`, or from post-processing the same bounding span?

## KB Synthesis

RETRIEVEDOCVSPANSET uses a **distinct traversal** — not post-processing of the bounding span.

The two operations use entirely different functions [SS-VSPAN-VS-VSPANSET, Finding 0035]:

- `RETRIEVEDOCVSPAN` calls `retrievevspanpm()` (`orglinks.c:165-172`): a raw root-node copy that reads `cdsp.dsas[V]` and `cwid.dsas[V]` directly. No subspace awareness whatsoever.
- `RETRIEVEDOCVSPANSET` calls `retrievevspansetpm()` (`orglinks.c:173-221`): a separate function that actively classifies content by subspace.

The classification mechanism in `retrievevspansetpm()` is [SS-DUAL-ENFILADE, Finding 0038]:

1. **`is1story()`** (`tumble.c:237-247`) — tests whether the stored width covers a single subspace or spans multiple subspaces. This is the discriminator, not a digit inspection of a returned span.
2. When multi-subspace is detected, it constructs the link span by **zeroing mantissa[1]** of the stored displacement, and computes the text span via **`maxtextwid()`** (`orglinks.c:224-245`) — a recursive traversal of the enfilade tree to find the actual text extent.

So the per-subspace separation comes from classification *during* the traversal of the enfilade tree, not from decomposing the bounding value that `RETRIEVEDOCVSPAN` returns. The bounding span from `RETRIEVEDOCVSPAN` carries no subspace structure that could be decomposed [SS-VSPAN-VS-VSPANSET, Finding 0035 — "meaningless bounding box"].

---

## Code Exploration

The finding is ready but write permission was denied. Here is the full answer from the source:

---

## RETRIEVEDOCVSPANSET: Distinct Traversal, Not Post-Processing

**Short answer:** The per-subspace separation in RETRIEVEDOCVSPANSET comes from a **distinct traversal**, not from post-processing the bounding span that RETRIEVEDOCVSPAN produces. The two operations diverge at `do1.c:312` vs `do1.c:322` and never share a code path.

---

### RETRIEVEDOCVSPAN — No Traversal, Reads Bounding Box Directly

Call chain: `fns.c:303` → `do1.c:312` → `orglinks.c:165`

```c
// orglinks.c:165-172  retrievevspanpm
bool retrievevspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

Zero traversal. It reads `cdsp.dsas[V]` (displacement) and `cwid.dsas[V]` (width) directly off the root crum and returns them as one span. For a mixed document, `cwid.dsas[V]` is the aggregate bounding width across both subspaces — hence the "broken" bounding span that covers both 0.x and 2.x (1.x internal).

---

### RETRIEVEDOCVSPANSET — Two Separate Extraction Paths

Call chain: `fns.c:129` → `do1.c:322` → `orglinks.c:173` (`retrievevspansetpm`)

For a **text-only** document, `is1story(&ccptr->cwid.dsas[V])` is true (`orglinks.c:184`) and it returns a single span, matching RETRIEVEDOCVSPAN.

For a **mixed document**, the code splits into two completely separate extraction paths — the comment at `orglinks.c:192` is explicit:

```c
/* the link part is simple, just grab the last digit off the wid */
/* the text part we get from a max function that delves into the crums */
/* in both cases we have to remove the first digit of the tumbler, the 1 and hack it around a bit. */
```

**Link span** (`orglinks.c:197-203`): taken directly from root crum's `cwid.dsas[V]`, then `mantissa[1]` is zeroed to isolate the link-subspace digit:
```c
movetumbler (&ccptr->cwid.dsas[V], &linkvspan.stream);
linkvspan.stream.mantissa[1] = 0;
tumblerjustify(&linkvspan.stream);
```

**Text span** (`orglinks.c:207-211`): computed by calling `maxtextwid()`, then `mantissa[0]` is zeroed to strip the subspace prefix:
```c
maxtextwid(taskptr, ccptr, &voffset, &maxwid);
...
vspan.width.mantissa[0] = 0;
```

---

### `maxtextwid` — The Actual Distinct Traversal

`orglinks.c:224` walks the enfilade tree recursively, accumulating the maximum V-extent, **skipping link crums**:

```c
// orglinks.c:239-241
for (ptr = findleftson((typecuc*)crumptr); ptr; ptr = findrightbro(ptr)) {
    if (ptr && !islinkcrum(ptr)) {  /* only look for text or overlapping stuff */
        maxtextwid(taskptr, ptr, &localvoffset, maxwidptr);
```

The crum classification uses mantissa-digit inspection:

- **`istextcrum`** (`orglinks.c:246`): `cdsp.mantissa[1] == 0 && is1story(cwid)` — crum entirely in text subspace
- **`islinkcrum`** (`orglinks.c:255`): `cdsp.mantissa[0] == 1 && cdsp.mantissa[1] != 0` — displacement is 1.N form, placing crum in link subspace

This is the functional equivalent of `first_digit(v)` classification. The mantissa array directly encodes the tumbler digits: mantissa[0]=1 and mantissa[1]≠0 means the crum's V-displacement is in the link subspace.

---

### Why RETRIEVEDOCVSPAN Is "Broken"

`retrievevspanpm` reads the stored bounding box from the root crum without inspecting the enfilade structure at all. The root crum's `cwid.dsas[V]` is the minimum bounding width over all children — which for a document containing both text crums (at 1.x) and link crums (at 0.x) produces a width that spans from 0.x to the end of 1.x. There is no subspace distinction at that level.

`retrievevspansetpm` avoids this by never consulting the root's bounding width for the text span — it re-derives text extent through `maxtextwid`'s tree walk.
