## Question 14 [evidence]

> For a multi-byte span insertion, do the n fresh I-addresses come out contiguous and consolidate into a single I-span/granfilade leaf, matching bulk-insert behavior?

## KB Synthesis

Yes, exactly. Here's the synthesis:

**I-address allocation is contiguous by construction** [SS-ADDRESS-SPACE, Finding 0033]. `inserttextingranf` calls `findisatoinsertgr` to find the highest existing I-address, then advances by the full text length via `tumblerincrement(&lsa, 0, textset->length, &lsa)`. All n bytes receive a single contiguous range `[I_start, I_start + n)` in one allocation call — not n separate increments.

**The result is a single I-span** [SS-SPAN, Finding 0031]. The width is computed as `tumblersub(endAddr, startAddr)`, so the entire insertion is represented as one `typeispan` with `stream = I_start` and `width = n`.

**Granfilade storage** [SS-GRAN-BOTTOM-SINGLETON, SS-ENFILADE-BRANCHING]. The granfilade's `MAXBCINLOAF = 1` means each height-0 crum holds one text atom (up to 950 bytes, `GRANTEXTLENGTH`). A single bulk insert of ≤950 bytes lands in exactly one bottom crum. Larger inserts would produce multiple bottom crums, but each crum's content still occupies a contiguous I-span.

**DOCISPAN creation confirms single-span treatment** [SS-DOCISPAN, Finding 0047]. `insertspanf` iterates over the ispanset linked list and makes one `insertnd` call per `typeispan`. Since bulk insert produces one I-span, it creates exactly 1 DOCISPAN entry — identical to the single-character sequential case once I-addresses consolidate.

**Sequential single-character inserts are equivalent** [Finding 0033]. Ten separate single-character inserts allocate I.1–I.10 (each call advances from the prior maximum), and `vspanset2ispanset` later consolidates them into 1 I-span of width 10 — same structure as a single 10-byte bulk insert.

**Caveat**: CREATELINK between two text inserts breaks contiguity [ST-CRUM-BOUND, Finding 0063], because link orgl allocation consumes I-address space from the same monotonic sequence, producing a gap in the text-only subsequence.

---

## Code Exploration

Here is my complete answer based on reading the source code directly.

---

## Multi-Byte Insertion: I-Address Contiguity and Consolidation

**Short answer:** Yes. A multi-byte insert allocates **one starting I-address**, increments by the full byte count, and returns a **single I-span** covering all bytes. This is identical to bulk-insert behavior because it _is_ bulk-insert behavior — there is no per-byte path.

---

### Call Chain: Inserting "hello" (5 bytes)

#### `fns.c` — Entry point

`insert()` at `fns.c:84–98` calls `doinsert` with the full `textset` struct (not individual bytes):

```c
(void) getinsert (taskptr, &docisa, &vsa, &textset);
putinsert (taskptr);
if (!doinsert (taskptr, &docisa, &vsa, textset))
```

#### `do1.c:doinsert()` — No per-byte loop here

`do1.c:87–123`. The function calls `inserttextingranf()` **once**, passing the entire textset. No byte-level iteration exists at this layer:

```c
ret = (inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
    && docopy (taskptr, docisaptr, vsaptr, ispanset)
);
```

#### `granf1.c:inserttextingranf()` — Thin wrapper

`granf1.c:44–47` delegates immediately to `granf2.c`:

```c
return (inserttextgr (taskptr, granfptr, hintptr, textset, ispansetptr));
```

#### `granf2.c:inserttextgr()` — Where I-addresses are born

This is the key function, `granf2.c:83–109`:

```c
if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))
    return (FALSE);
movetumbler (&lsa, &spanorigin);           // save start address
for (; textset; textset = textset->next) {
    locinfo.granstuff.textstuff.textlength = textset->length;
    movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);
    insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
    tumblerincrement (&lsa, 0, textset->length, &lsa);  // advance by N, not 1
}
ispanptr->stream = spanorigin;
tumblersub (&lsa, &spanorigin, &ispanptr->width);  // width = end - start
*ispansetptr = ispanptr;
```

Three facts fall directly out of this:

| Fact | Evidence |
|------|----------|
| One starting I-address allocated | `findisatoinsertgr()` called **once**, at `granf2.c:92` |
| Advance is by full byte count, not 1 | `tumblerincrement(&lsa, 0, textset->length, &lsa)` at `granf2.c:100` |
| Single I-span returned | One `ispanptr` built at `granf2.c:102–107`; `width = lsa − spanorigin` |

For "hello": if `spanorigin = X`, then after the loop `lsa = X+5`, and the returned span is `{stream: X, width: 5}`.

#### `granf2.c:findisatoinsertmolecule()` — How the start address is chosen

`granf2.c:158–181`. For TEXTATOM (the text content type), it finds the highest existing I-address below the document boundary and increments by 1:

```c
} else if (hintptr->atomtype == TEXTATOM) {
    tumblerincrement (&lowerbound, 0, 1, isaptr);   // granf2.c:169
```

This produces one new starting tumbler, contiguous with previously allocated text I-addresses for the same document.

#### `tumble.c:tumblerincrement()` — Sequential address arithmetic

`tumble.c:599–623`. Adds `bint` directly to the least-significant mantissa place:

```c
cptr->mantissa[idx + rightshift] += bint;
tumblerjustify (cptr);
```

A call with `bint=5` advances the tumbler by 5 in one operation. A call with `bint=1` advances by 1. The `rightshift=0` case used by `inserttextgr` operates on the lowest digit — so successive text inserts fill `.1`, `.2`, `.3`, … at the deepest level.

#### `spanf1.c:insertspanf()` — Spanfilade entry

`spanf1.c:15–54`. Iterates over the ispanset (which contains **one** ispan for a single insert), extracts `stream` and `width`, and calls `insertnd()` **once**:

```c
movetumbler (&((typeispan *)sporglset)->stream, &lstream);
movetumbler (&((typeispan *)sporglset)->width, &lwidth);
...
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

One call, one spanfilade leaf entry, covering the entire N-byte range.

---

### Answer to the Question

**Yes, fully.** For a multi-byte span insertion:

1. **Contiguous I-addresses:** `inserttextgr` allocates one starting I-address (`findisatoinsertgr`, `granf2.c:92`), then advances `lsa` by the full byte count (`tumblerincrement(..., textset->length, ...)`, `granf2.c:100`). The N bytes occupy I-addresses `[X, X+N)` — a contiguous range.

2. **Single I-span / granfilade leaf:** A single `typeispan` struct is constructed (`granf2.c:102–107`) with `stream=X` and `width=N`. No per-byte spans are created. `insertspanf` inserts this as one unit.

3. **Matches bulk-insert behavior:** There is no separate "bulk" path vs. "per-byte" path. `inserttextingranf` is always called once with the full `textset`. What the question calls "bulk-insert behavior" is simply what the code always does — the loop in `inserttextgr` iterates over `textset->next` chains (multiple distinct text segments in one request), not over individual bytes within a segment.
