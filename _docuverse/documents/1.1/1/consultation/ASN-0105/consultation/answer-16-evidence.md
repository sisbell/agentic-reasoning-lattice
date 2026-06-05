## Question 16 [evidence]

> Since the granfilade is byte-opaque [INV-BYTE-OPAQUE], if a read span boundary falls mid-way through a multi-byte UTF-8 character, does the operation return the partial byte sequence as-is?

## KB Synthesis

Yes. The operation returns the partial byte sequence as-is, with no encoding awareness.

[SS-CONTENT-IDENTITY] Finding 0034 is definitive: the retrieval path uses `movmem` (aliased to `memmove`) — a raw byte copy — with no encoding conversion or character boundary checking. Length is byte count, not character count. The system has no concept of multi-byte characters; each byte occupies exactly one V-space position.

[EC-ENCODING-BOUNDARY-SPLIT] documents the exact scenario you describe:

```
Content: "caf\xc3\xa9" (5 bytes, UTF-8 "café")
Retrieve V-span [1.1, 1.4] → returns "caf\xc3"  ← invalid UTF-8, missing \xa9
Retrieve V-span [1.5, 1.5] → returns "\xa9"      ← orphaned continuation byte
```

No precondition guards against this — the backend is encoding-agnostic by design, and this applies equally to retrieval operations, link endpoint boundaries, and transclusion spans ([INT-TRANSCLUSION]). The formal type for content is `seq<byte>`, not `string` or `seq<char>`.

---

## Code Exploration

I have all the evidence needed. Here is the full answer.

---

## Byte-Boundary Clipping at Mid-Character UTF-8 Boundaries

**Short answer: Yes. The operation returns the partial byte sequence as-is. There is no UTF-8 or Unicode awareness anywhere in the retrieval path.**

---

### 1. Granfilade leaf nodes are raw byte arrays

`wisp.h:75-78`:
```c
typedef struct structgrantext {
    char textstring[GRANTEXTLENGTH];   /* raw char array, 950 bytes max */
    unsigned textlength;               /* byte count, not character count */
} typegrantext;
```

`textlength` is a byte count. `textstring` is a raw `char[]`. No character type, no encoding field.

---

### 2. Insertion maps one tumbler unit per byte

`granf2.c:98-100`:
```c
movmem(textset->string, locinfo.granstuff.textstuff.textstring,
       locinfo.granstuff.textstuff.textlength);
insertseq((typecuc*)fullcrumptr, &lsa, &locinfo);
tumblerincrement(&lsa, 0, textset->length, &lsa);
```

The tumbler `lsa` advances by `textset->length` — the raw byte count. Each byte occupies one unit in ISA address space. A 3-byte UTF-8 character like `é` (U+00E9, encoded as `0xC3 0xA9`) occupies **two consecutive tumbler addresses**, not one.

---

### 3. Retrieval clips at raw byte boundaries

`context2vtext` (`context.c:277-309`) is the function that converts a granfilade context node into the text actually returned to the caller:

```c
/* context.c:293-308 */
vtlength = context->contextinfo.granbottomcruminfo.granstuff.textstuff.textlength;
if (tumblercmp(&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff(&ispanstart, &crumistart);   /* byte offset into textstring */
    vtlength -= i;
}
if (tumblercmp(&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff(&crumiend, &ispanend); /* clip tail bytes */
}
((typetext *)vstuffset)->length = vtlength > 0 ? vtlength : -vtlength;
movmem(&context->contextinfo.granbottomcruminfo.granstuff.textstuff.textstring[i],
       ((typetext *)vstuffset)->string, ((typetext *)vstuffset)->length);
```

The clip points `i` (leading bytes skipped) and `vtlength` (total bytes kept) are computed via `tumblerintdiff`, which is:

`tumble.c:591-597`:
```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr)
{
    tumbler c;
    tumblersub(aptr, bptr, &c);
    return (c.mantissa[0]);
}
```

Pure integer subtraction of tumbler mantissa. No character boundary detection, no lookahead for multi-byte sequences.

`movmem` then copies exactly `vtlength` raw bytes starting at `textstring[i]`. If `i` or `vtlength` falls in the middle of a multi-byte UTF-8 sequence, the copy proceeds regardless.

---

### 4. Span traversal uses the same byte-granular comparison

`retrie.c:423-430` — the intersection test for which leaf crums overlap a requested span:
```c
bool crumintersectsspanseq(typecorecrum *crumptr, tumbler *offsetptr,
                            tumbler *spanstart, tumbler *spanend)
{
    ...
    return ((whereoncrum(..., spanstart, WIDTH) < ONMYRIGHTBORDER)
          && (whereoncrum(..., spanend, WIDTH) > ONMYLEFTBORDER));
}
```

`whereoncrum` (`retrie.c:345`) compares tumblers for the GRAN case as:
```c
case GRAN:
    tumbleradd(&offset->dsas[WIDTH], &ptr->cwid.dsas[WIDTH], &right);
    return (intervalcmp(&offset->dsas[WIDTH], &right, address));
```

Again: pure tumbler arithmetic, no character-awareness.

---

### 5. Conclusion

The granfilade is byte-opaque by construction [INV-BYTE-OPAQUE]:

- **Address space**: one tumbler unit per raw byte (established at insert time, `granf2.c:100`)
- **Span clipping**: computed in bytes via `tumblerintdiff` (`context.c:298`, `context.c:305`)
- **Copy**: `movmem` copies the clipped byte range verbatim (`context.c:308`)
- **No UTF-8 guard**: not in the retrieval path, not in the insertion path, not anywhere in the struct definitions

If a read span boundary (an ispan with its tumbler `stream` and `width`) falls at a byte offset that is not a valid UTF-8 character boundary, `context2vtext` will produce a `typetext` whose `string` field begins or ends with a partial byte sequence. The partial bytes are returned to the FEBE caller as-is. The protocol sends them, and the client receives them. There is no error, no truncation, no rounding to a character boundary — only raw byte fidelity.

This is the correct behavior given the architecture: the granfilade makes no commitments about the encoding of the content it stores. Encoding interpretation is a client-side concern.
