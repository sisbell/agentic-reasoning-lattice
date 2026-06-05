## Question 18 [evidence]

> Given INV-BYTE-OPAQUE, does retrieving a VSpec whose boundaries fall mid-character return split partial UTF-8 bytes without any encoding correction?

## KB Synthesis

Yes. The system returns the raw split bytes with no encoding correction or error.

[SS-CONTENT-IDENTITY] Finding 0034 establishes the foundational property: content is stored as `seq<byte>`, not `seq<char>`. The storage unit is `typegrantext` with a `char textstring[950]` byte buffer, length tracked via `strlen()` (byte count), and retrieval done via `movmem` — a raw `memmove` with no encoding interpretation.

[INV-SINGLE-CHAR-GRANULARITY] Finding 0034 confirms that V-space width equals byte count, not character count. Each byte position receives its own I-space address. A 2-byte UTF-8 sequence occupies two independent V-positions with two distinct I-addresses.

[EC-ENCODING-BOUNDARY-SPLIT] states this explicitly: retrieving a sub-range that straddles a multi-byte character boundary returns the byte subsequence as-is. Their concrete example:

```
Content: "caf\xc3\xa9" (5 bytes, UTF-8 "café")
Retrieve V-span [1.1, 1.4]: Returns "caf\xc3"  — invalid UTF-8
Retrieve V-span [1.5, 1.5]: Returns "\xa9"      — invalid UTF-8 continuation byte
```

No precondition in [PRE-RETRIEVE-CONTENTS] or [PRE-SPECSET] checks encoding boundaries. The backend has no concept of character boundaries — V-addresses are byte offsets.

[INT-TRANSCLUSION] Finding 0034 further notes this property propagates through transclusion: transcluded content inherits whatever encoding the source had, and mixed encodings within a document are possible.

The note referenced as `INV-BYTE-OPAQUE` in your question is covered by this cluster — it is a design property, not a bug.

---

## Code Exploration

I have all the evidence. Here is the full answer.

---

## INV-BYTE-OPAQUE: Mid-Character UTF-8 Retrieval

**Answer: Yes.** The backend returns raw split bytes with no encoding correction of any kind. Every layer of the retrieval path operates on byte offsets.

---

### 1. The I-space address system is byte-indexed

In `granf2.c:95-101`, `inserttextgr` stores text and advances the granfilade address by the raw byte count:

```c
locinfo.granstuff.textstuff.textlength = textset->length;
movmem(textset->string, locinfo.granstuff.textstuff.textstring,
       locinfo.granstuff.textstuff.textlength);
insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
tumblerincrement (&lsa, 0, textset->length, &lsa);  // byte count advance
```

`textlength` is typed `unsigned` [`wisp.h:77`] and `textstring` is `char[GRANTEXTLENGTH]` [`wisp.h:76`] where `GRANTEXTLENGTH = 950` [`common.h:115`]. The tumbler address space is one unit per byte — there is no character layer.

---

### 2. Content clipping is pure byte arithmetic

`context2vtext` in `context.c:277-309` performs the clip that limits returned content to the requested ispan:

```c
// context.c:286
tumblerincrement (&crumistart, 0,
    (INT)context->contextinfo.granbottomcruminfo.granstuff.textstuff.textlength,
    &crumiend);                              // textlength is bytes

// context.c:294-299
if (tumblercmp (&crumistart, &ispanstart) == LESS) {
    i = tumblerintdiff (&ispanstart, &crumistart);  // byte offset to skip
    vtlength -= i;
}
// context.c:301-305
if (tumblercmp (&crumiend, &ispanend) == GREATER) {
    vtlength -= tumblerintdiff (&crumiend, &ispanend);  // byte clip from end
}
// context.c:308
movmem (&context->contextinfo...textstring[i],
        ((typetext *)vstuffset)->string, ((typetext *)vstuffset)->length);
```

`tumblerintdiff` at `tumble.c:591-597`:

```c
INT tumblerintdiff(tumbler *aptr, tumbler *bptr)
{
  tumbler c;
    tumblersub (aptr, bptr, &c);
    return (c.mantissa[0]);          // raw integer — no character semantics
}
```

The byte offset `i` and the clipped `vtlength` are both plain integer byte counts. Then `movmem` copies exactly those bytes into the output buffer — no UTF-8 validation, no alignment adjustment.

---

### 3. The FEBE wire protocol emits raw bytes

`puttext` in `putfe.c:208-219`:

```c
int puttext(typetask *taskptr, typetext *textptr)
{
    xuputc (TEXTFLAG, taskptr->outp);
    putnumber (taskptr->outp, textptr->length);     // byte count
    for (i = 0; i < textptr->length; ++i)
            xuputc (textptr->string[i], taskptr->outp);  // each byte
}
```

`putretrievev` at `putfe.c:270-275` calls `putitemset` which calls `puttextset` → `puttext`. The protocol frame carries `textptr->length` (bytes) followed by those bytes verbatim.

---

### 4. No UTF-8 awareness exists in the codebase

A search across all backend source for `utf`, `unicode`, `charset`, `encoding`, `multibyte`, `wchar` returns zero relevant matches. The concept does not exist in this codebase.

---

### Conclusion

The V→I mapping (`vspanset2ispanset → permute → span2spanset → retrieverestricted`) resolves VSpec boundaries to byte-exact I-space coordinates. `context2vtext` then clips the raw crum bytes at those byte boundaries and copies the result verbatim. `puttext` sends those bytes over the FEBE connection unchanged.

If a VSpec boundary falls within a multi-byte UTF-8 sequence — for example, byte 1 of a 3-byte `€` (`0xE2 0x82 0xAC`) — the backend returns the leading `0xE2` byte (or trailing `0x82 0xAC`) with no error, no signal, and no correction. The INV-BYTE-OPAQUE invariant holds: the backend treats content as an opaque byte sequence throughout, and that opacity extends unconditionally to the FEBE client.
