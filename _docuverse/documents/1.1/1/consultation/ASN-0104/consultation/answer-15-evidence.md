## Question 15 [evidence]

> For a multi-byte UTF-8 character spanning several I-positions, can a partial-width read return a fractured byte sequence that splits the character, and does the backend make any attempt to align reads to character boundaries?

## KB Synthesis

Yes, and no — definitively answered by the KB.

**Partial reads can and do fracture multi-byte encodings.** [EC-ENCODING-BOUNDARY-SPLIT] documents this explicitly:

> Retrieving a sub-range of a V-span that straddles a multi-byte character boundary returns byte sequences that are invalid in the original encoding.

The concrete example given: content `"caf\xc3\xa9"` (5 bytes, UTF-8 café). Retrieving V-span [1.1, 1.4] returns `"caf\xc3"` — the first byte of a two-byte sequence without its continuation.

**The backend makes zero attempt at character boundary alignment.** Three properties combine to make this structural:

1. **Byte-level addressing** [INV-SINGLE-CHAR-GRANULARITY, SS-CONTENT-IDENTITY/Finding 0034]: Each byte receives exactly one I-space address. V-space positions are 1:1 with bytes. Width equals byte count, not character count.

2. **Encoding-opaque retrieval** [SS-CONTENT-IDENTITY/Finding 0034]: `movmem` (`memmove`) performs raw byte copies with no encoding interpretation. `strlen()` returns byte count. The system stores, copies, and retrieves raw bytes unconditionally.

3. **No boundary validation anywhere** [EC-ENCODING-BOUNDARY-SPLIT]: "The backend performs no character boundary validation on any operation." This is not an omission — it is the design. The formal content type is `seq<byte>`, not `seq<char>`.

The consequence for spec: any precondition or postcondition involving retrieval width operates in bytes. A frontend wanting character-safe retrieval must manage encoding boundaries itself; the backend provides no assistance.

---

## Code Exploration

I have everything I need. Here is the complete analysis:

---

## UTF-8 Boundary Alignment in udanax-green: A Direct Code Reading

**Short answer:** Yes, a partial-width read can absolutely return a fractured byte sequence that splits a multi-byte UTF-8 character. The backend makes no attempt whatsoever to align reads to character boundaries. Every claim below is cited to specific source lines.

---

### 1. How Text Is Stored: Plain Bytes, No Encoding Metadata

The fundamental storage type is declared in `backend/wisp.h:74-78`:

```c
/* typegrantext */
typedef struct structgrantext {
        char textstring[GRANTEXTLENGTH];
        unsigned textlength;
} typegrantext;
```

`textstring` is a plain signed `char` array. `textlength` is an unsigned byte count. There is no encoding field, no code-point count, no flag — just raw bytes. `GRANTEXTLENGTH` is 950 bytes (`backend/common.h:115`).

---

### 2. How Text Is Written In: Byte-Count Advancement

When text is inserted, `inserttextgr()` at `backend/granf2.c:83-109` stores bytes and advances the I-space address by the raw byte count:

```c
locinfo.granstuff.textstuff.textlength = textset->length;          // line 97
movmem(textset->string, locinfo.granstuff.textstuff.textstring,    // line 98
       locinfo.granstuff.textstuff.textlength);
insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);                  // line 99
tumblerincrement(&lsa, 0, textset->length, &lsa);                  // line 100
```

`tumblerincrement` steps the I-space address by `textset->length` bytes. A 3-byte UTF-8 character occupies I-positions N, N+1, N+2. There is no concept of "character" at this layer — every byte gets its own I-position.

---

### 3. How Granule Packing Splits at Arbitrary Byte Offsets

When a granule approaches the 950-byte limit, `fillupcbcseq()` at `backend/insert.c:75-103` packs bytes until it hits `GRANTEXTLENGTH` exactly:

