## Question 19 [evidence]

> If a SpecSet crosses into the link subspace (`2.x` internally), does content delivery return link-orgl I-address bytes, or is delivery restricted to text subspace `1.x`?

## KB Synthesis

## Content Delivery When SpecSet Crosses Into Link Subspace

**Short answer:** Delivery is not restricted to `1.x`. The system silently returns garbage bytes or NULL for link-orgl I-addresses, mixed with valid text bytes — no error is raised.

---

### The delivery path is type-agnostic end-to-end

`doretrievev` calls `specset2ispanset` then `ispanset2vstuffset(taskptr, granf, ispanset, vstuffsetptr)` [PRE-RETRIEVE-CONTENTS, Finding 0010]. Both functions are fully type-agnostic — they treat all I-addresses as flat tumblers with no subspace awareness [SS-SUBSPACE-CONVENTION, Findings 0009/0010/0011].

The V→I conversion (`specset2ispanset`) faithfully maps the `2.x` V-positions to their stored I-addresses, which happen to be link orgl ISAs (e.g., `1.1.0.1.0.1.0.2.1`).

### What `ispanset2vstuffset` does with link ISAs

`ispanset2vstuffset` performs a permascroll lookup [SS-GRANF-OPERATIONS]. A link orgl ISA is **not** a permascroll address — it lives in a completely different part of the granfilade tree. The lookup produces NULL or garbage bytes, returned silently:

> "Looking up a link ISA in the permascroll produces NULL or garbage bytes — a silent failure."
> — [PRE-RETRIEVE-CONTENTS, Finding 0010]

The concrete consequence [SS-SUBSPACE-CONVENTION, Finding 0010 example]:

```
V 2.1 → I 1.1.0.1.0.2   (link ISA)
V 1.1..1.16 → I 2.1.0.5.0... (permascroll text)

retrieve_contents(specset covering both):
  link ISA 1.1.0.1.0.2 → permascroll lookup → NULL/garbage
  permascroll addrs    → valid text bytes
  Result: corrupt mixed output, no error
```

### Why there is no automatic 1.x restriction

`acceptablevsa()` in `do2.c:110-113` unconditionally returns `TRUE` [PRE-INSERT, PRE-RETRIEVE-CONTENTS, INV-SUBSPACE-CONVENTION] — the subspace validation stub was never implemented. There is no filter step between `specset2ispanset` and `ispanset2vstuffset`.

This is documented as a **missing precondition**: the spec *should* require text-subspace-only input for retrieve operations, but the implementation accepts any V-address and degrades silently [PRE-RETRIEVE-CONTENTS, FC-SUBSPACE].

### Summary

| Input V-span | I-address type | `ispanset2vstuffset` result |
|---|---|---|
| `1.x` (text) | Permascroll address | Valid content bytes |
| `2.x` (link, internal) | Link orgl ISA | NULL or garbage bytes |

Delivery is **not restricted to `1.x`**. The implementation returns whatever the permascroll lookup yields for the given I-address — valid bytes for permascroll addresses, garbage/NULL for link ISAs — silently, without error [PRE-RETRIEVE-CONTENTS, INT-LINK-RETRIEVAL, EC-RETRIEVE-VSPANSET-BOTH-SUBSPACES].

---

## Code Exploration

Now I have everything I need. Let me compile the full, cited answer.

---

## Answer: What `doretrievev` Returns When a SpecSet Crosses into Link Subspace (2.x)

The short answer: **content delivery does return link-orgl I-address items (ADDRESSID) when the SpecSet crosses into the 2.x link subspace**. Delivery is not restricted to text only. Here is the complete trace through the code.

---

### 1. Entry Point

`fns.c:175-187` — `retrievev()` dispatches:

```c
void retrievev(typetask *taskptr)
{
  typespecset specset;
  typevstuffset vstuffset;
    if (
       getretrievev (taskptr, &specset)
    && doretrievev (taskptr, specset, &vstuffset))
        putretrievev (taskptr, &vstuffset);
```

---

### 2. `doretrievev` — No Subspace Filter

`do1.c:338-346`:

```c
bool doretrievev(typetask *taskptr, typespecset specset, typevstuffset *vstuffsetptr)
{
  typeispanset ispanset;
    return
       specset2ispanset (taskptr, specset, &ispanset, READBERT)
    && ispanset2vstuffset (taskptr, granf, ispanset, vstuffsetptr);
}
```

**No filtering here.** The specset is passed as-is into `specset2ispanset`. Compare this to `doshowrelationof2versions` at `do1.c:428-449`, which explicitly calls `filter_specset_to_text_subspace()` before proceeding. That filter (`do1.c:386-426`) strips V-spans with `stream < 1.0`. The retrieve path omits that call entirely.

---

### 3. `specset2ispanset` → POOM Permutation on the V-Axis

`do2.c:14-46` — iterates the specset and for each `VSPECID`:

```c
findorgl (taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)
&& (ispansetptr = vspanset2ispanset (taskptr, docorgl, ((typevspec *)specset)->vspanset, ispansetptr))
```

`vspanset2ispanset` in `orglinks.c:397-402`:

```c
typeispanset *vspanset2ispanset(typetask *taskptr, typeorgl orgl, typevspanset vspanptr, typeispanset *ispansetptr)
{
  typespanset *permute();
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
}
```

`permute` calls `span2spanset` for each span, which calls `retrieverestricted` (`orglinks.c:425-453`). `retrieverestricted` in `retrie.c:56-85` invokes `retrieveinarea` → `findcbcinarea2d`, which walks the POOM (a 2D enfilade) and finds every crum whose V-extent intersects the requested V-span — including crums in the link subspace.

