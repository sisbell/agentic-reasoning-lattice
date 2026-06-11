## Question 2 [evidence]

> In the udanax-green find-links request format, is an empty type specification structurally identical to an omitted/NOSPECS type slot (so the slot is simply not consulted in the intersection), or can a caller supply a present-but-empty type spec that, like Q7's vacuously-resolving slot, short-circuits the find to the empty link-set — i.e., does the encoding make the abstract `Θ = ∅` request expressible at all?

## KB Synthesis

## Structural Distinction: NOSPECS vs Empty Specset in find-links

The KB allows a reasonably confident answer on the structural question, though it leaves the wire-format encoding ambiguous and the type-slot behavior complicated by a known bug.

---

### The implementation handles them as distinct cases

At the C level, NOSPECS threads through as a **NULL sporglset pointer**, while an empty specset converts via `specset2ispanset` / `vspanset2sporglset` to a **non-NULL but zero-element linked list**. The intersection function `intersectlinksets()` — described in [SS-FIND-LINKS] as an "O(n\*m) or O(n\*m\*p) intersection" over the three endpoint dimensions — branches on these differently:

- **NULL (NOSPECS)**: that dimension is not entered into the intersection; any link qualifies on that axis. [ST-FIND-LINKS, Finding 0029] formalises this as the AND-semantics asymmetry: `find_links(spec, NOSPECS)` returns all links whose source endpoint intersects `spec`, regardless of target or type.
- **Empty list**: `I-addresses(∅) = ∅`; intersecting any set with ∅ = ∅; result is the empty link set. The O(n\*m\*0) = O(0) case trivially short-circuits.

So the abstract request **Θ = ∅** (find links whose type endpoint intersects the empty set) *is* structurally representable and would produce the mathematically correct empty result — for the right reason — if the protocol permits encoding a present-but-empty third-slot specset distinct from the NOSPECS sentinel.

---

### The type-slot is already broken for non-NOSPECS values

