## Question 14 [gregory]

> The storage layer is byte-opaque with one I-position per byte. Was there ever a design for variable-width content atoms (a character, a media element) that would each occupy a single I-position, or was byte-granularity always the intended resolution for the permascroll?

## KB Synthesis

Answering strictly from what I can derive from the implementation — the KB captures behavior, not design history, so I'll be clear about the limits.

**What the implementation does**

The permascroll is byte-granular at the I-address level, unconditionally [INV-SINGLE-CHAR-GRANULARITY], [SS-CONTENT-IDENTITY Finding 0034]:

- Each inserted byte receives exactly one I-address. `inserttextgr` allocates by calling `tumblerincrement(&lsa, 0, textset->length, &lsa)` — width equals byte count [ST-INSERT Finding 0031].
- V-space width equals byte count. `strlen()` gives the length field. A 4-byte UTF-8 emoji occupies 4 V-positions.
- The I-width stored in POOM bottom crums represents a byte count [SS-POOM-BOTTOM-CRUM Finding 0076].

**Storage atoms are variable-width, but addressing is not**

There is a distinction the KB makes visible: the physical storage unit `typegrantext` holds up to 950 bytes (`GRANTEXTLENGTH`) as a chunk [SS-CONTENT-IDENTITY Finding 0034]. A single INSERT call stores a block of up to 950 bytes in one gran atom. But this is an implementation convenience — the I-address range over that block is still byte-by-byte contiguous. The atom is the *allocation* unit; the byte is the *addressing* unit.

**What the KB cannot answer**

The design history question — whether variable-width character atoms (one I-position per glyph, media element, or semantic unit) were ever specified or prototyped — is not answerable from the KB. The KB extracts behavioral properties from code; it has no access to pre-implementation design documents, Nelson's original spec language, or any design decisions that were considered but not built.