```c
remainingroom = GRANTEXTLENGTH - crumlength;                       // line 83
textlength = info->granstuff.textstuff.textlength;                 // line 84

if (remainingroom > textlength) {
    movmem(…, textlength);                                         // line 87: fits entirely
} else {
    movmem(…, remainingroom);                                      // line 92: fill to 950 exactly
    ptr->cinfo.granstuff.textstuff.textlength = GRANTEXTLENGTH;    // line 93
    tumblerincrement(crumboundary, 0, remainingroom, crumboundary); // line 94
}
info->granstuff.textstuff.textlength -= remainingroom;             // line 97 — remainder goes to next granule
```

If a 3-byte UTF-8 character starts at byte 949 of a granule, bytes 1–2 land in the current granule and byte 3 overflows into the next. The split point is determined purely by `GRANTEXTLENGTH - crumlength` with no look-ahead for continuation bytes.

---

### 4. How Partial-Width Reads Return Arbitrary Byte Windows

The critical function is `context2vtext()` at `backend/context.c:277-309`. Given a requested I-span that overlaps a granule, it:

**Step 1 — compute byte offset `i` into `textstring`:**
```c
if (tumblercmp(&crumistart, &ispanstart) == LESS) {          // line 294
    i = tumblerintdiff(&ispanstart, &crumistart);             // line 298
    vtlength -= i;                                            // line 299
}
```
`tumblerintdiff` returns a raw integer difference between two tumblers — a byte count. `i` is the byte offset into the granule's `textstring` where the requested span begins. No alignment rounding, no look-back for a lead byte.

**Step 2 — trim the end by raw byte count:**
```c
if (tumblercmp(&crumiend, &ispanend) == GREATER) {           // line 301
    vtlength -= tumblerintdiff(&crumiend, &ispanend);         // line 305
}
```
Same arithmetic, same result: the right edge is clipped at an arbitrary byte position.

**Step 3 — raw `movmem` copy:**
```c
movmem(&context->contextinfo.granbottomcruminfo.granstuff.textstuff.textstring[i],
       ((typetext *)vstuffset)->string,
       ((typetext *)vstuffset)->length);                      // line 308
```

This is a byte-for-byte memory copy starting at offset `i`. If `i` points into the middle of a UTF-8 multi-byte sequence, the copy begins with a continuation byte (0x80–0xBF), producing an invalid sequence. The result will not be valid UTF-8.

---

### 5. Exhaustive Search for UTF-8 Awareness

A search across all C source files in `backend/` for any of these patterns returns nothing relevant:

- `0x80`, `0xC0`, `0xE0`, `0xF0` — bit masks for detecting UTF-8 lead/continuation bytes
- `utf`, `UTF`, `unicode`, `Unicode`, `multibyte`, `multi-byte`, `char.bound`

There are zero occurrences. The word "character" does not appear in any comment or variable name in the retrieval path.

---

### Conclusion

The backend treats content as an opaque byte stream at every layer:

| Layer | Evidence |
|-------|----------|
| Storage | `char textstring[950]` with a byte-count `textlength` — `backend/wisp.h:75-77` |
| Insertion | I-space advanced by `textset->length` bytes — `backend/granf2.c:100` |
| Granule packing | Split at exactly byte 950, no look-ahead — `backend/insert.c:92-94` |
| Retrieval clipping | `i = tumblerintdiff(…)` raw byte offset, `movmem(&textstring[i], …)` — `backend/context.c:298,308` |
| UTF-8 awareness | None — no masking, no lead-byte detection anywhere in the backend |

A partial-width read requesting bytes N through M will return exactly bytes N through M — even if N falls in the middle of a 2-, 3-, or 4-byte UTF-8 sequence. The fractured sequence will arrive at the client with no error, no indication, and no padding. The client receives invalid UTF-8 and must handle it (or fail) on its own.

This is not a bug in the sense that the system was ever designed for a specific encoding. Udanax-green predates the UTF-8 standard (1993) by more than a decade. The I-space was designed as a universal address space for arbitrary byte sequences. The architecture is encoding-agnostic by design; UTF-8 alignment would need to be enforced by a higher layer outside the backend.