There is **no V-axis guard that skips 2.x crums**. `crumqualifies2d` (`retrie.c:270-305`) only checks whether the crum's intervals intersect the query spans; it has no concept of subspace identity.

---

### 4. Link Crums in the POOM at V ≥ 2.x

When a link is created, `docreatelink` (`do1.c:195-221`) calls `findnextlinkvsa` (`do2.c:151-167`):

```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // firstlink = [2]
tumblerincrement (&firstlink, 1, 1, &firstlink);  // firstlink = [2,1]
```

The link's ISA is then placed in the document POOM at V-address `2.1` or beyond via `insertpm`. The boundary is enforced by `findvsatoappend` (`orglinks.c:29-49`):

```c
tumblerclear (&linkspacevstart);
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);  // linkspacevstart = [2]
```

Any crum with V-displacement in the 2.x range is a link reference. `islinkcrum` (`orglinks.c:255-261`) identifies them by their V-displacement pattern (used only in `maxtextwid` for `retrievevspansetpm`, not in the retrieve path).

So when a V-span overlaps 2.x, the POOM walk **finds link crums** and translates them to I-spans — specifically the ISAs of link orgls as stored in the granfilade.

---

### 5. `ispanset2vstuffset` → `ispan2vstuffset`

`granf1.c:58-74`:

```c
bool ispanset2vstuffset(typetask *taskptr, typegranf granfptr, typeispanset ispanset, typevstuffset *vstuffsetptr)
{
    *vstuffsetptr = NULL;
    for (; ispanset; ispanset = ispanset->next) {
        vstuffsetptr = ispan2vstuffset (taskptr, granfptr, ispanset, vstuffsetptr);
    }
```

`ispan2vstuffset` (`granf2.c:286-318`) calls `retrieveinspan` on the granfilade, then iterates contexts:

```c
for (temp = context; temp; temp = temp->nextcontext) {
    if (context2vstuff (taskptr, temp, ispanptr, &vstuffset)) {
        *vstuffsetptr = vstuffset;
        vstuffsetptr = (typevstuffset *)&((typeitemheader *)vstuffset)->next;
    }
}
```

---

### 6. `context2vstuff` — The Fork: TEXTID vs ADDRESSID

`context.c:240-275`:

```c
bool context2vstuff(typetask *taskptr, typecontext *context, typeispan *ispanptr, typevstuffset *vstuffsetptr)
{
    contextinfotype = context->contextinfo.granbottomcruminfo.infotype;
    if (contextinfotype != GRANTEXT && contextinfotype != GRANORGL)
        return (FALSE);
    switch (contextinfotype) {
      case GRANTEXT:
        vstuffset = (typevstuffset) taskalloc (taskptr, sizeof (typetext));
        ((typeitemheader *)vstuffset)->itemid = TEXTID;
        context2vtext (context, ispanptr, vstuffset);
        break;
      case GRANORGL:
        vstuffset = (typevstuffset) taskalloc (taskptr, sizeof (typeaddress));
        ((typeitemheader *)vstuffset)->itemid = ADDRESSID;
        movetumbler (&context->totaloffset.dsas[WIDTH], &((typelink *)vstuffset)->address);
    }
    *vstuffsetptr = vstuffset;
    return (TRUE);
}
```

- **`GRANTEXT`** → `TEXTID` item: raw text bytes, copied from the granfilade crum's inline string.
- **`GRANORGL`** → `ADDRESSID` item: the link orgl's I-address (ISA) as a tumbler, placed directly from `context->totaloffset.dsas[WIDTH]`.

Granfilade crums for link orgls are stored as `GRANORGL` by `createorglgr` (`granf2.c:111-128`):

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
```

Their ISA positions in the granfilade are assigned by `findisatoinsertmolecule` (`granf2.c:158-181`) under the `LINKATOM` branch, which places them at `hintisa + 2 levels + 2` — a separate address range from text atoms (`hintisa + 0 levels + 1`), ensuring they land in distinct granfilade slots.

---

### 7. `acceptablevsa` Is a Stub

`do2.c:110-113`:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

No active subspace gate here. This function is called in `docopy` (`do1.c:56`) but not in the retrieve path at all.

---

### Summary

| Path segment | File:line | What happens |
|---|---|---|
| `retrievev` | `fns.c:175` | Dispatches to `doretrievev` |
| `doretrievev` | `do1.c:338` | No V-filter; passes specset raw into `specset2ispanset` |
| `vspanset2ispanset` → `permute` → `retrieverestricted` | `orglinks.c:397`, `retrie.c:56` | Walks POOM with V-restriction; link crums at V≥2.x are found |
| V ≥ 2.x link crums placed by `findnextlinkvsa` | `do2.c:151` | First link at `[2,1]`; boundary at `[2]` |
| `ispanset2vstuffset` → `ispan2vstuffset` | `granf1.c:58`, `granf2.c:286` | I-spans fed into granfilade `retrieveinspan` |
| `context2vstuff` on `GRANORGL` | `context.c:264-271` | Returns `ADDRESSID` item containing the link orgl's ISA |
| Filter `filter_vspanset_to_text_subspace` | `do1.c:386` | Only called from `doshowrelationof2versions`, never from `doretrievev` |

**Delivery is not restricted to text subspace.** When a SpecSet's V-span overlaps the link subspace (V ≥ 2.x), the POOM permutation produces I-spans for the corresponding link orgls, and `context2vstuff` emits `ADDRESSID` items — the I-addresses (ISAs) of those link orgls — alongside any `TEXTID` items from the text region. No raw link-content bytes are delivered because link orgls store their endpoint structure (sporgl sets) inside the orgl's own POOM, not as inline bytes in the granfilade.