This is where the practical picture complicates things. [EC-TYPE-FILTER-NONFUNCTIONAL] documents that `find_links(source, NOSPECS, type_spec)` returns `[]` even when `find_links(source)` returns the same links. The KB attributes this to the type I-addresses (VSpec references into the bootstrap document's type subspace at `1.0.2.x`, per [SS-LINK-ENDPOINT] Finding 0024) not intersecting correctly with whatever is indexed in the spanfilade for those links' type endsets.

Consequence: at present, the observable output is the same whether you pass:
- a valid `QUOTE_TYPE` specset → empty (broken)
- a present-but-empty type specset → empty (correct, wrong reason)

The only observably *different* behaviour comes from NOSPECS vs anything-else — not from a valid type spec vs an empty one.

---

### The orgl-dimension quirk does not affect span-dimension filtering

[EC-FIND-LINKS-GLOBAL] / [PRE-FIND-LINKS] (Finding 0069) notes that the orgl-range parameter is globally overridden by the `TRUE||!homeset` guard in `sporglset2linkset`. This bypasses orgl-dimension scoping but does **not** affect the span-dimension (I-address content) intersection that NOSPECS vs empty-specset governs. The two bugs are orthogonal.

---

### Summary

| Slot value | Span-dimension semantics | Current type-slot output |
|---|---|---|
| NOSPECS (NULL) | Dimension skipped; no filter | Links found on other dimensions |
| Valid type specset | Intersect; filter to matching types | Empty (EC-TYPE-FILTER-NONFUNCTIONAL) |
| Present-but-empty specset | Intersect with ∅ = ∅; vacuously false | Empty (correct reason) |

The **Θ = ∅** request is expressible if the FEBE wire format permits encoding a present-but-empty specset in the third slot (the KB does not document the wire format directly, so this is the remaining uncertainty). If it is encodable, the implementation would produce an empty result via the correct `∅ ∩ anything = ∅` path rather than via the bug that makes valid type specs return empty. But since both non-NOSPECS values currently produce empty, the caller cannot distinguish the two causes from the outside. NOSPECS and an empty specset are **not** structurally identical: one suppresses the constraint entirely while the other makes the constraint vacuously unsatisfiable.

---

## Code Exploration

I have the complete picture. Here is the full traced answer.

---

## Answer: Empty Type Spec vs. NOSPECS in `find_links`

**Short answer:** The encoding makes `Θ = ∅` inexpressible. An empty type specset and an omitted/NOSPECS type specset are structurally identical at every layer — wire format, parser output, and C execution guard. Both are treated as "slot not consulted." The code path that returns `∅` exists, but it is only reachable through a runtime miss, never through a vacuously-empty encoding.

---

### Layer 1 — Wire encoding (`client.py:543–553`)

`NOSPECS = SpecSet([])` is defined at `client.py:581`. When `find_links` is called, both `targetspecs=None` and `typespecs=None` are substituted with `NOSPECS` before sending:

```python
# client.py:751-754
if targetspecs is None: targetspecs = NOSPECS
if typespecs is None:   typespecs   = NOSPECS
...
self.xc.command(30, sourcespecs, targetspecs, typespecs, homedocids)
```

`SpecSet.write` serializes the count, then each item:

```python
# client.py:543-553
def write(self, stream):
    stream.write("%d~" % (len(self.specs)))   # "0~" for empty list
    for spec in self.specs:                   # never iterates for []
        ...
```

So `SpecSet([])` produces exactly `"0~"` on the wire — one byte for the count, one delimiter, no items.

---

### Layer 2 — Wire parsing (`get2fe.c:147–180`)

```c
// get2fe.c:147-180
bool getspecset(typetask *taskptr, typespecset *specsetptr)
{
  INT num;
  *specsetptr = NULL;               // line 154: always initialised to NULL
  if (!getnumber (taskptr, &num)) {
      return (FALSE);
  }
  if (num == 0)
      return (TRUE);                // line 158-159: immediate return, pointer stays NULL
  while (num--) {
      ...
  }
  return (TRUE);
}
```

When the wire count is `0`, execution hits the `return (TRUE)` at line 159 immediately, leaving `*specsetptr = NULL`. The exact same outcome occurs whether the caller sends `NOSPECS` (`SpecSet([])`) or the slot was never populated at all — **both produce a C `NULL` pointer.**

The `get1.c` version (interactive/non-FE path, `get1.c:110–125`) calls the same `getspecset` function and behaves identically.

---

### Layer 3 — `findlinksfromtothreesp` (`spanf1.c:56–103`)

This is where the null-pointer test determines whether the slot is consulted:

```c
// spanf1.c:69-102
fromlinkset = tolinkset = threelinkset = NULL;

if (fromvspecset)                              // line 70 — null-pointer guard
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)                                // line 72
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)                             // line 74 — TYPE slot guard
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) { ... }                      // line 76
if (tovspecset)   { ... }                      // line 84
if (threevspecset) {                           // line 92 — TYPE slot guard again
    sporglset2linkset(taskptr, (typecuc*)spanfptr, threesporglset,
                      &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) {
        *linksetptr = NULL;                    // line 95: Θ = ∅ path
        return (TRUE);
    }
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr); // line 100
```

`if (threevspecset)` is a C null-pointer test. Since both an empty specset and an omitted specset produce `threevspecset = NULL`, **the entire type-slot block is unconditionally skipped** in both cases. `threelinkset` stays `NULL`.

---

### Layer 4 — Intersection (`spanf2.c:46–120`)

```c
// spanf2.c:63-79
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;                  // line 64-65
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3)
    *linkset4ptr = linkset3;
else
    *linkset4ptr = NULL;                      // line 71
```

With `threelinkset = NULL` (type slot not consulted), `fromlinkset` populated from the source specset, and `tolinkset = NULL`: the first branch fires, returning `fromlinkset` directly. The null type-linkset contributes nothing to the intersection — it is not subtracted, not filtered, not treated as an empty constraint.

---

### What does the Θ = ∅ path at `spanf1.c:94–98` actually mean?

The path `*linksetptr = NULL; return (TRUE);` at line 95 **is** reachable, but only when:
1. `threevspecset` is **non-NULL** (type slot was populated with at least one item)
2. `sporglset2linkset` walks the spanfilade for those type spans and finds **no stored links** touching them

That is a runtime miss — the caller sent a real type address that happened to match nothing. It is not a vacuous Θ = ∅ from sending an empty set.

---

### Conclusion

| What the caller sends | Wire bytes | C pointer after parse | Type slot consulted? | Result |
|---|---|---|---|---|
| `typespecs=None` | `0~` | `NULL` | No | Type skipped in intersection |
| `typespecs=SpecSet([])` (NOSPECS) | `0~` | `NULL` | No | Type skipped in intersection |
| `typespecs=SpecSet([real_span])` with no matching links | `1~ v~ ...` | non-NULL | Yes, runtime miss → ∅ | Returns ∅ |

**The abstract `Θ = ∅` request — "type constraint is present but vacuously empty, force the result to ∅" — is not expressible.** The protocol encodes specset absence as count=0 (`"0~"`), and the parser collapses count=0 to `NULL`. The `if (threevspecset)` guard then skips the slot entirely. There is no encoding for "a specset with zero members that should nonetheless be treated as an active empty filter." A caller who wants `∅` must achieve it either through a source specset that matches nothing, or by relying on runtime spanfilade misses — neither of which is the vacuous Θ = ∅ path.