What I can say: there is *no evidence in the code* of any variable-width atom design. No type tags, no multi-byte-character boundary logic, no encoding metadata. The system treats content as `seq<byte>` throughout, and the byte granularity appears structural rather than an oversight (it's what `strlen`, `movmem`, `GRANTEXTLENGTH` all reinforce). If a variable-width atom design existed, it left no trace in the implementation.

---

## Code Exploration

---

## Answer: Byte-Granularity, Atomic Links, and the Unresolved Design Seam

Reading the source directly, I find two coexisting models inside udanax-green that make this question sharper than a simple yes/no.

---

### What the code does now: TEXTATOM is byte-granular

`inserttextgr` in `granf2.c:83–109` is the definitive path for all text insertion. After writing each `textset` node into the granfilade, it advances the running I-address by the raw byte count of that chunk:

```c
// granf2.c:100
tumblerincrement (&lsa, 0, textset->length, &lsa);
```

The resulting I-span width is computed at `granf2.c:106` as the tumbler difference between `lsa` (final) and `spanorigin` (initial). The permascroll records one I-position per byte. There is no character-level or element-level re-encoding happening here; `textlength` is a plain `unsigned` count of raw bytes (`wisp.h:77`: `unsigned textlength`), and `movmem` copies that many bytes verbatim (`granf2.c:98`).

So for text: **one I-position = one byte, always.**

---

### But LINKATOM already embodies a different model

Links are created through `tumbler2spanset` (`do2.c:48–61`), which builds the I-span for a link atom:

```c
// do2.c:58
tumblerincrement (&spanptr->width, tumblerlength (tumblerptr)-1/*zzzzz*/, 1, &spanptr->width);
```

The `/*zzzzz*/` is a developer uncertainty marker — it appeared also at `do2.c:41` (`/*zzz ... */`) on a commented-out null assignment. Here it marks the width calculation as known-provisional: the width is `1` at mantissa position `tumblerlength(address)-1`, which is the finest-grained unit at that tumbler depth — effectively "one logical point" rather than one byte.

A LINKATOM's I-address is allocated in `findisatoinsertmolecule` (`granf2.c:158–181`). The function partitions the I-address space by atomtype using **mantissa[2]**:

```c
// granf2.c:162
tumblerincrement (&hintptr->hintisa, 2, hintptr->atomtype + 1, &upperbound);
```

For TEXTATOM (`atomtype=1`), new text ISAs are allocated by incrementing the main counter (`mantissa[0]`) by 1 (`granf2.c:169`). For LINKATOM (`atomtype=2`), ISAs are allocated into a distinct sub-space via `mantissa[2]=2` (`granf2.c:171`):

```c
} else if (hintptr->atomtype == LINKATOM) {
    tumblerincrement (&hintptr->hintisa, 2, 2, isaptr);
```

A link gets one *address point*, not a byte sequence. It occupies a logical I-position measured at a finer tumbler mantissa level — not the same scale as bytes.

This is qualitatively different from text. A LINKATOM is the system's working model of "a content atom that is one logical unit regardless of how many bytes might back it."

---

### The ceiling: only two atom types, and it's load-bearing

`xanadu.h:144–146`:
```c
                      /* atom types - don't change these */
#define TEXTATOM  1
#define LINKATOM  2
```

The comment `/* atom types - don't change these */` is not decorative. The values 1 and 2 are arithmetic operands in `findisatoinsertmolecule` — they are added directly to tumbler mantissa positions to carve out address subspaces. Changing or adding values would corrupt existing address allocation.

The validation at `do2.c:94` enforces this:
```c
|| (hintptr->atomtype > 2)
```

No `atomtype=3` (say, an image atom or audio atom) is possible without extending both the address arithmetic and the hint validator.

---

### The `spanset2tumbler` commented-out function

Notably, `do2.c:63–76` contains a fully commented-out function:

```c
/*  bool
spanset2tumbler (taskptr, spanset, tmblptr)
...
{
    if (spanset->next || !iszerotumbler(&spanset->width))
        return (FALSE);
```

Its guard condition — returning FALSE if the span has nonzero width — treats an atom as valid only when its width **is zero**. This is the inverse of the byte-granular model: a zero-width atom is the expected case. The function was written, then abandoned. The `// SUSPECT //` annotation on line 74 (`movetumbler (&spanset->stream, tmblptr// SUSPECT //);`) marks it as doubted even when it was active. This is another artifact of the unresolved tension between "I-position = byte" and "I-position = atom."

---

### Synthesis

The code shows **two simultaneous models that were never fully reconciled**:

| Content type | I-span model | Mechanism |
|---|---|---|
| TEXTATOM | byte-granular: width = byte count | `granf2.c:100,106`, `tumblerincrement(..., 0, textset->length, ...)` |
| LINKATOM | atomic: width = 1 at finest tumbler depth | `do2.c:58`, `/*zzzzz*/` |

The byte-granular model for text was the **implemented** and **intended** resolution for the permascroll when storing character content. There is no multi-byte character encoding, no variable-width character remapping — bytes go in, byte positions come back out.

But the LINKATOM design embodies exactly the "variable-width atom" concept you are asking about: a single logical unit at one I-position, independent of byte count. The mantissa[2] partitioning infrastructure in `findisatoinsertmolecule` is extensible — atomtype 3, 4, 5 for image, audio, or other media would each get their own sub-address space. The `/* don't change these */` comment and the `> 2` ceiling in `validhint` mark the boundary where the design stopped being implemented without abandoning the extensible structure.

The `/*zzzzz*/` at `do2.c:58` is the most honest artifact: the developer who wrote the link span calculation was not certain whether a link should have any I-extent at all — zero or one? That unresolved question *is* the design seam between byte-granular permascroll and atom-granular permascroll. The code never chose a definitive answer.

**Conclusion**: Byte-granularity for text was the intended and implemented resolution. Variable-width atoms — where each logical content unit (character, media element) would occupy one I-position — existed as a structural affordance in the address arithmetic and atom-type design, instantiated only for LINKATOM, and never extended to other media types. The design anticipated it but did not finish it.
